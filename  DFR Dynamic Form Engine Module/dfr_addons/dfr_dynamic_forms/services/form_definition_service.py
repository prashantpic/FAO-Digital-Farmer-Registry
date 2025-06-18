# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from odoo import _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class FormDefinitionService:
    """
    Handles business logic for creating, versioning, publishing,
    and retrieving dynamic form definitions.
    """

    def create_form_master(self, env, form_data):
        """
        Creates a new dfr.form record.
        :param env: Odoo environment
        :param form_data: dict: {'name': str, 'description': str, 'country_id': int (optional)}
        :return: dfr.form recordset
        """
        _logger.info("Creating new form master with data: %s", form_data)
        if not form_data.get('name'):
            raise ValidationError(_("Form Title is required."))
        
        form_master = env['dfr.form'].create(form_data)
        _logger.info("Form master created: %s (ID: %s)", form_master.name, form_master.id)
        return form_master

    def create_new_form_version(self, env, form_master_id, version_data=None, source_version_id=None):
        """
        Creates a new dfr.form.version record.
        :param env: Odoo environment
        :param form_master_id: int, ID of the dfr.form master
        :param version_data: dict: {'description': str} optional
        :param source_version_id: int, optional: ID of dfr.form.version to copy fields from
        :return: dfr.form.version recordset
        """
        _logger.info("Creating new form version for master ID %s. Source version ID: %s. Data: %s",
                     form_master_id, source_version_id, version_data)
        
        form_master = env['dfr.form'].browse(form_master_id)
        if not form_master.exists():
            raise UserError(_("Form Master with ID %s not found.") % form_master_id)

        vals = {
            'form_master_id': form_master_id,
            'description': version_data.get('description') if version_data else None,
            'status': 'draft', # New versions always start as draft
        }

        if source_version_id:
            source_version = env['dfr.form.version'].browse(source_version_id)
            if not source_version.exists():
                raise UserError(_("Source Form Version with ID %s not found.") % source_version_id)
            if source_version.form_master_id.id != form_master_id:
                raise UserError(_("Source version does not belong to the specified form master."))
            
            # Use the copy method of form.version which handles field_ids copying
            new_version = source_version.copy(default=vals)
            # The copy method generates a new version_number, ensure description is updated if provided
            if vals.get('description'):
                new_version.description = vals['description']

        else:
            # Create a new version from scratch
            new_version = env['dfr.form.version'].create(vals)
            
        _logger.info("New form version created: %s (ID: %s) for form %s", 
                     new_version.version_number, new_version.id, form_master.name)
        return new_version

    def publish_form_version(self, env, form_version_id):
        """
        Publishes a form version.
        :param env: Odoo environment
        :param form_version_id: int, ID of dfr.form.version
        :return: bool (success)
        """
        _logger.info("Attempting to publish form version ID %s", form_version_id)
        form_version = env['dfr.form.version'].browse(form_version_id)
        if not form_version.exists():
            raise UserError(_("Form Version with ID %s not found.") % form_version_id)

        try:
            form_version.action_publish()
            _logger.info("Form version ID %s published successfully.", form_version_id)
            return True
        except (UserError, ValidationError) as e:
            _logger.error("Failed to publish form version ID %s: %s", form_version_id, e)
            raise
        except Exception as e:
            _logger.exception("An unexpected error occurred while publishing form version ID %s.", form_version_id)
            raise UserError(_("An unexpected error occurred: %s") % str(e))


    def archive_form_version(self, env, form_version_id):
        """
        Archives a form version.
        :param env: Odoo environment
        :param form_version_id: int, ID of dfr.form.version
        :return: bool (success)
        """
        _logger.info("Attempting to archive form version ID %s", form_version_id)
        form_version = env['dfr.form.version'].browse(form_version_id)
        if not form_version.exists():
            raise UserError(_("Form Version with ID %s not found.") % form_version_id)

        try:
            form_version.action_archive()
            _logger.info("Form version ID %s archived successfully.", form_version_id)
            return True
        except (UserError, ValidationError) as e:
            _logger.error("Failed to archive form version ID %s: %s", form_version_id, e)
            raise
        except Exception as e:
            _logger.exception("An unexpected error occurred while archiving form version ID %s.", form_version_id)
            raise UserError(_("An unexpected error occurred: %s") % str(e))

    def get_form_definition_for_rendering(self, env, form_version_id):
        """
        Retrieves a structured representation of the form suitable for rendering clients.
        :param env: Odoo environment
        :param form_version_id: int, ID of dfr.form.version
        :return: dict representing the form structure
        """
        _logger.debug("Getting form definition for rendering, version ID %s", form_version_id)
        form_version = env['dfr.form.version'].browse(form_version_id)
        if not form_version.exists():
            raise UserError(_("Form Version with ID %s not found.") % form_version_id)

        fields_data = []
        for field in form_version.field_ids.sorted(key=lambda f: f.sequence):
            field_dict = {
                'name': field.name,
                'label': field.label,
                'field_type': field.field_type,
                'is_required_form_level': field.is_required, # UI hint
                'help_text': field.help_text,
                'placeholder': field.placeholder,
                'selection_options': field.get_selection_options_parsed(),
                'validation_rules': {
                    'required': field.validation_rule_required,
                    'min_length': field.validation_rule_min_length,
                    'max_length': field.validation_rule_max_length,
                    'min_value': field.validation_rule_min_value,
                    'max_value': field.validation_rule_max_value,
                    'regex': field.validation_rule_regex,
                    'error_message': field.validation_error_message,
                },
                'default_value': None # Consolidate default values
            }
            if field.field_type in ('text', 'selection', 'computed_text'):
                field_dict['default_value'] = field.default_value_text
            elif field.field_type == 'number':
                field_dict['default_value'] = field.default_value_number
            elif field.field_type == 'boolean':
                field_dict['default_value'] = field.default_value_boolean
            # For date, datetime, gps_point, image - default values might need specific handling or not be supported via simple fields.

            try:
                if field.conditional_logic_json:
                    field_dict['conditional_logic'] = json.loads(field.conditional_logic_json)
                else:
                    field_dict['conditional_logic'] = []
            except json.JSONDecodeError:
                _logger.warning("Invalid JSON in conditional_logic_json for field ID %s: %s",
                                field.id, field.conditional_logic_json)
                field_dict['conditional_logic'] = [] # Or handle as an error for the specific field
            
            fields_data.append(field_dict)

        form_definition = {
            'form_name': form_version.name, # Related from form_master
            'form_version': form_version.version_number,
            'form_version_id': form_version.id,
            'form_master_id': form_version.form_master_id.id,
            'status': form_version.status,
            'fields': fields_data,
        }
        _logger.debug("Form definition for version ID %s retrieved successfully.", form_version_id)
        return form_definition

    def add_field_to_version(self, env, form_version_id, field_data):
        """
        Adds a new field to a form version.
        :param env: Odoo environment
        :param form_version_id: int, ID of dfr.form.version
        :param field_data: dict containing data for dfr.form.field
        :return: dfr.form.field recordset
        """
        _logger.info("Adding field to form version ID %s with data: %s", form_version_id, field_data)
        form_version = env['dfr.form.version'].browse(form_version_id)
        if not form_version.exists():
            raise UserError(_("Form Version with ID %s not found.") % form_version_id)
        if not form_version.is_editable:
            raise UserError(_("Cannot add fields to a form version that is not in 'Draft' state. Current state: %s") % form_version.status)

        if 'form_version_id' not in field_data:
            field_data['form_version_id'] = form_version_id
        elif field_data['form_version_id'] != form_version_id:
             raise UserError(_("Field data form_version_id mismatch."))


        new_field = env['dfr.form.field'].create(field_data)
        _logger.info("Field '%s' (ID: %s) added to form version ID %s.", new_field.name, new_field.id, form_version_id)
        return new_field

    def update_field_in_version(self, env, field_id, field_data):
        """
        Updates an existing field in a form version.
        :param env: Odoo environment
        :param field_id: int, ID of dfr.form.field
        :param field_data: dict with fields to update
        :return: bool (success)
        """
        _logger.info("Updating field ID %s with data: %s", field_id, field_data)
        form_field = env['dfr.form.field'].browse(field_id)
        if not form_field.exists():
            raise UserError(_("Form Field with ID %s not found.") % field_id)
        
        if not form_field.form_version_id.is_editable:
            raise UserError(_("Cannot update fields in a form version that is not in 'Draft' state. Current state: %s") % form_field.form_version_id.status)

        if 'form_version_id' in field_data and field_data['form_version_id'] != form_field.form_version_id.id:
            raise UserError(_("Cannot change the form version of a field."))

        form_field.write(field_data)
        _logger.info("Field ID %s updated successfully.", field_id)
        return True

    def remove_field_from_version(self, env, field_id):
        """
        Removes a field from a form version.
        :param env: Odoo environment
        :param field_id: int, ID of dfr.form.field
        :return: bool (success)
        """
        _logger.info("Removing field ID %s", field_id)
        form_field = env['dfr.form.field'].browse(field_id)
        if not form_field.exists():
            # Idempotent: if already removed, consider it a success
            _logger.warning("Attempted to remove non-existent Form Field with ID %s.", field_id)
            return True 
        
        if not form_field.form_version_id.is_editable:
            raise UserError(_("Cannot remove fields from a form version that is not in 'Draft' state. Current state: %s") % form_field.form_version_id.status)

        form_field.unlink()
        _logger.info("Field ID %s removed successfully.", field_id)
        return True