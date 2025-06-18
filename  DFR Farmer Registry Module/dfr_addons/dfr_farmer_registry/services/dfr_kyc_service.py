# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

# Assume supporting models like dfr.national.id.type are available

class DfrKycService(models.AbstractModel):
    _name = 'dfr.kyc.service'
    _description = 'DFR KYC Service'

    @api.model
    def initiate_kyc_verification_request(self, farmer_id, submitted_document_ids=None):
        """
        Initiates the KYC verification workflow for a farmer.
        Called from `dfr.farmer` model's `action_request_kyc_review`.

        :param farmer_id: ID of the farmer.
        :param submitted_document_ids: Optional list of ir.attachment IDs for KYC documents.
        :return: True if successful, raises error otherwise.
        """
        farmer = self.env['dfr.farmer'].browse(farmer_id)
        if not farmer.exists():
            _logger.error("Cannot initiate KYC: Farmer with ID %s not found.", farmer_id)
            raise UserError(_("Farmer with ID %s not found.") % farmer_id)

        if farmer.kyc_status in ('pending_review', 'verified'):
            _logger.warning("KYC verification request for Farmer %s (ID: %s) ignored. Current status: %s.",
                            farmer.name, farmer.id, farmer.kyc_status)
            # Depending on strictness, could raise UserError or just return True.
            # Let's be lenient and say it's "successful" as it's already in a desired state or beyond.
            return True

        vals_to_update = {'kyc_status': 'pending_review'}
        try:
            farmer.write(vals_to_update)
            log_message = _("KYC verification request initiated.")

            # Link documents if provided
            if submitted_document_ids:
                 attachments = self.env['ir.attachment'].browse(submitted_document_ids).exists()
                 if attachments:
                     farmer.message_post(
                         body=_("KYC documents submitted for review."),
                         attachment_ids=attachments.ids # Odoo expects list of IDs here
                     )
                     log_message += _(" %s document(s) attached.") % len(attachments)
                     _logger.info("Linked %s KYC documents to Farmer %s (ID: %s).", len(attachments), farmer.name, farmer.id)

            # Create activity for KYC review team (example)
            activity_type_id = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
            if activity_type_id:
                # Determine user_id: Assign to a specific user, a group, or leave unassigned for rules
                # Example: assign to farmer's creator if they are internal, or a specific KYC group user
                # user_id = farmer.create_uid.id # Simplistic example
                # A more robust solution involves user groups or dedicated KYC teams.
                # For now, let's leave it unassigned so it can be picked up or assigned by rules/supervisors.
                user_id = None
                activity_vals = {
                    'activity_type_id': activity_type_id.id,
                    'summary': _('Review KYC for Farmer: %s') % farmer.name,
                    'note': _('Please review the submitted KYC information and documents for farmer %s (UID: %s).') % (farmer.name, farmer.uid),
                    'user_id': user_id,
                    'date_deadline': fields.Date.today() + fields.timedelta(days=self.env.context.get('kyc_review_deadline_days', 7)), # Configurable deadline
                    'res_id': farmer.id,
                    'res_model_id': self.env['ir.model']._get_id('dfr.farmer'),
                }
                self.env['mail.activity'].create(activity_vals)
                log_message += _(" Review activity scheduled.")
                _logger.info("Scheduled KYC review activity for Farmer %s (ID: %s).", farmer.name, farmer.id)

            farmer.message_post(body=log_message)
            _logger.info("KYC verification request successfully initiated for Farmer %s (ID: %s). Status set to 'pending_review'.",
                         farmer.name, farmer.id)
            return True

        except Exception as e:
            _logger.error("Failed to initiate KYC for Farmer ID %s: %s", farmer_id, e)
            farmer.write({'kyc_status': 'not_started'}) # Revert status on failure
            raise UserError(_("Failed to initiate KYC verification: %s") % str(e))

    @api.model
    def process_kyc_manual_review(self, farmer_id, reviewer_id, review_outcome, review_notes):
        """
        Processes the outcome of a manual KYC review.
        Called from `dfr.farmer.kyc.wizard`.

        :param farmer_id: ID of the farmer.
        :param reviewer_id: ID of the res.users who performed the review.
        :param review_outcome: String 'verified' or 'rejected'.
        :param review_notes: Text notes from the reviewer.
        :return: True if successful, raises error otherwise.
        """
        farmer = self.env['dfr.farmer'].browse(farmer_id)
        reviewer = self.env['res.users'].browse(reviewer_id)

        if not farmer.exists():
            _logger.error("Cannot process KYC: Farmer with ID %s not found.", farmer_id)
            raise UserError(_("Farmer with ID %s not found.") % farmer_id)
        if not reviewer.exists():
            _logger.error("Cannot process KYC: Reviewer with ID %s not found.", reviewer_id)
            raise UserError(_("Reviewer with ID %s not found.") % reviewer_id)
        if review_outcome not in ('verified', 'rejected'):
             _logger.error("Invalid KYC review outcome '%s' for Farmer %s (ID: %s).", review_outcome, farmer.name, farmer.id)
             raise ValidationError(_("Invalid KYC review outcome: %s.") % review_outcome)

        if farmer.kyc_status != 'pending_review':
             _logger.warning("Processing KYC for Farmer %s (ID: %s) while status is %s (expected 'pending_review'). Proceeding.",
                             farmer.name, farmer.id, farmer.kyc_status)
             # Allow processing but log a warning. UI should ideally prevent this.

        vals_to_update = {
            'kyc_status': review_outcome,
            'kyc_verification_date': fields.Date.today(),
            'kyc_reviewer_id': reviewer_id,
            'kyc_review_notes': review_notes,
        }

        try:
            farmer.write(vals_to_update)
            log_message_outcome = _("Verified") if review_outcome == 'verified' else _("Rejected")
            log_message = _("KYC Review Processed: %s by %s.\nNotes: %s") % (
                log_message_outcome,
                reviewer.name,
                review_notes or _("N/A")
            )
            farmer.message_post(body=log_message)
            _logger.info("KYC manual review processed for Farmer %s (ID: %s). Outcome: %s. Reviewer: %s.",
                         farmer.name, farmer.id, review_outcome, reviewer.name)

            # Mark related KYC activity as done
            # Assuming the activity was for 'dfr.farmer' and res_id=farmer_id
            # And activity type was 'mail.mail_activity_data_todo'
            activity_type_id = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
            if activity_type_id:
                domain = [
                    ('res_model', '=', 'dfr.farmer'),
                    ('res_id', '=', farmer.id),
                    ('activity_type_id', '=', activity_type_id.id),
                    ('summary', 'ilike', _('Review KYC for Farmer: %s') % farmer.name), # More specific match
                    ('user_id', '=', reviewer_id), # Typically assigned to the reviewer
                ]
                # If activity might be unassigned or assigned to a group, broaden user_id search
                # For now, assume it's assigned to the reviewer or a user that can close it.
                activities = self.env['mail.activity'].search(domain)
                if activities:
                    activities.action_done() # Mark as done
                    _logger.info("Marked %s KYC review activities as done for Farmer %s.", len(activities), farmer.name)
                else: # Try broader search if user_id was None on creation.
                    broader_domain = [
                        ('res_model', '=', 'dfr.farmer'),
                        ('res_id', '=', farmer.id),
                        ('activity_type_id', '=', activity_type_id.id),
                        ('summary', 'ilike', _('Review KYC for Farmer: %s') % farmer.name),
                    ]
                    activities = self.env['mail.activity'].search(broader_domain)
                    if activities:
                        activities.action_feedback(feedback=f"KYC Processed: {log_message_outcome}. Notes: {review_notes or 'N/A'}")


            # If verified and farmer status was 'pending_verification', set to 'active'
            if review_outcome == 'verified' and farmer.status == 'pending_verification':
                farmer.action_set_status_active() # This method on farmer model handles logging

            return True
        except Exception as e:
            _logger.error("Failed to process KYC manual review for Farmer ID %s: %s", farmer_id, e)
            # Potentially revert KYC status if appropriate, though partial update might be complex
            raise UserError(_("Failed to process KYC review: %s") % str(e))


    @api.model
    def check_external_kyc_api(self, farmer_id, national_id_number, national_id_type):
        """
        Placeholder method for integrating with an external KYC API.
        This is not implemented in the current scope as per SDS focus on manual workflow.
        """
        _logger.info("External KYC API check STUB called for Farmer ID %s (National ID: %s, Type: %s). "
                     "This feature is not implemented in the current version.",
                     farmer_id, national_id_number, national_id_type)
        # Future implementation would:
        # 1. Get API endpoint and credentials from config.
        # 2. Prepare payload with farmer_data (national_id, name, dob, etc.).
        # 3. Make HTTP request to external API.
        # 4. Parse API response (success/failure, verification status, details).
        # 5. Call process_kyc_manual_review (or a dedicated method for API results) to update farmer.kyc_status.
        # 6. Log API interaction and outcome.
        # 7. Handle errors, retries, timeouts.
        return {
            'status': 'not_implemented',
            'message': _("External KYC API integration is not available in this version.")
        }