import logging
from .base_client import BaseApiClient
from .email_gateway_client_interface import EmailGatewayClientInterface
from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig, EmailAttachmentDTO
from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError, IntegrationAPIError
from typing import Dict, List, Any

_logger = logging.getLogger(__name__)

class EmailSendGridClient(BaseApiClient, EmailGatewayClientInterface):
    def __init__(self, config: EmailProviderConfig, timeout_seconds: int = 15):
        if not config.api_key:
            raise ConfigurationError("SendGrid API Key not configured.")
        
        api_url = config.api_url
        if not api_url:
            api_url = 'https://api.sendgrid.com/v3' # Default SendGrid API URL
            _logger.info(f"SendGrid API URL not provided, using default: {api_url}")

        super(BaseApiClient, self).__init__(
            base_url=api_url, 
            api_key=config.api_key, # Store api_key for use in _get_headers
            timeout_seconds=timeout_seconds, 
            service_name="SendGridEmail"
        )
        EmailGatewayClientInterface.__init__(self, config)

    def _get_headers(self) -> Dict[str, str]:
        headers = super()._get_headers() # Gets {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers['Authorization'] = f'Bearer {self.api_key}' # self.api_key is set in BaseApiClient constructor
        return headers

    def send_email(self, request_dto: EmailSendRequest) -> EmailSendResponse:
        # Sanitize recipient emails for logging
        log_to_emails = [e[:3] + '***' + e[e.find('@'):] if '@' in e and len(e) > 5 else '***' for e in request_dto.to_email]
        _logger.info(f"Sending email via SendGrid to {log_to_emails} with subject: {request_dto.subject}")
        
        personalizations: List[Dict[str, Any]] = [{"to": [{"email": email} for email in request_dto.to_email]}]
        
        # Add CC and BCC if they were part of EmailSendRequest DTO (not in current SDS DTO)
        # Example:
        # if request_dto.cc_email:
        #     personalizations[0]["cc"] = [{"email": email} for email in request_dto.cc_email]
        # if request_dto.bcc_email:
        #     personalizations[0]["bcc"] = [{"email": email} for email in request_dto.bcc_email]

        content: List[Dict[str, str]] = []
        if request_dto.text_body:
            content.append({"type": "text/plain", "value": request_dto.text_body})
        if request_dto.html_body:
            content.append({"type": "text/html", "value": request_dto.html_body})
        
        if not content:
             # This check aligns with SDS, but raising ValueError might be too harsh for a client method.
             # Returning a DTO with error is often preferred.
             _logger.error("Email must have either text_body or html_body.")
             return EmailSendResponse(status='failed', error_message="Email content (text or HTML) is required.", raw_response={"error_text": "Email content (text or HTML) is required."})

        sendgrid_payload: Dict[str, Any] = {
            "personalizations": personalizations,
            "from": {"email": request_dto.from_email}, # from_email is EmailStr, so it's validated
            "subject": request_dto.subject,
            "content": content,
        }

        if request_dto.reply_to_email:
            sendgrid_payload["reply_to"] = {"email": request_dto.reply_to_email}
        
        if request_dto.attachments:
            sendgrid_payload["attachments"] = [
                {
                    "content": att.content_base64,
                    "filename": att.filename,
                    "type": att.content_type,
                    "disposition": "attachment" # Could be made configurable per attachment DTO if needed
                } for att in request_dto.attachments
            ]

        # Log sanitized payload (omitting sensitive content like attachment base64 for brevity/security in logs)
        log_payload = sendgrid_payload.copy()
        if "attachments" in log_payload:
            log_payload["attachments"] = f"[{len(log_payload['attachments'])} attachments]"
        if "content" in log_payload:
             log_payload["content"] = f"[{len(log_payload['content'])} content parts (text/html)]"

        _logger.debug(f"SendGrid email payload (sanitized for log): {log_payload}")

        try:
            # SendGrid returns 202 Accepted for successful requests to /mail/send
            response = self._request(
                method='POST',
                endpoint='/mail/send', 
                json_data=sendgrid_payload, # Use original payload
                expected_status_codes=[202] 
            )
            # SendGrid returns an empty body on 202, message_id is in headers
            message_id = response.headers.get('X-Message-Id')
            _logger.info(f"Email accepted by SendGrid for delivery. Message ID: {message_id}")
            return EmailSendResponse(status='accepted', message_id=message_id, raw_response={"headers": dict(response.headers)})

        except InvalidResponseError as e: # This exception would be raised by _handle_api_error
            _logger.error(f"Invalid SendGrid response: {e.message}")
            raw_content = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return EmailSendResponse(status='failed', error_message=e.message, raw_response=raw_content)
        except IntegrationAPIError as e: # Other errors from BaseApiClient (timeout, auth, etc.)
            _logger.error(f"SendGrid API Integration Error: {e.message}", exc_info=True)
            raw_content = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return EmailSendResponse(status='failed', error_message=e.message, raw_response=raw_content)
        except Exception as e:
            _logger.error(f"Unexpected error sending email via SendGrid: {e}", exc_info=True)
            return EmailSendResponse(status='failed', error_message=f"An unexpected error occurred: {str(e)}")