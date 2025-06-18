# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
# Assuming FormDefinitionService is not directly imported into models/wizards
# but rather used by a controller or another service that wizards might call.
# For direct use within wizard action:
# from ..services.form_definition_service import FormDefinitionService

_logger = logging.getLogger(__name__)

class FormVersionWizard(models.TransientModel):
    _name = 'dfr.form.version.wizard'
    _description = 'Create New Form Version Wizard'

    form_master_id = fields.Many2one(
        'dfr.form',
        string='Form Master',
        required=True,
        readonly=True, # Typically set from context and not changed by user
        default=lambda self: self.env.context.get('active_id') if self.env.context.get('active_model') == 'dfr.form' else None
    )
    source_version_id = fields.Many2one(
        'dfr.form.version',
        string='Copy Fields From (Optional)',
        domain="[('form_master_id', '=', form_master_id), ('status', '!=', 'archived')]", # Allow copying from draft or published
        help="Optional existing version to copy fields and their settings from. Only non-archived versions are shown."
    )
    new_version_description = fields.Text(
        string='New Version Description',
        help="Provide a brief description for this new version (e.g., changes made, purpose)."
    )

    @api.model
    def default_get(self, fields_list):
        res = super(FormVersionWizard, self).default_get(fields_list)
        if 'form_master_id' not in res and self.env.context.get('active_model') == 'dfr.form' and self.env.context.get('active_id'):
            res['form_master_id'] = self.env.context.get('active_id')
        if not res.get('form_master_id'):
            raise UserError(_("Form Master must be selected or passed in context to create a new version."))
        return res

    def action_create_version(self):
        """
        Calls the FormDefinitionService (or directly creates a version)
        to create a new version and returns an action to open it.
        """
        self.ensure_one()
        _logger.info("Wizard action_create_version called for form_master_id: %s, source_version_id: %s",
                     self.form_master_id.id, self.source_version_id.id if self.source_version_id else "None")

        if not self.form_master_id:
            raise UserError(_("A Form Master must be specified."))

        # This wizard now directly calls the ORM model logic for creating a new version.
        # The FormDefinitionService could be used if it were instantiated and passed,
        # but typical wizard actions call ORM methods or other wizards.
        # Here, we'll mimic what the service would do or call a specific model method if it exists.

        vals = {
            'form_master_id': self.form_master_id.id,
            'description': self.new_version_description,
            'status': 'draft', # New versions always start as draft
        }

        if self.source_version_id:
            # Use the copy method of dfr.form.version, which handles deep copying of fields
            new_version = self.source_version_id.copy(default=vals)
            # Ensure description from wizard overrides copied description if provided
            if self.new_version_description:
                 new_version.description = self.new_version_description
            _logger.info("New form version (ID: %s) created by copying from version (ID: %s).",
                         new_version.id, self.source_version_id.id)
        else:
            # Create a new version from scratch (no fields initially, unless `field_ids` are handled by `create`)
            # `version_number` is typically handled by default lambda on the model using ir.sequence
            new_version = self.env['dfr.form.version'].create(vals)
            _logger.info("New form version (ID: %s) created from scratch.", new_version.id)
        
        # Return action to open the newly created form version
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'dfr.form.version',
            'view_mode': 'form',
            'res_id': new_version.id,
            'target': 'current', # Or 'new' to open in a dialog/new window
            'context': self.env.context, # Preserve context
        }
        return action