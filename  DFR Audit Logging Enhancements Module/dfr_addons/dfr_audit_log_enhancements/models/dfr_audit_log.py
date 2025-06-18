# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class DfrAuditLog(models.Model):
    _name = 'dfr.audit.log'
    _description = 'DFR Audit Log'
    _order = 'timestamp desc, id desc'
    _log_access = False  # To prevent audit logging of audit log CRUD operations

    name = fields.Char(
        string='Log ID',
        readonly=True,
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('dfr.audit.log') or _('New'),
        index=True
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        index=True
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        readonly=True,
        ondelete='restrict',
        index=True,
        help="User who performed the action or system user if automated."
    )
    event_type = fields.Selection(
        selection=[
            ('login_success', 'Login Success'),
            ('login_fail', 'Login Failed'),
            ('record_create', 'Record Created'),
            ('record_update', 'Record Updated'),
            ('record_delete', 'Record Deleted'),
            ('config_change', 'Configuration Changed'),
            ('sync_event', 'Sync Event'),
            ('data_export', 'Data Exported'),
            ('security_event', 'Security Event (e.g., permission change)'),
            ('access_event', 'Access Event (e.g., sensitive data viewed)'),
            ('custom_action', 'Custom Action (Module Specific)')
        ],
        string='Event Type',
        required=True,
        readonly=True,
        index=True,
        help="Categorizes the audit event."
    )
    model_id = fields.Many2one(
        'ir.model',
        string='Target Model',
        readonly=True,
        ondelete='cascade',
        index=True,
        help="The Odoo model related to the event, if applicable."
    )
    res_id = fields.Reference(
        selection='_selection_target_model',
        string='Target Record ID',
        readonly=True,
        help="ID of the record in the Target Model"
    )
    description = fields.Text(
        string='Description',
        readonly=True,
        required=True,
        help="Human-readable summary of the event."
    )
    technical_details = fields.Text(
        string='Technical Details (JSON)',
        readonly=True,
        help="JSON formatted string potentially containing old/new values for record changes, IP address, parameters, etc."
    )
    status = fields.Selection(
        selection=[
            ('success', 'Success'),
            ('failure', 'Failure')
        ],
        string='Status',
        readonly=True,
        default='success',
        help="Indicates if the audited action was successful or failed."
    )
    session_info = fields.Char(
        string='Session Info',
        readonly=True,
        help='e.g., IP Address, User Agent'
    )

    @api.model
    def _selection_target_model(self):
        """
        Dynamically fetches all Odoo models to populate the selection
        for the res_id field.
        """
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    def init(self):
        """
        Ensures the sequence for the 'name' field is created if it doesn't exist.
        This method is called by Odoo during module initialization.
        The main definition of the sequence is in dfr_audit_log_data.xml.
        This provides a programmatic fallback or can be used for initial setup.
        """
        sequence_code = 'dfr.audit.log'
        sequence = self.env['ir.sequence'].search([('code', '=', sequence_code)], limit=1)
        if not sequence:
            self.env['ir.sequence'].sudo().create({
                'name': 'DFR Audit Log Sequence Programmatic',
                'code': sequence_code,
                'prefix': 'ALOG/',
                'padding': 6,
                'company_id': False, # Global sequence
            })
            # Log creation of sequence if a logger is available/configured
            # _logger.info(f"Created sequence '{sequence_code}' programmatically.")