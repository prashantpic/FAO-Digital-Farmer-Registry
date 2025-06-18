```python
import os
import datetime
from dfr.testing.automation.config import global_config
from dfr.testing.automation.utils.logger_setup import setup_logger
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver # Type hint
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver # Type hint

logger = setup_logger(__name__)

# Ensure screenshot directory exists
global_config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def capture_screenshot_selenium(driver: SeleniumWebDriver, test_name: str):
    """
    Captures a screenshot using Selenium WebDriver and saves it.
    File name includes a timestamp.

    Args:
        driver (SeleniumWebDriver): The Selenium WebDriver instance.
        test_name (str): A descriptive name for the test or context of the screenshot.

    Returns:
        str | None: The absolute path to the saved screenshot file, or None if capture failed.
    """
    if not driver:
        logger.error(f"WebDriver instance is None. Cannot capture screenshot for {test_name}.")
        return None
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3] # Include milliseconds
        file_name = f"{test_name}_{timestamp}.png"
        screenshot_path = global_config.SCREENSHOTS_DIR / file_name
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot captured: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to capture Selenium screenshot for {test_name}: {e}")
        return None

def capture_screenshot_appium(driver: AppiumWebDriver, test_name: str):
    """
    Captures a screenshot using Appium WebDriver and saves it.
    File name includes a timestamp.

    Args:
        driver (AppiumWebDriver): The Appium WebDriver instance.
        test_name (str): A descriptive name for the test or context of the screenshot.

    Returns:
        str | None: The absolute path to the saved screenshot file, or None if capture failed.
    """
    if not driver:
        logger.error(f"AppiumDriver instance is None. Cannot capture screenshot for {test_name}.")
        return None
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3] # Include milliseconds
        file_name = f"{test_name}_{timestamp}.png"
        screenshot_path = global_config.SCREENSHOTS_DIR / file_name
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot captured: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to capture Appium screenshot for {test_name}: {e}")
        return None

def log_test_result_to_file(test_name: str, status: str, message: str = None, duration: float = None, screenshot_path: str = None):
    """
    Logs detailed test results to a custom CSV file in the reports directory.
    This is an illustrative custom logging mechanism; PyTest's built-in reporting
    (e.g., pytest-html) is generally preferred for comprehensive reports.

    Args:
        test_name (str): The name of the test case.
        status (str): The status of the test (e.g., "PASSED", "FAILED", "SKIPPED").
        message (str, optional): Any relevant message or error details.
        duration (float, optional): The duration of the test in seconds.
        screenshot_path (str, optional): Path to a captured screenshot if any.
    """
    custom_report_file = global_config.REPORTS_DIR / "custom_test_results.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    duration_str = f"{duration:.2f}s" if duration is not None else "N/A"
    message_str = message.replace('"', '""') if message is not None else "" # Escape quotes for CSV
    screenshot_str = screenshot_path or "N/A"
    
    header = "Timestamp,TestName,Status,Duration,Message,Screenshot\n"
    
    # Ensure reports directory exists (global_config should have handled this, but double check)
    global_config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        file_exists = custom_report_file.exists()
        # Write header only if file is new or empty
        if not file_exists or custom_report_file.stat().st_size == 0:
            with open(custom_report_file, "w", encoding='utf-8') as f:
                f.write(header)
        
        # Append the new result
        with open(custom_report_file, "a", encoding='utf-8') as f:
            f.write(f'"{timestamp}","{test_name}","{status}","{duration_str}","{message_str}","{screenshot_str}"\n')
        logger.info(f"Logged custom result for {test_name}: {status} to {custom_report_file}")
    except IOError as e:
        logger.error(f"Failed to write custom test result to {custom_report_file}: {e}")

# Other potential functions:
# - update_test_management_tool(test_case_id, status, comments)
#   (This would require integration with a specific test management tool's API)
```