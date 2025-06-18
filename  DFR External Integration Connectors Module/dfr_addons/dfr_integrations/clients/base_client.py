import requests
import logging
from typing import Optional, List, Dict, Any
from odoo.addons.dfr_integrations.exceptions import (
    IntegrationAPIError,
    ExternalServiceAuthenticationError,
    APITimeoutError,
    InvalidResponseError,
    ServiceUnavailableError,
    ConfigurationError
)

_logger = logging.getLogger(__name__)

class BaseApiClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout_seconds: int = 30, service_name: str = "ExternalService"):
        if not base_url:
            _logger.error(f"{service_name}: Base URL not configured.")
            raise ConfigurationError(f"{service_name}: Base URL not configured.")
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key # Subclasses will handle specific auth mechanisms
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.service_name = service_name
        # Ensure TLS verification is enabled; requests library defaults to True, but explicit is good.
        self.session.verify = True


    def _get_headers(self) -> Dict[str, str]:
        """
        Returns common headers. Subclasses should override to add authentication
        or service-specific headers.
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None, # For form-encoded data
        json_data: Optional[Dict[str, Any]] = None, # For JSON body
        expected_status_codes: Optional[List[int]] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Makes an HTTP request to the external API.
        """
        if expected_status_codes is None:
            expected_status_codes = [200, 201, 204]

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        if custom_headers:
            headers.update(custom_headers)

        # Note: Sensitive data in params or json_data should be sanitized before logging
        # by the caller or in overridden methods if context is available.
        _logger.debug(f"Requesting {self.service_name}: {method} {url} PARAMS: {params} JSON_DATA: {json_data}")

        try:
            response = self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout_seconds,
                verify=self.session.verify # Ensure TLS verification is used
            )
            # Log a snippet of the response content for debugging purposes.
            _logger.debug(f"Response from {self.service_name}: Status {response.status_code}, Content: {response.text[:500]}...")

            if response.status_code not in expected_status_codes:
                self._handle_api_error(response)
            return response
        except requests.exceptions.Timeout:
            _logger.error(f"{self.service_name} API request timed out: {method} {url}")
            raise APITimeoutError(f"{self.service_name} request timed out.", response_content="Request timed out")
        except requests.exceptions.RequestException as e:
            _logger.error(f"{self.service_name} API request failed: {method} {url}, Error: {e}")
            raise IntegrationAPIError(f"Failed to connect to {self.service_name}: {e}", response_content=str(e))

    def _handle_api_error(self, response: requests.Response):
        """
        Handles common API error responses and raises appropriate custom exceptions.
        Subclasses can override for service-specific error handling.
        """
        error_message = f"{self.service_name} API Error: Status {response.status_code}"
        response_content_for_exception = response.text # Default response content for exception
        
        try:
            # Try to parse JSON for more detailed error messages, but use raw text for exception content
            error_details = response.json()
            error_message += f" - Details: {error_details}"
        except ValueError: # Not JSON
            error_message += f" - Content: {response_content_for_exception[:200]}" # Log snippet of raw content

        _logger.error(error_message) # Log the potentially more detailed message

        if response.status_code in [401, 403]:
            raise ExternalServiceAuthenticationError(error_message, response.status_code, response_content_for_exception)
        elif response.status_code == 400:
            # Append a more specific message for bad request to the logged error_message
            detailed_error_msg = f"Bad Request to {self.service_name}. Check request parameters. {error_message}"
            raise InvalidResponseError(detailed_error_msg, response.status_code, response_content_for_exception)
        elif response.status_code == 404:
            detailed_error_msg = f"Resource not found on {self.service_name}. {error_message}"
            raise InvalidResponseError(detailed_error_msg, response.status_code, response_content_for_exception)
        elif response.status_code >= 500:
            detailed_error_msg = f"{self.service_name} unavailable or internal error. {error_message}"
            raise ServiceUnavailableError(detailed_error_msg, response.status_code, response_content_for_exception)
        else:
            raise IntegrationAPIError(error_message, response.status_code, response_content_for_exception)