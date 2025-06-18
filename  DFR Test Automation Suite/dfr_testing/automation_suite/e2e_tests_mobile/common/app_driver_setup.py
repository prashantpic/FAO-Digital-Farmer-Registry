```python
from appium import webdriver
from appium.webdriver.webdriver import WebDriver # For type hinting
from appium.options.android import UiAutomator2Options
# from appium.options.ios import XCUITestOptions # Example if iOS is added later

from dfr.testing.automation.utils.logger_setup import setup_logger
from dfr.testing.automation.config import global_config
import os
from pathlib import Path

logger = setup_logger(__name__)

class AppDriverSetup:
    """
    Manages the lifecycle of Appium WebDriver instances for mobile tests.
    Supports Android (UiAutomator2) and can be extended for iOS.
    Note: This class manages a single driver instance via a class variable `driver`.
    For parallel tests, each worker would need its own independent driver instance.
    """
    driver: WebDriver | None = None # Class variable to hold the current driver instance

    @staticmethod
    def get_appium_driver(platform_name: str = "Android",
                          device_name: str | None = None,
                          platform_version: str | None = None,
                          app_path: str | None = None,
                          app_package: str | None = None,
                          app_activity: str | None = None,
                          automation_name: str | None = None,
                          no_reset: bool = False,
                          full_reset: bool = False,
                          extra_caps: dict | None = None) -> WebDriver:
        """
        Initializes and returns a new Appium WebDriver instance.
        If a driver already exists, it returns the existing one. Call `quit_appium_driver` first for a new one.

        Args:
            platform_name (str): Mobile OS platform ('Android', 'iOS').
            device_name (str, optional): UDID of the device or name of the emulator.
            platform_version (str, optional): OS version of the device.
            app_path (str, optional): Absolute or relative path to the app file (.apk, .aab, .ipa).
                                      If relative, resolved against `global_config.BASE_DIR`.
            app_package (str, optional): Package name of the app (e.g., "com.example.myapp").
            app_activity (str, optional): Main activity of the app (e.g., ".MainActivity").
            automation_name (str, optional): Appium automation backend (e.g., "UiAutomator2", "XCUITest").
            no_reset (bool): If True, app data is kept between sessions. Defaults to False.
            full_reset (bool): If True, app is uninstalled/reinstalled. Defaults to False.
            extra_caps (dict, optional): Additional desired capabilities to merge/override.

        Returns:
            WebDriver: The initialized or existing Appium WebDriver instance.

        Raises:
            ValueError: If required capabilities are missing or platform is unsupported.
            FileNotFoundError: If app_path is provided but the file doesn't exist.
            Exception: If Appium driver initialization fails.
        """
        if AppDriverSetup.driver:
            logger.warning("Appium driver already initialized. Returning existing instance.")
            return AppDriverSetup.driver

        logger.info(f"Initializing Appium driver for {platform_name}.")
        
        options = None
        resolved_app_path = None

        if app_path:
            path_obj = Path(app_path)
            if not path_obj.is_absolute():
                resolved_app_path = str(global_config.BASE_DIR / app_path)
            else:
                resolved_app_path = str(app_path)
            
            if not Path(resolved_app_path).exists():
                logger.error(f"App file not found at: {resolved_app_path}")
                raise FileNotFoundError(f"App file not found at: {resolved_app_path}")
            logger.info(f"Using app from path: {resolved_app_path}")


        if platform_name.lower() == "android":
            options = UiAutomator2Options()
            options.automation_name = automation_name or "UiAutomator2"
            if device_name: options.device_name = device_name
            if platform_version: options.platform_version = platform_version
            
            if resolved_app_path:
                options.app = resolved_app_path
            elif app_package and app_activity:
                options.app_package = app_package
                options.app_activity = app_activity
            else:
                msg = "For Android, either 'app_path' or both 'app_package' and 'app_activity' must be provided."
                logger.error(msg)
                raise ValueError(msg)
            
            options.no_reset = no_reset
            options.full_reset = full_reset
            options.auto_grant_permissions = True # Commonly useful

        # Example for iOS (add when needed)
        # elif platform_name.lower() == "ios":
        #     options = XCUITestOptions()
        #     options.automation_name = automation_name or "XCUITest"
        #     if device_name: options.device_name = device_name
        #     if platform_version: options.platform_version = platform_version
        #     if resolved_app_path:
        #         options.app = resolved_app_path
        #     elif bundle_id: # iOS uses bundleId
        #          options.bundle_id = bundle_id
        #     else:
        #         msg = "For iOS, either 'app_path' or 'bundle_id' must be provided."
        #         logger.error(msg)
        #         raise ValueError(msg)
        #     options.no_reset = no_reset
        #     options.full_reset = full_reset
        else:
            logger.error(f"Unsupported platform: {platform_name}")
            raise ValueError(f"Unsupported platform: {platform_name}")

        if extra_caps:
            for cap, value in extra_caps.items():
                options.set_capability(cap, value)
        
        appium_server_url = global_config.APPIUM_SERVER_URL
        logger.info(f"Connecting to Appium server at: {appium_server_url}")
        logger.debug(f"Desired Capabilities (via Options object): {options.to_capabilities()}")

        try:
            AppDriverSetup.driver = webdriver.Remote(appium_server_url, options=options)
            # Set a basic implicit wait (prefer explicit waits in Screen Objects)
            AppDriverSetup.driver.implicitly_wait(global_config.DEFAULT_TIMEOUT_SECONDS / 3) # e.g. 10s
            logger.info(f"Appium driver for {platform_name} initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Appium driver from {appium_server_url}: {e}")
            AppDriverSetup.driver = None # Ensure driver is reset on failure
            raise
            
        return AppDriverSetup.driver

    @staticmethod
    def quit_appium_driver():
        """
        Quits the current Appium WebDriver instance and resets the class variable.
        """
        if AppDriverSetup.driver:
            try:
                AppDriverSetup.driver.quit()
                logger.info("Appium driver quit successfully.")
            except Exception as e:
                logger.error(f"Error quitting Appium driver: {e}")
            finally:
                AppDriverSetup.driver = None
        else:
            logger.info("No active Appium driver instance to quit.")

    # Flutter Driver setup is different and typically handled within Dart test files themselves by calling
    # `FlutterDriver.connect()`. This class focuses on Appium.
    # If Python needs to *trigger* Flutter Driver tests, it would typically be via a shell command.
```