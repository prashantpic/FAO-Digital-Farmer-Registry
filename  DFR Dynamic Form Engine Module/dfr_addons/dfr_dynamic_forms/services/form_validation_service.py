# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re
import json
from odoo import _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, safe_eval

_logger = logging.getLogger(__name__)

class FormValidationService:
    """
    Handles complex validation logic for dynamic form fields.
    """

    def _is_empty(self, value):
        """Checks if a value is considered empty."""
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, (list, tuple, dict)) and not value:
            return True
        return False

    def validate_field_response(self, env, form_field_record, response_value):
        """
        Validates a single field response against its rules.
        :param env: Odoo environment
        :param form_field_record: dfr.form.field recordset (single record)
        :param response_value: The value provided for the field
        :return: tuple (bool, str|None) -> (isValid, error_message_or_None)
        """
        field = form_field_record
        error_msg_key = field.validation_error_message or _("Invalid value for field '%s'.") % field.label

        # 1. Check 'Is Required (Validation)'
        if field.validation_rule_required and self._is_empty(response_value):
            return False, field.validation_error_message or _("Field '%s' is required.") % field.label
        
        # If not required and empty, no further validation needed for this field
        if self._is_empty(response_value):
            return True, None

        # 2. Type-specific validations
        if field.field_type == 'text':
            if not isinstance(response_value, str):
                return False, _("Field '%s' expects a text value.") % field.label
            if field.validation_rule_min_length and len(response_value) < field.validation_rule_min_length:
                return False, field.validation_error_message or _("Field '%s' must be at least %s characters long.") % (field.label, field.validation_rule_min_length)
            if field.validation_rule_max_length and len(response_value) > field.validation_rule_max_length:
                return False, field.validation_error_message or _("Field '%s' must be at most %s characters long.") % (field.label, field.validation_rule_max_length)
        
        elif field.field_type == 'number':
            try:
                num_value = float(response_value)
            except (ValueError, TypeError):
                return False, _("Field '%s' expects a numeric value.") % field.label
            
            if field.validation_rule_min_value is not None and float_compare(num_value, field.validation_rule_min_value, precision_digits=4) < 0:
                return False, field.validation_error_message or _("Field '%s' must be greater than or equal to %s.") % (field.label, field.validation_rule_min_value)
            if field.validation_rule_max_value is not None and float_compare(num_value, field.validation_rule_max_value, precision_digits=4) > 0:
                return False, field.validation_error_message or _("Field '%s' must be less than or equal to %s.") % (field.label, field.validation_rule_max_value)

        elif field.field_type in ('date', 'datetime'):
            # Basic format validation is typically handled by Odoo's field conversion.
            # More complex date range validations could be added here if needed.
            # For now, we assume the value is already in a Odoo-compatible format if it reaches here from ORM/service.
            pass 
        
        elif field.field_type == 'selection':
            valid_options = [opt[0] for opt in field.get_selection_options_parsed()]
            if response_value not in valid_options:
                return False, field.validation_error_message or _("Invalid selection for field '%s'.") % field.label
        
        elif field.field_type == 'multi_selection':
            if not isinstance(response_value, list):
                 return False, _("Field '%s' expects a list of selections.") % field.label
            valid_options = [opt[0] for opt in field.get_selection_options_parsed()]
            for val in response_value:
                if val not in valid_options:
                    return False, field.validation_error_message or _("Invalid selection '%s' for field '%s'.") % (val, field.label)
        
        # GPS Point validation (e.g. range for lat/long) can be added here if needed
        # Image/Attachment validation (e.g. file size, type) can be added here

        # 3. Regex Validation (if applicable and other rules passed)
        if field.validation_rule_regex and isinstance(response_value, str):
            try:
                if not re.match(field.validation_rule_regex, response_value):
                    return False, field.validation_error_message or _("Field '%s' does not match the required pattern.") % field.label
            except re.error as e:
                _logger.error("Invalid regex pattern for field ID %s: %s. Error: %s", field.id, field.validation_rule_regex, e)
                # Potentially raise a system error or return a generic validation failure
                return False, _("Field '%s' has an invalid validation pattern configured. Please contact administrator.") % field.label


        return True, None

    def validate_submission_responses(self, env, form_version_record, responses_dict):
        """
        Validates all responses in a submission.
        :param env: Odoo environment
        :param form_version_record: dfr.form.version recordset (single record)
        :param responses_dict: dict: {field_technical_name: value}
        :return: tuple (bool, dict) -> (all_isValid, errors_dict_by_field_technical_name)
        """
        _logger.debug("Validating submission responses for form version ID %s. Responses: %s",
                      form_version_record.id, responses_dict)
        
        all_valid = True
        errors = {}

        # Check for missing required fields that are not in responses_dict at all
        for field_record in form_version_record.field_ids:
            if field_record.validation_rule_required and field_record.name not in responses_dict:
                 # Check if the field is conditionally hidden
                is_conditionally_visible = self._check_conditional_visibility(env, field_record, responses_dict, form_version_record.field_ids)
                if is_conditionally_visible: # Only required if visible
                    all_valid = False
                    errors[field_record.name] = field_record.validation_error_message or _("Field '%s' is required.") % field_record.label
            
            # If field is present in responses, validate it
            if field_record.name in responses_dict:
                response_value = responses_dict.get(field_record.name)
                
                # Only validate if the field is supposed to be visible based on conditional logic
                is_conditionally_visible = self._check_conditional_visibility(env, field_record, responses_dict, form_version_record.field_ids)
                if not is_conditionally_visible and not field_record.validation_rule_required: # If hidden and not explicitly required, skip its validation
                    continue

                is_field_valid, error_message = self.validate_field_response(env, field_record, response_value)
                if not is_field_valid:
                    all_valid = False
                    errors[field_record.name] = error_message
        
        if not all_valid:
            _logger.warning("Submission validation failed for form version ID %s. Errors: %s",
                            form_version_record.id, errors)
        else:
            _logger.debug("Submission validation successful for form version ID %s.", form_version_record.id)
            
        return all_valid, errors

    def _check_conditional_visibility(self, env, field_to_check, responses_dict, all_fields_in_form):
        """
        Checks if a field should be visible based on its conditional logic and current responses.
        :param env: Odoo environment
        :param field_to_check: dfr.form.field recordset (single record whose visibility is being checked)
        :param responses_dict: dict: {field_technical_name: value} of current responses
        :param all_fields_in_form: recordset of all dfr.form.field in the current form version
        :return: bool (True if visible or no conditions, False if hidden by conditions)
        """
        if not field_to_check.conditional_logic_json:
            return True # No conditions, so it's visible by default

        try:
            conditions = json.loads(field_to_check.conditional_logic_json)
            if not isinstance(conditions, list):
                _logger.error("Conditional logic for field '%s' (ID: %s) is not a list: %s",
                              field_to_check.name, field_to_check.id, field_to_check.conditional_logic_json)
                return True # Treat as visible on error to be safe, or raise configuration error
        except json.JSONDecodeError:
            _logger.error("Invalid JSON in conditional_logic_json for field '%s' (ID: %s): %s",
                          field_to_check.name, field_to_check.id, field_to_check.conditional_logic_json)
            return True # Treat as visible on error


        # For simplicity, assuming conditions are ANDed. Complex OR/AND logic needs more sophisticated parsing.
        # This implementation assumes all conditions in the list must be met for the field to be SHOWN.
        # The SDS says "conditions to show/hide". Let's assume conditions define WHEN TO SHOW.
        # If any condition is not met, the field is hidden.
        
        for condition in conditions:
            trigger_field_name = condition.get('field_name')
            operator = condition.get('operator')
            conditional_value = condition.get('value')
            value_type = condition.get('value_type', 'text') # default to text

            if not all([trigger_field_name, operator, conditional_value is not None]): # value can be False or 0
                _logger.warning("Malformed condition for field '%s': %s. Skipping this condition.",
                                field_to_check.name, condition)
                continue

            trigger_field_response = responses_dict.get(trigger_field_name)
            
            # Find the trigger field to determine its type for proper comparison
            trigger_field_def = all_fields_in_form.filtered(lambda f: f.name == trigger_field_name)
            if not trigger_field_def:
                 _logger.warning("Trigger field '%s' for conditional logic of field '%s' not found. Condition cannot be evaluated.",
                                trigger_field_name, field_to_check.name)
                 return False # If a condition depends on non-existent field, assume it fails


            # Type casting for comparison
            actual_value = trigger_field_response
            expected_value = conditional_value

            if trigger_field_def.field_type == 'number' or value_type == 'number':
                try:
                    actual_value = float(trigger_field_response) if trigger_field_response is not None else None
                    expected_value = float(conditional_value)
                except (ValueError, TypeError): # If conversion fails, condition fails
                    return False
            elif trigger_field_def.field_type == 'boolean' or value_type == 'boolean':
                # Handle string "true"/"false" from JSON and actual boolean from responses
                actual_value = bool(safe_eval(str(trigger_field_response))) if trigger_field_response is not None else None
                expected_value = bool(safe_eval(str(conditional_value)))
            # Dates would need date object comparison
            
            # Evaluate condition
            if actual_value is None: # If trigger field has no value, most conditions won't match positively.
                 if operator == '!=' and expected_value is not None: # '!=' null is true for any non-null expected value
                    pass # Condition met
                 elif operator == '=' and expected_value is None: # '=' null is true
                    pass # Condition met
                 else:
                    return False # Condition not met

            elif operator == '=':
                if actual_value != expected_value: return False
            elif operator == '!=':
                if actual_value == expected_value: return False
            elif operator == '>':
                if not (actual_value > expected_value): return False
            elif operator == '<':
                if not (actual_value < expected_value): return False
            elif operator == '>=':
                if not (actual_value >= expected_value): return False
            elif operator == '<=':
                if not (actual_value <= expected_value): return False
            # Could add 'contains', 'startsWith' etc for text or multi_selection
            else:
                _logger.warning("Unsupported operator '%s' in conditional logic for field '%s'. Condition fails.",
                                operator, field_to_check.name)
                return False # Unknown operator, condition fails

        return True # All conditions met (or no valid conditions found to hide it)