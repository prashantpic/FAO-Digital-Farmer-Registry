# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class DfrFarmerKycWizard(models.TransientModel):
    _name = 'dfr.farmer.kyc.wizard'
    _description = 'DFR Farmer KYC Review Wizard'

    # --- Fields ---
    farmer_id = fields.Many2one(
        'dfr.farmer',
        string='Farmer',
        required=True,
        readonly=True,
        ondelete='cascade' # If farmer is deleted while wizard is open (unlikely but good practice)
    )
    current_kyc_status = fields.Selection(
        related='farmer_id.kyc_status',
        readonly=True,
        string="Current KYC Status"
    )
    national_id_display = fields.Char(
        string='National ID',
        compute='_compute_national_id_display', # Combine type and number
        readonly=True
    )
    verification_outcome = fields.Selection([
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ], string='Verification Outcome', required=True, default='verified')
    review_notes = fields.Text(string='Review Notes')

    # Display attachments linked to the farmer (e.g., KYC documents)
    # This wizard doesn't upload new ones, just for review context.
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Supporting Documents (from Farmer Record)',
        compute='_compute_farmer_attachments',
        readonly=True,
        help="Documents attached to the farmer record, potentially including submitted KYC documents."
    )

    # --- Compute Methods ---
    @api.depends('farmer_id.national_id_type_id', 'farmer_id.national_id_number')
    def _compute_national_id_display(self):
        for record in self:
            if record.farmer_id:
                parts = []
                if record.farmer_id.national_id_type_id:
                    parts.append(record.farmer_id.national_id_type_id.display_name)
                if record.farmer_id.national_id_number:
                    parts.append(record.farmer_id.national_id_number)
                record.national_id_display = ": ".join(parts) if parts else _("Not Set")
            else:
                record.national_id_display = _("N/A")

    @api.depends('farmer_id')
    def _compute_farmer_attachments(self):
        for record in self:
            if record.farmer_id:
                # Find attachments linked to messages on the farmer record.
                # This could be refined if KYC docs are tagged or linked via a specific field.
                # For now, show all attachments on the farmer's chatter.
                attachments = self.env['ir.attachment'].search([
                    ('res_model', '=', 'dfr.farmer'),
                    ('res_id', '=', record.farmer_id.id)
                ])
                record.attachment_ids = [(6, 0, attachments.ids)]
            else:
                record.attachment_ids = False


    # --- Default Methods ---
    @api.model
    def default_get(self, fields_list):
        res = super(DfrFarmerKycWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')

        if active_model == 'dfr.farmer' and active_id:
            farmer = self.env['dfr.farmer'].browse(active_id)
            if not farmer.exists():
                 raise UserError(_("The farmer record for KYC review (ID: %s) no longer exists.") % active_id)

            if farmer.kyc_status != 'pending_review':
                 # This check is good, but the button to launch wizard should ideally be invisible if not pending.
                 _logger.warning("KYC Review Wizard opened for Farmer %s (ID: %s) with status %s, not 'pending_review'.",
                                 farmer.name, farmer.id, farmer.kyc_status)
                 # Allow opening anyway, action_submit_kyc_review will re-check.

            res['farmer_id'] = farmer.id
            # Populate review_notes with existing notes if user is re-evaluating or continuing.
            # SDS: res['review_notes'] = farmer.kyc_review_notes # Decided against pre-filling to force fresh input.
            # User can see current notes on farmer form anyway.

        elif 'farmer_id' not in res and 'farmer_id' in fields_list : # Ensure farmer_id is always set if requested.
             raise UserError(_("This wizard must be launched from a farmer record's context."))
        return res

    # --- Action Methods ---
    def action_submit_kyc_review(self):
        self.ensure_one()
        if not self.farmer_id:
             # Should not happen due to required=True and default_get, but good check.
             raise UserError(_("No farmer record associated with this KYC review. Please close and retry."))

        if self.farmer_id.kyc_status != 'pending_review':
             # This is a critical check to prevent processing if status changed since wizard opened.
             raise UserError(
                _("KYC review can only be submitted for farmers in 'Pending Review' status. Farmer %s (ID: %s) currently has status: %s. Please refresh the farmer record.") %
                (self.farmer_id.name, self.farmer_id.id, dict(self.farmer_id._fields['kyc_status'].selection).get(self.farmer_id.kyc_status))
             )

        _logger.info("Submitting KYC Review for Farmer %s (ID: %s). Outcome: %s. Reviewer: %s (ID: %s).",
                     self.farmer_id.name, self.farmer_id.id, self.verification_outcome,
                     self.env.user.name, self.env.user.id)
        try:
            success = self.env['dfr.kyc.service'].process_kyc_manual_review(
                farmer_id=self.farmer_id.id,
                reviewer_id=self.env.user.id,
                review_outcome=self.verification_outcome,
                review_notes=self.review_notes,
            )

            if not success: # Service should raise error, but defensive check
                message = _("KYC review submission for Farmer %s (ID: %s) reported failure by the service. Please check logs.") % (self.farmer_id.name, self.farmer_id.id)
                self.env.user.notify_warning(message=message) # Non-blocking notification
                _logger.error(message)
                # No specific action to return, wizard stays open for user to retry or cancel.
                # Could re-raise to make it a blocking error on wizard:
                # raise UserError(message)
                return { # Keep wizard open if service returns False without raising
                    'type': 'ir.actions.do_nothing'
                }

            message = _("KYC review for Farmer %s (ID: %s) submitted successfully. Outcome: %s.") % (
                self.farmer_id.name, self.farmer_id.id,
                dict(self._fields['verification_outcome'].selection).get(self.verification_outcome)
            )
            self.env.user.notify_success(message=message)

            # Return an action to close the wizard and reload the farmer view (or just close)
            # To reload the farmer view specifically if launched from form:
            if self.env.context.get('active_model') == 'dfr.farmer' and self.env.context.get('active_id') == self.farmer_id.id:
                 return {
                     'type': 'ir.actions.act_window',
                     'res_model': 'dfr.farmer',
                     'res_id': self.farmer_id.id,
                     'view_mode': 'form',
                     'target': 'main', # Open in main content area, replacing wizard
                     'flags': {'initial_mode': 'view'},
                 }
            else: # If launched from elsewhere, or to simply close and let user navigate
                return {'type': 'ir.actions.act_window_close'}


        except UserError as ue: # Re-raise UserErrors from service
            _logger.warning("UserError during KYC review submission for Farmer %s: %s", self.farmer_id.name, ue)
            raise
        except ValidationError as ve: # Re-raise ValidationErrors from service
            _logger.warning("ValidationError during KYC review submission for Farmer %s: %s", self.farmer_id.name, ve)
            raise
        except Exception as e:
            _logger.error("Unexpected error submitting KYC review for Farmer %s (ID: %s): %s",
                          self.farmer_id.name, self.farmer_id.id, e, exc_info=True)
            raise UserError(_("An unexpected error occurred while submitting the KYC review: %s") % str(e))