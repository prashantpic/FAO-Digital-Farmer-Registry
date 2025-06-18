import os
from pathlib import Path

# Base directory for the test suite
# Assumes this file is in dfr_testing/automation_suite/config/
# and the suite root is dfr_testing/automation_suite/
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment URLs (can be overridden by specific env configs or environment variables)
BASE_URL_DEV_API = os.getenv("DFR_API_URL_DEV", "http://dev-dfr-api.example.com/api/v1")
BASE_URL_DEV_WEB_ADMIN = os.getenv("DFR_ADMIN_URL_DEV", "http://dev-dfr-admin.example.com")
BASE_URL_DEV_WEB_PORTAL = os.getenv("DFR_PORTAL_URL_DEV", "http://dev-dfr-portal.example.com")

BASE_URL_STAGING_API = os.getenv("DFR_API_URL_STAGING", "http://staging-dfr-api.example.com/api/v1")
BASE_URL_STAGING_WEB_ADMIN = os.getenv("DFR_ADMIN_URL_STAGING", "http://staging-dfr-admin.example.com")
BASE_URL_STAGING_WEB_PORTAL = os.getenv("DFR_PORTAL_URL_STAGING", "http://staging-dfr-portal.example.com")


# Default Timeouts
DEFAULT_TIMEOUT_SECONDS = 30  # For web element waits, API call timeouts
POLL_FREQUENCY_SECONDS = 0.5 # For explicit waits

# Test Data Paths
TEST_DATA_BASE_PATH = BASE_DIR / "test_data"
API_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "api"
WEB_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "web"
MOBILE_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "mobile"
# ODOO_TEST_DATA_PATH = TEST_DATA_BASE_PATH / "odoo" # Placeholder if Odoo specific data files are needed

# Reporting
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

# Appium Server Configuration
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723/wd/hub") # Default, can be overridden

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
    """
    Retrieves the API base URL for the specified or current target environment.
    Args:
        env_name (str, optional): Override target environment. Defaults to None (uses DFR_TARGET_ENV).
    Returns:
        str: The API base URL.
    """
    target_env = env_name or get_target_environment()
    if target_env == "staging":
        return BASE_URL_STAGING_API
    return BASE_URL_DEV_API # Default to dev

def get_web_admin_url(env_name: str = None) -> str:
    """
    Retrieves the Web Admin Portal URL for the specified or current target environment.
    Args:
        env_name (str, optional): Override target environment. Defaults to None (uses DFR_TARGET_ENV).
    Returns:
        str: The Web Admin Portal URL.
    """
    target_env = env_name or get_target_environment()
    if target_env == "staging":
        return BASE_URL_STAGING_WEB_ADMIN
    return BASE_URL_DEV_WEB_ADMIN

def get_web_portal_url(env_name: str = None) -> str:
    """
    Retrieves the Web Farmer Portal URL for the specified or current target environment.
    Args:
        env_name (str, optional): Override target environment. Defaults to None (uses DFR_TARGET_ENV).
    Returns:
        str: The Web Farmer Portal URL.
    """
    target_env = env_name or get_target_environment()
    if target_env == "staging":
        return BASE_URL_STAGING_WEB_PORTAL
    return BASE_URL_DEV_WEB_PORTAL

# Ensure report directories exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Ensure base test data directories exist (optional, individual loaders might also do this)
API_TEST_DATA_PATH.mkdir(parents=True, exist_ok=True)
WEB_TEST_DATA_PATH.mkdir(parents=True, exist_ok=True)
MOBILE_TEST_DATA_PATH.mkdir(parents=True, exist_ok=True)
# ODOO_TEST_DATA_PATH.mkdir(parents=True, exist_ok=True)