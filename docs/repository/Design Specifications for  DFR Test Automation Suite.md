markdown
# Software Design Specification: DFR Test Automation Suite

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the DFR Test Automation Suite. This suite is responsible for ensuring the quality, reliability, performance, and security of the Digital Farmer Registry (DFR) platform through various automated testing levels. It covers Odoo module integration tests, API tests, end-to-end (E2E) tests for web portals (Admin and Farmer Self-Service), and mobile application UI automation tests (Android).

### 1.2 Scope
The scope of this SDS includes:
-   Configuration management for the test suite.
-   Utility modules for logging, reporting, and common test operations.
-   API testing framework components: API client, authentication handler, test data loader, response validator, and API test scripts.
-   Web E2E testing framework components: WebDriver setup, Page Object Model (POM) base classes, specific Page Objects, and web E2E test scripts.
-   Mobile E2E testing framework components: Appium/Flutter Driver setup, Screen Object Model base classes, specific Screen Objects, and mobile E2E test scripts for Android.
-   Odoo integration testing framework components: Odoo test helpers and integration test scripts.
-   Test data management strategy.
-   Test execution runners.

### 1.3 Acronyms and Abbreviations
-   **DFR**: Digital Farmer Registry
-   **API**: Application Programming Interface
-   **E2E**: End-to-End
-   **UI**: User Interface
-   **POM**: Page Object Model
-   **SOM**: Screen Object Model
-   **SDS**: Software Design Specification
-   **CI/CD**: Continuous Integration / Continuous Deployment
-   **SDK**: Software Development Kit
-   **JWT**: JSON Web Token
-   **XSS**: Cross-Site Scripting
-   **PyTest**: Python Testing Framework
-   **Selenium**: Web Browser Automation Framework
-   **Appium**: Mobile Application Automation Framework
-   **Flutter Driver**: UI testing framework for Flutter applications
-   **Newman**: Command-line Collection Runner for Postman

## 2. System Overview

The DFR Test Automation Suite is a standalone repository designed to interact with and validate the various components of the DFR platform. It will use a combination of industry-standard testing frameworks and custom utilities to achieve comprehensive test coverage.

**Key Test Types:**
1.  **API Tests (PyTest, Requests):** Validate the DFR backend RESTful APIs for functionality, security, and performance.
2.  **Web E2E Tests (Selenium, PyTest):** Validate the Admin Portal and Farmer Self-Service Portal user interfaces and workflows.
3.  **Mobile E2E Tests (Appium/Python or Flutter Driver/Dart):** Validate the Android mobile enumerator application UI and workflows, including offline capabilities.
4.  **Odoo Integration Tests (PyTest, Odoo Test Environment):** Validate interactions between different Odoo modules and specific business logic within the Odoo backend.

## 3. Design Considerations

### 3.1 Modularity and Reusability
-   The suite will be structured modularly, with clear separation between test types, common utilities, page/screen objects, and test scripts.
-   Reusable components like API clients, base page/screen objects, and utility functions will be prioritized to reduce code duplication and improve maintainability.

### 3.2 Configurability
-   Environment-specific configurations (URLs, credentials, etc.) will be externalized from test scripts to allow easy execution against different DFR instances (Dev, Staging).
-   Global test parameters (timeouts, common paths) will be centrally managed.

### 3.3 Maintainability
-   Clear naming conventions for files, classes, methods, and variables.
-   Adherence to Page Object Model (POM) and Screen Object Model (SOM) design patterns for UI tests.
-   Comprehensive logging and reporting to aid in debugging test failures.

### 3.4 Scalability
-   The test suite architecture should support the addition of new test cases and test data with minimal effort.
-   Test runners should allow for selective execution of tests (e.g., smoke, regression, specific features).

### 3.5 CI/CD Integration
-   Test execution scripts will be designed for easy integration into CI/CD pipelines.
-   Reporting mechanisms will be CI/CD friendly (e.g., JUnit XML reports, HTML reports).

## 4. High-Level Architecture
The test suite will be organized into the following main directories:
-   `config/`: Configuration files for environments and global settings.
-   `utils/`: Common utility modules (logging, reporting).
-   `api_tests/`: API test scripts and related common components.
-   `e2e_tests_web/`: Web E2E test scripts and related common components (Page Objects).
-   `e2e_tests_mobile/`: Mobile E2E test scripts and related common components (Screen Objects).
-   `integration_tests_odoo/`: Odoo integration test scripts and helpers.
-   `test_data/`: Test data files organized by test type.
-   `runners/`: Scripts for executing test suites.
-   `reports/`: Directory for storing test execution reports (generated, not committed).

## 5. Detailed Design Specification

### 5.1 Core Configuration and Utilities

#### 5.1.1 `requirements.txt`
-   **Purpose:** Defines Python package dependencies.
-   **Content:**
    
    pytest==8.2.2
    pytest-html==4.1.1  # For HTML reports
    pytest-xdist==3.6.1 # For parallel test execution (optional)
    pytest-benchmark==4.0.0 # For performance benchmarking in pytest
    selenium==4.21.0
    Appium-Python-Client==4.0.0
    requests==2.32.3
    jsonschema==4.22.0 # For API response schema validation
    # Add other utility libraries as needed, e.g., for INI parsing if not using configparser directly
    configparser==7.0.0
    PyYAML==6.0.1 # For YAML based test data or config if needed
    
-   **Documentation:** Comments within the file explaining key dependencies.

#### 5.1.2 `pytest.ini`
-   **Purpose:** Configures PyTest execution environment.
-   **Content Structure:**
    ini
    [pytest]
    minversion = 7.0
    testpaths = api_tests e2e_tests_web e2e_tests_mobile integration_tests_odoo
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*

    # Markers for selective test runs
    markers =
        smoke: marks tests as smoke tests (for quick sanity checks)
        regression: marks tests as regression tests (for full suite runs)
        api: marks API tests
        web: marks Web E2E tests
        mobile_android: marks Android Mobile E2E tests
        mobile_flutter: marks Flutter Mobile E2E tests
        integration: marks Odoo integration tests
        security: marks security-focused tests
        performance: marks performance-focused tests
        farmer_lookup: tests related to farmer lookup
        auth: tests related to authentication

    # Logging configuration
    log_cli = true
    log_cli_level = INFO
    log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
    log_file = reports/pytest_run.log
    log_file_level = DEBUG
    log_file_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s (%(filename)s:%(lineno)s)

    # Add options for pytest-html report
    addopts = --html=reports/pytest_report.html --self-contained-html

    # Example: Environment variable setup (can be overridden by runners)
    # env =
    #     DFR_ENV=dev
    
-   **Documentation:** Comments within the file explaining sections and options.

#### 5.1.3 `config/global_config.py`
-   **Purpose:** Centralized global test configurations.
-   **Module:** `dfr.testing.automation.config.global_config`
-   **Class/Constants:**
    python
    import os
    from pathlib import Path

    # Base directory for the test suite
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Environment URLs (can be overridden by specific env configs or environment variables)
    BASE_URL_DEV_API = "http://dev-dfr-api.example.com/api/v1"
    BASE_URL_DEV_WEB_ADMIN = "http://dev-dfr-admin.example.com"
    BASE_URL_DEV_WEB_PORTAL = "http://dev-dfr-portal.example.com"

    BASE_URL_STAGING_API = "http://staging-dfr-api.example.com/api/v1"
    BASE_URL_STAGING_WEB_ADMIN = "http://staging-dfr-admin.example.com"
    BASE_URL_STAGING_WEB_PORTAL = "http://staging-dfr-portal.example.com"

    # Default Timeouts
    DEFAULT_TIMEOUT_SECONDS = 30  # For web element waits, API call timeouts
    POLL_FREQUENCY_SECONDS = 0.5 # For explicit waits

    # Test Data Paths
    TEST_DATA_BASE_PATH = BASE_DIR / "test_data"
    API_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "api"
    WEB_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "web"
    MOBILE_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "mobile"

    # Reporting
    REPORTS_DIR = BASE_DIR / "reports"
    SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

    # Appium Server Configuration
    APPIUM_SERVER_URL = "http://localhost:4723/wd/hub" # Default, can be overridden

    # Flutter Driver Configuration
    FLUTTER_VM_SERVICE_URL_ENV_VAR = "VM_SERVICE_URL" # Environment variable to get VM service URL

    def get_target_environment():
        """
        Determines the target environment based on an environment variable or a default.
        Returns:
            str: The target environment name (e.g., 'dev', 'staging').
        """
        return os.getenv("DFR_TARGET_ENV", "dev").lower()

    def get_api_base_url(env_name: str = None) -> str:
        target_env = env_name or get_target_environment()
        if target_env == "staging":
            return BASE_URL_STAGING_API
        return BASE_URL_DEV_API # Default to dev

    def get_web_admin_url(env_name: str = None) -> str:
        target_env = env_name or get_target_environment()
        if target_env == "staging":
            return BASE_URL_STAGING_WEB_ADMIN
        return BASE_URL_DEV_WEB_ADMIN

    def get_web_portal_url(env_name: str = None) -> str:
        target_env = env_name or get_target_environment()
        if target_env == "staging":
            return BASE_URL_STAGING_WEB_PORTAL
        return BASE_URL_DEV_WEB_PORTAL

    # Ensure report directories exist
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
-   **Documentation:** Docstrings for functions.

#### 5.1.4 `config/dev_env_config.ini` & `config/staging_env_config.ini`
-   **Purpose:** Environment-specific settings.
-   **Structure (Example for `dev_env_config.ini`):**
    ini
    [API]
    base_url = http://localhost:8069/api/v1  # Example DFR API running locally for dev
    admin_user = dev_admin_user
    admin_password_secret_ref = DFR_DEV_ADMIN_PASS # Reference to env var or secrets manager
    enumerator_user = dev_enum_user
    enumerator_password_secret_ref = DFR_DEV_ENUM_PASS

    [WEB_ADMIN_PORTAL]
    base_url = http://localhost:8069 # Example Odoo admin portal

    [WEB_FARMER_PORTAL]
    base_url = http://localhost:8069/farmer-portal # Example farmer portal

    [MOBILE_ANDROID]
    app_path = /path/to/dev/dfr_android_app.apk
    device_name = emulator-5554 # Or a specific physical device UDID for dev
    platform_version = 13.0

    [MOBILE_FLUTTER]
    # Flutter tests typically connect to an already running app, VM service URL is key
    # No specific app path needed here if app is pre-installed for Flutter Driver tests

    [ODOO_INTEGRATION_DB]
    host = localhost
    port = 5432
    user = odoo_dev_user
    password_secret_ref = ODOO_DEV_DB_PASS
    name = dfr_dev_db
    
-   **Note:** Passwords and sensitive credentials should ideally be fetched from environment variables or a secrets management tool, not hardcoded in these INI files. The `_secret_ref` suffix suggests this. Test scripts or a config loader utility will read these INI files.
-   **Documentation:** Comments within the INI files explaining sections and keys.

#### 5.1.5 `utils/logger_setup.py`
-   **Purpose:** Standardized test logging.
-   **Module:** `dfr.testing.automation.utils.logger_setup`
-   **Content:**
    python
    import logging
    import sys
    from dfr.testing.automation.config import global_config # Assuming this path after restructuring

    def setup_logger(name: str = 'DFR_Test_Logger', log_level: str = 'INFO', log_file=None):
        """
        Configures and returns a logger instance.

        Args:
            name (str): Name of the logger.
            log_level (str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
            log_file (str, optional): Path to the log file. If None, logs only to console.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        
        # Prevent adding multiple handlers if logger already configured
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)8s] - %(module)s.%(funcName)s:%(lineno)d - %(message)s'
        )

        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File Handler
        if log_file:
            log_file_path = global_config.REPORTS_DIR / log_file
            fh = logging.FileHandler(log_file_path, mode='a') # Append mode
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        
        logger.propagate = False # Avoid duplicate logs if root logger is also configured
        return logger

    # Example of a default logger instance for easy import
    # test_logger = setup_logger(log_file="test_run.log")
    
-   **Documentation:** Docstrings for the function.

#### 5.1.6 `utils/reporting_utils.py`
-   **Purpose:** Custom test reporting enhancements.
-   **Module:** `dfr.testing.automation.utils.reporting_utils`
-   **Content:**
    python
    import os
    import datetime
    from dfr.testing.automation.config import global_config # Assuming path
    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    def capture_screenshot_selenium(driver, test_name: str):
        """
        Captures a screenshot using Selenium WebDriver and saves it.
        File name includes a timestamp.
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{test_name}_{timestamp}.png"
            screenshot_path = global_config.SCREENSHOTS_DIR / file_name
            driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot captured: {screenshot_path}")
            return str(screenshot_path) # Return path for reporting
        except Exception as e:
            logger.error(f"Failed to capture screenshot for {test_name}: {e}")
            return None

    def capture_screenshot_appium(driver, test_name: str):
        """
        Captures a screenshot using Appium WebDriver and saves it.
        File name includes a timestamp.
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{test_name}_{timestamp}.png"
            screenshot_path = global_config.SCREENSHOTS_DIR / file_name
            driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot captured: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            logger.error(f"Failed to capture screenshot for {test_name}: {e}")
            return None
    
    def log_test_result_to_file(test_name: str, status: str, message: str = None, duration: float = None, screenshot_path: str = None):
        """
        Logs detailed test results to a custom CSV or text file.
        (This is an example; PyTest's built-in reporting or plugins like pytest-html are usually preferred)
        """
        custom_report_file = global_config.REPORTS_DIR / "custom_test_results.csv"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration_str = f"{duration:.2f}s" if duration is not None else "N/A"
        message_str = message or ""
        screenshot_str = screenshot_path or "N/A"
        
        header = "Timestamp,TestName,Status,Duration,Message,Screenshot\n"
        if not custom_report_file.exists():
            with open(custom_report_file, "w") as f:
                f.write(header)
        
        with open(custom_report_file, "a") as f:
            f.write(f'"{timestamp}","{test_name}","{status}","{duration_str}","{message_str}","{screenshot_str}"\n')
        logger.info(f"Logged result for {test_name}: {status}")

    # Other potential functions:
    # - update_test_management_tool(test_case_id, status, comments)
    
-   **Documentation:** Docstrings for functions.

### 5.2 API Testing (`api_tests/`)

#### 5.2.1 `api_tests/common/api_client.py`
-   **Purpose:** Reusable API client for DFR backend.
-   **Module:** `dfr.testing.automation.api_tests.common.api_client`
-   **Class:** `ApiClient`
    python
    import requests
    import json
    from dfr.testing.automation.utils.logger_setup import setup_logger
    from dfr.testing.automation.config import global_config

    logger = setup_logger(__name__)

    class ApiClient:
        def __init__(self, base_url: str = None, auth_handler=None): # auth_handler can be an instance of AuthHandler
            self.base_url = base_url or global_config.get_api_base_url()
            self.session = requests.Session()
            self.auth_handler = auth_handler
            self.session.headers.update({"Content-Type": "application/json"})
            logger.info(f"ApiClient initialized with base_url: {self.base_url}")

        def _get_auth_headers(self) -> dict:
            if self.auth_handler:
                return self.auth_handler.get_auth_header()
            return {}

        def request(self, method: str, endpoint: str, params: dict = None, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
            url = f"{self.base_url}{endpoint}"
            request_headers = self.session.headers.copy()
            request_headers.update(self._get_auth_headers())
            if headers:
                request_headers.update(headers)

            logger.debug(f"Request: {method.upper()} {url}")
            if params: logger.debug(f"Params: {params}")
            if data: logger.debug(f"Data: {data}") # form-data
            if json_payload: logger.debug(f"JSON Payload: {json.dumps(json_payload, indent=2)}") # Pretty print JSON
            
            try:
                response = self.session.request(
                    method, url, params=params, data=data, json=json_payload, headers=request_headers, 
                    timeout=global_config.DEFAULT_TIMEOUT_SECONDS, **kwargs
                )
                logger.info(f"Response: {response.status_code} {response.reason} from {url}")
                try:
                    logger.debug(f"Response Body: {response.json()}")
                except requests.exceptions.JSONDecodeError:
                    logger.debug(f"Response Body (Non-JSON): {response.text[:500]}...") # Log first 500 chars
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"API Request failed for {method.upper()} {url}: {e}")
                raise # Re-raise the exception to fail the test

        def get(self, endpoint: str, params: dict = None, headers: dict = None, **kwargs) -> requests.Response:
            return self.request("GET", endpoint, params=params, headers=headers, **kwargs)

        def post(self, endpoint: str, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
            return self.request("POST", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

        def put(self, endpoint: str, data: dict = None, json_payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
            return self.request("PUT", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

        def delete(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
            return self.request("DELETE", endpoint, headers=headers, **kwargs)
    
-   **Documentation:** Docstrings for class and methods.

#### 5.2.2 `api_tests/common/auth_handler.py`
-   **Purpose:** Manages API authentication (OAuth2/JWT).
-   **Module:** `dfr.testing.automation.api_tests.common.auth_handler`
-   **Class:** `AuthHandler` (example for JWT Bearer token)
    python
    import time
    import requests # For actual authentication if needed by a separate request
    from dfr.testing.automation.utils.logger_setup import setup_logger
    from dfr.testing.automation.config import global_config # For API URL
    # Assume config loader for user credentials from INI or env
    # from dfr.testing.automation.utils.config_loader import get_env_credential 

    logger = setup_logger(__name__)

    class AuthHandler:
        _token: str = None
        _token_expiry_timestamp: float = 0 # Unix timestamp
        _token_refresh_buffer_seconds: int = 60 # Refresh token if it expires within this buffer

        def __init__(self, auth_url_endpoint: str, client_id: str, client_secret: str, audience: str = None): # Example for OAuth2 client credentials
            self.auth_url = f"{global_config.get_api_base_url().rsplit('/api', 1)[0]}{auth_url_endpoint}" # Assuming auth endpoint is relative to base API
            self.client_id = client_id
            self.client_secret = client_secret
            self.audience = audience # Optional, for OAuth2
            logger.info("AuthHandler initialized.")

        def _is_token_valid(self) -> bool:
            if not self._token:
                return False
            # For JWT, could decode and check 'exp' claim if expiry is not returned separately
            return time.time() < (self._token_expiry_timestamp - self._token_refresh_buffer_seconds)

        def _fetch_token_oauth_client_credentials(self) -> None:
            """Example: Fetches a token using OAuth2 client credentials grant type."""
            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            if self.audience:
                payload['audience'] = self.audience
            
            logger.info(f"Attempting to fetch new token from {self.auth_url}")
            try:
                response = requests.post(self.auth_url, data=payload, timeout=global_config.DEFAULT_TIMEOUT_SECONDS)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                token_data = response.json()
                
                self._token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600) # Default to 1 hour if not provided
                self._token_expiry_timestamp = time.time() + expires_in
                
                if not self._token:
                    raise ValueError("Access token not found in authentication response.")
                logger.info("Successfully fetched new authentication token.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch token: {e}")
                raise
            except ValueError as e:
                logger.error(f"Token parsing error: {e}")
                raise


        def authenticate_user_password(self, username, password, token_endpoint="/auth/token"): # Example JWT
            """
            Authenticates a user and stores the token.
            This is a simplified example; actual DFR auth might differ.
            """
            logger.info(f"Authenticating user: {username}")
            # In a real JWT scenario, this would post to a token endpoint
            # For DFR, this might be /api/auth/login or similar from REQ-API-003
            # This method is illustrative. The actual DFR_MOD_API_GATEWAY spec will define auth.
            # For now, we'll simulate or directly set if an actual endpoint is not yet designed for tests.

            # Placeholder: Simulating fetching a token based on username/password if needed
            # This would typically involve a POST request to an auth server
            # For example:
            # auth_api_url = global_config.get_api_base_url()
            # response = requests.post(f"{auth_api_url}{token_endpoint}", data={"username": username, "password": password})
            # if response.status_code == 200:
            #     self._token = response.json().get("access_token")
            #     self._token_expiry_timestamp = time.time() + response.json().get("expires_in", 3600) # Example
            #     logger.info(f"User {username} authenticated. Token acquired.")
            # else:
            #     logger.error(f"Authentication failed for user {username}: {response.status_code} - {response.text}")
            #     self._token = None
            #     raise Exception(f"Authentication failed for {username}")
            
            # For testing purposes, if direct token fetch isn't the primary test focus here,
            # assume the token can be set externally or a mock is used.
            # This handler mainly focuses on *providing* the auth header once a token is present.
            # The _fetch_token_oauth_client_credentials shows a more complete fetch example.
            # Let's assume for REQ-API-003 we have a way to get a token.
            # If `auth_handler` instance is specific to a user, it would call its own auth method.

            # If using OAuth client credentials, call:
            # self._fetch_token_oauth_client_credentials()
            pass # Actual implementation depends on DFR auth specifics.


        def get_auth_header(self) -> dict:
            if not self._is_token_valid():
                logger.info("Token is invalid or expired. Attempting to refresh/re-authenticate.")
                # Depending on the auth flow (e.g., OAuth2 refresh token, or re-auth with credentials)
                # For client credentials, just re-fetch:
                try:
                    self._fetch_token_oauth_client_credentials() # Or a user-specific auth method
                except Exception as e:
                    logger.error(f"Failed to refresh/re-authenticate: {e}")
                    return {} # Return empty if auth fails, request will likely fail server-side
            
            if self._token:
                return {"Authorization": f"Bearer {self._token}"}
            return {}
    
-   **Documentation:** Docstrings. Logic for actual token acquisition depends on the DFR auth server implementation (`DFR_MOD_API_GATEWAY`).

#### 5.2.3 `api_tests/common/test_data_loader.py`
-   **Purpose:** Loads test data for API tests.
-   **Module:** `dfr.testing.automation.api_tests.common.test_data_loader`
-   **Content:**
    python
    import json
    from pathlib import Path
    from dfr.testing.automation.config import global_config
    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    class ApiTestDataLoader:
        _test_data_cache = {}

        @staticmethod
        def _load_json_file(file_path: Path) -> dict:
            if str(file_path) in ApiTestDataLoader._test_data_cache:
                return ApiTestDataLoader._test_data_cache[str(file_path)]
            
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    ApiTestDataLoader._test_data_cache[str(file_path)] = data
                    logger.debug(f"Loaded test data from: {file_path}")
                    return data
            except FileNotFoundError:
                logger.error(f"Test data file not found: {file_path}")
                raise
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from file {file_path}: {e}")
                raise

        @staticmethod
        def get_data(file_name: str, scenario_key: str = None):
            """
            Loads data from a JSON file in the API test data directory.
            If scenario_key is provided, returns the data under that key.
            Otherwise, returns the entire file content.
            """
            file_path = global_config.API_TEST_DATA_PATH / file_name
            data_content = ApiTestDataLoader._load_json_file(file_path)
            
            if scenario_key:
                if scenario_key in data_content:
                    logger.debug(f"Returning data for scenario '{scenario_key}' from {file_name}")
                    return data_content[scenario_key]
                else:
                    logger.error(f"Scenario key '{scenario_key}' not found in {file_name}")
                    raise KeyError(f"Scenario key '{scenario_key}' not found in {file_name}")
            return data_content

        @staticmethod
        def get_farmer_creation_data(scenario: str = "valid_default"):
            """Helper to get farmer creation data."""
            return ApiTestDataLoader.get_data("farmer_creation_data.json", scenario)

        # Add more specific helpers as needed
        # e.g., get_farmer_lookup_params(scenario: str)
    
-   **Documentation:** Docstrings. Test data files (e.g., `farmer_creation_data.json`) would reside in `test_data/api/`.

#### 5.2.4 `api_tests/common/response_validator.py`
-   **Purpose:** Validates API responses.
-   **Module:** `dfr.testing.automation.api_tests.common.response_validator`
-   **Content:**
    python
    import requests
    from jsonschema import validate, exceptions as jsonschema_exceptions
    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    class ResponseValidator:
        @staticmethod
        def assert_status_code(response: requests.Response, expected_code: int):
            """Asserts the HTTP status code of the response."""
            actual_code = response.status_code
            assert actual_code == expected_code, \
                f"Expected status code {expected_code}, but got {actual_code}. Response: {response.text[:200]}"
            logger.info(f"Status code assertion passed: {actual_code} == {expected_code}")

        @staticmethod
        def validate_json_schema(response_json: dict, schema: dict):
            """Validates a JSON object against a given JSON schema."""
            try:
                validate(instance=response_json, schema=schema)
                logger.info("JSON schema validation passed.")
            except jsonschema_exceptions.ValidationError as e:
                logger.error(f"JSON schema validation failed: {e.message}")
                raise AssertionError(f"JSON schema validation failed: {e.message} on instance {str(response_json)[:200]}")

        @staticmethod
        def assert_response_contains_key(response_json: dict, key: str, path: list = None):
            """Asserts that a key exists in the response JSON, potentially at a nested path."""
            current_level = response_json
            if path:
                for p_key in path:
                    assert p_key in current_level, f"Key '{p_key}' not found in path {'.'.join(path)} in response: {str(response_json)[:200]}"
                    current_level = current_level[p_key]
            
            assert key in current_level, f"Key '{key}' not found at specified level in response: {str(response_json)[:200]}"
            logger.info(f"Key '{key}' found in response.")

        @staticmethod
        def assert_response_key_value(response_json: dict, key: str, expected_value, path: list = None):
            """Asserts that a key has an expected value in the response JSON."""
            ResponseValidator.assert_response_contains_key(response_json, key, path)
            current_level = response_json
            if path:
                for p_key in path:
                    current_level = current_level[p_key]
            
            actual_value = current_level[key]
            assert actual_value == expected_value, \
                f"Expected value '{expected_value}' for key '{key}', but got '{actual_value}'. Response: {str(response_json)[:200]}"
            logger.info(f"Value assertion passed for key '{key}': '{actual_value}' == '{expected_value}'")
        
        @staticmethod
        def assert_response_is_list_not_empty(response_json: list):
            """Asserts that the response JSON is a list and is not empty."""
            assert isinstance(response_json, list), f"Response is not a list. Got: {type(response_json)}"
            assert len(response_json) > 0, "Response list is empty."
            logger.info(f"Response is a non-empty list with {len(response_json)} items.")

    # Example JSON Schemas (could be loaded from files or defined here for simplicity)
    # Example:
    # FARMER_SCHEMA = {
    #     "type": "object",
    #     "properties": {
    #         "uid": {"type": "string"},
    #         "fullName": {"type": "string"},
    #         # ... other properties
    #     },
    #     "required": ["uid", "fullName"]
    # }
    
-   **Documentation:** Docstrings. JSON schemas would ideally be loaded from separate files or a schema registry.

#### 5.2.5 `api_tests/conftest.py`
-   **Purpose:** PyTest fixtures for API tests.
-   **Module:** `dfr.testing.automation.api_tests.conftest` (PyTest discovers this automatically)
-   **Content:**
    python
    import pytest
    from dfr.testing.automation.api_tests.common.api_client import ApiClient
    from dfr.testing.automation.api_tests.common.auth_handler import AuthHandler
    from dfr.testing.automation.api_tests.common.test_data_loader import ApiTestDataLoader
    from dfr.testing.automation.utils.config_loader import ConfigLoader # Assume a utility to load INI

    # Load environment specific config
    # This could also be done via command-line options to pytest
    # For simplicity, using a ConfigLoader utility here.
    
    @pytest.fixture(scope="session")
    def env_config():
        # Example: Determine environment (dev/staging) from an env var or pytest option
        # For now, hardcoding to 'dev' for this example structure
        # In a real setup, use pytest_addoption to define --env
        # target_env = request.config.getoption("--env") 
        target_env = "dev" # or load from global_config.get_target_environment()
        return ConfigLoader.load_env_config(target_env)

    @pytest.fixture(scope="session")
    def api_base_url(env_config):
        return env_config.get("API", "base_url")
        
    @pytest.fixture(scope="session")
    def admin_auth_handler(api_base_url, env_config):
        # This assumes DFR API uses OAuth2 Client Credentials or similar for admin level access
        # Update client_id, client_secret, audience based on actual DFR auth mechanism
        # These credentials should be fetched securely
        client_id = env_config.get("API", "admin_client_id", fallback="dfr_admin_client") 
        client_secret = os.getenv(env_config.get("API", "admin_client_secret_ref")) # from env
        if not client_secret:
             pytest.skip("Admin client secret not configured for API tests.") # Or fail
        
        # The auth_url_endpoint would be like "/api/auth/token" or similar
        # if DFR_MOD_API_GATEWAY provides an OAuth2 token endpoint
        auth_endpoint = env_config.get("API", "token_endpoint", fallback="/oauth/token") # Example
        handler = AuthHandler(auth_url_endpoint=auth_endpoint, client_id=client_id, client_secret=client_secret)
        # Perform initial authentication if needed, or let ApiClient trigger it
        # handler._fetch_token_oauth_client_credentials() # or handler.authenticate_user_password for user flows
        return handler

    @pytest.fixture(scope="session")
    def enumerator_auth_handler(api_base_url, env_config):
        # Similar to admin_auth_handler but for enumerator-level credentials/client
        client_id = env_config.get("API", "enum_client_id", fallback="dfr_enum_client")
        client_secret = os.getenv(env_config.get("API", "enum_client_secret_ref"))
        if not client_secret:
             pytest.skip("Enumerator client secret not configured for API tests.")
        
        auth_endpoint = env_config.get("API", "token_endpoint", fallback="/oauth/token")
        handler = AuthHandler(auth_url_endpoint=auth_endpoint, client_id=client_id, client_secret=client_secret)
        return handler

    @pytest.fixture(scope="function") # Or "session" if client can be reused without state issues
    def api_client_unauthenticated(api_base_url):
        """Provides an API client without any authentication."""
        return ApiClient(base_url=api_base_url)

    @pytest.fixture(scope="function")
    def admin_api_client(api_base_url, admin_auth_handler):
        """Provides an API client authenticated as an admin."""
        client = ApiClient(base_url=api_base_url, auth_handler=admin_auth_handler)
        # Ensure token is fetched if lazy loading in AuthHandler is not preferred for first use
        # admin_auth_handler.get_auth_header() # This would trigger fetch if token is not valid
        return client
        
    @pytest.fixture(scope="function")
    def enumerator_api_client(api_base_url, enumerator_auth_handler):
        """Provides an API client authenticated as an enumerator."""
        client = ApiClient(base_url=api_base_url, auth_handler=enumerator_auth_handler)
        return client

    @pytest.fixture(scope="session")
    def test_data_loader_api():
        return ApiTestDataLoader()
    
-   **Documentation:** Docstrings for fixtures. Assumes a `ConfigLoader` utility exists.

#### 5.2.6 `api_tests/farmer_registry_api/test_farmer_lookup.py`
-   **Purpose:** Test Farmer Lookup API endpoint.
-   **Module:** `dfr.testing.automation.api_tests.farmer_registry_api.test_farmer_lookup`
-   **Content (Illustrative):**
    python
    import pytest
    from dfr.testing.automation.api_tests.common.response_validator import ResponseValidator
    # Schemas would be defined or loaded, e.g., from response_validator or a dedicated schemas module
    # from dfr.testing.automation.api_tests.schemas import FARMER_SCHEMA, ERROR_SCHEMA

    @pytest.mark.api
    @pytest.mark.farmer_lookup
    @pytest.mark.smoke
    def test_lookup_farmer_by_uid_valid(admin_api_client, test_data_loader_api):
        valid_farmer_uid = test_data_loader_api.get_data("farmer_lookup_data.json", "valid_uid_farmer_1")["uid"]
        response = admin_api_client.get(f"/farmers/{valid_farmer_uid}")
        
        ResponseValidator.assert_status_code(response, 200)
        response_data = response.json()
        # ResponseValidator.validate_json_schema(response_data, FARMER_SCHEMA) # Assuming FARMER_SCHEMA is defined
        ResponseValidator.assert_response_key_value(response_data, "uid", valid_farmer_uid)
        ResponseValidator.assert_response_contains_key(response_data, "fullName")

    @pytest.mark.api
    @pytest.mark.farmer_lookup
    def test_lookup_farmer_by_national_id_valid(admin_api_client, test_data_loader_api):
        # Assume setup where farmer with this national_id exists, or create one via API if needed
        national_id_data = test_data_loader_api.get_data("farmer_lookup_data.json", "valid_national_id_farmer_1")
        params = {"nationalIdNumber": national_id_data["nationalIdNumber"], "nationalIdType": national_id_data["nationalIdType"]}
        response = admin_api_client.get("/farmers/lookup", params=params)

        ResponseValidator.assert_status_code(response, 200)
        response_data = response.json() # Expecting a list if multiple matches, or single object
        ResponseValidator.assert_response_is_list_not_empty(response_data) # Or check for single object
        # Further assertions on the content of the found farmer(s)
        # ResponseValidator.validate_json_schema(response_data[0], FARMER_SCHEMA)


    @pytest.mark.api
    @pytest.mark.farmer_lookup
    def test_lookup_farmer_not_found(admin_api_client):
        non_existent_uid = "00000000-0000-0000-0000-000000000000"
        response = admin_api_client.get(f"/farmers/{non_existent_uid}")
        
        ResponseValidator.assert_status_code(response, 404)
        # ResponseValidator.validate_json_schema(response.json(), ERROR_SCHEMA) # Assuming ERROR_SCHEMA

    @pytest.mark.api
    @pytest.mark.farmer_lookup
    @pytest.mark.auth # Marking it as an auth related test
    def test_lookup_farmer_unauthorized(api_client_unauthenticated): # Uses unauthenticated client
        some_farmer_uid = "some-valid-looking-uid" # Doesn't matter if it exists, auth should fail first
        response = api_client_unauthenticated.get(f"/farmers/{some_farmer_uid}")
        
        ResponseValidator.assert_status_code(response, 401) # Or 403 depending on API design
    
-   **Documentation:** Docstrings, comments. Test data file `farmer_lookup_data.json` is assumed.

#### 5.2.7 `api_tests/security/test_auth_vulnerabilities.py`
-   **Purpose:** Security tests for API authentication.
-   **Module:** `dfr.testing.automation.api_tests.security.test_auth_vulnerabilities`
-   **Content (Illustrative Concepts):**
    python
    import pytest
    from dfr.testing.automation.api_tests.common.response_validator import ResponseValidator
    # For token manipulation, might need a JWT library like PyJWT
    # import jwt
    # from datetime import datetime, timedelta

    @pytest.mark.api
    @pytest.mark.security
    @pytest.mark.auth
    def test_access_with_expired_token(api_client_unauthenticated, admin_auth_handler): # Assuming admin_auth_handler can provide an expired token for test
        # This test requires a way to get/generate an expired token.
        # One way: authenticate, get a token with short expiry, wait, then use it.
        # Or, if auth_handler allows setting a token manually for testing:
        # expired_token = "manually_crafted_or_obtained_expired_token"
        # api_client_unauthenticated.session.headers.update({"Authorization": f"Bearer {expired_token}"})
        
        # More realistically, if admin_auth_handler._token_expiry_timestamp is accessible and modifiable for test:
        if admin_auth_handler._token: # Ensure a token was fetched first
            original_expiry = admin_auth_handler._token_expiry_timestamp
            admin_auth_handler._token_expiry_timestamp = time.time() - 3600 # Set expiry to 1 hour ago
            
            response = api_client_unauthenticated.get("/farmers/some-endpoint-requiring-auth") # Using unauth client, but setting token via handler
            # The api_client_unauthenticated would need to be configured to use the admin_auth_handler's (manipulated) token
            # This fixture setup needs careful design.
            # Alternative: A dedicated fixture that returns an api_client with an intentionally expired token.

            ResponseValidator.assert_status_code(response, 401) # Unauthorized
            
            # Restore original expiry for other tests if handler is session-scoped
            admin_auth_handler._token_expiry_timestamp = original_expiry
        else:
            pytest.skip("Cannot test expired token without an initial valid token from auth_handler.")


    @pytest.mark.api
    @pytest.mark.security
    @pytest.mark.auth
    def test_access_with_tampered_token(api_client_unauthenticated):
        # Craft a tampered JWT (e.g., modified payload, invalid signature)
        # tampered_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJyb2xlIjoiYWRtaW4ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" # Example, signature will be wrong
        # headers = {"Authorization": f"Bearer {tampered_token}"}
        # response = api_client_unauthenticated.get("/some/protected/resource", headers=headers)
        # ResponseValidator.assert_status_code(response, 401) # Or 400 Bad Request
        pytest.skip("Tampered token test needs JWT library and understanding of token structure/signing key.")


    @pytest.mark.api
    @pytest.mark.security
    @pytest.mark.auth
    def test_privilege_escalation_attempt_enum_to_admin_resource(enumerator_api_client):
        # Attempt to access an admin-only resource using an enumerator's token
        # This requires knowing an admin-only endpoint. Let's assume /admin/settings
        response = enumerator_api_client.get("/admin/system-settings") # Fictional admin endpoint
        
        # Expect 403 Forbidden if authenticated but not authorized
        # Or 404 if the endpoint is hidden entirely for non-admins
        assert response.status_code in [403, 404], \
            f"Enumerator accessed admin resource or got unexpected status: {response.status_code}"
    
-   **Documentation:** Detailed comments on test scenarios. Requires careful setup for token manipulation.

#### 5.2.8 `api_tests/performance/test_api_load_farmer_lookup.py`
-   **Purpose:** Performance test Farmer Lookup API.
-   **Module:** `dfr.testing.automation.api_tests.performance.test_api_load_farmer_lookup`
-   **Content:**
    python
    import pytest
    import time
    from dfr.testing.automation.api_tests.common.response_validator import ResponseValidator

    TARGET_RESPONSE_TIME_MS_P95 = 500 # From REQ-API-009
    NUM_REQUESTS_FOR_LOAD = 50 # Example, adjust based on B.5 and REQ-API-009 definition of peak load

    @pytest.mark.api
    @pytest.mark.performance
    @pytest.mark.farmer_lookup
    def test_farmer_lookup_response_time_under_load(admin_api_client, test_data_loader_api, benchmark):
        # Assuming test_data_loader can provide a list of UIDs for load testing
        farmer_uids = test_data_loader_api.get_data("farmer_lookup_perf_data.json", "farmer_uids_set_1")[:NUM_REQUESTS_FOR_LOAD]
        if not farmer_uids:
            pytest.skip("No farmer UIDs available for performance test.")

        def lookup_operation(uid):
            response = admin_api_client.get(f"/farmers/{uid}")
            ResponseValidator.assert_status_code(response, 200) # Ensure functionality during perf test

        # Using pytest-benchmark to measure
        # benchmark(lookup_operation, uid=farmer_uids[0]) # Benchmark a single call
        
        # For multiple calls and P95, custom logic or integration with Locust/k6 might be better.
        # Pytest-benchmark is more for single function calls.
        # Let's do a simplified custom timing for P95 demo:
        
        response_times = []
        for uid in farmer_uids:
            start_time = time.perf_counter()
            lookup_operation(uid) # Call the function we want to time
            end_time = time.perf_counter()
            response_times.append((end_time - start_time) * 1000) # in ms

        response_times.sort()
        p95_index = int(len(response_times) * 0.95) -1
        if p95_index < 0: p95_index = 0 # Handle small sample sizes

        if response_times:
            p95_response_time = response_times[p95_index]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = response_times[-1]
            
            print(f"\nFarmer Lookup Performance (ms) for {len(response_times)} requests:")
            print(f"  Average: {avg_response_time:.2f} ms")
            print(f"  P95: {p95_response_time:.2f} ms")
            print(f"  Max: {max_response_time:.2f} ms")

            assert p95_response_time < TARGET_RESPONSE_TIME_MS_P95, \
                f"P95 response time {p95_response_time:.2f}ms exceeds target {TARGET_RESPONSE_TIME_MS_P95}ms"
        else:
            pytest.fail("No response times recorded for performance test.")

    # If using pytest-benchmark for more granular function benchmarking:
    # def test_single_farmer_lookup_benchmark(admin_api_client, test_data_loader_api, benchmark):
    #     valid_farmer_uid = test_data_loader_api.get_data("farmer_lookup_data.json", "valid_uid_farmer_1")["uid"]
    #     
    #     @benchmark
    #     def operation():
    #         response = admin_api_client.get(f"/farmers/{valid_farmer_uid}")
    #         ResponseValidator.assert_status_code(response, 200)
    #
    #     # Pytest-benchmark will handle assertions against thresholds if configured, or report stats
    #     # benchmark.stats.stats.mean, benchmark.stats.stats.median etc.
    #     # Can set custom fail conditions: benchmark.extra_info['response_time_ms'] = response_time_ms
    #     # Then check `benchmark.extra_info` in `pytest_benchmark_update_json` hook or similar
    
-   **Documentation:** Comments. Requires `farmer_lookup_perf_data.json`. Note on `pytest-benchmark` vs custom P95.

### 5.3 Web E2E Testing (`e2e_tests_web/`)

#### 5.3.1 `e2e_tests_web/common/web_driver_setup.py`
-   **Purpose:** WebDriver lifecycle management.
-   **Module:** `dfr.testing.automation.e2e_tests_web.common.web_driver_setup`
-   **Content:**
    python
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    class WebDriverSetup:
        driver = None

        @staticmethod
        def get_webdriver(browser_name: str = 'chrome', headless: bool = True):
            browser_name = browser_name.lower()
            logger.info(f"Initializing WebDriver for browser: {browser_name}, headless: {headless}")
            
            if browser_name == 'chrome':
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox") # Often needed in CI
                options.add_argument("--disable-dev-shm-usage") # Often needed in CI
                options.add_argument("--window-size=1920,1080")
                try:
                    service = ChromeService(ChromeDriverManager().install())
                    WebDriverSetup.driver = webdriver.Chrome(service=service, options=options)
                except Exception as e:
                    logger.error(f"Failed to initialize Chrome WebDriver: {e}")
                    raise
            elif browser_name == 'firefox':
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                try:
                    service = FirefoxService(GeckoDriverManager().install())
                    WebDriverSetup.driver = webdriver.Firefox(service=service, options=options)
                except Exception as e:
                    logger.error(f"Failed to initialize Firefox WebDriver: {e}")
                    raise
            elif browser_name == 'edge':
                options = webdriver.EdgeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                try:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    WebDriverSetup.driver = webdriver.Edge(service=service, options=options)
                except Exception as e:
                    logger.error(f"Failed to initialize Edge WebDriver: {e}")
                    raise
            else:
                logger.error(f"Unsupported browser: {browser_name}")
                raise ValueError(f"Unsupported browser: {browser_name}")
            
            WebDriverSetup.driver.implicitly_wait(5) # Basic implicit wait
            logger.info(f"{browser_name.capitalize()} WebDriver initialized successfully.")
            return WebDriverSetup.driver

        @staticmethod
        def quit_webdriver():
            if WebDriverSetup.driver:
                try:
                    WebDriverSetup.driver.quit()
                    logger.info("WebDriver quit successfully.")
                    WebDriverSetup.driver = None
                except Exception as e:
                    logger.error(f"Error quitting WebDriver: {e}")
    
-   **Documentation:** Docstrings. Uses `webdriver-manager` for easy driver management.

#### 5.3.2 `e2e_tests_web/common/page_objects/base_page.py`
-   **Purpose:** Base class for Page Objects.
-   **Module:** `dfr.testing.automation.e2e_tests_web.common.page_objects.base_page`
-   **Class:** `BasePage`
    python
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from dfr.testing.automation.config import global_config
    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    class BasePage:
        def __init__(self, driver: WebDriver):
            self.driver = driver
            self.wait = WebDriverWait(self.driver, global_config.DEFAULT_TIMEOUT_SECONDS, 
                                      poll_frequency=global_config.POLL_FREQUENCY_SECONDS)

        def _find_element(self, locator: tuple, timeout: int = None) -> WebElement:
            """Finds a single element using the provided locator."""
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.presence_of_element_located(locator))
                logger.debug(f"Element found: {locator}")
                return element
            except TimeoutException:
                logger.error(f"Element not found within timeout: {locator}")
                raise NoSuchElementException(f"Element not found: {locator}")

        def _find_elements(self, locator: tuple, timeout: int = None) -> list[WebElement]:
            """Finds multiple elements using the provided locator."""
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                elements = _wait.until(EC.presence_of_all_elements_located(locator))
                logger.debug(f"Elements found: {locator} (count: {len(elements)})")
                return elements
            except TimeoutException:
                logger.warning(f"No elements found within timeout for locator: {locator}")
                return [] # Return empty list if no elements found

        def _click(self, locator: tuple, timeout: int = None):
            """Clicks on an element after ensuring it's clickable."""
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.element_to_be_clickable(locator))
                element.click()
                logger.info(f"Clicked element: {locator}")
            except TimeoutException:
                logger.error(f"Element not clickable within timeout: {locator}")
                raise
        
        def _type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
            """Types text into an input field."""
            element = self._wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Typed '{text}' into element: {locator}")

        def _get_text(self, locator: tuple, timeout: int = None) -> str:
            """Gets the text of an element."""
            element = self._wait_for_element_visible(locator, timeout)
            text = element.text
            logger.debug(f"Retrieved text '{text}' from element: {locator}")
            return text

        def _is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
            """Checks if an element is visible on the page."""
            try:
                self._wait_for_element_visible(locator, timeout)
                return True
            except TimeoutException:
                return False
            except NoSuchElementException: # If find_element raises this directly
                return False

        def _wait_for_element_visible(self, locator: tuple, timeout: int = None) -> WebElement:
            """Waits for an element to be visible and returns it."""
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.visibility_of_element_located(locator))
                logger.debug(f"Element is visible: {locator}")
                return element
            except TimeoutException:
                logger.error(f"Element not visible within timeout: {locator}")
                raise

        def get_page_title(self) -> str:
            title = self.driver.title
            logger.info(f"Current page title: {title}")
            return title
            
        def get_current_url(self) -> str:
            url = self.driver.current_url
            logger.info(f"Current page URL: {url}")
            return url

        def scroll_to_element(self, locator: tuple):
            """Scrolls the page to make the element visible."""
            try:
                element = self._find_element(locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                logger.info(f"Scrolled to element: {locator}")
            except Exception as e:
                logger.error(f"Error scrolling to element {locator}: {e}")
                raise
    
-   **Documentation:** Docstrings.

#### 5.3.3 `e2e_tests_web/common/page_objects/admin_portal/farmer_management_page.py`
-   **Purpose:** Page Object for Admin Portal Farmer Management.
-   **Module:** `dfr.testing.automation.e2e_tests_web.common.page_objects.admin_portal.farmer_management_page`
-   **Class:** `FarmerManagementPage(BasePage)`
    python
    from selenium.webdriver.common.by import By
    from dfr.testing.automation.e2e_tests_web.common.page_objects.base_page import BasePage
    # from .admin_login_page import AdminLoginPage # Example if login is prerequisite

    class FarmerManagementPage(BasePage):
        # Locators - these are examples and need to be updated based on actual DFR Admin Portal
        _ADD_FARMER_BUTTON = (By.XPATH, "//button[contains(., 'Create') or contains(., 'New Farmer')]") # Example XPath
        _FARMER_NAME_INPUT_ON_FORM = (By.XPATH, "//input[@name='name' or @name='full_name']") # Example, needs specific attr
        _FARMER_UID_INPUT_ON_FORM = (By.XPATH, "//input[@name='uid']")
        _SAVE_FARMER_BUTTON = (By.XPATH, "//button[@type='submit' and (contains(., 'Save') or @accesskey='s')]")
        _SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search...']")
        _FARMER_LIST_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'o_list_view')]/tbody/tr") # Example for Odoo list view

        def __init__(self, driver):
            super().__init__(driver)
            # Optionally, verify that we are on the correct page
            # assert "Farmer Management" in self.get_page_title() or "/farmers" in self.get_current_url()

        def click_add_farmer_button(self):
            self._click(self._ADD_FARMER_BUTTON)
            # Add wait for form to appear if necessary

        def enter_farmer_name(self, name: str):
            self._type_text(self._FARMER_NAME_INPUT_ON_FORM, name)
        
        def enter_farmer_uid(self, uid: str):
            self._type_text(self._FARMER_UID_INPUT_ON_FORM, uid)

        # Add more methods for other fields: date_of_birth, sex, contact_phone etc.

        def click_save_farmer_button(self):
            self._click(self._SAVE_FARMER_BUTTON)
            # Add wait for save confirmation or navigation if necessary

        def search_farmer(self, search_term: str):
            self._type_text(self._SEARCH_INPUT, search_term + "\n") # Assuming enter triggers search
            # Add wait for search results to load

        def is_farmer_listed(self, farmer_name_or_uid: str, column_index_for_name: int = 1) -> bool:
            """Checks if a farmer is listed in the farmer list table based on name/UID."""
            rows = self._find_elements(self._FARMER_LIST_TABLE_ROWS, timeout=10) # Wait for rows
            for row in rows:
                # This assumes farmer_name_or_uid is in a specific column. Adjust as needed.
                # Odoo list views can be complex to parse reliably without specific IDs/classes on cells.
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) > column_index_for_name:
                         if farmer_name_or_uid in cells[column_index_for_name].text:
                            return True
                except Exception:
                    # Stale element or other issues, continue searching
                    pass
            return False
        
        def get_success_message(self) -> str:
            # Locator for success message (e.g., Odoo's notification)
            # SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'o_notification_manager')]//div[contains(@class, 'o_notification_success')]")
            # return self._get_text(SUCCESS_MESSAGE)
            # This is highly dependent on Odoo's specific notification mechanism
            pass # Placeholder

    
-   **Documentation:** Docstrings. Locators are examples and must be updated.

#### 5.3.4 `e2e_tests_web/admin_portal_tests/test_farmer_creation_admin.py`
-   **Purpose:** E2E test for farmer creation in Admin Portal.
-   **Module:** `dfr.testing.automation.e2e_tests_web.admin_portal_tests.test_farmer_creation_admin`
-   **Content:**
    python
    import pytest
    from dfr.testing.automation.e2e_tests_web.common.web_driver_setup import WebDriverSetup
    from dfr.testing.automation.e2e_tests_web.common.page_objects.admin_portal.farmer_management_page import FarmerManagementPage
    # from dfr.testing.automation.e2e_tests_web.common.page_objects.admin_portal.admin_login_page import AdminLoginPage # If login is separate
    from dfr.testing.automation.config import global_config
    from dfr.testing.automation.utils.test_data_web_loader import WebTestDataLoader # Assume this exists
    from dfr.testing.automation.utils.reporting_utils import capture_screenshot_selenium

    @pytest.mark.web
    @pytest.mark.admin_portal
    @pytest.mark.smoke
    class TestFarmerCreationAdmin:

        @pytest.fixture(scope="function") # function scope to get fresh driver per test
        def selenium_driver(self, request): # request is a built-in pytest fixture
            # driver = WebDriverSetup.get_webdriver(browser_name="chrome", headless=True) # or from config
            # For now, assuming headless chrome. Can be parameterized.
            driver = WebDriverSetup.get_webdriver(browser_name=request.config.getoption("--browser", default="chrome"),
                                                headless=request.config.getoption("--headless", default=True))
            yield driver # provide the fixture value
            
            # Teardown: Capture screenshot on failure
            if request.node.rep_call.failed: # Requires conftest.py hook to set rep_call
                test_name = request.node.name
                capture_screenshot_selenium(driver, f"FAILED_{test_name}")
            WebDriverSetup.quit_webdriver()

        @pytest.fixture(scope="session")
        def test_data_web(self):
            return WebTestDataLoader() # Assume it loads from WEB_TEST_DATA_PATH

        def test_create_new_farmer_successfully(self, selenium_driver, test_data_web):
            # 0. Pre-requisite: Login (if not handled by direct navigation or session fixture)
            # admin_login_page = AdminLoginPage(selenium_driver)
            # admin_login_page.login("admin_user", "admin_pass") # Get credentials securely

            selenium_driver.get(global_config.get_web_admin_url() + "/web#model=dfr.farmer&view_type=list") # Example direct navigation
            
            farmer_page = FarmerManagementPage(selenium_driver)
            farmer_page.click_add_farmer_button()
            
            new_farmer_data = test_data_web.get_farmer_data("valid_new_farmer_admin_portal")
            
            farmer_page.enter_farmer_name(new_farmer_data["fullName"])
            farmer_page.enter_farmer_uid(new_farmer_data["uid"])
            # ... fill other fields ...
            
            farmer_page.click_save_farmer_button()
            
            # Verification
            # Option 1: Check for success message (needs reliable locator)
            # success_msg = farmer_page.get_success_message()
            # assert "Farmer created" in success_msg # Example message

            # Option 2: Verify the farmer appears in the list (more robust)
            # May need to navigate back to list or search
            assert farmer_page.is_farmer_listed(new_farmer_data["fullName"]), \
                f"Farmer '{new_farmer_data['fullName']}' not found in list after creation."
    
-   **Documentation:** Docstrings. Assumes `WebTestDataLoader` and `AdminLoginPage` exist. Also `conftest.py` setup for `--browser`, `--headless` options and failure reporting.

#### 5.3.5 `e2e_tests_web/security_web/test_xss_vulnerabilities.py`
-   **Purpose:** Test for XSS vulnerabilities.
-   **Module:** `dfr.testing.automation.e2e_tests_web.security_web.test_xss_vulnerabilities`
-   **Content:**
    python
    import pytest
    from dfr.testing.automation.e2e_tests_web.common.web_driver_setup import WebDriverSetup
    from dfr.testing.automation.e2e_tests_web.common.page_objects.admin_portal.farmer_management_page import FarmerManagementPage
    from dfr.testing.automation.config import global_config
    from selenium.common.exceptions import UnexpectedAlertPresentException

    @pytest.mark.web
    @pytest.mark.security
    class TestXSSVulnerabilities:

        @pytest.fixture(scope="function")
        def selenium_driver(self, request):
            driver = WebDriverSetup.get_webdriver(browser_name=request.config.getoption("--browser", default="chrome"),
                                                headless=request.config.getoption("--headless", default=True)) # Headless might hide alerts
            yield driver
            WebDriverSetup.quit_webdriver()

        @pytest.mark.parametrize("xss_payload", [
            "<script>alert('XSS_TEST_1')</script>",
            "<img src=x onerror=alert('XSS_TEST_2')>",
            "javascript:alert('XSS_TEST_3')" # For href attributes
        ])
        def test_farmer_name_field_xss_admin_portal(self, selenium_driver, xss_payload):
            selenium_driver.get(global_config.get_web_admin_url() + "/web#model=dfr.farmer&view_type=form") # Navigate to a form view or create new
            
            farmer_page = FarmerManagementPage(selenium_driver) # Assuming this page has relevant input fields
            # This test might need a more generic FormPage object or adapt FarmerManagementPage
            
            # Example: If creating a new farmer
            farmer_page.click_add_farmer_button() # Or navigate to edit an existing one
            
            try:
                farmer_page.enter_farmer_name(xss_payload)
                # Add other required fields with benign data
                farmer_page.enter_farmer_uid("XSS_UID_Test")
                farmer_page.click_save_farmer_button()

                # Verification 1: Check if an alert popped up (crude, might be blocked by browser/WebDriver settings)
                try:
                    alert = selenium_driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()
                    pytest.fail(f"XSS JavaScript alert displayed with text: {alert_text} for payload: {xss_payload}")
                except UnexpectedAlertPresentException as e: # Should not happen if properly handled
                     pytest.fail(f"XSS JavaScript alert was unexpectedly present and auto-dismissed or crashed: {e.msg} for payload: {xss_payload}")
                except Exception: # NoAlertPresentException is expected
                    pass # Good, no alert

                # Verification 2: Check if the payload is sanitized when displayed (more robust)
                # This requires navigating to a view where the entered data is displayed.
                # Example: search for the "XSS_UID_Test" farmer and check how the name is rendered.
                # farmer_page.search_farmer("XSS_UID_Test")
                # displayed_name_html = farmer_page.get_displayed_farmer_name_html("XSS_UID_Test") # Hypothetical method
                # assert "<script>" not in displayed_name_html, f"XSS payload not sanitized for: {xss_payload}"
                # assert "&lt;script&gt;" in displayed_name_html, f"XSS payload not HTML-escaped for: {xss_payload}"

            except UnexpectedAlertPresentException as e: # If alert appears during type/save
                 pytest.fail(f"XSS JavaScript alert displayed unexpectedly during operation: {e.msg} for payload: {xss_payload}")

            # Note: Effective XSS testing is complex. This is a basic check.
            # Proper validation involves checking HTML source or using security scanning tools.
            # For this test, we primarily check if an alert directly executes.
            # A more robust check would be to see if the input is rendered as harmless text on the page after saving/display.
    
-   **Documentation:** Comments on limitations and payload types.

#### 5.3.6 `e2e_tests_web/performance_web/test_page_load_times.py`
-   **Purpose:** Test page load times for web portals.
-   **Module:** `dfr.testing.automation.e2e_tests_web.performance_web.test_page_load_times`
-   **Content:**
    python
    import pytest
    import time
    from dfr.testing.automation.e2e_tests_web.common.web_driver_setup import WebDriverSetup
    from dfr.testing.automation.config import global_config

    MAX_PAGE_LOAD_TIME_S_PORTAL = 3 # As per REQ-FSSP-011
    MAX_PAGE_LOAD_TIME_S_ADMIN = 5 # Example general admin page target, adjust as per B.5 interpretation

    @pytest.mark.web
    @pytest.mark.performance
    class TestPageLoadTimes:

        @pytest.fixture(scope="function")
        def selenium_driver(self, request):
            driver = WebDriverSetup.get_webdriver(browser_name=request.config.getoption("--browser", default="chrome"),
                                                headless=request.config.getoption("--headless", default=True))
            yield driver
            WebDriverSetup.quit_webdriver()

        def measure_page_load(self, driver, url_to_load, expected_element_locator=None):
            start_time = time.perf_counter()
            driver.get(url_to_load)
            
            # Wait for document.readyState to be 'complete'
            WebDriverWait(driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Optionally wait for a specific element to be visible if document.readyState is not enough
            if expected_element_locator:
                WebDriverWait(driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                    EC.visibility_of_element_located(expected_element_locator)
                )
            
            end_time = time.perf_counter()
            return (end_time - start_time)

        def test_farmer_portal_home_page_load_time(self, selenium_driver):
            url = global_config.get_web_portal_url()
            load_time = self.measure_page_load(selenium_driver, url) # Add key element locator if needed
            print(f"Farmer Portal Home Page load time: {load_time:.2f}s")
            assert load_time < MAX_PAGE_LOAD_TIME_S_PORTAL, \
                f"Farmer Portal Home Page load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_PORTAL}s"

        def test_farmer_portal_registration_form_load_time(self, selenium_driver):
            # Assuming a direct URL to the registration form page
            url = global_config.get_web_portal_url() + "/register" # Example URL
            # Add a key element locator for the registration form, e.g. (By.ID, 'registration_form_submit_button')
            load_time = self.measure_page_load(selenium_driver, url) 
            print(f"Farmer Portal Registration Form load time: {load_time:.2f}s")
            assert load_time < MAX_PAGE_LOAD_TIME_S_PORTAL, \
                f"Farmer Portal Registration Form load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_PORTAL}s"

        def test_admin_portal_dashboard_load_time(self, selenium_driver):
            # Assuming login is handled or a direct link to dashboard post-login
            url = global_config.get_web_admin_url() + "/web#menu_id=...&action=..." # Example direct dashboard URL
            # Add key element for dashboard, e.g. (By.CLASS_NAME, 'o_control_panel')
            load_time = self.measure_page_load(selenium_driver, url)
            print(f"Admin Portal Dashboard load time: {load_time:.2f}s")
            assert load_time < MAX_PAGE_LOAD_TIME_S_ADMIN, \
                f"Admin Portal Dashboard load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_ADMIN}s"
    
-   **Documentation:** Comments. Needs specific URLs and potentially locators for key elements to ensure page is fully rendered.

### 5.4 Mobile E2E Testing (`e2e_tests_mobile/`)

#### 5.4.1 `e2e_tests_mobile/common/app_driver_setup.py`
-   **Purpose:** Appium/Flutter Driver lifecycle management.
-   **Module:** `dfr.testing.automation.e2e_tests_mobile.common.app_driver_setup`
-   **Content (Appium Example):**
    python
    from appium import webdriver
    from dfr.testing.automation.utils.logger_setup import setup_logger
    from dfr.testing.automation.config import global_config
    # from dfr.testing.automation.utils.config_loader import ConfigLoader # If loading app_path etc. from INI

    logger = setup_logger(__name__)

    class AppDriverSetup:
        driver = None

        @staticmethod
        def get_appium_driver(platform_name: str = "Android", 
                              device_name: str = "emulator-5554", # Example
                              platform_version: str = "13.0", # Example
                              app_path: str = None, # Path to .apk or .aab
                              app_package: str = "com.example.dfr.mobileapp", # Example
                              app_activity: str = ".MainActivity", # Example
                              extra_caps: dict = None):
            
            if AppDriverSetup.driver:
                logger.warning("Appium driver already initialized. Returning existing instance.")
                return AppDriverSetup.driver

            # env_name = global_config.get_target_environment()
            # env_specific_config = ConfigLoader.load_env_config(env_name)
            # actual_app_path = app_path or env_specific_config.get("MOBILE_ANDROID", "app_path")
            # actual_device_name = device_name or env_specific_config.get("MOBILE_ANDROID", "device_name")
            # actual_platform_version = platform_version or env_specific_config.get("MOBILE_ANDROID", "platform_version")
            
            # For simplicity, using direct parameters or global_config for app_path for now
            actual_app_path = app_path or (global_config.BASE_DIR / "apps/dfr_mobile_app.apk") # Example path
            
            desired_caps = {
                "platformName": platform_name,
                "appium:deviceName": device_name,
                "appium:platformVersion": platform_version,
                "appium:automationName": "UiAutomator2", # For Android
                "appium:app": str(actual_app_path), # Ensure it's a string
                # "appium:appPackage": app_package, # Use if app is already installed
                # "appium:appActivity": app_activity, # Use if app is already installed
                "appium:noReset": False, # Set to True to keep app data between sessions, False for clean state
                "appium:fullReset": False, # Set to True to uninstall and reinstall app
            }
            if extra_caps:
                desired_caps.update(extra_caps)

            logger.info(f"Initializing Appium driver with capabilities: {desired_caps}")
            try:
                AppDriverSetup.driver = webdriver.Remote(global_config.APPIUM_SERVER_URL, desired_caps)
                AppDriverSetup.driver.implicitly_wait(10) # Basic implicit wait for mobile
                logger.info("Appium driver initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Appium driver: {e}")
                raise
            return AppDriverSetup.driver

        @staticmethod
        def quit_appium_driver():
            if AppDriverSetup.driver:
                try:
                    AppDriverSetup.driver.quit()
                    logger.info("Appium driver quit successfully.")
                    AppDriverSetup.driver = None
                except Exception as e:
                    logger.error(f"Error quitting Appium driver: {e}")
    
-   **Documentation:** Docstrings. Capabilities are examples; actual ones depend on the DFR mobile app and test strategy. Flutter Driver setup would be different (likely managed within Dart tests).

#### 5.4.2 `e2e_tests_mobile/common/screen_objects/base_screen.py`
-   **Purpose:** Base class for Mobile Screen Objects.
-   **Module:** `dfr.testing.automation.e2e_tests_mobile.common.screen_objects.base_screen`
-   **Class:** `BaseScreen`
    python
    from appium.webdriver.webdriver import WebDriver
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from dfr.testing.automation.config import global_config
    from dfr.testing.automation.utils.logger_setup import setup_logger

    logger = setup_logger(__name__)

    class BaseScreen:
        def __init__(self, driver: WebDriver):
            self.driver = driver
            self.wait = WebDriverWait(self.driver, global_config.DEFAULT_TIMEOUT_SECONDS,
                                      poll_frequency=global_config.POLL_FREQUENCY_SECONDS)

        def _find_element(self, locator_type: AppiumBy, value: str, timeout: int = None):
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.presence_of_element_located((locator_type, value)))
                logger.debug(f"Element found: {locator_type} = {value}")
                return element
            except TimeoutException:
                logger.error(f"Element not found within timeout: {locator_type} = {value}")
                raise NoSuchElementException(f"Element not found: {locator_type} = {value}")
        
        def _find_elements(self, locator_type: AppiumBy, value: str, timeout: int = None):
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                elements = _wait.until(EC.presence_of_all_elements_located((locator_type, value)))
                logger.debug(f"Elements found: {locator_type} = {value} (count: {len(elements)})")
                return elements
            except TimeoutException:
                logger.warning(f"No elements found for: {locator_type} = {value}")
                return []

        def _tap(self, locator_type: AppiumBy, value: str, timeout: int = None):
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.element_to_be_clickable((locator_type, value)))
                element.click() # Appium's click often serves as tap
                logger.info(f"Tapped element: {locator_type} = {value}")
            except TimeoutException:
                logger.error(f"Element not tappable within timeout: {locator_type} = {value}")
                raise

        def _type_text(self, locator_type: AppiumBy, value: str, text: str, clear_first: bool = True, timeout: int = None):
            element = self._wait_for_element_visible(locator_type, value, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Typed '{text}' into element: {locator_type} = {value}")

        def _get_text(self, locator_type: AppiumBy, value: str, timeout: int = None) -> str:
            element = self._wait_for_element_visible(locator_type, value, timeout)
            text = element.text
            logger.debug(f"Retrieved text '{text}' from element: {locator_type} = {value}")
            return text

        def _is_element_visible(self, locator_type: AppiumBy, value: str, timeout: int = 5) -> bool:
            try:
                self._wait_for_element_visible(locator_type, value, timeout)
                return True
            except TimeoutException:
                return False
            except NoSuchElementException:
                return False
        
        def _wait_for_element_visible(self, locator_type: AppiumBy, value: str, timeout: int = None):
            _wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            try:
                element = _wait.until(EC.visibility_of_element_located((locator_type, value)))
                logger.debug(f"Element is visible: {locator_type} = {value}")
                return element
            except TimeoutException:
                logger.error(f"Element not visible within timeout: {locator_type} = {value}")
                raise
        
        def hide_keyboard(self):
            try:
                if self.driver.is_keyboard_shown():
                    self.driver.hide_keyboard()
                    logger.info("Keyboard hidden.")
            except Exception as e: # Catch broad exception as is_keyboard_shown might not be supported or fail
                logger.warning(f"Could not hide keyboard or check if shown: {e}")
    
-   **Documentation:** Docstrings. Uses `AppiumBy` for locators.

#### 5.4.3 `e2e_tests_mobile/android/test_android_farmer_registration_offline.py`
-   **Purpose:** E2E test for offline farmer registration (Android).
-   **Module:** `dfr.testing.automation.e2e_tests_mobile.android.test_android_farmer_registration_offline`
-   **Content (Illustrative, assuming Screen Objects like `RegistrationScreen` exist):**
    python
    import pytest
    from dfr.testing.automation.e2e_tests_mobile.common.app_driver_setup import AppDriverSetup
    # from dfr.testing.automation.e2e_tests_mobile.common.screen_objects.android.registration_screen import RegistrationScreen # Example
    # from dfr.testing.automation.e2e_tests_mobile.common.screen_objects.android.main_dashboard_screen import MainDashboardScreen # Example
    from dfr.testing.automation.utils.test_data_mobile_loader import MobileTestDataLoader # Assume this exists
    from dfr.testing.automation.utils.reporting_utils import capture_screenshot_appium
    from appium.webdriver.connectiontype import ConnectionType

    @pytest.mark.mobile_android
    @pytest.mark.offline_sync # Custom marker for offline related tests
    class TestAndroidFarmerRegistrationOffline:

        @pytest.fixture(scope="function")
        def appium_android_driver(self, request): # request is pytest built-in
            # Capabilities can be loaded from config based on --env or other params
            driver = AppDriverSetup.get_appium_driver(
                platform_name="Android",
                # device_name, platform_version, app_path should come from config or command line
            )
            yield driver
            if request.node.rep_call.failed:
                test_name = request.node.name
                capture_screenshot_appium(driver, f"FAILED_{test_name}")
            AppDriverSetup.quit_appium_driver()

        @pytest.fixture(scope="session")
        def test_data_mobile(self):
            return MobileTestDataLoader()

        def test_register_farmer_offline_and_verify_local_storage(self, appium_android_driver, test_data_mobile):
            driver = appium_android_driver
            
            # 1. Ensure app is in offline mode
            driver.set_network_connection(ConnectionType.AIRPLANE_MODE)
            assert driver.network_connection == ConnectionType.AIRPLANE_MODE, "Failed to set airplane mode."
            
            # 2. Navigate to registration screen (using Screen Objects)
            # main_dashboard = MainDashboardScreen(driver)
            # main_dashboard.navigate_to_farmer_registration()
            # registration_screen = RegistrationScreen(driver)

            # 3. Fill registration form with test data
            farmer_data = test_data_mobile.get_farmer_data("new_offline_farmer")
            # registration_screen.enter_full_name(farmer_data["fullName"])
            # registration_screen.enter_contact_phone(farmer_data["contactPhone"])
            # ... fill other fields ...
            # registration_screen.tap_save_button()

            # 4. Verify success message or navigation on app UI
            # assert registration_screen.is_success_message_displayed(), "Offline registration success message not shown."
            
            # 5. Verify data is stored locally (This is the tricky part for UI tests)
            # Option A: If app has a "pending sync" list UI, verify the record appears there.
            # pending_sync_screen = registration_screen.navigate_to_pending_sync() # Hypothetical
            # assert pending_sync_screen.is_farmer_in_pending_list(farmer_data["contactPhone"]), "Farmer not in pending sync list."

            # Option B: Use ADB or test hooks in the app (if dev adds them) to query local SQLite.
            # This is generally outside pure black-box UI testing scope unless facilitated.
            # For A.4 (security of offline storage), one might try to access the DB file via ADB
            # and check if it's encrypted, but not its content verification through UI tests.

            # 6. Restore network for subsequent tests / teardown if needed
            # driver.set_network_connection(ConnectionType.ALL_NETWORK_ON)
            # For this specific test, we might leave it offline to prove the point.
            
            pytest.skip("Offline farmer registration test needs specific Screen Objects and verification strategy for local storage.")
    
-   **Documentation:** Comments. Requires specific Android Screen Objects and a strategy for verifying local storage.

#### 5.4.4 `e2e_tests_mobile/performance_mobile/test_app_startup_time.py`
-   **Purpose:** Test mobile app startup time.
-   **Module:** `dfr.testing.automation.e2e_tests_mobile.performance_mobile.test_app_startup_time`
-   **Content:**
    python
    import pytest
    import time
    from dfr.testing.automation.e2e_tests_mobile.common.app_driver_setup import AppDriverSetup
    # from dfr.testing.automation.e2e_tests_mobile.common.screen_objects.android.main_dashboard_screen import MainDashboardScreen # Example
    from appium.webdriver.common.appiumby import AppiumBy

    MAX_APP_STARTUP_TIME_S = 5 # As per B.5 (example, adjust based on SRS interpretation)

    @pytest.mark.mobile_android # Or common mobile marker
    @pytest.mark.performance
    class TestAppStartupTime:

        # Fixture to get driver factory for multiple launches if needed, or just use one launch
        @pytest.fixture(scope="function")
        def appium_android_driver_perf(self, request):
            # For startup, we want a clean launch. fullReset might be true in caps.
            # Ensure capabilities are set for a cold start.
            caps = {"appium:noReset": False, "appium:fullReset": True} # Example for cold start
            driver = AppDriverSetup.get_appium_driver(
                platform_name="Android", 
                # Other caps from config...
                extra_caps=caps
            )
            yield driver
            AppDriverSetup.quit_appium_driver()


        def test_mobile_app_cold_start_performance(self, appium_android_driver_perf):
            driver = appium_android_driver_perf
            
            # Appium's launch_app() or driver initialization itself starts the timing.
            # The time is measured from when driver.init is called to when the app is ready.
            # Appium might provide launch time in capabilities or logs.
            # For a more controlled test:
            
            # 1. Ensure app is closed (fullReset in caps helps)
            # 2. Record time before launch
            # 3. Launch app (driver init does this)
            # 4. Wait for a known element on the first screen to appear
            # 5. Record time after element appears
            
            # This test assumes the `get_appium_driver` itself is the launch trigger.
            # We need to measure from before that call to when a specific element appears.
            # This fixture structure might need adjustment for precise start time capture.
            
            # Let's refine:
            # The fixture `appium_android_driver_perf` already launches the app.
            # We need to time how long it takes for a key element to be visible *after* launch.
            # Appium's `get_session()` returns capabilities which might include app startup time metrics.
            
            # Simplified approach: measure from end of driver init to first screen element.
            start_wait_time = time.perf_counter()
            
            # Wait for a known element on the initial screen, e.g., login button or dashboard title
            # This locator needs to be specific to the DFR app's first interactive screen
            # main_dashboard = MainDashboardScreen(driver)
            # main_dashboard.wait_for_dashboard_to_load() # Hypothetical method in ScreenObject
            
            # Example direct wait for an element (replace with actual locator)
            try:
                WebDriverWait(driver, MAX_APP_STARTUP_TIME_S + 5).until( # Give a bit more time for wait itself
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "welcome_message_or_key_element"))
                )
            except TimeoutException:
                pytest.fail(f"App failed to load initial screen within {MAX_APP_STARTUP_TIME_S + 5}s.")

            end_wait_time = time.perf_counter()
            
            # This measures time AFTER driver is initialized and app is launched.
            # True cold start time is harder to measure precisely this way without instrumenting the app
            # or using OS-level tools. Appium logs might contain `appLaunchDuration`.
            
            app_became_interactive_time = (end_wait_time - start_wait_time)
            
            # Check Appium logs for `appLaunchDuration` if available and more accurate
            # session_details = driver.session
            # app_launch_duration_ms = session_details.get('appLaunchDuration') # This is often Android specific

            # For now, using the element visibility as a proxy
            print(f"App first screen element visible time: {app_became_interactive_time:.2f}s (Target: < {MAX_APP_STARTUP_TIME_S}s for full start)")
            
            # This is a pragmatic check. True cold start needs more specialized measurement.
            # The B.5 criteria might refer to this perceived startup time by user.
            assert app_became_interactive_time < MAX_APP_STARTUP_TIME_S, \
                f"App perceived startup time {app_became_interactive_time:.2f}s exceeds target {MAX_APP_STARTUP_TIME_S}s"
                
            pytest.skip("Precise cold start time measurement might need Appium log parsing or app instrumentation. This test checks time to first interactive element.")

    
-   **Documentation:** Comments on measurement challenges.

#### 5.4.5 `e2e_tests_mobile/flutter_tests/test/farmer_registration_test.dart`
-   **Purpose:** Flutter Driver test for farmer registration.
-   **Framework:** Flutter Driver (Dart)
-   **Content (Illustrative):**
    dart
    // In e2e_tests_mobile/flutter_tests/test/farmer_registration_test.dart
    import 'package:flutter_driver/flutter_driver.dart';
    import 'package:test/test.dart';

    void main() {
      group('DFR Farmer Registration (Flutter App)', () {
        FlutterDriver? driver;

        setUpAll(() async {
          driver = await FlutterDriver.connect();
        });

        tearDownAll(() async {
          driver?.close();
        });

        test('should register a new farmer successfully in offline mode', () async {
          // Ensure offline mode (this needs a mechanism in the app controllable by tests, or manual setup)
          // await driver.requestData('set_offline_mode'); // Hypothetical

          // Finders for widgets (use ValueKey in your Flutter app for testability)
          final fullNameField = find.byValueKey('farmer_registration_fullName');
          final contactPhoneField = find.byValueKey('farmer_registration_contactPhone');
          final saveButton = find.byValueKey('farmer_registration_saveButton');
          // ... other finders

          // Navigate to registration screen if not already there
          // await driver.tap(find.byValueKey('goto_registration_button'));

          await driver!.tap(fullNameField);
          await driver!.enterText('Flutter Test Farmer');
          
          await driver!.tap(contactPhoneField);
          await driver!.enterText('1234567890');
          
          // ... fill other fields

          await driver!.tap(saveButton);

          // Verify success (e.g., navigation to another screen, success message displayed)
          // final successMessage = find.byValueKey('registration_success_message');
          // await driver.waitFor(successMessage);
          // expect(await driver.getText(successMessage), 'Farmer registered successfully!');
          
          // Verification of local storage is complex with Flutter Driver alone.
          // Might need to check UI for pending sync items or use test hooks.
        }, timeout: Timeout(Duration(minutes: 2))); // Adjust timeout
      });
    }
    
-   **Documentation:** Comments. Assumes `ValueKey`s are used in the Flutter app.

#### 5.4.6 `e2e_tests_mobile/flutter_tests/pubspec.yaml`
-   **Purpose:** Flutter test dependencies.
-   **Content:**
    yaml
    name: dfr_flutter_e2e_tests
    description: E2E tests for DFR Flutter mobile application.
    publish_to: 'none' # Prevent accidental publishing

    environment:
      sdk: '>=3.0.0 <4.0.0' # Match DFR_MOBILE_APP's Flutter SDK constraint
      flutter: ">=3.22.0"   # Match DFR_MOBILE_APP's Flutter version

    dev_dependencies:
      flutter_driver:
        sdk: flutter
      test: any # Standard Dart test package
      # Add other dev dependencies if needed, e.g., integration_test for combined tests

    # flutter_test dependency is usually for widget tests, not driver tests directly here
    # but often included in a flutter project by default.
    #  flutter_test:
    #    sdk: flutter
    
-   **Documentation:** Standard YAML comments if needed.

### 5.5 Odoo Integration Testing (`integration_tests_odoo/`)

#### 5.5.1 `integration_tests_odoo/common/odoo_test_helper.py`
-   **Purpose:** Utilities for Odoo integration tests.
-   **Module:** `dfr.testing.automation.integration_tests_odoo.common.odoo_test_helper`
-   **Content:**
    python
    # This helper assumes it's run within an Odoo test environment,
    # or has a way to connect to a running Odoo instance with test DB.
    # For true Odoo integration tests, you typically inherit from Odoo's test classes.
    # If running PyTest against a live Odoo instance:
    import odoorpc # Example library to connect to Odoo RPC if not using Odoo's own test runner
    from dfr.testing.automation.utils.logger_setup import setup_logger
    # from dfr.testing.automation.utils.config_loader import ConfigLoader # For DB details

    logger = setup_logger(__name__)

    class OdooTestHelper:
        def __init__(self, odoo_env=None): # odoo_env can be from Odoo's test runner or odoorpc
            self.env = odoo_env
            if not self.env:
                self._connect_odoo_rpc() # Example connection

        def _connect_odoo_rpc(self):
            # Load DB config (host, port, db_name, user, password)
            # target_env = global_config.get_target_environment()
            # db_config = ConfigLoader.load_env_config(target_env).get_section("ODOO_INTEGRATION_DB")
            # self.odoo = odoorpc.ODOO(db_config['host'], port=db_config.getint('port'))
            # self.odoo.login(db_config['name'], db_config['user'], os.getenv(db_config['password_secret_ref']))
            # self.env = self.odoo.env
            logger.warning("Odoo RPC connection for integration tests is illustrative. "
                           "Prefer Odoo's native test framework for deeper integration.")
            pass # Placeholder

        def create_test_farmer(self, name: str, uid: str, **kwargs):
            """Creates a test farmer record directly via ORM."""
            if not self.env:
                logger.error("Odoo environment not available for create_test_farmer.")
                return None
            
            farmer_model = self.env['dfr.farmer'] # Replace with actual model name
            vals = {'name': name, 'uid': uid, **kwargs}
            try:
                farmer = farmer_model.create(vals)
                logger.info(f"Created test farmer: {name} (ID: {farmer.id}, UID: {uid})")
                # self.env.cr.commit() # Important if not in Odoo's test transaction
                return farmer
            except Exception as e:
                logger.error(f"Failed to create test farmer {name}: {e}")
                # self.env.cr.rollback()
                raise

        def get_farmer_by_uid(self, uid: str):
            if not self.env: return None
            farmer_model = self.env['dfr.farmer']
            return farmer_model.search([('uid', '=', uid)], limit=1)

        def get_service(self, service_name: str):
            """Hypothetical: Accesses a custom Odoo service if applicable."""
            # This is highly dependent on how services are exposed in DFR Odoo modules.
            # Example: return self.env['ir.service']._get(service_name)
            logger.warning(f"get_service for '{service_name}' is a placeholder.")
            return None

        # Add more helpers: create_household, create_plot, create_dynamic_form_def, etc.
    
-   **Documentation:** Docstrings. Emphasizes using Odoo's native test framework where possible.

#### 5.5.2 `integration_tests_odoo/farmer_registry_integration/test_deduplication_logic.py`
-   **Purpose:** Integration test for farmer de-duplication.
-   **Module:** `dfr.testing.automation.integration_tests_odoo.farmer_registry_integration.test_deduplication_logic`
-   **Content (Requires Odoo Test Environment or RPC setup):**
    python
    import pytest
    # If using Odoo's test framework:
    # from odoo.tests.common import TransactionCase 
    # class TestDeduplicationLogic(TransactionCase): # Example
    #    def setUp(self, *args, **kwargs):
    #        super().setUp(*args, **kwargs)
    #        self.Farmer = self.env['dfr.farmer'] 
    #
    #    def test_create_duplicate_farmer_by_national_id(self):
    #        self.Farmer.create({'name': 'John Doe', 'uid': 'UID001', 'national_id_number': '12345'})
    #        with self.assertRaises(odoo.exceptions.ValidationError): # Or specific integrity error
    #            self.Farmer.create({'name': 'Jane Doe', 'uid': 'UID002', 'national_id_number': '12345'})
    
    # If using PyTest with an external Odoo instance via odoorpc or similar:
    from dfr.testing.automation.integration_tests_odoo.common.odoo_test_helper import OdooTestHelper
    
    @pytest.mark.integration
    @pytest.mark.odoo # Custom marker for Odoo specific integration
    class TestDeduplicationOdoo:

        @pytest.fixture(scope="class") # Or function if state needs reset
        def odoo_helper(self): # This fixture needs to provide a connected Odoo env
            # This setup is complex if not using Odoo's test runner.
            # It would involve setting up a test database or connecting to one.
            # For this SDS, we assume odoo_helper can provide `self.env`
            # helper = OdooTestHelper() # This would connect via RPC
            # if not helper.env:
            #     pytest.skip("Odoo environment not available for integration tests.")
            # return helper
            pytest.skip("Odoo integration test setup (external to Odoo runner) is complex and placeholder.")
            return None # Placeholder

        def test_create_duplicate_farmer_by_national_id(self, odoo_helper):
            # Assumes a clean state or rollback mechanism for each test
            farmer_model = odoo_helper.env['dfr.farmer'] # Replace with actual model name
            
            # Create first farmer
            farmer1_data = {'name': 'Unique Farmer A', 'uid': 'UID_DUP_A001', 'national_id_number': 'NATID_001_DUP', 'national_id_type': 'PASSPORT'}
            farmer1 = farmer_model.create(farmer1_data)
            assert farmer1, "Failed to create initial farmer for de-duplication test."
            # odoo_helper.env.cr.commit() # If not auto-committed

            # Attempt to create duplicate
            farmer2_data = {'name': 'Unique Farmer B', 'uid': 'UID_DUP_A002', 'national_id_number': 'NATID_001_DUP', 'national_id_type': 'PASSPORT'}
            
            # The DFR system should prevent this or flag it based on REQ-FHR-012 (real-time)
            # or REQ-FHR-013 (post-sync, harder to test in pure integration without simulating sync)
            # For Odoo model constraints (_sql_constraints or @api.constrains):
            with pytest.raises(Exception) as excinfo: # Catch Odoo's UserError, ValidationError, or IntegrityError
                farmer_model.create(farmer2_data)
            
            assert "duplicate key value violates unique constraint" in str(excinfo.value).lower() \
                or "already exists with this National ID" in str(excinfo.value), \
                f"Expected duplicate error not raised or message mismatch: {str(excinfo.value)}"

            # Clean up created records or rely on test transaction rollback
            # farmer1.unlink()
            # odoo_helper.env.cr.commit()

        def test_fuzzy_match_deduplication_flagging(self, odoo_helper):
            # This tests if potential duplicates are flagged (REQ-FHR-014)
            # It assumes a status or flag field (e.g., 'potential_duplicate_of') exists
            farmer_model = odoo_helper.env['dfr.farmer']

            farmer1_data = {'name': 'Johnathan Smythe', 'uid': 'UID_FUZZY_A001', 'village': 'Springfield'}
            farmer1 = farmer_model.create(farmer1_data)
            # odoo_helper.env.cr.commit()

            # Create a slightly different farmer that should trigger fuzzy match
            farmer2_data = {'name': 'Jonathan Smith', 'uid': 'UID_FUZZY_A002', 'village': 'Springfield'}
            farmer2 = farmer_model.create(farmer2_data) # This might trigger a background job or on_change to flag
            # odoo_helper.env.cr.commit()
            # farmer2.refresh() # To get updated values if a server action modified it

            # Verification depends on how fuzzy matching flags records:
            # Option 1: A field on farmer2 points to farmer1
            # assert farmer2.potential_duplicate_of.id == farmer1.id, "Fuzzy duplicate not linked."
            # Option 2: A separate model tracks potential duplicates
            # duplicate_pair_model = odoo_helper.env['dfr.duplicate.pair']
            # pair = duplicate_pair_model.search([('farmer1_id', '=', farmer1.id), ('farmer2_id', '=', farmer2.id)])
            # assert pair, "Fuzzy duplicate pair not created."
            pytest.skip("Fuzzy match flagging verification needs specific model design details for dfr.farmer")

    
-   **Documentation:** Comments. Emphasizes dependency on Odoo test environment setup.

### 5.6 Test Data (`test_data/`)

#### 5.6.1 `test_data/api/valid_farmer_data.json`
-   **Purpose:** Valid test data for API farmer creation.
-   **Format:** JSON
-   **Structure:**
    json
    {
      "valid_default_farmer": {
        "fullName": "Api Test Farmer",
        "dateOfBirth": "1985-07-15",
        "sex": "Male",
        "contactPhone": "+11234567890",
        "nationalIdType": "NATIONAL_ID",
        "nationalIdNumber": "API-TEST-12345",
        "householdUid": "HH-API-001", // If relevant for creation endpoint
        "village": "API Testville",
        "customFields": { // If dynamic form data can be sent during creation
            "primary_crop": "Maize",
            "farm_size_hectares": 10.5
        }
      },
      "minimal_valid_farmer": {
        "fullName": "Api Min Farmer",
        "contactPhone": "+10987654321"
        // Other fields optional or defaulted by API
      }
      // ... other scenarios
    }
    
-   **Documentation:** This file will be used by `ApiTestDataLoader`. Path: `test_data/api/farmer_creation_data.json` (as used in loader).
    Other files like `farmer_lookup_data.json` and `farmer_lookup_perf_data.json` will follow similar structures.

#### 5.6.2 Web and Mobile Test Data
-   Similar JSON or YAML files will be created under `test_data/web/` and `test_data/mobile/` for web and mobile E2E tests respectively, loaded by their respective data loader utilities (e.g., `WebTestDataLoader`, `MobileTestDataLoader` - to be created similar to `ApiTestDataLoader`).

### 5.7 Test Runners (`runners/`)

#### 5.7.1 `runners/run_api_tests.sh`
-   **Purpose:** Execute API tests.
-   **Language:** Shell Script (Bash)
-   **Content:**
    bash
    #!/bin/bash
    # Script to run DFR API tests

    # Default environment, can be overridden by command line arg
    TARGET_ENV=${1:-dev} # dev or staging
    MARKERS=${2} # Optional: pytest markers like "smoke" or "regression and not performance"

    echo "Running DFR API Tests for Environment: $TARGET_ENV"
    if [ -n "$MARKERS" ]; then
        echo "Applying Markers: $MARKERS"
    fi

    # Activate virtual environment if used
    # source /path/to/venv/bin/activate

    # Set environment variable for config loading
    export DFR_TARGET_ENV=$TARGET_ENV

    PYTEST_ARGS="-v" # Verbose output
    if [ -n "$MARKERS" ]; then
        PYTEST_ARGS="$PYTEST_ARGS -m \"$MARKERS\""
    fi

    # Path to the root of the test suite
    TEST_SUITE_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
    cd "$TEST_SUITE_ROOT_DIR"

    # Ensure reports directory exists
    mkdir -p reports

    # Run PyTest for API tests
    # The pytest.ini should already specify testpaths and html report location
    eval pytest api_tests $PYTEST_ARGS

    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "API tests completed successfully for $TARGET_ENV."
    else
        echo "API tests failed for $TARGET_ENV. Exit code: $EXIT_CODE"
    fi

    # Deactivate virtual environment if used
    # deactivate
    exit $EXIT_CODE
    
-   **Documentation:** Comments in script.

#### 5.7.2 `runners/run_all_tests.sh`
-   **Purpose:** Master script to execute all test suites.
-   **Language:** Shell Script (Bash)
-   **Content:**
    bash
    #!/bin/bash
    # Master script to run all DFR automated test suites

    TARGET_ENV=${1:-dev}
    MARKERS_API=${2}
    MARKERS_WEB=${3}
    MARKERS_MOBILE=${4}
    MARKERS_INTEGRATION=${5}

    echo "Starting DFR Full Test Suite for Environment: $TARGET_ENV"
    TEST_SUITE_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
    cd "$TEST_SUITE_ROOT_DIR"

    # Activate virtual environment if used
    # source /path/to/venv/bin/activate
    export DFR_TARGET_ENV=$TARGET_ENV

    # Ensure reports directory exists
    mkdir -p reports
    
    OVERALL_EXIT_CODE=0

    echo "----------------------------------------"
    echo "Running API Tests..."
    echo "----------------------------------------"
    ./runners/run_api_tests.sh "$TARGET_ENV" "$MARKERS_API"
    if [ $? -ne 0 ]; then OVERALL_EXIT_CODE=1; fi

    # echo "----------------------------------------"
    # echo "Running Web E2E Tests..."
    # echo "----------------------------------------"
    # ./runners/run_web_e2e_tests.sh "$TARGET_ENV" "$MARKERS_WEB" # Assuming this script exists
    # if [ $? -ne 0 ]; then OVERALL_EXIT_CODE=1; fi
    
    # echo "----------------------------------------"
    # echo "Running Mobile E2E Tests (Android - Appium/Python)..."
    # echo "----------------------------------------"
    # # Ensure Appium server is running for these
    # ./runners/run_mobile_android_appium_tests.sh "$TARGET_ENV" "$MARKERS_MOBILE" # Assuming this script exists
    # if [ $? -ne 0 ]; then OVERALL_EXIT_CODE=1; fi

    # echo "----------------------------------------"
    # echo "Running Mobile E2E Tests (Flutter Driver)..."
    # echo "----------------------------------------"
    # ./runners/run_mobile_flutter_driver_tests.sh "$TARGET_ENV" "$MARKERS_MOBILE" # Assuming this script exists
    # if [ $? -ne 0 ]; then OVERALL_EXIT_CODE=1; fi
    
    # echo "----------------------------------------"
    # echo "Running Odoo Integration Tests..."
    # echo "----------------------------------------"
    # ./runners/run_odoo_integration_tests.sh "$TARGET_ENV" "$MARKERS_INTEGRATION" # Assuming this script exists
    # if [ $? -ne 0 ]; then OVERALL_EXIT_CODE=1; fi

    echo "----------------------------------------"
    if [ $OVERALL_EXIT_CODE -eq 0 ]; then
        echo "All test suites completed successfully for $TARGET_ENV."
    else
        echo "One or more test suites failed for $TARGET_ENV. Overall Exit code: $OVERALL_EXIT_CODE"
    fi
    echo "----------------------------------------"

    # Deactivate virtual environment if used
    # deactivate
    exit $OVERALL_EXIT_CODE
    
-   **Documentation:** Comments. Assumes individual runner scripts for web, mobile, and integration tests exist.

## 6. Data Model (for Test Data)
-   Test data will primarily be stored in JSON files (as shown in 5.6.1).
-   Structure will typically be a main JSON object, with keys representing different test scenarios or data sets.
-   Each scenario/data set will contain the necessary key-value pairs to populate request payloads (for API tests) or form fields (for UI tests).
-   Sensitive data (like passwords) in test data files should be placeholders, with actual values injected at runtime from secure sources (environment variables, secrets manager).

## 7. Deployment Considerations (for Test Suite)
-   The test suite is designed to be run from a machine that has network access to the target DFR environment (Dev, Staging).
-   For mobile tests, an Appium server must be running and accessible, with test devices/emulators connected.
-   For Flutter Driver tests, a running instance of the DFR Flutter app (in debug/profile mode) is required, accessible via its VM Service URL.
-   Dependencies (`requirements.txt`, Flutter SDK for Flutter tests) must be installed in the execution environment.
-   CI/CD pipelines will clone this repository, install dependencies, and execute the runner scripts.

## 8. Security Testing Strategy
-   **API Security (REQ-A.4):**
    -   Test authentication mechanisms: token handling (expiry, tampering), access control with different roles. (e.g., `test_auth_vulnerabilities.py`)
    -   Input validation tests: attempt common injection patterns (SQLi might be mitigated by ORM, but test for other types like NoSQL injection if applicable, parameter tampering).
    -   Test for insecure direct object references (IDOR) by trying to access data belonging to other users/tenants with valid tokens but insufficient privilege.
-   **Web E2E Security (REQ-A.4):**
    -   Test for Cross-Site Scripting (XSS) in input fields. (e.g., `test_xss_vulnerabilities.py`)
    -   Test for weak session management (e.g., session fixation, if applicable).
    -   Check for proper implementation of security headers (CSP, HSTS, X-Frame-Options) via browser developer tools during E2E tests (can be automated partially).
-   **Mobile App Security (REQ-A.4):**
    -   Verify encryption of offline data (REQ-SADG-004). This might involve manual inspection of app's data directory on a rooted device/emulator during test setup, or specific test hooks.
    -   Test secure communication (TLS/SSL pinning if implemented in the app).
    -   Test for insecure data storage beyond the encrypted DB (e.g., logs, temporary files).
    -   Analyze network traffic during E2E tests for sensitive data leaks.
-   **General:**
    -   Dependency vulnerability scanning (tools like Snyk, Trivy, GitHub Dependabot) should be part of the CI/CD pipeline, although test suite itself doesn't execute these scans on DFR directly, it maintains its own dependencies.

## 9. Performance Testing Strategy
-   **API Performance (REQ-B.5, REQ-API-009):**
    -   Use PyTest with custom timing or `pytest-benchmark` for individual endpoint response times. (e.g., `test_api_load_farmer_lookup.py`)
    -   For more complex load scenarios (concurrent users, ramp-up), consider integrating tools like Locust or k6, where PyTest can orchestrate or trigger these external load tests. For this SDS, we'll focus on what PyTest can achieve directly or with simple extensions.
    -   Measure P95 response times under defined load conditions.
-   **Web E2E Performance (REQ-B.5, REQ-FSSP-011):**
    -   Measure page load times for critical Admin and Farmer Portal pages using Selenium's navigation timing or JavaScript `performance.timing` API. (e.g., `test_page_load_times.py`)
    -   Test under simulated concurrent user load (can be approximated by running multiple browser instances via Selenium Grid or `pytest-xdist`, though true load testing often needs dedicated tools).
-   **Mobile App Performance (REQ-B.5):**
    -   Measure app startup time (cold start). (e.g., `test_app_startup_time.py`)
    -   Measure screen transition times.
    -   Measure response time for key user interactions (e.g., saving a form offline).
    -   Appium and platform-specific profiling tools (Android Profiler, Flutter DevTools) can aid in identifying bottlenecks, though direct automation of these profilers in PyTest is complex. Test scripts will focus on end-user perceived performance.
-   **REQ-PCA-013 Test Validation:** This test suite itself is a form of validation for CI/CD pipeline readiness, providing automated checks that can be integrated.

## 10. Traceability
-   **REQ-PCA-013 (CI/CD standards):** Addressed by test runners, PyTest configuration for reporting, and overall structure allowing automated execution.
-   **A.4 (Security Best Practices):** Addressed by dedicated security test files (`test_auth_vulnerabilities.py`, `test_xss_vulnerabilities.py`) and considerations in mobile offline storage tests.
-   **B.5 (Performance and Load Testing):** Addressed by dedicated performance test files for API, Web, and Mobile (`test_api_load_farmer_lookup.py`, `test_page_load_times.py`, `test_app_startup_time.py`).

This SDS provides a detailed blueprint for developing the DFR Test Automation Suite. Further refinement of locators, test data, and specific test scenarios will occur during the implementation phase.
