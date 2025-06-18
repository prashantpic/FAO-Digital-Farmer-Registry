# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DfrFormVersion(models.Model):
    _name = 'dfr.form.version'
    _description = 'Dynamic Form Version'
    _inherit = ['mail.thread']
    _order = 'form_master_id, version_number desc'

    form_master_id = fields.Many2one(
        comodel_name='dfr.form',
        string=_("Form Master"),
        required=True,
        ondelete='cascade',
        tracking=True
    )
    version_number = fields.Char(
        string=_("Version Number"),
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: _('New')
    )
    name = fields.Char(
        related='form_master_id.name',
        store=True,
        string=_("Form Name"),
        readonly=True
    )
    description = fields.Text(
        string=_("Version Description"),
        translate=True
    )
    status = fields.Selection(
        selection=[
            ('draft', _('Draft')),
            ('published', _('Published')),
            ('archived', _('Archived'))
        ],
        default='draft',
        string=_("Status"),
        tracking=True,
        copy=False,
        required=True
    )
    publish_date = fields.Datetime(
        string=_("Publish Date"),
        readonly=True,
        copy=False
    )
    archive_date = fields.Datetime(
        string=_("Archive Date"),
        readonly=True,
        copy=False
    )
    field_ids = fields.One2many(
        comodel_name='dfr.form.field',
        inverse_name='form_version_id',
        string=_("Fields"),
        copy=True
    )
    submission_count = fields.Integer(
        compute='_compute_submission_count',
        string=_("Submissions"),
        store=False # Dynamic computation
    )
    can_be_published = fields.Boolean(
        compute='_compute_can_be_published',
        string=_("Can Publish?")
    )
    can_be_archived = fields.Boolean(
        compute='_compute_can_be_archived',
        string=_("Can Archive?")
    )
    is_editable = fields.Boolean(
        compute='_compute_is_editable',
        string=_("Is Editable?"),
        help=_("Indicates if the form version (fields) can still be edited. Typically true only in 'draft' state.")
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('version_number', _('New')) == _('New'):
                form_master_id = vals.get('form_master_id')
                if form_master_id:
                    vals['version_number'] = self.env['ir.sequence'].next_by_code('dfr.form.version.sequence') or _('New')
                else: # Should not happen if form_master_id is required, but good practice
                    vals['version_number'] = self.env['ir.sequence'].next_by_code('dfr.form.version.sequence') or _('New')
        return super().create(vals_list)

    def action_publish(self):
        for version in self:
            if version.status != 'draft':
                raise UserError(_("Only draft versions can be published."))
            if not version.field_ids:
                raise UserError(_("Cannot publish a form version with no fields defined."))

            # Archive other published versions of the same form master
            other_published_versions = self.env['dfr.form.version'].search([
                ('form_master_id', '=', version.form_master_id.id),
                ('status', '=', 'published'),
                ('id', '!=', version.id)
            ])
            other_published_versions.action_archive()

            version.write({
                'status': 'published',
                'publish_date': fields.Datetime.now()
            })
            version.form_master_id._compute_current_published_version() # Trigger recompute
            version.message_post(body=_("Form version published."))
        return True

    def action_archive(self):
        for version in self:
            if version.status not in ['draft', 'published']:
                raise UserError(_("Only draft or published versions can be archived."))
            
            was_current_published = (version.form_master_id.current_published_version_id == version)
            
            version.write({
                'status': 'archived',
                'archive_date': fields.Datetime.now()
            })
            
            if was_current_published:
                version.form_master_id._compute_current_published_version() # Trigger recompute

            version.message_post(body=_("Form version archived."))
        return True

    def action_set_to_draft(self):
        for version in self:
            if version.status != 'archived': # Or any other state we allow from
                raise UserError(_("Only archived versions can be set back to draft."))
            
            was_current_published = (version.form_master_id.current_published_version_id == version)

            version.write({
                'status': 'draft',
                'publish_date': False,
                'archive_date': False
            })

            if was_current_published:
                 version.form_master_id._compute_current_published_version() # Trigger recompute
            version.message_post(body=_("Form version set to draft."))
        return True

    def _compute_submission_count(self):
        for version in self:
            version.submission_count = self.env['dfr.form.submission'].search_count(
                [('form_version_id', '=', version.id)]
            )

    @api.depends('status')
    def _compute_can_be_published(self):
        for version in self:
            version.can_be_published = (version.status == 'draft')

    @api.depends('status')
    def _compute_can_be_archived(self):
        for version in self:
            version.can_be_archived = (version.status in ['draft', 'published'])

    @api.depends('status')
    def _compute_is_editable(self):
        for version in self:
            version.is_editable = (version.status == 'draft')

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            'status': 'draft',
            'publish_date': False,
            'archive_date': False,
            'version_number': self.env['ir.sequence'].next_by_code('dfr.form.version.sequence') or _('New'),
            'description': _("Copy of %s", self.description or self.name),
            'submission_count': 0, # Reset submission count for the new copy
        })
        new_version = super(DfrFormVersion, self).copy(default)
        # Deep copy of fields is handled by copy=True on field_ids one2many
        # but ensure their form_version_id is set to the new version
        # This is typically handled by Odoo's copy mechanism for one2many with copy=True
        
        # Odoo's copy mechanism for One2many with copy=True already handles this correctly.
        # If any specific post-copy logic for fields is needed, it would go here.
        # For example, if field names needed to be reset or slightly altered.

        return new_version

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.form_master_id.name} ({record.version_number})"
            result.append((record.id, name))
        return result