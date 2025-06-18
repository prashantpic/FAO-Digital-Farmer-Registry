# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class DfrForm(models.Model):
    _name = 'dfr.form'
    _description = 'Dynamic Form Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string=_("Form Title"),
        required=True,
        tracking=True
    )
    description = fields.Text(
        string=_("Description"),
        translate=True
    )
    active = fields.Boolean(
        string=_("Active"),
        default=True,
        tracking=True
    )
    form_version_ids = fields.One2many(
        comodel_name='dfr.form.version',
        inverse_name='form_master_id',
        string=_("Versions")
    )
    current_published_version_id = fields.Many2one(
        comodel_name='dfr.form.version',
        string=_("Current Published Version"),
        compute='_compute_current_published_version',
        store=True,
        help=_("The currently active and published version of this form.")
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string=_("Country"),
        tracking=True,
        help=_("Country for which this form is applicable, if specific. Used for access control or filtering if needed.")
    )

    @api.depends('form_version_ids.status', 'form_version_ids.publish_date')
    def _compute_current_published_version(self):
        for form in self:
            published_versions = form.form_version_ids.filtered(lambda v: v.status == 'published')
            if published_versions:
                # Sort by publish_date descending to get the latest one
                form.current_published_version_id = published_versions.sorted(
                    key=lambda v: v.publish_date, reverse=True
                )[0]
            else:
                form.current_published_version_id = False

    def action_create_new_version(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dfr.form.version.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_form_master_id': self.id,
            }
        }

    def action_view_versions(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('dfr_dynamic_forms.action_dfr_form_version_tree')
        action['domain'] = [('form_master_id', '=', self.id)]
        action['context'] = {'default_form_master_id': self.id}
        return action