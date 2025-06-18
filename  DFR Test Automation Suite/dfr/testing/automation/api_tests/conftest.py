```python
import pytest
import os
from dfr.testing.automation.api_tests.common.api_client import ApiClient
from dfr.testing.automation.api_tests.common.auth_handler import AuthHandler
from dfr.testing.automation.api_tests.common.test_data_loader import ApiTestDataLoader
from dfr.testing.automation.utils.config_loader import ConfigLoader
from dfr.testing.automation.utils.logger_setup import setup_logger
# from dfr.testing.automation.config import global_config # Not directly used here, but ConfigLoader might use it

logger = setup_logger(__name__)

# Add command-line options for pytest (e.g., --env)
# This allows specifying the target environment from the command line.
def pytest_addoption(parser):
    """Adds custom command-line options to PyTest."""
    parser.addoption(
        "--env", action="store", default="dev", help="Specify environment: dev or staging"
    )
    # Add other options if needed, e.g., --baseurl-api to override API URL directly

@pytest.fixture(scope="session")
def env_config(request):
    """
    Loads and provides the environment-specific configuration (e.g., from INI files).
    The target environment is determined by the '--env' command-line option.
    """
    target_env = request.config.getoption("--env")
    logger.info(f"Loading configuration for target environment: {target_env}")
    try:
        config = ConfigLoader.load_env_config(target_env)
        return config
    except FileNotFoundError:
        pytest.fail(f"Environment config file for '{target_env}' not found. Ensure config/{target_env}_env_config.ini exists.")
    except Exception as e:
        pytest.fail(f"Error loading environment config for '{target_env}': {e}")

@pytest.fixture(scope="session")
def api_base_url(env_config):
    """Provides the base URL for API tests from the loaded environment configuration."""
    try:
        return ConfigLoader.get_option(env_config, "API", "base_url")
    except KeyError:
        pytest.fail("API 'base_url' not configured in the environment INI file for section [API].")

@pytest.fixture(scope="session")
def admin_auth_handler(env_config, api_base_url): # api_base_url needed if auth_url is relative
    """
    Provides an AuthHandler instance for admin-level API access.
    Uses client credentials specified in the environment configuration.
    Secrets are expected to be in environment variables referenced by the INI file.
    """
    try:
        client_id = ConfigLoader.get_option(env_config, "API", "admin_client_id")
        client_secret_ref = ConfigLoader.get_option(env_config, "API", "admin_client_secret_ref")
        auth_endpoint = ConfigLoader.get_option(env_config, "API", "token_endpoint", fallback="/oauth/token")
    except KeyError as e:
        pytest.skip(f"Admin API authentication details (client_id, client_secret_ref, or token_endpoint) missing in config: {e}")
        return None

    client_secret = ConfigLoader.get_env_credential(env_config, "API", client_secret_ref)
    if not client_secret:
        pytest.skip(f"Admin client secret environment variable '{client_secret_ref}' not set or empty.")
        return None

    # The AuthHandler constructor expects the auth_url_endpoint to be relative to the API's root domain
    # (e.g. /oauth/token). It then constructs the full URL using this and global_config.
    # Ensure the auth_url_endpoint from INI is just the path part.
    handler = AuthHandler(auth_url_endpoint=auth_endpoint, client_id=client_id, client_secret=client_secret)
    
    # Optionally trigger initial token fetch to fail early if auth is broken
    # try:
    #     handler.get_auth_header() 
    # except Exception as e:
    #     pytest.fail(f"Initial authentication failed for admin client: {e}")
    return handler

@pytest.fixture(scope="session")
def enumerator_auth_handler(env_config, api_base_url):
    """
    Provides an AuthHandler instance for enumerator-level API access.
    Similar to admin_auth_handler but uses enumerator-specific credentials.
    """
    try:
        client_id = ConfigLoader.get_option(env_config, "API", "enum_client_id")
        client_secret_ref = ConfigLoader.get_option(env_config, "API", "enum_client_secret_ref")
        auth_endpoint = ConfigLoader.get_option(env_config, "API", "token_endpoint", fallback="/oauth/token")
    except KeyError as e:
        pytest.skip(f"Enumerator API authentication details (client_id, client_secret_ref, or token_endpoint) missing in config: {e}")
        return None

    client_secret = ConfigLoader.get_env_credential(env_config, "API", client_secret_ref)
    if not client_secret:
        pytest.skip(f"Enumerator client secret environment variable '{client_secret_ref}' not set or empty.")
        return None

    handler = AuthHandler(auth_url_endpoint=auth_endpoint, client_id=client_id, client_secret=client_secret)
    return handler

@pytest.fixture(scope="function")
def api_client_unauthenticated(api_base_url):
    """Provides an API client instance without any authentication handler."""
    client = ApiClient(base_url=api_base_url, auth_handler=None)
    logger.debug("Provided unauthenticated API client.")
    return client

@pytest.fixture(scope="function")
def admin_api_client(api_base_url, admin_auth_handler):
    """
    Provides an API client instance authenticated as an admin.
    Skips if admin_auth_handler is not available.
    """
    if admin_auth_handler is None:
        pytest.skip("Admin auth handler not available, skipping admin API client fixture.")
    client = ApiClient(base_url=api_base_url, auth_handler=admin_auth_handler)
    logger.debug("Provided admin-authenticated API client.")
    return client

@pytest.fixture(scope="function")
def enumerator_api_client(api_base_url, enumerator_auth_handler):
    """
    Provides an API client instance authenticated as an enumerator.
    Skips if enumerator_auth_handler is not available.
    """
    if enumerator_auth_handler is None:
        pytest.skip("Enumerator auth handler not available, skipping enumerator API client fixture.")
    client = ApiClient(base_url=api_base_url, auth_handler=enumerator_auth_handler)
    logger.debug("Provided enumerator-authenticated API client.")
    return client

@pytest.fixture(scope="session")
def test_data_loader_api():
    """Provides a test data loader instance for API tests."""
    return ApiTestDataLoader()

# Pytest hook to store test outcome on the item object.
# This can be used by other fixtures (e.g., in web/mobile tests) to capture screenshots on failure.
# While not directly used by API tests for screenshots, it's a common utility hook.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture the outcome of each test phase (setup, call, teardown).
    The outcome report is stored on the 'item' object.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Store the report on the test item for each phase
    # e.g., item.rep_setup, item.rep_call, item.rep_teardown
    setattr(item, "rep_" + rep.when, rep)
```