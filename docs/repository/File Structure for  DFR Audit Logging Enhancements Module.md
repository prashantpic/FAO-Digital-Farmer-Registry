# Specification

# 1. Files

- **Path:** dfr_addons/dfr_audit_log_enhancements/__manifest__.py  
**Description:** Odoo manifest file for the DFR Audit Logging Enhancements module. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    - REQ-SADG-005
    
**Purpose:** Declares the Odoo module, its name, version, author, dependencies (like dfr_common_core, dfr_rbac_config), and data files to be loaded (security, views).  
**Logic Description:** Contains a Python dictionary with keys like 'name', 'version', 'summary', 'description', 'author', 'website', 'category', 'depends', 'data', 'installable', 'application', 'auto_install'. Dependencies will include 'base', 'mail', 'dfr_common_core', 'dfr_rbac_config'. Data files will list security CSV, security XML, and view XML files.  
**Documentation:**
    
    - **Summary:** Module manifest for DFR Audit Logging Enhancements.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/__init__.py  
**Description:** Root __init__.py file for the DFR Audit Logging Enhancements module. Imports sub-modules like 'models' and 'services'.  
**Template:** Python Package Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'models' and 'services' sub-directories importable as Python packages within this Odoo module.  
**Logic Description:** Contains 'from . import models' and 'from . import services' statements.  
**Documentation:**
    
    - **Summary:** Initializes the dfr_audit_log_enhancements Python package.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements  
**Metadata:**
    
    - **Category:** ModuleInitialization
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/models/__init__.py  
**Description:** __init__.py file for the 'models' sub-directory. Imports all Odoo model definition files.  
**Template:** Python Package Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Loading
    
**Requirement Ids:**
    
    
**Purpose:** Imports model files like 'dfr_audit_log.py' and 'res_users_audit.py' to make them available to Odoo.  
**Logic Description:** Contains 'from . import dfr_audit_log' and potentially 'from . import res_users_audit' statements.  
**Documentation:**
    
    - **Summary:** Initializes the models package for DFR audit logging.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements.models  
**Metadata:**
    
    - **Category:** ModelDefinition
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/models/dfr_audit_log.py  
**Description:** Defines the 'dfr.audit.log' Odoo model used to store detailed audit log entries for DFR specific events and enhanced change tracking.  
**Template:** Odoo Model Template  
**Dependancy Level:** 2  
**Name:** dfr_audit_log  
**Type:** Model  
**Relative Path:** models/dfr_audit_log.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - MVC
    - Active Record
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** string='Log ID', readonly=True, required=True, copy=False, default='New'  
    - **Name:** timestamp  
**Type:** fields.Datetime  
**Attributes:** string='Timestamp', required=True, readonly=True, default=fields.Datetime.now, index=True  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', string='User', readonly=True, ondelete='restrict'  
    - **Name:** event_type  
**Type:** fields.Selection  
**Attributes:** selection=[('login_success', 'Login Success'), ('login_fail', 'Login Failed'), ('record_create', 'Record Created'), ('record_update', 'Record Updated'), ('record_delete', 'Record Deleted'), ('config_change', 'Configuration Changed'), ('sync_event', 'Sync Event'), ('data_export', 'Data Exported'), ('security_event', 'Security Event'), ('access_event', 'Access Event'), ('custom_action', 'Custom Action')], string='Event Type', required=True, readonly=True, index=True  
    - **Name:** model_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='ir.model', string='Model', readonly=True, ondelete='cascade'  
    - **Name:** res_id  
**Type:** fields.Reference  
**Attributes:** selection='_selection_target_model', string='Record ID', readonly=True  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Description', readonly=True, required=True  
    - **Name:** technical_details  
**Type:** fields.Text  
**Attributes:** string='Technical Details (JSON)', readonly=True, help='JSON formatted string containing old/new values, IP address, etc.'  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** selection=[('success', 'Success'), ('failure', 'Failure')], string='Status', readonly=True  
    - **Name:** session_info  
**Type:** fields.Char  
**Attributes:** string='Session Info', readonly=True, help='e.g., IP Address, User Agent'  
    
**Methods:**
    
    - **Name:** _selection_target_model  
**Parameters:**
    
    - self
    
**Return Type:** list  
**Attributes:** private  
    - **Name:** init  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** protected, for creating sequence  
    
**Implemented Features:**
    
    - Audit Log Storage
    - Structured Log Data
    
**Requirement Ids:**
    
    - REQ-SADG-005
    - REQ-SADG-006
    - REQ-FHR-010
    
**Purpose:** To provide a persistent, queryable store for comprehensive audit trails beyond Odoo's default chatter, capturing critical user and system actions.  
**Logic Description:** Defines fields for timestamp, user, event type, affected model/record, description, old/new values (in technical_details as JSON), and status. Implements a sequence for the 'name' field. Provides a method to get a dynamic selection of target models for res_id. Access control will be strictly managed via security files.  
**Documentation:**
    
    - **Summary:** Odoo model for storing DFR audit log entries.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/models/res_users_audit.py  
**Description:** Extends the 'res.users' model to integrate with the DFR audit logging system, specifically for logging login attempts.  
**Template:** Odoo Model Extension Template  
**Dependancy Level:** 4  
**Name:** res_users_audit  
**Type:** ModelExtension  
**Relative Path:** models/res_users_audit.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - MVC
    - Decorator
    
**Members:**
    
    
**Methods:**
    
    - **Name:** _check_credentials  
**Parameters:**
    
    - self
    - password
    - env
    
**Return Type:** void  
**Attributes:** public, inherited  
    - **Name:** _log_login_attempt  
**Parameters:**
    
    - self
    - login
    - result
    - user_agent_env=None
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - Login Attempt Auditing
    
**Requirement Ids:**
    
    - REQ-SADG-005
    
**Purpose:** To capture successful and failed login attempts and record them into the 'dfr.audit.log' model via the audit log service.  
**Logic Description:** Inherits from 'res.users'. Overrides methods related to login (e.g., `_check_credentials` or hooks into controller logic if more suitable) to call a private method `_log_login_attempt`. This private method then calls the `audit_log_service` to create a structured log entry for the login event, capturing username, IP, user agent, and success/failure status.  
**Documentation:**
    
    - **Summary:** Extends res.users for enhanced login auditing.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements.models.res_users_audit  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/services/__init__.py  
**Description:** __init__.py file for the 'services' sub-directory. Imports service definition files.  
**Template:** Python Package Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** services/__init__.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Loading
    
**Requirement Ids:**
    
    
**Purpose:** Imports service files like 'audit_log_service.py' to make them available within this Odoo module.  
**Logic Description:** Contains 'from . import audit_log_service' statement.  
**Documentation:**
    
    - **Summary:** Initializes the services package for DFR audit logging.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements.services  
**Metadata:**
    
    - **Category:** ServiceDefinition
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/services/audit_log_service.py  
**Description:** Implements the Audit Log Recording Service Interface (DFR_MOD_AUDIT_LOG_RECORDING_SVC). Provides methods for other DFR modules to record auditable events.  
**Template:** Odoo Service Template  
**Dependancy Level:** 3  
**Name:** audit_log_service  
**Type:** Service  
**Relative Path:** services/audit_log_service.py  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** log_event  
**Parameters:**
    
    - cls
    - env
    - event_type
    - description
    - model_name=None
    - res_id=None
    - user_id=None
    - technical_details=None
    - status='success'
    - session_info=None
    
**Return Type:** odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog  
**Attributes:** public, classmethod  
    - **Name:** log_record_change  
**Parameters:**
    
    - cls
    - env
    - model_name
    - res_id
    - change_type
    - description
    - old_values=None
    - new_values=None
    - user_id=None
    - session_info=None
    
**Return Type:** odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog  
**Attributes:** public, classmethod  
    - **Name:** log_login_event  
**Parameters:**
    
    - cls
    - env
    - login
    - success
    - ip_address=None
    - user_agent=None
    
**Return Type:** odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog  
**Attributes:** public, classmethod  
    
**Implemented Features:**
    
    - Centralized Audit Event Recording
    - Structured Logging API
    
**Requirement Ids:**
    
    - REQ-SADG-005
    - REQ-SADG-006
    - REQ-FHR-010
    
**Purpose:** To provide a consistent and centralized mechanism for all DFR modules to log significant actions and data changes into the 'dfr.audit.log' model.  
**Logic Description:** Contains class methods that take event details as parameters. These methods interact with the 'dfr.audit.log' Odoo model to create new log entries. Handles formatting of technical_details (e.g., old/new values into JSON). Ensures user context (user_id, IP from request if available) is captured. This service is the implementation of the 'DFR_MOD_AUDIT_LOG_RECORDING_SVC' endpoint/interface.  
**Documentation:**
    
    - **Summary:** Service layer for recording DFR audit events.
    
**Namespace:** odoo.addons.dfr_audit_log_enhancements.services.audit_log_service  
**Metadata:**
    
    - **Category:** ApplicationService
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/security/ir.model.access.csv  
**Description:** Defines model-level access rights (CRUD) for the 'dfr.audit.log' model and any other custom models introduced by this module.  
**Template:** Odoo Security CSV Template  
**Dependancy Level:** 3  
**Name:** ir.model.access  
**Type:** SecurityConfiguration  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Access Control
    
**Requirement Ids:**
    
    - REQ-SADG-005
    
**Purpose:** To control who can create, read, update, or delete audit log records. Typically, read access for specific admin roles, and create access for the system/users performing actions. No update/delete for general users.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Defines access for 'dfr.audit.log'. For example, a 'group_dfr_audit_viewer' (defined in dfr_rbac_config or here) gets perm_read=1, others 0. perm_create might be 1 for 'base.group_user' if service calls are made in user context, or controlled by service logic. perm_write and perm_unlink should be 0 for almost all groups to ensure log immutability.  
**Documentation:**
    
    - **Summary:** Access control list for DFR audit log models.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/security/dfr_audit_log_security.xml  
**Description:** Defines security groups and record rules, if needed, for more granular control over audit log access or functionality.  
**Template:** Odoo Security XML Template  
**Dependancy Level:** 3  
**Name:** dfr_audit_log_security  
**Type:** SecurityConfiguration  
**Relative Path:** security/dfr_audit_log_security.xml  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Viewer Role Definition (if not central)
    
**Requirement Ids:**
    
    - REQ-SADG-005
    
**Purpose:** To define any specific security groups for accessing audit log functionalities or to implement record rules that might filter audit log visibility based on user's country or other criteria (though less common for audit logs). This file will primarily ensure the menu item is visible only to appropriate roles.  
**Logic Description:** XML file using Odoo's security record syntax. May define a 'group_dfr_audit_log_viewer' if not already defined in a central RBAC module. This group would be assigned to the menu item for audit logs. It would reference groups from DFR_MOD_RBAC_CONFIG.  
**Documentation:**
    
    - **Summary:** Security groups and record rules for DFR audit logs.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/views/dfr_audit_log_views.xml  
**Description:** Defines Odoo views (list, form, search) for the 'dfr.audit.log' model, enabling authorized administrators to view and filter audit logs.  
**Template:** Odoo View XML Template  
**Dependancy Level:** 4  
**Name:** dfr_audit_log_views  
**Type:** ViewDefinition  
**Relative Path:** views/dfr_audit_log_views.xml  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log UI
    - Audit Log Filtering
    - Audit Log Export Trigger
    
**Requirement Ids:**
    
    - REQ-SADG-005
    - REQ-SYSADM-007
    
**Purpose:** To provide a user interface for administrators to inspect audit log entries, search for specific events, and export log data.  
**Logic Description:** XML file defining Odoo views. Includes a tree (list) view showing key fields (timestamp, user, event_type, model, res_id, description). A form view to show all details of a single log entry, including 'technical_details'. A search view with filters for 'timestamp' (date range), 'user_id', 'event_type', 'model_id'. Odoo's native export functionality will be available from the list view. This view definition is associated with the DFR_MOD_AUDIT_LOG_VIEW_ADMIN_ACTION endpoint.  
**Documentation:**
    
    - **Summary:** Odoo views for displaying and searching DFR audit logs.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/views/dfr_audit_log_menus.xml  
**Description:** Defines menu items within the Odoo interface to access the DFR audit log views.  
**Template:** Odoo Menu XML Template  
**Dependancy Level:** 4  
**Name:** dfr_audit_log_menus  
**Type:** MenuDefinition  
**Relative Path:** views/dfr_audit_log_menus.xml  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Menu Access
    
**Requirement Ids:**
    
    - REQ-SYSADM-007
    
**Purpose:** To make the audit log functionality easily discoverable and accessible for authorized administrative users within the Odoo backend.  
**Logic Description:** XML file defining Odoo menu items (`ir.ui.menu`). Creates a menu item, likely under a 'DFR Administration' or 'Audit' main menu, that triggers the action to open the 'dfr.audit.log' list view. Access to this menu item will be controlled by security groups defined in `dfr_audit_log_security.xml` or inherited from `DFR_MOD_RBAC_CONFIG`.  
**Documentation:**
    
    - **Summary:** Odoo menu items for accessing DFR audit logs.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_audit_log_enhancements/data/dfr_audit_log_data.xml  
**Description:** Contains data records for the module, such as sequence definitions for audit log IDs.  
**Template:** Odoo Data XML Template  
**Dependancy Level:** 3  
**Name:** dfr_audit_log_data  
**Type:** DataConfiguration  
**Relative Path:** data/dfr_audit_log_data.xml  
**Repository Id:** DFR_MOD_AUDIT_LOG  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log ID Sequencing
    
**Requirement Ids:**
    
    - REQ-SADG-005
    
**Purpose:** To initialize any required data for the audit log module, primarily the ir.sequence for generating unique, readable IDs for dfr.audit.log records.  
**Logic Description:** XML file defining an `ir.sequence` record. The sequence will have a specific prefix (e.g., 'ALOG') and padding for generating IDs for the 'dfr.audit.log' model's 'name' field.  
**Documentation:**
    
    - **Summary:** Data definitions for the DFR Audit Log module, including sequences.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableDetailedLoginAuditing
  - EnableOldNewValueDiffInTechnicalDetails
  
- **Database Configs:**
  
  


---

