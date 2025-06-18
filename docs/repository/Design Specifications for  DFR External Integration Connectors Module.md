# DFR External Integration Connectors Module - Software Design Specification

## 1. Introduction

This document outlines the software design specification for the **DFR External Integration Connectors Module (`dfr_integrations`)**. This Odoo module is responsible for providing the client-side logic and adapters necessary to connect to various third-party external systems. These systems include, but are not limited to, National ID validation APIs, weather services, SMS/Email gateways, and payment platforms.

The primary goal of this module is to encapsulate the complexities of interacting with these external APIs, offering a clean and reusable service layer for other DFR modules to consume.

**Relevant Requirements:**
*   `REQ-API-007`: Readiness for integration with external systems.
*   `REQ-API-011`: Identification and documentation of external API details.
*   `REQ-FHR-006`: National ID input and optional KYC logic (implies integration).
*   `REQ-NS-004`: Integration-ready with third-party SMS/email gateway services.

## 2. Design Goals

*   **Modularity:** Each external service integration (client) should be implemented in a way that is independent and easily maintainable.
*   **Configurability:** API credentials, endpoints, and provider choices must be configurable per country instance through Odoo settings.
*   **Extensibility:** The design should allow for easy addition of new external service connectors or alternative implementations for existing services (e.g., different SMS providers).
*   **Robust Error Handling:** Clear and specific exceptions should be raised for different integration failures.
*   **Abstraction:** Provide a service layer within Odoo to abstract the direct client interactions from other DFR modules.
*   **Security:** Securely handle and store API credentials. All external communication must use HTTPS.

## 3. Architecture Overview

The `dfr_integrations` module will be an Odoo 18.0 Community addon. It follows a layered approach internally:

1.  **Configuration Models (`models/`):** Odoo models (extending `res.config.settings`) to store API credentials and configuration parameters.
2.  **Data Transfer Objects (DTOs - `dtos/`):** Python classes (Pydantic models or dataclasses) to represent structured data for requests and responses to external APIs, ensuring type safety and clarity.
3.  **API Clients (`clients/`):** Python classes responsible for the actual HTTP communication with external APIs.
    *   A `BaseApiClient` will provide common functionality (HTTP requests, error handling, logging).
    *   Specific clients will inherit from `BaseApiClient` or implement defined interfaces.
    *   Interfaces (ABCs) will be defined for services like SMS and Email gateways to allow for multiple provider implementations (Strategy Pattern).
4.  **Odoo Services (`services/`):** Odoo AbstractModels providing a higher-level API for other DFR modules to use. These services will utilize the API clients and handle Odoo-specific logic like configuration retrieval.
5.  **Custom Exceptions (`exceptions/`):** A set of custom Python exceptions for granular error reporting from client interactions.

This module primarily resides in the `dfr_integration` layer of the DFR platform architecture.

## 4. Detailed Design

### 4.1. Module Initialization

#### 4.1.1. `__init__.py`
*   **Purpose:** Initializes the Python package for the `dfr_integrations` Odoo module.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/__init__.py
    from . import models
    from . import exceptions
    from . import dtos
    from . import clients
    from . import services
    

#### 4.1.2. `__manifest__.py`
*   **Purpose:** Odoo manifest file.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/__manifest__.py
    {
        'name': 'DFR - External Integration Connectors',
        'version': '18.0.1.0.0',
        'summary': 'Module for connecting to various third-party external APIs.',
        'author': 'FAO DFR Project Team',
        'license': 'MIT',  # Or Apache 2.0 as per final decision
        'category': 'DigitalFarmerRegistry/Integrations',
        'depends': [
            'base',
            'mail',  # For potential fallback email sending and general Odoo mail features
            'dfr_common', # Assuming dfr_common is a dependency
        ],
        'data': [
            'security/ir.model.access.csv',
            'views/res_config_settings_views.xml',
            # Add other data files if any (e.g., security rules for services)
        ],
        'installable': True,
        'application': False,
        'auto_install': False,
    }
    

### 4.2. Custom Exceptions (`exceptions/`)

#### 4.2.1. `exceptions/__init__.py`
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/exceptions/__init__.py
    from .integration_exceptions import (
        IntegrationAPIError,
        ExternalServiceAuthenticationError,
        APITimeoutError,
        InvalidResponseError,
        ConfigurationError,
        ServiceUnavailableError,
    )
    

#### 4.2.2. `exceptions/integration_exceptions.py`
*   **Purpose:** Defines custom exceptions for external API integration failures.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/exceptions/integration_exceptions.py
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
    

### 4.3. Data Transfer Objects (DTOs - `dtos/`)

*Recommended library: Pydantic for data validation and serialization.*

#### 4.3.1. `dtos/__init__.py`
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/dtos/__init__.py
    from .national_id_api_dtos import NationalIdValidationRequest, NationalIdValidationResponse
    from .sms_api_dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig
    from .email_api_dtos import EmailSendRequest, EmailSendResponse, EmailAttachmentDTO, EmailProviderConfig
    # Add other DTO imports as needed (e.g., for weather, payment)
    

#### 4.3.2. `dtos/national_id_api_dtos.py`
*   **Purpose:** DTOs for National ID validation API.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/dtos/national_id_api_dtos.py
    from typing import Optional
    from datetime import date
    from pydantic import BaseModel, Field

    class NationalIdValidationRequest(BaseModel):
        id_number: str = Field(..., description="The National ID number to validate.")
        id_type: str = Field(..., description="The type of National ID (e.g., 'PASSPORT', 'NATIONAL_CARD').")
        country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code.")
        # Add any other parameters required by the specific National ID API

    class NationalIdValidationResponse(BaseModel):
        is_valid: bool = Field(..., description="Whether the ID is considered valid.")
        full_name: Optional[str] = Field(None, description="Validated full name associated with the ID.")
        date_of_birth: Optional[date] = Field(None, description="Validated date of birth.")
        # Include other validated fields like gender, address components if provided by API
        raw_response: Optional[dict] = Field(None, description="The raw response from the external API for debugging.")
        error_message: Optional[str] = Field(None, description="Error message if validation failed or an error occurred.")
        error_code: Optional[str] = Field(None, description="Specific error code from the external API.")
    

#### 4.3.3. `dtos/sms_api_dtos.py`
*   **Purpose:** DTOs for SMS gateway API.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/dtos/sms_api_dtos.py
    from typing import Optional
    from pydantic import BaseModel, Field

    class SmsSendRequest(BaseModel):
        recipient_phone: str = Field(..., description="Recipient's phone number in E.164 format.")
        message_body: str = Field(..., description="The content of the SMS message.")
        sender_id: Optional[str] = Field(None, description="Optional sender ID (alphanumeric).")
        # Add other common SMS parameters like `message_type` (e.g., 'text', 'unicode') if needed

    class SmsSendResponse(BaseModel):
        message_sid: Optional[str] = Field(None, description="Unique message identifier from the gateway.")
        status: str = Field(..., description="Dispatch status (e.g., 'queued', 'sent', 'failed', 'delivered').")
        error_code: Optional[str] = Field(None, description="Gateway-specific error code if sending failed.")
        error_message: Optional[str] = Field(None, description="Human-readable error message if sending failed.")
        raw_response: Optional[dict] = Field(None, description="The raw response from the SMS gateway.")

    class SmsProviderConfig(BaseModel):
        provider_name: str
        api_url: Optional[str] = None
        api_key: Optional[str] = None
        api_secret: Optional[str] = None # For Twilio account_sid, auth_token, etc.
        # Add other provider-specific fields
    

#### 4.3.4. `dtos/email_api_dtos.py`
*   **Purpose:** DTOs for Email gateway API.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/dtos/email_api_dtos.py
    from typing import Optional, List
    from pydantic import BaseModel, Field, EmailStr

    class EmailAttachmentDTO(BaseModel):
        filename: str
        content_base64: str # Base64 encoded content
        content_type: str # MIME type

    class EmailSendRequest(BaseModel):
        to_email: List[EmailStr] = Field(..., description="List of recipient email addresses.")
        from_email: EmailStr = Field(..., description="Sender email address.")
        reply_to_email: Optional[EmailStr] = Field(None, description="Optional reply-to email address.")
        subject: str = Field(..., description="Email subject.")
        html_body: Optional[str] = Field(None, description="HTML content of the email.")
        text_body: Optional[str] = Field(None, description="Plain text content of the email.")
        attachments: Optional[List[EmailAttachmentDTO]] = Field(None, description="List of attachments.")
        # Add cc, bcc if needed

    class EmailSendResponse(BaseModel):
        message_id: Optional[str] = Field(None, description="Unique message identifier from the gateway.")
        status: str = Field(..., description="Dispatch status (e.g., 'accepted', 'sent', 'failed').")
        error_message: Optional[str] = Field(None, description="Error message if sending failed.")
        raw_response: Optional[dict] = Field(None, description="The raw response from the email gateway.")

    class EmailProviderConfig(BaseModel):
        provider_name: str
        api_url: Optional[str] = None
        api_key: Optional[str] = None
        # Add other provider-specific fields
    

### 4.4. API Clients (`clients/`)

#### 4.4.1. `clients/__init__.py`
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/__init__.py
    from .base_client import BaseApiClient
    from .national_id_api_client import NationalIdApiClient
    from .sms_gateway_client_interface import SmsGatewayClientInterface
    from .sms_twilio_client import SmsTwilioClient
    # Import other SMS clients (e.g., Vonage) if implemented
    from .email_gateway_client_interface import EmailGatewayClientInterface
    from .email_sendgrid_client import EmailSendGridClient
    # Import other Email clients if implemented
    from .weather_service_client import WeatherServiceClient # Placeholder
    from .payment_platform_client import PaymentPlatformClient # Placeholder
    

#### 4.4.2. `clients/base_client.py`
*   **Purpose:** Abstract base class for external API clients.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/base_client.py
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
                raise ConfigurationError(f"{service_name}: Base URL not configured.")
            self.base_url = base_url.rstrip('/')
            self.api_key = api_key # Subclasses will handle specific auth mechanisms
            self.timeout_seconds = timeout_seconds
            self.session = requests.Session()
            self.service_name = service_name

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

            _logger.debug(f"Requesting {self.service_name}: {method} {url} PARAMS: {params} JSON_DATA: {json_data}")

            try:
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=headers,
                    timeout=self.timeout_seconds
                )
                _logger.debug(f"Response from {self.service_name}: Status {response.status_code}, Content: {response.text[:500]}...") # Log snippet

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
            try:
                error_details = response.json()
                error_message += f" - Details: {error_details}"
            except ValueError: # Not JSON
                error_message += f" - Content: {response.text[:200]}" # Log snippet

            _logger.error(error_message)

            if response.status_code in [401, 403]:
                raise ExternalServiceAuthenticationError(error_message, response.status_code, response.text)
            elif response.status_code == 400:
                raise InvalidResponseError(f"Bad Request to {self.service_name}. Check request parameters. {error_message}", response.status_code, response.text)
            elif response.status_code == 404:
                 raise InvalidResponseError(f"Resource not found on {self.service_name}. {error_message}", response.status_code, response.text)
            elif response.status_code >= 500:
                raise ServiceUnavailableError(f"{self.service_name} unavailable or internal error. {error_message}", response.status_code, response.text)
            else:
                raise IntegrationAPIError(error_message, response.status_code, response.text)

    

#### 4.4.3. `clients/national_id_api_client.py`
*   **Purpose:** Client for National ID validation API.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/national_id_api_client.py
    import logging
    from .base_client import BaseApiClient
    from odoo.addons.dfr_integrations.dtos import NationalIdValidationRequest, NationalIdValidationResponse
    from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError

    _logger = logging.getLogger(__name__)

    class NationalIdApiClient(BaseApiClient):
        def __init__(self, base_url: str, api_key: str, timeout_seconds: int = 10):
            if not api_key:
                raise ConfigurationError("National ID API Key not configured.")
            super().__init__(base_url=base_url, api_key=api_key, timeout_seconds=timeout_seconds, service_name="NationalIDService")
            # Specific initialization for this client if needed

        def _get_headers(self) -> dict:
            headers = super()._get_headers()
            # Example: Add API key to headers if required by the specific API
            # This depends on how the actual National ID API expects authentication
            headers['X-API-Key'] = self.api_key # Or 'Authorization': f'Bearer {self.api_key}'
            return headers

        def validate_national_id(self, request_dto: NationalIdValidationRequest) -> NationalIdValidationResponse:
            _logger.info(f"Validating National ID: {request_dto.id_number} (Type: {request_dto.id_type}) for country {request_dto.country_code}")
            try:
                # Endpoint should be configurable or a constant for this client
                response = self._request(
                    method='POST',
                    endpoint='/validate_id', # Example endpoint
                    json_data=request_dto.model_dump(exclude_none=True)
                )
                response_data = response.json()
                return NationalIdValidationResponse(**response_data, raw_response=response_data)
            except InvalidResponseError as e: # Catch specific error from base client
                _logger.error(f"Invalid response during National ID validation: {e.message}")
                # Potentially parse e.response_content if it contains structured error from external API
                return NationalIdValidationResponse(is_valid=False, error_message=e.message, error_code=str(e.status_code), raw_response=e.response_content if isinstance(e.response_content,dict) else {"error_text": str(e.response_content)})
            except Exception as e: # Catch other errors (timeout, connection, etc.)
                _logger.error(f"Error validating National ID: {e}", exc_info=True)
                return NationalIdValidationResponse(is_valid=False, error_message=str(e))
    

#### 4.4.4. `clients/sms_gateway_client_interface.py`
*   **Purpose:** ABC for SMS gateway clients.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/sms_gateway_client_interface.py
    from abc import ABC, abstractmethod
    from odoo.addons.dfr_integrations.dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig

    class SmsGatewayClientInterface(ABC):
        def __init__(self, config: SmsProviderConfig):
            self.config = config
            super().__init__()

        @abstractmethod
        def send_sms(self, request_dto: SmsSendRequest) -> SmsSendResponse:
            """Sends an SMS message."""
            pass
    

#### 4.4.5. `clients/sms_twilio_client.py`
*   **Purpose:** Twilio SMS client implementation.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/sms_twilio_client.py
    import logging
    from .base_client import BaseApiClient
    from .sms_gateway_client_interface import SmsGatewayClientInterface
    from odoo.addons.dfr_integrations.dtos import SmsSendRequest, SmsSendResponse, SmsProviderConfig
    from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError
    from requests.auth import HTTPBasicAuth

    _logger = logging.getLogger(__name__)

    class SmsTwilioClient(BaseApiClient, SmsGatewayClientInterface):
        def __init__(self, config: SmsProviderConfig, timeout_seconds: int = 10):
            if not config.api_key or not config.api_secret: # Using api_key for Account SID, api_secret for Auth Token
                raise ConfigurationError("Twilio Account SID or Auth Token not configured.")
            
            # Twilio base URL usually includes Account SID
            # Example: https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}
            # The service/config should provide the full base_url or components to build it
            if not config.api_url:
                 raise ConfigurationError("Twilio API base URL not configured (should include Account SID).")

            super(BaseApiClient, self).__init__(
                base_url=config.api_url, # This should be the full path up to /Messages.json for Twilio
                timeout_seconds=timeout_seconds, 
                service_name="TwilioSMS"
            )
            SmsGatewayClientInterface.__init__(self, config) # Call ABC's init
            self.auth = HTTPBasicAuth(self.config.api_key, self.config.api_secret)


        def _get_headers(self) -> dict:
            # Twilio typically uses Basic Auth, not custom headers for auth, handled by requests.auth
            # Content-Type for Twilio is application/x-www-form-urlencoded
            return {'Accept': 'application/json'} # Twilio can return JSON

        def send_sms(self, request_dto: SmsSendRequest) -> SmsSendResponse:
            _logger.info(f"Sending SMS via Twilio to {request_dto.recipient_phone}")
            payload = {
                'To': request_dto.recipient_phone,
                'Body': request_dto.message_body,
            }
            if request_dto.sender_id: # Twilio uses 'From'
                payload['From'] = request_dto.sender_id
            elif self.config.extra_config and self.config.extra_config.get('default_sender_id'): # Assuming SmsProviderConfig can have extra_config
                 payload['From'] = self.config.extra_config.get('default_sender_id')
            else:
                raise ConfigurationError("Twilio sender ID ('From' number) not configured.")

            try:
                # Twilio's message creation endpoint is typically /Messages.json
                # The base_url from config should point to /Accounts/{ACCOUNT_SID}
                response = self.session.post( # Using session directly for Basic Auth
                    f"{self.base_url}/Messages.json", 
                    data=payload,
                    auth=self.auth,
                    headers=self._get_headers(), # Get other headers like Accept
                    timeout=self.timeout_seconds
                )
                
                _logger.debug(f"Twilio Response: Status {response.status_code}, Content: {response.text[:200]}")

                if response.status_code not in [200, 201]: # Twilio success is 201 Created
                     self._handle_api_error(response) # Let base_client handle general errors or override for Twilio specific

                response_data = response.json()
                return SmsSendResponse(
                    message_sid=response_data.get('sid'),
                    status=response_data.get('status'), # e.g., 'queued', 'sent', 'failed'
                    error_code=response_data.get('error_code'),
                    error_message=response_data.get('error_message'),
                    raw_response=response_data
                )
            except InvalidResponseError as e:
                _logger.error(f"Invalid Twilio response: {e.message}")
                return SmsSendResponse(status='failed', error_message=e.message, raw_response=e.response_content if isinstance(e.response_content,dict) else {"error_text": str(e.response_content)})
            except Exception as e:
                _logger.error(f"Error sending SMS via Twilio: {e}", exc_info=True)
                return SmsSendResponse(status='failed', error_message=str(e))
    
    *Note: Twilio client uses form-encoded data and Basic Auth, so it slightly deviates from pure `BaseApiClient` JSON flow but can still use its error handling.*

#### 4.4.6. `clients/email_gateway_client_interface.py`
*   **Purpose:** ABC for Email gateway clients.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/email_gateway_client_interface.py
    from abc import ABC, abstractmethod
    from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig

    class EmailGatewayClientInterface(ABC):
        def __init__(self, config: EmailProviderConfig):
            self.config = config
            super().__init__()

        @abstractmethod
        def send_email(self, request_dto: EmailSendRequest) -> EmailSendResponse:
            """Sends an email message."""
            pass
    

#### 4.4.7. `clients/email_sendgrid_client.py`
*   **Purpose:** SendGrid Email client implementation.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/email_sendgrid_client.py
    import logging
    from .base_client import BaseApiClient
    from .email_gateway_client_interface import EmailGatewayClientInterface
    from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig
    from odoo.addons.dfr_integrations.exceptions import ConfigurationError, InvalidResponseError

    _logger = logging.getLogger(__name__)

    class EmailSendGridClient(BaseApiClient, EmailGatewayClientInterface):
        def __init__(self, config: EmailProviderConfig, timeout_seconds: int = 15):
            if not config.api_key:
                raise ConfigurationError("SendGrid API Key not configured.")
            if not config.api_url:
                config.api_url = 'https://api.sendgrid.com/v3' # Default SendGrid API URL

            super(BaseApiClient, self).__init__(
                base_url=config.api_url, 
                api_key=config.api_key, # Store api_key for _get_headers
                timeout_seconds=timeout_seconds, 
                service_name="SendGridEmail"
            )
            EmailGatewayClientInterface.__init__(self, config)

        def _get_headers(self) -> dict:
            headers = super()._get_headers()
            headers['Authorization'] = f'Bearer {self.api_key}'
            return headers

        def send_email(self, request_dto: EmailSendRequest) -> EmailSendResponse:
            _logger.info(f"Sending email via SendGrid to {request_dto.to_email}")
            
            # Construct SendGrid payload
            personalizations = [{"to": [{"email": email} for email in request_dto.to_email]}]
            if request_dto.reply_to_email:
                reply_to = {"email": request_dto.reply_to_email}
            else:
                reply_to = None

            content = []
            if request_dto.text_body:
                content.append({"type": "text/plain", "value": request_dto.text_body})
            if request_dto.html_body:
                content.append({"type": "text/html", "value": request_dto.html_body})
            
            if not content:
                 raise ValueError("Email must have either text_body or html_body.")

            sendgrid_payload = {
                "personalizations": personalizations,
                "from": {"email": request_dto.from_email},
                "subject": request_dto.subject,
                "content": content,
            }
            if reply_to:
                sendgrid_payload["reply_to"] = reply_to
            
            if request_dto.attachments:
                sendgrid_payload["attachments"] = [
                    {
                        "content": att.content_base64,
                        "filename": att.filename,
                        "type": att.content_type,
                        "disposition": "attachment" # or "inline"
                    } for att in request_dto.attachments
                ]

            try:
                response = self._request(
                    method='POST',
                    endpoint='/mail/send', # SendGrid mail send endpoint
                    json_data=sendgrid_payload,
                    expected_status_codes=[202] # SendGrid returns 202 Accepted
                )
                # SendGrid returns an empty body on 202, message_id is in headers
                message_id = response.headers.get('X-Message-Id')
                return EmailSendResponse(status='accepted', message_id=message_id, raw_response={})

            except InvalidResponseError as e: # Catch specific error from base client
                _logger.error(f"Invalid SendGrid response: {e.message}")
                return EmailSendResponse(status='failed', error_message=e.message, raw_response=e.response_content if isinstance(e.response_content,dict) else {"error_text": str(e.response_content)})
            except Exception as e:
                _logger.error(f"Error sending email via SendGrid: {e}", exc_info=True)
                return EmailSendResponse(status='failed', error_message=str(e))
    

#### 4.4.8. `clients/weather_service_client.py` (Placeholder)
*   **Purpose:** Placeholder for Weather Service API client.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/weather_service_client.py
    import logging
    from typing import Optional, Dict, Any
    from .base_client import BaseApiClient
    from odoo.addons.dfr_integrations.exceptions import ConfigurationError

    _logger = logging.getLogger(__name__)

    class WeatherServiceClient(BaseApiClient):
        def __init__(self, base_url: str, api_key: str, timeout_seconds: int = 10):
            if not api_key:
                raise ConfigurationError("Weather Service API Key not configured.")
            super().__init__(base_url=base_url, api_key=api_key, timeout_seconds=timeout_seconds, service_name="WeatherService")

        def _get_headers(self) -> dict:
            headers = super()._get_headers()
            # Add specific auth if needed, e.g., headers['apikey'] = self.api_key
            return headers

        def get_forecast(self, latitude: float, longitude: float, date_str: Optional[str] = None) -> Dict[str, Any]:
            _logger.info(f"Fetching weather forecast for lat: {latitude}, lon: {longitude}, date: {date_str}")
            params = {'lat': latitude, 'lon': longitude}
            if date_str:
                params['date'] = date_str
            
            # This is a placeholder - actual endpoint and DTOs would depend on the specific weather API
            # response = self._request(method='GET', endpoint='/forecast', params=params)
            # response_data = response.json()
            # return WeatherForecastResponseDTO(**response_data) # Assuming a DTO
            _logger.warning("WeatherServiceClient.get_forecast is a placeholder and not implemented.")
            return {"status": "placeholder", "message": "Weather service integration not fully implemented."}
    

#### 4.4.9. `clients/payment_platform_client.py` (Placeholder)
*   **Purpose:** Placeholder for Payment Platform API client.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/clients/payment_platform_client.py
    import logging
    from typing import Dict, Any
    from .base_client import BaseApiClient
    from odoo.addons.dfr_integrations.exceptions import ConfigurationError

    _logger = logging.getLogger(__name__)

    class PaymentPlatformClient(BaseApiClient):
        def __init__(self, base_url: str, api_key: str, secret_key: Optional[str] = None, timeout_seconds: int = 20):
            # Authentication method might vary greatly (API Key, OAuth, HMAC, etc.)
            if not api_key: # Or other primary credential
                raise ConfigurationError("Payment Platform API Key not configured.")
            super().__init__(base_url=base_url, api_key=api_key, timeout_seconds=timeout_seconds, service_name="PaymentPlatform")
            self.secret_key = secret_key 

        def _get_headers(self) -> dict:
            headers = super()._get_headers()
            # Add specific auth headers based on the payment platform's requirements
            # e.g., headers['Authorization'] = f'Bearer {self.api_key}'
            return headers

        def initiate_payment(self, payment_details: Dict[str, Any]) -> Dict[str, Any]:
            _logger.info(f"Initiating payment with details: {payment_details}")
            # Placeholder - actual implementation depends on the payment API
            # response = self._request(method='POST', endpoint='/payments', json_data=payment_details)
            # return response.json() # Assuming a PaymentResponseDTO
            _logger.warning("PaymentPlatformClient.initiate_payment is a placeholder.")
            return {"status": "placeholder", "message": "Payment initiation not fully implemented."}

        def check_payment_status(self, transaction_id: str) -> Dict[str, Any]:
            _logger.info(f"Checking payment status for transaction ID: {transaction_id}")
            # Placeholder - actual implementation depends on the payment API
            # response = self._request(method='GET', endpoint=f'/payments/{transaction_id}/status')
            # return response.json() # Assuming a PaymentStatusResponseDTO
            _logger.warning("PaymentPlatformClient.check_payment_status is a placeholder.")
            return {"status": "placeholder", "message": "Payment status check not fully implemented."}
    

### 4.5. Odoo Services (`services/`)

#### 4.5.1. `services/__init__.py`
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/services/__init__.py
    from . import national_id_validation_service
    from . import sms_dispatch_service
    from . import email_dispatch_service
    # Import other services (weather, payment) if they are created
    

#### 4.5.2. `services/national_id_validation_service.py`
*   **Purpose:** Odoo service for National ID validation.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/services/national_id_validation_service.py
    import logging
    from odoo import api, models, _
    from odoo.exceptions import UserError
    from odoo.addons.dfr_integrations.clients import NationalIdApiClient
    from odoo.addons.dfr_integrations.dtos import NationalIdValidationRequest, NationalIdValidationResponse
    from odoo.addons.dfr_integrations.exceptions import IntegrationAPIError, ConfigurationError

    _logger = logging.getLogger(__name__)

    class NationalIdValidationService(models.AbstractModel):
        _name = 'dfr.national.id.validation.service'
        _description = 'DFR National ID Validation Service'

        def _get_client(self) -> NationalIdApiClient:
            ICP = self.env['ir.config_parameter'].sudo()
            api_url = ICP.get_param('dfr_integrations.national_id_api_url')
            api_key = ICP.get_param('dfr_integrations.national_id_api_key')
            
            if not api_url:
                _logger.error("National ID API URL not configured.")
                raise ConfigurationError(_("National ID Validation Service is not configured (URL missing). Please contact administrator."))
            if not api_key: # API key might be optional depending on the service
                _logger.warning("National ID API Key not configured. Service might fail if key is required.")
                # Depending on API, this might be an error or just a warning
                # raise ConfigurationError(_("National ID Validation Service is not configured (API Key missing). Please contact administrator."))


            # Timeout can also be a config parameter
            timeout_seconds = int(ICP.get_param('dfr_integrations.national_id_api_timeout', '10'))
            
            return NationalIdApiClient(base_url=api_url, api_key=api_key, timeout_seconds=timeout_seconds)

        @api.model
        def validate_id(self, id_number: str, id_type: str, country_code: str) -> NationalIdValidationResponse:
            """
            Validates a National ID using the configured external service.
            :return: NationalIdValidationResponse DTO
            :raises: UserError if service is not configured or a non-recoverable API error occurs.
            """
            _logger.info(f"Service call: Validate ID {id_number} (type: {id_type}, country: {country_code})")
            try:
                client = self._get_client()
                request_dto = NationalIdValidationRequest(
                    id_number=id_number,
                    id_type=id_type,
                    country_code=country_code
                )
                response_dto = client.validate_national_id(request_dto)
                if not response_dto.is_valid and response_dto.error_message:
                     _logger.warning(f"National ID validation failed for {id_number}: {response_dto.error_message}")
                return response_dto
            except ConfigurationError as e:
                _logger.error(f"Configuration error for National ID Validation Service: {e}")
                raise UserError(str(e)) # Propagate config error to user
            except IntegrationAPIError as e:
                _logger.error(f"API error during National ID validation: {e.message}", exc_info=True)
                # For API errors, we might not want to show raw technical details to end user
                # Return a response indicating failure rather than raising UserError that halts flow
                return NationalIdValidationResponse(is_valid=False, error_message=_("Could not connect to the ID validation service or an error occurred."), raw_response={"error": str(e)})
            except Exception as e:
                _logger.error(f"Unexpected error in National ID Validation Service: {e}", exc_info=True)
                return NationalIdValidationResponse(is_valid=False, error_message=_("An unexpected error occurred during ID validation."), raw_response={"error": str(e)})

    

#### 4.5.3. `services/sms_dispatch_service.py`
*   **Purpose:** Odoo service for sending SMS.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/services/sms_dispatch_service.py
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
    from typing import Optional

    _logger = logging.getLogger(__name__)

    class SmsDispatchService(models.AbstractModel):
        _name = 'dfr.sms.dispatch.service'
        _description = 'DFR SMS Dispatch Service'

        # Map provider names from config to client classes
        PROVIDER_CLIENT_MAP = {
            'twilio': SmsTwilioClient,
            # 'vonage': SmsVonageClient, # Add other providers here
            # 'other': CustomOtherSmsClient
        }

        def _get_configured_sms_client(self) -> Optional[SmsGatewayClientInterface]:
            ICP = self.env['ir.config_parameter'].sudo()
            provider_name = ICP.get_param('dfr_integrations.sms_gateway_provider')

            if not provider_name or provider_name == 'none': # Assuming 'none' can be a choice
                _logger.info("SMS Gateway provider not configured or set to 'none'. SMS will not be sent via external gateway.")
                return None

            client_class = self.PROVIDER_CLIENT_MAP.get(provider_name)
            if not client_class:
                _logger.error(f"Unsupported SMS gateway provider configured: {provider_name}")
                raise ConfigurationError(_(f"Unsupported SMS gateway provider: {provider_name}"))

            # Gather config for the specific provider
            # This part needs to be flexible for different providers
            if provider_name == 'twilio':
                config = SmsProviderConfig(
                    provider_name=provider_name,
                    api_key=ICP.get_param('dfr_integrations.sms_twilio_account_sid'), # Using api_key for SID
                    api_secret=ICP.get_param('dfr_integrations.sms_twilio_auth_token'), # Using api_secret for Auth Token
                    api_url=ICP.get_param('dfr_integrations.sms_twilio_api_url', f"https://api.twilio.com/2010-04-01/Accounts/{ICP.get_param('dfr_integrations.sms_twilio_account_sid')}"), # Default Twilio URL structure
                    # Example for extra config:
                    # extra_config={'default_sender_id': ICP.get_param('dfr_integrations.sms_twilio_default_sender_id')}
                )
            # Add elif blocks for other providers (Vonage, SendGrid SMS, etc.)
            # elif provider_name == 'vonage':
            #     config = SmsProviderConfig(...)
            else: # For 'other' or unmapped configured providers
                # This generic config might not be enough for 'other', specific handling or error needed
                config = SmsProviderConfig(
                    provider_name=provider_name,
                    api_url=ICP.get_param('dfr_integrations.sms_gateway_url'),
                    api_key=ICP.get_param('dfr_integrations.sms_gateway_api_key'),
                    api_secret=ICP.get_param('dfr_integrations.sms_gateway_secret')
                )
            
            if not config.api_url and provider_name != 'twilio': # Twilio builds its URL often
                 _logger.warning(f"API URL not set for SMS provider {provider_name}, but may not be required by all.")
            
            timeout = int(ICP.get_param('dfr_integrations.sms_gateway_timeout', '10'))
            
            try:
                return client_class(config=config, timeout_seconds=timeout) # Pass timeout if client supports it
            except ConfigurationError as e:
                _logger.error(f"Configuration error initializing SMS client {provider_name}: {e}")
                raise # Re-raise to be caught by sender
            except Exception as e:
                _logger.error(f"Error initializing SMS client {provider_name}: {e}", exc_info=True)
                raise ConfigurationError(_(f"Could not initialize SMS client {provider_name}: {e}"))


        @api.model
        def send_sms_message(self, recipient_phone: str, message_body: str, sender_id: Optional[str] = None, country_id: Optional[int] = None) -> SmsSendResponse:
            """
            Sends an SMS message using the configured gateway.
            Country_id can be passed to fetch country-specific configurations if settings are per-company/country.
            """
            _logger.info(f"Service call: Send SMS to {recipient_phone} (sender: {sender_id})")
            
            # If configurations are company-specific, you might need to switch context
            # env_context = self.env
            # if country_id:
            #     company = self.env['res.company'].search([('partner_id.country_id', '=', country_id)], limit=1)
            #     if company:
            #         env_context = self.with_company(company)
            
            try:
                client = self._get_configured_sms_client() # Potentially pass env_context to _get_client
                if not client:
                    _logger.warning("SMS sending skipped: No SMS client configured or available.")
                    return SmsSendResponse(status='skipped', error_message="No SMS client configured.")

                request_dto = SmsSendRequest(
                    recipient_phone=recipient_phone,
                    message_body=message_body,
                    sender_id=sender_id
                )
                response_dto = client.send_sms(request_dto)
                if response_dto.status != 'sent' and response_dto.status != 'queued' and response_dto.status != 'accepted': # Check for various success statuses
                     _logger.error(f"SMS sending to {recipient_phone} failed/not sent by gateway: {response_dto.status} - {response_dto.error_message}")
                return response_dto
            except ConfigurationError as e:
                _logger.error(f"Configuration error for SMS Dispatch Service: {e}")
                # Don't raise UserError here as this service might be called from automated actions
                return SmsSendResponse(status='config_error', error_message=str(e))
            except IntegrationAPIError as e:
                _logger.error(f"API error during SMS dispatch: {e.message}", exc_info=True)
                return SmsSendResponse(status='api_error', error_message=e.message, raw_response=e.response_content if isinstance(e.response_content,dict) else {"error_text": str(e.response_content)})
            except Exception as e:
                _logger.error(f"Unexpected error in SMS Dispatch Service: {e}", exc_info=True)
                return SmsSendResponse(status='error', error_message=str(e))
    

#### 4.5.4. `services/email_dispatch_service.py`
*   **Purpose:** Odoo service for sending Email.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/services/email_dispatch_service.py
    import logging
    from odoo import api, models, _
    from odoo.exceptions import UserError
    from odoo.addons.dfr_integrations.clients import (
        EmailGatewayClientInterface, 
        EmailSendGridClient # Example
    )
    from odoo.addons.dfr_integrations.dtos import EmailSendRequest, EmailSendResponse, EmailProviderConfig, EmailAttachmentDTO
    from odoo.addons.dfr_integrations.exceptions import IntegrationAPIError, ConfigurationError
    from typing import Optional, List, Union
    import base64

    _logger = logging.getLogger(__name__)

    class EmailDispatchService(models.AbstractModel):
        _name = 'dfr.email.dispatch.service'
        _description = 'DFR Email Dispatch Service'

        PROVIDER_CLIENT_MAP = {
            'sendgrid': EmailSendGridClient,
            # Add other providers here
        }

        def _get_configured_email_client(self) -> Optional[EmailGatewayClientInterface]:
            ICP = self.env['ir.config_parameter'].sudo()
            provider_name = ICP.get_param('dfr_integrations.email_gateway_provider')

            if not provider_name or provider_name == 'odoo' or provider_name == 'none':
                _logger.info("External email gateway not configured or set to 'odoo'/'none'. Will use Odoo's internal mail system if needed.")
                return None

            client_class = self.PROVIDER_CLIENT_MAP.get(provider_name)
            if not client_class:
                _logger.error(f"Unsupported email gateway provider configured: {provider_name}")
                raise ConfigurationError(_(f"Unsupported email gateway provider: {provider_name}"))

            if provider_name == 'sendgrid':
                config = EmailProviderConfig(
                    provider_name=provider_name,
                    api_key=ICP.get_param('dfr_integrations.email_sendgrid_api_key'), # Example for SendGrid
                    api_url=ICP.get_param('dfr_integrations.email_sendgrid_api_url', 'https://api.sendgrid.com/v3')
                )
            # Add elif for other providers
            else:
                config = EmailProviderConfig(
                    provider_name=provider_name,
                    api_url=ICP.get_param(f'dfr_integrations.email_{provider_name}_api_url'), # Generic pattern
                    api_key=ICP.get_param(f'dfr_integrations.email_{provider_name}_api_key')
                )
            
            if not config.api_key:
                 _logger.error(f"API Key not configured for email provider {provider_name}")
                 raise ConfigurationError(_(f"API Key not configured for email provider {provider_name}"))

            timeout = int(ICP.get_param('dfr_integrations.email_gateway_timeout', '15'))
            try:
                return client_class(config=config, timeout_seconds=timeout)
            except ConfigurationError as e:
                _logger.error(f"Configuration error initializing email client {provider_name}: {e}")
                raise
            except Exception as e:
                _logger.error(f"Error initializing email client {provider_name}: {e}", exc_info=True)
                raise ConfigurationError(_(f"Could not initialize email client {provider_name}: {e}"))

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
                to_emails_list = [to_emails]
            else:
                to_emails_list = to_emails

            _logger.info(f"Service call: Send Email to {', '.join(to_emails_list)} with subject: {subject}")
            
            ICP = self.env['ir.config_parameter'].sudo()
            final_from_email = from_email_str or ICP.get_param('dfr_integrations.default_email_from') or ICP.get_param('mail.default.from')
            
            if not final_from_email:
                _logger.error("Default 'from' email address not configured for sending emails.")
                return EmailSendResponse(status='config_error', error_message="Default 'from' email not configured.") if self._get_configured_email_client() else False # Match return type

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
                        attachments=attachments
                    )
                    response_dto = external_client.send_email(request_dto)
                    if response_dto.status != 'accepted' and response_dto.status != 'sent' and response_dto.status != 'queued':
                         _logger.error(f"Email sending to {to_emails_list} failed/not sent by gateway: {response_dto.status} - {response_dto.error_message}")
                    return response_dto
                else:
                    _logger.info("Using Odoo's internal mail system for sending email.")
                    mail_values = {
                        'subject': subject,
                        'body_html': body_html or (body_text.replace('\n', '<br/>') if body_text else ''),
                        'email_to': ','.join(to_emails_list),
                        'email_from': final_from_email,
                        'auto_delete': True, # Or False depending on policy
                    }
                    if reply_to_email_str:
                        mail_values['reply_to'] = reply_to_email_str
                    if mail_server_id:
                         mail_values['mail_server_id'] = mail_server_id
                    
                    mail = self.env['mail.mail'].sudo().create(mail_values)
                    
                    if attachments:
                        attachment_ids = []
                        for att_dto in attachments:
                            try:
                                attachment_ids.append(self.env['ir.attachment'].sudo().create({
                                    'name': att_dto.filename,
                                    'datas': att_dto.content_base64, # Already base64
                                    'mimetype': att_dto.content_type,
                                    'res_model': 'mail.message', # Or link to a specific record if available
                                    'res_id': 0, # Needs a res_id if linked to a specific record's chatter
                                }).id)
                            except Exception as att_err:
                                _logger.error(f"Failed to create attachment {att_dto.filename}: {att_err}")
                        if attachment_ids:
                            mail.attachment_ids = [(6, 0, attachment_ids)]
                            
                    mail.send()
                    _logger.info(f"Email to {to_emails_list} queued via Odoo internal mail system (ID: {mail.id}).")
                    return True # Odoo's send() doesn't return rich status directly, assumes success if no exception

            except ConfigurationError as e:
                _logger.error(f"Configuration error for Email Dispatch Service: {e}")
                return EmailSendResponse(status='config_error', error_message=str(e)) if external_client else False
            except IntegrationAPIError as e:
                _logger.error(f"API error during email dispatch: {e.message}", exc_info=True)
                return EmailSendResponse(status='api_error', error_message=e.message, raw_response=e.response_content if isinstance(e.response_content,dict) else {"error_text": str(e.response_content)})
            except Exception as e:
                _logger.error(f"Unexpected error in Email Dispatch Service: {e}", exc_info=True)
                return EmailSendResponse(status='error', error_message=str(e)) if external_client else False
    

### 4.6. Odoo Models (`models/`)

#### 4.6.1. `models/__init__.py`
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/models/__init__.py
    from . import res_config_settings
    

#### 4.6.2. `models/res_config_settings.py`
*   **Purpose:** Extends Odoo settings for external integration parameters.
*   **Logic:**
    python
    # dfr_addons/dfr_integrations/models/res_config_settings.py
    from odoo import fields, models

    class ResConfigSettings(models.TransientModel):
        _inherit = 'res.config.settings'

        # National ID Validation Settings
        dfr_national_id_api_url = fields.Char(
            string="National ID API URL",
            config_parameter='dfr_integrations.national_id_api_url',
            help="Base URL for the National ID Validation API."
        )
        dfr_national_id_api_key = fields.Char(
            string="National ID API Key",
            config_parameter='dfr_integrations.national_id_api_key',
            help="API Key for the National ID Validation Service."
        )
        dfr_national_id_api_timeout = fields.Integer(
            string="National ID API Timeout (s)",
            config_parameter='dfr_integrations.national_id_api_timeout',
            default=10,
            help="Timeout in seconds for National ID API requests."
        )

        # SMS Gateway Settings
        dfr_sms_gateway_provider = fields.Selection(
            string="SMS Gateway Provider",
            config_parameter='dfr_integrations.sms_gateway_provider',
            selection=[
                ('none', 'None (Disable External SMS)'),
                ('twilio', 'Twilio'),
                ('vonage', 'Vonage (Placeholder)'), # Add actual providers
                ('other', 'Other (Manual Config)')
            ],
            default='none',
            help="Select the SMS gateway provider."
        )
        # Twilio Specific (example)
        dfr_sms_twilio_account_sid = fields.Char(
            string="Twilio Account SID",
            config_parameter='dfr_integrations.sms_twilio_account_sid'
        )
        dfr_sms_twilio_auth_token = fields.Char(
            string="Twilio Auth Token",
            config_parameter='dfr_integrations.sms_twilio_auth_token'
        )
        dfr_sms_twilio_api_url = fields.Char( # Allow override, service might construct default
            string="Twilio API Base URL",
            config_parameter='dfr_integrations.sms_twilio_api_url',
            help="E.g., https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID"
        )
        dfr_sms_twilio_default_sender_id = fields.Char(
            string="Twilio Default Sender ID/Number",
            config_parameter='dfr_integrations.sms_twilio_default_sender_id'
        )
        
        # Generic 'Other' SMS provider settings (less ideal, but for flexibility)
        dfr_sms_gateway_url = fields.Char(
            string="Other SMS Gateway URL",
            config_parameter='dfr_integrations.sms_gateway_url'
        )
        dfr_sms_gateway_api_key = fields.Char(
            string="Other SMS Gateway API Key",
            config_parameter='dfr_integrations.sms_gateway_api_key'
        )
        dfr_sms_gateway_secret = fields.Char(
            string="Other SMS Gateway Secret/Token",
            config_parameter='dfr_integrations.sms_gateway_secret'
        )
        dfr_sms_gateway_timeout = fields.Integer(
            string="SMS Gateway Timeout (s)",
            config_parameter='dfr_integrations.sms_gateway_timeout',
            default=10
        )

        # Email Gateway Settings
        dfr_email_gateway_provider = fields.Selection(
            string="Email Gateway Provider",
            config_parameter='dfr_integrations.email_gateway_provider',
            selection=[
                ('odoo', 'Odoo Default Mail Server'),
                ('sendgrid', 'SendGrid'),
                # ('mailgun', 'Mailgun (Placeholder)'),
                ('other', 'Other (Manual Config)')
            ],
            default='odoo',
            help="Select the Email gateway provider. 'Odoo Default' uses built-in Odoo mail servers."
        )
        # SendGrid Specific (example)
        dfr_email_sendgrid_api_key = fields.Char(
            string="SendGrid API Key",
            config_parameter='dfr_integrations.email_sendgrid_api_key'
        )
        dfr_email_sendgrid_api_url = fields.Char(
            string="SendGrid API Base URL",
            config_parameter='dfr_integrations.email_sendgrid_api_url',
            default='https://api.sendgrid.com/v3'
        )
        
        dfr_default_email_from = fields.Char(
            string="Default 'From' Email Address",
            config_parameter='dfr_integrations.default_email_from',
            help="Default sender address for emails if not specified per message. Overrides Odoo's system default if set."
        )
        dfr_email_gateway_timeout = fields.Integer(
            string="Email Gateway Timeout (s)",
            config_parameter='dfr_integrations.email_gateway_timeout',
            default=15
        )

        # Placeholder for Weather Service Config
        dfr_weather_service_api_url = fields.Char(string="Weather Service API URL", config_parameter='dfr_integrations.weather_api_url')
        dfr_weather_service_api_key = fields.Char(string="Weather Service API Key", config_parameter='dfr_integrations.weather_api_key')
        
        # Placeholder for Payment Platform Config
        dfr_payment_platform_api_url = fields.Char(string="Payment Platform API URL", config_parameter='dfr_integrations.payment_api_url')
        dfr_payment_platform_api_key = fields.Char(string="Payment Platform API Key", config_parameter='dfr_integrations.payment_api_key')
        dfr_payment_platform_secret_key = fields.Char(string="Payment Platform Secret Key", config_parameter='dfr_integrations.payment_secret_key')

    
*   **Associated View (`views/res_config_settings_views.xml` - Out of scope for this JSON but critical):**
    An XML view extending `res_config_settings_view_form` to display these fields in Odoo's general settings, typically grouped in a new section.

### 4.7. Security (`security/ir.model.access.csv`)
*   **Purpose:** Define access rights for any new models or to control access to services if needed.
*   **Logic:**
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    # Access for system administrators to configure settings
    access_res_config_settings_dfr_integrations,dfr.integrations.res.config.settings,model_res_config_settings,base.group_system,1,1,1,1
    # If services are directly callable via XML-RPC by certain groups (unlikely for these internal services)
    # access_dfr_national_id_validation_service_user,dfr.nid.validation.service.user,model_dfr_national_id_validation_service,base.group_user,1,0,0,0 
    
    *Note: Access to AbstractModel services is typically controlled by the calling model's permissions or Python code-level checks, not directly via `ir.model.access.csv` for the service model itself unless it's made accessible via other means.*

## 5. Error Handling Strategy

*   **Client-Level:** `BaseApiClient` and its derivatives will catch `requests.exceptions` (Timeout, ConnectionError, etc.) and raise corresponding custom exceptions from `dfr_integrations.exceptions` (e.g., `APITimeoutError`, `IntegrationAPIError`). They will also parse HTTP error statuses (4xx, 5xx) from external APIs and raise specific exceptions like `ExternalServiceAuthenticationError`, `InvalidResponseError`, or `ServiceUnavailableError`.
*   **Service-Level:** Odoo services (`dfr.national.id.validation.service`, etc.) will:
    *   Catch `ConfigurationError` and propagate it as an Odoo `UserError` if the service cannot operate due to missing configuration, providing feedback to the administrator.
    *   Catch other `IntegrationAPIError` subtypes from clients. For user-initiated actions (e.g., manual ID validation check), they might raise a `UserError` with a user-friendly message. For background/automated processes, they should log the error thoroughly and return a status/DTO indicating failure (e.g., `NationalIdValidationResponse(is_valid=False, error_message=...)`). This prevents halting critical background tasks due to transient external API issues.
*   **Logging:** All caught exceptions will be logged with relevant context (e.g., service name, input parameters (sanitized), external API response if available).

## 6. Logging Strategy

*   **Standard Logger:** Use `_logger = logging.getLogger(__name__)` in all Python files.
*   **`BaseApiClient`:**
    *   DEBUG: Log outgoing request details (method, URL, sanitized headers, sanitized payload).
    *   DEBUG: Log incoming response details (status code, snippet of response body).
    *   ERROR: Log details when an API error is encountered (status code, full error message, response body if helpful).
*   **Specific Clients:**
    *   INFO: Log key actions (e.g., "Sending SMS via Twilio to +123...").
*   **Services:**
    *   INFO: Log service invocation with key parameters (sanitized).
    *   INFO: Log successful outcomes.
    *   WARNING/ERROR: Log failures or exceptions, including tracebacks for unexpected errors.
*   **Configuration:** Ensure sensitive data like API keys are not directly logged. Log placeholders or indications that they were used.

## 7. Security Considerations

*   **Credential Storage:** API keys, secrets, and tokens will be stored as Odoo system parameters (`ir.config_parameter`) via the `res.config.settings` model. Access to the Odoo settings views where these are managed must be restricted to appropriate administrative roles (e.g., `base.group_system`).
*   **HTTPS Enforcement:** `BaseApiClient` will inherently use HTTPS if the `base_url` is HTTPS. No fallback to HTTP should be allowed for external API calls. TLS verification will be enabled by default in the `requests` library.
*   **Input Sanitization:** While this module primarily calls external APIs, any data passed to it from other Odoo modules should already be validated/sanitized by those modules. This module should focus on constructing valid requests for external APIs.
*   **Output Handling:** Responses from external APIs should be carefully parsed. Avoid directly rendering raw HTML or script content from external APIs in Odoo views if such responses were ever to occur.
*   **Principle of Least Privilege:** API keys configured should ideally have only the permissions required for the integration's function (e.g., an SMS API key should only be able to send SMS, not manage account settings). This is dependent on the external service's API key capabilities.

## 8. Dependencies

*   **Python Libraries:**
    *   `requests`: For making HTTP calls. This is a standard Odoo dependency.
    *   `pydantic` (Optional but Recommended): For DTOs. If used, it must be added as a Python dependency.
*   **Odoo Modules:**
    *   `base`: Core Odoo framework.
    *   `mail`: For Odoo's internal email sending capabilities (fallback for email service) and general mail features.
    *   `dfr_common`: (Assumed) For any shared utilities, base classes, or configurations provided by the DFR common module. If `dfr_common` defines a base configuration model that `res.config.settings` in this module should inherit from, or common exception base classes, this dependency is critical.

## 9. Testing Considerations

*   **Unit Tests:**
    *   Test DTO validation and serialization/deserialization.
    *   Test `BaseApiClient` methods for constructing requests and handling standard responses/errors (using `unittest.mock` for `requests.Session`).
    *   Test individual methods of specific API clients, mocking the `_request` method of `BaseApiClient` to simulate various API responses (success, different error codes, timeouts).
    *   Test logic within Odoo services, mocking the client instances they use. Test configuration retrieval and error handling logic.
*   **Integration Tests (within Odoo test environment):**
    *   Test Odoo services interacting with mocked API clients that return predefined DTOs or raise specific exceptions.
    *   Test the configuration flow: setting parameters in `res.config.settings` and verifying that services pick up these configurations correctly.
*   **Mocking:** Use Python's `unittest.mock` extensively to mock external API calls. Avoid making real API calls during automated tests.
*   **Manual/Staging Tests:** For critical integrations like SMS or National ID validation, manual tests against sandbox/test environments of the actual external services will be necessary on a staging DFR instance.
*   **Focus Areas:**
    *   Correct instantiation of different clients based on configuration (Strategy pattern in SMS/Email dispatch services).
    *   Error handling pathways in both clients and services.
    *   Parsing of various success and error responses from (mocked) external APIs.
    *   Secure handling of credentials (i.e., ensuring they are fetched from config and not hardcoded).