# Specification

# 1. Files

- **Path:** dfr_addons/dfr_dynamic_forms/__init__.py  
**Description:** Initializes the Python package for the dfr_dynamic_forms Odoo module, importing submodules like models, services, wizards.  
**Template:** Odoo Python Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Odoo Module Initializer  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Discovery
    
**Requirement Ids:**
    
    - REQ-3-012
    
**Purpose:** Makes Python submodules and their contents available when Odoo loads the dfr_dynamic_forms module.  
**Logic Description:** Contains import statements for 'models', 'services', 'wizards', and other Python directories within the module.  
**Documentation:**
    
    - **Summary:** Standard Odoo module Python package initializer. Ensures all Python code is discoverable by Odoo.
    
**Namespace:** odoo.addons.dfr_dynamic_forms  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_dynamic_forms/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, data files, and other configurations.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - REQ-3-012
    
**Purpose:** Provides Odoo with essential information about the dfr_dynamic_forms module, such as its name, version, author, dependencies, and data files to load.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'description', 'category', 'author', 'website', 'license', 'depends' (listing 'dfr_common', 'dfr_farmer_registry', 'dfr_rbac_config', 'mail'), 'data' (listing XML files for views, security, data, wizards), 'assets' (listing static assets like JS/CSS/OWL).  
**Documentation:**
    
    - **Summary:** Defines the dfr_dynamic_forms module for Odoo, its dependencies, and resources. Specifies it as an Odoo 18.0 Community addon.
    
**Namespace:** odoo.addons.dfr_dynamic_forms  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/__init__.py  
**Description:** Initializes the 'models' Python package, importing all Odoo model files.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Odoo Models Initializer  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-004
    - REQ-3-008
    
**Purpose:** Makes all defined Odoo models within the 'models' directory accessible to the Odoo framework.  
**Logic Description:** Contains import statements for each model file, e.g., 'from . import dfr_form', 'from . import dfr_form_version', 'from . import dfr_form_field', 'from . import dfr_form_submission', 'from . import dfr_form_response'.  
**Documentation:**
    
    - **Summary:** Standard Python package initializer for Odoo models. Imports all domain model definitions.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form.py  
**Description:** Defines the 'dfr.form' Odoo model, representing a master dynamic form template. Manages high-level form properties and relationships to its versions.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** private|static|default:['mail.thread','mail.activity.mixin']  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** active  
**Type:** fields.Boolean  
**Attributes:** public|default:True  
    - **Name:** form_version_ids  
**Type:** fields.One2many  
**Attributes:** public|comodel_name:dfr.form.version|inverse_name:form_master_id  
    - **Name:** current_published_version_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.version|compute:_compute_current_published_version|store:True  
    - **Name:** country_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:res.country|help:Country for which this form is applicable, if specific.  
    
**Methods:**
    
    - **Name:** _compute_current_published_version  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|api.depends:form_version_ids.status  
    - **Name:** action_create_new_version  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** action_view_versions  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Form Master Definition
    - Link to Form Versions
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-004
    
**Purpose:** To store and manage the overarching template for a dynamic form, acting as a parent for multiple versions.  
**Logic Description:** This model holds the main identity of a form. It includes fields for name, description, and a one-to-many relationship to 'dfr.form.version'. A computed field identifies the currently published version. Methods allow creating new versions and viewing existing ones.  
**Documentation:**
    
    - **Summary:** Represents the master template for a dynamic data collection form. Allows managing different versions of the form.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form_version.py  
**Description:** Defines the 'dfr.form.version' Odoo model, representing a specific version of a dynamic form template, including its fields and status.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form_version  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form_version.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** private|static|default:['mail.thread']  
    - **Name:** form_master_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form|required:True|ondelete:cascade  
    - **Name:** version_number  
**Type:** fields.Char  
**Attributes:** public|required:True|readonly:True|default:lambda self: self.env['ir.sequence'].next_by_code('dfr.form.version.sequence') or 'New'  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public|related:form_master_id.name|store:True|string:Form Name  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public|selection:[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')]|default:'draft'  
    - **Name:** publish_date  
**Type:** fields.Datetime  
**Attributes:** public|readonly:True  
    - **Name:** archive_date  
**Type:** fields.Datetime  
**Attributes:** public|readonly:True  
    - **Name:** field_ids  
**Type:** fields.One2many  
**Attributes:** public|comodel_name:dfr.form.field|inverse_name:form_version_id  
    - **Name:** submission_count  
**Type:** fields.Integer  
**Attributes:** public|compute:_compute_submission_count|string:Submissions  
    - **Name:** can_be_published  
**Type:** fields.Boolean  
**Attributes:** public|compute:_compute_can_be_published  
    - **Name:** can_be_archived  
**Type:** fields.Boolean  
**Attributes:** public|compute:_compute_can_be_archived  
    - **Name:** is_editable  
**Type:** fields.Boolean  
**Attributes:** public|compute:_compute_is_editable|help:Indicates if the form version (fields) can still be edited.  
    
**Methods:**
    
    - **Name:** action_publish  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** action_archive  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** action_set_to_draft  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** _compute_submission_count  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _compute_can_be_published  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _compute_can_be_archived  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _compute_is_editable  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** copy  
**Parameters:**
    
    - self
    - default=None
    
**Return Type:** record  
**Attributes:** public|api.returns:self, lambda record: record.id|help:Creates a new draft version from this one.  
    
**Implemented Features:**
    
    - Form Version Management
    - Form Publishing Workflow
    - Field Association
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-004
    
**Purpose:** To store a snapshot of a dynamic form at a particular point in time, including its fields, status, and version identifier.  
**Logic Description:** This model represents a version of a dfr.form. It stores fields specific to this version (via O2M to dfr.form.field), status (draft, published, archived), and versioning info. Methods control publishing and archiving. Editing is restricted once published. A sequence generates version numbers.  
**Documentation:**
    
    - **Summary:** Defines a specific version of a dynamic form, managing its lifecycle (draft, published, archived) and its constituent fields.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form_version  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form_field.py  
**Description:** Defines the 'dfr.form.field' Odoo model, representing a single field within a dynamic form version.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form_field  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form_field.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _order  
**Type:** str  
**Attributes:** private|static|default:sequence, id  
    - **Name:** form_version_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.version|required:True|ondelete:cascade  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public|required:True|help:Technical name for the field, used for data storage and logic.  
    - **Name:** label  
**Type:** fields.Char  
**Attributes:** public|required:True|translate:True  
    - **Name:** field_type  
**Type:** fields.Selection  
**Attributes:** public|required:True|selection:[('text', 'Text'), ('number', 'Number'), ('date', 'Date'), ('datetime', 'Datetime'), ('selection', 'Selection (Dropdown)'), ('multi_selection', 'Multi-Selection (Tags)'), ('boolean', 'Boolean (Checkbox)'), ('gps_point', 'GPS Point'), ('image', 'Image/Binary'), ('computed_text', 'Computed Text (Read-only)')]|default:'text'  
    - **Name:** sequence  
**Type:** fields.Integer  
**Attributes:** public|default:10  
    - **Name:** is_required  
**Type:** fields.Boolean  
**Attributes:** public|default:False  
    - **Name:** help_text  
**Type:** fields.Text  
**Attributes:** public|translate:True  
    - **Name:** selection_options  
**Type:** fields.Text  
**Attributes:** public|help:For selection/multi_selection types. One option per line in format 'value:Label'.  
    - **Name:** validation_rule_required  
**Type:** fields.Boolean  
**Attributes:** public|string:Is Required (Validation)  
    - **Name:** validation_rule_min_length  
**Type:** fields.Integer  
**Attributes:** public|string:Min Length  
    - **Name:** validation_rule_max_length  
**Type:** fields.Integer  
**Attributes:** public|string:Max Length  
    - **Name:** validation_rule_min_value  
**Type:** fields.Float  
**Attributes:** public|string:Min Value (for Number)  
    - **Name:** validation_rule_max_value  
**Type:** fields.Float  
**Attributes:** public|string:Max Value (for Number)  
    - **Name:** validation_rule_regex  
**Type:** fields.Char  
**Attributes:** public|string:Regex Pattern  
    - **Name:** validation_error_message  
**Type:** fields.Char  
**Attributes:** public|translate:True|string:Custom Validation Error Message  
    - **Name:** conditional_logic_json  
**Type:** fields.Text  
**Attributes:** public|string:Conditional Logic (JSON)|help:JSON defining conditions to show/hide this field. Example: [{'field_name': 'other_field', 'operator': '=', 'value': 'some_value'}]  
    - **Name:** placeholder  
**Type:** fields.Char  
**Attributes:** public|translate:True  
    - **Name:** default_value_text  
**Type:** fields.Char  
**Attributes:** public|string:Default Text Value  
    - **Name:** default_value_number  
**Type:** fields.Float  
**Attributes:** public|string:Default Number Value  
    - **Name:** default_value_boolean  
**Type:** fields.Boolean  
**Attributes:** public|string:Default Boolean Value  
    
**Methods:**
    
    - **Name:** get_selection_options_parsed  
**Parameters:**
    
    - self
    
**Return Type:** list  
**Attributes:** public|help:Returns parsed selection options as a list of tuples.  
    - **Name:** _validate_conditional_logic_json  
**Parameters:**
    
    - self
    - vals
    
**Return Type:** void  
**Attributes:** private|api.constrains:conditional_logic_json  
    
**Implemented Features:**
    
    - Field Definition
    - Field Type Configuration
    - Validation Rule Storage
    - Conditional Logic Storage
    - Selection Options Management
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    
**Purpose:** To define the properties and behavior of a single field within a dynamic form version, including its type, label, validation rules, and display conditions.  
**Logic Description:** This model holds all metadata for a form field. It links to a 'dfr.form.version'. It stores various attributes for validation (min/max length, value, regex) and conditional display (JSON based). Selection options are stored as text to be parsed. A sequence field determines display order.  
**Documentation:**
    
    - **Summary:** Represents an individual field in a dynamic form. Stores type, label, validation constraints, conditional visibility logic, and options for selection fields.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form_field  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form_submission.py  
**Description:** Defines the 'dfr.form.submission' Odoo model, representing an instance of a completed dynamic form for a specific farmer.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form_submission  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form_submission.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** private|static|default:['mail.thread','mail.activity.mixin']  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public|compute:_compute_name|store:True|string:Submission Reference  
    - **Name:** farmer_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.farmer|required:True|ondelete:restrict|string:Farmer  
    - **Name:** form_version_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.version|required:True|ondelete:restrict|string:Form Version  
    - **Name:** submission_date  
**Type:** fields.Datetime  
**Attributes:** public|required:True|default:fields.Datetime.now|readonly:True  
    - **Name:** submitted_by_user_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:res.users|string:Submitted By|default:lambda self: self.env.user|readonly:True  
    - **Name:** response_ids  
**Type:** fields.One2many  
**Attributes:** public|comodel_name:dfr.form.response|inverse_name:submission_id|string:Responses  
    - **Name:** state  
**Type:** fields.Selection  
**Attributes:** public|selection:[('draft', 'Draft'), ('submitted', 'Submitted'), ('validated', 'Validated'), ('rejected', 'Rejected')]|default:'submitted'|tracking:True  
    - **Name:** notes  
**Type:** fields.Text  
**Attributes:** public|string:Internal Notes  
    
**Methods:**
    
    - **Name:** _compute_name  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|api.depends:farmer_id,form_version_id,submission_date  
    - **Name:** action_validate_submission  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_reject_submission  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Form Submission Storage
    - Link to Farmer and Form Version
    - Submission Lifecycle
    
**Requirement Ids:**
    
    - REQ-3-008
    
**Purpose:** To store metadata about a completed dynamic form submission, linking it to a farmer, the specific form version used, and its responses.  
**Logic Description:** This model records each instance of a form being filled out. It links to 'dfr.farmer' (from dfr_farmer_registry module) and 'dfr.form.version'. It also has a one-to-many relationship to 'dfr.form.response' to store the actual data. A computed name field provides a human-readable reference.  
**Documentation:**
    
    - **Summary:** Represents a single submission of a dynamic form, linking it to the farmer and the form version. Holds all responses provided by the user.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form_submission  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form_response.py  
**Description:** Defines the 'dfr.form.response' Odoo model, storing the actual answer for a specific field within a form submission.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form_response  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form_response.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** submission_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.submission|required:True|ondelete:cascade  
    - **Name:** field_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.field|required:True|ondelete:restrict  
    - **Name:** field_label  
**Type:** fields.Char  
**Attributes:** public|related:field_id.label|string:Field Label|readonly:True  
    - **Name:** field_type  
**Type:** fields.Selection  
**Attributes:** public|related:field_id.field_type|string:Field Type|readonly:True  
    - **Name:** value_text  
**Type:** fields.Text  
**Attributes:** public|string:Text Value  
    - **Name:** value_number  
**Type:** fields.Float  
**Attributes:** public|string:Number Value  
    - **Name:** value_date  
**Type:** fields.Date  
**Attributes:** public|string:Date Value  
    - **Name:** value_datetime  
**Type:** fields.Datetime  
**Attributes:** public|string:Datetime Value  
    - **Name:** value_boolean  
**Type:** fields.Boolean  
**Attributes:** public|string:Boolean Value  
    - **Name:** value_selection  
**Type:** fields.Char  
**Attributes:** public|string:Selection Value (Key)  
    - **Name:** value_multi_selection_ids  
**Type:** fields.Many2many  
**Attributes:** public|comodel_name:dfr.form.selection.option.answer|string:Multi-Selection Values  
    - **Name:** value_gps_latitude  
**Type:** fields.Float  
**Attributes:** public|string:GPS Latitude|digits:(10, 7)  
    - **Name:** value_gps_longitude  
**Type:** fields.Float  
**Attributes:** public|string:GPS Longitude|digits:(10, 7)  
    - **Name:** value_attachment_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:ir.attachment|string:Attachment Value  
    
**Methods:**
    
    - **Name:** get_display_value  
**Parameters:**
    
    - self
    
**Return Type:** str  
**Attributes:** public|help:Returns a human-readable representation of the response value.  
    
**Implemented Features:**
    
    - Storage of Individual Field Responses
    - Typed Value Storage
    
**Requirement Ids:**
    
    - REQ-3-008
    
**Purpose:** To store the specific answer provided by a user for a single field within a dynamic form submission.  
**Logic Description:** This model links to 'dfr.form.submission' and 'dfr.form.field'. It stores the response value. To handle different data types, it has multiple 'value_*' fields; only the one corresponding to the 'field_id.field_type' will be populated. A 'get_display_value' method can provide a user-friendly representation.  
**Documentation:**
    
    - **Summary:** Represents the answer to a single field within a dynamic form submission. Stores the value according to the field's type.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form_response  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/models/dfr_form_selection_option_answer.py  
**Description:** Helper model to store selected options for many2many selection fields in form responses. This is needed because a direct M2M to a static list of options is complex if options are just strings.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** dfr_form_selection_option_answer  
**Type:** Odoo Model  
**Relative Path:** models/dfr_form_selection_option_answer.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public|required:True|string:Option Value (Key)  
    - **Name:** display_name  
**Type:** fields.Char  
**Attributes:** public|string:Option Label  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Store Multi-Selection Answers
    
**Requirement Ids:**
    
    - REQ-3-008
    
**Purpose:** To act as a target for Many2many fields representing multi-select answers, allowing storage of the selected option keys and labels.  
**Logic Description:** This model isn't directly user-facing in views but serves as a technical table to store choices for 'multi_selection' field types. When a user selects multiple options, records in this table (or references to them) will be linked to the `dfr.form.response`.  
**Documentation:**
    
    - **Summary:** Helper model for storing selected options from multi-select dynamic form fields.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.models.dfr_form_selection_option_answer  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_dynamic_forms/security/ir.model.access.csv  
**Description:** CSV file defining model-level access rights (CRUD) for different user groups for the dynamic forms models.  
**Template:** Odoo CSV Data  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** Odoo Security Data  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - RoleBasedAccessControl
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To specify which user groups can perform create, read, write (update), and unlink (delete) operations on the dynamic form related models.  
**Logic Description:** Contains rows defining access rights. Columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Groups will be from 'dfr_rbac_config' (e.g., National Administrator, Supervisor, Enumerator).  
**Documentation:**
    
    - **Summary:** Configures Create, Read, Update, Delete (CRUD) permissions for dynamic form models based on user roles.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_dynamic_forms/security/dfr_dynamic_forms_security.xml  
**Description:** XML file for defining security groups specific to dynamic forms management, if any, or record rules.  
**Template:** Odoo XML Data  
**Dependancy Level:** 1  
**Name:** dfr_dynamic_forms_security  
**Type:** Odoo Security Data  
**Relative Path:** security/dfr_dynamic_forms_security.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - RoleBasedAccessControl
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Record Rule Definition
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To define fine-grained access control, such as record rules limiting visibility of forms or submissions based on country or other criteria, if not handled by core RBAC module.  
**Logic Description:** May contain <record model="ir.rule"> elements to define record-level security. For example, a rule to ensure National Admins only see forms relevant to their country if 'country_id' is used on 'dfr.form'.  
**Documentation:**
    
    - **Summary:** Defines specific security groups or record rules for the dynamic forms module, augmenting ir.model.access.csv.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_dynamic_forms/data/dfr_form_field_types_data.xml  
**Description:** XML data file to pre-populate or configure available field types if they are managed as data or require specific default settings.  
**Template:** Odoo XML Data  
**Dependancy Level:** 1  
**Name:** dfr_form_field_types_data  
**Type:** Odoo Data  
**Relative Path:** data/dfr_form_field_types_data.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Field Type Configuration
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To initialize the system with a base set of dynamic form field types if their properties are complex or configurable via data records.  
**Logic Description:** If field types are simple selections on 'dfr.form.field', this file might not be strictly needed unless certain types have default behaviors or icons defined via data. For now, assuming field_type is a selection field on `dfr.form.field` and this file provides sequence for `ir.sequence` for `dfr.form.version`.  
**Documentation:**
    
    - **Summary:** Provides initial data for sequences, or could be used for more complex field type definitions if required.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** dfr_addons/dfr_dynamic_forms/data/ir_sequence_data.xml  
**Description:** XML data file to define sequences for models like dfr.form.version.  
**Template:** Odoo XML Data  
**Dependancy Level:** 1  
**Name:** ir_sequence_data  
**Type:** Odoo Data  
**Relative Path:** data/ir_sequence_data.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Sequence Definitions
    
**Requirement Ids:**
    
    - REQ-3-004
    
**Purpose:** To define number sequences used for generating unique identifiers, e.g., for form version numbers.  
**Logic Description:** Contains <record model="ir.sequence"> elements to define sequences, e.g., for 'dfr.form.version.sequence'.  
**Documentation:**
    
    - **Summary:** Defines Odoo sequences for generating unique identifiers for dynamic form versions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** dfr_addons/dfr_dynamic_forms/services/__init__.py  
**Description:** Initializes the 'services' Python package.  
**Template:** Odoo Python Init  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Odoo Services Initializer  
**Relative Path:** services/__init__.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    
**Requirement Ids:**
    
    
**Purpose:** Makes service classes available within the module.  
**Logic Description:** Contains import statements for each service file, e.g., 'from . import form_definition_service'.  
**Documentation:**
    
    - **Summary:** Initializes the Python package for application services related to dynamic forms.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.services  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_dynamic_forms/services/form_definition_service.py  
**Description:** Python service class for managing dynamic form definitions and versions.  
**Template:** Python Service  
**Dependancy Level:** 2  
**Name:** form_definition_service  
**Type:** Application Service  
**Relative Path:** services/form_definition_service.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_form_master  
**Parameters:**
    
    - self
    - env
    - form_data
    
**Return Type:** recordset (dfr.form)  
**Attributes:** public|static  
    - **Name:** create_new_form_version  
**Parameters:**
    
    - self
    - env
    - form_master_id
    - version_data=None
    
**Return Type:** recordset (dfr.form.version)  
**Attributes:** public|static  
    - **Name:** publish_form_version  
**Parameters:**
    
    - self
    - env
    - form_version_id
    
**Return Type:** bool  
**Attributes:** public|static  
    - **Name:** archive_form_version  
**Parameters:**
    
    - self
    - env
    - form_version_id
    
**Return Type:** bool  
**Attributes:** public|static  
    - **Name:** get_form_definition_for_rendering  
**Parameters:**
    
    - self
    - env
    - form_version_id
    
**Return Type:** dict  
**Attributes:** public|static|help:Returns a structured representation of the form suitable for rendering clients.  
    - **Name:** add_field_to_version  
**Parameters:**
    
    - self
    - env
    - form_version_id
    - field_data
    
**Return Type:** recordset (dfr.form.field)  
**Attributes:** public|static  
    - **Name:** update_field_in_version  
**Parameters:**
    
    - self
    - env
    - field_id
    - field_data
    
**Return Type:** bool  
**Attributes:** public|static  
    - **Name:** remove_field_from_version  
**Parameters:**
    
    - self
    - env
    - field_id
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Form Creation Logic
    - Form Versioning Logic
    - Form Publishing Logic
    - Form Definition Retrieval
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-004
    
**Purpose:** To provide business logic operations for creating, versioning, publishing, and retrieving dynamic form definitions.  
**Logic Description:** This service contains methods to manage the lifecycle of form definitions and their versions. It interacts with 'dfr.form' and 'dfr.form.version' models. The 'get_form_definition_for_rendering' method is crucial for providing a clean structure (e.g., JSON) for UIs (Odoo backend, mobile app, portal) to render the form.  
**Documentation:**
    
    - **Summary:** Handles application logic related to the definition, versioning, and lifecycle management of dynamic forms.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.services.form_definition_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_dynamic_forms/services/form_submission_service.py  
**Description:** Python service class for processing and storing dynamic form submissions.  
**Template:** Python Service  
**Dependancy Level:** 2  
**Name:** form_submission_service  
**Type:** Application Service  
**Relative Path:** services/form_submission_service.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** process_submission  
**Parameters:**
    
    - self
    - env
    - farmer_uid_or_id
    - form_version_id
    - responses_data
    - submitted_by_user_id=None
    
**Return Type:** recordset (dfr.form.submission)  
**Attributes:** public|static|help:Processes raw submission data, validates it, and creates submission and response records.  
    - **Name:** get_farmer_submissions  
**Parameters:**
    
    - self
    - env
    - farmer_id
    - form_master_id=None
    
**Return Type:** recordset (dfr.form.submission)  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Form Submission Processing
    - Link Submission to Farmer
    - Store Responses
    
**Requirement Ids:**
    
    - REQ-3-008
    
**Purpose:** To handle the logic of receiving form submission data, linking it to the correct farmer and form version, and persisting the responses.  
**Logic Description:** This service takes submitted data (e.g., from an API endpoint or portal controller), validates it against the form definition (field types, required fields, using form_validation_service), finds the farmer record, and creates 'dfr.form.submission' and 'dfr.form.response' records.  
**Documentation:**
    
    - **Summary:** Manages the processing, validation, and storage of data submitted through dynamic forms.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.services.form_submission_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_dynamic_forms/services/form_validation_service.py  
**Description:** Python service class for handling complex validation logic for dynamic form fields.  
**Template:** Python Service  
**Dependancy Level:** 2  
**Name:** form_validation_service  
**Type:** Application Service  
**Relative Path:** services/form_validation_service.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - ServiceLayer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_field_response  
**Parameters:**
    
    - self
    - env
    - form_field_record
    - response_value
    
**Return Type:** tuple (bool, str|None)|help:Returns (isValid, error_message_or_None)  
**Attributes:** public|static  
    - **Name:** validate_submission_responses  
**Parameters:**
    
    - self
    - env
    - form_version_record
    - responses_dict
    
**Return Type:** tuple (bool, dict)|help:Returns (isValid, errors_dict_by_field_name)  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Field-level Validation
    - Submission-level Validation
    
**Requirement Ids:**
    
    - REQ-3-002
    
**Purpose:** To centralize and execute validation logic for dynamic form field responses, based on configured rules.  
**Logic Description:** This service contains methods to validate individual field responses against rules stored in 'dfr.form.field' (required, min/max length, regex, etc.). It can be used by 'form_submission_service' before saving responses or by the UI for real-time feedback.  
**Documentation:**
    
    - **Summary:** Provides services for validating data submitted through dynamic forms against their defined rules.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.services.form_validation_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_dynamic_forms/wizards/__init__.py  
**Description:** Initializes the 'wizards' Python package.  
**Template:** Odoo Python Init  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Odoo Wizards Initializer  
**Relative Path:** wizards/__init__.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Discovery
    
**Requirement Ids:**
    
    - REQ-3-004
    
**Purpose:** Makes wizard (TransientModel) classes available within the module.  
**Logic Description:** Contains import statements for each wizard model file, e.g., 'from . import form_version_wizard'.  
**Documentation:**
    
    - **Summary:** Initializes the Python package for Odoo wizards related to dynamic forms.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.wizards  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_dynamic_forms/wizards/form_version_wizard.py  
**Description:** Defines the Odoo wizard (TransientModel) for creating a new version of a dynamic form.  
**Template:** Odoo Python Wizard  
**Dependancy Level:** 2  
**Name:** form_version_wizard  
**Type:** Odoo Wizard Model  
**Relative Path:** wizards/form_version_wizard.py  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static|default:'dfr.form.version.wizard'  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static|default:'Create New Form Version Wizard'  
    - **Name:** form_master_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form|required:True  
    - **Name:** source_version_id  
**Type:** fields.Many2one  
**Attributes:** public|comodel_name:dfr.form.version|help:Optional source version to copy fields from.  
    - **Name:** new_version_description  
**Type:** fields.Text  
**Attributes:** public|string:New Version Description  
    
**Methods:**
    
    - **Name:** action_create_version  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public|help:Calls the form_definition_service to create a new version and returns an action to open it.  
    
**Implemented Features:**
    
    - Guided Form Version Creation
    
**Requirement Ids:**
    
    - REQ-3-004
    
**Purpose:** To provide a user-friendly, multi-step process for creating a new version of an existing dynamic form, potentially copying from a previous version.  
**Logic Description:** This TransientModel will capture necessary information (e.g., source version to copy from if any) and then call the 'form_definition_service' to perform the actual version creation. It guides the admin through the process.  
**Documentation:**
    
    - **Summary:** Wizard to facilitate the creation of new versions of dynamic forms, optionally copying an existing version as a template.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.wizards.form_version_wizard  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/views/dfr_form_views.xml  
**Description:** XML file defining Odoo views (tree, form, search) and actions for 'dfr.form' and 'dfr.form.version' models. This includes the main UI for the form builder.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** dfr_form_views  
**Type:** Odoo View Definition  
**Relative Path:** views/dfr_form_views.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Form Builder UI
    - Form Version Management UI
    - Form Field Configuration UI
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    - REQ-3-004
    
**Purpose:** To define the user interface for administrators to create, design, manage, and version dynamic forms and their fields.  
**Logic Description:** Contains <record model="ir.ui.view"> elements for form, tree, and search views of 'dfr.form' and 'dfr.form.version'. The 'dfr.form.version' form view will be the main form builder interface, allowing inline editing of 'dfr.form.field' records. It will use standard Odoo fields and potentially custom widgets (defined in static/src) for advanced features like conditional logic setup.  
**Documentation:**
    
    - **Summary:** Provides the administrative user interface for managing dynamic form templates, their versions, and fields. This is the core of the form builder.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/views/dfr_form_submission_views.xml  
**Description:** XML file defining Odoo views (tree, form, search) and actions for 'dfr.form.submission' and 'dfr.form.response' models.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** dfr_form_submission_views  
**Type:** Odoo View Definition  
**Relative Path:** views/dfr_form_submission_views.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Form Submission Viewing UI
    - Response Viewing UI
    
**Requirement Ids:**
    
    - REQ-3-008
    
**Purpose:** To define the user interface for administrators to view and manage data submitted through dynamic forms.  
**Logic Description:** Contains <record model="ir.ui.view"> elements for 'dfr.form.submission'. The form view will display submission metadata and the list of responses ('dfr.form.response') in a readable format, possibly as a one2many list or a custom widget rendering the filled form.  
**Documentation:**
    
    - **Summary:** Provides the administrative user interface for viewing and managing submitted dynamic form data.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/views/dfr_dynamic_forms_menus.xml  
**Description:** XML file defining menu items for accessing dynamic form management features in the Odoo backend.  
**Template:** Odoo XML Menu  
**Dependancy Level:** 2  
**Name:** dfr_dynamic_forms_menus  
**Type:** Odoo Menu Definition  
**Relative Path:** views/dfr_dynamic_forms_menus.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Menu Configuration
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To provide navigation entries in the Odoo application menu for accessing the dynamic forms builder and submission views.  
**Logic Description:** Contains <menuitem> records to create main menus (e.g., 'Dynamic Forms') and sub-menus linking to actions defined for 'dfr.form' and 'dfr.form.submission'.  
**Documentation:**
    
    - **Summary:** Defines the menu structure within Odoo for accessing dynamic form functionalities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/views/form_version_wizard_views.xml  
**Description:** XML file defining the Odoo view for the 'form.version.wizard'.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** form_version_wizard_views  
**Type:** Odoo View Definition  
**Relative Path:** views/form_version_wizard_views.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Form Version Creation Wizard UI
    
**Requirement Ids:**
    
    - REQ-3-004
    
**Purpose:** To define the user interface for the wizard that guides administrators in creating new versions of dynamic forms.  
**Logic Description:** Contains a <record model="ir.ui.view"> for the 'dfr.form.version.wizard' form view, with fields to select the master form, source version (optional), and add a description.  
**Documentation:**
    
    - **Summary:** Defines the UI for the wizard that helps administrators create new form versions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/static/src/js/form_builder_widget.js  
**Description:** JavaScript file for a custom Odoo form builder widget, enhancing the UI for designing dynamic forms with features like drag-and-drop, advanced property configuration for fields, and conditional logic setup.  
**Template:** Odoo JavaScript Widget  
**Dependancy Level:** 3  
**Name:** form_builder_widget  
**Type:** Odoo Frontend Component (JS)  
**Relative Path:** static/src/js/form_builder_widget.js  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    
**Methods:**
    
    - **Name:** _renderFields  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _onAddField  
**Parameters:**
    
    - event
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _onEditField  
**Parameters:**
    
    - fieldId
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _onDeleteField  
**Parameters:**
    
    - fieldId
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _configureConditionalLogic  
**Parameters:**
    
    - fieldId
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** _configureValidationRules  
**Parameters:**
    
    - fieldId
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - Enhanced Form Design UI
    - Conditional Logic Configuration UI
    - Validation Rule Configuration UI
    
**Requirement Ids:**
    
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    
**Purpose:** To provide a rich, 'no-code/low-code' user experience for designing dynamic forms, going beyond standard Odoo field widgets if necessary.  
**Logic Description:** This widget will be included in the 'dfr.form.version' form view. It will interact with the Odoo backend (RPC calls to services or model methods) to manage field definitions. It will handle rendering the list of fields, allowing reordering, adding new fields from a palette, and configuring properties like label, type, validation rules, and conditional logic through modal dialogs or inline editors.  
**Documentation:**
    
    - **Summary:** Custom JavaScript widget for the Odoo backend providing an interactive form builder interface for dynamic forms.
    
**Namespace:** odoo.addons.dfr_dynamic_forms.form_builder_widget  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/static/src/xml/form_builder_templates.xml  
**Description:** OWL templates for the custom form builder JavaScript widget.  
**Template:** Odoo OWL Template  
**Dependancy Level:** 3  
**Name:** form_builder_templates  
**Type:** Odoo Frontend Component (OWL)  
**Relative Path:** static/src/xml/form_builder_templates.xml  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    - ModelViewController
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Form Builder UI Rendering
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To define the HTML structure and presentation logic for the custom form builder widget using Odoo's OWL framework.  
**Logic Description:** Contains QWeb/OWL templates defining the layout of the form builder area, field representations, property editor dialogs, conditional logic builder interface, etc. These templates are used by 'form_builder_widget.js'.  
**Documentation:**
    
    - **Summary:** OWL (Odoo Web Library) templates defining the visual structure of the dynamic form builder.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_dynamic_forms/static/src/scss/form_builder.scss  
**Description:** SCSS/CSS file for styling the custom form builder widget and related UI elements.  
**Template:** SCSS/CSS  
**Dependancy Level:** 3  
**Name:** form_builder  
**Type:** Odoo Frontend Asset (CSS)  
**Relative Path:** static/src/scss/form_builder.scss  
**Repository Id:** DFR_MOD_DYNAMIC_FORMS  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Form Builder Styling
    
**Requirement Ids:**
    
    - REQ-3-001
    
**Purpose:** To provide custom styles for the dynamic form builder interface, ensuring a user-friendly and visually appealing design.  
**Logic Description:** Contains SCSS rules to style the form builder elements, field palette, property editors, and overall layout. This will be compiled into CSS and loaded by Odoo.  
**Documentation:**
    
    - **Summary:** Custom styles for the dynamic form builder UI components.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_advanced_form_builder_widget
  - enable_form_version_auto_archive
  
- **Database Configs:**
  
  


---

