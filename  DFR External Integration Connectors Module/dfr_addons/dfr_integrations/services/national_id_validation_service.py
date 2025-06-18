import logging
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.addons.dfr_integrations.clients import NationalIdApiClient
from odoo.addons.dfr_integrations.dtos import NationalIdValidationRequest, NationalIdValidationResponse
from odoo.addons.dfr_integrations.exceptions import IntegrationAPIError, ConfigurationError, InvalidResponseError

_logger = logging.getLogger(__name__)

class NationalIdValidationService(models.AbstractModel):
    _name = 'dfr.national.id.validation.service'
    _description = 'DFR National ID Validation Service'

    def _get_client(self) -> NationalIdApiClient:
        ICP = self.env['ir.config_parameter'].sudo()
        api_url = ICP.get_param('dfr_integrations.national_id_api_url')
        api_key = ICP.get_param('dfr_integrations.national_id_api_key') # This might be optional for some providers
        
        if not api_url:
            _logger.error("National ID API URL ('dfr_integrations.national_id_api_url') not configured.")
            # This ConfigurationError should be caught by the calling method and translated to UserError
            raise ConfigurationError(_("National ID Validation Service is not properly configured (API URL missing). Please contact your system administrator."))
        
        # API key check is deferred to the client, as some APIs might not require it or have it in URL
        # if not api_key:
        #     _logger.warning("National ID API Key ('dfr_integrations.national_id_api_key') not configured. Service might fail if key is required by the provider.")
        
        try:
            timeout_seconds = int(ICP.get_param('dfr_integrations.national_id_api_timeout', '10'))
        except ValueError:
            _logger.warning("Invalid value for 'dfr_integrations.national_id_api_timeout', using default 10s.")
            timeout_seconds = 10
        
        try:
            # Client's __init__ will raise ConfigurationError if api_key is mandatory and missing, or if base_url is invalid.
            return NationalIdApiClient(base_url=api_url, api_key=api_key, timeout_seconds=timeout_seconds)
        except ConfigurationError as e: # Catch config errors from client init
            _logger.error(f"Configuration error initializing NationalIdApiClient: {str(e)}")
            raise # Re-raise to be caught and converted to UserError by the public method
        except Exception as e:
            _logger.error(f"Unexpected error initializing NationalIdApiClient: {str(e)}", exc_info=True)
            # Generic catch, re-raise as ConfigurationError to signal setup issue
            raise ConfigurationError(_("Failed to initialize the National ID validation client due to an unexpected error. Check logs and configuration.")) from e


    @api.model
    def validate_id(self, id_number: str, id_type: str, country_code: str) -> NationalIdValidationResponse:
        """
        Validates a National ID using the configured external service.
        :param id_number: The National ID number to validate.
        :param id_type: The type of National ID (e.g., 'PASSPORT', 'NATIONAL_CARD').
        :param country_code: ISO 3166-1 alpha-2 country code.
        :return: NationalIdValidationResponse DTO.
        :raises: UserError if the service is not configured correctly.
                 Other exceptions are caught and returned as error fields in the DTO.
        """
        # Sanitize ID number for logging
        log_id_number = id_number[:3] + '***' + id_number[-3:] if id_number and len(id_number) > 6 else '***'
        _logger.info(f"Service call: Validate ID {log_id_number} (type: {id_type}, country: {country_code})")
        
        try:
            client = self._get_client()
            request_dto = NationalIdValidationRequest(
                id_number=id_number, # Pass original ID number to client
                id_type=id_type,
                country_code=country_code
            )
            response_dto = client.validate_national_id(request_dto)

            if not response_dto.is_valid and response_dto.error_message:
                 _logger.warning(f"National ID validation failed for ID {log_id_number} (type: {id_type}, country: {country_code}): {response_dto.error_message} (Code: {response_dto.error_code})")
            elif response_dto.is_valid:
                 _logger.info(f"National ID validation successful for ID {log_id_number} (type: {id_type}, country: {country_code}). Name: {response_dto.full_name or 'N/A'}")
            
            return response_dto

        except ConfigurationError as e:
            _logger.error(f"Configuration error encountered in National ID Validation Service: {str(e)}")
            # Propagate configuration errors as UserError to inform administrators directly.
            raise UserError(str(e)) from e
        except InvalidResponseError as e: # Specific error from client (e.g., 400 Bad Request)
            _logger.error(f"Invalid response from National ID API for ID {log_id_number}: {e.message}", exc_info=True)
            raw_resp = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=_("The ID validation service reported an issue with the request: %s") % e.message,
                error_code=str(e.status_code),
                raw_response=raw_resp
            )
        except IntegrationAPIError as e: # More generic API errors (timeout, auth, service unavailable)
            _logger.error(f"API error during National ID validation for ID {log_id_number}: {e.message}", exc_info=True)
            raw_resp = e.response_content if isinstance(e.response_content, dict) else {"error_text": str(e.response_content)}
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=_("Could not connect to the ID validation service or an API error occurred: %s") % e.message,
                error_code=str(e.status_code) if e.status_code else 'API_ERROR',
                raw_response=raw_resp
            )
        except Exception as e:
            _logger.error(f"Unexpected error in National ID Validation Service for ID {log_id_number}: {str(e)}", exc_info=True)
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=_("An unexpected error occurred during ID validation. Please check logs or contact support."),
                raw_response={"error_text": str(e)}
            )