# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class DfrFarm(models.Model):
    _name = 'dfr.farm'
    _description = 'Digital Farmer Registry Farm'
    _inherit = ['mail.thread']

    name = fields.Char(string='Farm Name/Identifier', required=True, tracking=True)
    farmer_id = fields.Many2one('dfr.farmer', string='Managing Farmer', tracking=True, help="Primary farmer responsible for this farm.")
    household_id = fields.Many2one('dfr.household', string='Associated Household', tracking=True, help="Household associated with this farm.")
    plot_ids = fields.One2many('dfr.plot', 'farm_id', string='Plots')
    total_area = fields.Float(string='Total Farm Area', compute='_compute_total_area', store=True, digits=(12, 4), help="Sum of all plot sizes in their respective UoM, requires consistent UoM or conversion for meaningful sum if mixed.")
    administrative_area_id = fields.Many2one('dfr.administrative.area', string='Farm Main Location', tracking=True, help="Primary administrative area of the farm.")
    active = fields.Boolean(default=True, help="Set to false to archive the record instead of deleting.")

    _sql_constraints = [
        ('farmer_or_household_required', 'CHECK (farmer_id IS NOT NULL OR household_id IS NOT NULL)', 'A farm must be associated with either a farmer or a household.'),
        # ('name_farmer_household_uniq', 'unique(name, farmer_id, household_id, company_id)', 'Farm name must be unique per farmer/household combination.'), # This might be too strict
    ]

    @api.depends('plot_ids.size', 'plot_ids.size_unit_id')
    def _compute_total_area(self):
        # This computation assumes all plots use a comparable unit of measure (e.g. hectares)
        # or that a conversion mechanism is in place if units are mixed.
        # For simplicity, it sums sizes directly. A more robust solution would convert to a base UoM.
        for rec in self:
            # Check if all plots have the same UoM or handle conversion
            # For now, simple sum
            rec.total_area = sum(plot.size for plot in rec.plot_ids if plot.size)


    @api.model_create_multi
    def create(self, vals_list):
        records = super(DfrFarm, self).create(vals_list)
        for record in records:
            _logger.info("DFR Farm created: Name %s", record.name)
        return records

    def write(self, vals):
        res = super(DfrFarm, self).write(vals)
        _logger.info("DFR Farm %s written with values: %s", self.mapped('name'), vals.keys())
        return res

    def unlink(self):
        _logger.info("Attempting to unlink DFR Farms: %s. Implementing logical delete.", self.mapped('name'))
        # Logical delete
        records_to_archive = self.filtered(lambda r: r.active)
        if records_to_archive:
            records_to_archive.write({'active': False})
            _logger.info("DFR Farms %s logically deleted (archived).", records_to_archive.mapped('name'))
        return True