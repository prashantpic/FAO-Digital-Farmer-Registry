# Software Design Specification: DFR Data Management Toolkit Module (dfr_data_tools)

## 1. Introduction

### 1.1. Purpose
This document provides the detailed software design specification for the DFR Data Management Toolkit Odoo module (`dfr_data_tools`). This module is responsible for providing tools within the Odoo Admin Portal for bulk import of legacy farmer data (from CSV/XLSX formats), including bulk data validation, field mapping capabilities, and exportable reports/extracts. It is a key component supporting data migration activities for the Digital Farmer Registry (DFR) platform.

### 1.2. Scope
The scope of this module includes:
-   User interfaces (wizards and views) for initiating and managing data import jobs.
-   Backend services for parsing, validating, transforming, and importing data into DFR Odoo models.
-   Data models for tracking import jobs and their detailed logs.
-   Configuration of Odoo's standard export features for DFR data.
-   Security configurations for accessing data management tools.
-   Technical documentation related to the module's usage and extensibility.

### 1.3. Definitions, Acronyms, and Abbreviations
-   **DFR**: Digital Farmer Registry
-   **SDS**: Software Design Specification
-   **ORM**: Object-Relational Mapper
-   **CSV**: Comma-Separated Values
-   **XLSX**: XML Spreadsheet (Excel)
-   **UI**: User Interface
-   **API**: Application Programming Interface
-   **OWL**: Odoo Web Library
-   **CRUD**: Create, Read, Update, Delete
-   **UAT**: User Acceptance Testing
-   **ETL**: Extract, Transform, Load
-   **SOP**: Standard Operating Procedure

### 1.4. References
-   DFR System Requirements Specification (SRS) Document
-   DFR Architecture Design Document
-   Odoo 18.0 Developer Documentation

## 2. System Overview
The `dfr_data_tools` module extends the Odoo platform to provide specialized data management capabilities for the DFR. It allows administrators to perform bulk data operations, primarily focused on migrating legacy data into the DFR system. Key features include a guided import wizard, data validation, error reporting, and integration with Odoo's standard export functionality. The module interacts with other DFR modules like `dfr_farmer_registry` (for target data models) and `dfr_core_common` (for shared utilities or base models if any).

## 3. Design Considerations

### 3.1. Assumptions and Dependencies
-   The module will be developed for Odoo 18.0 Community Edition.
-   Core DFR models (e.g., Farmer, Household, Plot from `dfr_farmer_registry`) are defined and accessible.
-   Odoo's standard import/export framework will be leveraged and extended where necessary.
-   Users performing data import/export will have appropriate administrative privileges.
-   Source data files (CSV/XLSX) will have a consistent structure for each import batch.

### 3.2. General Constraints
-   Performance for bulk operations on large datasets (e.g., 10,000+ records) needs to be considered.
-   Error handling and reporting must be robust and user-friendly.
-   The user interface for the import wizard should be intuitive for administrators.

### 3.3. Goals and Guidelines
-   **Modularity**: Encapsulate data management logic within this module.
-   **Reusability**: Design services and components to be potentially reusable if similar functionalities are needed elsewhere.
-   **Maintainability**: Code should be well-documented and follow Odoo and Python best practices (PEP 8).
-   **Extensibility**: Provide hooks or clear extension points for custom data transformations if required (REQ-DM-007).
-   **User-Friendliness**: Ensure administrative tools are easy to understand and operate.

## 4. System Architecture
The module follows Odoo's standard architecture:
-   **Models**: Define data structures for import jobs and logs.
-   **Wizards**: Provide UI for interactive processes like data import.
-   **Views (XML)**: Define the presentation of models and wizards.
-   **Services (Python)**: Encapsulate backend business logic for data processing.
-   **Security**: Define access rights for module components.
-   **Static Assets (JS/OWL)**: For enhanced client-side interactions, like progress display.

This module resides primarily in the `dfr_odoo_application_services` and `dfr_odoo_presentation` layers.

## 5. High-Level Design
The module will introduce:
1.  **Data Import Job Tracking**: Models `data.import.job` and `data.import.job.log` to record and detail each import attempt.
2.  **Bulk Data Import Wizard**: A transient model and associated views (`bulk.data.import.wizard`) to guide users through file upload, target model selection, (basic) field mapping, and import initiation.
3.  **Data Import Service**: A Python service (`DataImportService`) responsible for the heavy lifting: parsing files, validating rows against target model constraints, performing basic transformations, creating/updating Odoo records, and logging results.
4.  **Menu Items and Actions**: To access the wizard and view import job history.
5.  **Enhanced Progress Indication**: A client-side widget (`ImportProgressWidget`) to show real-time progress for large imports.

## 6. Detailed Design

### 6.1. Module Initialization and Manifest

#### 6.1.1. `dfr_addons/dfr_data_tools/__init__.py`
-   **Purpose**: Initializes the Python package for the `dfr_data_tools` module.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import models
    from . import wizards
    from . import services
    

#### 6.1.2. `dfr_addons/dfr_data_tools/__manifest__.py`
-   **Purpose**: Odoo module manifest file.
-   **Content**:
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'DFR Data Management Toolkit',
        'version': '18.0.1.0.0',
        'summary': 'Provides tools for bulk data import/export and migration for DFR.',
        'author': 'DFR Project Team',
        'website': 'https://www.example.com', # To be updated
        'category': 'DigitalFarmerRegistry/Tools',
        'license': 'AGPL-3', # Or MIT/Apache 2.0 as per REQ-CM-001
        'depends': [
            'base',
            'web',
            'mail', # For activity tracking on import jobs
            'dfr_farmer_registry', # Dependency for target models
            'dfr_core_common', # For any shared utilities
        ],
        'data': [
            'security/ir.model.access.csv',
            'security/dfr_data_tools_security.xml', # If custom groups are needed
            'views/dfr_data_tools_menus.xml',
            'views/bulk_data_import_wizard_views.xml',
            'views/data_import_job_views.xml',
            'views/data_import_job_log_views.xml',
        ],
        'assets': {
            'web.assets_backend': [
                'dfr_data_tools/static/src/js/import_progress_widget.js',
                'dfr_data_tools/static/src/xml/import_progress_templates.xml',
            ],
        },
        'installable': True,
        'application': False,
        'auto_install': False,
    }
    

### 6.2. Data Models (`models/`)

#### 6.2.1. `dfr_addons/dfr_data_tools/models/__init__.py`
-   **Purpose**: Initializes the models submodule.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import data_import_job
    from . import data_import_job_log
    

#### 6.2.2. `dfr_addons/dfr_data_tools/models/data_import_job.py`
-   **Purpose**: Tracks each bulk import attempt.
-   **Class**: `DataImportJob(models.Model)`
    -   `_name = 'data.import.job'`
    -   `_description = 'Data Import Job'`
    -   `_inherit = ['mail.thread', 'mail.activity.mixin']` (for tracking and communication)
    -   **Fields**:
        -   `name = fields.Char(string='Job Name', required=True, readonly=True, states={'draft': [('readonly', False)]}, index=True)`: User-defined or auto-generated job name.
        -   `file_name = fields.Char(string='Uploaded File Name', readonly=True)`
        -   `import_date = fields.Datetime(string='Import Started', default=fields.Datetime.now, readonly=True)`
        -   `user_id = fields.Many2one('res.users', string='Imported By', default=lambda self: self.env.user, readonly=True)`
        -   `target_model_id = fields.Many2one('ir.model', string='Target Model', required=True, readonly=True, states={'draft': [('readonly', False)]})`
        -   `target_model_name = fields.Char(related='target_model_id.model', string='Target Model Name', readonly=True, store=True)`
        -   `state = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Completed'), ('error', 'Error'), ('cancelled', 'Cancelled')], string='Status', default='draft', readonly=True, tracking=True, index=True)`
        -   `total_records_in_file = fields.Integer(string='Total Records in File', readonly=True, default=0)`
        -   `total_records_processed = fields.Integer(string='Records Processed', readonly=True, default=0)`
        -   `successful_records = fields.Integer(string='Successful Records', readonly=True, default=0)`
        -   `failed_records = fields.Integer(string='Failed Records', readonly=True, default=0)`
        -   `log_ids = fields.One2many('data.import.job.log', 'job_id', string='Import Logs', readonly=True)`
        -   `log_summary = fields.Text(string='Log Summary', compute='_compute_log_summary', store=False, readonly=True)`: A textual summary of errors for quick view.
        -   `attachment_id = fields.Many2one('ir.attachment', string='Uploaded File Attachment', readonly=True)`: Stores the uploaded file for reference.
        -   `field_mapping_info = fields.Text(string='Field Mapping Info', readonly=True)`: Stores JSON or textual representation of the mapping used.
        -   `create_if_not_exist = fields.Boolean(string='Create if Not Exist', default=True, readonly=True)`
        -   `update_existing = fields.Boolean(string='Update Existing Records', default=False, readonly=True)`
    -   **Methods**:
        -   `_compute_log_summary(self)`: Concatenates the first N error messages or provides a summary count.
            python
            @api.depends('log_ids.log_message')
            def _compute_log_summary(self):
                for job in self:
                    if job.failed_records > 0:
                        summary_lines = []
                        error_logs = job.log_ids.filtered(lambda l: l.log_type == 'error')[:5] # Show first 5 errors
                        for log_entry in error_logs:
                            summary_lines.append(f"L{log_entry.line_number or 'N/A'}: {log_entry.log_message or ''}")
                        if len(job.log_ids.filtered(lambda l: l.log_type == 'error')) > 5:
                            summary_lines.append(f"... and {len(job.log_ids.filtered(lambda l: l.log_type == 'error')) - 5} more errors.")
                        job.log_summary = "\n".join(summary_lines)
                    else:
                        job.log_summary = "No errors reported."
            
        -   `action_view_logs(self)`: Returns an action to open the `log_ids` tree view.
            python
            def action_view_logs(self):
                self.ensure_one()
                return {
                    'name': 'Import Job Logs',
                    'type': 'ir.actions.act_window',
                    'res_model': 'data.import.job.log',
                    'view_mode': 'tree,form',
                    'domain': [('job_id', '=', self.id)],
                    'context': {'default_job_id': self.id}
                }
            
        -   `action_cancel_job(self)`: (If applicable for jobs that can be cancelled) Sets state to 'cancelled'.
        -   `action_reprocess_failed(self)`: (Optional enhancement) Could potentially re-trigger processing for failed records if source data is still available or corrections can be applied.

#### 6.2.3. `dfr_addons/dfr_data_tools/models/data_import_job_log.py`
-   **Purpose**: Stores detailed log messages for individual records during import.
-   **Class**: `DataImportJobLog(models.Model)`
    -   `_name = 'data.import.job.log'`
    -   `_description = 'Data Import Job Log'`
    -   `_order = 'job_id, line_number, id'`
    -   **Fields**:
        -   `job_id = fields.Many2one('data.import.job', string='Import Job', required=True, ondelete='cascade', index=True)`
        -   `line_number = fields.Integer(string='File Line Number')`
        -   `record_identifier = fields.Char(string='Record Identifier')`: e.g., an ID from the source file.
        -   `log_message = fields.Text(string='Message', required=True)`
        -   `log_type = fields.Selection([('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')], string='Log Type', default='info', required=True, index=True)`
        -   `raw_row_data = fields.Text(string='Raw Row Data')`: Stores the raw data of the problematic row for inspection.

### 6.3. Wizards (`wizards/`)

#### 6.3.1. `dfr_addons/dfr_data_tools/wizards/__init__.py`
-   **Purpose**: Initializes the wizards submodule.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import bulk_data_import_wizard
    

#### 6.3.2. `dfr_addons/dfr_data_tools/wizards/bulk_data_import_wizard.py`
-   **Purpose**: UI for guiding administrators through the bulk data import.
-   **Class**: `BulkDataImportWizard(models.TransientModel)`
    -   `_name = 'bulk.data.import.wizard'`
    -   `_description = 'Bulk Data Import Wizard'`
    -   **Fields**:
        -   `file_upload = fields.Binary(string='Upload File', required=True, attachment=False)`
        -   `file_name = fields.Char(string='File Name')`
        -   `target_model_id = fields.Many2one('ir.model', string='Target DFR Model', required=True, domain="[('model', 'like', 'dfr.%')]")`: Filter for DFR models.
        -   `create_if_not_exist = fields.Boolean(string='Create New Records', default=True, help="If checked, new records will be created. Otherwise, only existing records will be updated.")`
        -   `update_existing = fields.Boolean(string='Update Existing Records', default=False, help="If checked, existing records matching an identifier will be updated. Requires defining an update key.")`
        -   `skip_header_row = fields.Boolean(string='Skip Header Row', default=True)`
        -   `field_mapping_info = fields.Text(string='Field Mapping Instructions', readonly=True, compute='_compute_field_mapping_info', help="Ensure your CSV/XLSX columns match Odoo field names or use Odoo's standard import mapping capabilities after initial load.")`: Provides basic guidance. Advanced mapping is handled by Odoo's native import if this wizard acts as a pre-processor or job creator.
        -   `job_id = fields.Many2one('data.import.job', string='Created Import Job', readonly=True)`
        -   `job_name = fields.Char(string="Import Job Name", default=lambda self: f"Import {fields.Date.today().strftime('%Y-%m-%d')}")`
    -   **Methods**:
        -   `_compute_field_mapping_info(self)`:
            python
            @api.depends('target_model_id')
            def _compute_field_mapping_info(self):
                for wizard in self:
                    if wizard.target_model_id:
                        model_obj = self.env[wizard.target_model_id.model]
                        fields_info = []
                        # Get a few example fields
                        for field_name, field_obj in list(model_obj._fields.items())[:10]: # Example: show first 10
                            if not field_obj.automatic and not field_obj.related:
                                fields_info.append(f"- {field_name} ({field_obj.string}, type: {field_obj.type})")
                        wizard.field_mapping_info = (
                            f"Target Model: {wizard.target_model_id.name} ({wizard.target_model_id.model})\n\n"
                            "Ensure your file's column headers match the 'technical names' (or Odoo's export labels) "
                            "of the fields in the target model. \n"
                            "Odoo's standard import tool allows more advanced mapping if needed after this step.\n\n"
                            "Example fields for this model:\n" +
                            "\n".join(fields_info) +
                            "\n..." if len(fields_info) == 10 else ""
                        )
                    else:
                        wizard.field_mapping_info = "Select a Target Model to see field mapping guidance."
            
        -   `action_start_import(self)`:
            -   Validates inputs (file uploaded, target model selected).
            -   Creates a `data.import.job` record in 'draft' state with relevant details (file name, user, target model, options).
            -   Attaches the uploaded file to the `data.import.job` record.
            -   Changes `data.import.job` state to 'in_progress'.
            -   Calls `DataImportService.process_uploaded_file()` asynchronously (e.g., using Odoo cron, queue_job, or a threaded approach if suitable for the specific Odoo setup and performance needs). For simplicity, a direct call can be made for smaller jobs, but for `REQ-DM-007` (large volumes), async is better.
            -   Returns an action to view the created `data.import.job` record.
            python
            def action_start_import(self):
                self.ensure_one()
                if not self.file_upload or not self.target_model_id:
                    raise UserError(_("Please upload a file and select a target model."))

                # Create Import Job
                job_vals = self._prepare_import_job_vals()
                job = self.env['data.import.job'].create(job_vals)
                self.job_id = job.id

                # Attach the file to the job
                attachment = self.env['ir.attachment'].create({
                    'name': self.file_name,
                    'datas': self.file_upload,
                    'res_model': 'data.import.job',
                    'res_id': job.id,
                    'mimetype': 'application/octet-stream' # Or detect based on file_name
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
                    self.env['data.import.service'].process_uploaded_file(
                        job_id=job.id,
                        file_content=file_content_bytes,
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
                    job.message_post(body=f"Import failed critically: {e}")
                    # Log detailed error to job or specific log entry if possible

                return {
                    'name': _('Import Job Status'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'data.import.job',
                    'view_mode': 'form',
                    'res_id': job.id,
                    'target': 'current', # Or 'new' to open in a dialog
                }
            
        -   `_prepare_import_job_vals(self)`: Helper to prepare values for `data.import.job` creation.
            python
            def _prepare_import_job_vals(self):
                return {
                    'name': self.job_name or f"Import {self.target_model_id.name} - {self.file_name}",
                    'file_name': self.file_name,
                    'user_id': self.env.user.id,
                    'target_model_id': self.target_model_id.id,
                    'state': 'draft',
                    'create_if_not_exist': self.create_if_not_exist,
                    'update_existing': self.update_existing,
                    # field_mapping_info could be set here if a more structured mapping is done in the wizard
                }
            
        -   `_get_file_content(self)`: Not strictly needed if passing `file_upload` directly.
        -   **(No parsing logic directly in wizard)** Parsing is delegated to `DataImportService`.

### 6.4. Services (`services/`)

#### 6.4.1. `dfr_addons/dfr_data_tools/services/__init__.py`
-   **Purpose**: Initializes the services submodule.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import data_import_service
    

#### 6.4.2. `dfr_addons/dfr_data_tools/services/data_import_service.py`
-   **Purpose**: Core logic for data parsing, validation, transformation, and import.
-   **Class**: `DataImportService(models.AbstractModel)` (Or a plain Python class if preferred, but AbstractModel allows easy `self.env` access)
    -   `_name = 'data.import.service'`
    -   `_description = 'DFR Data Import Service'`
    -   **Methods**:
        -   `process_uploaded_file(self, job_id, file_content, file_name, target_model_name, options)`:
            -   Retrieves the `data.import.job` record.
            -   Updates job status to 'in_progress'.
            -   Determines file type (CSV/XLSX) based on `file_name` or content sniffing.
            -   Calls `_parse_csv` or `_parse_xlsx`.
            -   Updates `job.total_records_in_file`.
            -   Calls `_validate_headers` against `target_model_name`.
            -   Iterates through rows:
                -   Calls `_process_row` for each data row.
            -   Updates job status to 'done' or 'error' based on outcomes.
            -   Updates `job.successful_records`, `job.failed_records`, `job.total_records_processed`.
            -   Handles overall exceptions using `_handle_exception`.
        -   `_parse_csv(self, file_content)`:
            -   Uses `csv.reader` to parse decoded `file_content`.
            -   Returns list of lists (rows).
        -   `_parse_xlsx(self, file_content)`:
            -   Uses `openpyxl` (or similar, needs to be added as lib dependency if not standard) to parse `file_content`.
            -   Returns list of lists (rows).
        -   `_validate_headers(self, headers, target_model_name)`:
            -   Retrieves fields of `target_model_name` using `_get_target_model_fields`.
            -   Compares `headers` with model field names (technical names).
            -   Creates a mapping `{'column_header': 'odoo_field_name'}`. Logs warnings for unmapped or unknown headers.
            -   Returns the header map. *This is a basic mapping. Odoo's built-in import tool handles more complex mapping. This service can prepare data for Odoo's tool or do direct import.*
        -   `_process_row(self, job_id, row_data_list, header_map, target_model_name, options, line_num)`:
            -   Converts `row_data_list` to a `data_dict` using `header_map`.
            -   **Data Validation**:
                -   Checks for required fields based on target model.
                -   Attempts basic type conversions (e.g., string to int/float/boolean, date strings to Odoo date format). Log errors on failure.
                -   (REQ-DM-002) Apply any specific business validation rules defined for `target_model_name`.
            -   Calls `_apply_transformations(data_dict, target_model_name)`.
            -   If validation passes, calls `_create_or_update_record`.
            -   Logs success or failure for the row to `DataImportJobLog` via `_log_job_activity`.
            -   Returns `True` on success, `False` on failure for this row.
        -   `_apply_transformations(self, data_dict, target_model_name)`:
            -   (REQ-DM-007 Extensibility Point) Placeholder for basic transformations.
            -   This method can be overridden or extended in country-specific modules to apply complex transformations if needed.
            -   Example: Standardize 'sex' field: 'M'/'Male' -> 'male'.
            -   Returns transformed `data_dict`.
        -   `_create_or_update_record(self, job_id, data_dict, target_model_name, options)`:
            -   Accesses `target_model_name` via `self.env[target_model_name]`.
            -   If `options['update_existing']` is true, attempt to find existing record (requires an update key/external ID logic, not fully detailed here but essential for updates).
            -   If updating and record found, call `record.write(data_dict)`.
            -   If `options['create_if_not_exist']` is true and no record found (or not updating), call `Model.create(data_dict)`.
            -   Handles ORM exceptions, logs them via `_log_job_activity`.
            -   Returns the created/updated Odoo recordset or `None` on failure.
        -   `_log_job_activity(self, job_id, message, level='info', record_identifier=None, line_num=None, raw_row_data=None)`:
            -   Creates a `data.import.job.log` entry.
        -   `_get_target_model_fields(self, target_model_name)`:
            -   Uses `self.env['ir.model.fields'].search([('model', '=', target_model_name)])` to get field definitions.
            -   Returns a dictionary of field names and their properties (type, required, etc.).
        -   `_handle_exception(self, job_id, exception, message_prefix="", line_num=None, record_data=None)`:
            -   Logs a general error to the `data.import.job.log`.
            -   Updates the main `data.import.job` state if it's a critical failure.

**Important Considerations for `DataImportService`**:
*   **Performance (REQ-DM-007 for large volumes)**: For very large files, process in batches. Commit transactions periodically, not after every record, to improve speed. Odoo's `cr.commit()` should be used judiciously.
*   **Error Granularity**: Log errors at the row and field level where possible.
*   **Extensibility (REQ-DM-007)**: Design `_apply_transformations` and potentially `_validate_row_custom` to be easily overridable or accept registered hook functions from other modules. This allows country-specific transformation logic without modifying the core `dfr_data_tools` module.
*   **Asynchronous Processing**: For production, use Odoo's `queue_job` or a similar mechanism to run `process_uploaded_file` in the background to prevent UI timeouts and provide better user experience. The wizard would then show the `job_id` and the user can monitor its progress.

python
# Example structure for data_import_service.py
import base64
import csv
import io
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except ImportError:
    _logger.debug("openpyxl library not found. XLSX import will not be available.")
    openpyxl = None

class DataImportService(models.AbstractModel):
    _name = 'data.import.service'
    _description = 'DFR Data Import Service'

    def _log_job_activity(self, job_id, message, level='info', record_identifier=None, line_num=None, raw_row_data=None):
        job_log_model = self.env['data.import.job.log']
        log_vals = {
            'job_id': job_id,
            'log_message': message,
            'log_type': level,
            'line_number': line_num,
            'record_identifier': record_identifier,
            'raw_row_data': str(raw_row_data) if raw_row_data else None,
        }
        job_log_model.create(log_vals)

    def _get_target_model_fields_info(self, target_model_name):
        """ Returns a dict of field_name: ir.model.fields record """
        ModelField = self.env['ir.model.fields']
        field_recs = ModelField.search([
            ('model', '=', target_model_name),
            ('store', '=', True) # Consider only stored fields
        ])
        return {field.name: field for field in field_recs}

    def _parse_csv(self, file_content_bytes):
        decoded_content = file_content_bytes.decode('utf-8') # Or try other encodings
        csv_data = csv.reader(io.StringIO(decoded_content))
        return list(csv_data)

    def _parse_xlsx(self, file_content_bytes):
        if not openpyxl:
            raise UserError(_("The 'openpyxl' library is required to import XLSX files. Please install it."))
        workbook = openpyxl.load_workbook(io.BytesIO(file_content_bytes))
        sheet = workbook.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(list(row))
        return data

    def _map_headers(self, headers, target_model_name, job_id):
        """ Basic header mapping. Logs issues. Returns {csv_header: odoo_field_name} or field_index: odoo_field_name """
        # This is a simplified version. Odoo's base_import module has more robust mapping.
        # For a production system, leverage or replicate Odoo's mapping capabilities.
        # For this example, we assume headers match Odoo technical field names.
        model_fields_info = self._get_target_model_fields_info(target_model_name)
        odoo_field_names = list(model_fields_info.keys())
        
        mapped_headers = {}
        unmapped_csv = []
        
        for i, header in enumerate(headers):
            normalized_header = str(header).strip().lower()
            found_match = False
            for odoo_field in odoo_field_names:
                if normalized_header == odoo_field.lower():
                    mapped_headers[i] = odoo_field # Map by index for simplicity
                    found_match = True
                    break
            if not found_match:
                unmapped_csv.append(header)
                self._log_job_activity(job_id, f"Column '{header}' not found in target model '{target_model_name}'. It will be ignored.", level='warning', line_num=0)
        
        if not mapped_headers:
             self._log_job_activity(job_id, "No columns could be mapped. Please check headers.", level='error', line_num=0)
             raise ValidationError(_("No columns could be mapped. Ensure CSV/XLSX headers match target model field names."))

        return mapped_headers


    def _transform_and_validate_row(self, job_id, target_model_obj, row_dict, line_num):
        """
        Apply transformations and validations.
        row_dict is {odoo_field_name: value_from_file}
        Returns validated_data_dict or raises ValidationError.
        """
        # Placeholder for custom transformations (REQ-DM-007)
        # Example: data_dict['gender'] = self._transform_gender(data_dict.get('gender'))

        # Basic Type Validation and Conversion (example)
        validated_data = {}
        errors = []
        for field_name, value in row_dict.items():
            field_obj = target_model_obj._fields.get(field_name)
            if not field_obj: # Should not happen if mapping is correct
                continue

            if value is None or str(value).strip() == "": # Handle empty values
                if field_obj.required:
                    errors.append(f"Field '{field_obj.string}' ({field_name}) is required but empty.")
                else:
                    validated_data[field_name] = False # Odoo expects False for empty non-required fields generally
                continue

            try:
                if field_obj.type == 'char':
                    validated_data[field_name] = str(value)
                elif field_obj.type == 'text':
                    validated_data[field_name] = str(value)
                elif field_obj.type == 'integer':
                    validated_data[field_name] = int(value)
                elif field_obj.type == 'float':
                    validated_data[field_name] = float(value)
                elif field_obj.type == 'boolean':
                    validated_data[field_name] = str(value).lower() in ['true', '1', 'yes']
                elif field_obj.type == 'date':
                    # Add robust date parsing here, e.g., using dateutil.parser
                    validated_data[field_name] = fields.Date.to_string(fields.Date.from_string(str(value)))
                elif field_obj.type == 'datetime':
                    validated_data[field_name] = fields.Datetime.to_string(fields.Datetime.from_string(str(value)))
                elif field_obj.type in ['many2one', 'one2many', 'many2many']:
                    # For relational fields, this is more complex.
                    # Usually, you'd import by name or external ID.
                    # Example for Many2one using name_search or exact match on 'name' (simplistic):
                    if field_obj.type == 'many2one':
                        related_model = self.env[field_obj.comodel_name]
                        # Attempt to find by name or external ID (if external IDs are used in source)
                        # This is a common area for custom logic.
                        # For now, assuming value is an ID or exact name.
                        # A robust solution would try multiple lookup strategies.
                        found_related = related_model.search([('name', '=ilike', str(value))], limit=1) \
                                     or related_model.browse(int(value) if str(value).isdigit() else -1)
                        if found_related:
                            validated_data[field_name] = found_related.id
                        else:
                            # Option: create related record if not found (if configured)
                            # Option: log error if not found
                            errors.append(f"Related record for '{field_obj.string}' with value '{value}' not found in '{field_obj.comodel_name}'.")
                else:
                    validated_data[field_name] = value # Passthrough for other types
            except ValueError as e:
                errors.append(f"Field '{field_obj.string}' ({field_name}): Invalid value '{value}'. Error: {e}")
            except Exception as e:
                 errors.append(f"Field '{field_obj.string}' ({field_name}): Unexpected error processing value '{value}'. Error: {e}")


        if errors:
            error_msg = "; ".join(errors)
            self._log_job_activity(job_id, error_msg, level='error', line_num=line_num, raw_row_data=row_dict)
            raise ValidationError(error_msg) # Raise to stop this row processing

        return validated_data

    def process_uploaded_file(self, job_id, file_content_bytes, file_name, target_model_name, options):
        job = self.env['data.import.job'].browse(job_id)
        if not job.exists():
            _logger.error(f"Import Job ID {job_id} not found.")
            return

        _logger.info(f"Starting import for job {job.name} (ID: {job.id}), file: {file_name}, target: {target_model_name}")
        job.write({'state': 'in_progress', 'import_date': fields.Datetime.now()})
        self.env.cr.commit() # Commit state change

        processed_count = 0
        success_count = 0
        error_count = 0
        
        target_model_obj = self.env[target_model_name]

        try:
            if file_name.lower().endswith('.csv'):
                rows = self._parse_csv(file_content_bytes)
            elif file_name.lower().endswith(('.xls', '.xlsx')):
                rows = self._parse_xlsx(file_content_bytes)
            else:
                raise UserError(_("Unsupported file format. Please use CSV or XLSX."))

            if not rows:
                self._log_job_activity(job_id, "File is empty or could not be parsed.", level='error')
                job.write({'state': 'error'})
                return

            job.total_records_in_file = len(rows) - (1 if options.get('skip_header_row', True) else 0)
            
            headers = rows[0]
            data_rows = rows[1:] if options.get('skip_header_row', True) else rows

            # header_map should be {csv_column_index: odoo_field_name}
            header_map = self._map_headers(headers, target_model_name, job_id)
            
            if not header_map: # map_headers logs error if it fails
                job.write({'state': 'error'})
                return

            for i, row_list_data in enumerate(data_rows):
                processed_count += 1
                line_num_in_file = i + (2 if options.get('skip_header_row', True) else 1)
                
                # Construct raw_row_dict {csv_header: value} for logging
                raw_row_dict_for_log = {headers[idx]: val for idx, val in enumerate(row_list_data) if idx < len(headers)}

                # Construct data_dict {odoo_field_name: value}
                data_dict_to_process = {}
                for col_idx, odoo_field_name in header_map.items():
                    if col_idx < len(row_list_data):
                        data_dict_to_process[odoo_field_name] = row_list_data[col_idx]
                    else:
                        data_dict_to_process[odoo_field_name] = None # Or handle missing columns

                if not any(data_dict_to_process.values()): # Skip entirely empty rows
                    self._log_job_activity(job_id, "Skipping empty row.", level='info', line_num=line_num_in_file)
                    continue

                try:
                    # Apply transformations and validations
                    validated_data = self._transform_and_validate_row(job_id, target_model_obj, data_dict_to_process, line_num_in_file)
                    
                    # Create or Update logic
                    # This is simplified. Production needs robust external ID matching for updates.
                    # For now, assumes creation if not found, or simple update based on an 'external_id' field if present
                    
                    # External ID logic placeholder:
                    # external_id_field = 'x_studio_external_id' # Example, make configurable
                    # external_id_value = validated_data.get(external_id_field)
                    # existing_record = None
                    # if options.get('update_existing') and external_id_value and external_id_field in target_model_obj._fields:
                    #    existing_record = target_model_obj.search([(external_id_field, '=', external_id_value)], limit=1)

                    # if existing_record and options.get('update_existing'):
                    #    existing_record.write(validated_data)
                    #    self._log_job_activity(job_id, "Record updated successfully.", level='info', line_num=line_num_in_file, record_identifier=str(existing_record.id))
                    #    success_count +=1
                    # elif options.get('create_if_not_exist'):
                    
                    # Simplified: always create for this example
                    if options.get('create_if_not_exist'):
                        new_record = target_model_obj.create(validated_data)
                        self._log_job_activity(job_id, f"Record created successfully with ID: {new_record.id}", level='info', line_num=line_num_in_file, record_identifier=str(new_record.id))
                        success_count += 1
                    else:
                         self._log_job_activity(job_id, "Skipped record creation (create_if_not_exist is False and no update logic matched).", level='warning', line_num=line_num_in_file)


                except ValidationError as ve: # Validation errors from _transform_and_validate_row
                    # Already logged by _transform_and_validate_row
                    error_count += 1
                except Exception as e:
                    _logger.error(f"Error processing row {line_num_in_file} for job {job.id}: {e}", exc_info=True)
                    self._log_job_activity(job_id, f"Unexpected error: {e}", level='error', line_num=line_num_in_file, raw_row_data=raw_row_dict_for_log)
                    error_count += 1
                
                if processed_count % 100 == 0: # Commit periodically for large files
                    job.write({
                        'total_records_processed': processed_count,
                        'successful_records': success_count,
                        'failed_records': error_count,
                    })
                    self.env.cr.commit()
                    _logger.info(f"Job {job.id}: Processed {processed_count}/{job.total_records_in_file} records...")


            final_state = 'done' if error_count == 0 else 'error'
            job.write({
                'state': final_state,
                'total_records_processed': processed_count,
                'successful_records': success_count,
                'failed_records': error_count,
            })
            _logger.info(f"Import job {job.name} (ID: {job.id}) finished. Status: {final_state}. Success: {success_count}, Failed: {error_count}")

        except UserError as ue: # User-friendly errors
            _logger.warning(f"UserError during import for job {job.id}: {ue.args[0]}")
            self._log_job_activity(job_id, f"Import Process Error: {ue.args[0]}", level='error')
            job.write({'state': 'error'})
        except Exception as e:
            _logger.error(f"Critical error during import for job {job.id}: {e}", exc_info=True)
            self._log_job_activity(job_id, f"Critical System Error: {e}", level='error')
            job.write({'state': 'error'})
        finally:
            self.env.cr.commit() # Ensure final state is committed



### 6.5. Views (XML)

#### 6.5.1. `dfr_addons/dfr_data_tools/views/dfr_data_tools_menus.xml`
-   **Purpose**: Defines Odoo menu items.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data>
            <!-- Main DFR Menu (if not already defined in dfr_core_common or dfr_farmer_registry) -->
            <menuitem id="menu_dfr_root" name="DFR" sequence="10" web_icon="dfr_data_tools,static/description/icon.png"/>

            <!-- Data Management Submenu -->
            <menuitem id="menu_dfr_data_management" name="Data Management" parent="menu_dfr_root" sequence="30"/>

            <menuitem id="menu_action_bulk_data_import_wizard"
                      name="Bulk Data Import"
                      parent="menu_dfr_data_management"
                      action="action_bulk_data_import_wizard_launch"
                      sequence="10"/>

            <menuitem id="menu_action_data_import_job_history"
                      name="Import Job History"
                      parent="menu_dfr_data_management"
                      action="action_data_import_job_tree"
                      sequence="20"/>
            
            <!-- Standard Odoo export is available on list views, no specific menu needed unless custom export reports are built -->

        </data>
    </odoo>
    

#### 6.5.2. `dfr_addons/dfr_data_tools/views/bulk_data_import_wizard_views.xml`
-   **Purpose**: UI for the Bulk Data Import Wizard.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <record id="view_bulk_data_import_wizard_form" model="ir.ui.view">
            <field name="name">bulk.data.import.wizard.form</field>
            <field name="model">bulk.data.import.wizard</field>
            <field name="arch" type="xml">
                <form string="Bulk Data Import">
                    <group>
                        <group>
                            <field name="job_name"/>
                            <field name="file_upload" widget="binary" filename="file_name" required="1"/>
                            <field name="file_name" invisible="1"/>
                            <field name="target_model_id" required="1" options="{'no_create': True, 'no_open': True}"/>
                        </group>
                        <group>
                            <field name="skip_header_row"/>
                            <field name="create_if_not_exist"/>
                            <field name="update_existing"/>
                        </group>
                    </group>
                    <group string="Field Mapping Guidance" attrs="{'invisible': [('target_model_id', '=', False)]}">
                         <field name="field_mapping_info" nolabel="1" class="oe_grey" readonly="1"/>
                    </group>
                     <group string="Import Job Status" attrs="{'invisible': [('job_id', '=', False)]}">
                        <field name="job_id" readonly="1" options="{'no_create': True, 'no_open': True}"/>
                        <!-- Placeholder for ImportProgressWidget if implemented and integrated here -->
                        <!-- <div class="mt16 mb16">
                            <widget name="import_progress_widget" job_id="job_id"/>
                        </div> -->
                    </group>
                    <footer>
                        <button name="action_start_import" string="Start Import" type="object" class="btn-primary" data-hotkey="q"/>
                        <button string="Cancel" class="btn-secondary" special="cancel" data-hotkey="z" />
                    </footer>
                </form>
            </field>
        </record>

        <record id="action_bulk_data_import_wizard_launch" model="ir.actions.act_window">
            <field name="name">Bulk Data Import</field>
            <field name="res_model">bulk.data.import.wizard</field>
            <field name="view_mode">form</field>
            <field name="target">new</field>
        </record>
    </odoo>
    

#### 6.5.3. `dfr_addons/dfr_data_tools/views/data_import_job_views.xml`
-   **Purpose**: Views for `data.import.job` model.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <record id="view_data_import_job_tree" model="ir.ui.view">
            <field name="name">data.import.job.tree</field>
            <field name="model">data.import.job</field>
            <field name="arch" type="xml">
                <tree string="Data Import Jobs" decoration-success="state=='done'" decoration-info="state=='in_progress'" decoration-danger="state=='error'" decoration-muted="state=='cancelled'">
                    <field name="name"/>
                    <field name="file_name"/>
                    <field name="target_model_name"/>
                    <field name="import_date"/>
                    <field name="user_id"/>
                    <field name="state"/>
                    <field name="total_records_in_file"/>
                    <field name="successful_records"/>
                    <field name="failed_records"/>
                </tree>
            </field>
        </record>

        <record id="view_data_import_job_form" model="ir.ui.view">
            <field name="name">data.import.job.form</field>
            <field name="model">data.import.job</field>
            <field name="arch" type="xml">
                <form string="Data Import Job">
                    <header>
                        <!-- Add buttons for actions like re-process, cancel if implemented -->
                         <button name="action_view_logs" type="object" string="View Detailed Logs" class="oe_highlight" attrs="{'invisible': [('log_ids', '=', [])]}"/>
                        <field name="state" widget="statusbar" statusbar_visible="draft,in_progress,done,error"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <h1><field name="name" readonly="1"/></h1>
                        </div>
                        <group>
                            <group>
                                <field name="file_name" readonly="1"/>
                                <field name="target_model_id" readonly="1" options="{'no_create': True, 'no_open': True}"/>
                                <field name="import_date" readonly="1"/>
                                <field name="user_id" readonly="1" widget="many2one_avatar_user"/>
                                <field name="attachment_id" widget="binary" filename="file_name" string="Uploaded File" readonly="1"/>
                            </group>
                            <group>
                                <field name="total_records_in_file" readonly="1"/>
                                <field name="total_records_processed" readonly="1"/>
                                <field name="successful_records" readonly="1"/>
                                <field name="failed_records" readonly="1"/>
                                <field name="create_if_not_exist" readonly="1"/>
                                <field name="update_existing" readonly="1"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Import Logs" name="import_logs">
                                <field name="log_ids" readonly="1">
                                    <tree editable="bottom" decoration-danger="log_type=='error'" decoration-warning="log_type=='warning'">
                                        <field name="line_number"/>
                                        <field name="record_identifier"/>
                                        <field name="log_type"/>
                                        <field name="log_message"/>
                                        <field name="raw_row_data" optional="hide"/>
                                    </tree>
                                </field>
                            </page>
                            <page string="Log Summary" name="log_summary_page">
                                <field name="log_summary" nolabel="1" readonly="1"/>
                            </page>
                             <page string="Field Mapping Used" name="field_mapping_page" attrs="{'invisible': [('field_mapping_info', '=', False)]}">
                                <field name="field_mapping_info" nolabel="1" readonly="1"/>
                            </page>
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record id="action_data_import_job_tree" model="ir.actions.act_window">
            <field name="name">Data Import Job History</field>
            <field name="res_model">data.import.job</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No data import jobs found.
                </p><p>
                    Use the 'Bulk Data Import' menu to start importing data.
                </p>
            </field>
        </record>
    </odoo>
    

#### 6.5.4. `dfr_addons/dfr_data_tools/views/data_import_job_log_views.xml`
-   **Purpose**: Views for `data.import.job.log`, mainly for embedding.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <record id="view_data_import_job_log_tree" model="ir.ui.view">
            <field name="name">data.import.job.log.tree</field>
            <field name="model">data.import.job.log</field>
            <field name="arch" type="xml">
                <tree string="Import Job Logs" decoration-danger="log_type=='error'" decoration-warning="log_type=='warning'">
                    <field name="job_id" optional="hide"/>
                    <field name="line_number"/>
                    <field name="record_identifier"/>
                    <field name="log_type"/>
                    <field name="log_message" string="Message"/>
                    <field name="raw_row_data" optional="hide"/>
                </tree>
            </field>
        </record>

        <record id="view_data_import_job_log_form" model="ir.ui.view">
            <field name="name">data.import.job.log.form</field>
            <field name="model">data.import.job.log</field>
            <field name="arch" type="xml">
                <form string="Import Job Log Entry">
                    <sheet>
                        <group>
                            <field name="job_id"/>
                            <field name="line_number"/>
                            <field name="record_identifier"/>
                            <field name="log_type"/>
                            <field name="log_message"/>
                            <field name="raw_row_data" attrs="{'invisible': [('raw_row_data', '=', False)]}"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
    </odoo>
    

### 6.6. Security (`security/`)

#### 6.6.1. `dfr_addons/dfr_data_tools/security/ir.model.access.csv`
-   **Purpose**: Model-level access rights.
-   **Content**:
    csv
    id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
    access_data_import_job_system_admin,data.import.job system admin access,model_data_import_job,base.group_system,1,1,1,1
    access_data_import_job_log_system_admin,data.import.job.log system admin access,model_data_import_job_log,base.group_system,1,1,1,1
    access_bulk_data_import_wizard_system_admin,bulk.data.import.wizard system admin access,model_bulk_data_import_wizard,base.group_system,1,1,1,1
    
    # If a custom group 'group_dfr_data_migration_manager' is defined:
    # access_data_import_job_migration_manager,data.import.job migration manager access,model_data_import_job,group_dfr_data_migration_manager,1,1,1,0
    # access_data_import_job_log_migration_manager,data.import.job.log migration manager access,model_data_import_job_log,group_dfr_data_migration_manager,1,1,1,0
    # access_bulk_data_import_wizard_migration_manager,bulk.data.import.wizard migration manager access,model_bulk_data_import_wizard,group_dfr_data_migration_manager,1,1,1,1
    

#### 6.6.2. `dfr_addons/dfr_data_tools/security/dfr_data_tools_security.xml` (Optional)
-   **Purpose**: Defines custom security groups if needed.
-   **Content** (Example, if a custom group is desired):
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent overriding on module update after manual changes -->
            <!-- <record id="group_dfr_data_migration_manager" model="res.groups">
                <field name="name">DFR Data Migration Manager</field>
                <field name="category_id" ref="base.module_category_administration_settings"/>
                <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
                <field name="comment">Group for users managing DFR data migration tasks.</field>
            </record> -->
        </data>
    </odoo>
    
    *Note: For now, assume `base.group_system` (Odoo Administrators) is sufficient. If more granular roles are needed, this file will be used.*

### 6.7. Static Assets (`static/src/`)

#### 6.7.1. `dfr_addons/dfr_data_tools/static/src/js/import_progress_widget.js`
-   **Purpose**: Client-side logic for real-time import progress display.
-   **Component**: `ImportProgressWidget` (OWL Component)
    -   **Properties**: `jobId` (passed from view context or parent).
    -   **State**: `progress` (0-100), `statusText`, `successfulRecords`, `failedRecords`, `totalRecordsProcessed`, `totalRecordsInFile`.
    -   **Methods**:
        -   `setup()`: Initialize state, set up polling interval.
        -   `onWillStart()`: Initial fetch of job status.
        -   `_fetchProgress()`: Makes an RPC call to a Python controller/method on `data.import.job` to get current job statistics.
            python
            # Odoo controller method (example, place in data_import_job.py or a new controller file)
            # class DataImportJobController(http.Controller):
            #     @http.route('/dfr_data_tools/job_progress/<int:job_id>', type='json', auth='user')
            #     def get_job_progress(self, job_id, **kwargs):
            #         job = request.env['data.import.job'].sudo().browse(job_id)
            #         if not job.exists():
            #             return {'error': 'Job not found'}
            #         return {
            #             'state': job.state,
            #             'total_records_in_file': job.total_records_in_file,
            #             'total_records_processed': job.total_records_processed,
            #             'successful_records': job.successful_records,
            #             'failed_records': job.failed_records,
            #         }
            
        -   Updates component state based on fetched data.
        -   `onWillUnmount()`: Clear polling interval.
    -   **Logic Description**: Polls a backend endpoint every few seconds (e.g., 3-5s) using `rpc.query` to get the status of the `data.import.job` record identified by `jobId`. Updates local state variables which are bound to the OWL template, causing the UI to refresh. Stops polling if job state is 'done', 'error', or 'cancelled'.

javascript
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, onWillUnmount, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ImportProgressWidget extends Component {
    static template = "dfr_data_tools.ImportProgressWidget";
    static props = {
        jobId: { type: Number, optional: false },
    };

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            progress: 0,
            statusText: "Initializing...",
            successfulRecords: 0,
            failedRecords: 0,
            totalRecordsProcessed: 0,
            totalRecordsInFile: 0,
            jobState: "draft",
            errorMessage: "",
        });
        this.intervalId = null;
    }

    async onWillStart() {
        await this._fetchProgress();
    }

    onMounted() {
        // Start polling only if the job is in a state that implies it's running or could run
        if (['draft', 'in_progress'].includes(this.state.jobState)) {
             this.intervalId = setInterval(async () => {
                await this._fetchProgress();
            }, 5000); // Poll every 5 seconds
        }
    }

    onWillUnmount() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }

    async _fetchProgress() {
        if (!this.props.jobId) {
            this.state.statusText = "No Job ID provided.";
            return;
        }
        try {
            const data = await this.rpc("/dfr_data_tools/job_progress/" + this.props.jobId, {});
            if (data.error) {
                this.state.statusText = `Error: ${data.error}`;
                this.state.errorMessage = `Error fetching progress: ${data.error}`;
                 if (this.intervalId) clearInterval(this.intervalId);
            } else {
                this.state.totalRecordsInFile = data.total_records_in_file || 0;
                this.state.totalRecordsProcessed = data.total_records_processed || 0;
                this.state.successfulRecords = data.successful_records || 0;
                this.state.failedRecords = data.failed_records || 0;
                this.state.jobState = data.state;

                if (this.state.totalRecordsInFile > 0) {
                    this.state.progress = Math.round((this.state.totalRecordsProcessed / this.state.totalRecordsInFile) * 100);
                } else {
                    this.state.progress = data.state === 'done' ? 100 : 0;
                }
                
                this.state.statusText = `State: ${data.state}. Processed: ${this.state.totalRecordsProcessed}/${this.state.totalRecordsInFile}. Success: ${this.state.successfulRecords}, Failed: ${this.state.failedRecords}.`;

                if (data.state === 'error' && !this.state.errorMessage) { // Fetch summary if not already set
                    const jobDetails = await this.rpc("/web/dataset/call_kw/data.import.job/read", {
                        model: "data.import.job",
                        method: "read",
                        args: [[this.props.jobId], ['log_summary']],
                        kwargs: {},
                    });
                    if (jobDetails && jobDetails.length > 0) {
                        this.state.errorMessage = jobDetails[0].log_summary || "Job failed. Check detailed logs.";
                    }
                }


                if (['done', 'error', 'cancelled'].includes(data.state)) {
                    if (this.intervalId) {
                        clearInterval(this.intervalId);
                        this.intervalId = null;
                    }
                }
            }
        } catch (error) {
            console.error("Error fetching import progress:", error);
            this.state.statusText = "Error fetching progress.";
            this.state.errorMessage = `RPC Error: ${error.message || error}`;
            if (this.intervalId) clearInterval(this.intervalId);
        }
    }
}

registry.category("view_widgets").add("import_progress_widget", ImportProgressWidget);

*Note: The RPC endpoint `/dfr_data_tools/job_progress/` needs to be defined in a Python controller.*

#### 6.7.2. `dfr_addons/dfr_data_tools/static/src/xml/import_progress_templates.xml`
-   **Purpose**: OWL template for `ImportProgressWidget`.
-   **Content**:
    xml
    <?xml version="1.0" encoding="UTF-8"?>
    <templates xml:space="preserve">
        <t t-name="dfr_data_tools.ImportProgressWidget" owl="1">
            <div class="o_import_progress_widget">
                <div t-if="props.jobId">
                    <div><strong>Import Progress:</strong></div>
                    <div class="progress mt-2 mb-2" style="height: 20px;">
                        <div class="progress-bar" role="progressbar"
                             t-attf-style="width: {{ state.progress }}%;"
                             t-att-aria-valuenow="state.progress"
                             aria-valuemin="0" aria-valuemax="100">
                            <span t-if="state.progress > 10"><t t-esc="state.progress"/>%</span>
                        </div>
                    </div>
                    <p><t t-esc="state.statusText"/></p>
                    <p t-if="state.jobState === 'error' &amp;&amp; state.errorMessage" class="text-danger">
                        <strong>Error Summary:</strong> <pre><t t-esc="state.errorMessage"/></pre>
                    </p>
                     <p t-if="state.jobState === 'done' &amp;&amp; state.failedRecords === 0" class="text-success">
                        <strong>Import completed successfully!</strong>
                    </p>
                    <p t-if="state.jobState === 'done' &amp;&amp; state.failedRecords > 0" class="text-warning">
                        <strong>Import completed with some errors. Please check the logs.</strong>
                    </p>
                </div>
                <div t-else="">
                    <p>Loading progress...</p>
                </div>
            </div>
        </t>
    </templates>
    

### 6.8. Documentation (`doc/`)

#### 6.8.1. `dfr_addons/dfr_data_tools/doc/index.rst`
-   **Purpose**: Main entry point for technical documentation.
-   **Content Outline**:
    -   Module Title: DFR Data Management Toolkit
    -   Introduction: Purpose and key features of the module (bulk import, validation, logging, export).
    -   Table of Contents (`.. toctree::`):
        -   `usage_import_wizard`
        -   `data_transformation_hooks` (if applicable)
        -   `export_functionality`

#### 6.8.2. `dfr_addons/dfr_data_tools/doc/usage_import_wizard.rst`
-   **Purpose**: Technical guide for using the import wizard and understanding logs.
-   **Content Outline**:
    -   **Overview**: How to access the Bulk Data Import wizard.
    -   **Steps for Importing Data**:
        -   Uploading a File (CSV/XLSX format requirements, encoding UTF-8).
        -   Selecting the Target DFR Model.
        -   Import Options (Skip Header, Create New, Update Existing - explain implications).
        -   Field Mapping Guidance (how Odoo expects headers, link to Odoo's general import docs for advanced mapping).
        -   Starting the Import.
    -   **Monitoring Import Jobs**:
        -   Navigating to Import Job History.
        -   Understanding Job Statuses (Draft, In Progress, Completed, Error, Cancelled).
        -   Interpreting Job Summary (Total records, Processed, Successful, Failed).
    -   **Understanding Import Logs**:
        -   Accessing Detailed Logs for a job.
        -   Log Entry Details (Line Number, Record Identifier, Log Type, Message, Raw Row Data).
        -   Common Error Types and Troubleshooting Tips.
    -   **Performance Considerations**: Notes on importing large files. (REQ-DM-007)

#### 6.8.3. `dfr_addons/dfr_data_tools/doc/data_transformation_hooks.rst`
-   **Purpose**: Guide for developers on extending data transformation capabilities.
-   **Content Outline**:
    -   **Introduction**: Purpose of custom transformations (REQ-DM-007).
    -   **Extensibility Mechanism**:
        -   How `DataImportService` allows for custom transformation logic (e.g., method overrides, specific hook points, registry pattern).
        -   Example: Creating a new module that depends on `dfr_data_tools` and overrides `_apply_transformations` for a specific target model or adds a model-specific transformation function.
    -   **Developing Custom Transformations**:
        -   Accessing row data and job context.
        -   Best practices for writing transformation functions (idempotency, error handling).
        -   Registering custom transformation functions if a registry pattern is used.
    -   **Example Transformation**:
        -   Code snippet for a common transformation scenario (e.g., concatenating fields, looking up related records based on complex criteria, data cleansing).

#### 6.8.4. `dfr_addons/dfr_data_tools/doc/export_functionality.rst`
-   **Purpose**: Guide for administrators on using Odoo's standard export features for DFR data.
-   **Content Outline**:
    -   **Overview**: How to access Odoo's export functionality from list views.
    -   **Exporting Data**:
        -   Selecting records for export (using filters and search).
        -   Choosing fields to export.
        -   Selecting export format (CSV, XLSX).
        -   "Import-Compatible Export" option.
    -   **Common DFR Models for Export**:
        -   `dfr.farmer`
        -   `dfr.household`
        -   `dfr.plot`
        -   `data.import.job` and `data.import.job.log` (for exporting import results).
    -   **Tips for Exporting**:
        -   Using saved filters.
        -   Understanding exported field names.

## 7. Data Export (REQ-DM-004)
Odoo's standard export functionality will be primarily used.
-   Users with appropriate permissions can navigate to any list view (e.g., Farmer list, Plot list, Dynamic Form Submissions list).
-   Select records (or all).
-   Click "Action" > "Export".
-   Choose fields for export.
-   Select format (CSV or Excel/XLSX).
-   The system will generate and download the file.
-   This module does not need to implement custom export logic beyond ensuring appropriate models and fields are accessible through Odoo's security and views. Training materials (REQ-TSE-001) will cover how to use Odoo's standard export.

## 8. Error Handling and Logging
-   **Import Wizard**: User-friendly error messages using `UserError` for invalid inputs.
-   **DataImportService**:
    -   Catches exceptions during file parsing, validation, transformation, and ORM operations.
    -   Logs detailed errors to `data.import.job.log` model, including line number, raw data (if possible), and specific error message.
    -   Updates the parent `data.import.job` status to 'error' if critical failures occur or if a significant number of rows fail.
    -   Uses standard Python logging (`_logger`) for service-level debug/info/error messages visible in Odoo server logs.
-   **Progress Widget**: Displays error messages fetched from the job status or summary.

## 9. Security Considerations
-   **Access Control**:
    -   `ir.model.access.csv` will restrict access to `data.import.job` and `data.import.job.log` models typically to system administrators or a dedicated "Data Migration Manager" group.
    -   The `bulk.data.import.wizard` action will also be restricted to these groups.
    -   Odoo's standard security applies to exporting data from other models (e.g., only users who can read farmer records can export them).
-   **File Uploads**:
    -   Odoo's standard mechanisms for handling binary file uploads will be used.
    -   File type validation (CSV/XLSX) will be performed.
    -   Consider constraints on file size if necessary, though Odoo itself might have system-level limits.

## 10. Performance Considerations
-   **Bulk Import (REQ-DM-007, REQ-DM-011)**:
    -   The `DataImportService` should process records in batches with periodic `self.env.cr.commit()` to avoid long transactions and high memory usage, especially for files with 10,000+ records. The batch size can be configurable (e.g., 100-500 records).
    -   Database indexes on fields used for lookups during import (e.g., external IDs for updates) are crucial and should be defined in the respective DFR entity modules (e.g., `dfr_farmer_registry`).
    -   Asynchronous processing of the import job via `queue_job` addon (if installed and permitted) or custom threading (with caution) is highly recommended to prevent UI freezes and timeouts. The progress widget will then poll the job status.
-   **Log Queries**: Indexes on `data.import.job.log.job_id` and `data.import.job.log.log_type` will improve performance when viewing logs.

## 11. Scalability
-   The design relies on Odoo's scalability features.
-   Efficient batch processing in `DataImportService` will be key for handling large data volumes.
-   The database schema for import jobs and logs is simple and should scale well with proper indexing.

## 12. Test Plan Outline
-   **Unit Tests (Python)**:
    -   Test `DataImportService` parsing for CSV and XLSX.
    -   Test validation logic for various field types and constraints.
    -   Test transformation logic (if any specific basic ones are built-in).
    -   Test error logging mechanisms.
-   **Integration Tests (Odoo)**:
    -   Test the full import wizard flow with sample valid and invalid CSV/XLSX files for key DFR models (e.g., `dfr.farmer`).
    -   Verify record creation and updates.
    -   Verify `data.import.job` and `data.import.job.log` records are created correctly.
    -   Test security: ensure only authorized users can access the wizard and job history.
    -   Test progress widget functionality (if implemented as more than a placeholder).
-   **Manual Testing/UAT**:
    -   Import larger datasets (e.g., 100, 1000, 10000 records) to check performance and progress reporting (REQ-DM-011).
    -   Verify user-friendliness of the wizard and error messages.
    -   Test Odoo's standard export functionality for key DFR models.

## 13. Documentation (REQ-TSE-001)
-   **User Manual Section**: For administrators, detailing how to use the Bulk Data Import wizard, prepare files, understand options, and interpret results/logs. How to use Odoo's standard export for DFR data.
-   **Developer Documentation (doc/*.rst)**:
    -   `index.rst`: Overview of the module.
    -   `usage_import_wizard.rst`: Technical details of the wizard, job/log models.
    -   `data_transformation_hooks.rst`: How to extend the `DataImportService` for custom transformations (REQ-DM-007).
    -   `export_functionality.rst`: Notes on leveraging Odoo's export.

This SDS provides a comprehensive plan for developing the DFR Data Management Toolkit. The key focus is on a robust and user-friendly import mechanism, leveraging Odoo's strengths while providing specific tracking and logging for DFR data migration tasks. Extensibility for transformations and considerations for performance with large datasets are important aspects of the design.