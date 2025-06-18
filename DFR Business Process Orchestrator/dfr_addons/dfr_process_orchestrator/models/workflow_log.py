# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WorkflowLog(models.Model):
    _name = 'workflow.log'
    _description = 'DFR Workflow Log'
    _order = 'create_date desc'

    name = fields.Char(string='Log Entry Name', compute='_compute_name', store=True, readonly=True)
    workflow_name = fields.Char(string='Workflow Name', required=True, index=True, help="Name or key of the workflow being logged.")
    
    related_record_model = fields.Char(string='Related Model', index=True, help="Model of the primary record this log entry relates to.")
    related_record_id = fields.Integer(string='Related Record ID', index=True, help="Database ID of the related record.")
    
    @api.model
    def _selection_target_model(self):
        # Add other relevant DFR models here as the system grows
        return [
            ('dfr.farmer', 'Farmer'),
            ('dfr.household', 'Household'),
            ('dfr.farm', 'Farm'),
            ('dfr.plot', 'Plot'),
            ('dfr.form.submission', 'Form Submission'),
            ('res.users', 'User'),
            # Add other models that might be part of workflows
        ]

    related_record_ref = fields.Reference(
        selection='_selection_target_model', 
        string='Related Record', 
        compute='_compute_related_record_ref', 
        store=True, # Storing for easier searching/filtering if needed
        readonly=True,
        help="Reference to the primary record associated with this log entry."
    )
    
    message = fields.Text(string='Message', required=True, help="Detailed log message.")
    level = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug')
        ], string='Level', required=True, default='info', index=True, help="Severity level of the log entry.")
    
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, index=True, help="User who triggered or is associated with the event.")
    # create_date is an Odoo default field (Datetime, string='Timestamp', readonly=True, default=fields.Datetime.now)

    @api.depends('workflow_name', 'create_date')
    def _compute_name(self):
        for log in self:
            ts = fields.Datetime.to_string(log.create_date) if log.create_date else 'No Timestamp'
            log.name = f"Log: {log.workflow_name or 'Unnamed Workflow'} - {ts}"

    @api.depends('related_record_model', 'related_record_id')
    def _compute_related_record_ref(self):
        for log in self:
            if log.related_record_model and log.related_record_id:
                try:
                    # Validate that the model exists before creating the reference string
                    self.env[log.related_record_model].browse(log.related_record_id).check_access_rights('read', raise_exception=False)
                    log.related_record_ref = f"{log.related_record_model},{log.related_record_id}"
                except Exception: # Catch if model does not exist or ID is invalid
                    log.related_record_ref = False
            else:
                log.related_record_ref = False
    
    @api.model
    def log_event(self, workflow_name, message, level='info', record=None, user_id=None):
        """
        Creates a new workflow.log entry.
        :param workflow_name: str, Name of the workflow.
        :param message: str, The log message.
        :param level: str, Log level ('info', 'warning', 'error', 'debug').
        :param record: Odoo recordset, optional, The primary record associated with the event.
        :param user_id: int, optional, ID of the user performing the action; defaults to current user's ID.
        :return: The created workflow.log record.
        """
        vals = {
            'workflow_name': workflow_name,
            'message': message,
            'level': level,
            'user_id': user_id if user_id is not None else self.env.user.id,
        }
        if record and isinstance(record, models.BaseModel) and len(record) == 1: # Ensure it's a single record
            vals['related_record_model'] = record._name
            vals['related_record_id'] = record.id
        
        return self.create(vals)