# -*- coding: utf-8 -*-
import json
import werkzeug
from odoo.http import Response

class ApiHelper:

    @staticmethod
    def _json_response(data, status_code=200):
        """Helper to create a JSON response."""
        return Response(
            json.dumps(data),
            content_type='application/json;charset=utf-8',
            status=status_code
        )

    @staticmethod
    def format_success_response(data=None, message=None, status_code=200, http_headers=None):
        response_data = {'success': True}
        if message:
            response_data['message'] = message
        if data is not None: # Allow data to be None, empty list, etc.
            response_data['data'] = data
        
        # http_headers are not directly used with odoo.http.Response constructor in this way.
        # Custom headers would typically be added to the Response object after creation if needed,
        # but for simple JSON responses, content_type and status are the primary concerns.
        return ApiHelper._json_response(response_data, status_code=status_code)


    @staticmethod
    def format_error_response(error_code, error_message, status_code, details=None, http_headers=None):
        error_payload = {
            'code': error_code,
            'message': error_message,
        }
        if details:
            error_payload['details'] = details
        
        response_data = {
            'success': False,
            'error': error_payload
        }
        return ApiHelper._json_response(response_data, status_code=status_code)

    @staticmethod
    def validate_request_payload(payload, schema_validator_func):
        """
        Validates a payload against a given schema validation function.
        schema_validator_func should be a function that takes payload and returns (is_valid, errors_dict).
        Example schema libs: Cerberus, Marshmallow, jsonschema
        """
        # This is a placeholder. Actual implementation would depend on the chosen validation library.
        # For example, if using jsonschema:
        # try:
        #     jsonschema.validate(instance=payload, schema=schema_validator_func) # schema_validator_func would be the schema dict
        #     return True, {}
        # except jsonschema.exceptions.ValidationError as err:
        #     return False, {"message": err.message, "path": list(err.path)}
        # except Exception as e:
        #     return False, {"error": "Validation error", "details": str(e)}

        if schema_validator_func: # pragma: no cover
            is_valid, errors = schema_validator_func(payload)
            return is_valid, errors
        return True, {} # Default to true if no validator provided (not recommended for production)