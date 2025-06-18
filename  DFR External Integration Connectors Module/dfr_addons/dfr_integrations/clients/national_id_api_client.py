import logging
from .base_client import BaseApiClient
from odoo.addons.dfr_integrations.dtos import NationalIdValidationRequest, NationalIdValidationResponse
from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError, IntegrationAPIError

_logger = logging.getLogger(__name__)

class NationalIdApiClient(BaseApiClient):
    """
    Client for interacting with an external National ID validation API.
    """
    def __init__(self, base_url: str, api_key: str, timeout_seconds: int = 10):
        """
        Initializes the NationalIdApiClient.

        :param base_url: The base URL of the National ID API.
        :param api_key: The API key for authentication.
        :param timeout_seconds: Timeout for API requests in seconds.
        :raises ConfigurationError: If the API key is not provided.
        """
        if not api_key:
            _logger.error("National ID API Key not configured.")
            raise ConfigurationError("National ID API Key not configured.")
        super().__init__(base_url=base_url, api_key=api_key, timeout_seconds=timeout_seconds, service_name="NationalIDService")

    def _get_headers(self) -> dict:
        """
        Overrides _get_headers to include the API key for National ID service.
        The specific header name (e.g., 'X-API-Key', 'Authorization') depends on the API.
        """
        headers = super()._get_headers()
        # Assuming the API expects the key in 'X-API-Key' header.
        # Adjust if the API uses a different mechanism like 'Authorization: Bearer <token>'.
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        return headers

    def validate_national_id(self, request_dto: NationalIdValidationRequest) -> NationalIdValidationResponse:
        """
        Validates a National ID using the external service.

        :param request_dto: An instance of NationalIdValidationRequest containing the ID details.
        :return: An instance of NationalIdValidationResponse with the validation result.
        """
        # Sanitize ID number for logging
        log_id_number = '***' + request_dto.id_number[-4:] if request_dto.id_number and len(request_dto.id_number) > 4 else '***'
        _logger.info(
            f"Validating National ID: {log_id_number} (Type: {request_dto.id_type}) for country {request_dto.country_code}"
        )
        try:
            # The specific endpoint for validation, e.g., '/validate_id' or '/validate'
            # This should be defined by the actual API documentation.
            endpoint = '/validate_id' 
            
            # Use model_dump to convert Pydantic model to dict, excluding None values.
            payload = request_dto.model_dump(exclude_none=True)
            
            # Sanitize payload for logging
            log_payload = payload.copy()
            if 'id_number' in log_payload:
                log_payload['id_number'] = '***'
            _logger.debug(f"National ID validation request payload (sanitized): {log_payload}")


            response = self._request(
                method='POST',
                endpoint=endpoint,
                json_data=payload # Send original payload to API
            )
            response_data = response.json()
            _logger.debug(f"National ID validation raw response: {response_data}")
            
            # Assuming the response_data directly maps to NationalIdValidationResponse fields
            return NationalIdValidationResponse(**response_data, raw_response=response_data)

        except InvalidResponseError as e:
            _logger.error(f"Invalid response during National ID validation for ID {log_id_number}: {e.message}", exc_info=True)
            raw_response_content = e.response_content if isinstance(e.response_content, (dict, str)) else {"error_text": str(e.response_content)}
            if isinstance(raw_response_content, str):
                 raw_response_content = {"error_text": raw_response_content} # Ensure dict for raw_response
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=e.message, 
                error_code=str(e.status_code) if e.status_code else 'API_ERROR', 
                raw_response=raw_response_content
            )
        except IntegrationAPIError as e: # Catch other API errors (timeout, auth, service unavailable)
            _logger.error(f"API error during National ID validation for ID {log_id_number}: {e.message}", exc_info=True)
            raw_response_content = e.response_content if isinstance(e.response_content, (dict, str)) else {"error_text": str(e.response_content)}
            if isinstance(raw_response_content, str):
                 raw_response_content = {"error_text": raw_response_content}
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=e.message, 
                error_code=str(e.status_code) if e.status_code else 'API_ERROR', 
                raw_response=raw_response_content
            )
        except Exception as e:
            _logger.error(f"Unexpected error validating National ID {log_id_number}: {e}", exc_info=True)
            return NationalIdValidationResponse(
                is_valid=False, 
                error_message=f"An unexpected error occurred: {str(e)}"
            )