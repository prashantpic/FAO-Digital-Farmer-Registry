# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import uuid
import logging

_logger = logging.getLogger(__name__)

class DfrFarmer(models.Model):
    _name = 'dfr.farmer'
    _description = 'Digital Farmer Registry Farmer'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Assuming dfr_common_core provides audit fields if needed

    # --- Fields ---
    uid = fields.Char(string='Farmer UID', required=True, readonly=True, copy=False, index=True, help="Unique Farmer Identifier")
    name = fields.Char(string='Full Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Sex', tracking=True)
    role_in_household = fields.Selection([
        ('head', 'Head'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('other_relative', 'Other Relative'),
        ('non_relative', 'Non-Relative'),
        ('unknown', 'Unknown'), # Added as a default/fallback
    ], string='Role in Household', tracking=True, default='unknown')
    education_level_id = fields.Many2one('dfr.education.level', string='Education Level', tracking=True)
    contact_phone = fields.Char(string='Phone Number', tracking=True)
    contact_email = fields.Char(string='Email Address', tracking=True)
    national_id_type_id = fields.Many2one('dfr.national.id.type', string='National ID Type', tracking=True)
    national_id_number = fields.Char(string='National ID Number', tracking=True)
    kyc_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('pending_review', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ], string='KYC Status', default='not_started', required=True, tracking=True)
    kyc_verification_date = fields.Date(string='KYC Verification Date', readonly=True, tracking=True)
    kyc_reviewer_id = fields.Many2one('res.users', string='KYC Reviewer', readonly=True, tracking=True)
    kyc_review_notes = fields.Text(string='KYC Review Notes', tracking=True)
    status = fields.Selection([
        ('pending_verification', 'Pending Verification'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deceased', 'Deceased'),
        ('potential_duplicate', 'Potential Duplicate'), # Renamed from 'duplicate' for clarity
        ('archived', 'Archived'),
        ('merged_duplicate', 'Merged Duplicate') # Added for clarity on merged records
    ], string='Farmer Status', default='pending_verification', required=True, tracking=True, help="Lifecycle status of the farmer record.")

    household_member_ids = fields.One2many('dfr.household_member', 'farmer_id', string='Household Memberships')
    farm_ids = fields.One2many('dfr.farm', 'farmer_id', string='Farms')
    administrative_area_id = fields.Many2one('dfr.administrative.area', string='Administrative Area', tracking=True) # Assumed from dfr_common_core
    gps_latitude_homestead = fields.Float(string='Homestead Latitude', digits=(10, 7), tracking=True)
    gps_longitude_homestead = fields.Float(string='Homestead Longitude', digits=(10, 7), tracking=True)

    consent_status = fields.Selection([
        ('pending', 'Pending'),
        ('given', 'Given'),
        ('withdrawn', 'Withdrawn')
    ], string='Consent Status', default='pending', required=True, tracking=True)
    consent_date = fields.Datetime(string='Consent Date', readonly=True, tracking=True)
    consent_version_agreed = fields.Char(string='Consent Version Agreed', tracking=True)
    consent_purpose_ids = fields.Many2many('dfr.consent.purpose', 'dfr_farmer_consent_purpose_rel', 'farmer_id', 'purpose_id', string='Consent Purposes', tracking=True)
    consent_withdrawal_date = fields.Datetime(string='Consent Withdrawal Date', readonly=True, tracking=True)
    consent_withdrawal_reason = fields.Text(string='Consent Withdrawal Reason', tracking=True)

    deduplication_potential_duplicate_ids = fields.Many2many(
        'dfr.farmer', 'dfr_farmer_duplicate_rel', 'farmer_id', 'duplicate_id',
        string='Potential Duplicates', help="Other farmers identified as potential duplicates.")
    deduplication_master_farmer_id = fields.Many2one(
        'dfr.farmer', string='Merged Into Master', readonly=True, copy=False,
        help="If this record was merged, points to the master record.")
    active = fields.Boolean(default=True, help="Set to false to archive the record instead of deleting.") # For logical delete


    _sql_constraints = [
        ('uid_uniq', 'unique(uid, company_id)', 'Farmer UID must be unique!'), # Assuming company_id from dfr_common_core or Odoo base
        ('national_id_number_type_uniq', 'unique(national_id_number, national_id_type_id, company_id)', 'National ID Number must be unique per ID type!')
    ]

    @api.model
    def _compute_default_uid(self):
        return str(uuid.uuid4().hex)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'uid' not in vals or not vals['uid']:
                vals['uid'] = self._compute_default_uid()
            # Default status from field definition is 'pending_verification'
        records = super(DfrFarmer, self).create(vals_list)
        for record in records:
            _logger.info("DFR Farmer created: UID %s, Name %s", record.uid, record.name)
            # Trigger real-time duplicate check if enabled and on create
            if self.env['ir.config_parameter'].sudo().get_param('dfr.deduplication.realtime.enabled', 'True').lower() == 'true':
                 record._onchange_check_potential_duplicates() # Call programmatically
        return records

    def write(self, vals):
        # Log significant status changes or other auditable events if not covered by mail.thread tracking
        res = super(DfrFarmer, self).write(vals)
        if any(f in vals for f in ['name', 'national_id_number', 'date_of_birth']): # Key fields for deduplication
            if self.env['ir.config_parameter'].sudo().get_param('dfr.deduplication.realtime.enabled', 'True').lower() == 'true':
                for record in self:
                    record._onchange_check_potential_duplicates() # Call programmatically
        _logger.info("DFR Farmer %s written with values: %s", self.mapped('uid'), vals.keys())
        return res

    def unlink(self):
        _logger.info("Attempting to unlink DFR Farmers: %s. Implementing logical delete.", self.mapped('uid'))
        # Logical delete: set active to False and status to 'archived'
        # Ensure not to re-archive already archived/merged records
        records_to_archive = self.filtered(lambda r: r.active and r.status not in ('archived', 'merged_duplicate'))
        if records_to_archive:
            records_to_archive.write({'active': False, 'status': 'archived'})
            _logger.info("DFR Farmers %s logically deleted (archived).", records_to_archive.mapped('uid'))
        return True # Return True to indicate success of logical delete

    def action_request_kyc_review(self):
        self.ensure_one()
        if self.kyc_status in ('not_started', 'rejected'):
            self.write({'kyc_status': 'pending_review'})
            # Create activity for KYC review team (example)
            activity_type_id = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
            if activity_type_id:
                self.activity_schedule(
                    activity_type_id=activity_type_id.id,
                    summary=_('Review KYC for Farmer: %s') % self.name,
                    note=_('Please review the KYC details and documents for farmer %s (UID: %s).') % (self.name, self.uid),
                    # user_id=... # Assign to specific user/group if defined
                )
            _logger.info("KYC review requested for Farmer %s (UID: %s).", self.name, self.uid)
        else:
            raise ValidationError(_("KYC review can only be requested if status is 'Not Started' or 'Rejected'. Current status: %s") % self.kyc_status)

    def action_process_kyc_manual(self, outcome, notes, reviewer_id):
        self.ensure_one()
        if self.kyc_status != 'pending_review':
             raise ValidationError(_("KYC can only be processed if status is 'Pending Review'. Current status: %s") % self.kyc_status)

        vals_to_write = {
            'kyc_status': outcome,
            'kyc_verification_date': fields.Date.today(),
            'kyc_reviewer_id': reviewer_id,
            'kyc_review_notes': notes,
        }
        self.write(vals_to_write)
        _logger.info("KYC manually processed for Farmer %s (UID: %s). Outcome: %s.", self.name, self.uid, outcome)

        if outcome == 'verified' and self.status == 'pending_verification':
            self.action_set_status_active()

    def action_set_status_active(self):
        for record in self:
            if record.status != 'active':
                record.write({'status': 'active'})
                _logger.info("Farmer %s (UID: %s) status set to Active.", record.name, record.uid)

    def action_set_status_inactive(self):
        for record in self:
            if record.status != 'inactive':
                record.write({'status': 'inactive'})
                _logger.info("Farmer %s (UID: %s) status set to Inactive.", record.name, record.uid)

    def action_set_status_deceased(self):
        for record in self:
            if record.status != 'deceased':
                record.write({'status': 'deceased', 'active': False}) # Deceased implies inactive/archived
                _logger.info("Farmer %s (UID: %s) status set to Deceased.", record.name, record.uid)

    @api.onchange('name', 'date_of_birth', 'national_id_number', 'national_id_type_id', 'administrative_area_id')
    def _onchange_check_potential_duplicates(self):
        if not (self.name or self.national_id_number): # Only check if some key data is present
            if 'warning' in (self._context.get('warning') or {}): # Clear previous warning if fields are cleared
                return {'warning': False}
            return

        # Avoid check on new records not yet saved, or if service is not available
        if not self._origin and not self.id: # Check this condition logic
             return

        if self.env.context.get('deduplication_merge_in_progress', False):
            return # Skip during merge

        farmer_data = {
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'national_id_number': self.national_id_number,
            'national_id_type_id': self.national_id_type_id.id if self.national_id_type_id else False,
            'administrative_area_id': self.administrative_area_id.id if self.administrative_area_id else False,
            # Add other fields as per deduplication service config
        }
        # Use try-except as service might not be available or fuzzywuzzy not installed
        try:
            # Pass current farmer ID to exclude self from search
            current_id = self.id or (self._origin.id if self._origin else None)

            duplicates = self.env['dfr.deduplication.service'].find_potential_duplicates(
                self._name, farmer_data, current_farmer_id=current_id
            )
            if duplicates:
                # Update status to potential_duplicate if not already, and link them
                # This direct write in onchange is generally discouraged, but for immediate feedback:
                # self.status = 'potential_duplicate' # This might be too aggressive for onchange
                # self.deduplication_potential_duplicate_ids = [(6, 0, [d['id'] for d in duplicates])]
                # Better to just show a warning and let a user/batch process handle status and linking
                warning_msg = _("Potential duplicates found for this farmer based on current data:\n")
                for dup in duplicates[:3]: # Show top 3
                    dup_record = self.env['dfr.farmer'].browse(dup['id'])
                    warning_msg += _("- %s (UID: %s, Score: %s%%)\n") % (dup_record.name, dup_record.uid, dup['score'])
                if len(duplicates) > 3:
                    warning_msg += _("... and %s more.") % (len(duplicates) - 3)

                return {'warning': {'title': _("Potential Duplicates Detected!"), 'message': warning_msg}}
            elif 'warning' in (self._context.get('warning') or {}): # Clear previous warning
                 return {'warning': False}

        except Exception as e:
            _logger.error("Error during onchange duplicate check for farmer %s: %s", self.name, e)
            # Do not block UI, just log

    def action_open_deduplication_review(self):
        self.ensure_one()
        # This action opens the wizard for the current farmer
        # The wizard's default_get will handle loading this farmer
        return {
            'name': _('Review Potential Duplicates'),
            'type': 'ir.actions.act_window',
            'res_model': 'dfr.deduplication.review.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_selected_farmer_id': self.id, 'default_farmer_ids_to_review': [self.id] + self.deduplication_potential_duplicate_ids.ids},
        }

    def action_record_consent(self, consent_version_agreed, consent_purpose_ids, consent_date=None, consent_text_agreed_to_id=None):
        self.ensure_one()
        vals = {
            'consent_status': 'given',
            'consent_date': consent_date or fields.Datetime.now(),
            'consent_version_agreed': consent_version_agreed,
            'consent_purpose_ids': [(6, 0, consent_purpose_ids)],
            'consent_withdrawal_date': False, # Clear withdrawal info
            'consent_withdrawal_reason': False,
        }
        # if consent_text_agreed_to_id: vals['consent_text_agreed_to_id'] = consent_text_agreed_to_id # If such field exists
        self.write(vals)
        _logger.info("Consent recorded for Farmer %s (UID: %s). Version: %s", self.name, self.uid, consent_version_agreed)
        self.message_post(body=_("Consent granted. Version: %s. Purposes: %s") % (consent_version_agreed, ", ".join(self.consent_purpose_ids.mapped('name'))))


    def action_withdraw_consent(self, withdrawal_reason, withdrawal_date=None):
        self.ensure_one()
        if self.consent_status != 'given':
            raise ValidationError(_("Consent can only be withdrawn if it was previously 'Given'."))
        vals = {
            'consent_status': 'withdrawn',
            'consent_withdrawal_date': withdrawal_date or fields.Datetime.now(),
            'consent_withdrawal_reason': withdrawal_reason,
            # Policy: what happens to consent_purpose_ids on withdrawal? Clear them or keep for history?
            # Clearing them:
            'consent_purpose_ids': [(5, 0, 0)],
        }
        self.write(vals)
        _logger.info("Consent withdrawn for Farmer %s (UID: %s). Reason: %s", self.name, self.uid, withdrawal_reason)
        self.message_post(body=_("Consent withdrawn. Reason: %s") % withdrawal_reason)