# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import uuid
import logging

_logger = logging.getLogger(__name__)

class DfrHousehold(models.Model):
    _name = 'dfr.household'
    _description = 'Digital Farmer Registry Household'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    uid = fields.Char(string='Household UID', required=True, readonly=True, copy=False, index=True, help="Unique Household Identifier")
    name = fields.Char(string='Household Name', compute='_compute_household_name', store=True, help="Typically derived from Head of Household's name or UID if no head.")
    head_of_household_id = fields.Many2one('dfr.farmer', string='Head of Household', tracking=True, domain="[('status', '=', 'active'), ('sex', '!=', False)]") # Example domain
    member_ids = fields.One2many('dfr.household_member', 'household_id', string='Household Members')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('dissolved', 'Dissolved')
    ], string='Household Status', default='active', required=True, tracking=True)
    farm_ids = fields.One2many('dfr.farm', 'household_id', string='Farms')
    administrative_area_id = fields.Many2one(
        related='head_of_household_id.administrative_area_id',
        string='Administrative Area', store=True, readonly=True,
        help="Derived from the Head of Household's administrative area.")
    active = fields.Boolean(default=True, help="Set to false to archive the record instead of deleting.")


    _sql_constraints = [
        ('uid_uniq', 'unique(uid, company_id)', 'Household UID must be unique!'),
    ]

    @api.model
    def _compute_default_uid(self):
        return str(uuid.uuid4().hex)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'uid' not in vals or not vals['uid']:
                vals['uid'] = self._compute_default_uid()
        records = super(DfrHousehold, self).create(vals_list)
        for record in records:
            _logger.info("DFR Household created: UID %s, Name %s", record.uid, record.name)
        return records

    def write(self, vals):
        res = super(DfrHousehold, self).write(vals)
        _logger.info("DFR Household %s written with values: %s", self.mapped('uid'), vals.keys())
        return res

    def unlink(self):
        _logger.info("Attempting to unlink DFR Households: %s. Implementing logical delete.", self.mapped('uid'))
        # Logical delete
        records_to_archive = self.filtered(lambda r: r.active)
        if records_to_archive:
            records_to_archive.write({'active': False, 'status': 'dissolved'}) # Or inactive
            _logger.info("DFR Households %s logically deleted (archived/dissolved).", records_to_archive.mapped('uid'))
        return True

    @api.depends('head_of_household_id', 'head_of_household_id.name', 'uid')
    def _compute_household_name(self):
        for rec in self:
            if rec.head_of_household_id and rec.head_of_household_id.name:
                rec.name = _("Household of %s") % rec.head_of_household_id.name
            else:
                rec.name = _("Household %s") % (rec.uid or _("Unknown"))

    def action_set_status_active(self):
        for record in self:
            if record.status != 'active':
                record.write({'status': 'active'})
                _logger.info("Household %s (UID: %s) status set to Active.", record.name, record.uid)

    def action_set_status_inactive(self):
        for record in self:
            if record.status != 'inactive':
                record.write({'status': 'inactive'})
                _logger.info("Household %s (UID: %s) status set to Inactive.", record.name, record.uid)

    def action_set_status_dissolved(self):
        for record in self:
            if record.status != 'dissolved':
                record.write({'status': 'dissolved', 'active': False}) # Dissolved implies inactive/archived
                _logger.info("Household %s (UID: %s) status set to Dissolved.", record.name, record.uid)