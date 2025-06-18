# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import _, fields
from odoo.exceptions import UserError, ValidationError
from .form_validation_service import FormValidationService

_logger = logging.getLogger(__name__)

class FormSubmissionService:
    """
    Processes and stores dynamic form submissions.
    """

    def __init__(self):
        self.validation_service = FormValidationService()

    def process_submission(self, env, farmer_uid_or_id, form_version_id, responses_data, 
                           submitted_by_user_id=None, submission_source='admin'):
        """
        Processes raw submission data, validates it, and creates submission and response records.
        :param env: Odoo environment
        :param farmer_uid_or_id: str UID or int ID of dfr.farmer
        :param form_version_id: int, ID of dfr.form.version
        :param responses_data: dict: {field_technical_name: value}
        :param submitted_by_user_id: int, optional, ID of res.users
        :param submission_source: str, e.g., 'admin', 'mobile', 'portal'
        :return: dfr.form.submission recordset
        """
        _logger.info(
            "Processing submission for farmer '%s', form version ID %s, source '%s'. Responses: %s",
            farmer_uid_or_id, form_version_id, submission_source, responses_data
        )

        Farmer = env['dfr.farmer']
        if isinstance(farmer_uid_or_id, str):
            farmer = Farmer.search([('uid', '=', farmer_uid_or_id)], limit=1)
        else:
            farmer = Farmer.browse(farmer_uid_or_id)
        
        if not farmer.exists():
            raise UserError(_("Farmer with identifier '%s' not found.") % farmer_uid_or_id)

        form_version = env['dfr.form.version'].browse(form_version_id)
        if not form_version.exists():
            raise UserError(_("Form Version with ID %s not found.") % form_version_id)
        if form_version.status != 'published':
            raise UserError(_("Cannot submit to form version '%s' (ID: %s) as it is not published. Current status: %s.") % 
                            (form_version.name, form_version_id, form_version.status))

        # Validate responses
        is_valid, errors = self.validation_service.validate_submission_responses(env, form_version, responses_data)
        if not is_valid:
            error_messages = []
            for field_name, msg in errors.items():
                field_label = form_version.field_ids.filtered(lambda f: f.name == field_name).label or field_name
                error_messages.append(f"{_('Field')} '{field_label}': {msg}")
            raise ValidationError(_("Submission contains validation errors:\n%s") % "\n".join(error_messages))

        # Create submission record
        submission_vals = {
            'farmer_id': farmer.id,
            'form_version_id': form_version_id,
            'submission_date': fields.Datetime.now(),
            'submitted_by_user_id': submitted_by_user_id or env.user.id,
            'submission_source': submission_source,
            'state': 'submitted', # Default state after successful processing
        }
        submission = env['dfr.form.submission'].create(submission_vals)
        _logger.info("Form submission record created: ID %s", submission.id)

        # Create response records
        response_model = env['dfr.form.response']
        attachment_model = env['ir.attachment']
        selection_option_answer_model = env['dfr.form.selection.option.answer']

        for field_technical_name, value in responses_data.items():
            form_field = form_version.field_ids.filtered(lambda f: f.name == field_technical_name)
            if not form_field:
                _logger.warning("Field with technical name '%s' not found in form version ID %s. Skipping response.",
                                field_technical_name, form_version_id)
                continue
            
            form_field = form_field[0] # Take the first one if (incorrectly) multiple exist

            response_vals = {
                'submission_id': submission.id,
                'field_id': form_field.id,
            }

            if form_field.field_type == 'text' or form_field.field_type == 'computed_text':
                response_vals['value_text'] = value
            elif form_field.field_type == 'number':
                response_vals['value_number'] = float(value) if value is not None else None
            elif form_field.field_type == 'date':
                response_vals['value_date'] = value # Expects YYYY-MM-DD string or date object
            elif form_field.field_type == 'datetime':
                response_vals['value_datetime'] = value # Expects YYYY-MM-DD HH:MM:SS string or datetime object
            elif form_field.field_type == 'boolean':
                response_vals['value_boolean'] = bool(value)
            elif form_field.field_type == 'selection':
                response_vals['value_selection'] = value # Stores the key
            elif form_field.field_type == 'multi_selection':
                if value and isinstance(value, list):
                    option_ids = []
                    for val_key in value:
                        # Find or create dfr.form.selection.option.answer
                        # For simplicity, assume options are value:label and we store value as 'name'
                        # A better approach might be to have pre-defined selection options if they are reused
                        option_rec = selection_option_answer_model.search([('name', '=', val_key)], limit=1)
                        if not option_rec:
                             # Try to derive display_name (label) from field's selection_options
                            parsed_options = dict(form_field.get_selection_options_parsed())
                            display_name = parsed_options.get(val_key, val_key)
                            option_rec = selection_option_answer_model.create({'name': val_key, 'display_name': display_name})
                        option_ids.append(option_rec.id)
                    response_vals['value_multi_selection_ids'] = [(6, 0, option_ids)]
            elif form_field.field_type == 'gps_point':
                if isinstance(value, dict) and 'latitude' in value and 'longitude' in value:
                    response_vals['value_gps_latitude'] = float(value['latitude']) if value['latitude'] is not None else None
                    response_vals['value_gps_longitude'] = float(value['longitude']) if value['longitude'] is not None else None
                elif isinstance(value, (list, tuple)) and len(value) == 2:
                    response_vals['value_gps_latitude'] = float(value[0]) if value[0] is not None else None
                    response_vals['value_gps_longitude'] = float(value[1]) if value[1] is not None else None
                else:
                     _logger.warning("Invalid GPS data format for field %s: %s", field_technical_name, value)
            elif form_field.field_type == 'image':
                # Expects value to be a dict {'name': 'filename.png', 'data': 'base64_encoded_data_string'}
                # Or it could be a direct attachment_id if already created elsewhere
                if isinstance(value, int): # Assuming it's an ir.attachment ID
                    response_vals['value_attachment_id'] = value
                elif isinstance(value, dict) and value.get('data') and value.get('name'):
                    attachment = attachment_model.create({
                        'name': value['name'],
                        'datas': value['data'], # Odoo expects base64 string here
                        'res_model': 'dfr.form.response', # Or 'dfr.form.submission'
                        'res_id': 0, # Will be updated after response is created, or link to submission
                    })
                    response_vals['value_attachment_id'] = attachment.id
                elif value: # if only base64 string is passed.
                     attachment = attachment_model.create({
                        'name': f"{field_technical_name}_{submission.id}",
                        'datas': value,
                        'res_model': 'dfr.form.response',
                        'res_id': 0,
                    })
                     response_vals['value_attachment_id'] = attachment.id

            response = response_model.create(response_vals)
            # If attachment was created, link its res_id now
            if form_field.field_type == 'image' and response_vals.get('value_attachment_id') and not isinstance(value, int):
                attachment = attachment_model.browse(response_vals['value_attachment_id'])
                if attachment.res_id == 0: # only if it was newly created for this response
                    attachment.write({'res_id': response.id}) # Link to response

        _logger.info("All responses for submission ID %s created successfully.", submission.id)
        return submission

    def get_farmer_submissions(self, env, farmer_id, form_master_id=None):
        """
        Searches dfr.form.submission records for the given farmer_id.
        :param env: Odoo environment
        :param farmer_id: int, ID of dfr.farmer
        :param form_master_id: int, optional, ID of dfr.form (master)
        :return: dfr.form.submission recordset
        """
        _logger.debug("Getting submissions for farmer ID %s, form master ID %s", farmer_id, form_master_id)
        domain = [('farmer_id', '=', farmer_id)]
        if form_master_id:
            domain.append(('form_version_id.form_master_id', '=', form_master_id))
        
        submissions = env['dfr.form.submission'].search(domain, order='submission_date desc')
        _logger.debug("Found %s submissions.", len(submissions))
        return submissions