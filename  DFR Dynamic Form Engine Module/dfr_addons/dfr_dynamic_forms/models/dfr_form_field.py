# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DfrFormField(models.Model):
    _name = 'dfr.form.field'
    _description = 'Dynamic Form Field'
    _order = 'sequence, id'

    form_version_id = fields.Many2one(
        comodel_name='dfr.form.version',
        string=_("Form Version"),
        required=True,
        ondelete='cascade'
    )
    name = fields.Char(
        string=_("Technical Name"),
        required=True,
        help=_("Technical name for the field (e.g., 'farmer_age', 'crop_type'). "
               "Must be unique within a form version. Used for data storage and logic.")
    )
    label = fields.Char(
        string=_("Label"),
        required=True,
        translate=True
    )
    field_type = fields.Selection(
        selection=[
            ('text', _('Text')),
            ('number', _('Number')),
            ('date', _('Date')),
            ('datetime', _('Datetime')),
            ('selection', _('Selection (Dropdown)')),
            ('multi_selection', _('Multi-Selection (Tags)')),
            ('boolean', _('Boolean (Checkbox)')),
            ('gps_point', _('GPS Point (Latitude, Longitude)')),
            ('image', _('Image/File Attachment')),
            ('computed_text', _('Computed Text (Read-only)'))
        ],
        required=True,
        default='text',
        string=_("Field Type")
    )
    sequence = fields.Integer(
        default=10,
        string=_("Sequence")
    )
    is_required = fields.Boolean(
        default=False,
        string=_("Is Required (Form Level)"),
        help=_("Simple 'required' flag for UI indication. More complex validation via rules.")
    )
    help_text = fields.Text(
        string=_("Help Text"),
        translate=True
    )
    selection_options = fields.Text(
        string=_("Selection Options"),
        help=_("For 'selection'/'multi_selection' types. One option per line in format 'value:Label'. "
               "Example: 'opt1:Option 1\\nopt2:Option 2'. The 'value' part is stored.")
    )
    validation_rule_required = fields.Boolean(
        string=_("Validation: Is Required")
    )
    validation_rule_min_length = fields.Integer(
        string=_("Validation: Min Length")
    )
    validation_rule_max_length = fields.Integer(
        string=_("Validation: Max Length")
    )
    validation_rule_min_value = fields.Float(
        string=_("Validation: Min Value")
    )
    validation_rule_max_value = fields.Float(
        string=_("Validation: Max Value")
    )
    validation_rule_regex = fields.Char(
        string=_("Validation: Regex Pattern")
    )
    validation_error_message = fields.Char(
        string=_("Custom Validation Error Message"),
        translate=True
    )
    conditional_logic_json = fields.Text(
        string=_("Conditional Logic (JSON)"),
        help=_("JSON defining conditions to show/hide this field. Example: "
               "[{'field_name': 'other_field_technical_name', 'operator': '=', 'value': 'some_value', 'value_type': 'text'}] "
               "where value_type can be 'text', 'number', 'boolean'. Other operators: '!=', '>', '<', '>=', '<='.")
    )
    placeholder = fields.Char(
        string=_("Placeholder"),
        translate=True
    )
    default_value_text = fields.Char(string=_("Default Text Value"))
    default_value_number = fields.Float(string=_("Default Number Value"))
    default_value_boolean = fields.Boolean(string=_("Default Boolean Value"))
    # Note: Default values for date, datetime, selection, multi_selection, gps, image might need
    # different field types or a more complex handling mechanism if strict type validation for defaults is needed.
    # For now, text, number, boolean are directly supported as per SDS.

    _sql_constraints = [
        ('unique_name_per_form_version', 'UNIQUE(form_version_id, name)',
         _('The technical name of a field must be unique per form version.'))
    ]

    def get_selection_options_parsed(self):
        self.ensure_one()
        options = []
        if self.field_type in ['selection', 'multi_selection'] and self.selection_options:
            lines = self.selection_options.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':', 1)
                if len(parts) == 2:
                    value, label = parts[0].strip(), parts[1].strip()
                    if value: # Value must not be empty
                        options.append((value, label))
                else:
                    # If no colon, use the line as both value and label
                    options.append((line, line))
        return options

    @api.constrains('conditional_logic_json')
    def _validate_conditional_logic_json(self):
        for field_record in self:
            if field_record.conditional_logic_json:
                try:
                    logic_data = json.loads(field_record.conditional_logic_json)
                    if not isinstance(logic_data, list):
                        raise ValidationError(_("Conditional logic JSON must be a list of conditions."))
                    for condition in logic_data:
                        if not isinstance(condition, dict):
                            raise ValidationError(_("Each condition in the JSON list must be a dictionary."))
                        required_keys = ['field_name', 'operator', 'value'] # 'value_type' is good practice but not strictly enforced here
                        if not all(key in condition for key in required_keys):
                            raise ValidationError(
                                _("Each condition must contain 'field_name', 'operator', and 'value' keys. Found: %s", condition.keys())
                            )
                        # Further validation of operator, value_type could be added.
                        # e.g. check if condition['field_name'] exists in the same form version
                except json.JSONDecodeError as e:
                    raise ValidationError(_("Invalid JSON format for Conditional Logic: %s", e))
                except ValidationError: # Re-raise Odoo's validation errors
                    raise
                except Exception as e: # Catch other potential errors during parsing
                     _logger.error("Error validating conditional_logic_json for field %s: %s", field_record.name, e)
                     raise ValidationError(_("Error processing Conditional Logic JSON: %s", e))

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if record.name and not record.name.isidentifier():
                raise ValidationError(
                    _("The technical name '%s' is not a valid Python identifier. "
                      "Please use only letters, numbers, and underscores, and do not start with a number.", record.name)
                )

    @api.constrains(
        'validation_rule_min_length', 'validation_rule_max_length',
        'validation_rule_min_value', 'validation_rule_max_value'
    )
    def _check_validation_rules(self):
        for record in self:
            if record.validation_rule_min_length and record.validation_rule_min_length < 0:
                raise ValidationError(_("Min Length cannot be negative."))
            if record.validation_rule_max_length and record.validation_rule_max_length < 0:
                raise ValidationError(_("Max Length cannot be negative."))
            if record.validation_rule_min_length and record.validation_rule_max_length and \
               record.validation_rule_min_length > record.validation_rule_max_length:
                raise ValidationError(_("Min Length cannot be greater than Max Length."))
            if record.validation_rule_min_value is not False and \
               record.validation_rule_max_value is not False and \
               record.validation_rule_min_value > record.validation_rule_max_value:
                raise ValidationError(_("Min Value cannot be greater than Max Value."))