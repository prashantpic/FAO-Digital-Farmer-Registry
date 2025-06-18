```python
import requests
import json
from dfr.testing.automation.utils.logger_setup import setup_logger
from dfr.testing.automation.config import global_config

logger = setup_logger(__name__)

class ApiClient:
    """
    A reusable API client for interacting with the DFR backend APIs.
    Manages sessions, base URL, and authentication headers.
    """
    def __init__(self, base_url: str = None, auth_handler=None):
        """
        Initializes the ApiClient.

        Args:
            base_url (str, optional): The base URL for the API. If None, it's fetched from global_config.
            auth_handler (AuthHandler, optional): An instance of AuthHandler for managing authentication.
        """
        self.base_url = base_url or global_config.get_api_base_url()
        self.session = requests.Session()
        self.auth_handler = auth_handler
        # Default headers, can be overridden per request
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        logger.info(f"ApiClient initialized with base_url: {self.base_url}")

    def _get_auth_headers(self) -> dict:
        """Fetches current authentication headers from the auth handler if available."""
        if self.auth_handler:
            return self.auth_handler.get_auth_header()
        return {}

    def request(self, method: str, endpoint: str, params: dict = None, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request to the specified endpoint.

        Args:
            method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint (str): The API endpoint (e.g., "/farmers").
            params (dict, optional): Dictionary of URL query parameters.
            data (dict, optional): Dictionary, bytes, or file-like object to send in the body (form-encoded).
            json_payload (dict, optional): Dictionary to send in the body as JSON.
            headers (dict, optional): Dictionary of request headers to override defaults.
            **kwargs: Additional arguments passed to requests.Session.request (e.g., files, timeout).

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.RequestException: If the request fails due to network issues or HTTP errors that requests.raise_for_status() would catch (if enabled).
        """
        url = f"{self.base_url.rstrip('/')}{endpoint}" # Ensure no double slashes
        
        request_headers = self.session.headers.copy() # Start with session defaults
        request_headers.update(self._get_auth_headers()) # Add/override with auth headers
        if headers:
            request_headers.update(headers) # Add/override with per-request headers

        logger.debug(f"Request: {method.upper()} {url}")
        if params: 
            logger.debug(f"Params: {params}")
        if data: 
            # Be careful logging potentially large or sensitive data
            logger.debug(f"Data (form-data/bytes): {str(data)[:200]}...") 
        if json_payload is not None: 
            try:
                logger.debug(f"JSON Payload: {json.dumps(json_payload, indent=2)}")
            except TypeError: # Handle non-serializable if any (should not happen for dicts)
                logger.debug(f"JSON Payload (raw): {str(json_payload)[:200]}...")
        
        # Ensure timeout is applied if not specified in kwargs
        timeout = kwargs.pop('timeout', global_config.DEFAULT_TIMEOUT_SECONDS)

        try:
            response = self.session.request(
                method, url, params=params, data=data, json=json_payload, headers=request_headers,
                timeout=timeout, **kwargs
            )
            logger.info(f"Response: {response.status_code} {response.reason} from {method.upper()} {url}")
            # Log response body (first N chars or parse if JSON)
            try:
                # Attempt to log JSON response prettily if it's JSON
                logger.debug(f"Response Body (JSON): {json.dumps(response.json(), indent=2)}")
            except requests.exceptions.JSONDecodeError:
                # Log non-JSON or empty response text (first 500 chars)
                logger.debug(f"Response Body (Text): {response.text[:500]}{'...' if len(response.text) > 500 else ''}")
            
            # Optionally, enable raise_for_status for all responses or handle specific status codes
            # response.raise_for_status() # Uncomment to automatically raise HTTPError for 4xx/5xx responses
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed for {method.upper()} {url}: {e}")
            raise # Re-raise the exception to allow test framework to catch it

    def get(self, endpoint: str, params: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """Sends a GET request."""
        return self.request("GET", endpoint, params=params, headers=headers, **kwargs)

    def post(self, endpoint: str, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """Sends a POST request."""
        return self.request("POST", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

    def put(self, endpoint: str, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """Sends a PUT request."""
        return self.request("PUT", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

    def delete(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """Sends a DELETE request."""
        return self.request("DELETE", endpoint, headers=headers, **kwargs)

    def patch(self, endpoint: str, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """Sends a PATCH request."""
        return self.request("PATCH", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)
```