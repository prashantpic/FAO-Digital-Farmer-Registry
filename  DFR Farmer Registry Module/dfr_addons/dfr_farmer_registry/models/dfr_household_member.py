# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class DfrHouseholdMember(models.Model):
    _name = 'dfr.household_member'
    _description = 'Digital Farmer Registry Household Member'
    _inherit = ['mail.thread'] # If chatter/tracking is needed for members

    household_id = fields.Many2one('dfr.household', string='Household', required=True, ondelete='cascade', index=True)
    farmer_id = fields.Many2one('dfr.farmer', string='Registered Farmer Profile',
                                help="Link to dfr.farmer if this member is also a registered farmer (e.g., spouse, adult child who is also a farmer).")
    name = fields.Char(string='Full Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, help="Calculated from Date of Birth if available.")
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Sex', tracking=True)
    relationship_to_head_id = fields.Many2one('dfr.relationship.type', string='Relationship to Head', tracking=True)
    role_in_household = fields.Selection([ # Aligns with Farmer's role_in_household for consistency
        ('head', 'Head'), # This member is the head (rare if head_of_household_id is set on dfr.household)
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('other_relative', 'Other Relative'),
        ('non_relative', 'Non-Relative'),
        ('unknown', 'Unknown'),
    ], string='Role in Household', tracking=True, default='unknown')
    education_level_id = fields.Many2one('dfr.education.level', string='Education Level', tracking=True)
    is_farmer_record_linked = fields.Boolean(string="Is Linked to Farmer Record?", compute='_compute_is_farmer_record_linked', store=True)
    active = fields.Boolean(default=True, help="Set to false to archive the record instead of deleting.")

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                born = rec.date_of_birth
                rec.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                rec.age = 0

    @api.depends('farmer_id')
    def _compute_is_farmer_record_linked(self):
        for rec in self:
            rec.is_farmer_record_linked = bool(rec.farmer_id)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(DfrHouseholdMember, self).create(vals_list)
        for record in records:
            _logger.info("DFR Household Member created: Name %s for Household %s", record.name, record.household_id.name)
        return records

    def write(self, vals):
        res = super(DfrHouseholdMember, self).write(vals)
        _logger.info("DFR Household Member %s written with values: %s", self.mapped('name'), vals.keys())
        return res

    def unlink(self):
        # Physical delete is allowed by ondelete='cascade' from household if household is deleted.
        # If unlinking directly, it implies removal from household.
        _logger.info("Unlinking DFR Household Members: %s", self.mapped('name'))
        # If we need logical delete for members too:
        # self.write({'active': False})
        # return True
        return super(DfrHouseholdMember, self).unlink()