```python
import pytest
import time
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # For potential direct driver interactions if needed

from e2e_tests_web.common.web_driver_setup import WebDriverSetup
from e2e_tests_web.common.page_objects.admin_portal.farmer_management_page import FarmerManagementPage
from config import global_config
from utils.test_data_web_loader import WebTestDataLoader
from utils.config_loader import ConfigLoader
from utils.reporting_utils import capture_screenshot_selenium
from utils.logger_setup import setup_logger

logger = setup_logger(__name__)

@pytest.mark.web
@pytest.mark.security
class TestXSSVulnerabilitiesWeb:
    """
    Security tests targeting Cross-Site Scripting (XSS) vulnerabilities in web portals.
    Focuses on input fields in the Admin Portal Farmer Management form.
    """

    @pytest.fixture(scope="function")
    def selenium_driver(self, request):
        browser_name = request.config.getoption("--browser", default="chrome")
        # Note: Headless browsers might suppress JavaScript alerts.
        # For reliable XSS testing via alert detection, non-headless might be better.
        headless_option_str = request.config.getoption("--headless", default="True")
        headless = headless_option_str.lower() in ('true', '1', 'yes')

        driver = None
        try:
            driver = WebDriverSetup.get_webdriver(browser_name=browser_name, headless=headless)
            yield driver
        except Exception as e:
            logger.error(f"WebDriver setup failed for XSS test: {e}")
            pytest.fail(f"Failed to initialize WebDriver for XSS test: {e}")
        finally:
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                test_name = request.node.name
                if driver:
                    capture_screenshot_selenium(driver, f"FAILED_XSS_{test_name}")
            if driver:
                WebDriverSetup.quit_webdriver(driver)

    @pytest.fixture(scope="function")
    def admin_authenticated_session(self, selenium_driver, env_config): # env_config from root conftest.py
         admin_portal_config = ConfigLoader.get_section(env_config, "WEB_ADMIN_PORTAL")
         admin_url = admin_portal_config.get("base_url", global_config.get_web_admin_url())
         
         try:
             admin_user = admin_portal_config.get("admin_user")
             admin_pass_ref = admin_portal_config.get("admin_password_secret_ref")
             admin_password = ConfigLoader.get_env_credential(env_config, "WEB_ADMIN_PORTAL", "admin_password_secret_ref")

             if not admin_user or not admin_password:
                  pytest.skip(f"Admin web user/password not fully configured for XSS test.")

             logger.info(f"Attempting to login to Admin Portal at {admin_url} as user {admin_user} for XSS test.")
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
                 EC.visibility_of_element_located(post_login_indicator),
                 message="Admin portal post-login element not visible, login might have failed for XSS test."
             )
             logger.info(f"Successfully logged in as {admin_user} for XSS test.")
             return selenium_driver
         except Exception as e:
              logger.error(f"Failed during admin portal login setup for XSS test: {e}")
              capture_screenshot_selenium(selenium_driver, "LOGIN_FAILURE_XSS_ADMIN_PORTAL")
              pytest.fail(f"Failed during admin portal login setup for XSS test: {e}")
    
    @pytest.fixture(scope="session")
    def test_data_web(self):
        return WebTestDataLoader()

    @pytest.mark.parametrize("xss_payload, payload_desc", [
        ("<script>alert('XSS_TEST_ALERT_1')</script>", "basic_script_alert"),
        ("<img src=x onerror=alert('XSS_TEST_IMG_ERROR_2')>", "img_onerror_alert"),
        ("<svg/onload=alert('XSS_TEST_SVG_ONLOAD_3')>", "svg_onload_alert"),
        ("\"><script>alert('XSS_TEST_ATTR_BREAKOUT_4')</script><\"", "attribute_breakout_script"),
        ("';alert('XSS_TEST_JS_CONTEXT_BREAKOUT_5')//", "js_context_breakout_alert"),
        # javascript:alert might not work in direct input fields but for hrefs/event handlers
        # "javascript:alert('XSS_TEST_JS_PROTO_6')" 
    ])
    def test_farmer_name_field_xss_admin_portal(self, admin_authenticated_session, test_data_web, xss_payload, payload_desc):
        """
        Tests the Farmer Name input field on the Admin Portal form for XSS vulnerabilities.
        """
        driver = admin_authenticated_session
        admin_base_url = ConfigLoader.get_option(driver.env_config, "WEB_ADMIN_PORTAL", "base_url")

        farmer_page = FarmerManagementPage(driver)
        farmer_page.navigate_to_list_view(admin_base_url) # Start from list view
        farmer_page.click_create_button() # Go to new farmer form

        # Generate a unique UID for this test instance to help locate it later if needed
        unique_test_uid = f"XSS-UID-{payload_desc}-{int(time.time())}"
        logger.info(f"Testing XSS payload ({payload_desc}): {xss_payload} with UID: {unique_test_uid}")

        alert_triggered = False
        try:
            farmer_page.enter_farmer_name(xss_payload)
            farmer_page.enter_farmer_uid(unique_test_uid) # Benign UID
            # Fill other required fields with benign data if any, e.g., from test_data_web
            # farmer_page.enter_farmer_dob("2000-01-01") # Example
            
            farmer_page.click_save_button()

            # Verification 1: Check for JavaScript Alerts immediately after action
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present()) # Short wait for alert
                alert = driver.switch_to.alert
                alert_text = alert.text
                logger.warning(f"XSS ALERT DETECTED! Text: '{alert_text}' for payload ({payload_desc}): '{xss_payload}'")
                alert.accept() # Dismiss the alert
                alert_triggered = True
            except TimeoutException:
                logger.info(f"No JavaScript alert detected immediately after save for payload ({payload_desc}). (Expected)")
            except UnexpectedAlertPresentException as e: # Should be caught by explicit wait ideally
                 logger.error(f"UnexpectedAlertPresentException for payload ({payload_desc}): {e.msg}")
                 try: driver.switch_to.alert.accept() # Try to dismiss
                 except NoAlertPresentException: pass
                 alert_triggered = True # Alert was present

            if alert_triggered:
                pytest.fail(f"XSS Vulnerability: JavaScript alert was triggered by payload ({payload_desc}): '{xss_payload}'")

            # Verification 2: Check if the payload is sanitized when displayed (if no alert)
            # Navigate back to list, search for the item, and inspect its rendered name.
            # This step assumes the save was successful or at least didn't crash the UI flow.
            logger.info(f"Navigating to list view to check sanitization for payload ({payload_desc}).")
            farmer_page.navigate_to_list_view(admin_base_url)
            farmer_page.search_farmer(unique_test_uid) # Search by the unique UID

            # Get the page source of the list view (or the specific element's HTML)
            # This part is complex as it requires precise locators for the displayed name.
            # For simplicity, check page source for raw payload. More robust: check specific element.
            time.sleep(1) # Allow search results to render
            page_source = driver.page_source

            if xss_payload in page_source:
                # This is a strong indicator of vulnerability if the exact raw payload is found.
                # However, context matters (e.g., if it's inside a JS variable string vs. rendered HTML).
                # A more specific check would be to find the element and check its innerHTML.
                logger.error(f"XSS POTENTIAL: Raw payload ({payload_desc}) '{xss_payload}' found in page source after saving.")
                # This check is a heuristic. Real verification needs careful DOM inspection.
                # For now, we'll consider this a failure if the raw payload is reflected.
                pytest.fail(f"XSS Vulnerability: Raw payload ({payload_desc}) '{xss_payload}' found in page source.")
            
            # More advanced: check for escaped versions. Example:
            # escaped_payload = xss_payload.replace("<", "&lt;").replace(">", "&gt;")
            # if not (escaped_payload in page_source):
            #     logger.warning(f"Payload ({payload_desc}) '{xss_payload}' not found as escaped string '{escaped_payload}' in page source.")
            # else:
            #     logger.info(f"Payload ({payload_desc}) appears to be HTML-escaped: '{escaped_payload}' found.")

            logger.info(f"XSS test for payload ({payload_desc}) completed. No direct alert and raw payload not found in source (basic check).")

        except UnexpectedAlertPresentException as e:
             logger.error(f"XSS ALERT DETECTED (during operation) for payload ({payload_desc}): {e.msg}")
             try: driver.switch_to.alert.accept()
             except NoAlertPresentException: pass
             pytest.fail(f"XSS Vulnerability: JavaScript alert displayed unexpectedly for payload ({payload_desc}): '{e.msg}'")
        except Exception as e:
            logger.error(f"An error occurred during XSS test with payload ({payload_desc}): {e}", exc_info=True)
            pytest.fail(f"Test failed due to unexpected error with payload ({payload_desc}): {e}")

    @pytest.mark.skip(reason="Needs a web page element that accepts untrusted user input in a URL or attribute for thorough testing.")
    @pytest.mark.parametrize("xss_payload", [
         "javascript:alert('URL_XSS_1')",
         "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTX0RFU1RfSURFQS séptima')PC9zY3JpcHQ+", # data: URI XSS
    ])
    def test_url_attribute_xss_web_portal(self, admin_authenticated_session, xss_payload):
        """
        Illustrative: Tests for XSS vulnerabilities in URL or HTML attributes.
        Requires identifying specific elements (e.g., profile image src, external link href)
        that can be influenced by user input containing crafted URLs.
        """
        driver = admin_authenticated_session
        # 1. Navigate to a page with a field that becomes part of a URL/attribute.
        # 2. Enter `xss_payload` into that field.
        # 3. Save/submit.
        # 4. Navigate to where this URL/attribute is rendered (e.g., view profile page).
        # 5. Check for alert or unsanitized payload in the element's attribute (e.g., `element.get_attribute('href')`).
        logger.info(f"Skipping URL/attribute XSS test for payload: {xss_payload}. Requires specific target element.")
        pass
```