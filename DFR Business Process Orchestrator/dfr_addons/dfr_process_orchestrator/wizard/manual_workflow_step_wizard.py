# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ManualWorkflowStepWizard(models.TransientModel):
    _name = 'manual.workflow.step.wizard'
    _description = 'Manual Workflow Step Execution Wizard'

    # This selection should ideally be populated dynamically or be very generic.
    # For now, providing some common DFR workflow types.
    WORKFLOW_TYPES = [
        ('farmer_lifecycle', 'Farmer Lifecycle'),
        ('portal_submission', 'Portal Submission Review'),
        ('deduplication_review', 'De-duplication Review Task'), 
        # Add other relevant workflow contexts
    ]
    
    workflow_type = fields.Selection(
        selection=WORKFLOW_TYPES,
        string='Workflow Type',
        required=True,
        help="Select the type of workflow you want to interact with."
    )
    
    record_ref_model = fields.Char(string="Record Model", help="Technical name of the model (e.g., dfr.farmer).")
    record_ref_id = fields.Integer(string="Record ID", help="ID of the record.")

    @api.model
    def _selection_target_model_wizard(self):
        # Reuse the selection from workflow_log or create a broader one
        # Ensure workflow.log model is available in env
        if 'workflow.log' in self.env:
            return self.env['workflow.log']._selection_target_model()
        # Fallback if workflow.log or its method isn't available during wizard model load
        # This fallback should ideally be more robust or ensure dependencies correctly load models
        return [('res.partner', 'Partner'), ('res.users', 'User')]


    record_ref = fields.Reference(
        string='Target Record', 
        selection='_selection_target_model_wizard',
        help="Select the record to apply the manual step to."
    )

    # This field would ideally be filtered based on workflow_type and selected record_ref.
    # For now, a generic Many2one to ir.actions.server.
    target_step_action_id = fields.Many2one(
        'ir.actions.server',
        string='Target Workflow Step/Action',
        required=True,
        # The domain needs record_ref_model to be set.
        # If record_ref is set, record_ref_model can be derived from it.
        # If record_ref_model is set directly, use that.
        domain="[('model_id.model', '=', record_ref_model)]",
        help="Select the server action representing the workflow step to execute manually."
    )
    
    reason = fields.Text(string='Reason for Manual Intervention', required=True)

    # If using separate model/id fields to populate record_ref:
    # This onchange is crucial if the view primarily uses record_ref_model and record_ref_id
    # but the action_execute_manual_step relies on record_ref.
    # As per SDS, this is commented out, so I will leave it commented.
    # If this is not active, record_ref needs to be populated by other means (e.g. context or direct field in view)
    # @api.onchange('record_ref_model', 'record_ref_id')
    # def _onchange_record_identifier(self):
    #    if self.record_ref_model and self.record_ref_id:
    #        try:
    #            # Check if model exists
    #            self.env[self.record_ref_model]
    #            # Check if record id is valid for model (optional, browse will fail if not)
    #            # record = self.env[self.record_ref_model].browse(self.record_ref_id)
    #            # if not record.exists():
    #            #    self.record_ref = False
    #            #    # Optional: raise a warning to the user
    #            #    return {'warning': {'title': _("Warning"), 'message': _("Record ID not found for the selected model.")}}
    #            self.record_ref = f"{self.record_ref_model},{self.record_ref_id}"
    #        except KeyError: # Model does not exist
    #            self.record_ref = False
    #            # Optional: raise a warning to the user
    #            # return {'warning': {'title': _("Warning"), 'message': _("Invalid model name.")}}
    #        except Exception: # Other potential errors, e.g. invalid ID format for browse
    #            self.record_ref = False
    #    else:
    #        self.record_ref = False

    @api.onchange('record_ref')
    def _onchange_record_ref(self):
        if self.record_ref:
            self.record_ref_model = self.record_ref._name
            self.record_ref_id = self.record_ref.id
        else:
            self.record_ref_model = False
            self.record_ref_id = False


    def action_execute_manual_step(self):
        self.ensure_one()
        if not self.record_ref: # This is the critical field used by the action logic
            # If using record_ref_model and record_ref_id as primary input,
            # we need to construct record_ref from them if it's not already set.
            if self.record_ref_model and self.record_ref_id:
                try:
                    self.record_ref = self.env[self.record_ref_model].browse(self.record_ref_id)
                    if not self.record_ref.exists():
                         raise UserError(_("Target record specified by Model and ID does not exist or you don't have access."))
                except Exception as e:
                    _logger.error(f"Error trying to browse record {self.record_ref_model},{self.record_ref_id}: {e}")
                    raise UserError(_("Could not access target record from Model and ID. Error: %s") % e)
            else: # If record_ref is not set and model/id are also not set, then error.
                raise UserError(_("Target record must be selected."))

        if not self.target_step_action_id:
            raise UserError(_("Target workflow step/action must be selected."))

        target_record = self.record_ref # self.record_ref should now be a recordset
        
        # Log the manual intervention
        self.env['workflow.log'].log_event(
            workflow_name=f"Manual Intervention ({self.workflow_type})",
            message=f"Manually executing step '{self.target_step_action_id.name}' on record {target_record.display_name if hasattr(target_record, 'display_name') else str(target_record)}. Reason: {self.reason}",
            level='warning',
            record=target_record,
            user_id=self.env.user.id
        )

        _logger.info(
            f"User {self.env.user.name} manually triggered action '{self.target_step_action_id.name}' "
            f"on record {target_record._name} ID {target_record.id}."
        )
        
        # Execute the server action
        # The server action's code will run in the context of the target_record
        try:
            # Pass active_id, active_ids, and active_model in context for the server action
            context = {
                'active_id': target_record.id,
                'active_ids': [target_record.id],
                'active_model': target_record._name,
            }
            self.target_step_action_id.with_context(**context).run()
            
            # Check if the target record has a 'message_post' method (chatter)
            if hasattr(target_record, 'message_post'):
                target_record.message_post(body=_(
                    "Workflow step '%(action_name)s' manually executed by %(user_name)s. Reason: %(reason)s",
                    action_name=self.target_step_action_id.name,
                    user_name=self.env.user.name,
                    reason=self.reason
                ))
        except Exception as e:
            _logger.error(f"Error executing manual workflow step '{self.target_step_action_id.name}' on {target_record}: {e}")
            self.env['workflow.log'].log_event(
                workflow_name=f"Manual Intervention ({self.workflow_type}) - ERROR",
                message=f"Error executing step '{self.target_step_action_id.name}' on record {target_record.display_name if hasattr(target_record, 'display_name') else str(target_record)}. Error: {e}",
                level='error',
                record=target_record
            )
            raise UserError(_("Failed to execute the workflow step. Error: %s") % e)

        return {'type': 'ir.actions.act_window_close'}