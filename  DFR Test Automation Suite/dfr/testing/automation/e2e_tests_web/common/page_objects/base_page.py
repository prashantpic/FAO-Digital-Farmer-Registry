```python
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from dfr.testing.automation.config import global_config
from dfr.testing.automation.utils.logger_setup import setup_logger

logger = setup_logger(__name__)

class BasePage:
    """
    Base class for all Page Objects in the web E2E test suite.
    Provides common methods for interacting with web elements using explicit waits.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the BasePage with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver
        # Set up WebDriverWait with default timeout and poll frequency from global config
        self.wait = WebDriverWait(self.driver, global_config.DEFAULT_TIMEOUT_SECONDS,
                                  poll_frequency=global_config.POLL_FREQUENCY_SECONDS)
        logger.debug(f"BasePage initialized with driver and default wait of {global_config.DEFAULT_TIMEOUT_SECONDS}s.")

    def _wait_for(self, condition, timeout: int = None):
        """
        Generic helper to wait for a specific ExpectedCondition.

        Args:
            condition: The ExpectedCondition to wait for.
            timeout (int, optional): Custom timeout for this wait. Defaults to global default.

        Returns:
            The result of the condition if successful.

        Raises:
            TimeoutException: If the condition is not met within the timeout.
        """
        _wait_instance = self.wait
        if timeout is not None:
            _wait_instance = WebDriverWait(self.driver, timeout, poll_frequency=global_config.POLL_FREQUENCY_SECONDS)
        
        try:
            return _wait_instance.until(condition)
        except TimeoutException as e:
            # Log the specific condition that timed out for better debugging
            logger.error(f"Timeout waiting for condition: {condition}. Details: {e.msg}")
            raise  # Re-raise the TimeoutException
        except Exception as e:
            logger.error(f"An unexpected error occurred while waiting for condition {condition}: {e}")
            raise

    def _find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Finds a single web element using the provided locator after waiting for its presence.

        Args:
            locator (tuple): The locator tuple (e.g., (By.ID, "element_id")).
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            WebElement: The found web element.

        Raises:
            NoSuchElementException: If the element is not found (re-raised from TimeoutException).
        """
        logger.debug(f"Attempting to find element: {locator}")
        try:
            element = self._wait_for(EC.presence_of_element_located(locator), timeout)
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            # Convert TimeoutException to NoSuchElementException for semantic clarity in this context
            logger.error(f"Element not found (timed out waiting for presence): {locator}")
            raise NoSuchElementException(f"Element not found by locator: {locator}")

    def _find_elements(self, locator: tuple, timeout: int = None) -> list[WebElement]:
        """
        Finds multiple web elements using the provided locator after waiting for their presence.

        Args:
            locator (tuple): The locator tuple.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            list[WebElement]: A list of found web elements (empty if none found).
        """
        logger.debug(f"Attempting to find elements: {locator}")
        try:
            elements = self._wait_for(EC.presence_of_all_elements_located(locator), timeout)
            logger.debug(f"Found {len(elements)} elements with locator: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found (timed out waiting for presence) for locator: {locator}")
            return [] # Return empty list if no elements found within timeout

    def _click(self, locator: tuple, timeout: int = None):
        """
        Clicks on a web element after ensuring it is visible and clickable.

        Args:
            locator (tuple): The locator tuple for the element to click.
            timeout (int, optional): Custom timeout. Defaults to global default.
        """
        logger.debug(f"Attempting to click element: {locator}")
        try:
            element = self._wait_for(EC.element_to_be_clickable(locator), timeout)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except StaleElementReferenceException:
            logger.warning(f"StaleElementReferenceException for {locator}. Retrying click once...")
            # Simple retry logic for stale elements, common in dynamic pages
            element = self._wait_for(EC.element_to_be_clickable(locator), timeout)
            element.click()
            logger.info(f"Clicked element after retry: {locator}")
        except TimeoutException:
            logger.error(f"Element not clickable within timeout: {locator}")
            raise # Re-raise TimeoutException if element is not clickable

    def _type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
        """
        Types text into an input field after ensuring it is visible.

        Args:
            locator (tuple): The locator tuple for the input field.
            text (str): The text to type.
            clear_first (bool): Whether to clear the field before typing. Defaults to True.
            timeout (int, optional): Custom timeout. Defaults to global default.
        """
        logger.debug(f"Attempting to type '{text}' into element: {locator}")
        element = self._wait_for_element_visible(locator, timeout) # Ensure element is visible first
        if clear_first:
            try:
                element.clear()
                logger.debug(f"Cleared text in element: {locator}")
            except Exception as e:
                logger.warning(f"Could not clear element {locator} before typing: {e}. Proceeding to type.")
        element.send_keys(text)
        logger.info(f"Typed text into element: {locator}")

    def _get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Gets the text content of a web element after ensuring it is visible.

        Args:
            locator (tuple): The locator tuple for the element.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            str: The text of the element.
        """
        logger.debug(f"Attempting to get text from element: {locator}")
        element = self._wait_for_element_visible(locator, timeout)
        text = element.text
        logger.debug(f"Retrieved text '{text}' from element: {locator}")
        return text

    def _is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Checks if a web element is visible on the page within a given timeout.
        Uses a shorter timeout by default for quick checks.

        Args:
            locator (tuple): The locator tuple for the element.
            timeout (int): The maximum time (in seconds) to wait for visibility. Defaults to 5.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        logger.debug(f"Checking visibility of element: {locator} with timeout: {timeout}s")
        try:
            self._wait_for_element_visible(locator, timeout=timeout)
            logger.debug(f"Element {locator} is visible.")
            return True
        except TimeoutException:
            logger.debug(f"Element {locator} not visible within {timeout}s timeout.")
            return False
        except NoSuchElementException: # Should be caught by _wait_for_element_visible's TimeoutException
            logger.debug(f"Element {locator} not found, thus not visible.")
            return False

    def _wait_for_element_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Waits for a web element to be visible on the page and returns it.

        Args:
            locator (tuple): The locator tuple for the element.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            WebElement: The visible web element.

        Raises:
            TimeoutException: If the element is not visible within the timeout.
        """
        logger.debug(f"Waiting for element visibility: {locator}")
        try:
            element = self._wait_for(EC.visibility_of_element_located(locator), timeout)
            logger.debug(f"Element is visible: {locator}")
            return element
        except TimeoutException: # Already logged by _wait_for, re-raise
            raise

    def get_page_title(self) -> str:
        """Gets the current page title."""
        title = self.driver.title
        logger.info(f"Current page title: '{title}'")
        return title

    def get_current_url(self) -> str:
        """Gets the current page URL."""
        url = self.driver.current_url
        logger.info(f"Current page URL: '{url}'")
        return url

    def navigate_to(self, url: str):
        """Navigates the browser to the specified URL."""
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)
        logger.info(f"Navigation to {url} complete.")

    def scroll_to_element(self, locator: tuple):
        """
        Scrolls the page to make the specified element visible.
        This is useful for elements that are not in the viewport.

        Args:
            locator (tuple): The locator tuple for the element to scroll to.
        """
        logger.debug(f"Scrolling to element: {locator}")
        try:
            # First, ensure the element is present in the DOM
            element = self._find_element(locator) # Uses presence_of_element_located
            # Then, use JavaScript to scroll it into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # Optional: Add a small wait for scrolling animation if needed
            # time.sleep(0.5)
            logger.info(f"Scrolled to make element visible: {locator}")
        except Exception as e:
            logger.error(f"Error scrolling to element {locator}: {e}")
            raise
```