```python
import requests
from jsonschema import validate, exceptions as jsonschema_exceptions
from dfr.testing.automation.utils.logger_setup import setup_logger

logger = setup_logger(__name__)

class ResponseValidator:
    """
    Utility class for validating API responses based on status codes,
    JSON structure (schema), and content. Provides static methods for assertions.
    """

    @staticmethod
    def assert_status_code(response: requests.Response, expected_code: int):
        """
        Asserts that the HTTP status code of the response matches the expected code.
        Provides an informative error message including part of the response body on failure.

        Args:
            response (requests.Response): The response object from an API call.
            expected_code (int): The expected HTTP status code.

        Raises:
            AssertionError: If the actual status code does not match the expected code.
        """
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"Expected status code {expected_code}, but got {actual_code}. " \
            f"URL: {response.request.url}. " \
            f"Response Body: {response.text[:500]}{'...' if len(response.text) > 500 else ''}"
        logger.info(f"Status code assertion passed: Actual {actual_code} == Expected {expected_code} for URL {response.request.url}")

    @staticmethod
    def validate_json_schema(response_json: dict, schema: dict):
        """
        Validates a JSON object (Python dictionary) against a given JSON schema.

        Args:
            response_json (dict): The JSON response body parsed into a Python dictionary.
            schema (dict): The JSON schema dictionary to validate against.

        Raises:
            AssertionError: If the JSON validation fails, containing details from jsonschema.ValidationError.
            jsonschema.exceptions.SchemaError: If the provided schema itself is invalid.
        """
        try:
            validate(instance=response_json, schema=schema)
            logger.info("JSON schema validation passed successfully.")
        except jsonschema_exceptions.ValidationError as e:
            # Provide a more detailed error message for easier debugging
            error_path = " -> ".join(map(str, e.path)) if e.path else "root"
            error_msg = (
                f"JSON schema validation failed: {e.message}\n"
                f"Schema Path: {error_path}\n"
                f"Problematic Instance Snippet: {str(e.instance)[:200]}{'...' if len(str(e.instance)) > 200 else ''}\n"
                f"Validator: {e.validator} = {e.validator_value}\n"
                f"Schema Snippet: {str(e.schema)[:200]}{'...' if len(str(e.schema)) > 200 else ''}"
            )
            logger.error(error_msg)
            raise AssertionError(error_msg)
        except jsonschema_exceptions.SchemaError as e:
            logger.error(f"Invalid JSON schema provided: {e.message}")
            raise # Re-raise schema error as it's a test setup issue

    @staticmethod
    def assert_response_contains_key(response_json: dict, key: str, path: list[str] | None = None):
        """
        Asserts that a specific key exists in the response JSON, optionally at a nested path.

        Args:
            response_json (dict): The JSON response body as a Python dictionary.
            key (str): The key to check for at the specified level.
            path (list[str], optional): A list of strings representing the nested path to the level
                                        where the key should be found. E.g., `['data', 'attributes']`.

        Raises:
            AssertionError: If the key or any key in the path is not found, or if path traversal encounters non-dict types.
        """
        current_level = response_json
        full_path_str = ""
        if path:
            for i, p_key in enumerate(path):
                full_path_str += f"['{p_key}']"
                assert isinstance(current_level, dict), \
                    f"Path element '{p_key}' at index {i} (Path: {full_path_str}) expects a dictionary, but found {type(current_level)}. Response snippet: {str(response_json)[:200]}"
                assert p_key in current_level, \
                    f"Path key '{p_key}' not found in path {full_path_str}. Response snippet: {str(response_json)[:200]}"
                current_level = current_level[p_key]
        
        final_path_str = (full_path_str + f"['{key}']") if full_path_str else f"Key '{key}'"
        assert isinstance(current_level, dict), \
            f"Expected a dictionary at path {full_path_str} to check for key '{key}', but found {type(current_level)}. Response snippet: {str(response_json)[:200]}"
        assert key in current_level, \
            f"{final_path_str} not found in response JSON. Response snippet: {str(response_json)[:200]}"
        logger.info(f"Key '{key}' found in response JSON at path '{full_path_str}'.")

    @staticmethod
    def assert_response_key_value(response_json: dict, key: str, expected_value, path: list[str] | None = None):
        """
        Asserts that a key in the response JSON has an expected value, optionally at a nested path.

        Args:
            response_json (dict): The JSON response body.
            key (str): The key whose value to check.
            expected_value: The expected value of the key.
            path (list[str], optional): Nested path to the key.

        Raises:
            AssertionError: If the key is not found, its value does not match, or path traversal fails.
        """
        ResponseValidator.assert_response_contains_key(response_json, key, path) # First assert existence

        current_level = response_json
        full_path_str = ""
        if path:
            for p_key in path:
                full_path_str += f"['{p_key}']"
                current_level = current_level[p_key]
        
        actual_value = current_level[key]
        final_path_str = (full_path_str + f"['{key}']") if full_path_str else f"Key '{key}'"

        assert actual_value == expected_value, \
            f"Expected value '{expected_value}' for {final_path_str}, but got '{actual_value}'. Response snippet: {str(response_json)[:200]}"
        logger.info(f"Value assertion passed for {final_path_str}: Actual '{actual_value}' == Expected '{expected_value}'.")

    @staticmethod
    def assert_response_is_list_not_empty(response_data: list):
        """
        Asserts that the provided data is a list and is not empty.

        Args:
            response_data (list): The data to check, expected to be a list.

        Raises:
            AssertionError: If the data is not a list or is empty.
        """
        assert isinstance(response_data, list), \
            f"Response data is not a list. Got type: {type(response_data)}. Snippet: {str(response_data)[:200]}"
        assert len(response_data) > 0, \
            f"Response list is empty. Snippet: {str(response_data)[:200]}"
        logger.info(f"Response is a non-empty list with {len(response_data)} items.")

    @staticmethod
    def assert_response_is_empty_list(response_data: list):
        """
        Asserts that the provided data is a list and is empty.

        Args:
            response_data (list): The data to check, expected to be a list.

        Raises:
            AssertionError: If the data is not a list or is not empty.
        """
        assert isinstance(response_data, list), \
            f"Response data is not a list. Got type: {type(response_data)}. Snippet: {str(response_data)[:200]}"
        assert len(response_data) == 0, \
            f"Response list is not empty. It has {len(response_data)} items. Snippet: {str(response_data)[:200]}"
        logger.info("Response is an empty list as expected.")

    # Example JSON Schemas (Illustrative - should be defined based on DFR API specs)
    # These could be loaded from separate .json files or a dedicated schemas module.
    #
    # FARMER_OBJECT_SCHEMA = {
    #     "type": "object",
    #     "properties": {
    #         "uid": {"type": "string", "format": "uuid"},
    #         "fullName": {"type": "string", "minLength": 1},
    #         "dateOfBirth": {"type": ["string", "null"], "format": "date"},
    #         "sex": {"type": ["string", "null"], "enum": ["Male", "Female", "Other", None]},
    #         "contactPhone": {"type": ["string", "null"]}, # Add pattern for phone number
    #         "nationalIdType": {"type": ["string", "null"]},
    #         "nationalIdNumber": {"type": ["string", "null"]},
    #         "village": {"type": ["string", "null"]},
    #         "createdAt": {"type": "string", "format": "date-time"},
    #         "updatedAt": {"type": "string", "format": "date-time"},
    #         "customFields": {"type": ["object", "null"]},
    #         # ... add all other expected fields and their types/constraints
    #     },
    #     "required": ["uid", "fullName", "createdAt", "updatedAt"] # Example required fields
    # }
    #
    # PAGINATED_LIST_SCHEMA = {
    #     "type": "object",
    #     "properties": {
    #         "items": {"type": "array", "items": FARMER_OBJECT_SCHEMA}, # Example for a list of farmers
    #         "totalCount": {"type": "integer", "minimum": 0},
    #         "page": {"type": "integer", "minimum": 1},
    #         "pageSize": {"type": "integer", "minimum": 1},
    #         "totalPages": {"type": "integer", "minimum": 0},
    #     },
    #     "required": ["items", "totalCount", "page", "pageSize", "totalPages"]
    # }
    #
    # API_ERROR_SCHEMA = {
    #     "type": "object",
    #     "properties": {
    #         "timestamp": {"type": "string", "format": "date-time"},
    #         "status": {"type": "integer"},
    #         "error": {"type": "string"},
    #         "message": {"type": "string"},
    #         "path": {"type": "string"},
    #         "details": {"type": ["array", "object", "string", "null"]}, # Can vary
    #     },
    #     "required": ["timestamp", "status", "error", "message", "path"]
    # }
```