.. _dfr_data_tools_usage_import_wizard:

=========================
Using the Bulk Data Import Wizard
=========================

Overview
========
The Bulk Data Import wizard provides a user-friendly interface for administrators to import data into various DFR (Digital Farmer Registry) models within Odoo. This tool is essential for migrating legacy data or bulk-loading new information.

To access the wizard:
1. Navigate to the "DFR" main menu.
2. Click on "Data Management".
3. Select "Bulk Data Import".

Steps for Importing Data
========================

1. Uploading a File
-------------------
- Click the "Upload File" field and select your data file.
- **Supported Formats**: CSV (Comma-Separated Values) and XLSX (Excel Spreadsheet).
- **Encoding**: Ensure files, especially CSVs, are UTF-8 encoded for compatibility.
- The file name will be automatically populated.

2. Selecting the Target DFR Model
---------------------------------
- From the "Target DFR Model" dropdown, select the Odoo model into which you want to import data (e.g., `dfr.farmer`, `dfr.household`).
- The list is typically filtered to show DFR-related models (e.g., models with technical names starting with `dfr.`).

3. Import Options
-----------------
- **Job Name**: Provide a descriptive name for this import job (e.g., "Farmer Import Batch 1 - March 2024"). This helps in tracking. Defaults to a name including the current date.
- **Skip Header Row**:
    - Check this box (default) if your CSV/XLSX file contains a header row with column names. The system will then skip this first row during data processing.
    - Uncheck if your file contains only data rows.
- **Create New Records**:
    - Check this box (default) to allow the system to create new records in the target model for rows in your file that do not match existing records.
- **Update Existing Records**:
    - Check this box if you want the system to attempt to update existing records in the target model.
    - **Important**: This functionality typically requires an "external ID" or a unique key in your source file and corresponding configuration in the import service to identify matching records. The current basic implementation might have limited update capabilities and might focus on creation. Refer to specific model import guidelines or advanced Odoo import documentation for robust update strategies.

4. Field Mapping Guidance
-------------------------
- Once a "Target DFR Model" is selected, the "Field Mapping Guidance" section will display information about the target model and some of its fields (technical name, label, type).
- **Crucial**: Your CSV/XLSX file's column headers should ideally match the **technical names** of the fields in the Odoo target model (e.g., `first_name`, `date_of_birth`, `gender_id`).
- Odoo's standard import tool (often available on list views or accessible after an initial load via tools like this) offers more advanced field mapping capabilities if your column names do not directly match or if transformations are needed. This wizard primarily facilitates the job creation and initial processing based on direct header-to-field_name matching.

5. Starting the Import
----------------------
- After configuring all options and uploading the file, click the "Start Import" button.
- The wizard will create an "Import Job" record and initiate the data processing.
- You will be redirected to the form view of the newly created "Import Job" to monitor its progress. An import progress widget may also appear on the wizard itself if the import is processed synchronously and the wizard remains open.

Monitoring Import Jobs
======================
You can track the status and results of all import attempts.

1. Navigating to Import Job History
-----------------------------------
- Go to "DFR" -> "Data Management" -> "Import Job History".
- This will display a list of all import jobs.

2. Understanding Job Statuses
-----------------------------
Each import job will have one of the following statuses:
- **Draft**: The job has been created but processing has not yet started.
- **In Progress**: The system is actively processing the file.
- **Completed (Done)**: The import process finished. This status indicates completion, but there might still be errors for individual records. Check `Successful Records` and `Failed Records` counts.
- **Error**: The import process encountered a critical error and could not complete, or a significant number of records failed.
- **Cancelled**: The job was manually cancelled (if this functionality is implemented and used).

3. Interpreting Job Summary
---------------------------
The Import Job form view provides summary counts:
- **Total Records in File**: The total number of data rows detected in your uploaded file (after skipping the header, if applicable).
- **Records Processed**: The number of rows the system has attempted to process so far.
- **Successful Records**: The number of rows that were successfully imported/created/updated in Odoo.
- **Failed Records**: The number of rows that encountered errors during validation or import.

Understanding Import Logs
=========================

1. Accessing Detailed Logs
-------------------------
- Open an "Import Job" from the history.
- Go to the "Import Logs" tab. This tab lists individual log entries for the job in a table.
- Alternatively, click the "View Detailed Logs" button (if available and logs exist) which typically opens the same log list.
- The "Log Summary" tab (or field) on the main job form provides a quick overview of the first few error messages for jobs with failures.

2. Log Entry Details
--------------------
Each log entry typically contains:
- **File Line Number**: The line number in your source file corresponding to this log message.
- **Record Identifier**: An identifier from the source row, if available (e.g., a source ID from one of the columns).
- **Log Type**:
    - `Info`: Informational message (e.g., record created successfully).
    - `Warning`: A non-critical issue was encountered (e.g., an optional field was unmapped and ignored, or a non-blocking transformation issue).
    - `Error`: A critical issue prevented the record from being imported (e.g., a required field was missing, data type mismatch, validation failure).
- **Message**: A detailed description of the event, validation failure, or error.
- **Raw Row Data**: (Optional, may be hidden by default in the list view but visible in the log entry's form view) The raw data from the source file for the problematic row, useful for debugging.

3. Common Error Types and Troubleshooting Tips
---------------------------------------------
- **Required Field Missing**: Ensure all mandatory fields in the target Odoo model have corresponding columns and values in your file.
- **Data Type Mismatch**: E.g., providing text for a number field, or an invalid date format. Check field types in Odoo (visible in Field Mapping Guidance or by inspecting the model) and format your data accordingly.
- **Relational Field Not Found**: E.g., for a Many2one field (like `country_id`), if you provide a name or ID that doesn't exist in the related model (e.g., `res.country`). Ensure related data exists in Odoo or use correct identifiers (Odoo technical ID or a name that can be uniquely resolved by `name_search`).
- **File Encoding Issues**: If special characters appear garbled, ensure your CSV is UTF-8 encoded.
- **Header Mismatch**: If the system cannot map your file's columns to Odoo fields, verify your column headers against Odoo's technical field names. Case sensitivity might also be a factor depending on the implementation.
- **Validation Error**: Custom validation rules on the Odoo model might prevent import if data doesn't conform (e.g., a phone number format, a specific value range).

Performance Considerations (REQ-DM-007)
=======================================
- For very large files (e.g., 10,000+ records), the import process can take time.
- The system is designed to process records and commit periodically (e.g., every 100 records) to manage resources and provide intermediate progress.
- If UI timeouts occur with extremely large files when the import is run synchronously from the wizard, it might indicate that a background processing mechanism (like Odoo's `queue_job`, if integrated for this service) is not fully utilized or the server resources are strained. Consult your system administrator.
- Breaking down very large datasets into smaller files can sometimes improve manageability and error tracking.