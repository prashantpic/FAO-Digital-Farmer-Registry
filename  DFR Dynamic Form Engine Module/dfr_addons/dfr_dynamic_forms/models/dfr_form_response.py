# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class DfrFormResponse(models.Model):
    _name = 'dfr.form.response'
    _description = 'Dynamic Form Response'
    _order = 'submission_id, field_id' # Or sequence of field_id

    submission_id = fields.Many2one(
        comodel_name='dfr.form.submission',
        string=_("Submission"),
        required=True,
        ondelete='cascade',
        index=True
    )
    field_id = fields.Many2one(
        comodel_name='dfr.form.field',
        string=_("Form Field"),
        required=True,
        ondelete='restrict', # Keep response even if field is somehow deleted (though fields are part of version)
        index=True
    )
    field_label = fields.Char(
        related='field_id.label',
        string=_("Field Label"),
        readonly=True,
        store=True # Denormalized for reporting
    )
    field_type = fields.Selection(
        related='field_id.field_type',
        string=_("Field Type"),
        readonly=True,
        store=True # Denormalized for reporting and value interpretation
    )

    # Value fields - only one should be populated based on field_type
    value_text = fields.Text(string=_("Text Value"))
    value_number = fields.Float(string=_("Number Value"), digits=(16, 4)) # SDS specified (16,4)
    value_date = fields.Date(string=_("Date Value"))
    value_datetime = fields.Datetime(string=_("Datetime Value"))
    value_boolean = fields.Boolean(string=_("Boolean Value"))
    value_selection = fields.Char(string=_("Selection Value (Key)")) # Stores the key

    value_multi_selection_ids = fields.Many2many(
        comodel_name='dfr.form.selection.option.answer',
        relation='dfr_form_response_selection_option_rel',
        column1='response_id',
        column2='option_id',
        string=_("Multi-Selection Values")
    )

    value_gps_latitude = fields.Float(string=_("GPS Latitude"), digits=(10, 7)) # SDS specified (10,7)
    value_gps_longitude = fields.Float(string=_("GPS Longitude"), digits=(10, 7)) # SDS specified (10,7)

    # Attachment handling: SDS prefers ir.attachment
    # value_attachment_name = fields.Char(string=_("Attachment Name")) # Kept from SDS, but usually ir.attachment.name is used
    # value_attachment_data = fields.Binary(string=_("Attachment Data")) # Kept from SDS
    value_attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        string=_("Attachment Value"),
        ondelete='restrict' # Or set null depending on policy
    )

    def get_display_value(self):
        """
        Returns a human-readable representation of the response value.
        """
        self.ensure_one()
        value = ""
        field_type = self.field_type

        if field_type == 'text':
            value = self.value_text or ""
        elif field_type == 'number':
            value = str(self.value_number) if self.value_number is not None else ""
        elif field_type == 'date':
            value = fields.Date.to_string(self.value_date) if self.value_date else ""
        elif field_type == 'datetime':
            value = fields.Datetime.to_string(self.value_datetime) if self.value_datetime else ""
        elif field_type == 'boolean':
            value = _("Yes") if self.value_boolean else _("No")
        elif field_type == 'selection':
            if self.value_selection and self.field_id:
                options = self.field_id.get_selection_options_parsed()
                option_label = next((label for val, label in options if val == self.value_selection), self.value_selection)
                value = option_label
            else:
                value = self.value_selection or ""
        elif field_type == 'multi_selection':
            value = ", ".join(self.value_multi_selection_ids.mapped('display_name'))
        elif field_type == 'gps_point':
            if self.value_gps_latitude is not None and self.value_gps_longitude is not None:
                value = f"Lat: {self.value_gps_latitude}, Lon: {self.value_gps_longitude}"
            else:
                value = ""
        elif field_type == 'image': # or file attachment
            if self.value_attachment_id:
                value = self.value_attachment_id.name or _("Attachment")
            # elif self.value_attachment_name: # Fallback if direct binary was used
            #     value = self.value_attachment_name
            else:
                value = _("No attachment")
        elif field_type == 'computed_text':
            # This would require actual computation logic, perhaps based on other fields
            # For now, just display stored text value
            value = self.value_text or _("[Computed Value Not Available]")
        else:
            value = _("N/A")

        return value

    @api.constrains(
        'value_text', 'value_number', 'value_date', 'value_datetime', 'value_boolean',
        'value_selection', 'value_multi_selection_ids',
        'value_gps_latitude', 'value_gps_longitude', 'value_attachment_id'
    )
    def _check_value_type_consistency(self):
        """
        Ensures that only the correct value_* field is populated based on field_type.
        This is more of a data integrity check during development/direct manipulation.
        Service layer should handle correct population.
        """
        for response in self:
            populated_fields_count = 0
            # Define which value fields are expected for each field type
            type_to_value_field_map = {
                'text': ['value_text'],
                'number': ['value_number'],
                'date': ['value_date'],
                'datetime': ['value_datetime'],
                'boolean': ['value_boolean'], # value_boolean is always True or False, so it's always "populated"
                'selection': ['value_selection'],
                'multi_selection': ['value_multi_selection_ids'], # M2M can be empty, so presence is enough
                'gps_point': ['value_gps_latitude', 'value_gps_longitude'], # Both or none
                'image': ['value_attachment_id'],
                'computed_text': ['value_text'], # Stored as text
            }

            expected_value_fields = type_to_value_field_map.get(response.field_type, [])

            all_value_fields_attrs = [
                'value_text', 'value_number', 'value_date', 'value_datetime',
                'value_boolean', 'value_selection', 'value_multi_selection_ids',
                'value_gps_latitude', 'value_gps_longitude', 'value_attachment_id'
            ]

            for attr_name in all_value_fields_attrs:
                val = getattr(response, attr_name)
                is_populated = False
                if isinstance(val, models.BaseModel): # Many2many or Many2one
                    is_populated = bool(val)
                elif isinstance(val, bool): # Boolean fields are always considered "populated" in a sense
                    # We only care if other non-boolean value fields are set when field_type is boolean
                    pass # Don't count boolean itself unless it's the expected type
                else: # Char, Text, Float, Date, Datetime
                    is_populated = bool(val)


                if is_populated:
                    if response.field_type == 'boolean' and attr_name == 'value_boolean':
                        # This is fine, boolean field has boolean value
                        pass
                    elif attr_name not in expected_value_fields:
                        _logger.warning(
                            "Response ID %s for field '%s' (type %s) has an unexpected value in '%s'.",
                            response.id, response.field_id.name, response.field_type, attr_name
                        )
                        # raise ValidationError(_(
                        #     "Field '%s' of type '%s' has an inconsistent value stored in '%s'.",
                        #     response.field_label, response.field_type, attr_name
                        # )) # This might be too strict for existing data or edge cases
            
            # Special check for GPS: both lat and lon should be present or both absent
            if response.field_type == 'gps_point':
                if (response.value_gps_latitude is not None and response.value_gps_longitude is None) or \
                   (response.value_gps_latitude is None and response.value_gps_longitude is not None):
                    _logger.warning(
                        "Response ID %s for GPS field '%s' has inconsistent latitude/longitude values.",
                        response.id, response.field_id.name
                    )
                    # raise ValidationError(_(
                    #    "For GPS fields, both latitude and longitude must be provided, or neither."
                    # ))
    
    @api.model
    def _get_selection_label(self, field_technical_name, option_value, form_version_id):
        """
        Helper to get display label for a selection option.
        This is more for external use or reporting if needed, get_display_value is for internal.
        """
        if not form_version_id or not field_technical_name or not option_value:
            return option_value

        field_model = self.env['dfr.form.field']
        domain = [
            ('form_version_id', '=', form_version_id),
            ('name', '=', field_technical_name),
            ('field_type', 'in', ['selection', 'multi_selection'])
        ]
        target_field = field_model.search(domain, limit=1)
        
        if target_field:
            options = target_field.get_selection_options_parsed()
            for val, label in options:
                if val == option_value:
                    return label
        return option_value