```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from e2e_tests_web.common.web_driver_setup import WebDriverSetup
from e2e_tests_web.common.page_objects.admin_portal.farmer_management_page import FarmerManagementPage
# from e2e_tests_web.common.page_objects.admin_portal.admin_login_page import AdminLoginPage # If login is separate & detailed
from config import global_config
from utils.test_data_web_loader import WebTestDataLoader
from utils.reporting_utils import capture_screenshot_selenium
from utils.config_loader import ConfigLoader
from utils.logger_setup import setup_logger

logger = setup_logger(__name__)

# Assume a pytest conftest.py hook is set up for `request.node.rep_call`
# Example hook in root conftest.py or e2e_tests_web/conftest.py:
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)

@pytest.mark.web
@pytest.mark.admin_portal
class TestFarmerCreationAdmin:
    """
    E2E tests for creating new farmers in the DFR Admin Portal (Odoo).
    """

    @pytest.fixture(scope="function")
    def selenium_driver(self, request):
        """
        Sets up and tears down the Selenium WebDriver for each test function.
        Captures a screenshot on test failure.
        """
        browser_name = request.config.getoption("--browser", default="chrome")
        headless_option_str = request.config.getoption("--headless", default="True")
        headless = headless_option_str.lower() in ('true', '1', 'yes')


        driver = None
        try:
            driver = WebDriverSetup.get_webdriver(browser_name=browser_name, headless=headless)
            yield driver
        except Exception as e:
            logger.error(f"WebDriver setup failed: {e}")
            pytest.fail(f"Failed to initialize WebDriver: {e}")
        finally:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                test_name = request.node.name
                if driver:
                    capture_screenshot_selenium(driver, f"FAILED_{test_name}")
                else:
                    logger.warning(f"Driver not available to capture screenshot for failed test: {test_name}")
            
            if driver:
                WebDriverSetup.quit_webdriver(driver)

    @pytest.fixture(scope="session")
    def test_data_web(self):
        """Provides a test data loader instance for web E2E tests."""
        return WebTestDataLoader()

    @pytest.fixture(scope="function")
    def admin_authenticated_session(self, selenium_driver, env_config): # env_config from root conftest.py
         """
         Logs in to the Admin Portal and returns the driver.
         This fixture assumes a login page exists or uses direct navigation as placeholder.
         """
         admin_portal_config = ConfigLoader.get_section(env_config, "WEB_ADMIN_PORTAL")
         admin_url = admin_portal_config.get("base_url", global_config.get_web_admin_url())
         
         try:
             admin_user = admin_portal_config.get("admin_user")
             admin_pass_ref = admin_portal_config.get("admin_password_secret_ref")
             admin_password = ConfigLoader.get_env_credential(env_config, "WEB_ADMIN_PORTAL", "admin_password_secret_ref")


             if not admin_user or not admin_password:
                  pytest.skip(f"Admin web user/password not fully configured. User: {admin_user}, Pass Ref: {admin_pass_ref}")

             # Placeholder: Simulate login by navigating directly to a post-login URL or use AdminLoginPage
             # Actual Odoo login involves finding username, password fields, and login button.
             # For simplicity of SDS, assuming Odoo login page is at admin_url
             logger.info(f"Attempting to login to Admin Portal at {admin_url} as user {admin_user}")
             selenium_driver.get(admin_url)

             # Example Odoo login locators (these are very generic, specific app might differ)
             login_field = (By.ID, "login")
             password_field = (By.ID, "password")
             # Odoo login button might not have a simple ID, could be by type/text
             login_button = (By.XPATH, "//button[@type='submit']")
             
             WebDriverWait(selenium_driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                 EC.presence_of_element_located(login_field)
             ).send_keys(admin_user)
             
             selenium_driver.find_element(*password_field).send_keys(admin_password)
             selenium_driver.find_element(*login_button).click()

             # Wait for a post-login element (e.g., Odoo main navbar, app menu)
             # This locator is highly dependent on Odoo version and DFR customization
             post_login_indicator = (By.CLASS_NAME, "o_main_navbar") # Generic Odoo main navbar
             # post_login_indicator = (By.XPATH, "//nav[contains(@class, 'o_main_navbar')]") # More specific
             WebDriverWait(selenium_driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
                 EC.visibility_of_element_located(post_login_indicator),
                 message="Admin portal post-login element not visible, login might have failed."
             )
             logger.info(f"Successfully logged in as {admin_user}.")
             return selenium_driver

         except Exception as e:
              logger.error(f"Failed during admin portal login setup: {e}")
              capture_screenshot_selenium(selenium_driver, "LOGIN_FAILURE_ADMIN_PORTAL")
              pytest.fail(f"Failed during admin portal login setup: {e}")


    @pytest.mark.smoke
    def test_create_new_farmer_successfully(self, admin_authenticated_session, test_data_web):
        """
        Tests the end-to-end flow of creating a new farmer via the Admin Portal UI.
        """
        driver = admin_authenticated_session
        admin_base_url = ConfigLoader.get_option(admin_authenticated_session.env_config, "WEB_ADMIN_PORTAL", "base_url")


        farmer_manager_page = FarmerManagementPage(driver)
        # Navigate to farmer list view (assumes Odoo navigation pattern)
        # This URL might need specific action IDs from Odoo backend for robust navigation
        # farmer_list_url = f"{admin_base_url}/web#model=dfr.farmer&view_type=list"
        # logger.info(f"Navigating to Farmer List view: {farmer_list_url}")
        # driver.get(farmer_list_url)
        # WebDriverWait(driver, global_config.DEFAULT_TIMEOUT_SECONDS).until(
        #    EC.visibility_of_element_located(farmer_manager_page._CONTROL_PANEL)
        # )
        # Prefer navigation via POM methods if available or menu clicks
        farmer_manager_page.navigate_to_list_view(admin_base_url)


        farmer_manager_page.click_create_button()
        
        new_farmer_data = test_data_web.get_farmer_data("valid_new_farmer_admin_portal")
        
        farmer_manager_page.enter_farmer_name(new_farmer_data["fullName"])
        farmer_manager_page.enter_farmer_uid(new_farmer_data["uid"])
        # Example of filling other fields based on FarmerManagementPage methods (add them if needed)
        # if "dateOfBirth" in new_farmer_data:
        #    farmer_manager_page.enter_farmer_dob(new_farmer_data["dateOfBirth"])
        # ... fill other required fields ...
        
        farmer_manager_page.click_save_button()
        
        # Verification
        # Odoo typically shows a notification or redirects.
        # Let's assume after save, it might go back to the list or stay on form view.
        # If it stays on form, the title might change or some readonly fields appear.
        # If it goes to list, search and verify.
        
        # For simplicity, we will navigate back to list and search
        logger.info("Navigating back to list view to verify farmer creation.")
        farmer_manager_page.navigate_to_list_view(admin_base_url)
        farmer_manager_page.search_farmer(new_farmer_data["uid"]) # Search by UID as it should be unique

        assert farmer_manager_page.is_farmer_listed(new_farmer_data["fullName"]), \
            f"Farmer '{new_farmer_data['fullName']}' with UID '{new_farmer_data['uid']}' not found in list after creation."
        logger.info(f"Farmer '{new_farmer_data['fullName']}' created and listed successfully.")


    @pytest.mark.regression
    def test_create_farmer_with_missing_required_fields(self, admin_authenticated_session, test_data_web):
        """
        Tests farmer creation with missing required fields to verify validation.
        """
        driver = admin_authenticated_session
        admin_base_url = ConfigLoader.get_option(admin_authenticated_session.env_config, "WEB_ADMIN_PORTAL", "base_url")

        farmer_manager_page = FarmerManagementPage(driver)
        farmer_manager_page.navigate_to_list_view(admin_base_url)
        farmer_manager_page.click_create_button()

        incomplete_farmer_data = test_data_web.get_farmer_data("incomplete_new_farmer")

        # Fill only some fields, intentionally skip required ones like 'fullName' or 'uid'
        # Example: If 'contactPhone' is provided in incomplete_farmer_data and is not required
        if "contactPhone" in incomplete_farmer_data:
             # Assuming a method exists for contact phone, placeholder for now
             # farmer_manager_page.enter_contact_phone(incomplete_farmer_data["contactPhone"])
             logger.info(f"Attempting to create farmer with incomplete data (e.g., missing name/uid). Data: {incomplete_farmer_data}")
        
        # If UID is part of incomplete data but name is missing
        if "uid" in incomplete_farmer_data:
             farmer_manager_page.enter_farmer_uid(incomplete_farmer_data["uid"])
        # Intentionally DO NOT set farmer_name if it's required and missing from data

        farmer_manager_page.click_save_button()

        # Verification: Check for Odoo validation error messages
        # Odoo often shows a red notification for validation errors.
        error_message = farmer_manager_page.get_notification_text(timeout=10)
        
        assert error_message is not None, "No error notification displayed for incomplete data."
        # Odoo error messages can vary, check for common keywords
        assert ("validation error" in error_message.lower() or 
                "is invalid" in error_message.lower() or 
                "required field" in error_message.lower() or
                "missing field" in error_message.lower()), \
             f"Expected validation error message not found or content mismatch. Actual: '{error_message}'"
        
        logger.info(f"Validation error received as expected: {error_message}")

        # Optionally, check if still on the form view (i.e., save was blocked)
        # assert farmer_manager_page._is_element_visible(farmer_manager_page._FORM_VIEW, timeout=1), \
        #        "Form view is not visible after attempting to save with missing required fields."
```