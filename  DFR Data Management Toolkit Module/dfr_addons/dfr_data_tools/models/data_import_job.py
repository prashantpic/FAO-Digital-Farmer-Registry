# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class DataImportJob(models.Model):
    _name = 'data.import.job'
    _description = 'Data Import Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Job Name', 
        required=True, 
        readonly=True, 
        states={'draft': [('readonly', False)]}, 
        index=True
    )
    file_name = fields.Char(string='Uploaded File Name', readonly=True)
    import_date = fields.Datetime(
        string='Import Started', 
        default=fields.Datetime.now, 
        readonly=True
    )
    user_id = fields.Many2one(
        'res.users', 
        string='Imported By', 
        default=lambda self: self.env.user, 
        readonly=True
    )
    target_model_id = fields.Many2one(
        'ir.model', 
        string='Target Model', 
        required=True, 
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    target_model_name = fields.Char(
        related='target_model_id.model', 
        string='Target Model Name', 
        readonly=True, 
        store=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('error', 'Error'),
        ('cancelled', 'Cancelled')
        ], 
        string='Status', 
        default='draft', 
        readonly=True, 
        tracking=True, 
        index=True
    )
    total_records_in_file = fields.Integer(
        string='Total Records in File', 
        readonly=True, 
        default=0
    )
    total_records_processed = fields.Integer(
        string='Records Processed', 
        readonly=True, 
        default=0
    )
    successful_records = fields.Integer(
        string='Successful Records', 
        readonly=True, 
        default=0
    )
    failed_records = fields.Integer(
        string='Failed Records', 
        readonly=True, 
        default=0
    )
    log_ids = fields.One2many(
        'data.import.job.log', 
        'job_id', 
        string='Import Logs', 
        readonly=True
    )
    log_summary = fields.Text(
        string='Log Summary', 
        compute='_compute_log_summary', 
        store=False, 
        readonly=True
    )
    attachment_id = fields.Many2one(
        'ir.attachment', 
        string='Uploaded File Attachment', 
        readonly=True
    )
    field_mapping_info = fields.Text(
        string='Field Mapping Info', 
        readonly=True
    )
    create_if_not_exist = fields.Boolean(
        string='Create if Not Exist', 
        default=True, 
        readonly=True
    )
    update_existing = fields.Boolean(
        string='Update Existing Records', 
        default=False, 
        readonly=True
    )

    @api.depends('log_ids.log_message', 'log_ids.log_type', 'failed_records')
    def _compute_log_summary(self):
        for job in self:
            if job.failed_records > 0:
                summary_lines = []
                error_logs = job.log_ids.filtered(lambda l: l.log_type == 'error')[:5] # Show first 5 errors
                for log_entry in error_logs:
                    summary_lines.append(f"L{log_entry.line_number or 'N/A'}: {log_entry.log_message or ''}")
                
                total_error_logs = len(job.log_ids.filtered(lambda l: l.log_type == 'error'))
                if total_error_logs > 5:
                    summary_lines.append(f"... and {total_error_logs - 5} more errors.")
                job.log_summary = "\n".join(summary_lines)
            else:
                job.log_summary = _("No errors reported.")

    def action_view_logs(self):
        self.ensure_one()
        return {
            'name': _('Import Job Logs'),
            'type': 'ir.actions.act_window',
            'res_model': 'data.import.job.log',
            'view_mode': 'tree,form',
            'domain': [('job_id', '=', self.id)],
            'context': {'default_job_id': self.id}
        }

    def action_cancel_job(self):
        """
        Cancels the import job.
        This method should implement the logic to gracefully stop any ongoing processing
        and set the job state to 'cancelled'.
        """
        for job in self:
            if job.state in ['draft', 'in_progress']:
                job.state = 'cancelled'
                job.message_post(body=_("Job cancelled by user."))
            else:
                job.message_post(body=_("Job cannot be cancelled as it is already in state: %s.") % job.state)
        return True


    def action_reprocess_failed(self):
        """
        Optional enhancement: Reprocess failed records.
        This method would typically:
        1. Check if the original file is still attached.
        2. Identify failed records from the logs.
        3. Potentially create a new job or re-use the current one (set to 'draft' or 'in_progress').
        4. Re-trigger the import process for the identified failed records.
        This requires careful consideration of data consistency and idempotency.
        """
        # Placeholder for future implementation
        self.message_post(body=_("Reprocessing failed records is not yet implemented."))
        return True