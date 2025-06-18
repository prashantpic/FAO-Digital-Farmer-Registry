# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DfrFormSubmission(models.Model):
    _name = 'dfr.form.submission'
    _description = 'Dynamic Form Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'submission_date desc, id desc'

    name = fields.Char(
        compute='_compute_name',
        store=True,
        string=_("Submission Reference"),
        readonly=True
    )
    farmer_id = fields.Many2one(
        comodel_name='dfr.farmer', # Assuming this model comes from dfr_farmer_registry
        string=_("Farmer"),
        required=True,
        ondelete='restrict',
        tracking=True,
        index=True
    )
    form_version_id = fields.Many2one(
        comodel_name='dfr.form.version',
        string=_("Form Version"),
        required=True,
        ondelete='restrict',
        tracking=True,
        index=True
    )
    submission_date = fields.Datetime(
        string=_("Submission Date"),
        required=True,
        default=fields.Datetime.now,
        readonly=True,
        copy=False
    )
    submitted_by_user_id = fields.Many2one(
        comodel_name='res.users',
        string=_("Submitted By"),
        default=lambda self: self.env.user,
        readonly=True,
        copy=False,
        tracking=True
    )
    submission_source = fields.Selection(
        selection=[
            ('admin', _('Admin Portal')),
            ('mobile', _('Mobile App')),
            ('portal', _('Farmer Portal'))
        ],
        string=_("Source"),
        default='admin',
        tracking=True
    )
    response_ids = fields.One2many(
        comodel_name='dfr.form.response',
        inverse_name='submission_id',
        string=_("Responses"),
        copy=True # Responses should be copied if the submission is copied (though less common)
    )
    state = fields.Selection(
        selection=[
            ('draft', _('Draft')),
            ('submitted', _('Submitted')),
            ('validated', _('Validated')),
            ('rejected', _('Rejected'))
        ],
        default='submitted',
        tracking=True,
        string=_("Status"),
        copy=False,
        required=True
    )
    notes = fields.Text(
        string=_("Internal Notes"),
        translate=True
    )

    @api.depends('farmer_id.name', 'form_version_id.name', 'submission_date', 'form_version_id.form_master_id.name')
    def _compute_name(self):
        for submission in self:
            form_name = submission.form_version_id.form_master_id.name or _("Unknown Form")
            farmer_name = submission.farmer_id.name or _("Unknown Farmer")
            date_str = fields.Date.to_string(submission.submission_date.date()) if submission.submission_date else _("No Date")
            submission.name = f"{form_name} / {farmer_name} / {date_str}"

    def action_validate_submission(self):
        self.ensure_one()
        if self.state not in ['submitted', 'rejected']:
            raise UserError(_("Only submitted or rejected submissions can be validated."))
        self.write({'state': 'validated'})
        self.message_post(body=_("Submission validated."))
        # Potentially trigger notifications or other workflows here
        _logger.info(f"Submission {self.name} (ID: {self.id}) validated by {self.env.user.name}")


    def action_reject_submission(self):
        self.ensure_one()
        if self.state not in ['submitted', 'validated']:
            raise UserError(_("Only submitted or validated submissions can be rejected."))
        # Consider a wizard to capture rejection reason
        self.write({'state': 'rejected'})
        self.message_post(body=_("Submission rejected."))
        _logger.info(f"Submission {self.name} (ID: {self.id}) rejected by {self.env.user.name}")

    @api.model
    def create(self, vals):
        if 'form_version_id' in vals:
            form_version = self.env['dfr.form.version'].browse(vals['form_version_id'])
            if form_version.status != 'published':
                 _logger.warning(
                    f"Attempt to create submission for non-published form version ID {vals['form_version_id']} "
                    f"with status '{form_version.status}'."
                )
                # Depending on strictness, could raise UserError or allow for specific cases
                # For now, let's allow it but log a warning.
                # raise UserError(_("Cannot create submission for a form version that is not published."))
        submission = super(DfrFormSubmission, self).create(vals)
        _logger.info(f"Submission {submission.name} (ID: {submission.id}) created.")
        return submission

    def write(self, vals):
        res = super(DfrFormSubmission, self).write(vals)
        if 'state' in vals:
            for record in self:
                 _logger.info(f"Submission {record.name} (ID: {record.id}) state changed to {record.state} by {self.env.user.name}.")
        return res

    def unlink(self):
        for record in self:
            if record.state not in ['draft', 'rejected']: # Example policy
                raise UserError(_("Cannot delete submissions that are not in draft or rejected state."))
            _logger.info(f"Submission {record.name} (ID: {record.id}) unlinked by {self.env.user.name}.")
        return super(DfrFormSubmission, self).unlink()