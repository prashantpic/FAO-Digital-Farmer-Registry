import logging
from .base_client import BaseApiClient
from .sms_gateway_client_interface import SmsGatewayClientInterface
from odoo.addons.dfr_integrations.dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig
from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError, IntegrationAPIError
from requests.auth import HTTPBasicAuth
from typing import Dict

_logger = logging.getLogger(__name__)

class SmsTwilioClient(BaseApiClient, SmsGatewayClientInterface):
    def __init__(self, config: SmsProviderConfig, timeout_seconds: int = 10):
        # api_key from SmsProviderConfig is used for Account SID
        # api_secret from SmsProviderConfig is used for Auth Token
        if not config.api_key or not config.api_secret:
            raise ConfigurationError("Twilio Account SID or Auth Token not configured.")
        
        # The config.api_url for Twilio should be the full base URL including the Account SID,
        # e.g., https://api.twilio.com/2010-04-01/Accounts/ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        if not config.api_url:
             # This case should ideally be handled by the service layer constructing the URL
             # or by a more specific error if the URL format from config is incorrect.
             raise ConfigurationError("Twilio API base URL (including Account SID) not configured.")

        # Initialize BaseApiClient. Note: api_key here isn't directly used by BaseApiClient's auth,
        # as Twilio uses HTTPBasicAuth. It's stored for reference if needed.
        super(BaseApiClient, self).__init__(
            base_url=config.api_url, 
            api_key=config.api_key, # Storing Account SID as api_key for BaseApiClient consistency
            timeout_seconds=timeout_seconds, 
            service_name="TwilioSMS"
        )
        # Initialize SmsGatewayClientInterface
        SmsGatewayClientInterface.__init__(self, config)
        
        # Twilio specific: HTTPBasicAuth uses Account SID and Auth Token
        self.auth = HTTPBasicAuth(self.config.api_key, self.config.api_secret)
        self.default_sender_id = None
        if self.config.extra_config and isinstance(self.config.extra_config, dict):
            self.default_sender_id = self.config.extra_config.get('default_sender_id')

    def _get_headers(self) -> Dict[str, str]:
        # Twilio uses Basic Auth for authentication, which is handled by requests' `auth` parameter.
        # The primary content type for sending messages is application/x-www-form-urlencoded.
        # We expect a JSON response from Twilio.
        return {'Accept': 'application/json'}

    def send_sms(self, request_dto: SmsSendRequest) -> SmsSendResponse:
        # Sanitize recipient for logging
        log_recipient_phone = '***' + request_dto.recipient_phone[-4:] if request_dto.recipient_phone and len(request_dto.recipient_phone) > 4 else '***'
        _logger.info(f"Sending SMS via Twilio to {log_recipient_phone}")

        payload = {
            'To': request_dto.recipient_phone,
            'Body': request_dto.message_body,
        }

        sender_id_to_use = request_dto.sender_id or self.default_sender_id
        
        if not sender_id_to_use:
            error_msg = "Twilio sender ID ('From' number/alphanumeric sender) not provided in request or default not configured."
            _logger.error(error_msg)
            return SmsSendResponse(status='failed', error_message=error_msg, raw_response={"error_text": error_msg})
        
        payload['From'] = sender_id_to_use
        
        # Log sanitized payload
        log_payload = payload.copy()
        log_payload['To'] = log_recipient_phone # Use already sanitized version
        if 'From' in log_payload and len(log_payload['From']) > 4: # Sanitize sender if it's a number
            try:
                int(log_payload['From'].replace('+', '')) # Check if numeric-like
                log_payload['From'] = '***' + log_payload['From'][-4:]
            except ValueError:
                pass # Keep alphanumeric sender as is for logs, or apply other rule

        _logger.debug(f"Twilio SMS payload (sanitized for log): {log_payload}")

        try:
            # Twilio's message creation endpoint is typically /Messages.json
            # The self.base_url should be like: https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}
            response = self.session.post(
                f"{self.base_url}/Messages.json", 
                data=payload, # Twilio expects form-encoded data
                auth=self.auth,
                headers=self._get_headers(), # Primarily for 'Accept: application/json'
                timeout=self.timeout_seconds
            )
            
            _logger.debug(f"Twilio Response: Status {response.status_code}, Content (snippet): {response.text[:200]}")

            # Twilio success is typically 201 Created (or 200 OK for some read operations)
            if response.status_code not in [200, 201]:
                 # Use BaseApiClient's error handler which can raise specific exceptions
                 self._handle_api_error(response) 
                 # If _handle_api_error doesn't raise, it implies an unexpected situation.
                 # For robustness, we'll construct a failed DTO if no exception was raised by _handle_api_error
                 # but this path should ideally not be hit if _handle_api_error is comprehensive.
                 error_details = {"error_text": f"Unhandled API error with status {response.status_code}", "response_body": response.text[:500]}
                 try:
                    error_details.update(response.json())
                 except ValueError:
                    pass
                 return SmsSendResponse(status='failed', error_message=error_details.get('message', f"Twilio API error {response.status_code}"), error_code=str(error_details.get('code', response.status_code)), raw_response=error_details)


            response_data = response.json()
            return SmsSendResponse(
                message_sid=response_data.get('sid'),
                status=response_data.get('status'), # e.g., 'queued', 'sent', 'failed', 'delivered'
                error_code=str(response_data.get('code')) if response_data.get('code') is not None else None, # Twilio error code
                error_message=response_data.get('message'), # Twilio error message for specific codes
                raw_response=response_data
            )
        except InvalidResponseError as e: # This exception would be raised by _handle_api_error
            _logger.error(f"Invalid Twilio response: {e.message}")
            raw_content = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return SmsSendResponse(status='failed', error_message=e.message, error_code=str(e.status_code), raw_response=raw_content)
        except IntegrationAPIError as e: # Other errors from BaseApiClient (timeout, auth from base, etc.)
            _logger.error(f"Twilio API Integration Error: {e.message}", exc_info=True)
            raw_content = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return SmsSendResponse(status='failed', error_message=e.message, error_code=str(e.status_code), raw_response=raw_content)
        except Exception as e:
            _logger.error(f"Unexpected error sending SMS via Twilio: {e}", exc_info=True)
            return SmsSendResponse(status='failed', error_message=f"An unexpected error occurred: {str(e)}")