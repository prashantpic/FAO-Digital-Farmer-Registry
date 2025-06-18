```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from dfr.testing.automation.e2e_tests_web.common.page_objects.base_page import BasePage
# from .admin_login_page import AdminLoginPage # Example if login is prerequisite from another PO
from dfr.testing.automation.utils.logger_setup import setup_logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = setup_logger(__name__)

class FarmerManagementPage(BasePage):
    """
    Page Object Model for the Farmer Management page in the DFR Admin Portal.
    Assumes an Odoo-like backend for the Admin Portal. Locators are examples
    and need to be verified and updated based on the actual DFR Admin Portal HTML structure.
    """

    # --- Locators ---
    # These are illustrative and highly dependent on Odoo's version and DFR customizations.
    # It's crucial to use stable and unique locators.
    
    # General Page Elements (Odoo specific examples)
    _URL_PATH_FRAGMENT_LIST = "/web#model=dfr.farmer&view_type=list" # Example, needs correct model and action
    _URL_PATH_FRAGMENT_FORM = "/web#model=dfr.farmer&view_type=form" # Example
    _PAGE_TITLE_IDENTIFIER = "Farmers" # Part of the title or a header element text

    # Buttons in List View
    _CREATE_BUTTON_LIST_VIEW = (By.XPATH, "//button[contains(@class, 'o_list_button_add') and normalize-space(text())='Create']") # Common Odoo create button

    # Search elements in List View
    _SEARCH_INPUT_LIST_VIEW = (By.XPATH, "//input[contains(@class, 'o_searchview_input')]")
    _SEARCH_VIEW_FACET_CLOSE = (By.XPATH, "//div[contains(@class, 'o_facet_values')]//span[contains(@class, 'o_facet_remove')]") # To clear search terms

    # Farmer List Table (Odoo specific example)
    _FARMER_LIST_TABLE = (By.XPATH, "//table[contains(@class, 'o_list_view')]")
    _FARMER_LIST_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'o_list_view')]/tbody/tr[not(contains(@class, 'o_list_renderer_empty_row'))]") # Rows with data

    # Form View Elements (when creating or editing a farmer)
    _FORM_VIEW_CONTAINER = (By.CLASS_NAME, "o_form_view") # Common Odoo form view container
    _FARMER_NAME_INPUT_FORM = (By.XPATH, "//div[contains(@class, 'o_field_char') and .//label[contains(text(),'Name') or contains(text(),'Full Name')]]//input[@type='text']") # More robust example
    _FARMER_UID_INPUT_FORM = (By.XPATH, "//div[contains(@class, 'o_field_char') and .//label[contains(text(),'UID')]]//input[@type='text']") # Example for UID field
    # Add locators for other fields: date_of_birth, sex, contact_phone, national_id_type, national_id_number, village, etc.
    # E.g., _DATE_OF_BIRTH_INPUT_FORM = (By.NAME, "date_of_birth") # Depends on field name/ID
    _SAVE_BUTTON_FORM = (By.XPATH, "//button[contains(@class, 'o_form_button_save') and normalize-space(text())='Save']")
    _DISCARD_BUTTON_FORM = (By.XPATH, "//button[contains(@class, 'o_form_button_cancel') and normalize-space(text())='Discard']") # Odoo discard

    # Notification / Message Elements (Odoo specific example)
    _NOTIFICATION_MANAGER = (By.CLASS_NAME, "o_notification_manager")
    _SUCCESS_NOTIFICATION = (By.XPATH, "//div[contains(@class, 'o_notification_success')]//span") # More specific to text
    _ERROR_NOTIFICATION = (By.XPATH, "//div[contains(@class, 'o_notification_danger')]//span")


    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        logger.debug("FarmerManagementPage initialized.")

    def navigate_to_farmer_list(self, admin_base_url: str):
        """Navigates to the farmer list view."""
        # Construct the full URL. This might require knowing the specific Odoo action ID.
        # For simplicity, using a common pattern. Replace with actual navigation if needed.
        # Example: admin_base_url + "/web#action=YOUR_ACTION_ID&model=dfr.farmer&view_type=list"
        target_url = f"{admin_base_url}{self._URL_PATH_FRAGMENT_LIST}" 
        logger.info(f"Navigating to Farmer List page: {target_url}")
        self.driver.get(target_url)
        self._wait_for_element_visible(self._CREATE_BUTTON_LIST_VIEW, timeout=20) # Wait for a key element
        logger.info("Farmer List page loaded.")

    def click_add_farmer_button(self):
        """Clicks the 'Add Farmer' or 'Create' button to open the new farmer form."""
        logger.info("Clicking 'Create' button on Farmer List view.")
        self._click(self._CREATE_BUTTON_LIST_VIEW)
        self._wait_for_element_visible(self._FORM_VIEW_CONTAINER, timeout=15) # Wait for form to appear
        logger.info("New Farmer form loaded.")

    def enter_farmer_name(self, name: str):
        """Enters the farmer's full name on the form."""
        logger.info(f"Entering farmer name: {name}")
        self._type_text(self._FARMER_NAME_INPUT_FORM, name)

    def enter_farmer_uid(self, uid: str):
        """Enters the farmer's UID on the form."""
        logger.info(f"Entering farmer UID: {uid}")
        self._type_text(self._FARMER_UID_INPUT_FORM, uid)

    # Add more methods for other fields based on the DFR Admin Portal form:
    # def enter_date_of_birth(self, dob: str): self._type_text(self._DATE_OF_BIRTH_INPUT_FORM, dob)
    # def select_sex(self, sex: str): # This might involve clicking a dropdown then an option
    # def enter_contact_phone(self, phone: str): ...
    # etc.

    def click_save_farmer_button(self):
        """Clicks the 'Save' button on the farmer form."""
        logger.info("Clicking 'Save' button on Farmer form.")
        self._click(self._SAVE_BUTTON_FORM)
        # Add a wait for the save operation to complete.
        # This could be waiting for a success notification, or for the view to change (e.g., back to list or form in read-only).
        # Example: Wait for a success notification (if applicable and reliable)
        try:
            self._wait_for_element_visible(self._SUCCESS_NOTIFICATION, timeout=10)
            logger.info("Save successful (notification detected).")
        except (TimeoutException, NoSuchElementException):
            logger.warning("No immediate success notification detected after save. "
                           "Further verification might be needed based on view change.")
            # Alternative: wait for URL change or for the form to become non-editable.

    def search_farmer(self, search_term: str):
        """Enters a search term in the list view search box and submits."""
        logger.info(f"Searching for farmer: {search_term}")
        # Clear existing search facets if any (Odoo specific behavior)
        try:
            close_facet_buttons = self._find_elements(self._SEARCH_VIEW_FACET_CLOSE, timeout=2)
            for button in close_facet_buttons:
                button.click()
                logger.debug("Cleared a search facet.")
        except (TimeoutException, NoSuchElementException):
            logger.debug("No active search facets to clear.")
            
        self._type_text(self._SEARCH_INPUT_LIST_VIEW, search_term + "\n", clear_first=True) # Append Enter to trigger search
        # Add a wait for search results to load/update.
        # This could be waiting for a loading spinner to disappear or for the number of rows to change.
        # For Odoo, sometimes waiting for the list view to re-render is needed.
        self._wait_for_element_present(self._FARMER_LIST_TABLE, timeout=10) # Wait for table to be present
        logger.info(f"Search submitted for: {search_term}")


    def is_farmer_listed(self, farmer_name_or_uid: str, column_index_for_check: int = 1) -> bool:
        """
        Checks if a farmer is listed in the current list view table.
        Args:
            farmer_name_or_uid (str): The name, UID, or other unique identifier to search for in the cells.
            column_index_for_check (int): The 0-based index of the column to check for the text.
                                          Adjust based on the Odoo view configuration.
        Returns:
            bool: True if the farmer is found, False otherwise.
        """
        logger.info(f"Verifying if '{farmer_name_or_uid}' is listed in column index {column_index_for_check}.")
        try:
            # Wait for rows to be present; use a shorter timeout as search should have completed.
            rows = self._find_elements(self._FARMER_LIST_TABLE_ROWS, timeout=15)
            if not rows:
                logger.warning("No rows found in the farmer list table.")
                return False

            for i, row in enumerate(rows):
                try:
                    # Get all cells in the current row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) > column_index_for_check:
                        cell_text = cells[column_index_for_check].text
                        logger.debug(f"Row {i}, Column {column_index_for_check} text: '{cell_text}'")
                        if farmer_name_or_uid.lower() in cell_text.lower():
                            logger.info(f"Farmer '{farmer_name_or_uid}' found in list at row {i}.")
                            return True
                except StaleElementReferenceException:
                    logger.warning(f"Stale element reference for row {i} cell, re-fetching rows might be needed or skip.")
                    # For simplicity, just continue to the next row or fail if many stale elements.
                    # A more robust solution might re-fetch rows or cells if staleness is frequent.
                except Exception as e:
                    logger.error(f"Error processing row {i} while checking for farmer: {e}")
            
            logger.warning(f"Farmer '{farmer_name_or_uid}' not found in the list.")
            return False
        except TimeoutException:
            logger.warning("Timed out waiting for farmer list rows to appear.")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred in is_farmer_listed: {e}")
            raise # Re-raise unexpected errors

    def get_success_message(self, timeout: int = 10) -> str | None:
        """
        Gets the text of a success notification message if displayed.
        Assumes Odoo's standard notification mechanism.
        Returns the message text or None if not found.
        """
        logger.debug("Attempting to get success notification message.")
        try:
            # Wait for the notification container to be visible, then the success message itself
            self._wait_for_element_visible(self._NOTIFICATION_MANAGER, timeout=timeout)
            message_element = self._find_element(self._SUCCESS_NOTIFICATION, timeout=timeout) # Find within container
            message_text = message_element.text
            logger.info(f"Success notification found: '{message_text}'")
            return message_text
        except (TimeoutException, NoSuchElementException):
            logger.warning("No success notification message found within timeout.")
            return None
        except Exception as e:
            logger.error(f"Error getting success notification: {e}")
            return None
            
    def get_error_message(self, timeout: int = 10) -> str | None:
        """
        Gets the text of an error notification message if displayed.
        Returns the message text or None if not found.
        """
        logger.debug("Attempting to get error notification message.")
        try:
            self._wait_for_element_visible(self._NOTIFICATION_MANAGER, timeout=timeout)
            message_element = self._find_element(self._ERROR_NOTIFICATION, timeout=timeout)
            message_text = message_element.text
            logger.warning(f"Error notification found: '{message_text}'") # Log as warning as it's an error message
            return message_text
        except (TimeoutException, NoSuchElementException):
            logger.info("No error notification message found within timeout.")
            return None
        except Exception as e:
            logger.error(f"Error getting error notification: {e}")
            return None

```