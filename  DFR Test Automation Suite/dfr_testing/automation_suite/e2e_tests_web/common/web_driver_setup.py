```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.remote.webdriver import WebDriver # For type hinting

from dfr.testing.automation.utils.logger_setup import setup_logger
from dfr.testing.automation.config import global_config

logger = setup_logger(__name__)

class WebDriverSetup:
    """
    Manages the lifecycle of Selenium WebDriver instances.
    Supports different browsers and headless mode using webdriver-manager.
    Note: This class manages a single driver instance via a class variable `driver`.
    For parallel tests (e.g., with pytest-xdist), each worker/process would need its own
    independent driver instance, typically managed by a test-scoped fixture.
    """
    driver: WebDriver | None = None # Class variable to hold the current driver instance

    @staticmethod
    def get_webdriver(browser_name: str = 'chrome', headless: bool = True, options_config: dict | None = None) -> WebDriver:
        """
        Initializes and returns a WebDriver instance. If a driver already exists, it returns the existing one.
        To get a new instance, call `quit_webdriver` first.

        Args:
            browser_name (str): The name of the browser ('chrome', 'firefox', 'edge').
            headless (bool): Whether to run the browser in headless mode.
            options_config (dict, optional): A dictionary of browser-specific options to apply.
                                            Example: {"chrome": {"arguments": ["--incognito"]}}

        Returns:
            WebDriver: The initialized or existing WebDriver instance.

        Raises:
            ValueError: If the browser name is unsupported.
            Exception: If WebDriver initialization fails.
        """
        if WebDriverSetup.driver:
            logger.warning("WebDriver already initialized. Returning existing instance.")
            return WebDriverSetup.driver

        browser_name = browser_name.lower()
        logger.info(f"Initializing WebDriver for browser: {browser_name}, headless: {headless}")

        current_options_config = options_config or {}

        try:
            if browser_name == 'chrome':
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless=new") # Recommended way for new headless
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu") # Often useful for headless
                options.add_argument("--log-level=WARNING") # Reduce console noise from Chrome
                # Apply custom options
                for arg in current_options_config.get("chrome", {}).get("arguments", []):
                    options.add_argument(arg)
                for cap, value in current_options_config.get("chrome", {}).get("capabilities", {}).items():
                    options.set_capability(cap, value)
                
                service = ChromeService(ChromeDriverManager().install())
                WebDriverSetup.driver = webdriver.Chrome(service=service, options=options)

            elif browser_name == 'firefox':
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                # Apply custom options
                for arg in current_options_config.get("firefox", {}).get("arguments", []):
                    options.add_argument(arg)
                # Firefox capabilities are often set differently or less commonly via options directly
                
                service = FirefoxService(GeckoDriverManager().install())
                WebDriverSetup.driver = webdriver.Firefox(service=service, options=options)

            elif browser_name == 'edge':
                options = webdriver.EdgeOptions()
                if headless:
                    options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu") # Often useful for headless
                # Apply custom options
                for arg in current_options_config.get("edge", {}).get("arguments", []):
                    options.add_argument(arg)

                service = EdgeService(EdgeChromiumDriverManager().install())
                WebDriverSetup.driver = webdriver.Edge(service=service, options=options)
            else:
                logger.error(f"Unsupported browser: {browser_name}")
                raise ValueError(f"Unsupported browser: {browser_name}")

            WebDriverSetup.driver.implicitly_wait(global_config.DEFAULT_TIMEOUT_SECONDS / 6) # Example: 5s if default is 30s
            if not headless:
                WebDriverSetup.driver.maximize_window()
            
            logger.info(f"{browser_name.capitalize()} WebDriver initialized successfully. Implicit wait: {WebDriverSetup.driver.timeouts.implicit_wait}s")
            return WebDriverSetup.driver

        except Exception as e:
            logger.error(f"Failed to initialize {browser_name.capitalize()} WebDriver: {e}")
            WebDriverSetup.driver = None # Ensure driver is reset on failure
            raise

    @staticmethod
    def quit_webdriver():
        """
        Quits the current WebDriver instance and resets the class variable.
        """
        if WebDriverSetup.driver:
            try:
                WebDriverSetup.driver.quit()
                logger.info("WebDriver quit successfully.")
            except Exception as e:
                logger.error(f"Error quitting WebDriver: {e}")
            finally:
                WebDriverSetup.driver = None
        else:
            logger.info("No active WebDriver instance to quit.")
```