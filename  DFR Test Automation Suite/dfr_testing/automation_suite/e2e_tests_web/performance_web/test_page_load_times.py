```python
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from e2e_tests_web.common.web_driver_setup import WebDriverSetup
from e2e_tests_web.common.page_objects.admin_portal.farmer_management_page import FarmerManagementPage # For Admin Portal URLs/elements
from config import global_config
from utils.config_loader import ConfigLoader # For login if needed for admin pages
from utils.reporting_utils import capture_screenshot_selenium
from utils.logger_setup import setup_logger

logger = setup_logger(__name__)

# Performance targets from SDS (REQ-FSSP-011, REQ-B.5 interpretation)
MAX_PAGE_LOAD_TIME_S_PORTAL = 3.0  # For Farmer Self-Service Portal pages
MAX_PAGE_LOAD_TIME_S_ADMIN_DASHBOARD = 7.0 # Example, Admin dashboard might be heavier
MAX_PAGE_LOAD_TIME_S_ADMIN_LIST_VIEW = 10.0 # Example, Admin list view with data

@pytest.mark.web
@pytest.mark.performance
class TestPageLoadTimesWeb:

    @pytest.fixture(scope="function")
    def selenium_driver(self, request):
        browser_name = request.config.getoption("--browser", default="chrome")
        headless_option_str = request.config.getoption("--headless", default="True")
        headless = headless_option_str.lower() in ('true', '1', 'yes')
        
        driver = None
        try:
            driver = WebDriverSetup.get_webdriver(browser_name=browser_name, headless=headless)
            yield driver
        except Exception as e:
            logger.error(f"WebDriver setup failed for performance test: {e}")
            pytest.fail(f"Failed to initialize WebDriver for performance test: {e}")
        finally:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                test_name = request.node.name
                if driver:
                    capture_screenshot_selenium(driver, f"FAILED_PERF_{test_name}")
            if driver:
                WebDriverSetup.quit_webdriver(driver)

    @pytest.fixture(scope="function")
    def admin_authenticated_session_perf(self, selenium_driver, env_config): # env_config from root conftest.py
         """ Authenticates admin for performance tests requiring login. """
         admin_portal_config = ConfigLoader.get_section(env_config, "WEB_ADMIN_PORTAL")
         admin_url = admin_portal_config.get("base_url", global_config.get_web_admin_url())
         
         try:
             admin_user = admin_portal_config.get("admin_user")
             admin_password = ConfigLoader.get_env_credential(env_config, "WEB_ADMIN_PORTAL", "admin_password_secret_ref")

             if not admin_user or not admin_password:
                  pytest.skip(f"Admin web user/password not fully configured for performance test.")

             selenium_driver.get(admin_url)
             login_field = (By.ID, "login")
             password_field = (By.ID, "password")
             login_button = (By.XPATH, "//button[@type='submit']")
             
             WebDriverWait(selenium_driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                 EC.presence_of_element_located(login_field)
             ).send_keys(admin_user)
             selenium_driver.find_element(*password_field).send_keys(admin_password)
             selenium_driver.find_element(*login_button).click()

             post_login_indicator = (By.CLASS_NAME, "o_main_navbar")
             WebDriverWait(selenium_driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                 EC.visibility_of_element_located(post_login_indicator)
             )
             return selenium_driver
         except Exception as e:
              capture_screenshot_selenium(selenium_driver, "LOGIN_FAILURE_PERF_ADMIN_PORTAL")
              pytest.fail(f"Failed during admin portal login setup for performance test: {e}")

    def _measure_page_load(self, driver, url_to_load: str, expected_element_locator: tuple = None, timeout: int = None):
        """
        Navigates to a URL and measures load time.
        Waits for document.readyState 'complete' and optionally for a key element.
        """
        _timeout = timeout or global_config.DEFAULT_TIMEOUT_SECONDS
        logger.info(f"Measuring page load time for: {url_to_load}")
        
        load_time = -1.0 # Default if measurement fails before completion
        start_time = time.perf_counter()
        try:
            driver.get(url_to_load)
            
            WebDriverWait(driver, _timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete',
                message=f"Document did not reach 'complete' state for {url_to_load} within {_timeout}s"
            )
            
            if expected_element_locator:
                WebDriverWait(driver, _timeout).until(
                    EC.visibility_of_element_located(expected_element_locator),
                    message=f"Key element {expected_element_locator} not visible for {url_to_load} within {_timeout}s"
                )
            
            end_time = time.perf_counter()
            load_time = end_time - start_time
            logger.info(f"Page load time for {url_to_load}: {load_time:.2f}s")
            
        except TimeoutException as e:
            end_time = time.perf_counter() # Record time of timeout
            load_time = end_time - start_time # This will be roughly the timeout duration
            logger.error(f"Page load timed out for {url_to_load} after {load_time:.2f}s: {e.msg}")
            # Re-raise to fail the test, or return a very high value for assertion failure
            pytest.fail(f"Page load timed out for {url_to_load} after {load_time:.2f}s. Details: {e.msg}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during page load for {url_to_load}: {e}", exc_info=True)
            pytest.fail(f"Unexpected error during page load for {url_to_load}: {e}")
            
        return load_time

    @pytest.mark.regression
    def test_farmer_portal_home_page_load_time(self, selenium_driver):
        """Measures load time of the Farmer Self-Service Portal Home page."""
        url = global_config.get_web_portal_url()
        # Key element on Farmer Portal home page (replace with actual locator)
        # Example: (By.ID, "fssp_welcome_header") or a main content block
        key_element = (By.TAG_NAME, "body") # Fallback to body tag if no specific element known
        
        load_time = self._measure_page_load(selenium_driver, url, key_element)
        assert load_time < MAX_PAGE_LOAD_TIME_S_PORTAL, \
            f"Farmer Portal Home Page load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_PORTAL}s"

    @pytest.mark.regression
    def test_farmer_portal_registration_form_load_time(self, selenium_driver):
        """Measures load time of the Farmer Self-Service Portal Registration Form page."""
        url = global_config.get_web_portal_url() + "/register" # Example URL path
        # Key element on registration form (replace with actual locator)
        # Example: (By.ID, "register_button") or (By.NAME, "fullName_field")
        key_element = (By.XPATH, "//form[contains(@action,'register')]//button[@type='submit']") # Generic submit button in a register form

        load_time = self._measure_page_load(selenium_driver, url, key_element)
        assert load_time < MAX_PAGE_LOAD_TIME_S_PORTAL, \
            f"Farmer Portal Registration Form load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_PORTAL}s"

    @pytest.mark.regression
    def test_admin_portal_dashboard_load_time(self, admin_authenticated_session_perf):
        """Measures load time of the Admin Portal Dashboard (post-login)."""
        driver = admin_authenticated_session_perf
        # Dashboard URL might be the base URL after login, or a specific path
        # Odoo often uses /web or /web#home for dashboard
        admin_base_url = ConfigLoader.get_option(driver.env_config, "WEB_ADMIN_PORTAL", "base_url")
        dashboard_url = f"{admin_base_url}/web" # Adjust if Odoo uses a specific dashboard fragment like #home
        
        # Key element on Admin Dashboard (Odoo example: main content area or app switcher)
        key_element = (By.CLASS_NAME, "o_action_manager") # Odoo's main content area for actions
        
        load_time = self._measure_page_load(driver, dashboard_url, key_element)
        assert load_time < MAX_PAGE_LOAD_TIME_S_ADMIN_DASHBOARD, \
            f"Admin Portal Dashboard load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_ADMIN_DASHBOARD}s"

    @pytest.mark.regression
    def test_admin_portal_farmer_list_load_time(self, admin_authenticated_session_perf):
        """Measures load time of the Admin Portal Farmer List view (post-login)."""
        driver = admin_authenticated_session_perf
        admin_base_url = ConfigLoader.get_option(driver.env_config, "WEB_ADMIN_PORTAL", "base_url")

        # Construct Farmer List URL using FarmerManagementPage details (if available and robust)
        # This requires knowing the Odoo model name and potentially action ID.
        # Example (generic Odoo list view URL for a model):
        # Replace 'dfr.farmer' with actual model name from Odoo.
        # Replace action_id if navigation is action-based.
        farmer_list_url = f"{admin_base_url}/web#model=dfr.farmer&view_type=list" 
        # A more robust way is to navigate via UI using FarmerManagementPage, but for pure load time, direct URL is fine.
        
        # Key element on Farmer List view (Odoo example: the list view container or create button)
        key_element = FarmerManagementPage._LIST_VIEW # Using the locator from POM
        
        load_time = self._measure_page_load(driver, farmer_list_url, key_element)
        assert load_time < MAX_PAGE_LOAD_TIME_S_ADMIN_LIST_VIEW, \
            f"Admin Portal Farmer List View load time {load_time:.2f}s exceeds target {MAX_PAGE_LOAD_TIME_S_ADMIN_LIST_VIEW}s"
```