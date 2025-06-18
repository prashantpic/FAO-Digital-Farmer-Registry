# Specification

# 1. Files

- **Path:** dfr_addons/dfr_integrations/__init__.py  
**Description:** Initializes the Python package for the dfr_integrations Odoo module, importing submodules like models, services, and clients.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 4  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** __init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the dfr_integrations module and its components (models, services, clients) available to Odoo.  
**Logic Description:** Contains import statements for sub-packages and modules within dfr_integrations (e.g., from . import models, from . import services, from . import clients).  
**Documentation:**
    
    - **Summary:** Root __init__.py for the dfr_integrations Odoo module.
    
**Namespace:** odoo.addons.dfr_integrations  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_integrations/__manifest__.py  
**Description:** Odoo manifest file for the DFR External Integration Connectors module. Defines module metadata, dependencies, and data files.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Module Manifest  
**Relative Path:** __manifest__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    
**Purpose:** Provides Odoo with essential information about the dfr_integrations module, such as its name, version, author, dependencies (e.g., base, mail, dfr_common), and data files to load (e.g., views for configuration).  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'license', 'category', 'depends', 'data', 'installable', 'application'. The 'depends' key will list 'base', 'mail', and 'dfr_common'. The 'data' key will list XML files for views (e.g., 'views/res_config_settings_views.xml').  
**Documentation:**
    
    - **Summary:** Manifest file for the dfr_integrations Odoo module, defining its properties and dependencies.
    
**Namespace:** odoo.addons.dfr_integrations  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_integrations/exceptions/__init__.py  
**Description:** Initializes the Python package for integration-specific exceptions.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** exceptions/__init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Exception Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes custom exception classes available for import within the dfr_integrations module and potentially by other modules.  
**Logic Description:** Contains import statements for specific exception classes defined in this sub-package (e.g., from .integration_exceptions import IntegrationAPIError, APITimeoutError).  
**Documentation:**
    
    - **Summary:** __init__.py for the exceptions sub-package.
    
**Namespace:** odoo.addons.dfr_integrations.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** dfr_addons/dfr_integrations/exceptions/integration_exceptions.py  
**Description:** Defines custom exception classes for handling errors related to external API integrations.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** integration_exceptions  
**Type:** Exception Definitions  
**Relative Path:** exceptions/integration_exceptions  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom API Error Handling
    
**Requirement Ids:**
    
    - REQ-API-007
    - REQ-FHR-006
    - REQ-NS-004
    
**Purpose:** To provide specific, catchable error types for different external integration failures, improving error handling and debugging.  
**Logic Description:** Defines Python classes inheriting from `Exception` or Odoo's `UserError`. Examples: `IntegrationAPIError(Exception)` base class, `ExternalServiceAuthenticationError(IntegrationAPIError)`, `APITimeoutError(IntegrationAPIError)`, `InvalidResponseError(IntegrationAPIError)`, `ConfigurationError(IntegrationAPIError)`. Each exception can take a message and optionally other context.  
**Documentation:**
    
    - **Summary:** Custom exceptions for external API integration failures.
    
**Namespace:** odoo.addons.dfr_integrations.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** dfr_addons/dfr_integrations/dtos/__init__.py  
**Description:** Initializes the Python package for Data Transfer Objects (DTOs) used in external API communications.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** dtos/__init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DTO Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes DTO classes available for representing structured data for requests and responses to external APIs.  
**Logic Description:** Contains import statements for DTO classes defined in this sub-package (e.g., from .national_id_api_dtos import NationalIdValidationRequest, NationalIdValidationResponse).  
**Documentation:**
    
    - **Summary:** __init__.py for the dtos sub-package.
    
**Namespace:** odoo.addons.dfr_integrations.dtos  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** dfr_addons/dfr_integrations/dtos/national_id_api_dtos.py  
**Description:** Defines Data Transfer Objects (DTOs) for National ID validation API requests and responses.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** national_id_api_dtos  
**Type:** DTO Definitions  
**Relative Path:** dtos/national_id_api_dtos  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - DataTransferObject
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - National ID API Data Structures
    
**Requirement Ids:**
    
    - REQ-FHR-006
    
**Purpose:** To provide typed structures for data exchanged with the external National ID validation service, ensuring clarity and type safety.  
**Logic Description:** Defines Pydantic models or dataclasses. Examples: `NationalIdValidationRequest(BaseModel)` with fields like `id_number: str`, `id_type: str`, `country_code: str`. `NationalIdValidationResponse(BaseModel)` with fields like `is_valid: bool`, `full_name: Optional[str]`, `date_of_birth: Optional[date]`, `error_message: Optional[str]`. Use `Optional` from `typing` for non-mandatory fields.  
**Documentation:**
    
    - **Summary:** DTOs for National ID validation API interactions.
    
**Namespace:** odoo.addons.dfr_integrations.dtos  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** dfr_addons/dfr_integrations/dtos/sms_api_dtos.py  
**Description:** Defines Data Transfer Objects (DTOs) for SMS gateway API requests and responses.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** sms_api_dtos  
**Type:** DTO Definitions  
**Relative Path:** dtos/sms_api_dtos  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - DataTransferObject
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - SMS Gateway API Data Structures
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To provide typed structures for data exchanged with external SMS gateway services.  
**Logic Description:** Defines Pydantic models or dataclasses. Examples: `SmsSendRequest(BaseModel)` with fields like `recipient_phone: str`, `message_body: str`, `sender_id: Optional[str]`. `SmsSendResponse(BaseModel)` with fields like `message_sid: Optional[str]`, `status: str`, `error_code: Optional[str]`, `error_message: Optional[str]`.  
**Documentation:**
    
    - **Summary:** DTOs for SMS gateway API interactions.
    
**Namespace:** odoo.addons.dfr_integrations.dtos  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** dfr_addons/dfr_integrations/dtos/email_api_dtos.py  
**Description:** Defines Data Transfer Objects (DTOs) for Email gateway API requests and responses (if not using Odoo's mail.mail directly for all external sending).  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** email_api_dtos  
**Type:** DTO Definitions  
**Relative Path:** dtos/email_api_dtos  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - DataTransferObject
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Email Gateway API Data Structures
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To provide typed structures for data exchanged with external Email gateway services, if custom integration is needed beyond Odoo's capabilities.  
**Logic Description:** Defines Pydantic models or dataclasses. Examples: `EmailSendRequest(BaseModel)` with fields like `to_email: str`, `from_email: str`, `subject: str`, `html_body: Optional[str]`, `text_body: Optional[str]`, `attachments: Optional[List[AttachmentDTO]]`. `EmailSendResponse(BaseModel)` with fields like `message_id: Optional[str]`, `status: str`, `error_message: Optional[str]`.  
**Documentation:**
    
    - **Summary:** DTOs for Email gateway API interactions.
    
**Namespace:** odoo.addons.dfr_integrations.dtos  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** dfr_addons/dfr_integrations/clients/__init__.py  
**Description:** Initializes the Python package for external API client implementations.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** clients/__init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Client Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes API client classes available for use by the services layer.  
**Logic Description:** Contains import statements for client classes (e.g., from .base_client import BaseApiClient, from .national_id_api_client import NationalIdApiClient).  
**Documentation:**
    
    - **Summary:** __init__.py for the clients sub-package.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/base_client.py  
**Description:** Abstract base class for external API clients, providing common functionalities like HTTP request handling, error parsing, and logging.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 1  
**Name:** base_client  
**Type:** Base API Client  
**Relative Path:** clients/base_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - TemplateMethod
    - Gateway
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** protected  
    - **Name:** api_key  
**Type:** Optional[str]  
**Attributes:** protected  
    - **Name:** timeout_seconds  
**Type:** int  
**Attributes:** protected  
    - **Name:** session  
**Type:** requests.Session  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url: str
    - api_key: Optional[str] = None
    - timeout_seconds: int = 30
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _get_headers  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** protected|virtual  
    - **Name:** _request  
**Parameters:**
    
    - method: str
    - endpoint: str
    - params: Optional[dict] = None
    - data: Optional[dict] = None
    - json_data: Optional[dict] = None
    - expected_status_codes: Optional[List[int]] = None
    
**Return Type:** requests.Response  
**Attributes:** protected  
    - **Name:** _handle_api_error  
**Parameters:**
    
    - response: requests.Response
    
**Return Type:** void  
**Attributes:** protected|virtual  
    
**Implemented Features:**
    
    - Common HTTP Client Logic
    - Error Handling Foundation
    - Configurable Timeouts
    
**Requirement Ids:**
    
    - REQ-API-007
    - REQ-NS-004
    - REQ-FHR-006
    
**Purpose:** To provide a reusable foundation for specific API client implementations, promoting DRY principles and consistent behavior.  
**Logic Description:** Uses the `requests` library. The `__init__` method initializes `requests.Session()`. `_get_headers` can be overridden by subclasses to add specific auth headers. `_request` method makes HTTP calls (GET, POST, etc.), handles timeouts, and basic response validation (e.g., expected_status_codes). `_handle_api_error` parses common error responses and raises appropriate custom exceptions from `integration_exceptions.py`. Includes logging of requests and responses (at debug level).  
**Documentation:**
    
    - **Summary:** Base class for making HTTP requests to external APIs, handling common concerns.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/national_id_api_client.py  
**Description:** Client for interacting with an external National ID validation API.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 2  
**Name:** national_id_api_client  
**Type:** API Client  
**Relative Path:** clients/national_id_api_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Adapter
    - Gateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url: str
    - api_key: str
    - timeout_seconds: int = 10
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** validate_national_id  
**Parameters:**
    
    - request_dto: NationalIdValidationRequest
    
**Return Type:** NationalIdValidationResponse  
**Attributes:** public  
    
**Implemented Features:**
    
    - National ID Validation API Integration
    
**Requirement Ids:**
    
    - REQ-FHR-006
    - REQ-API-007
    
**Purpose:** To provide a dedicated interface for validating National IDs against an external service.  
**Logic Description:** Inherits from `BaseApiClient`. The `__init__` calls `super().__init__`. `validate_national_id` constructs the request payload using `NationalIdValidationRequest` DTO, calls the appropriate endpoint (e.g., '/validate') using `self._request()`, parses the JSON response into `NationalIdValidationResponse` DTO, and handles specific API errors by raising custom exceptions. The `_get_headers` method might be overridden to include the API key in a specific way if required by the external API.  
**Documentation:**
    
    - **Summary:** Client for communicating with the National ID validation service.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/sms_gateway_client_interface.py  
**Description:** Abstract Base Class (ABC) defining the interface for an SMS gateway client.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 2  
**Name:** sms_gateway_client_interface  
**Type:** Interface  
**Relative Path:** clients/sms_gateway_client_interface  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Interface
    - Strategy
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - config: dict
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** send_sms  
**Parameters:**
    
    - request_dto: SmsSendRequest
    
**Return Type:** SmsSendResponse  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - SMS Gateway Abstraction
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To define a common contract for different SMS gateway implementations, allowing for pluggability.  
**Logic Description:** Uses `abc.ABC` and `abc.abstractmethod`. The `__init__` takes a generic configuration dictionary. `send_sms` is an abstract method to be implemented by concrete gateway clients.  
**Documentation:**
    
    - **Summary:** Defines the common interface for all SMS gateway clients.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/sms_twilio_client.py  
**Description:** Example Twilio SMS gateway client implementation.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 3  
**Name:** sms_twilio_client  
**Type:** API Client  
**Relative Path:** clients/sms_twilio_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Adapter
    - StrategyPatternElement
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - account_sid: str
    - auth_token: str
    - base_url: str = 'https://api.twilio.com/2010-04-01'
    - timeout_seconds: int = 10
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** send_sms  
**Parameters:**
    
    - request_dto: SmsSendRequest
    
**Return Type:** SmsSendResponse  
**Attributes:** public  
    
**Implemented Features:**
    
    - Twilio SMS Sending
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To send SMS messages using the Twilio API.  
**Logic Description:** Inherits from `SmsGatewayClientInterface` and `BaseApiClient` (or directly uses BaseApiClient logic). `__init__` stores Twilio specific credentials and base URL. `send_sms` method constructs the request for Twilio's API (e.g., form-encoded data), uses `self._request()` to send it, handles Twilio-specific response formats and error codes, mapping them to `SmsSendResponse` and custom exceptions. Overrides `_get_headers` if Twilio uses basic auth or specific headers.  
**Documentation:**
    
    - **Summary:** Twilio client for sending SMS messages.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/email_gateway_client_interface.py  
**Description:** Abstract Base Class (ABC) defining the interface for an Email gateway client.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 2  
**Name:** email_gateway_client_interface  
**Type:** Interface  
**Relative Path:** clients/email_gateway_client_interface  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Interface
    - Strategy
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - config: dict
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** send_email  
**Parameters:**
    
    - request_dto: EmailSendRequest
    
**Return Type:** EmailSendResponse  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - Email Gateway Abstraction
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To define a common contract for different Email gateway implementations.  
**Logic Description:** Uses `abc.ABC` and `abc.abstractmethod`. The `__init__` takes a generic configuration dictionary. `send_email` is an abstract method.  
**Documentation:**
    
    - **Summary:** Defines the common interface for all Email gateway clients.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/email_sendgrid_client.py  
**Description:** Example SendGrid Email gateway client implementation.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 3  
**Name:** email_sendgrid_client  
**Type:** API Client  
**Relative Path:** clients/email_sendgrid_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Adapter
    - StrategyPatternElement
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - api_key: str
    - base_url: str = 'https://api.sendgrid.com/v3'
    - timeout_seconds: int = 15
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** send_email  
**Parameters:**
    
    - request_dto: EmailSendRequest
    
**Return Type:** EmailSendResponse  
**Attributes:** public  
    
**Implemented Features:**
    
    - SendGrid Email Sending
    
**Requirement Ids:**
    
    - REQ-NS-004
    
**Purpose:** To send Email messages using the SendGrid API.  
**Logic Description:** Inherits from `EmailGatewayClientInterface` and `BaseApiClient`. `__init__` stores SendGrid API key and base URL. `send_email` method constructs the JSON request for SendGrid's API, uses `self._request()` to send it, handles SendGrid-specific response formats and error codes, mapping them to `EmailSendResponse` and custom exceptions. Overrides `_get_headers` to include `Authorization: Bearer <api_key>`.  
**Documentation:**
    
    - **Summary:** SendGrid client for sending Email messages.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/weather_service_client.py  
**Description:** Placeholder client for interacting with an external weather service API. (REQ-API-007)  
**Template:** Python Odoo Module File  
**Dependancy Level:** 2  
**Name:** weather_service_client  
**Type:** API Client  
**Relative Path:** clients/weather_service_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Adapter
    - Gateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url: str
    - api_key: str
    - timeout_seconds: int = 10
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_forecast  
**Parameters:**
    
    - latitude: float
    - longitude: float
    - date: Optional[str] = None
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Weather Service API Integration (Placeholder)
    
**Requirement Ids:**
    
    - REQ-API-007
    
**Purpose:** To provide a dedicated interface for fetching weather data from an external service.  
**Logic Description:** Inherits from `BaseApiClient`. Implements methods to fetch weather forecasts or historical data based on location and date. Uses DTOs from `weather_dtos.py` (to be defined if DTOs are complex).  
**Documentation:**
    
    - **Summary:** Client for communicating with an external weather service.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/clients/payment_platform_client.py  
**Description:** Placeholder client for interacting with an external payment platform API. (REQ-API-007)  
**Template:** Python Odoo Module File  
**Dependancy Level:** 2  
**Name:** payment_platform_client  
**Type:** API Client  
**Relative Path:** clients/payment_platform_client  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - Adapter
    - Gateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url: str
    - api_key: str
    - secret_key: str
    - timeout_seconds: int = 20
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** initiate_payment  
**Parameters:**
    
    - payment_details: dict
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** check_payment_status  
**Parameters:**
    
    - transaction_id: str
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Payment Platform API Integration (Placeholder)
    
**Requirement Ids:**
    
    - REQ-API-007
    
**Purpose:** To provide a dedicated interface for initiating and checking payments via an external platform.  
**Logic Description:** Inherits from `BaseApiClient`. Implements methods for payment initiation, status checking, etc. Uses DTOs from `payment_dtos.py` (to be defined if DTOs are complex).  
**Documentation:**
    
    - **Summary:** Client for communicating with an external payment platform.
    
**Namespace:** odoo.addons.dfr_integrations.clients  
**Metadata:**
    
    - **Category:** Integration
    
- **Path:** dfr_addons/dfr_integrations/services/__init__.py  
**Description:** Initializes the Python package for Odoo services that utilize the API clients.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** services/__init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Odoo service classes available, providing the internal API for other DFR modules.  
**Logic Description:** Contains import statements for service classes (e.g., from .national_id_validation_service import NationalIdValidationService).  
**Documentation:**
    
    - **Summary:** __init__.py for the services sub-package.
    
**Namespace:** odoo.addons.dfr_integrations.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_integrations/services/national_id_validation_service.py  
**Description:** Odoo service to manage National ID validation by calling the appropriate API client.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 3  
**Name:** national_id_validation_service  
**Type:** Odoo Service  
**Relative Path:** services/national_id_validation_service  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - ServiceLayer
    - Facade
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static|final  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static|final  
    
**Methods:**
    
    - **Name:** validate_id  
**Parameters:**
    
    - self
    - id_number: str
    - id_type: str
    - country_code: str
    
**Return Type:** NationalIdValidationResponse  
**Attributes:** public  
    
**Implemented Features:**
    
    - National ID Validation Service Logic
    
**Requirement Ids:**
    
    - REQ-FHR-006
    - REQ-API-007
    - REQ-API-011
    
**Purpose:** Provides a structured way for other Odoo modules to request National ID validation, abstracting the direct client interaction.  
**Logic Description:** Inherits from `odoo.models.AbstractModel`. `_name = 'dfr.national.id.validation.service'`. The `validate_id` method retrieves API configuration (URL, key) from Odoo system parameters (`ir.config_parameter`). It instantiates `NationalIdApiClient`, creates the `NationalIdValidationRequest` DTO, calls the client's `validate_national_id` method, and returns the `NationalIdValidationResponse`. Handles exceptions from the client and logs them.  
**Documentation:**
    
    - **Summary:** Service for handling National ID validation requests within Odoo.
    
**Namespace:** odoo.addons.dfr_integrations.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_integrations/services/sms_dispatch_service.py  
**Description:** Odoo service to manage sending SMS messages via configured gateway(s).  
**Template:** Python Odoo Module File  
**Dependancy Level:** 4  
**Name:** sms_dispatch_service  
**Type:** Odoo Service  
**Relative Path:** services/sms_dispatch_service  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - ServiceLayer
    - Facade
    - Strategy
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static|final  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static|final  
    
**Methods:**
    
    - **Name:** _get_configured_sms_client  
**Parameters:**
    
    - self
    
**Return Type:** SmsGatewayClientInterface  
**Attributes:** private  
    - **Name:** send_sms_message  
**Parameters:**
    
    - self
    - recipient_phone: str
    - message_body: str
    - sender_id: Optional[str] = None
    
**Return Type:** SmsSendResponse  
**Attributes:** public  
    
**Implemented Features:**
    
    - SMS Dispatch Service Logic
    
**Requirement Ids:**
    
    - REQ-NS-004
    - REQ-API-011
    
**Purpose:** Provides a centralized service for sending SMS messages, allowing dynamic selection of SMS gateway providers based on configuration.  
**Logic Description:** Inherits from `odoo.models.AbstractModel`. `_name = 'dfr.sms.dispatch.service'`. `_get_configured_sms_client` reads system parameters to determine the active SMS gateway (e.g., 'twilio', 'vonage') and its credentials, then instantiates and returns the corresponding client (e.g., `SmsTwilioClient`). `send_sms_message` uses `_get_configured_sms_client` to get a client instance, creates `SmsSendRequest`, calls the client's `send_sms` method, and returns the response. Handles exceptions.  
**Documentation:**
    
    - **Summary:** Service for dispatching SMS messages via configured gateways.
    
**Namespace:** odoo.addons.dfr_integrations.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_integrations/services/email_dispatch_service.py  
**Description:** Odoo service to manage sending Email messages via configured gateway(s) or Odoo's internal mail system.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 4  
**Name:** email_dispatch_service  
**Type:** Odoo Service  
**Relative Path:** services/email_dispatch_service  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    - ServiceLayer
    - Facade
    - Strategy
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static|final  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static|final  
    
**Methods:**
    
    - **Name:** _get_configured_email_client  
**Parameters:**
    
    - self
    
**Return Type:** Optional[EmailGatewayClientInterface]  
**Attributes:** private  
    - **Name:** send_email_message  
**Parameters:**
    
    - self
    - to_email: str
    - subject: str
    - body_html: Optional[str] = None
    - body_text: Optional[str] = None
    - from_email: Optional[str] = None
    - attachments: Optional[list] = None
    
**Return Type:** Union[EmailSendResponse, bool]  
**Attributes:** public  
    
**Implemented Features:**
    
    - Email Dispatch Service Logic
    
**Requirement Ids:**
    
    - REQ-NS-004
    - REQ-API-011
    
**Purpose:** Provides a centralized service for sending Email messages, allowing dynamic selection of Email gateway providers or using Odoo's default mail server.  
**Logic Description:** Inherits from `odoo.models.AbstractModel`. `_name = 'dfr.email.dispatch.service'`. `_get_configured_email_client` reads system parameters for active external email gateway and credentials, instantiates client. `send_email_message` first tries `_get_configured_email_client`. If an external client is configured and returned, it uses it. Otherwise, it falls back to using Odoo's `mail.mail` model to send the email. Handles exceptions and logs outcomes. `from_email` might be configured globally or per message.  
**Documentation:**
    
    - **Summary:** Service for dispatching Email messages via configured external gateways or Odoo's internal mail system.
    
**Namespace:** odoo.addons.dfr_integrations.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_integrations/models/__init__.py  
**Description:** Initializes the Python package for Odoo models within the dfr_integrations module.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Package Initializer  
**Relative Path:** models/__init__  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Odoo model classes (e.g., for configuration) available to the Odoo framework.  
**Logic Description:** Contains import statements for model classes defined in this sub-package (e.g., from . import res_config_settings).  
**Documentation:**
    
    - **Summary:** __init__.py for the models sub-package.
    
**Namespace:** odoo.addons.dfr_integrations.models  
**Metadata:**
    
    - **Category:** DataModeling
    
- **Path:** dfr_addons/dfr_integrations/models/res_config_settings.py  
**Description:** Extends Odoo's base configuration settings (res.config.settings) to include parameters for external integrations.  
**Template:** Python Odoo Module File  
**Dependancy Level:** 1  
**Name:** res_config_settings  
**Type:** Odoo Model Extension  
**Relative Path:** models/res_config_settings  
**Repository Id:** DFR_MOD_EXT_INTEGRATION_CONNECTORS  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** dfr_national_id_api_url  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.national_id_api_url'  
    - **Name:** dfr_national_id_api_key  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.national_id_api_key'  
    - **Name:** dfr_sms_gateway_provider  
**Type:** fields.Selection  
**Attributes:** config_parameter='dfr_integrations.sms_gateway_provider', selection=[('twilio', 'Twilio'), ('vonage', 'Vonage'), ('other', 'Other')]  
    - **Name:** dfr_sms_gateway_api_key  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.sms_gateway_api_key'  
    - **Name:** dfr_sms_gateway_secret  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.sms_gateway_secret'  
    - **Name:** dfr_sms_gateway_url  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.sms_gateway_url'  
    - **Name:** dfr_email_gateway_provider  
**Type:** fields.Selection  
**Attributes:** config_parameter='dfr_integrations.email_gateway_provider', selection=[('sendgrid', 'SendGrid'), ('odoo', 'Odoo Default'), ('other', 'Other')]  
    - **Name:** dfr_email_gateway_api_key  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.email_gateway_api_key'  
    - **Name:** dfr_default_email_from  
**Type:** fields.Char  
**Attributes:** config_parameter='dfr_integrations.default_email_from'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - External API Configuration Storage
    
**Requirement Ids:**
    
    - REQ-API-011
    - REQ-NS-004
    
**Purpose:** To allow administrators to securely configure credentials and endpoints for various external services through Odoo's standard settings interface.  
**Logic Description:** Inherits from `odoo.models.TransientModel` and `_inherit = 'res.config.settings'`. Defines `fields.Char` and `fields.Selection` for API URLs, keys, secrets, and provider choices. These fields use the `config_parameter` attribute to store values in `ir.config_parameter` table. Corresponding views (XML, out of scope for this JSON) would expose these in Odoo settings.  
**Documentation:**
    
    - **Summary:** Model for storing configuration parameters related to external integrations in Odoo settings.
    
**Namespace:** odoo.addons.dfr_integrations.models  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_national_id_validation_mock
  - enable_sms_gateway_mock
  - enable_email_gateway_mock
  
- **Database Configs:**
  
  


---

