```python
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction # For more complex gestures if needed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from dfr.testing.automation.config import global_config
from dfr.testing.automation.utils.logger_setup import setup_logger
import time

logger = setup_logger(__name__)

class BaseScreen:
    """
    Base class for all Screen Objects in the mobile E2E test suite (Appium).
    Provides common methods for interacting with mobile elements using explicit waits.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializes the BaseScreen with an Appium WebDriver instance.

        Args:
            driver (WebDriver): The Appium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, global_config.DEFAULT_TIMEOUT_SECONDS,
                                  poll_frequency=global_config.POLL_FREQUENCY_SECONDS)
        logger.debug(f"BaseScreen initialized with Appium driver and default wait of {global_config.DEFAULT_TIMEOUT_SECONDS}s.")

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
            logger.error(f"Timeout waiting for mobile condition: {condition}. Details: {e.msg}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while waiting for mobile condition {condition}: {e}")
            raise

    def _find_element(self, locator_type: AppiumBy, value: str, timeout: int = None):
        """
        Finds a single mobile element using the provided locator after waiting for its presence.

        Args:
            locator_type (AppiumBy): The Appium locator strategy (e.g., AppiumBy.ID).
            value (str): The locator value.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            WebElement: The found mobile element.

        Raises:
            NoSuchElementException: If the element is not found (re-raised from TimeoutException).
        """
        logger.debug(f"Attempting to find mobile element: {locator_type.value} = {value}")
        try:
            element = self._wait_for(EC.presence_of_element_located((locator_type, value)), timeout)
            logger.debug(f"Mobile element found: {locator_type.value} = {value}")
            return element
        except TimeoutException:
            logger.error(f"Mobile element not found (timed out waiting for presence): {locator_type.value} = {value}")
            raise NoSuchElementException(f"Mobile element not found by locator: {locator_type.value} = {value}")

    def _find_elements(self, locator_type: AppiumBy, value: str, timeout: int = None):
        """
        Finds multiple mobile elements using the provided locator after waiting for their presence.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            list[WebElement]: A list of found mobile elements (empty if none found).
        """
        logger.debug(f"Attempting to find mobile elements: {locator_type.value} = {value}")
        try:
            elements = self._wait_for(EC.presence_of_all_elements_located((locator_type, value)), timeout)
            logger.debug(f"Found {len(elements)} mobile elements with locator: {locator_type.value} = {value}")
            return elements
        except TimeoutException:
            logger.warning(f"No mobile elements found (timed out waiting for presence) for locator: {locator_type.value} = {value}")
            return []

    def _tap(self, locator_type: AppiumBy, value: str, timeout: int = None):
        """
        Taps on a mobile element after ensuring it is visible and clickable.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the element to tap.
            timeout (int, optional): Custom timeout. Defaults to global default.
        """
        logger.debug(f"Attempting to tap mobile element: {locator_type.value} = {value}")
        try:
            element = self._wait_for(EC.element_to_be_clickable((locator_type, value)), timeout)
            element.click() # Appium's click() method generally performs a tap action
            logger.info(f"Tapped mobile element: {locator_type.value} = {value}")
        except StaleElementReferenceException:
            logger.warning(f"StaleElementReferenceException for {locator_type.value}={value}. Retrying tap once...")
            element = self._wait_for(EC.element_to_be_clickable((locator_type, value)), timeout)
            element.click()
            logger.info(f"Tapped mobile element after retry: {locator_type.value} = {value}")
        except TimeoutException:
            logger.error(f"Mobile element not tappable within timeout: {locator_type.value} = {value}")
            raise

    def _type_text(self, locator_type: AppiumBy, value: str, text: str, clear_first: bool = True, timeout: int = None):
        """
        Types text into an input field on a mobile screen after ensuring it is visible.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the input field.
            text (str): The text to type.
            clear_first (bool): Whether to clear the field before typing. Defaults to True.
            timeout (int, optional): Custom timeout. Defaults to global default.
        """
        logger.debug(f"Attempting to type '{text}' into mobile element: {locator_type.value} = {value}")
        element = self._wait_for_element_visible(locator_type, value, timeout) # Ensure element is visible
        if clear_first:
            try:
                element.clear()
                logger.debug(f"Cleared text in mobile element: {locator_type.value} = {value}")
            except Exception as e: # Some elements might not support clear or might throw errors
                logger.warning(f"Could not clear mobile element {locator_type.value}={value}: {e}. Proceeding to type.")
        element.send_keys(text)
        logger.info(f"Typed text into mobile element: {locator_type.value} = {value}")

    def _get_text(self, locator_type: AppiumBy, value: str, timeout: int = None) -> str:
        """
        Gets the text content of a mobile element after ensuring it is visible.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the element.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            str: The text of the element (often from 'text' or 'content-desc' attribute).
        """
        logger.debug(f"Attempting to get text from mobile element: {locator_type.value} = {value}")
        element = self._wait_for_element_visible(locator_type, value, timeout)
        # For Appium, .text usually gets the visible text.
        # Sometimes, content-description might be needed: element.get_attribute('content-desc')
        text_content = element.text
        logger.debug(f"Retrieved text '{text_content}' from mobile element: {locator_type.value} = {value}")
        return text_content

    def _is_element_visible(self, locator_type: AppiumBy, value: str, timeout: int = 5) -> bool:
        """
        Checks if a mobile element is visible on the screen within a given timeout.
        Uses a shorter timeout by default for quick checks.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the element.
            timeout (int): The maximum time (in seconds) to wait for visibility. Defaults to 5.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        logger.debug(f"Checking visibility of mobile element: {locator_type.value} = {value} with timeout: {timeout}s")
        try:
            self._wait_for_element_visible(locator_type, value, timeout=timeout)
            logger.debug(f"Mobile element {locator_type.value}={value} is visible.")
            return True
        except TimeoutException:
            logger.debug(f"Mobile element {locator_type.value}={value} not visible within {timeout}s timeout.")
            return False
        except NoSuchElementException:
            logger.debug(f"Mobile element {locator_type.value}={value} not found, thus not visible.")
            return False

    def _wait_for_element_visible(self, locator_type: AppiumBy, value: str, timeout: int = None):
        """
        Waits for a mobile element to be visible on the screen and returns it.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the element.
            timeout (int, optional): Custom timeout. Defaults to global default.

        Returns:
            WebElement: The visible mobile element.

        Raises:
            TimeoutException: If the element is not visible within the timeout.
        """
        logger.debug(f"Waiting for mobile element visibility: {locator_type.value} = {value}")
        try:
            element = self._wait_for(EC.visibility_of_element_located((locator_type, value)), timeout)
            logger.debug(f"Mobile element is visible: {locator_type.value} = {value}")
            return element
        except TimeoutException: # Already logged by _wait_for, re-raise
            raise

    def hide_keyboard(self):
        """Attempts to hide the mobile keyboard if it is currently shown."""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
                logger.info("Keyboard hidden successfully.")
            else:
                logger.debug("Keyboard was not shown, no action taken to hide.")
        except Exception as e:
            # This can fail on some platforms or if no keyboard is shown.
            logger.warning(f"Could not hide keyboard or verify if shown: {e}")
            # Don't fail the test for this, but log it.

    def _swipe(self, start_x, start_y, end_x, end_y, duration_ms=300):
        """Performs a swipe gesture from start to end coordinates."""
        logger.debug(f"Swiping from ({start_x},{start_y}) to ({end_x},{end_y}) duration {duration_ms}ms")
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration_ms)
            logger.info("Swipe action performed.")
        except Exception as e:
            logger.error(f"Swipe action failed: {e}")
            raise

    def _swipe_direction(self, direction: str, distance_percentage: float = 0.5, duration_ms: int = 300):
        """
        Performs a swipe in a given direction (UP, DOWN, LEFT, RIGHT).
        Distance is a percentage of screen height/width.
        """
        size = self.driver.get_window_size()
        width, height = size['width'], size['height']
        
        start_x, start_y, end_x, end_y = 0, 0, 0, 0

        # Define swipe mid-points and distances carefully to avoid edges
        mid_x, mid_y = width / 2, height / 2
        swipe_distance_v = height * distance_percentage
        swipe_distance_h = width * distance_percentage

        direction = direction.upper()
        if direction == "UP": # Swipe up gesture scrolls content down
            start_x, end_x = mid_x, mid_x
            start_y = mid_y + swipe_distance_v / 2
            end_y   = mid_y - swipe_distance_v / 2
        elif direction == "DOWN": # Swipe down gesture scrolls content up
            start_x, end_x = mid_x, mid_x
            start_y = mid_y - swipe_distance_v / 2
            end_y   = mid_y + swipe_distance_v / 2
        elif direction == "LEFT": # Swipe left gesture scrolls content right
            start_y, end_y = mid_y, mid_y
            start_x = mid_x + swipe_distance_h / 2
            end_x   = mid_x - swipe_distance_h / 2
        elif direction == "RIGHT": # Swipe right gesture scrolls content left
            start_y, end_y = mid_y, mid_y
            start_x = mid_x - swipe_distance_h / 2
            end_x   = mid_x + swipe_distance_h / 2
        else:
            raise ValueError(f"Invalid swipe direction: {direction}. Use UP, DOWN, LEFT, or RIGHT.")

        # Ensure coordinates are within screen bounds
        start_x, start_y = max(0, start_x), max(0, start_y)
        end_x, end_y = max(0, end_x), max(0, end_y)
        start_x, end_x = min(width - 1, start_x), min(width - 1, end_x)
        start_y, end_y = min(height - 1, start_y), min(height - 1, end_y)
        
        self._swipe(int(start_x), int(start_y), int(end_x), int(end_y), duration_ms)

    def _scroll_to_element(self, locator_type: AppiumBy, value: str, direction: str = "UP", max_swipes: int = 10):
        """
        Scrolls/swipes in a given direction until an element is visible or max swipes reached.
        'UP' swipe scrolls content Down. 'DOWN' swipe scrolls content Up.

        Args:
            locator_type (AppiumBy): The Appium locator strategy.
            value (str): The locator value for the element.
            direction (str): Swipe direction ('UP', 'DOWN', 'LEFT', 'RIGHT'). Default is 'UP' (scrolls down).
            max_swipes (int): Maximum number of swipes to perform.

        Returns:
            WebElement: The found visible element.

        Raises:
            NoSuchElementException: If the element is not found after max_swipes.
        """
        logger.debug(f"Attempting to scroll to element {locator_type.value}={value} by swiping {direction}.")
        for _ in range(max_swipes):
            try:
                # Attempt to find the element with a short timeout (e.g., 1-2 seconds)
                # If it's found and visible, no need to scroll further.
                element = self._wait_for_element_visible(locator_type, value, timeout=2)
                if element.is_displayed(): # Redundant if _wait_for_element_visible works correctly
                    logger.info(f"Element {locator_type.value}={value} found and visible.")
                    return element
            except (TimeoutException, NoSuchElementException):
                # Element not yet visible, perform a swipe
                logger.debug(f"Element not visible, performing swipe {direction}.")
                self._swipe_direction(direction)
                time.sleep(0.5) # Brief pause after swipe to allow UI to settle
            except Exception as e:
                logger.error(f"Unexpected error during scroll_to_element: {e}")
                break # Stop on unexpected errors

        # If loop finishes without finding the element
        logger.error(f"Element {locator_type.value}={value} not found after {max_swipes} swipes in direction {direction}.")
        raise NoSuchElementException(f"Element {locator_type.value}={value} not found after scrolling.")

```