# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BulkDataImportWizard(models.TransientModel):
    _name = 'bulk.data.import.wizard'
    _description = 'Bulk Data Import Wizard'

    file_upload = fields.Binary(string='Upload File', required=True, attachment=False)
    file_name = fields.Char(string='File Name')
    target_model_id = fields.Many2one(
        'ir.model',
        string='Target DFR Model',
        required=True,
        domain="[('model', 'like', 'dfr.%')]",
        options={'no_create': True, 'no_open': True}
    )
    create_if_not_exist = fields.Boolean(
        string='Create New Records',
        default=True,
        help="If checked, new records will be created. Otherwise, only existing records will be updated."
    )
    update_existing = fields.Boolean(
        string='Update Existing Records',
        default=False,
        help="If checked, existing records matching an identifier will be updated. Requires defining an update key."
    )
    skip_header_row = fields.Boolean(string='Skip Header Row', default=True)
    field_mapping_info = fields.Text(
        string='Field Mapping Instructions',
        readonly=True,
        compute='_compute_field_mapping_info',
        help="Ensure your CSV/XLSX columns match Odoo field names or use Odoo's standard import mapping capabilities after initial load."
    )
    job_id = fields.Many2one('data.import.job', string='Created Import Job', readonly=True)
    job_name = fields.Char(
        string="Import Job Name",
        default=lambda self: f"Import {fields.Date.today().strftime('%Y-%m-%d')}"
    )

    @api.depends('target_model_id')
    def _compute_field_mapping_info(self):
        for wizard in self:
            if wizard.target_model_id:
                model_obj = self.env[wizard.target_model_id.model]
                fields_info = []
                # Get a few example fields
                count = 0
                for field_name, field_obj in model_obj._fields.items():
                    if not field_obj.automatic and not field_obj.related:
                        fields_info.append(f"- {field_name} ({field_obj.string}, type: {field_obj.type})")
                        count += 1
                        if count >= 10:
                            break
                wizard.field_mapping_info = (
                    f"Target Model: {wizard.target_model_id.name} ({wizard.target_model_id.model})\n\n"
                    "Ensure your file's column headers match the 'technical names' (or Odoo's export labels) "
                    "of the fields in the target model. \n"
                    "Odoo's standard import tool allows more advanced mapping if needed after this step.\n\n"
                    "Example fields for this model:\n" +
                    "\n".join(fields_info) +
                    ("\n..." if count == 10 and len(model_obj._fields) > 10 else "")
                )
            else:
                wizard.field_mapping_info = "Select a Target Model to see field mapping guidance."

    def _prepare_import_job_vals(self):
        self.ensure_one()
        return {
            'name': self.job_name or f"Import {self.target_model_id.name} - {self.file_name}",
            'file_name': self.file_name,
            'user_id': self.env.user.id,
            'target_model_id': self.target_model_id.id,
            'state': 'draft',
            'create_if_not_exist': self.create_if_not_exist,
            'update_existing': self.update_existing,
            # field_mapping_info could be set here if a more structured mapping is done in the wizard
            # For now, the service will log what mapping it deduced or was configured if advanced.
        }

    def action_start_import(self):
        self.ensure_one()
        if not self.file_upload or not self.target_model_id:
            raise UserError(_("Please upload a file and select a target model."))

        # Create Import Job
        job_vals = self._prepare_import_job_vals()
        job = self.env['data.import.job'].create(job_vals)
        self.job_id = job.id

        # Attach the file to the job
        # Determine mimetype based on filename extension
        mimetype = 'application/octet-stream'
        if self.file_name:
            if self.file_name.lower().endswith('.csv'):
                mimetype = 'text/csv'
            elif self.file_name.lower().endswith('.xlsx'):
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif self.file_name.lower().endswith('.xls'):
                mimetype = 'application/vnd.ms-excel'
        
        attachment = self.env['ir.attachment'].create({
            'name': self.file_name,
            'datas': self.file_upload,
            'res_model': 'data.import.job',
            'res_id': job.id,
            'mimetype': mimetype
        })
        job.attachment_id = attachment.id
        
        file_content_bytes = base64.b64decode(self.file_upload)

        # Asynchronous processing is preferred for large files.
        # For this example, direct call, but consider using `queue_job` for production.
        # self.env['data.import.service'].with_delay().process_uploaded_file(job.id, file_content_bytes, self.file_name, self.target_model_id.model, ...)
        
        # For immediate feedback or smaller jobs, can call directly:
        # Note: This will block the UI if the import is long.
        try:
            job.state = 'in_progress' # Update state before processing
            self.env.cr.commit() # Commit job state before long operation
            
            self.env['data.import.service'].process_uploaded_file(
                job_id=job.id,
                file_content_bytes=file_content_bytes, # Pass bytes directly
                file_name=self.file_name,
                target_model_name=self.target_model_id.model,
                options={
                    'create_if_not_exist': self.create_if_not_exist,
                    'update_existing': self.update_existing,
                    'skip_header_row': self.skip_header_row,
                }
            )
            # Service should update job state to 'done' or 'error'
        except Exception as e:
            job.state = 'error'
            job.message_post(body=_("Import failed critically: %s") % str(e))
            self.env.cr.commit() # Ensure error state is saved
            # Log detailed error to job or specific log entry if possible
            # The service itself should log the error in detail via _log_job_activity

        return {
            'name': _('Import Job Status'),
            'type': 'ir.actions.act_window',
            'res_model': 'data.import.job',
            'view_mode': 'form',
            'res_id': job.id,
            'target': 'current', # Or 'new' to open in a dialog
        }

    # _get_file_content is not strictly needed if passing file_upload (base64)
    # or file_content_bytes directly to service.
    # CSV reader and XLSX workbook methods would be part of the service, not the wizard.
    # action_preview_file is not specified in detail, so not implemented.