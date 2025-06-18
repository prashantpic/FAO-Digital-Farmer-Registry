# Specification

# 1. Files

- **Path:** dfr_testing/automation_suite/requirements.txt  
**Description:** Lists all Python dependencies required for the DFR Test Automation Suite, including pytest, selenium, appium-python-client, requests, and other utility libraries.  
**Template:** Python Requirements File  
**Dependancy Level:** 0  
**Name:** requirements  
**Type:** DependencyManagement  
**Relative Path:** requirements.txt  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management for Test Suite
    
**Requirement Ids:**
    
    
**Purpose:** To define and manage Python package dependencies for the test automation suite, ensuring reproducible environments.  
**Logic Description:** This file will contain entries like 'pytest==x.y.z', 'selenium==a.b.c', 'Appium-Python-Client==u.v.w', 'requests==p.q.r'. Versions should be pinned for stability. Tools like pip can use this file to install dependencies.  
**Documentation:**
    
    - **Summary:** Specifies Python libraries and their versions needed to run the test automation scripts. Used by pip for installation.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/pytest.ini  
**Description:** PyTest configuration file. Defines markers, default options, logging settings, and plugin configurations for running PyTest-based tests (API, Web E2E, Odoo Integration).  
**Template:** INI Configuration  
**Dependancy Level:** 0  
**Name:** pytest  
**Type:** Configuration  
**Relative Path:** pytest.ini  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PyTest Test Framework Configuration
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To configure the PyTest execution environment, including test discovery, reporting, and fixtures.  
**Logic Description:** Contains sections for pytest configuration, such as markers (e.g., 'api', 'web', 'mobile', 'integration', 'smoke', 'regression', 'security', 'performance'), log format, and test paths. Specifies options for HTML reports or other plugins.  
**Documentation:**
    
    - **Summary:** Configuration file for the PyTest framework, controlling how tests are discovered, run, and reported.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/config/global_config.py  
**Description:** Contains global configurations and constants for the test suite, such as environment URLs, default timeouts, and paths to test data.  
**Template:** Python Utility  
**Dependancy Level:** 0  
**Name:** global_config  
**Type:** Configuration  
**Relative Path:** config/global_config.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** BASE_URL_DEV  
**Type:** str  
**Attributes:** public|static  
    - **Name:** BASE_URL_STAGING  
**Type:** str  
**Attributes:** public|static  
    - **Name:** DEFAULT_TIMEOUT  
**Type:** int  
**Attributes:** public|static  
    - **Name:** TEST_DATA_PATH  
**Type:** str  
**Attributes:** public|static  
    
**Methods:**
    
    - **Name:** get_environment_url  
**Parameters:**
    
    - env_name: str
    
**Return Type:** str  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Centralized Test Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a single source for global test parameters, facilitating easy updates and environment switching.  
**Logic Description:** This module will define constants for URLs (development, staging), default timeouts for web/API calls, and base paths for test data. A function might allow selecting the target environment URL based on an input or environment variable.  
**Documentation:**
    
    - **Summary:** Defines global constants and configuration settings accessible throughout the test automation suite.
    
**Namespace:** dfr.testing.automation.config  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/config/dev_env_config.ini  
**Description:** Environment-specific configurations for the 'development' environment, such as API base URLs, user credentials (placeholders or references to secure storage), and database connection details for integration tests.  
**Template:** INI Configuration  
**Dependancy Level:** 0  
**Name:** dev_env_config  
**Type:** Configuration  
**Relative Path:** config/dev_env_config.ini  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Development Environment Configuration
    
**Requirement Ids:**
    
    
**Purpose:** To store environment-specific settings for development, separating them from global configurations and test logic.  
**Logic Description:** Contains key-value pairs for API endpoints, web application URLs, specific test user credentials (ideally referencing secrets management tools, not hardcoded), and any specific flags for the dev environment.  
**Documentation:**
    
    - **Summary:** INI file holding configuration parameters specific to the development test environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/config/staging_env_config.ini  
**Description:** Environment-specific configurations for the 'staging' environment, similar to dev_env_config.ini but with values appropriate for the staging/UAT setup.  
**Template:** INI Configuration  
**Dependancy Level:** 0  
**Name:** staging_env_config  
**Type:** Configuration  
**Relative Path:** config/staging_env_config.ini  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging Environment Configuration
    
**Requirement Ids:**
    
    
**Purpose:** To store environment-specific settings for staging, allowing tests to run against the staging environment without code changes.  
**Logic Description:** Contains key-value pairs similar to dev_env_config.ini, but tailored for the staging environment URLs, credentials, and settings.  
**Documentation:**
    
    - **Summary:** INI file holding configuration parameters specific to the staging test environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/utils/logger_setup.py  
**Description:** Configures a standardized logger for use across all test scripts, enabling consistent log formats, levels, and output destinations (console, file).  
**Template:** Python Utility  
**Dependancy Level:** 0  
**Name:** logger_setup  
**Type:** Utility  
**Relative Path:** utils/logger_setup.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** setup_logger  
**Parameters:**
    
    - name: str
    - log_level: str = 'INFO'
    
**Return Type:** logging.Logger  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Standardized Test Logging
    
**Requirement Ids:**
    
    
**Purpose:** To provide a consistent and configurable logging mechanism for test automation scripts.  
**Logic Description:** This module will use Python's `logging` module. The `setup_logger` function will configure a logger instance with a specified name, log level, formatter, and handlers (e.g., StreamHandler for console, FileHandler for log files).  
**Documentation:**
    
    - **Summary:** Utility for setting up and configuring Python loggers for test automation.
    
**Namespace:** dfr.testing.automation.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** dfr_testing/automation_suite/utils/reporting_utils.py  
**Description:** Provides utility functions for custom test reporting, such as formatting test results, capturing screenshots on failure (for UI tests), or integrating with test management tools.  
**Template:** Python Utility  
**Dependancy Level:** 1  
**Name:** reporting_utils  
**Type:** Utility  
**Relative Path:** utils/reporting_utils.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** capture_screenshot  
**Parameters:**
    
    - driver
    - file_name: str
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** log_test_result  
**Parameters:**
    
    - test_name: str
    - status: str
    - message: str = None
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Custom Test Reporting Enhancements
    - Screenshot on Failure
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To augment standard test reporting capabilities with custom features like screenshots or specific log formatting.  
**Logic Description:** The `capture_screenshot` function (for Selenium/Appium) will take a WebDriver/AppiumDriver instance and save a screenshot. `log_test_result` could format and write test outcomes to a custom log or integrate with an external reporting system.  
**Documentation:**
    
    - **Summary:** Utilities to assist with test reporting, including error capturing and custom logging.
    
**Namespace:** dfr.testing.automation.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** dfr_testing/automation_suite/api_tests/common/api_client.py  
**Description:** A reusable API client class or set of functions to make HTTP requests to the DFR backend API. Handles base URL, headers, and common request patterns.  
**Template:** Python Utility  
**Dependancy Level:** 1  
**Name:** api_client  
**Type:** Utility  
**Relative Path:** api_tests/common/api_client.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** session  
**Type:** requests.Session  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get  
**Parameters:**
    
    - endpoint: str
    - params: dict = None
    - headers: dict = None
    
**Return Type:** requests.Response  
**Attributes:** public  
    - **Name:** post  
**Parameters:**
    
    - endpoint: str
    - data: dict = None
    - json: dict = None
    - headers: dict = None
    
**Return Type:** requests.Response  
**Attributes:** public  
    - **Name:** put  
**Parameters:**
    
    - endpoint: str
    - data: dict = None
    - json: dict = None
    - headers: dict = None
    
**Return Type:** requests.Response  
**Attributes:** public  
    - **Name:** delete  
**Parameters:**
    
    - endpoint: str
    - headers: dict = None
    
**Return Type:** requests.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - Centralized API Request Handling
    
**Requirement Ids:**
    
    
**Purpose:** To provide a consistent interface for making API calls, abstracting away common request logic.  
**Logic Description:** This class will use the `requests` library. The constructor will take the base API URL. Methods for GET, POST, PUT, DELETE will handle constructing the full URL, adding default headers (like Content-Type), and managing session state if needed.  
**Documentation:**
    
    - **Summary:** A client for interacting with the DFR RESTful API, providing methods for various HTTP requests.
    
**Namespace:** dfr.testing.automation.api_tests.common  
**Metadata:**
    
    - **Category:** APIInteraction
    
- **Path:** dfr_testing/automation_suite/api_tests/common/auth_handler.py  
**Description:** Manages API authentication (OAuth2/JWT). Handles token acquisition, storage, and inclusion in API requests.  
**Template:** Python Utility  
**Dependancy Level:** 1  
**Name:** auth_handler  
**Type:** Utility  
**Relative Path:** api_tests/common/auth_handler.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** token  
**Type:** str  
**Attributes:** private|static  
    - **Name:** token_expiry  
**Type:** datetime  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** get_auth_header  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public|static  
    - **Name:** authenticate  
**Parameters:**
    
    - username: str
    - password: str
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** _refresh_token_if_needed  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** private|static  
    
**Implemented Features:**
    
    - API Authentication Management
    
**Requirement Ids:**
    
    - A.4
    
**Purpose:** To abstract authentication logic for API tests, providing valid auth tokens for requests.  
**Logic Description:** This module will handle obtaining OAuth2/JWT tokens from the DFR authentication endpoint. The `get_auth_header` method will return the appropriate 'Authorization' header. It might cache tokens and refresh them when expired.  
**Documentation:**
    
    - **Summary:** Handles authentication for API tests, including token retrieval and management.
    
**Namespace:** dfr.testing.automation.api_tests.common  
**Metadata:**
    
    - **Category:** APIInteraction
    
- **Path:** dfr_testing/automation_suite/api_tests/common/test_data_loader.py  
**Description:** Loads test data from JSON or other file formats for API tests, providing easy access to different data scenarios.  
**Template:** Python Utility  
**Dependancy Level:** 1  
**Name:** test_data_loader  
**Type:** Utility  
**Relative Path:** api_tests/common/test_data_loader.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - DataDrivenTesting
    
**Members:**
    
    
**Methods:**
    
    - **Name:** load_json_data  
**Parameters:**
    
    - file_path: str
    
**Return Type:** dict  
**Attributes:** public|static  
    - **Name:** get_farmer_data  
**Parameters:**
    
    - scenario_name: str
    
**Return Type:** dict  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - API Test Data Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a structured way to load and access test data for API test cases.  
**Logic Description:** Functions in this module will read data from files (e.g., JSON) located in the `test_data/api/` directory. It can provide specific datasets based on a scenario name or file name.  
**Documentation:**
    
    - **Summary:** Utility for loading and providing test data for API automated tests.
    
**Namespace:** dfr.testing.automation.api_tests.common  
**Metadata:**
    
    - **Category:** TestData
    
- **Path:** dfr_testing/automation_suite/api_tests/common/response_validator.py  
**Description:** Contains functions to validate API responses against expected schemas, status codes, and content.  
**Template:** Python Utility  
**Dependancy Level:** 1  
**Name:** response_validator  
**Type:** Utility  
**Relative Path:** api_tests/common/response_validator.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** assert_status_code  
**Parameters:**
    
    - response: requests.Response
    - expected_code: int
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** validate_json_schema  
**Parameters:**
    
    - response_json: dict
    - schema: dict
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** assert_response_contains_key  
**Parameters:**
    
    - response_json: dict
    - key: str
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - API Response Validation
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To provide reusable functions for common API response assertions, improving test readability and maintainability.  
**Logic Description:** This module will include functions for common assertions like checking HTTP status codes, validating JSON response bodies against predefined schemas (e.g., using `jsonschema` library), and checking for the presence of specific keys or values in responses.  
**Documentation:**
    
    - **Summary:** Utility functions for validating API responses, including status codes and payload content.
    
**Namespace:** dfr.testing.automation.api_tests.common  
**Metadata:**
    
    - **Category:** Validation
    
- **Path:** dfr_testing/automation_suite/api_tests/conftest.py  
**Description:** PyTest fixtures specific to API tests. This could include fixtures for initializing the API client, loading common test data, or setting up authentication.  
**Template:** Python PyTest Fixture  
**Dependancy Level:** 2  
**Name:** conftest_api  
**Type:** TestFixture  
**Relative Path:** api_tests/conftest.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** api_client_fixture  
**Parameters:**
    
    - request
    
**Return Type:** ApiClient  
**Attributes:** public  
    - **Name:** authenticated_api_client  
**Parameters:**
    
    - api_client_fixture
    
**Return Type:** ApiClient  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Test Fixture Management
    
**Requirement Ids:**
    
    
**Purpose:** To define reusable setup and teardown logic for API tests using PyTest fixtures.  
**Logic Description:** Defines PyTest fixtures. For example, a fixture `api_client_fixture` that initializes and returns an instance of `ApiClient`. Another fixture `authenticated_api_client` could use the `api_client_fixture` and perform authentication before returning the client.  
**Documentation:**
    
    - **Summary:** PyTest conftest file for API tests, providing shared fixtures and hooks.
    
**Namespace:** dfr.testing.automation.api_tests  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/api_tests/farmer_registry_api/test_farmer_lookup.py  
**Description:** PyTest test cases for the Farmer Lookup API endpoint. Includes tests for valid lookups, invalid inputs, and different search criteria.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 3  
**Name:** test_farmer_lookup  
**Type:** TestScript  
**Relative Path:** api_tests/farmer_registry_api/test_farmer_lookup.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - DataDrivenTesting
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_lookup_farmer_by_uid_valid  
**Parameters:**
    
    - authenticated_api_client
    - test_data_loader
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_lookup_farmer_by_national_id_valid  
**Parameters:**
    
    - authenticated_api_client
    - test_data_loader
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_lookup_farmer_not_found  
**Parameters:**
    
    - authenticated_api_client
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_lookup_farmer_unauthorized  
**Parameters:**
    
    - api_client_fixture
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Farmer Lookup Testing
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - B.5
    
**Purpose:** To verify the functionality, reliability, and performance of the Farmer Lookup API endpoint.  
**Logic Description:** Uses the `authenticated_api_client` fixture. Test methods will call the lookup endpoint with various parameters (valid UID, invalid UID, national ID). Uses `response_validator` to assert status codes and response content. May include performance assertions for B.5.  
**Documentation:**
    
    - **Summary:** Test suite for validating the Farmer Lookup API endpoints provided by DFR_MOD_API_GATEWAY.
    
**Namespace:** dfr.testing.automation.api_tests.farmer_registry_api  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/api_tests/security/test_auth_vulnerabilities.py  
**Description:** PyTest test cases focusing on security vulnerabilities of API authentication and authorization mechanisms, aligning with A.4.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 3  
**Name:** test_auth_vulnerabilities  
**Type:** TestScript  
**Relative Path:** api_tests/security/test_auth_vulnerabilities.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_access_with_expired_token  
**Parameters:**
    
    - api_client_fixture
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_access_with_invalid_token_signature  
**Parameters:**
    
    - api_client_fixture
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_privilege_escalation_attempt  
**Parameters:**
    
    - authenticated_api_client_low_privilege
    - authenticated_api_client_high_privilege
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Authentication Security Testing
    
**Requirement Ids:**
    
    - A.4
    - REQ-PCA-013
    
**Purpose:** To validate the robustness of API authentication and authorization against common security threats.  
**Logic Description:** These tests will attempt to exploit potential vulnerabilities in the auth system: using expired/malformed tokens, trying to access resources without proper permissions, etc. Uses `api_client_fixture` and potentially specialized fixtures for different privilege levels.  
**Documentation:**
    
    - **Summary:** Security tests for API authentication and authorization mechanisms.
    
**Namespace:** dfr.testing.automation.api_tests.security  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/api_tests/performance/test_api_load_farmer_lookup.py  
**Description:** PyTest based performance test for the Farmer Lookup API. Measures response times under simulated load, aligning with B.5.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 3  
**Name:** test_api_load_farmer_lookup  
**Type:** TestScript  
**Relative Path:** api_tests/performance/test_api_load_farmer_lookup.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** TARGET_RESPONSE_TIME_MS  
**Type:** int  
**Attributes:** private|static  
**Value:** 500  
    
**Methods:**
    
    - **Name:** test_farmer_lookup_response_time_under_load  
**Parameters:**
    
    - authenticated_api_client
    - test_data_loader
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - API Performance Testing (Farmer Lookup)
    
**Requirement Ids:**
    
    - B.5
    - REQ-PCA-013
    
**Purpose:** To measure and validate the response time of the Farmer Lookup API under specific load conditions.  
**Logic Description:** This test will make a number of concurrent or sequential calls to the Farmer Lookup API using valid test data. It will measure the response time for each call (or average/percentiles) and assert that it's within the target defined in B.5 (e.g., < 500ms for 95% of calls). Libraries like `pytest-benchmark` or custom timing logic can be used.  
**Documentation:**
    
    - **Summary:** Performance tests for the Farmer Lookup API endpoint, measuring response times.
    
**Namespace:** dfr.testing.automation.api_tests.performance  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/common/web_driver_setup.py  
**Description:** Sets up and tears down Selenium WebDriver instances for different browsers (Chrome, Firefox). Handles driver configurations and capabilities.  
**Template:** Python Selenium Utility  
**Dependancy Level:** 1  
**Name:** web_driver_setup  
**Type:** Utility  
**Relative Path:** e2e_tests_web/common/web_driver_setup.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_webdriver  
**Parameters:**
    
    - browser_name: str = 'chrome'
    
**Return Type:** selenium.webdriver.Remote  
**Attributes:** public|static  
    - **Name:** quit_webdriver  
**Parameters:**
    
    - driver
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - WebDriver Lifecycle Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a consistent way to initialize and close WebDriver instances for web E2E tests.  
**Logic Description:** Uses `selenium.webdriver` to create driver instances. It can read browser choice from config or parameter. Handles setting up driver options (e.g., headless mode, window size) and paths to WebDriver executables.  
**Documentation:**
    
    - **Summary:** Utility for managing Selenium WebDriver instances for web UI testing.
    
**Namespace:** dfr.testing.automation.e2e_tests_web.common  
**Metadata:**
    
    - **Category:** WebDriverManagement
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/common/page_objects/base_page.py  
**Description:** Base class for all Page Objects. Contains common web element interactions and utility methods.  
**Template:** Python Selenium Page Object  
**Dependancy Level:** 2  
**Name:** base_page  
**Type:** PageObject  
**Relative Path:** e2e_tests_web/common/page_objects/base_page.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    - **Name:** driver  
**Type:** selenium.webdriver.Remote  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - driver
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** find_element  
**Parameters:**
    
    - locator: tuple
    
**Return Type:** WebElement  
**Attributes:** protected  
    - **Name:** click  
**Parameters:**
    
    - locator: tuple
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** type_text  
**Parameters:**
    
    - locator: tuple
    - text: str
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** get_page_title  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** wait_for_element_visible  
**Parameters:**
    
    - locator: tuple
    - timeout: int = 10
    
**Return Type:** WebElement  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Base Page Object Functionality
    
**Requirement Ids:**
    
    
**Purpose:** To provide common functionalities and a base structure for all page objects, reducing code duplication.  
**Logic Description:** The constructor takes a WebDriver instance. It includes helper methods for common Selenium actions like finding elements, clicking, sending keys, waiting for elements, etc., often using `WebDriverWait` for robustness.  
**Documentation:**
    
    - **Summary:** A base class for page objects, encapsulating common web interactions and WebDriver utilities.
    
**Namespace:** dfr.testing.automation.e2e_tests_web.common.page_objects  
**Metadata:**
    
    - **Category:** UITestingFramework
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/common/page_objects/admin_portal/farmer_management_page.py  
**Description:** Page Object for the Farmer Management section in the DFR Admin Portal. Encapsulates locators and actions for this page.  
**Template:** Python Selenium Page Object  
**Dependancy Level:** 3  
**Name:** farmer_management_page  
**Type:** PageObject  
**Relative Path:** e2e_tests_web/common/page_objects/admin_portal/farmer_management_page.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    - **Name:** ADD_FARMER_BUTTON  
**Type:** tuple  
**Attributes:** private|static  
**Value:** (By.ID, 'add_farmer_btn')  
    - **Name:** FARMER_NAME_INPUT  
**Type:** tuple  
**Attributes:** private|static  
**Value:** (By.ID, 'farmer_name_field')  
    
**Methods:**
    
    - **Name:** click_add_farmer_button  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** enter_farmer_name  
**Parameters:**
    
    - name: str
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** is_farmer_listed  
**Parameters:**
    
    - farmer_name: str
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Admin Portal Farmer Management Page Interactions
    
**Requirement Ids:**
    
    
**Purpose:** To model the Farmer Management page in the Admin Portal, providing a clear API for test scripts to interact with it.  
**Logic Description:** Inherits from `BasePage`. Defines locators for elements on the Farmer Management page (e.g., add farmer button, search field, farmer list). Provides methods to perform actions like clicking 'Add Farmer', entering search criteria, verifying a farmer is listed.  
**Documentation:**
    
    - **Summary:** Page Object representing the Farmer Management page in the Admin Portal.
    
**Namespace:** dfr.testing.automation.e2e_tests_web.common.page_objects.admin_portal  
**Metadata:**
    
    - **Category:** UITestingFramework
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/admin_portal_tests/test_farmer_creation_admin.py  
**Description:** PyTest E2E test case for creating a new farmer through the DFR Admin Portal.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 4  
**Name:** test_farmer_creation_admin  
**Type:** TestScript  
**Relative Path:** e2e_tests_web/admin_portal_tests/test_farmer_creation_admin.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_create_new_farmer_successfully  
**Parameters:**
    
    - selenium_driver
    - test_data_loader_web
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Web E2E Test: Admin Farmer Creation
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To verify the end-to-end flow of creating a farmer record via the Admin Portal UI.  
**Logic Description:** Uses a `selenium_driver` fixture (defined in conftest.py for web tests). Instantiates relevant Page Objects (LoginPage, AdminDashboardPage, FarmerManagementPage). Navigates through the portal, fills in farmer details using data from `test_data_loader_web`, submits the form, and verifies successful creation.  
**Documentation:**
    
    - **Summary:** End-to-end test for the farmer creation functionality in the Admin Portal (targets DFR_MOD_FARMER_PORTAL if admin portal is part of it, or a general Odoo backend UI).
    
**Namespace:** dfr.testing.automation.e2e_tests_web.admin_portal_tests  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/security_web/test_xss_vulnerabilities.py  
**Description:** PyTest E2E test case to check for common Cross-Site Scripting (XSS) vulnerabilities in web portal input fields.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 4  
**Name:** test_xss_vulnerabilities  
**Type:** TestScript  
**Relative Path:** e2e_tests_web/security_web/test_xss_vulnerabilities.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_farmer_name_field_xss  
**Parameters:**
    
    - selenium_driver
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Web E2E Security Test: XSS
    
**Requirement Ids:**
    
    - A.4
    - REQ-PCA-013
    
**Purpose:** To validate web portals against common XSS attack vectors by inputting malicious scripts.  
**Logic Description:** Uses Page Objects to navigate to forms with input fields. Enters various XSS payloads (e.g., `<script>alert('XSS')</script>`) into fields and submits. Verifies that the script is not executed (e.g., no alert pops up, or the script is properly sanitized/escaped on display).  
**Documentation:**
    
    - **Summary:** Security test case to identify potential XSS vulnerabilities in web portal input fields.
    
**Namespace:** dfr.testing.automation.e2e_tests_web.security_web  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_web/performance_web/test_page_load_times.py  
**Description:** PyTest E2E test to measure page load times for critical pages in the web portals, aligning with B.5.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 4  
**Name:** test_page_load_times  
**Type:** TestScript  
**Relative Path:** e2e_tests_web/performance_web/test_page_load_times.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    - **Name:** MAX_PAGE_LOAD_TIME_S  
**Type:** int  
**Attributes:** private|static  
**Value:** 3  
    
**Methods:**
    
    - **Name:** test_admin_dashboard_load_time  
**Parameters:**
    
    - selenium_driver
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_farmer_portal_registration_form_load_time  
**Parameters:**
    
    - selenium_driver
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Web E2E Performance Test: Page Load Times
    
**Requirement Ids:**
    
    - B.5
    - REQ-PCA-013
    
**Purpose:** To validate that critical web pages load within acceptable performance thresholds.  
**Logic Description:** Uses Selenium to navigate to specific pages. Measures the time taken for the page to load completely (e.g., using JavaScript `performance.timing` or waiting for a specific element). Asserts that the load time is below the defined threshold (e.g., 3 seconds as per REQ-FSSP-011 which is related to B.5).  
**Documentation:**
    
    - **Summary:** Performance test case for measuring page load times of key web portal pages.
    
**Namespace:** dfr.testing.automation.e2e_tests_web.performance_web  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/common/app_driver_setup.py  
**Description:** Sets up and tears down Appium (or Flutter Driver) instances for mobile application testing. Handles capabilities for different devices/OS versions.  
**Template:** Python Appium Utility  
**Dependancy Level:** 1  
**Name:** app_driver_setup  
**Type:** Utility  
**Relative Path:** e2e_tests_mobile/common/app_driver_setup.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_appium_driver  
**Parameters:**
    
    - platform_name: str
    - device_name: str
    - app_path: str
    - extra_caps: dict = None
    
**Return Type:** appium.webdriver.Remote  
**Attributes:** public|static  
    - **Name:** quit_appium_driver  
**Parameters:**
    
    - driver
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Mobile Driver Lifecycle Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a consistent way to initialize and close Appium/Flutter Driver instances for mobile E2E tests.  
**Logic Description:** Initializes Appium driver with desired capabilities (platform, device, app path). For Flutter Driver, this might involve different setup if tests are run from Python. Provides a method to cleanly quit the driver session.  
**Documentation:**
    
    - **Summary:** Utility for managing Appium (or Flutter Driver) instances for mobile UI testing.
    
**Namespace:** dfr.testing.automation.e2e_tests_mobile.common  
**Metadata:**
    
    - **Category:** MobileDriverManagement
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/common/screen_objects/base_screen.py  
**Description:** Base class for all Mobile Screen Objects. Contains common mobile element interactions.  
**Template:** Python Appium Screen Object  
**Dependancy Level:** 2  
**Name:** base_screen  
**Type:** ScreenObject  
**Relative Path:** e2e_tests_mobile/common/screen_objects/base_screen.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - ScreenObjectModel
    
**Members:**
    
    - **Name:** driver  
**Type:** appium.webdriver.Remote  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - driver
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** find_element_by_accessibility_id  
**Parameters:**
    
    - acc_id: str
    
**Return Type:** WebElement  
**Attributes:** protected  
    - **Name:** tap_element  
**Parameters:**
    
    - element: WebElement
    
**Return Type:** void  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Base Screen Object Functionality
    
**Requirement Ids:**
    
    
**Purpose:** To provide common functionalities for mobile screen objects.  
**Logic Description:** Similar to BasePage, but for mobile screens using Appium. Contains methods for finding elements by various strategies (ID, accessibility ID, XPath) and performing common mobile gestures like tap, swipe.  
**Documentation:**
    
    - **Summary:** Base class for mobile screen objects, encapsulating common Appium interactions.
    
**Namespace:** dfr.testing.automation.e2e_tests_mobile.common.screen_objects  
**Metadata:**
    
    - **Category:** UITestingFramework
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/android/test_android_farmer_registration_offline.py  
**Description:** Appium/PyTest E2E test case for farmer registration on the Android app in offline mode.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 4  
**Name:** test_android_farmer_registration_offline  
**Type:** TestScript  
**Relative Path:** e2e_tests_mobile/android/test_android_farmer_registration_offline.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    - ScreenObjectModel
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_register_farmer_offline_and_verify_local_storage  
**Parameters:**
    
    - appium_android_driver
    - test_data_loader_mobile
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Mobile E2E Test: Offline Farmer Registration (Android)
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - A.4
    
**Purpose:** To verify that farmer registration can be completed offline on the Android app and data is stored locally.  
**Logic Description:** Uses an `appium_android_driver` fixture. Simulates turning off network connectivity. Navigates through the app using Screen Objects, fills farmer registration details, saves the record. Verifies data is saved in the local mobile DB (might require specific test hooks or querying local DB if possible in test environment). Also checks security aspects of offline storage (A.4).  
**Documentation:**
    
    - **Summary:** End-to-end test for offline farmer registration on the DFR Android mobile application.
    
**Namespace:** dfr.testing.automation.e2e_tests_mobile.android  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/performance_mobile/test_app_startup_time.py  
**Description:** Measures the startup time of the DFR mobile application, aligning with B.5 acceptance criteria.  
**Template:** Python PyTest Test Case  
**Dependancy Level:** 4  
**Name:** test_app_startup_time  
**Type:** TestScript  
**Relative Path:** e2e_tests_mobile/performance_mobile/test_app_startup_time.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** MAX_APP_STARTUP_TIME_S  
**Type:** int  
**Attributes:** private|static  
**Value:** 5  
    
**Methods:**
    
    - **Name:** test_mobile_app_cold_start_performance  
**Parameters:**
    
    - appium_android_driver_factory
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Mobile App Performance Test: Startup Time
    
**Requirement Ids:**
    
    - B.5
    - REQ-PCA-013
    
**Purpose:** To ensure the mobile application starts within an acceptable time frame for good user experience.  
**Logic Description:** This test will use Appium to launch the application from a cold start (not running in the background). It will measure the time taken from launching the app until a specific element on the main screen is visible. Asserts that this time is within the performance targets specified or implied by B.5.  
**Documentation:**
    
    - **Summary:** Performance test for measuring the cold startup time of the DFR mobile application.
    
**Namespace:** dfr.testing.automation.e2e_tests_mobile.performance_mobile  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/flutter_tests/test/farmer_registration_test.dart  
**Description:** Flutter Driver test case for farmer registration on the DFR mobile app (if Flutter is used and Flutter Driver tests are preferred for some scenarios).  
**Template:** Dart Flutter Driver Test Case  
**Dependancy Level:** 3  
**Name:** farmer_registration_test  
**Type:** TestScript  
**Relative Path:** e2e_tests_mobile/flutter_tests/test/farmer_registration_test.dart  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** testFarmerRegistrationFlow  
**Parameters:**
    
    - FlutterDriver driver
    
**Return Type:** Future<void>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Mobile E2E Test: Farmer Registration (Flutter)
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To verify the farmer registration flow using Flutter Driver tests within the Flutter testing framework.  
**Logic Description:** This Dart file uses the `flutter_driver` package. It defines test groups and test cases. Interacts with Flutter widgets using `find.byValueKey`, `driver.tap()`, `driver.enterText()`. Asserts widget states or navigation outcomes.  
**Documentation:**
    
    - **Summary:** Flutter Driver test for the farmer registration functionality in the DFR mobile app.
    
**Namespace:** dfr.testing.automation.e2e_tests_mobile.flutter_tests  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/e2e_tests_mobile/flutter_tests/pubspec.yaml  
**Description:** Dependencies for Flutter Driver tests, including `flutter_driver` and `test`.  
**Template:** YAML Configuration  
**Dependancy Level:** 0  
**Name:** pubspec_flutter_tests  
**Type:** DependencyManagement  
**Relative Path:** e2e_tests_mobile/flutter_tests/pubspec.yaml  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Flutter Test Dependency Management
    
**Requirement Ids:**
    
    
**Purpose:** To define dependencies for running Flutter Driver tests.  
**Logic Description:** A standard `pubspec.yaml` file listing `flutter_driver`, `test`, and any other necessary Dart packages under `dev_dependencies`.  
**Documentation:**
    
    - **Summary:** Flutter package manifest for the mobile app's Flutter Driver tests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_testing/automation_suite/integration_tests_odoo/common/odoo_test_helper.py  
**Description:** Helper functions or classes for setting up the Odoo test environment, creating test records directly via ORM, or interacting with Odoo services for integration tests.  
**Template:** Python Odoo Utility  
**Dependancy Level:** 1  
**Name:** odoo_test_helper  
**Type:** Utility  
**Relative Path:** integration_tests_odoo/common/odoo_test_helper.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_test_farmer  
**Parameters:**
    
    - odoo_env
    - name: str
    - uid: str
    
**Return Type:** odoo.model.BaseModel  
**Attributes:** public|static  
    - **Name:** get_service  
**Parameters:**
    
    - odoo_env
    - service_name: str
    
**Return Type:** object  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Odoo Integration Test Setup Utilities
    
**Requirement Ids:**
    
    
**Purpose:** To simplify interaction with the Odoo environment and data setup for integration tests.  
**Logic Description:** Contains functions that use the Odoo ORM (`env`) to create prerequisite data (e.g., a test farmer, a dynamic form definition). May also provide easy access to Odoo services needed by tests.  
**Documentation:**
    
    - **Summary:** Utility functions to support Odoo integration testing, such as data creation and service access.
    
**Namespace:** dfr.testing.automation.integration_tests_odoo.common  
**Metadata:**
    
    - **Category:** OdooIntegration
    
- **Path:** dfr_testing/automation_suite/integration_tests_odoo/farmer_registry_integration/test_deduplication_logic.py  
**Description:** PyTest/Odoo integration test for the farmer de-duplication logic within Odoo modules.  
**Template:** Python PyTest Odoo Test Case  
**Dependancy Level:** 3  
**Name:** test_deduplication_logic  
**Type:** TestScript  
**Relative Path:** integration_tests_odoo/farmer_registry_integration/test_deduplication_logic.py  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_create_duplicate_farmer_by_national_id  
**Parameters:**
    
    - odoo_env_fixture
    - odoo_test_helper
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_fuzzy_match_deduplication  
**Parameters:**
    
    - odoo_env_fixture
    - odoo_test_helper
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Odoo Integration Test: De-duplication Logic
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To verify the correctness and effectiveness of the de-duplication rules and algorithms implemented in the Odoo backend.  
**Logic Description:** Uses an `odoo_env_fixture` (from Odoo test framework or custom conftest.py for integration tests) to get an Odoo environment. Creates farmer records via ORM that should trigger de-duplication rules (exact matches on National ID, fuzzy matches on name/village). Asserts that potential duplicates are flagged or prevented as per system design.  
**Documentation:**
    
    - **Summary:** Integration tests for the farmer de-duplication logic within the DFR Odoo modules.
    
**Namespace:** dfr.testing.automation.integration_tests_odoo.farmer_registry_integration  
**Metadata:**
    
    - **Category:** Testing
    
- **Path:** dfr_testing/automation_suite/test_data/api/valid_farmer_data.json  
**Description:** JSON file containing valid test data for creating a farmer via API.  
**Template:** JSON Test Data  
**Dependancy Level:** 0  
**Name:** valid_farmer_data  
**Type:** TestData  
**Relative Path:** test_data/api/valid_farmer_data.json  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Test Data Provisioning
    
**Requirement Ids:**
    
    
**Purpose:** To supply valid data payloads for API testing scenarios related to farmer creation.  
**Logic Description:** A JSON object or array of objects, where each object represents a farmer with all required and optional fields populated with valid data according to the API schema.  
**Documentation:**
    
    - **Summary:** Contains valid sample data for farmer creation API requests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestData
    
- **Path:** dfr_testing/automation_suite/runners/run_api_tests.sh  
**Description:** Shell script to execute all API tests using PyTest. Can accept parameters for environment selection or specific test markers.  
**Template:** Shell Script  
**Dependancy Level:** 4  
**Name:** run_api_tests  
**Type:** TestRunner  
**Relative Path:** runners/run_api_tests.sh  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Test Execution Orchestration
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To provide a command-line interface for running the API test suite, suitable for local execution and CI/CD pipelines.  
**Logic Description:** This script will navigate to the `api_tests` directory (or run from root) and execute `pytest` with appropriate arguments. Arguments might include selecting test markers (e.g., `-m smoke`), specifying the target environment configuration, and configuring HTML report generation.  
**Documentation:**
    
    - **Summary:** Script to trigger the execution of the API test suite.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Execution
    
- **Path:** dfr_testing/automation_suite/runners/run_all_tests.sh  
**Description:** Master shell script to execute all test suites (API, Web E2E, Mobile E2E, Odoo Integration) sequentially or in parallel if configured.  
**Template:** Shell Script  
**Dependancy Level:** 5  
**Name:** run_all_tests  
**Type:** TestRunner  
**Relative Path:** runners/run_all_tests.sh  
**Repository Id:** DFR_TEST_AUTOMATION  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Comprehensive Test Suite Execution
    
**Requirement Ids:**
    
    - REQ-PCA-013
    
**Purpose:** To provide a single command to run the entire DFR test automation suite for full regression testing or release validation.  
**Logic Description:** This script will call the individual test runner scripts (`run_api_tests.sh`, `run_web_e2e_tests.sh`, etc.) in a defined order. It might include logic for aggregating results or exiting on first failure depending on configuration.  
**Documentation:**
    
    - **Summary:** A master script to execute all available automated test suites for the DFR platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Execution
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - RUN_PERFORMANCE_TESTS
  - RUN_SECURITY_SCANS_INTEGRATED
  
- **Database Configs:**
  
  - ODOO_INTEGRATION_DB_HOST
  - ODOO_INTEGRATION_DB_PORT
  - ODOO_INTEGRATION_DB_USER
  - ODOO_INTEGRATION_DB_PASSWORD
  - ODOO_INTEGRATION_DB_NAME
  


---

