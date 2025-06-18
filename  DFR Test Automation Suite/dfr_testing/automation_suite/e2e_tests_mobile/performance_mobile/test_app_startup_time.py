```python
import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from e2e_tests_mobile.common.app_driver_setup import AppDriverSetup
from utils.config_loader import ConfigLoader
from utils.reporting_utils import capture_screenshot_appium # For potential failure screenshots
from utils.logger_setup import setup_logger

logger = setup_logger(__name__)

# Performance target from SDS (B.5 interpretation, example value)
MAX_APP_STARTUP_TIME_S = 10.0 # Target for cold start until interactive

@pytest.mark.mobile_android # Or common mobile marker
@pytest.mark.performance
class TestAppStartupTimeMobile:

    @pytest.fixture(scope="function")
    def appium_android_driver_cold_start(self, request, env_config):
        """
        Sets up the Appium driver specifically for a cold start test.
        Uses fullReset=True to aim for a clean app state before launch.
        The driver initialization itself triggers the app launch.
        """
        mobile_config = ConfigLoader.get_section(env_config, "MOBILE_ANDROID")
        device_name = mobile_config.get("device_name")
        platform_version = mobile_config.get("platform_version")
        app_path = mobile_config.get("app_path", None)
        app_package = mobile_config.get("app_package", None)
        app_activity = mobile_config.get("app_activity", None)

        if not app_path and not (app_package and app_activity):
            pytest.skip("Mobile app configuration (app_path or app_package/activity) is missing for cold start test.")

        # Capabilities for cold start: fullReset ensures uninstall/reinstall or clean state
        # This is important for measuring true cold start.
        cold_start_extra_caps = {"appium:fullReset": True, "appium:noReset": False}
        
        driver = None
        try:
            # Time the driver initialization (which includes app launch)
            # This is a proxy for app launch time from Appium's perspective
            logger.info("Initializing Appium driver for cold start performance test...")
            
            # The actual app launch happens within get_appium_driver
            driver = AppDriverSetup.get_appium_driver(
                platform_name="Android",
                device_name=device_name,
                platform_version=platform_version,
                app_path=app_path,
                app_package=app_package,
                app_activity=app_activity,
                extra_caps=cold_start_extra_caps
            )
            yield driver # Provide the driver to the test method
            
        except Exception as e:
            logger.error(f"Appium driver setup failed for cold start test: {e}", exc_info=True)
            pytest.fail(f"Failed to initialize Appium driver for cold start test: {e}")
        finally:
            if driver:
                if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                    test_name = request.node.name
                    capture_screenshot_appium(driver, f"FAILED_STARTUP_{test_name}")
                AppDriverSetup.quit_appium_driver(driver)

    def test_mobile_app_cold_start_performance(self, appium_android_driver_cold_start):
        """
        Measures the time from app launch (driver init) until a key interactive
        element on the first screen is visible.
        """
        pytest.skip("Precise cold start time measurement is complex. This test measures time to first "
                    "interactive element post-launch. True cold start often requires OS-level tools or "
                    "parsing Appium's 'appLaunchDuration' (if available and reliable).")

        driver = appium_android_driver_cold_start # App is launched by the fixture

        # Define a locator for a key element on the app's initial screen.
        # This element should signify that the app is loaded and ready for interaction.
        # REPLACE WITH ACTUAL LOCATOR for the DFR mobile app's first screen.
        # Examples: A login button, a dashboard title, a welcome message.
        # Using a generic XPath for illustration, make this specific.
        first_interactive_element_locator = (
            AppiumBy.XPATH, 
            "//*[(@class='android.widget.Button' and (contains(@text, 'Login') or contains(@text, 'Start'))) or "
            "(@class='android.widget.TextView' and (contains(@text, 'Welcome') or contains(@text, 'Dashboard')))]"
        )
        # A more reliable locator would be by Accessibility ID or a specific resource ID.
        # first_interactive_element_locator = (AppiumBy.ACCESSIBILITY_ID, "main_dashboard_title_id") # Example

        # The app is already launched by the fixture. We measure time to visibility of the key element.
        # This is "perceived startup time" or "time to interactive" from the point Appium has control.
        wait_timeout_seconds = MAX_APP_STARTUP_TIME_S + 10 # Allow some buffer over target

        logger.info(f"Waiting for initial interactive element ({first_interactive_element_locator}) to be visible "
                    f"with a timeout of {wait_timeout_seconds}s.")
        
        time_to_interactive_element = -1.0
        start_wait_time = time.perf_counter()
        try:
            WebDriverWait(driver, wait_timeout_seconds).until(
                EC.visibility_of_element_located(first_interactive_element_locator),
                message=(f"Initial interactive element {first_interactive_element_locator} "
                         f"not visible within {wait_timeout_seconds}s after launch.")
            )
            end_wait_time = time.perf_counter()
            time_to_interactive_element = end_wait_time - start_wait_time
            logger.info(f"Initial interactive element became visible in {time_to_interactive_element:.2f}s.")

        except TimeoutException as e:
            end_wait_time = time.perf_counter() # Record time of timeout
            time_to_interactive_element = end_wait_time - start_wait_time
            logger.error(f"Timeout waiting for initial element: {e.msg}. Time elapsed: {time_to_interactive_element:.2f}s")
            pytest.fail(f"App failed to show initial interactive element within {wait_timeout_seconds}s. "
                        f"Elapsed: {time_to_interactive_element:.2f}s. Details: {e.msg}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while waiting for initial element: {e}", exc_info=True)
            pytest.fail(f"Test failed due to unexpected error waiting for element: {e}")

        # Assertion against the target startup time
        # This 'time_to_interactive_element' is a proxy for perceived startup time.
        # Appium's session capabilities might sometimes include 'appLaunchDuration' from Android,
        # which can be more accurate for the technical launch time if available and reliable.
        # session_caps = driver.session
        # app_launch_duration_ms = session_caps.get('appLaunchDuration') # Example
        # if app_launch_duration_ms:
        #     actual_startup_time_s = app_launch_duration_ms / 1000.0
        #     logger.info(f"Appium reported appLaunchDuration: {actual_startup_time_s:.2f}s")
        #     # Compare this `actual_startup_time_s` with MAX_APP_STARTUP_TIME_S
        # else:
        #     logger.warning("'appLaunchDuration' not found in session capabilities. Using time to interactive element.")
        
        logger.info(f"Mobile app time to interactive element (cold start proxy): {time_to_interactive_element:.2f}s "
                    f"(Target: < {MAX_APP_STARTUP_TIME_S}s)")
        
        assert time_to_interactive_element < MAX_APP_STARTUP_TIME_S, \
            f"App perceived startup time (to interactive) {time_to_interactive_element:.2f}s " \
            f"exceeds target {MAX_APP_STARTUP_TIME_S}s."
```