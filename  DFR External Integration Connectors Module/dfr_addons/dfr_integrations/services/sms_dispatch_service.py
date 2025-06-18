import logging
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.addons.dfr_integrations.clients import (
    SmsGatewayClientInterface,
    SmsTwilioClient # Example
    # Import other clients like SmsVonageClient here
)
from odoo.addons.dfr_integrations.dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig
from odoo.addons.dfr_integrations.exceptions import IntegrationAPIError, ConfigurationError
from typing import Optional, Dict, Any

_logger = logging.getLogger(__name__)

class SmsDispatchService(models.AbstractModel):
    _name = 'dfr.sms.dispatch.service'
    _description = 'DFR SMS Dispatch Service'

    # Map provider names from config to client classes
    PROVIDER_CLIENT_MAP: Dict[str, type[SmsGatewayClientInterface]] = {
        'twilio': SmsTwilioClient,
        # 'vonage': SmsVonageClient, # Add actual providers here as they are implemented
        # 'other': CustomOtherSmsClient # If 'other' implies a specific custom client
    }

    def _get_configured_sms_client(self) -> Optional[SmsGatewayClientInterface]:
        """
        Fetches configuration and instantiates the appropriate SMS client.
        Returns None if no external provider is configured or provider is 'none'.
        Raises ConfigurationError if a provider is selected but config is invalid or client is unsupported.
        """
        ICP = self.env['ir.config_parameter'].sudo()
        provider_name = ICP.get_param('dfr_integrations.sms_gateway_provider')

        if not provider_name or provider_name == 'none':
            _logger.info("SMS Gateway provider not configured or set to 'none'. SMS will not be sent via external gateway.")
            return None

        client_class = self.PROVIDER_CLIENT_MAP.get(provider_name)
        if not client_class:
            _logger.error(f"Unsupported SMS gateway provider configured: {provider_name}")
            raise ConfigurationError(_(f"Unsupported SMS gateway provider: {provider_name}. Please check configuration."))

        # Gather config for the specific provider
        config_data: Dict[str, Any] = {'provider_name': provider_name}
        extra_config_data: Dict[str, Any] = {}

        if provider_name == 'twilio':
            config_data['api_key'] = ICP.get_param('dfr_integrations.sms_twilio_account_sid') # Account SID
            config_data['api_secret'] = ICP.get_param('dfr_integrations.sms_twilio_auth_token') # Auth Token
            # Allow Twilio API URL to be overridden, or construct if not set (client might do this)
            default_twilio_api_url = None
            if config_data['api_key']: # Only construct if SID is present
                default_twilio_api_url = f"https://api.twilio.com/2010-04-01/Accounts/{config_data['api_key']}"
            config_data['api_url'] = ICP.get_param('dfr_integrations.sms_twilio_api_url') or default_twilio_api_url
            extra_config_data['default_sender_id'] = ICP.get_param('dfr_integrations.sms_twilio_default_sender_id')
        # Add elif blocks for other providers (Vonage, SendGrid SMS, etc.)
        # elif provider_name == 'vonage':
        #     config_data['api_key'] = ICP.get_param('dfr_integrations.sms_vonage_api_key')
        #     config_data['api_secret'] = ICP.get_param('dfr_integrations.sms_vonage_api_secret')
        #     config_data['api_url'] = ICP.get_param('dfr_integrations.sms_vonage_api_url')
        elif provider_name == 'other': # Generic 'other' provider settings
             config_data['api_url'] = ICP.get_param('dfr_integrations.sms_gateway_url')
             config_data['api_key'] = ICP.get_param('dfr_integrations.sms_gateway_api_key')
             config_data['api_secret'] = ICP.get_param('dfr_integrations.sms_gateway_secret')
             # 'other' might require more specific extra_config, depending on the client
        else:
            _logger.error(f"Configuration logic missing for SMS provider: {provider_name}")
            raise ConfigurationError(_(f"Internal configuration logic missing for SMS provider: {provider_name}"))

        if extra_config_data:
            config_data['extra_config'] = extra_config_data

        try:
            config = SmsProviderConfig(**config_data)
        except Exception as e: # Catch Pydantic validation errors
            _logger.error(f"Invalid configuration data for SMS provider {provider_name}: {e}", exc_info=True)
            raise ConfigurationError(_(f"Invalid configuration data for SMS provider {provider_name}: {e}"))


        # API URL and key/secret checks (some might be optional depending on client logic)
        if not config.api_url and provider_name != 'twilio': # Twilio client might construct its own URL if partial info given
             _logger.warning(f"API URL not set for SMS provider {provider_name}, but may not be required by all implementations.")
        # Key/secret checks are usually done within the client's __init__

        timeout = int(ICP.get_param('dfr_integrations.sms_gateway_timeout', '10'))

        try:
            # Instantiate the client using the gathered config and timeout
            return client_class(config=config, timeout_seconds=timeout)
        except ConfigurationError as e:
            _logger.error(f"Configuration error initializing SMS client {provider_name}: {e}", exc_info=True)
            raise # Re-raise to be caught by sender and converted to UserError or DTO
        except Exception as e:
            _logger.error(f"Unexpected error initializing SMS client {provider_name}: {e}", exc_info=True)
            raise ConfigurationError(_(f"Could not initialize SMS client {provider_name}: An unexpected error occurred. Check logs."))


    @api.model
    def send_sms_message(self, recipient_phone: str, message_body: str, sender_id: Optional[str] = None, country_id: Optional[int] = None) -> SmsSendResponse:
        """
        Sends an SMS message using the configured gateway.
        Country_id can be passed to fetch country-specific configurations if settings were per-company/country (not currently implemented in config retrieval).
        :return: SmsSendResponse DTO indicating status.
        """
        # Sanitize sensitive data for logging
        log_recipient_phone = '***' + recipient_phone[-4:] if recipient_phone and len(recipient_phone) > 4 else 'Invalid/Short Phone'
        log_sender_id = sender_id if sender_id else 'Default' # Sender ID might not be sensitive

        _logger.info(f"Service call: Send SMS to {log_recipient_phone} (sender: {log_sender_id})")

        # If configurations were company-specific based on country, context switching logic would go here.
        # For now, config parameters are global.

        client = None
        try:
            client = self._get_configured_sms_client()
            if not client:
                _logger.warning("SMS sending skipped: No external SMS client configured or available.")
                # Return a specific status indicating it was skipped intentionally
                return SmsSendResponse(status='skipped', error_message="No external SMS client configured.")

            request_dto = SmsSendRequest(
                recipient_phone=recipient_phone, # Send original phone to client
                message_body=message_body,
                sender_id=sender_id
            )
            response_dto = client.send_sms(request_dto)

            # Log based on the response status
            if response_dto.status in ['sent', 'queued', 'accepted', 'delivered']: # Add 'delivered' if some clients provide it as success
                _logger.info(
                    f"SMS successfully processed by gateway {client.config.provider_name} to {log_recipient_phone}. "
                    f"Status: {response_dto.status}, Message SID: {response_dto.message_sid or 'N/A'}"
                )
            else:
                _logger.error(
                    f"SMS sending to {log_recipient_phone} failed or status indicated an issue with gateway {client.config.provider_name}: "
                    f"Status: {response_dto.status}, Error: {response_dto.error_message or 'N/A'} (Code: {response_dto.error_code or 'N/A'})"
                )

            return response_dto

        except ConfigurationError as e:
            _logger.error(f"Configuration error for SMS Dispatch Service: {e}", exc_info=True)
            # For automated processes, returning a failure DTO is preferred over UserError
            return SmsSendResponse(status='config_error', error_message=str(e))
        except IntegrationAPIError as e:
            _logger.error(f"API error during SMS dispatch to {log_recipient_phone}: {e.message}", exc_info=True)
            raw_response_content = e.response_content if isinstance(e.response_content, (dict, str)) else {"error_text": str(e)}
            if isinstance(raw_response_content, str):
                 raw_response_content = {"error_text": raw_response_content}
            return SmsSendResponse(status='api_error', error_message=e.message, error_code=str(e.status_code) if e.status_code else 'API_ERR', raw_response=raw_response_content)
        except Exception as e: # Catch any other unexpected errors
            _logger.error(f"Unexpected error in SMS Dispatch Service to {log_recipient_phone}: {e}", exc_info=True)
            return SmsSendResponse(status='error', error_message=f"An unexpected error occurred: {str(e)}")