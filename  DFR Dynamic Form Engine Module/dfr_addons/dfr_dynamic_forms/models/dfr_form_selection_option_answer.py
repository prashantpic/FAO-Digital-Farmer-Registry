# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class DfrFormSelectionOptionAnswer(models.Model):
    _name = 'dfr.form.selection.option.answer'
    _description = 'Dynamic Form Selection Option Answer'
    _rec_name = 'display_name' # Or 'name' if display_name is not always set

    name = fields.Char(
        string=_("Option Value (Key)"),
        required=True,
        index=True,
        help=_("The internal key/value of the selection option (e.g., 'opt1').")
    )
    display_name = fields.Char(
        string=_("Option Label"),
        compute='_compute_display_name',
        store=True, # Store for performance if computation is simple or can be set manually
        help=_("The user-friendly label for the option (e.g., 'Option 1').")
    )

    # If this model were to store options globally, we might add a field like:
    # form_field_id = fields.Many2one('dfr.form.field', string="Originating Field", ondelete='cascade')
    # This would allow ensuring uniqueness of 'name' per field_id if desired.
    # However, SDS describes it as a helper for Many2many on dfr.form.response,
    # implying records are created on-the-fly or found based on name/display_name.

    @api.depends('name')
    def _compute_display_name(self):
        """
        Computes the display_name.
        For simplicity, if display_name is not directly set during creation (e.g., from an API
        that provides both key and label), it defaults to the 'name' (key).
        In a more complex scenario, this could try to look up a global label definition
        if 'name' was just a key. But as per SDS, 'display_name' can be set.
        """
        for record in self:
            if not record.display_name: # Only compute if not already set (e.g. by create values)
                record.display_name = record.name


    @api.model
    def _find_or_create_options(self, options_data_list):
        """
        Helper method to find existing options or create new ones.
        :param options_data_list: A list of dictionaries, each with 'name' (key) and 'display_name' (label).
                                  Example: [{'name': 'opt1', 'display_name': 'Option 1'}, ...]
        :return: A list of IDs of dfr.form.selection.option.answer records.
        """
        option_ids = []
        if not options_data_list:
            return option_ids

        existing_options_map = {}
        option_names_to_search = [opt['name'] for opt in options_data_list if 'name' in opt]
        
        if option_names_to_search:
            existing_records = self.search([('name', 'in', list(set(option_names_to_search)))])
            for rec in existing_records:
                existing_options_map[rec.name] = rec.id
        
        options_to_create = []
        for opt_data in options_data_list:
            key = opt_data.get('name')
            label = opt_data.get('display_name', key) # Default label to key if not provided

            if not key:
                _logger.warning("Skipping option data with no 'name' (key): %s", opt_data)
                continue

            if key in existing_options_map:
                option_ids.append(existing_options_map[key])
            else:
                # Check if it was already added to be created to avoid duplicates in this batch
                if not any(o['name'] == key for o in options_to_create):
                    options_to_create.append({'name': key, 'display_name': label})
        
        if options_to_create:
            created_records = self.create(options_to_create)
            option_ids.extend(created_records.ids)
            # Add newly created to map to handle potential duplicates within options_data_list
            for rec in created_records:
                 existing_options_map[rec.name] = rec.id


        # Re-ensure all original options_data_list (with valid keys) are processed
        # This handles cases where options_data_list might have duplicates that were not
        # present in DB but are within the list itself.
        final_option_ids = []
        for opt_data in options_data_list:
            key = opt_data.get('name')
            if key and key in existing_options_map:
                 if existing_options_map[key] not in final_option_ids: # Ensure unique IDs
                    final_option_ids.append(existing_options_map[key])
        
        return final_option_ids