# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models

# Supporting Models (as per SDS 3.6, defined here if specific and not in dfr_common_core)
# These are defined here to support data files (like dfr_national_id_type_data.xml)
# and model field definitions within this module.

class DfrEducationLevel(models.Model):
    _name = 'dfr.education.level'
    _description = 'DFR Education Level'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Education level name must be unique.'),
    ]

class DfrNationalIdType(models.Model):
    _name = 'dfr.national.id.type'
    _description = 'DFR National ID Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', help="Optionally restrict this ID type to a specific country.")
    # country_code_filter = fields.Char(string='Country Code Filter', help="Comma-separated country codes (e.g., SB,VU) if needed for filtering.")

    _sql_constraints = [
        ('name_country_uniq', 'unique (name, country_id)', 'National ID Type name must be unique per country (if country is set).'),
    ]

class DfrConsentPurpose(models.Model):
    _name = 'dfr.consent.purpose'
    _description = 'DFR Consent Purpose'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    key = fields.Char(string='Key', help="A technical key for programmatic access, e.g., 'data_sharing_research'.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Consent purpose name must be unique.'),
        ('key_uniq', 'unique (key)', 'Consent purpose key must be unique if provided.'),
    ]

class DfrRelationshipType(models.Model):
    _name = 'dfr.relationship.type'
    _description = 'DFR Relationship Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Relationship type name must be unique.'),
    ]

class DfrLandTenureType(models.Model):
    _name = 'dfr.land.tenure.type'
    _description = 'DFR Land Tenure Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Land tenure type name must be unique.'),
    ]

class DfrCropLivestockType(models.Model):
    _name = 'dfr.crop.livestock.type'
    _description = 'DFR Crop/Livestock Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Selection([
        ('crop', 'Crop'),
        ('livestock', 'Livestock')
    ], string='Type', required=True)

    _sql_constraints = [
        ('name_type_uniq', 'unique (name, type)', 'Crop/Livestock name must be unique per type.'),
    ]

# Main model imports
from . import dfr_farmer
from . import dfr_household
from . import dfr_household_member
from . import dfr_farm
from . import dfr_plot