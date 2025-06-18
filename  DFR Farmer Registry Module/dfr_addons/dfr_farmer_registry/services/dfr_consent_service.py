# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

# Assume supporting model dfr.consent.purpose is available

class DfrConsentService(models.AbstractModel):
    _name = 'dfr.consent.service'
    _description = 'DFR Consent Service'

    @api.model
    def record_consent(self, farmer_id, consent_status, consent_date, consent_version_agreed, consent_purpose_ids, consent_text_agreed_to_id=None):
        """
        Records or updates consent for a farmer.
        This method is called from `dfr.farmer` model's `action_record_consent` which prepares some of these parameters.
        The `consent_status` here is expected to be 'given'.

        :param farmer_id: ID of the farmer.
        :param consent_status: String, typically 'given'.
        :param consent_date: Datetime object for when consent was given.
        :param consent_version_agreed: String representing the version of consent policy agreed to.
        :param consent_purpose_ids: List of IDs of dfr.consent.purpose records.
        :param consent_text_agreed_to_id: Optional ID of a dfr.consent.text.version record.
        :return: True if successful, raises error otherwise.
        """
        if consent_status != 'given':
            raise ValidationError(_("This method is intended for recording 'given' consent. Status provided: %s") % consent_status)

        farmer = self.env['dfr.farmer'].browse(farmer_id)
        if not farmer.exists():
            _logger.error("Cannot record consent: Farmer with ID %s not found.", farmer_id)
            raise UserError(_("Farmer with ID %s not found.") % farmer_id)

        vals_to_update = {
            'consent_status': consent_status,
            'consent_date': consent_date or fields.Datetime.now(),
            'consent_version_agreed': consent_version_agreed,
            'consent_purpose_ids': [(6, 0, consent_purpose_ids or [])],
            'consent_withdrawal_date': False, # Clear withdrawal date if re-consenting
            'consent_withdrawal_reason': False, # Clear withdrawal reason
        }
        # Assuming dfr.consent.text.version is a model that might exist, linked via a M2O field.
        # If such a field (e.g., 'consent_text_version_id') exists on 'dfr.farmer':
        # if consent_text_agreed_to_id and 'consent_text_version_id' in farmer._fields:
        #     vals_to_update['consent_text_version_id'] = consent_text_agreed_to_id

        try:
            farmer.write(vals_to_update)
            purpose_names = farmer.consent_purpose_ids.mapped('name')
            log_message = _("Consent status updated to '%s'.\nVersion Agreed: %s\nPurposes: %s") % (
                dict(farmer._fields['consent_status'].selection).get(farmer.consent_status),
                farmer.consent_version_agreed,
                ", ".join(purpose_names) or _("None specified")
            )
            farmer.message_post(body=log_message)
            _logger.info("Consent successfully recorded for Farmer %s (ID: %s). Status: %s. Purposes: %s.",
                         farmer.name, farmer.id, farmer.consent_status, purpose_names)
            return True
        except Exception as e:
            _logger.error("Failed to record consent for Farmer ID %s: %s", farmer_id, e)
            raise UserError(_("Failed to record consent: %s") % str(e))


    @api.model
    def withdraw_consent(self, farmer_id, withdrawal_date, withdrawal_reason):
        """
        Records consent withdrawal for a farmer.
        This method is called from `dfr.farmer` model's `action_withdraw_consent`.

        :param farmer_id: ID of the farmer.
        :param withdrawal_date: Datetime object for when consent was withdrawn.
        :param withdrawal_reason: String explaining the reason for withdrawal.
        :return: True if successful, raises error otherwise.
        """
        farmer = self.env['dfr.farmer'].browse(farmer_id)
        if not farmer.exists():
            _logger.error("Cannot withdraw consent: Farmer with ID %s not found.", farmer_id)
            raise UserError(_("Farmer with ID %s not found.") % farmer_id)

        if farmer.consent_status != 'given':
            raise ValidationError(_("Consent can only be withdrawn if currently 'Given'. Current status: %s") %
                                  dict(farmer._fields['consent_status'].selection).get(farmer.consent_status))

        vals_to_update = {
            'consent_status': 'withdrawn',
            'consent_withdrawal_date': withdrawal_date or fields.Datetime.now(),
            'consent_withdrawal_reason': withdrawal_reason,
            'consent_purpose_ids': [(5, 0, 0)], # Clear all purposes on withdrawal
        }

        try:
            farmer.write(vals_to_update)
            log_message = _("Consent Withdrawn.\nReason: %s") % (farmer.consent_withdrawal_reason or _("Not specified"))
            farmer.message_post(body=log_message)
            _logger.info("Consent withdrawal successfully recorded for Farmer %s (ID: %s). Reason: %s.",
                         farmer.name, farmer.id, farmer.consent_withdrawal_reason)
            return True
        except Exception as e:
            _logger.error("Failed to withdraw consent for Farmer ID %s: %s", farmer_id, e)
            raise UserError(_("Failed to withdraw consent: %s") % str(e))

    @api.model
    def get_farmer_consent_history(self, farmer_id):
        """
        Retrieves consent change history for a farmer.
        This currently relies on mail.thread tracking messages.
        A dedicated 'dfr.consent.log' model would be more robust for structured history.
        """
        farmer = self.env['dfr.farmer'].browse(farmer_id)
        if not farmer.exists():
             _logger.warning("Attempted to get consent history for non-existent Farmer ID %s.", farmer_id)
             return []

        # This queries messages related to consent field changes if tracking is enabled on them.
        # It's a very basic interpretation. Mail.message stores subtype descriptions or tracking values.
        # `mail.tracking.value` stores old/new values for tracked fields.
        consent_field_ids = [
            self.env['ir.model.fields']._get('dfr.farmer', 'consent_status').id,
            self.env['ir.model.fields']._get('dfr.farmer', 'consent_purpose_ids').id,
            self.env['ir.model.fields']._get('dfr.farmer', 'consent_version_agreed').id,
        ]
        consent_field_ids = [fid for fid in consent_field_ids if fid] # Filter out False if field not found

        consent_messages = self.env['mail.message'].search([
            ('model', '=', 'dfr.farmer'),
            ('res_id', '=', farmer_id),
            ('tracking_value_ids.field_id', 'in', consent_field_ids) # Check if message has tracking for these fields
        ], order='date DESC')

        history = []
        for msg in consent_messages:
            summary_parts = [msg.subject or msg.body[:100]] # Use subject or snippet of body
            for tracking_value in msg.tracking_value_ids.filtered(lambda tv: tv.field_id.id in consent_field_ids):
                field_desc = tracking_value.field_desc
                old_val_char = tracking_value.get_old_value()[1] if tracking_value.get_old_value() else 'N/A'
                new_val_char = tracking_value.get_new_value()[1] if tracking_value.get_new_value() else 'N/A'
                summary_parts.append(f"{field_desc}: '{old_val_char}' -> '{new_val_char}'")

            history.append({
                'date': msg.date,
                'author': msg.author_id.name if msg.author_id else (msg.email_from or _("System")),
                'summary': "\n".join(summary_parts),
                'message_body': msg.body, # Full body for details if needed
            })
        _logger.debug("Consent history retrieved for Farmer ID %s: %s entries.", farmer_id, len(history))
        return history

    @api.model
    def is_consent_valid_for_purpose(self, farmer_id, purpose_key_or_id):
        """
        Checks if a farmer has given valid (current status 'given') consent for a specific purpose.

        :param farmer_id: ID of the farmer.
        :param purpose_key_or_id: Key (e.g., 'data_sharing_research') or ID of the dfr.consent.purpose.
        :return: Boolean.
        """
        farmer = self.env['dfr.farmer'].browse(farmer_id)
        if not farmer.exists():
            _logger.warning("is_consent_valid_for_purpose: Farmer ID %s not found.", farmer_id)
            return False

        if farmer.consent_status != 'given':
            _logger.debug("Farmer ID %s consent status is '%s', not 'given'.", farmer_id, farmer.consent_status)
            return False

        ConsentPurpose = self.env['dfr.consent.purpose']
        purpose_domain = []
        if isinstance(purpose_key_or_id, int):
            purpose_domain = [('id', '=', purpose_key_or_id)]
        elif isinstance(purpose_key_or_id, str):
            # Assuming dfr.consent.purpose has a 'key' field for programmatic access
            purpose_domain = [('key', '=', purpose_key_or_id)]
        else:
            _logger.warning("Invalid purpose_key_or_id type: %s", type(purpose_key_or_id))
            return False

        purpose = ConsentPurpose.search(purpose_domain, limit=1)
        if not purpose.exists():
             _logger.warning("Consent purpose '%s' not found in dfr.consent.purpose.", purpose_key_or_id)
             return False

        is_valid = purpose in farmer.consent_purpose_ids
        _logger.debug("Consent check for Farmer ID %s, Purpose '%s' (ID: %s): %s",
                      farmer_id, purpose.name, purpose.id, is_valid)
        return is_valid