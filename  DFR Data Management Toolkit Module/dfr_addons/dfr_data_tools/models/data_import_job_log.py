# -*- coding: utf-8 -*-
from odoo import fields, models, _

class DataImportJobLog(models.Model):
    _name = 'data.import.job.log'
    _description = 'Data Import Job Log'
    _order = 'job_id, line_number, id'

    job_id = fields.Many2one(
        'data.import.job', 
        string='Import Job', 
        required=True, 
        ondelete='cascade', 
        index=True
    )
    line_number = fields.Integer(string='File Line Number')
    record_identifier = fields.Char(string='Record Identifier')
    log_message = fields.Text(string='Message', required=True)
    log_type = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error')
        ], 
        string='Log Type', 
        default='info', 
        required=True, 
        index=True
    )
    raw_row_data = fields.Text(string='Raw Row Data')