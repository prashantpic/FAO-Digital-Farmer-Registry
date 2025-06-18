# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class DfrPlot(models.Model):
    _name = 'dfr.plot'
    _description = 'Digital Farmer Registry Plot'
    _inherit = ['mail.thread']

    farm_id = fields.Many2one('dfr.farm', string='Farm', required=True, ondelete='cascade', index=True, tracking=True)
    name = fields.Char(string='Plot Name/Identifier', required=True, tracking=True)
    size = fields.Float(string='Plot Size', digits=(12, 4), tracking=True, help="Size of the plot.")
    size_unit_id = fields.Many2one(
        'uom.uom', string='Unit of Measure',
        domain="[('category_id', '=', ref('uom.uom_categ_surface'))]", # Standard Odoo Area UoM category
        default=lambda self: self.env.ref('uom.uom_hectare', raise_if_not_found=False), # Default to hectare
        required=True, tracking=True
    )
    land_tenure_type_id = fields.Many2one('dfr.land.tenure.type', string='Land Tenure Type', tracking=True)
    primary_crop_livestock_ids = fields.Many2many(
        'dfr.crop.livestock.type', 'dfr_plot_crop_livestock_rel',
        'plot_id', 'crop_livestock_id',
        string='Primary Crops/Livestock', tracking=True
    )
    gps_latitude = fields.Float(string='GPS Latitude (Centroid)', digits=(10, 7), tracking=True, help="Latitude of the plot's approximate center.")
    gps_longitude = fields.Float(string='GPS Longitude (Centroid)', digits=(10, 7), tracking=True, help="Longitude of the plot's approximate center.")
    gps_polygon = fields.Text(string='GPS Polygon Coordinates (GeoJSON)', tracking=True,
                              help="Stores plot boundary as GeoJSON text. Example: '[[[lon1, lat1], [lon2, lat2], ...]]'")
    administrative_area_id = fields.Many2one('dfr.administrative.area', string='Administrative Area', required=True, tracking=True)
    ownership_details = fields.Text(string='Land Ownership Details', tracking=True)
    active = fields.Boolean(default=True, help="Set to false to archive the record instead of deleting.")

    # SQL Constraints if any, e.g., unique plot name within a farm
    _sql_constraints = [
        ('name_farm_uniq', 'unique(name, farm_id, company_id)', 'Plot name must be unique per farm!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(DfrPlot, self).create(vals_list)
        for record in records:
            _logger.info("DFR Plot created: Name %s for Farm %s", record.name, record.farm_id.name)
        return records

    def write(self, vals):
        res = super(DfrPlot, self).write(vals)
        _logger.info("DFR Plot %s written with values: %s", self.mapped('name'), vals.keys())
        # If size changes, the related farm's total_area needs recompute.
        # This is handled by @api.depends('plot_ids.size') on dfr.farm._compute_total_area
        return res

    def unlink(self):
        _logger.info("Attempting to unlink DFR Plots: %s. Implementing logical delete.", self.mapped('name'))
        # Logical delete
        records_to_archive = self.filtered(lambda r: r.active)
        if records_to_archive:
            records_to_archive.write({'active': False})
            _logger.info("DFR Plots %s logically deleted (archived).", records_to_archive.mapped('name'))
        # Also trigger recompute of farm's total area
        farms_to_recompute = records_to_archive.mapped('farm_id')
        if farms_to_recompute:
            farms_to_recompute._compute_total_area() # Manually trigger if unlink doesn't trigger @api.depends
        return True