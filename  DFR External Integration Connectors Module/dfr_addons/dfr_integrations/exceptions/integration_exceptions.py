class IntegrationAPIError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message, status_code=None, response_content=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_content = response_content
        self.message = message

class ExternalServiceAuthenticationError(IntegrationAPIError):
    """Raised when authentication with an external service fails."""
    pass

class APITimeoutError(IntegrationAPIError):
    """Raised when a request to an external API times out."""
    pass

class InvalidResponseError(IntegrationAPIError):
    """Raised when the external API returns an unexpected or invalid response."""
    pass

class ConfigurationError(IntegrationAPIError):
    """Raised for errors related to misconfiguration of an integration."""
    pass

class ServiceUnavailableError(IntegrationAPIError):
    """Raised when an external service is temporarily unavailable."""
    pass