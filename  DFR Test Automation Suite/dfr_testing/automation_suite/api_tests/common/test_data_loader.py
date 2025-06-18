```python
import json
from pathlib import Path
from dfr.testing.automation.config import global_config
from dfr.testing.automation.utils.logger_setup import setup_logger

logger = setup_logger(__name__)

class ApiTestDataLoader:
    """
    Utility for loading test data from JSON files for API tests.
    Caches data to avoid repeated file reads during a test session.
    """
    _test_data_cache: dict = {}

    @staticmethod
    def _load_json_file(file_path: Path) -> dict:
        """
        Loads data from a JSON file and caches it.

        Args:
            file_path (Path): The path to the JSON file.

        Returns:
            dict: The loaded JSON data.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file content is not valid JSON.
            Exception: For other unexpected errors during file loading.
        """
        file_key = str(file_path.resolve()) # Use resolved path as cache key
        if file_key in ApiTestDataLoader._test_data_cache:
            logger.debug(f"Using cached test data from: {file_key}")
            return ApiTestDataLoader._test_data_cache[file_key]

        logger.debug(f"Loading test data from: {file_key}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ApiTestDataLoader._test_data_cache[file_key] = data
                logger.debug(f"Successfully loaded and cached test data from: {file_key}")
                return data
        except FileNotFoundError:
            logger.error(f"Test data file not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading test data from {file_path}: {e}")
            raise

    @staticmethod
    def get_data(file_name: str, scenario_key: str = None):
        """
        Loads data from a specified JSON file within the API test data directory.
        If `scenario_key` is provided, returns the data associated with that key from the loaded JSON.
        Otherwise, returns the entire content of the JSON file.

        Args:
            file_name (str): The name of the JSON file (e.g., "farmer_creation_data.json").
            scenario_key (str, optional): The key within the JSON file for a specific scenario.

        Returns:
            dict | list | any: The loaded data or data for a specific scenario. The type depends on JSON structure.

        Raises:
            FileNotFoundError: If the data file does not exist.
            json.JSONDecodeError: If the file content is not valid JSON.
            KeyError: If `scenario_key` is provided but not found in the JSON data.
        """
        if not file_name.endswith(".json"):
            logger.warning(f"File name '{file_name}' does not end with .json. Appending .json extension.")
            file_name += ".json"
            
        file_path = global_config.API_TEST_DATA_PATH / file_name
        data_content = ApiTestDataLoader._load_json_file(file_path)

        if scenario_key:
            if isinstance(data_content, dict) and scenario_key in data_content:
                logger.debug(f"Returning data for scenario '{scenario_key}' from {file_name}")
                return data_content[scenario_key]
            else:
                logger.error(f"Scenario key '{scenario_key}' not found in {file_name}, or data is not a dictionary.")
                raise KeyError(f"Scenario key '{scenario_key}' not found in {file_name} or root JSON is not a dict.")
        
        logger.debug(f"Returning all data from {file_name}")
        return data_content

    @staticmethod
    def get_farmer_creation_data(scenario: str = "valid_default_farmer"):
        """
        Helper method to get farmer creation data for a specific scenario.
        Defaults to "valid_default_farmer" scenario from "farmer_creation_data.json".

        Args:
            scenario (str): The scenario key for farmer creation data.

        Returns:
            dict: Farmer creation data for the specified scenario.
        """
        return ApiTestDataLoader.get_data("farmer_creation_data.json", scenario)

    @staticmethod
    def get_farmer_lookup_data(scenario: str):
        """
        Helper method to get farmer lookup parameters or expected data.

        Args:
            scenario (str): The scenario key for farmer lookup data.

        Returns:
            dict: Farmer lookup data for the specified scenario.
        """
        return ApiTestDataLoader.get_data("farmer_lookup_data.json", scenario)

    @staticmethod
    def get_farmer_lookup_perf_data(scenario: str):
        """
        Helper method to get data for farmer lookup performance tests,
        e.g., a list of UIDs.

        Args:
            scenario (str): The scenario key for performance test data.

        Returns:
            list | dict: Data for performance testing.
        """
        return ApiTestDataLoader.get_data("farmer_lookup_perf_data.json", scenario)

    # Add more specific helper methods for other data files or scenarios as needed
    # Example:
    # @staticmethod
    # def get_household_data(scenario: str):
    #     return ApiTestDataLoader.get_data("household_data.json", scenario)

    @staticmethod
    def clear_cache():
        """Clears the internal test data cache. Useful for specific test scenarios or between test runs."""
        ApiTestDataLoader._test_data_cache.clear()
        logger.info("Cleared ApiTestDataLoader cache.")
```