# Specification

# 1. Files

- **Path:** dfr_addons/dfr_notifications/__init__.py  
**Description:** Odoo module initializer. Imports sub-packages like models, services, views, etc.  
**Template:** Python Odoo Module __init__.py  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Initializer  
**Relative Path:** __init__  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the Python package for the dfr_notifications Odoo module, making its components discoverable by Odoo.  
**Logic Description:** Contains import statements for subdirectories/modules like 'models', 'services', 'views', 'controllers' (if any), 'wizards' (if any).  
**Documentation:**
    
    - **Summary:** Standard Odoo module __init__.py file. Imports various Python files and submodules.
    
**Namespace:** odoo.addons.dfr_notifications  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_addons/dfr_notifications/__manifest__.py  
**Description:** Odoo module manifest file. Declares module metadata, dependencies, data files, etc.  
**Template:** Python Odoo Module __manifest__.py  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Manifest  
**Relative Path:** __manifest__  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Declaration
    
**Requirement Ids:**
    
    
**Purpose:** Defines metadata for the dfr_notifications module, including its name, version, dependencies (e.g., DFR_MOD_CORE_COMMON, DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS, Odoo's mail module), and data files to be loaded.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'website', 'category', 'depends', 'data', 'installable', 'application'. Dependencies should list 'base', 'mail', 'dfr_common', and 'dfr_external_connectors'. Data files will list XML files from views, security, and data directories.  
**Documentation:**
    
    - **Summary:** Standard Odoo module manifest. Describes the module and its dependencies.
    
**Namespace:** odoo.addons.dfr_notifications  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_addons/dfr_notifications/models/__init__.py  
**Description:** Initializer for the models sub-package.  
**Template:** Python Package __init__.py  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Initializer  
**Relative Path:** models/__init__  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python files within the 'models' directory part of the dfr_notifications.models package.  
**Logic Description:** Contains import statements for each model file within this directory (e.g., from . import dfr_notification_template).  
**Documentation:**
    
    - **Summary:** Initializes the 'models' sub-package, importing all defined Odoo models.
    
**Namespace:** odoo.addons.dfr_notifications.models  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_addons/dfr_notifications/models/dfr_notification_template.py  
**Description:** Odoo model for defining and managing notification templates (SMS, email, push).  
**Template:** Python Odoo Model  
**Dependancy Level:** 2  
**Name:** dfr_notification_template  
**Type:** Model  
**Relative Path:** models/dfr_notification_template  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** channel_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** model_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** model_name  
**Type:** fields.Char  
**Attributes:** public|related  
    - **Name:** subject_template  
**Type:** fields.Text  
**Attributes:** public|translate  
    - **Name:** body_template_qweb  
**Type:** fields.Text  
**Attributes:** public|translate  
    - **Name:** lang  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** active  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** gateway_config_id  
**Type:** fields.Many2one  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** render_template  
**Parameters:**
    
    - self
    - record_ids
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Notification Template Management
    - Template Localization
    - Dynamic Placeholder Support
    
**Requirement Ids:**
    
    - REQ-NS-005
    - REQ-SYSADM-004
    
**Purpose:** Defines the data structure for notification templates, allowing administrators to create and manage templates for different channels with localization and dynamic content rendering.  
**Logic Description:** Model 'dfr.notification.template'. Fields: name, channel_type (selection: sms, email, push), model_id (m2o ir.model for context), subject_template (Text, for email/push), body_template_qweb (Text, for all channels, QWeb/Jinja syntax), lang (Char, for language-specific template, can be linked from recipient), active (Boolean). Subject and body templates should be translatable. `render_template` method takes a list of record IDs (related to `model_id`) and returns rendered subject/body for each. Gateway_config_id links to preferred gateway for this template.  
**Documentation:**
    
    - **Summary:** Model for storing and managing notification templates. Handles template rendering using QWeb/Jinja for dynamic content based on Odoo records. Supports translation of template content.
    
**Namespace:** odoo.addons.dfr_notifications.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_notifications/models/dfr_notification_gateway_config.py  
**Description:** Odoo model for configuring credentials and settings for third-party SMS/email/push gateway services.  
**Template:** Python Odoo Model  
**Dependancy Level:** 2  
**Name:** dfr_notification_gateway_config  
**Type:** Model  
**Relative Path:** models/dfr_notification_gateway_config  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** channel_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** provider_name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** api_key  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** api_secret  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** base_url  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** sender_id  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** email_from  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** is_odoo_default_email  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** active  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Gateway Configuration Management
    - Secure Credential Storage Hints
    
**Requirement Ids:**
    
    - REQ-SYSADM-004
    
**Purpose:** Defines the data structure for storing configurations of various notification gateways, enabling country-specific setup for SMS, email, and push services.  
**Logic Description:** Model 'dfr.notification.gateway.config'. Fields: name (e.g., 'Country X SMS Gateway'), channel_type (selection: sms, email, push), provider_name (e.g., 'Twilio', 'SendGrid', 'FCM', 'Odoo Default Email'), api_key (Char, ensure proper protection via field attributes or separate secure storage), api_secret (Char), base_url (Char), sender_id (Char, for SMS/Push), email_from (Char, for Email), is_odoo_default_email (Boolean), active (Boolean). This model will be used by the dispatch service to get credentials.  
**Documentation:**
    
    - **Summary:** Model for storing notification gateway configurations. Allows administrators to set up different providers for SMS, email, and push notifications, including necessary credentials.
    
**Namespace:** odoo.addons.dfr_notifications.models  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_notifications/models/dfr_notification_log.py  
**Description:** Odoo model for logging dispatched notifications, their status, and any errors.  
**Template:** Python Odoo Model  
**Dependancy Level:** 2  
**Name:** dfr_notification_log  
**Type:** Model  
**Relative Path:** models/dfr_notification_log  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** private|static  
    - **Name:** template_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** recipient_partner_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** recipient_email  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** recipient_phone  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** channel_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** gateway_config_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** subject  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** body  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** error_message  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** dispatch_timestamp  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** related_record_model  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** related_record_id  
**Type:** fields.Integer  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Notification Auditing
    - Dispatch Status Tracking
    
**Requirement Ids:**
    
    
**Purpose:** Provides a persistent log of all notification dispatch attempts, aiding in troubleshooting, auditing, and monitoring the notification system's reliability.  
**Logic Description:** Model 'dfr.notification.log'. Fields: template_id (m2o dfr.notification.template), recipient_partner_id (m2o res.partner, if applicable), recipient_email (Char), recipient_phone (Char), channel_type (Selection: sms, email, push), gateway_config_id (m2o dfr.notification.gateway.config), subject (Char), body (Text), status (Selection: pending, sent, failed, delivered - if feedback is possible), error_message (Text), dispatch_timestamp (Datetime), related_record_model (Char), related_record_id (Integer).  
**Documentation:**
    
    - **Summary:** Stores a record for each notification sent or attempted. Captures recipient, channel, content snippet, status, and any errors for auditing and debugging.
    
**Namespace:** odoo.addons.dfr_notifications.models  
**Metadata:**
    
    - **Category:** Auditing
    
- **Path:** dfr_addons/dfr_notifications/services/__init__.py  
**Description:** Initializer for the services sub-package.  
**Template:** Python Package __init__.py  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Initializer  
**Relative Path:** services/__init__  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python files within the 'services' directory part of the dfr_notifications.services package.  
**Logic Description:** Contains import statements for each service file within this directory (e.g., from . import notification_dispatch_service).  
**Documentation:**
    
    - **Summary:** Initializes the 'services' sub-package, importing all defined service classes or modules.
    
**Namespace:** odoo.addons.dfr_notifications.services  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_addons/dfr_notifications/services/notification_dispatch_service.py  
**Description:** Core Odoo service for preparing, rendering, and dispatching notifications through configured gateways.  
**Template:** Python Odoo Service  
**Dependancy Level:** 3  
**Name:** notification_dispatch_service  
**Type:** Service  
**Relative Path:** services/notification_dispatch_service  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Service Layer
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** send_notification_by_template_name  
**Parameters:**
    
    - self
    - template_technical_name
    - record_id
    - recipient_partner_ids=None
    - recipient_emails=None
    - recipient_phones=None
    - force_channel_type=None
    - custom_context=None
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** send_notification_by_template_id  
**Parameters:**
    
    - self
    - template_id
    - record_id
    - recipient_partner_ids=None
    - recipient_emails=None
    - recipient_phones=None
    - force_channel_type=None
    - custom_context=None
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** _render_template_content  
**Parameters:**
    
    - self
    - template_obj
    - record
    - custom_context=None
    
**Return Type:** tuple  
**Attributes:** private  
    - **Name:** _dispatch_via_channel  
**Parameters:**
    
    - self
    - template_obj
    - gateway_config
    - subject
    - body
    - recipient_info
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** _log_notification_attempt  
**Parameters:**
    
    - self
    - template_obj
    - recipient_info
    - gateway_config
    - status
    - error_message=None
    - subject=None
    - body=None
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Notification Dispatch Logic
    - Template Rendering
    - Channel Selection
    - Gateway Integration Call
    - Notification Logging
    
**Requirement Ids:**
    
    - REQ-NS-001
    - REQ-NS-003
    - REQ-NS-005
    - REQ-SYSADM-004
    
**Purpose:** Provides a centralized service to trigger and send notifications. It handles template rendering, channel selection, interaction with gateway connectors, and logging of dispatch attempts.  
**Logic Description:** Service class 'dfr.notification.dispatch.service'. Main method `send_notification_by_template_name` or `send_notification_by_template_id` takes template identifier, context record (for placeholders), and recipient details. It fetches the template, renders subject and body using `template.render_template(record)` or `env['ir.qweb']._render()`. Determines recipients (partner, email, phone). Fetches appropriate `dfr.notification.gateway.config` based on template's channel_type or override. Calls the relevant service from `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` (e.g., `self.env['dfr.sms.connector'].send_sms(...)`, `self.env['dfr.email.connector'].send_email(...)`, or `self.env['mail.mail'].create().send()` for Odoo default email). Logs the attempt in `dfr.notification.log`. Handles push notifications by calling a push connector if `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` provides one. Automated actions will call methods of this service or methods on business models that then call this service.  
**Documentation:**
    
    - **Summary:** This service is the core engine for dispatching notifications. It retrieves templates, renders them with dynamic data, selects the appropriate communication channel and gateway, and invokes external gateway services (via DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS) to send the message. It also logs all attempts.
    
**Namespace:** odoo.addons.dfr_notifications.services  
**Metadata:**
    
    - **Category:** ApplicationServices
    
- **Path:** dfr_addons/dfr_notifications/views/dfr_notification_template_views.xml  
**Description:** XML definitions for Odoo views (tree, form, search) for the Notification Template model.  
**Template:** Odoo View XML  
**Dependancy Level:** 3  
**Name:** dfr_notification_template_views  
**Type:** View  
**Relative Path:** views/dfr_notification_template_views  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Notification Template Admin UI
    
**Requirement Ids:**
    
    - REQ-NS-005
    - REQ-SYSADM-004
    
**Purpose:** Provides the user interface within Odoo's admin portal for National Administrators to create, view, edit, and manage notification templates.  
**Logic Description:** Defines `ir.ui.view` records for `dfr.notification.template` model. Includes a tree view displaying key fields (name, channel_type, active). A form view with fields for name, channel_type, model_id (for selecting context model), subject_template, body_template_qweb (using Odoo's HTML editor or plain text), lang, active, gateway_config_id. A search view for filtering templates. Defines the window action `ir.actions.act_window` for accessing these views.  
**Documentation:**
    
    - **Summary:** Defines the Odoo list, form, and search views for `dfr.notification.template` model, enabling administrators to manage notification templates through the UI.
    
**Namespace:** odoo.addons.dfr_notifications.views  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_notifications/views/dfr_notification_gateway_config_views.xml  
**Description:** XML definitions for Odoo views (tree, form, search) for Notification Gateway Configuration model.  
**Template:** Odoo View XML  
**Dependancy Level:** 3  
**Name:** dfr_notification_gateway_config_views  
**Type:** View  
**Relative Path:** views/dfr_notification_gateway_config_views  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Gateway Configuration Admin UI
    
**Requirement Ids:**
    
    - REQ-SYSADM-004
    
**Purpose:** Provides the user interface within Odoo's admin portal for National Administrators to configure and manage credentials and settings for various notification gateways.  
**Logic Description:** Defines `ir.ui.view` records for `dfr.notification.gateway.config` model. Includes a tree view (name, channel_type, provider_name, active). A form view with fields for name, channel_type, provider_name, api_key (password field), api_secret (password field), base_url, sender_id, email_from, is_odoo_default_email, active. A search view. Defines the window action `ir.actions.act_window`.  
**Documentation:**
    
    - **Summary:** Defines Odoo list, form, and search views for the `dfr.notification.gateway.config` model, allowing administrators to manage gateway settings.
    
**Namespace:** odoo.addons.dfr_notifications.views  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_notifications/views/dfr_notification_log_views.xml  
**Description:** XML definitions for Odoo views (tree, form, search) for the Notification Log model.  
**Template:** Odoo View XML  
**Dependancy Level:** 3  
**Name:** dfr_notification_log_views  
**Type:** View  
**Relative Path:** views/dfr_notification_log_views  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Notification Log Viewing UI
    
**Requirement Ids:**
    
    
**Purpose:** Provides a user interface for administrators to view and search through the logs of dispatched notifications.  
**Logic Description:** Defines `ir.ui.view` records for `dfr.notification.log` model. Tree view: dispatch_timestamp, recipient_info (computed), channel_type, subject (if any), status, error_message. Form view (read-only mostly): all fields from the model. Search view: filter by status, channel_type, date range, recipient.  
**Documentation:**
    
    - **Summary:** Defines Odoo views for displaying notification logs, allowing administrators to review dispatch history and troubleshoot issues.
    
**Namespace:** odoo.addons.dfr_notifications.views  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_notifications/views/dfr_notifications_menus.xml  
**Description:** XML definitions for menu items to access notification system functionalities in Odoo.  
**Template:** Odoo Menu XML  
**Dependancy Level:** 4  
**Name:** dfr_notifications_menus  
**Type:** Menu  
**Relative Path:** views/dfr_notifications_menus  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Navigation Menu
    
**Requirement Ids:**
    
    - REQ-NS-005
    - REQ-SYSADM-004
    
**Purpose:** Creates menu entries in the Odoo admin interface for accessing Notification Templates, Gateway Configurations, and Notification Logs.  
**Logic Description:** Defines `ir.ui.menu` records. A main menu for 'DFR Notifications', with sub-menus for 'Templates' (action to `dfr.notification.template`), 'Gateway Configurations' (action to `dfr.notification.gateway.config`), and 'Logs' (action to `dfr.notification.log`).  
**Documentation:**
    
    - **Summary:** Defines the menu structure in Odoo for accessing notification system features like template management and gateway configuration.
    
**Namespace:** odoo.addons.dfr_notifications.views  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_notifications/data/ir_actions_server_data.xml  
**Description:** XML definitions for predefined Odoo Server Actions to trigger notifications on specific events.  
**Template:** Odoo Data XML  
**Dependancy Level:** 4  
**Name:** ir_actions_server_data  
**Type:** Data  
**Relative Path:** data/ir_actions_server_data  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Example Notification Triggers
    
**Requirement Ids:**
    
    - REQ-NS-001
    - REQ-SYSADM-004
    
**Purpose:** Provides example server actions that can be configured by administrators to trigger notifications based on DFR system events, demonstrating how to use the notification service.  
**Logic Description:** Contains `ir.actions.server` records. For example, an action on `dfr.farmer` model, triggered on 'create', could call a method like `record.action_send_welcome_notification()`. This model method would then invoke the `dfr.notification.dispatch.service` with the appropriate template name and record. These serve as examples for admins to customize or create new ones using Odoo's UI.  
**Documentation:**
    
    - **Summary:** Provides initial server action configurations that link system events (e.g., new farmer registration) to notification dispatch via the notification service.
    
**Namespace:** odoo.addons.dfr_notifications.data  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_notifications/data/dfr_notification_template_data.xml  
**Description:** XML definitions for example/default notification templates.  
**Template:** Odoo Data XML  
**Dependancy Level:** 4  
**Name:** dfr_notification_template_data  
**Type:** Data  
**Relative Path:** data/dfr_notification_template_data  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Example Notification Templates
    
**Requirement Ids:**
    
    - REQ-NS-005
    
**Purpose:** Provides a set of pre-defined notification templates (e.g., welcome email, registration confirmation SMS) that administrators can use or customize.  
**Logic Description:** Contains `dfr.notification.template` records. For example, a template for 'Welcome Email to Farmer' with `channel_type='email'`, a subject like `Welcome to DFR, <t t-out='object.name'/>!`, and a body using QWeb. Another for 'SMS Registration Confirmation' with `channel_type='sms'` and a simple text body with placeholders.  
**Documentation:**
    
    - **Summary:** Provides sample notification templates that can be used out-of-the-box or as a starting point for customization by administrators.
    
**Namespace:** odoo.addons.dfr_notifications.data  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_notifications/security/ir.model.access.csv  
**Description:** CSV file defining access control rights for the module's Odoo models.  
**Template:** Odoo Security CSV  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** Security  
**Relative Path:** security/ir.model.access  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Role-Based Access Control (RBAC)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-NS-005
    - REQ-SYSADM-004
    
**Purpose:** Specifies which user groups have create, read, write, and delete (CRUD) permissions on the notification system's custom models.  
**Logic Description:** Format: id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink. Defines access for `dfr.notification.template`, `dfr.notification.gateway.config`, `dfr.notification.log`. Typically, system administrators (`base.group_system` or a custom DFR Admin group) would have full access. Other users might have read-only access to logs, for example.  
**Documentation:**
    
    - **Summary:** Defines the basic CRUD access rights for models introduced by this module (templates, gateway configs, logs) for different user groups.
    
**Namespace:** odoo.addons.dfr_notifications.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_notifications/security/dfr_notifications_groups.xml  
**Description:** XML file defining custom security groups for the notification system if needed.  
**Template:** Odoo Security XML  
**Dependancy Level:** 1  
**Name:** dfr_notifications_groups  
**Type:** Security  
**Relative Path:** security/dfr_notifications_groups  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    - Role-Based Access Control (RBAC)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Role Definitions (Optional)
    
**Requirement Ids:**
    
    - REQ-SYSADM-004
    
**Purpose:** Defines specific security groups (roles) if the standard Odoo groups are insufficient for managing notification system configurations (e.g., 'Notification Template Manager').  
**Logic Description:** Contains `res.groups` records. For instance, a group `group_dfr_notification_admin` that inherits from `base.group_user` and is implied by DFR National Admin group. This group would then be used in `ir.model.access.csv`.  
**Documentation:**
    
    - **Summary:** Defines any custom security groups specific to managing the notification system, allowing finer-grained access control beyond default Odoo groups.
    
**Namespace:** odoo.addons.dfr_notifications.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_notifications/i18n/dfr_notifications.pot  
**Description:** Main translation template (POT) file for the module.  
**Template:** Odoo i18n POT  
**Dependancy Level:** 0  
**Name:** dfr_notifications  
**Type:** Localization  
**Relative Path:** i18n/dfr_notifications  
**Repository Id:** DFR_MOD_NOTIFICATION_SYSTEM  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Template
    
**Requirement Ids:**
    
    - REQ-NS-005
    
**Purpose:** Contains all translatable strings extracted from Python code and XML views of this module, serving as a base for creating language-specific .po files.  
**Logic Description:** Standard POT file format. Generated by Odoo's i18n tools. Includes strings from model field labels, view labels, messages in Python code, etc. Also includes translatable content from `dfr_notification_template` if those fields are marked `translate=True`.  
**Documentation:**
    
    - **Summary:** The master template file for internationalization, containing all translatable strings from the module.
    
**Namespace:** odoo.addons.dfr_notifications.i18n  
**Metadata:**
    
    - **Category:** Localization
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnablePushNotificationsGlobally
  
- **Database Configs:**
  
  


---

