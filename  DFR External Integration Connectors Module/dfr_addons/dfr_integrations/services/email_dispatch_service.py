import logging
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.addons.dfr_integrations.clients import (
    EmailGatewayClientInterface,
    EmailSendGridClient # Example
    # Import other clients like EmailMailgunClient here
)
from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig, EmailAttachmentDTO
from odoo.addons.dfr_integrations.exceptions import IntegrationAPIError, ConfigurationError
from typing import Optional, List, Union, Dict, Any
import base64
import requests # For requests.exceptions.RequestException

_logger = logging.getLogger(__name__)

class EmailDispatchService(models.AbstractModel):
    _name = 'dfr.email.dispatch.service'
    _description = 'DFR Email Dispatch Service'

    PROVIDER_CLIENT_MAP: Dict[str, type[EmailGatewayClientInterface]] = {
        'sendgrid': EmailSendGridClient,
        # 'mailgun': EmailMailgunClient, # Add actual providers here
    }

    def _get_configured_email_client(self) -> Optional[EmailGatewayClientInterface]:
        """
        Fetches configuration and instantiates the appropriate Email client.
        Returns None if no external provider is configured ('odoo' or 'none').
        Raises ConfigurationError if a provider is selected but config is invalid or client is unsupported.
        """
        ICP = self.env['ir.config_parameter'].sudo()
        provider_name = ICP.get_param('dfr_integrations.email_gateway_provider')

        if not provider_name or provider_name in ['odoo', 'none']:
            _logger.info("External email gateway not configured or set to 'odoo'/'none'. Will use Odoo's internal mail system if needed.")
            return None

        client_class = self.PROVIDER_CLIENT_MAP.get(provider_name)
        if not client_class:
            _logger.error(f"Unsupported email gateway provider configured: {provider_name}")
            raise ConfigurationError(_(f"Unsupported email gateway provider: {provider_name}. Please check configuration."))

        # Gather config for the specific provider
        config_data: Dict[str, Any] = {'provider_name': provider_name}
        extra_config_data: Dict[str, Any] = {}

        if provider_name == 'sendgrid':
            config_data['api_key'] = ICP.get_param('dfr_integrations.email_sendgrid_api_key')
            config_data['api_url'] = ICP.get_param('dfr_integrations.email_sendgrid_api_url') or 'https://api.sendgrid.com/v3'
        # Add elif for other providers
        # elif provider_name == 'mailgun':
        #    config_data['api_key'] = ICP.get_param('dfr_integrations.email_mailgun_api_key')
        #    config_data['api_url'] = ICP.get_param('dfr_integrations.email_mailgun_api_url')
        #    extra_config_data['domain'] = ICP.get_param('dfr_integrations.email_mailgun_domain')
        elif provider_name == 'other': # Generic 'other' email provider settings
             config_data['api_url'] = ICP.get_param('dfr_integrations.email_gateway_url') # Assuming generic fields in settings
             config_data['api_key'] = ICP.get_param('dfr_integrations.email_gateway_api_key')
             config_data['api_secret'] = ICP.get_param('dfr_integrations.email_gateway_secret')
        else:
            _logger.error(f"Configuration logic missing for email provider: {provider_name}")
            raise ConfigurationError(_(f"Internal configuration logic missing for email provider: {provider_name}"))
        
        if extra_config_data:
            config_data['extra_config'] = extra_config_data

        try:
            config = EmailProviderConfig(**config_data)
        except Exception as e: # Catch Pydantic validation errors
            _logger.error(f"Invalid configuration data for email provider {provider_name}: {e}", exc_info=True)
            raise ConfigurationError(_(f"Invalid configuration data for email provider {provider_name}: {e}"))


        if not config.api_key and provider_name not in ['odoo', 'none']: # Odoo provider doesn't use API key from these params
             _logger.error(f"API Key not configured for email provider {provider_name}")
             raise ConfigurationError(_(f"API Key not configured for email provider {provider_name}. Please ensure it is set in DFR Integration Settings."))


        timeout = int(ICP.get_param('dfr_integrations.email_gateway_timeout', '15'))
        try:
            # Instantiate the client using the gathered config and timeout
            return client_class(config=config, timeout_seconds=timeout)
        except ConfigurationError as e:
            _logger.error(f"Configuration error initializing email client {provider_name}: {e}", exc_info=True)
            raise # Re-raise
        except Exception as e:
            _logger.error(f"Unexpected error initializing email client {provider_name}: {e}", exc_info=True)
            raise ConfigurationError(_(f"Could not initialize email client {provider_name}: An unexpected error occurred. Check logs."))

    @api.model
    def send_email_message(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        body_html: Optional[str] = None,
        body_text: Optional[str] = None,
        from_email_str: Optional[str] = None, # Specific sender for this message
        reply_to_email_str: Optional[str] = None,
        attachments: Optional[List[EmailAttachmentDTO]] = None, # DTO for attachments
        mail_server_id: Optional[int] = None # To use a specific Odoo mail server
    ) -> Union[EmailSendResponse, bool]:
        """
        Sends an email using configured external gateway or Odoo's internal system.
        Attachments should be list of EmailAttachmentDTO.
        Returns EmailSendResponse if external gateway is used, or True/False from Odoo mail.
        """
        if isinstance(to_emails, str):
            to_emails_list = [email.strip() for email in to_emails.split(',') if email.strip()]
        else:
            to_emails_list = [email.strip() for email in to_emails if email.strip()]
        
        if not to_emails_list:
            _logger.warning("Email sending skipped: No recipient email addresses provided.")
            return EmailSendResponse(status='skipped', error_message="No recipient(s) provided.") if self.env['ir.config_parameter'].sudo().get_param('dfr_integrations.email_gateway_provider') not in ['odoo', 'none', False] else False


        _logger.info(f"Service call: Send Email to {', '.join(to_emails_list)} with subject: {subject}")

        ICP = self.env['ir.config_parameter'].sudo()
        # Determine the final 'from' email address
        # Priority: 1. message-specific, 2. DFR integration default, 3. Odoo company email, 4. Odoo mail.default.from
        final_from_email = from_email_str or \
                           ICP.get_param('dfr_integrations.default_email_from') or \
                           self.env.company.email or \
                           ICP.get_param('mail.default.from')

        if not final_from_email:
            _logger.error("Default 'from' email address not configured for sending emails. Please set it in DFR Integration Settings or Odoo General Settings.")
            # Match return type based on potential client usage
            external_provider_configured = ICP.get_param('dfr_integrations.email_gateway_provider') not in ['odoo', 'none', False]
            return EmailSendResponse(status='config_error', error_message="Default 'from' email not configured.") if external_provider_configured else False

        external_client = None # To track if we attempted external client
        try:
            external_client = self._get_configured_email_client()
            if external_client:
                _logger.info(f"Using external email gateway: {external_client.config.provider_name}")
                request_dto = EmailSendRequest(
                    to_email=to_emails_list,
                    from_email=final_from_email,
                    reply_to_email=reply_to_email_str,
                    subject=subject,
                    html_body=body_html,
                    text_body=body_text,
                    attachments=attachments or [] # Ensure it's a list for the DTO
                )
                response_dto = external_client.send_email(request_dto)

                # Log based on the response status
                if response_dto.status in ['accepted', 'sent', 'queued']:
                     _logger.info(
                         f"Email successfully processed by gateway {external_client.config.provider_name} to {', '.join(to_emails_list)}. "
                         f"Status: {response_dto.status}, Message ID: {response_dto.message_id or 'N/A'}"
                     )
                else:
                     _logger.error(
                         f"Email sending to {', '.join(to_emails_list)} failed or status indicated an issue with gateway {external_client.config.provider_name}: "
                         f"Status: {response_dto.status}, Error: {response_dto.error_message or 'N/A'}"
                     )
                return response_dto
            else:
                _logger.info("Using Odoo's internal mail system for sending email.")
                # Prepare mail.mail values
                mail_values = {
                    'subject': subject,
                    'body_html': body_html or (body_text.replace('\n', '<br/>') if body_text else ''),
                    'email_to': ','.join(to_emails_list),
                    'email_from': final_from_email,
                    'auto_delete': True, # Auto-delete sent mail records is a common practice
                }
                if reply_to_email_str:
                    mail_values['reply_to'] = reply_to_email_str
                if mail_server_id: # Use a specific Odoo mail server if requested
                     mail_values['mail_server_id'] = mail_server_id

                # Create the mail.mail record
                mail = self.env['mail.mail'].sudo().create(mail_values)

                # Attach files if any, using ir.attachment and linking to mail.mail
                if attachments:
                    attachment_ids = []
                    for att_dto in attachments:
                        try:
                            if not att_dto.content_base64 or not att_dto.filename or not att_dto.content_type:
                                _logger.warning(f"Skipping invalid attachment: {att_dto.filename or 'Unknown Filename'}, missing essential data (content, filename, or type).")
                                continue
                            attachment_data = {
                                'name': att_dto.filename,
                                'datas': att_dto.content_base64, # datas field expects base64 string
                                'mimetype': att_dto.content_type,
                                'res_model': 'mail.mail', # Link attachments to the mail.mail record
                                'res_id': mail.id,       # Link to the specific mail.mail record ID
                            }
                            attachment_ids.append(self.env['ir.attachment'].sudo().create(attachment_data).id)
                        except Exception as att_err:
                            _logger.error(f"Failed to create attachment '{att_dto.filename}': {att_err}", exc_info=True)
                    # Linking attachments to mail.mail is handled by res_model/res_id on attachment creation.
                    # If direct linking to mail.attachment_ids is needed for some reason after creation:
                    # if attachment_ids:
                    #    mail.attachment_ids = [(6, 0, attachment_ids)]


                # Send the email using Odoo's mail server
                mail.send() # This method can raise exceptions on immediate failure
                _logger.info(f"Email to {', '.join(to_emails_list)} queued via Odoo internal mail system (Mail ID: {mail.id}).")
                # Odoo's send() typically returns True on success (or if queued), raises error on failure.
                return True

        except ConfigurationError as e:
            _logger.error(f"Configuration error for Email Dispatch Service: {e}", exc_info=True)
            return EmailSendResponse(status='config_error', error_message=str(e)) if external_client else False
        except (IntegrationAPIError, requests.exceptions.RequestException) as e:
            # Catch both custom IntegrationAPIError and lower-level requests library exceptions
            error_message = str(e)
            raw_response_content = None
            if isinstance(e, IntegrationAPIError):
                error_message = e.message
                if isinstance(e.response_content, (dict, str)):
                    raw_response_content = e.response_content
                    if isinstance(raw_response_content, str):
                        raw_response_content = {"error_text": raw_response_content}
            elif isinstance(e, requests.exceptions.RequestException):
                 raw_response_content = {"error_type": type(e).__name__, "error_text": str(e)}

            _logger.error(f"API/Network error during email dispatch to {', '.join(to_emails_list)}: {error_message}", exc_info=True)
            return EmailSendResponse(status='api_error', error_message=error_message, raw_response=raw_response_content) if external_client else False

        except UserError: # Let UserErrors (e.g., from mail.send misconfiguration) propagate if using Odoo internal
             raise
        except Exception as e: # Catch any other unexpected errors
            _logger.error(f"Unexpected error in Email Dispatch Service to {', '.join(to_emails_list)}: {e}", exc_info=True)
            return EmailSendResponse(status='error', error_message=f"An unexpected error occurred: {str(e)}") if external_client else False