```python
import time
import requests
import os
from dfr.testing.automation.utils.logger_setup import setup_logger
from dfr.testing.automation.config import global_config
# from dfr.testing.automation.utils.config_loader import ConfigLoader # Assumed to be used by fixtures, not directly here for simplicity

logger = setup_logger(__name__)

class AuthHandler:
    """
    Manages authentication tokens (e.g., OAuth2) for API requests.
    Handles fetching and refreshing tokens, specifically for client credentials grant type.
    """
    _token: str | None = None
    _token_expiry_timestamp: float = 0  # Unix timestamp when the token expires
    _token_refresh_buffer_seconds: int = 120  # Refresh token if it expires within this buffer (e.g., 2 minutes)

    def __init__(self, auth_url_endpoint: str, client_id: str, client_secret: str, audience: str | None = None):
        """
        Initializes the AuthHandler for OAuth2 client credentials flow.

        Args:
            auth_url_endpoint (str): The API endpoint for fetching tokens (e.g., "/oauth/token").
                                     This is typically relative to the API domain root.
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.
            audience (str, optional): The audience for the token (relevant for some OAuth2 flows).
        """
        # Construct the full auth URL. Assumes auth_url_endpoint is relative to the domain root.
        # Example: if api_base_url is "http://domain.com/api/v1", and endpoint is "/oauth/token",
        # auth_url becomes "http://domain.com/oauth/token".
        api_base = global_config.get_api_base_url() # Use the one from global config for current env
        
        # Attempt to find the domain root from the API base URL
        # This handles cases like "http://host/api/v1" -> "http://host"
        # or "http://host.domain.com" -> "http://host.domain.com" if no /api path part
        parts = api_base.split("://", 1)
        if len(parts) == 2:
            protocol, rest_of_url = parts
            domain_part = rest_of_url.split("/", 1)[0]
            self.auth_url_base = f"{protocol}://{domain_part}"
        else: # Fallback if URL structure is unexpected
            self.auth_url_base = api_base.rsplit('/api', 1)[0] if '/api' in api_base else api_base

        self.auth_url = f"{self.auth_url_base.rstrip('/')}{auth_url_endpoint}"
        
        self.client_id = client_id
        self.client_secret = client_secret # Note: This secret should be handled securely.
        self.audience = audience
        logger.info(f"AuthHandler initialized. Auth URL: {self.auth_url}, Client ID: {self.client_id}")

    def _is_token_valid(self) -> bool:
        """Checks if the current token is valid and not near expiry."""
        if not self._token:
            return False
        # Check if current time is less than expiry minus buffer
        return time.time() < (self._token_expiry_timestamp - self._token_refresh_buffer_seconds)

    def _fetch_token_oauth_client_credentials(self) -> None:
        """
        Fetches an access token using the OAuth2 client credentials grant type.
        Updates `_token` and `_token_expiry_timestamp`.
        """
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if self.audience:
            payload['audience'] = self.audience

        # OAuth2 token endpoints typically expect form-urlencoded data
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        logger.info(f"Attempting to fetch new token from {self.auth_url} using client_credentials.")
        try:
            # Use a new requests session for auth to avoid interference with API client's session defaults
            response = requests.post(self.auth_url, data=payload, headers=headers, timeout=global_config.DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            token_data = response.json()
            self._token = token_data.get('access_token')
            expires_in = token_data.get('expires_in')

            if not self._token:
                raise ValueError("Access token not found in authentication response.")
            if expires_in is None or not isinstance(expires_in, (int, float)):
                logger.warning(f"Invalid or missing 'expires_in' in token response. Got: {expires_in}. Defaulting to 3600 seconds.")
                expires_in = 3600 # Default to 1 hour

            self._token_expiry_timestamp = time.time() + float(expires_in)
            logger.info(f"Successfully fetched new authentication token. Expires in: {expires_in}s.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch token from {self.auth_url}: {e}")
            self._token = None
            self._token_expiry_timestamp = 0
            raise  # Re-raise to indicate authentication failure
        except (ValueError, KeyError) as e: # Catch issues with token data parsing
            logger.error(f"Token data parsing error: {e}. Response: {response.text if 'response' in locals() else 'N/A'}")
            self._token = None
            self._token_expiry_timestamp = 0
            raise

    def authenticate_user_password(self, username: str, password: str, token_endpoint: str = "/api/auth/login"):
        """
        Illustrative method for authenticating a user via username/password.
        This method's implementation would depend heavily on the DFR_MOD_API_GATEWAY's
        specific user authentication endpoint (REQ-API-003).
        The primary authentication mechanism for test suite backend access is likely client_credentials.
        """
        logger.warning("authenticate_user_password is an illustrative placeholder and not fully implemented for DFR.")
        # Example logic (adjust to DFR's actual user auth flow):
        # auth_api_url = global_config.get_api_base_url()
        # login_url = f"{auth_api_url.rstrip('/')}{token_endpoint}"
        # payload = {"username": username, "password": password}
        # headers = {"Content-Type": "application/json"}
        # try:
        #     response = requests.post(login_url, json=payload, headers=headers, timeout=global_config.DEFAULT_TIMEOUT_SECONDS)
        #     response.raise_for_status()
        #     token_data = response.json()
        #     self._token = token_data.get("access_token")
        #     # ... handle expiry ...
        #     logger.info(f"User {username} authenticated successfully (illustrative).")
        # except Exception as e:
        #     logger.error(f"User authentication failed for {username} (illustrative): {e}")
        #     self._token = None
        #     self._token_expiry_timestamp = 0
        #     raise
        pass # This method is not the primary focus for backend service auth in tests

    def get_auth_header(self) -> dict:
        """
        Returns the authentication header (e.g., {'Authorization': 'Bearer <token>'}).
        Automatically fetches or refreshes the token if needed using client credentials flow.
        """
        if not self._is_token_valid():
            logger.info("Token is invalid, expired, or not present. Attempting to fetch/refresh token via client credentials.")
            try:
                self._fetch_token_oauth_client_credentials()
            except Exception as e:
                logger.error(f"Failed to fetch/refresh token during get_auth_header: {e}")
                # Return empty headers. Subsequent API request will likely fail with 401/403.
                return {}

        if self._token:
            return {"Authorization": f"Bearer {self._token}"}
        
        logger.warning("No valid token available to generate authorization header.")
        return {} # No token available

    def set_token_for_testing(self, token: str, expires_in_seconds: int = 3600):
        """
        Helper method for testing purposes (e.g., expired token tests).
        Allows setting a token manually. USE WITH CAUTION.
        """
        self._token = token
        self._token_expiry_timestamp = time.time() + expires_in_seconds
        logger.warning(f"Authentication token manually set for testing. Expires in approx {expires_in_seconds}s.")

    def clear_token(self):
        """Clears the current token, forcing a re-fetch on next get_auth_header call."""
        self._token = None
        self._token_expiry_timestamp = 0
        logger.info("Auth token cleared.")
```