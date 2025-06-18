# Specification

# 1. Files

- **Path:** dfr_addons/dfr_data_tools/__init__.py  
**Description:** Initializes the Python package for the dfr_data_tools module, importing submodules like models, wizards, and services.  
**Template:** Odoo Python Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python modules within dfr_data_tools accessible.  
**Logic Description:** Contains import statements for ./models, ./wizards, ./services.  
**Documentation:**
    
    - **Summary:** Standard Odoo module Python package initializer.
    
**Namespace:** odoo.addons.dfr_data_tools  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_data_tools/__manifest__.py  
**Description:** Odoo module manifest file for DFR Data Management Toolkit. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Declaration
    
**Requirement Ids:**
    
    - REQ-DM-001
    
**Purpose:** Declares the dfr_data_tools module to Odoo, specifying its properties, dependencies (base, web, dfr_farmer_registry, dfr_core_common), and files to load.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'category', 'depends', 'data', 'assets'. 'depends' will include 'base', 'web', 'dfr_farmer_registry', 'dfr_core_common'. 'data' will list XML files from views/ and security/.  
**Documentation:**
    
    - **Summary:** Defines metadata and resource loading for the dfr_data_tools Odoo module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_data_tools/models/__init__.py  
**Description:** Initializes the Python package for models within the dfr_data_tools module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Submodule Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all model files within this directory to make them accessible to Odoo.  
**Logic Description:** Contains import statements for data_import_job.py and data_import_job_log.py.  
**Documentation:**
    
    - **Summary:** Initializes the models submodule.
    
**Namespace:** odoo.addons.dfr_data_tools.models  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_data_tools/models/data_import_job.py  
**Description:** Odoo model to store metadata and status for each bulk data import job.  
**Template:** Odoo Model  
**Dependancy Level:** 2  
**Name:** DataImportJob  
**Type:** Model  
**Relative Path:** models/data_import_job.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** file_name  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** import_date  
**Type:** fields.Datetime  
**Attributes:**   
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:**   
    - **Name:** state  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** total_records_processed  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** successful_records  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** failed_records  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** log_ids  
**Type:** fields.One2many  
**Attributes:**   
    - **Name:** log_summary  
**Type:** fields.Text  
**Attributes:** compute=_compute_log_summary  
    - **Name:** target_model_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name=ir.model  
    
**Methods:**
    
    - **Name:** _compute_log_summary  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - Import Job Tracking
    - Status Management
    - Summary Reporting
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Tracks each bulk import attempt, its status (e.g., pending, processing, completed, failed), number of records processed, success/failure counts, and links to detailed logs.  
**Logic Description:** Defines fields for job name (e.g., from wizard), file name, date, user, state (selection: draft, in_progress, done, error), record counts. Includes a One2many field to 'data.import.job.log'.  
**Documentation:**
    
    - **Summary:** Model representing a single bulk data import execution instance.
    
**Namespace:** odoo.addons.dfr_data_tools.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_data_tools/models/data_import_job_log.py  
**Description:** Odoo model to store detailed log messages for individual records that failed during a bulk import job.  
**Template:** Odoo Model  
**Dependancy Level:** 2  
**Name:** DataImportJobLog  
**Type:** Model  
**Relative Path:** models/data_import_job_log.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    - ActiveRecord
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** job_id  
**Type:** fields.Many2one  
**Attributes:**   
    - **Name:** line_number  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** record_identifier  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** log_message  
**Type:** fields.Text  
**Attributes:**   
    - **Name:** log_type  
**Type:** fields.Selection  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - Detailed Error Logging
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Stores individual error or validation messages related to specific rows/records from an import file, linked to a parent DataImportJob.  
**Logic Description:** Defines fields for the related job (Many2one to 'data.import.job'), line number from source file, failing record's identifier (if available), and the detailed error message.  
**Documentation:**
    
    - **Summary:** Model representing a log entry for a specific record within an import job.
    
**Namespace:** odoo.addons.dfr_data_tools.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_data_tools/wizards/__init__.py  
**Description:** Initializes the Python package for wizards within the dfr_data_tools module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** wizards/__init__.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Submodule Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all wizard files within this directory to make them accessible to Odoo.  
**Logic Description:** Contains import statements for bulk_data_import_wizard.py.  
**Documentation:**
    
    - **Summary:** Initializes the wizards submodule.
    
**Namespace:** odoo.addons.dfr_data_tools.wizards  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_data_tools/wizards/bulk_data_import_wizard.py  
**Description:** Odoo wizard for guiding administrators through the bulk data import process.  
**Template:** Odoo Wizard  
**Dependancy Level:** 3  
**Name:** BulkDataImportWizard  
**Type:** Wizard  
**Relative Path:** wizards/bulk_data_import_wizard.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** file_upload  
**Type:** fields.Binary  
**Attributes:**   
    - **Name:** file_name  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** target_model_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name=ir.model  
    - **Name:** create_if_not_exist  
**Type:** fields.Boolean  
**Attributes:**   
    - **Name:** update_existing  
**Type:** fields.Boolean  
**Attributes:**   
    - **Name:** field_mapping_info  
**Type:** fields.Text  
**Attributes:** readonly=True  
    - **Name:** job_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name=data.import.job  
    
**Methods:**
    
    - **Name:** action_preview_file  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** action_start_import  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** _prepare_import_job_vals  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** _get_file_content  
**Parameters:**
    
    - self
    
**Return Type:** bytes  
**Attributes:** private  
    - **Name:** _get_csv_reader  
**Parameters:**
    
    - self
    - file_content
    
**Return Type:** csv.reader  
**Attributes:** private  
    - **Name:** _get_xlsx_workbook  
**Parameters:**
    
    - self
    - file_content
    
**Return Type:** openpyxl.Workbook  
**Attributes:** private  
    
**Implemented Features:**
    
    - File Upload (CSV/XLSX)
    - Target Model Selection
    - Basic Field Mapping Guidance
    - Import Option Configuration
    - Import Process Initiation
    - Link to Import Job for Status/Logs
    
**Requirement Ids:**
    
    - REQ-DM-001
    - REQ-DM-002
    
**Purpose:** Provides a step-by-step UI for administrators to upload data files (CSV, XLSX), select target DFR models, configure import options, and initiate the import process.  
**Logic Description:** Inherits from TransientModel. Defines fields for file upload, target model, import options (e.g., create new, update existing). Methods to handle file parsing (delegating to service), preview data, trigger the import process (which calls DataImportService), and display progress/results by linking to a DataImportJob record.  
**Documentation:**
    
    - **Summary:** Wizard model guiding users through the bulk data import steps.
    
**Namespace:** odoo.addons.dfr_data_tools.wizards  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/services/__init__.py  
**Description:** Initializes the Python package for services within the dfr_data_tools module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** services/__init__.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Submodule Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all service files within this directory to make them accessible.  
**Logic Description:** Contains import statements for data_import_service.py.  
**Documentation:**
    
    - **Summary:** Initializes the services submodule.
    
**Namespace:** odoo.addons.dfr_data_tools.services  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_data_tools/services/data_import_service.py  
**Description:** Service layer handling the core logic of data parsing, validation, transformation, and import into DFR models.  
**Template:** Odoo Python Service  
**Dependancy Level:** 2  
**Name:** DataImportService  
**Type:** Service  
**Relative Path:** services/data_import_service.py  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    - job_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_uploaded_file  
**Parameters:**
    
    - self
    - file_content
    - file_name
    - target_model_name
    - options
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _parse_csv  
**Parameters:**
    
    - self
    - file_content
    
**Return Type:** list  
**Attributes:** private  
    - **Name:** _parse_xlsx  
**Parameters:**
    
    - self
    - file_content
    
**Return Type:** list  
**Attributes:** private  
    - **Name:** _validate_headers  
**Parameters:**
    
    - self
    - headers
    - target_model_name
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** _process_row  
**Parameters:**
    
    - self
    - row_data
    - header_map
    - target_model_name
    - options
    - line_num
    
**Return Type:** bool  
**Attributes:** private  
    - **Name:** _apply_transformations  
**Parameters:**
    
    - self
    - data_dict
    - target_model_name
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** _create_or_update_record  
**Parameters:**
    
    - self
    - data_dict
    - target_model_name
    - options
    
**Return Type:** recordset  
**Attributes:** private  
    - **Name:** _log_job_activity  
**Parameters:**
    
    - self
    - message
    - level='info'
    - record_identifier=None
    - line_num=None
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _get_target_model_fields  
**Parameters:**
    
    - self
    - target_model_name
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** _handle_exception  
**Parameters:**
    
    - self
    - exception
    - line_num=None
    - record_data=None
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - File Parsing (CSV, XLSX)
    - Data Validation against Schema
    - Configurable Data Transformation Hooks
    - Odoo Record Creation/Update
    - Detailed Error Logging to DataImportJobLog
    - Progress Tracking Update to DataImportJob
    
**Requirement Ids:**
    
    - REQ-DM-001
    - REQ-DM-002
    - REQ-DM-007
    
**Purpose:** Encapsulates the business logic for processing imported data files. It is called by the import wizard and performs validation, transformation, and interaction with Odoo's ORM.  
**Logic Description:** Class with methods to: load data from CSV/XLSX; iterate through rows; validate data types and constraints against target Odoo model (e.g., 'dfr.farmer'); apply basic transformations; call custom transformation hooks if defined (for REQ-DM-007 extensibility); create or update Odoo records; log successes and failures to DataImportJob and DataImportJobLog. Utilizes Odoo environment (self.env).  
**Documentation:**
    
    - **Summary:** Core service for handling the backend processing of bulk data imports.
    
**Namespace:** odoo.addons.dfr_data_tools.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_data_tools/views/dfr_data_tools_menus.xml  
**Description:** Defines menu items for accessing the Data Management Toolkit features in the Odoo admin interface.  
**Template:** Odoo XML View  
**Dependancy Level:** 1  
**Name:** dfr_data_tools_menus  
**Type:** Odoo Menu  
**Relative Path:** views/dfr_data_tools_menus.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Menu Configuration
    
**Requirement Ids:**
    
    - REQ-DM-001
    - REQ-DM-002
    
**Purpose:** Creates top-level or sub-level menu items in Odoo for users to access the 'Bulk Data Import' wizard and 'Import Jobs' history.  
**Logic Description:** XML defining <menuitem> records. One menu item to launch the 'bulk.data.import.wizard' action, and another to open the tree view of 'data.import.job'.  
**Documentation:**
    
    - **Summary:** Configures navigation menus for the Data Management Toolkit.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/views/bulk_data_import_wizard_views.xml  
**Description:** Defines the Odoo views (form, action) for the Bulk Data Import Wizard.  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** bulk_data_import_wizard_views  
**Type:** Odoo View  
**Relative Path:** views/bulk_data_import_wizard_views.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard UI Definition
    
**Requirement Ids:**
    
    - REQ-DM-001
    
**Purpose:** Provides the user interface for the bulk data import wizard, including fields for file upload, model selection, and action buttons.  
**Logic Description:** XML defining an <act_window> record to launch the wizard and a <form> view for the 'bulk.data.import.wizard' model. The form view will contain fields for file_upload, target_model_id, etc., and buttons for actions like 'Preview File' and 'Start Import'.  
**Documentation:**
    
    - **Summary:** Defines the form view and action for the bulk data import wizard.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/views/data_import_job_views.xml  
**Description:** Defines Odoo views (tree/list, form) for the Data Import Job model.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** data_import_job_views  
**Type:** Odoo View  
**Relative Path:** views/data_import_job_views.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Import Job History UI
    - Import Job Detail UI
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Allows administrators to view a history of import jobs, their status, and summary information. Form view allows drilling down into details and associated logs.  
**Logic Description:** XML defining <tree> and <form> views for the 'data.import.job' model. The tree view shows key job info. The form view shows all job details and includes the One2many field 'log_ids' to display related DataImportJobLog records (potentially using a nested tree view for logs).  
**Documentation:**
    
    - **Summary:** Defines list and form views for managing and reviewing data import jobs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/views/data_import_job_log_views.xml  
**Description:** Defines Odoo views (tree/list, form) for the Data Import Job Log model, primarily for display within the DataImportJob form.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** data_import_job_log_views  
**Type:** Odoo View  
**Relative Path:** views/data_import_job_log_views.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Import Error Log Display
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Provides views for displaying detailed error messages associated with an import job, typically embedded in the DataImportJob form view.  
**Logic Description:** XML defining <tree> and <form> views for the 'data.import.job.log' model. The tree view is primarily used within the 'data.import.job' form view to list logs. A separate form view for 'data.import.job.log' allows viewing individual log details if necessary.  
**Documentation:**
    
    - **Summary:** Defines list and form views for individual import job log entries.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/security/ir.model.access.csv  
**Description:** Defines model-level access rights for the custom models in the dfr_data_tools module.  
**Template:** Odoo CSV Data  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** Odoo Security  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Access Control Configuration
    
**Requirement Ids:**
    
    - REQ-DM-001
    - REQ-DM-002
    
**Purpose:** Specifies which user groups have read, write, create, and delete permissions for the 'data.import.job' and 'data.import.job.log' models.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Entries for 'data.import.job' and 'data.import.job.log', typically granting full access to admin groups (e.g., 'base.group_system') or a custom 'Data Migration Administrator' group.  
**Documentation:**
    
    - **Summary:** Manages CRUD permissions for custom data management models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_data_tools/security/dfr_data_tools_security.xml  
**Description:** Defines custom security groups related to data management functionalities, if needed.  
**Template:** Odoo XML Data  
**Dependancy Level:** 0  
**Name:** dfr_data_tools_security  
**Type:** Odoo Security  
**Relative Path:** security/dfr_data_tools_security.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom User Group Definition
    
**Requirement Ids:**
    
    - REQ-DM-001
    
**Purpose:** Creates specific user roles/groups (e.g., 'Data Migration Manager') if granular control over data management tools is required beyond standard Odoo groups.  
**Logic Description:** XML file defining <record> entries for 'res.groups'. For example, a group 'group_dfr_data_migration_manager' inheriting from 'base.group_user' or 'base.group_system'. This is optional if standard admin groups suffice.  
**Documentation:**
    
    - **Summary:** Defines custom security groups for data management toolkit access.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_data_tools/static/src/js/import_progress_widget.js  
**Description:** JavaScript for a custom import progress widget, providing enhanced visual feedback during long import operations.  
**Template:** Odoo JavaScript (OWL Component)  
**Dependancy Level:** 1  
**Name:** ImportProgressWidget  
**Type:** JavaScript UI Component  
**Relative Path:** static/src/js/import_progress_widget.js  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    - MVVM (OWL)
    
**Members:**
    
    - **Name:** jobId  
**Type:** Number  
**Attributes:**   
    - **Name:** progress  
**Type:** Number  
**Attributes:**   
    - **Name:** statusText  
**Type:** String  
**Attributes:**   
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _fetchProgress  
**Parameters:**
    
    
**Return Type:** Promise  
**Attributes:** private  
    - **Name:** onWillStart  
**Parameters:**
    
    
**Return Type:** Promise  
**Attributes:** public  
    - **Name:** onWillUnmount  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Real-time Import Progress Display
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Provides a client-side component to poll the backend (e.g., DataImportJob status) and display a more dynamic progress bar or status updates than standard Odoo wizards might offer for long-running tasks.  
**Logic Description:** An OWL component that takes a 'data.import.job' ID. It periodically calls a controller or reads data from the job record to update its progress display (e.g., percentage, records processed). Should handle polling intervals and stop polling when the job is complete or failed.  
**Documentation:**
    
    - **Summary:** Client-side JavaScript component for displaying import progress.
    
**Namespace:** dfr_data_tools.ImportProgressWidget  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/static/src/xml/import_progress_templates.xml  
**Description:** OWL templates for the custom import progress widget.  
**Template:** Odoo XML (OWL Template)  
**Dependancy Level:** 0  
**Name:** import_progress_templates  
**Type:** OWL Template  
**Relative Path:** static/src/xml/import_progress_templates.xml  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Import Progress UI Structure
    
**Requirement Ids:**
    
    - REQ-DM-002
    
**Purpose:** Defines the HTML structure and presentation logic for the ImportProgressWidget using OWL templating syntax.  
**Logic Description:** XML containing <t t-name='dfr_data_tools.ImportProgressWidget'>...</t> defining the visual elements like a progress bar, status text, and record counts, bound to the JavaScript component's state.  
**Documentation:**
    
    - **Summary:** OWL templates for rendering the import progress indicator.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_data_tools/doc/index.rst  
**Description:** Root file for the technical documentation of the dfr_data_tools module, typically for Sphinx.  
**Template:** ReStructuredText  
**Dependancy Level:** 0  
**Name:** index  
**Type:** Documentation  
**Relative Path:** doc/index.rst  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Technical Documentation Index
    
**Requirement Ids:**
    
    - REQ-TSE-001
    
**Purpose:** Serves as the main entry point for the module's technical documentation, outlining its purpose and linking to other documentation pages.  
**Logic Description:** Contains a title, brief introduction to the module, and a toctree directive listing other .rst files like usage_import_wizard.rst and data_transformation_hooks.rst.  
**Documentation:**
    
    - **Summary:** Main index for the dfr_data_tools module's technical documentation.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** dfr_addons/dfr_data_tools/doc/usage_import_wizard.rst  
**Description:** Technical documentation detailing the usage of the Bulk Data Import Wizard and interpretation of import job logs.  
**Template:** ReStructuredText  
**Dependancy Level:** 1  
**Name:** usage_import_wizard  
**Type:** Documentation  
**Relative Path:** doc/usage_import_wizard.rst  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Import Wizard Technical Guide
    
**Requirement Ids:**
    
    - REQ-TSE-001
    - REQ-DM-001
    - REQ-DM-002
    
**Purpose:** Provides technical guidance for administrators and developers on how to use the import wizard, expected file formats, field mapping considerations, and how to understand validation reports and error logs.  
**Logic Description:** Details steps for using the wizard, required CSV/XLSX structures, explanations of validation rules enforced, and how to access and interpret import job statuses and logs for troubleshooting.  
**Documentation:**
    
    - **Summary:** Technical guide for using the bulk data import functionality.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    
- **Path:** dfr_addons/dfr_data_tools/doc/data_transformation_hooks.rst  
**Description:** Technical documentation explaining how developers can extend the import service with custom data transformation logic.  
**Template:** ReStructuredText  
**Dependancy Level:** 1  
**Name:** data_transformation_hooks  
**Type:** Documentation  
**Relative Path:** doc/data_transformation_hooks.rst  
**Repository Id:** DFR_MOD_DATA_MGMT_TOOLKIT  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Developer Extensibility Guide
    
**Requirement Ids:**
    
    - REQ-DM-007
    
**Purpose:** Describes the mechanism or plugin points within the DataImportService where custom Python scripts or functions can be integrated to handle complex data transformations during the import process.  
**Logic Description:** Explains the interface or conventions for defining custom transformation functions/classes and how they are discovered or registered with the import service. Includes examples if applicable.  
**Documentation:**
    
    - **Summary:** Guide for developers on extending data transformation capabilities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedFieldMappingUI
  - EnableDirectDatabaseSourceConnectors_POC
  
- **Database Configs:**
  
  


---

