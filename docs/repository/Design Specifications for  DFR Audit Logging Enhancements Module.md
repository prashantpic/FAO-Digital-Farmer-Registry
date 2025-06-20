# Software Design Specification: DFR Audit Logging Enhancements Module (DFR_MOD_AUDIT_LOG)

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR Audit Logging Enhancements Module (`DFR_MOD_AUDIT_LOG`). This module is responsible for enhancing Odoo's native auditing capabilities to meet DFR-specific requirements. It will capture comprehensive audit logs for user actions and critical system events, store them persistently, and provide an interface for authorized administrators to view and filter these logs. This ensures traceability, compliance, and supports data governance.

### 1.2 Scope
The scope of this module includes:
*   Defining a dedicated Odoo model for storing detailed audit log entries (`dfr.audit.log`).
*   Providing a service layer (`audit_log_service`) for other DFR modules to record auditable events.
*   Extending existing Odoo models (e.g., `res.users`) to automatically log specific events like login attempts.
*   Developing Odoo views (list, form, search) and menu items for administrators to access and review audit logs.
*   Defining security configurations to control access to audit log data and functionalities.
*   Ensuring that logged information includes details such as timestamp, user, event type, affected record, description, and technical details (e.g., old/new values for data changes).

This module focuses on enhancing audit capabilities *within* the DFR Odoo platform. It relies on other DFR modules (like `DFR_MOD_CORE_COMMON` for shared utilities and `DFR_MOD_RBAC_CONFIG` for role definitions) for foundational elements.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **DFR**: Digital Farmer Registry
*   **SDS**: Software Design Specification
*   **ORM**: Object-Relational Mapper
*   **CRUD**: Create, Read, Update, Delete
*   **UI**: User Interface
*   **PII**: Personally Identifiable Information
*   **JSON**: JavaScript Object Notation
*   **CSV**: Comma-Separated Values
*   **RBAC**: Role-Based Access Control
*   **SADG**: Security, Auditing & Data Governance
*   **FHR**: Farmer & Household Registration Management
*   **SYSADM**: System Administration & Configuration

## 2. System Overview
The `DFR_MOD_AUDIT_LOG` module is an Odoo addon designed to integrate seamlessly with the DFR platform. It acts as a centralized sink for audit information generated by various user actions and system events across different DFR modules.

**Module Architecture:**
*   **Models Layer**: Contains the `dfr.audit.log` model for data persistence and extensions to core Odoo models like `res.users`.
*   **Services Layer**: Provides the `AuditLogService` with methods to programmatically create audit log entries. This service implements the `DFR_MOD_AUDIT_LOG_RECORDING_SVC` interface.
*   **Views Layer**: Defines the UI (list, form, search views, and menus) for administrators to interact with audit logs, implementing the `DFR_MOD_AUDIT_LOG_VIEW_ADMIN_ACTION`.
*   **Security Layer**: Manages access rights to the audit log data and UI components.
*   **Data Layer**: Includes sequences for unique log identifiers.

**Dependencies:**
*   `base`: Standard Odoo module.
*   `mail`: For `mail.thread` capabilities if leveraged, and general Odoo infrastructure.
*   `dfr_common_core` (DFR_MOD_CORE_COMMON): For any shared base models, utilities, or configurations.
*   `dfr_rbac_config` (DFR_MOD_RBAC_CONFIG): For referencing centrally defined DFR roles/groups for security configurations.

**External Interfaces:**
*   **DFR_MOD_AUDIT_LOG_VIEW_ADMIN_ACTION**: Implemented through Odoo views and menus, providing a UI for administrators.
*   **DFR_MOD_AUDIT_LOG_RECORDING_SVC**: Implemented by `audit_log_service.py`, offering Python methods for other modules to call.

## 3. Detailed Design

### 3.1 Module Structure and File Descriptions

#### 3.1.1 `__manifest__.py`
*   **Purpose**: Declares the Odoo module, its metadata, dependencies, and data files.
    *   Fulfills: Module Definition
*   **Logic/Contents**:
    python
    {
        'name': 'DFR Audit Logging Enhancements',
        'version': '18.0.1.0.0',
        'summary': 'Enhances DFR auditing with detailed logging and viewing capabilities.',
        'description': """
            This module provides comprehensive audit logging for the Digital Farmer Registry (DFR) platform.
            It includes:
            - A dedicated model to store audit logs (dfr.audit.log).
            - Services for other modules to record auditable events.
            - UI for administrators to view and filter audit logs.
            - Enhanced logging for specific events like login attempts.
        """,
        'author': 'SSS-AI (FAO Project)',
        'website': 'https://www.fao.org', # Placeholder
        'category': 'DFR/Administration',
        'depends': [
            'base',
            'mail',
            'dfr_common_core', # DFR_MOD_CORE_COMMON
            'dfr_rbac_config', # DFR_MOD_RBAC_CONFIG
        ],
        'data': [
            'security/ir.model.access.csv',
            'security/dfr_audit_log_security.xml',
            'data/dfr_audit_log_data.xml', # Sequence definition
            'views/dfr_audit_log_views.xml',
            'views/dfr_audit_log_menus.xml',
        ],
        'installable': True,
        'application': False, # It's a supporting module, not a standalone application
        'auto_install': False,
        'license': 'MIT', # Or Apache 2.0 as per REQ-CM-001
    }
    
*   **Requirements Traceability**: `REQ-SADG-005` (implicitly by defining the module).

#### 3.1.2 `__init__.py`
*   **Purpose**: Initializes the Python package for the Odoo module.
    *   Fulfills: Module Initialization
*   **Logic/Contents**:
    python
    # -*- coding: utf-8 -*-
    from . import models
    from . import services
    

#### 3.1.3 `models/__init__.py`
*   **Purpose**: Initializes the `models` sub-package, importing all model files.
    *   Fulfills: Model Loading
*   **Logic/Contents**:
    python
    # -*- coding: utf-8 -*-
    from . import dfr_audit_log
    from . import res_users_audit
    # Import other models that might be extended for auditing in the future
    

#### 3.1.4 `models/dfr_audit_log.py`
*   **Purpose**: Defines the `dfr.audit.log` Odoo model for storing audit log entries.
    *   Fulfills: Audit Log Storage, Structured Log Data
*   **Class Definition**: `DfrAuditLog(models.Model)`
*   **Attributes**:
    *   `_name = 'dfr.audit.log'`
    *   `_description = 'DFR Audit Log'`
    *   `_order = 'timestamp desc, id desc'`
    *   `_log_access = False` (To prevent this model's CRUD operations from creating audit logs of audit logs, unless specifically desired)
*   **Fields**:
    *   `name`: `fields.Char(string='Log ID', readonly=True, required=True, copy=False, default=lambda self: _('New'), index=True)`
        *   Sequence generated ID.
    *   `timestamp`: `fields.Datetime(string='Timestamp', required=True, readonly=True, default=fields.Datetime.now, index=True)`
        *   Timestamp of the event.
    *   `user_id`: `fields.Many2one('res.users', string='User', readonly=True, ondelete='restrict', index=True)`
        *   User who performed the action or system user if automated.
    *   `event_type`: `fields.Selection(selection=[('login_success', 'Login Success'), ('login_fail', 'Login Failed'), ('record_create', 'Record Created'), ('record_update', 'Record Updated'), ('record_delete', 'Record Deleted'), ('config_change', 'Configuration Changed'), ('sync_event', 'Sync Event'), ('data_export', 'Data Exported'), ('security_event', 'Security Event (e.g., permission change)'), ('access_event', 'Access Event (e.g., sensitive data viewed)'), ('custom_action', 'Custom Action (Module Specific)')], string='Event Type', required=True, readonly=True, index=True)`
        *   Categorizes the audit event.
    *   `model_id`: `fields.Many2one('ir.model', string='Target Model', readonly=True, ondelete='cascade', index=True)`
        *   The Odoo model related to the event, if applicable.
    *   `res_id`: `fields.Reference(selection='_selection_target_model', string='Target Record ID', readonly=True, help="ID of the record in the Target Model")`
        *   The specific record ID in `model_id` related to the event.
    *   `description`: `fields.Text(string='Description', readonly=True, required=True)`
        *   Human-readable summary of the event.
    *   `technical_details`: `fields.Text(string='Technical Details (JSON)', readonly=True, help="JSON formatted string potentially containing old/new values for record changes, IP address, parameters, etc.")`
        *   Stores structured data like field changes (old/new values), request parameters.
        *   Crucial for `REQ-SADG-006` and `REQ-FHR-010`.
    *   `status`: `fields.Selection(selection=[('success', 'Success'), ('failure', 'Failure')], string='Status', readonly=True, default='success')`
        *   Indicates if the audited action was successful or failed.
    *   `session_info`: `fields.Char(string='Session Info', readonly=True, help='e.g., IP Address, User Agent')`
        *   Information about the user's session.
*   **Methods**:
    *   `_selection_target_model(self)`:
        *   **Logic**: Dynamically fetches all Odoo models (`ir.model`) to populate the selection for the `res_id` field.
        *   **Returns**: `list` of `(model_name, model_description)` tuples.
    *   `init(self)`:
        *   **Logic**: Creates the `ir.sequence` for the `name` field if it doesn't exist. This is automatically called by Odoo.
        *   Referenced by `dfr_audit_log_data.xml`.
*   **Requirements Traceability**: `REQ-SADG-005`, `REQ-SADG-006`, `REQ-FHR-010`.

#### 3.1.5 `models/res_users_audit.py`
*   **Purpose**: Extends `res.users` to log login attempts.
    *   Fulfills: Login Attempt Auditing
*   **Class Definition**: `ResUsersAudit(models.Model)`
*   **Attributes**:
    *   `_inherit = 'res.users'`
*   **Methods**:
    *   `_check_credentials(self, password, env)`:
        *   **Logic**: Overrides the standard Odoo method. Calls `super()._check_credentials(password, env)` to perform the actual password check.
            After the super call (or by wrapping it in try/except to catch `AccessDenied`), calls `self._log_login_attempt(self.login, result, user_agent_env=env)` where `result` is True for success, False for failure.
            The `user_agent_env` parameter is the environment passed to `_check_credentials`. The `request` object can be accessed from `self.env.context.get('request')` or from `env` if it carries the request.
        *   **Parameters**: `self`, `password (str)`, `env (odoo.api.Environment)`
        *   **Returns**: `void` (or raises `AccessDenied` as per Odoo standard).
    *   `_log_login_attempt(self, login, success, user_agent_env=None)`:
        *   **Logic**:
            1.  Determine IP address and user agent. If `user_agent_env` is provided and has a `request` object, use `user_agent_env['request'].httprequest.remote_addr` and `user_agent_env['request'].httprequest.user_agent.string`. Fallback if not available.
            2.  Construct `session_info` string.
            3.  Call `self.env['dfr.audit_log.service'].log_login_event(login, success, ip_address=ip_address, user_agent=user_agent)`.
            4.  Handles cases where `self` might be a recordset of users by iterating or ensuring it's a single user context if login is specific.
        *   **Parameters**: `self`, `login (str)`, `success (bool)`, `user_agent_env (odoo.api.Environment, optional)`
        *   **Returns**: `void`
*   **Requirements Traceability**: `REQ-SADG-005`.

#### 3.1.6 `services/__init__.py`
*   **Purpose**: Initializes the `services` sub-package.
    *   Fulfills: Service Loading
*   **Logic/Contents**:
    python
    # -*- coding: utf-8 -*-
    from . import audit_log_service
    

#### 3.1.7 `services/audit_log_service.py`
*   **Purpose**: Implements the `DFR_MOD_AUDIT_LOG_RECORDING_SVC` interface, providing methods to create audit log entries.
    *   Fulfills: Centralized Audit Event Recording, Structured Logging API
*   **Class Definition**: `AuditLogService(models.AbstractModel)`
    *   **Note**: Using `models.AbstractModel` makes it easy to register the service as `self.env['dfr.audit_log.service']` if needed, or it can be a plain Python class whose methods are called directly. For simplicity and consistency with Odoo, `models.AbstractModel` is a good choice for service-like components.
*   **Attributes**:
    *   `_name = 'dfr.audit_log.service'` (If registered as an Odoo service/component)
    *   `_description = 'DFR Audit Log Service'`
*   **Methods**:
    *   `_get_request_session_info(env)`:
        *   **Logic**: Helper method to extract IP address and User Agent from the current request in `env`.
        *   **Parameters**: `env (odoo.api.Environment)`
        *   **Returns**: `str` (formatted session info or None)
    *   `log_event(cls, env, event_type, description, model_name=None, res_id=None, user_id=None, technical_details=None, status='success', session_info=None)`:
        *   **Logic**:
            1.  Validate required parameters (`event_type`, `description`).
            2.  Determine `user_id`: if `None`, use `env.user.id`.
            3.  Determine `model_id`: if `model_name` is provided, find `ir.model` record.
            4.  Determine `session_info`: if `None`, call `_get_request_session_info(env)`.
            5.  Prepare `technical_details`: if dictionary, convert to JSON string.
            6.  Create `dfr.audit.log` record using `env['dfr.audit.log'].sudo().create({...})`. Using `sudo()` might be necessary if called from contexts with insufficient direct create permissions on `dfr.audit.log`, but the service should ideally operate with the calling user's permissions if possible, unless system-level logging is intended. This needs careful consideration based on security policy. For broader DFR module usage, it's safer to assume the calling context provides the user, and the service creates the log as that user (if that user has create rights on audit log) or as a system user if permissions are an issue. Let's assume `sudo()` for now to ensure logs are always created, but this is a security consideration.
            7.  Return the created log record.
        *   **Parameters**: `cls`, `env`, `event_type (str)`, `description (str)`, `model_name (str, optional)`, `res_id (int or str, optional)`, `user_id (int, optional)`, `technical_details (dict or str, optional)`, `status (str, default 'success')`, `session_info (str, optional)`
        *   **Returns**: `odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog` record.
    *   `log_record_change(cls, env, model_name, res_id, change_type, description, old_values=None, new_values=None, user_id=None, session_info=None)`:
        *   **Logic**:
            1.  A specialized version of `log_event`.
            2.  Sets `event_type` based on `change_type` (e.g., 'record_create', 'record_update', 'record_delete').
            3.  Formats `old_values` and `new_values` dictionaries into a structured JSON for `technical_details`. Example: `{"changed_fields": {"field1": {"old": "val1", "new": "val2"}}, "raw_old": {...}, "raw_new": {...}}`.
            4.  Calls `log_event` with appropriate parameters.
        *   **Parameters**: `cls`, `env`, `model_name (str)`, `res_id (int or str)`, `change_type (str, e.g., 'create', 'update', 'delete')`, `description (str)`, `old_values (dict, optional)`, `new_values (dict, optional)`, `user_id (int, optional)`, `session_info (str, optional)`
        *   **Returns**: `odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog` record.
    *   `log_login_event(cls, env, login, success, ip_address=None, user_agent=None)`:
        *   **Logic**:
            1.  Specialized method for login events.
            2.  Determines `event_type` ('login_success' or 'login_fail').
            3.  Constructs `description` (e.g., "Login attempt for user 'login_name' failed/succeeded.").
            4.  Tries to find user by `login` to link `user_id` if successful, otherwise `user_id` might be `None` or a system user for failed attempts if the user doesn't exist.
            5.  Constructs `session_info` from `ip_address` and `user_agent`.
            6.  Sets `technical_details` with `login_username: login`.
            7.  Calls `log_event`.
        *   **Parameters**: `cls`, `env`, `login (str)`, `success (bool)`, `ip_address (str, optional)`, `user_agent (str, optional)`
        *   **Returns**: `odoo.addons.dfr_audit_log_enhancements.models.dfr_audit_log.DfrAuditLog` record.
*   **Requirements Traceability**: `REQ-SADG-005`, `REQ-SADG-006`, `REQ-FHR-010`.

#### 3.1.8 `security/ir.model.access.csv`
*   **Purpose**: Defines model-level CRUD access rights for `dfr.audit.log`.
    *   Fulfills: Audit Log Access Control
*   **Logic/Contents**:
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    access_dfr_audit_log_group_system,dfr.audit.log.system,model_dfr_audit_log,base.group_system,1,0,1,0
    access_dfr_audit_log_group_user,dfr.audit.log.user,model_dfr_audit_log,base.group_user,0,0,1,0
    access_dfr_audit_log_group_dfr_nat_admin,dfr.audit.log.nat_admin,model_dfr_audit_log,dfr_rbac_config.group_dfr_national_administrator,1,0,0,0
    access_dfr_audit_log_group_dfr_super_admin,dfr.audit.log.super_admin,model_dfr_audit_log,dfr_rbac_config.group_dfr_super_administrator,1,0,0,0
    # Add other DFR roles that might need to view logs if necessary, e.g., support team.
    # By default, system users (including automated actions) and regular users can create logs.
    # Write and Unlink are generally 0 for all to ensure log immutability from user actions.
    # Specific DFR admin roles get read access.
    
*   **Notes**:
    *   `model_dfr_audit_log` refers to the `ir.model` record for `dfr.audit.log`.
    *   `dfr_rbac_config.group_dfr_national_administrator` and `dfr_rbac_config.group_dfr_super_administrator` are assumed to be defined in the `DFR_MOD_RBAC_CONFIG` module.
    *   `perm_create` for `base.group_user` allows users performing actions to have those actions logged under their own UID by the service, assuming the service doesn't always use `sudo()`. If `sudo()` is always used by the service, then only `base.group_system` might need `perm_create`.
*   **Requirements Traceability**: `REQ-SADG-005`.

#### 3.1.9 `security/dfr_audit_log_security.xml`
*   **Purpose**: Defines security groups (if any specific to this module) and record rules for menu/action access.
    *   Fulfills: Audit Log Viewer Role Definition (primarily for menu access)
*   **Logic/Contents**:
    xml
    <odoo>
        <data noupdate="1">
            <!--
            If specific groups for audit log viewing are needed beyond standard DFR roles,
            they would be defined here. However, it's preferable to reuse roles from
            dfr_rbac_config. This file will primarily ensure the menu action for viewing
            audit logs is restricted to appropriate DFR roles.
            Example:
            <record id="group_dfr_audit_log_viewer_explicit" model="res.groups">
                <field name="name">DFR Audit Log Viewer (Explicit)</field>
                <field name="category_id" ref="base.module_category_hidden"/>
                <field name="implied_ids" eval="[(4, ref('dfr_rbac_config.group_dfr_national_administrator'))]"/>
            </record>
            The menu item in dfr_audit_log_menus.xml will then reference this group or directly
            the DFR admin groups from dfr_rbac_config.
            -->
        </data>
    </odoo>
    
*   **Note**: For simplicity and centralization of roles, it's better if the menu access is directly tied to roles defined in `DFR_MOD_RBAC_CONFIG` (e.g., National Administrator, Super Administrator). This file might be minimal or not define new groups if existing roles suffice.
*   **Requirements Traceability**: `REQ-SADG-005`.

#### 3.1.10 `views/dfr_audit_log_views.xml`
*   **Purpose**: Defines Odoo views (list/tree, form, search) for the `dfr.audit.log` model.
    *   Fulfills: Audit Log UI, Audit Log Filtering, Audit Log Export Trigger
*   **Logic/Contents**:
    xml
    <odoo>
        <data>
            <!-- Tree View (List View) -->
            <record id="view_dfr_audit_log_tree" model="ir.ui.view">
                <field name="name">dfr.audit.log.tree</field>
                <field name="model">dfr.audit.log</field>
                <field name="arch" type="xml">
                    <tree string="DFR Audit Logs" decoration-danger="status=='failure'">
                        <field name="timestamp"/>
                        <field name="user_id"/>
                        <field name="event_type"/>
                        <field name="model_id" optional="hide"/>
                        <field name="res_id" optional="hide"/>
                        <field name="description"/>
                        <field name="session_info" optional="hide"/>
                        <field name="status" optional="show"/>
                    </tree>
                </field>
            </record>

            <!-- Form View -->
            <record id="view_dfr_audit_log_form" model="ir.ui.view">
                <field name="name">dfr.audit.log.form</field>
                <field name="model">dfr.audit.log</field>
                <field name="arch" type="xml">
                    <form string="DFR Audit Log Entry">
                        <sheet>
                            <group>
                                <group>
                                    <field name="name"/>
                                    <field name="timestamp"/>
                                    <field name="user_id"/>
                                    <field name="event_type"/>
                                </group>
                                <group>
                                    <field name="model_id"/>
                                    <field name="res_id"/>
                                    <field name="status"/>
                                    <field name="session_info"/>
                                </group>
                            </group>
                            <notebook>
                                <page string="Details">
                                    <group>
                                        <field name="description" widget="text"/>
                                        <field name="technical_details" widget="text" placeholder="JSON formatted technical details..."/>
                                    </group>
                                </page>
                            </notebook>
                        </sheet>
                    </form>
                </field>
            </record>

            <!-- Search View -->
            <record id="view_dfr_audit_log_search" model="ir.ui.view">
                <field name="name">dfr.audit.log.search</field>
                <field name="model">dfr.audit.log</field>
                <field name="arch" type="xml">
                    <search string="Search DFR Audit Logs">
                        <field name="user_id"/>
                        <field name="event_type"/>
                        <field name="model_id"/>
                        <field name="res_id"/>
                        <field name="description"/>
                        <field name="session_info" string="IP/Session"/>
                        <filter string="Today" name="filter_today" domain="[('timestamp', '&gt;=', context_today().strftime('%Y-%m-%d 00:00:00')), ('timestamp', '&lt;=', context_today().strftime('%Y-%m-%d 23:59:59'))]"/>
                        <filter string="This Week" name="filter_this_week" domain="[('timestamp', '&gt;=', (context_today() - relativedelta(weeks=1, weekday=0)).strftime('%Y-%m-%d 00:00:00')), ('timestamp', '&lt;=', (context_today() + relativedelta(weekday=6)).strftime('%Y-%m-%d 23:59:59'))]"/>
                        <filter string="Successful Events" name="filter_successful" domain="[('status', '=', 'success')]"/>
                        <filter string="Failed Events" name="filter_failed" domain="[('status', '=', 'failure')]"/>
                        <separator/>
                        <group expand="0" string="Group By">
                            <filter string="User" name="group_by_user" context="{'group_by': 'user_id'}"/>
                            <filter string="Event Type" name="group_by_event_type" context="{'group_by': 'event_type'}"/>
                            <filter string="Target Model" name="group_by_model" context="{'group_by': 'model_id'}"/>
                            <filter string="Date (Day)" name="group_by_date" context="{'group_by': 'timestamp:day'}"/>
                        </group>
                    </search>
                </field>
            </record>

            <!-- Action Window -->
            <record id="action_dfr_audit_log_view" model="ir.actions.act_window">
                <field name="name">DFR Audit Logs</field>
                <field name="res_model">dfr.audit.log</field>
                <field name="view_mode">tree,form</field>
                <field name="search_view_id" ref="view_dfr_audit_log_search"/>
                <field name="context">{'search_default_filter_today': 1}</field>
                <field name="help" type="html">
                    <p class="o_view_nocontent_smiling_face">
                        No audit log entries found.
                    </p><p>
                        This log records important user actions and system events.
                    </p>
                </field>
            </record>
        </data>
    </odoo>
    
*   **Note**: The action (`action_dfr_audit_log_view`) implements `DFR_MOD_AUDIT_LOG_VIEW_ADMIN_ACTION`. Odoo's standard export functionality will be available from the tree view.
*   **Requirements Traceability**: `REQ-SADG-005`, `REQ-SYSADM-007`.

#### 3.1.11 `views/dfr_audit_log_menus.xml`
*   **Purpose**: Defines menu items to access the audit log views.
    *   Fulfills: Audit Log Menu Access
*   **Logic/Contents**:
    xml
    <odoo>
        <data>
            <!-- Main DFR Menu (assuming this is defined in dfr_common_core or dfr_rbac_config) -->
            <!-- Example: <menuitem id="menu_dfr_root" name="DFR Platform" sequence="10"/> -->

            <!-- DFR Administration Submenu (assuming this is defined, or can be created here if specific) -->
            <!-- Example: <menuitem id="menu_dfr_administration_root" name="Administration" parent="menu_dfr_root" sequence="100"/> -->

            <menuitem
                id="menu_dfr_audit_log"
                name="DFR Audit Logs"
                action="action_dfr_audit_log_view"
                parent="dfr_rbac_config.menu_dfr_administration_settings" <!-- Or a more suitable parent menu from dfr_rbac_config -->
                sequence="50"
                groups="dfr_rbac_config.group_dfr_national_administrator,dfr_rbac_config.group_dfr_super_administrator"
            />
            <!--
            Alternative parent if menu_dfr_administration_settings is not suitable:
            Could be parent="base.menu_administration" (Odoo's general Settings)
            Or create a new top-level 'Audit' menu if desired.
            The parent `dfr_rbac_config.menu_dfr_administration_settings` is an example
            and should match a menu defined in the DFR_MOD_RBAC_CONFIG module.
            -->
        </data>
    </odoo>
    
*   **Requirements Traceability**: `REQ-SYSADM-007`.

#### 3.1.12 `data/dfr_audit_log_data.xml`
*   **Purpose**: Contains data for initializing the module, like sequences.
    *   Fulfills: Audit Log ID Sequencing
*   **Logic/Contents**:
    xml
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent overwriting on module update -->
            <record id="seq_dfr_audit_log" model="ir.sequence">
                <field name="name">DFR Audit Log Sequence</field>
                <field name="code">dfr.audit.log</field>
                <field name="prefix">ALOG/</field>
                <field name="padding">6</field>
                <field name="company_id" eval="False"/> <!-- Global sequence -->
            </record>
        </data>
    </odoo>
    
*   **Note**: The `dfr.audit.log` model's `name` field default should use this sequence: `default=lambda self: self.env['ir.sequence'].next_by_code('dfr.audit.log') or _('New')`.
*   **Requirements Traceability**: `REQ-SADG-005`.

### 3.2 Data Model
The primary data model introduced by this module is `dfr.audit.log`. Its fields are detailed in section `3.1.4`.
This model is designed to store a comprehensive history of actions.

Key design considerations for the data model:
*   **Immutability**: Audit logs, once created, should not be alterable by regular users or even most administrators. `perm_write` and `perm_unlink` are set to 0 for most groups.
*   **Traceability**: Fields like `user_id`, `timestamp`, `model_id`, `res_id`, and `session_info` ensure actions can be traced back to their origin.
*   **Detail**: `description` provides a human-readable summary, while `technical_details` (JSON) stores structured data like old/new values for field changes, which is essential for `REQ-SADG-006` (Change history) and `REQ-FHR-010` (audit trail for profile edits).
*   **Performance**: Indexed fields (`timestamp`, `user_id`, `event_type`, `model_id`) are crucial for efficient querying and filtering of potentially large audit log tables.

### 3.3 Interfaces

#### 3.3.1 Audit Log Viewer Admin Action (`DFR_MOD_AUDIT_LOG_VIEW_ADMIN_ACTION`)
*   **Description**: UI for authorized administrators to view and filter audit logs.
*   **Implementation**:
    *   Realized through `ir.actions.act_window` record `action_dfr_audit_log_view` defined in `views/dfr_audit_log_views.xml`.
    *   This action uses the tree, form, and search views also defined in `views/dfr_audit_log_views.xml` for the `dfr.audit.log` model.
    *   Access is granted via the menu item `menu_dfr_audit_log` defined in `views/dfr_audit_log_menus.xml`, which is restricted by security groups (e.g., `dfr_rbac_config.group_dfr_national_administrator`).
*   **Requirements Traceability**: `REQ-SYSADM-007`.

#### 3.3.2 Audit Log Recording Service Interface (`DFR_MOD_AUDIT_LOG_RECORDING_SVC`)
*   **Description**: Internal Python service for other DFR modules to record auditable events.
*   **Implementation**:
    *   Implemented by the `AuditLogService` class in `services/audit_log_service.py`.
    *   Other DFR modules will call its class methods (e.g., `AuditLogService.log_event(...)` or `self.env['dfr.audit.log.service'].log_event(...)` if registered).
    *   This service handles the creation of `dfr.audit.log` records.
*   **Key Methods (as detailed in 3.1.7)**:
    *   `log_event(...)`: Generic event logging.
    *   `log_record_change(...)`: Specific for logging CRUD operations with old/new values.
    *   `log_login_event(...)`: Specific for logging login attempts.
*   **Requirements Traceability**: `REQ-SADG-005`, `REQ-SADG-006`.

### 3.4 Security Considerations
*   **Access Control**:
    *   Read access to `dfr.audit.log` records is restricted to designated administrative roles (e.g., National Administrator, Super Administrator) as defined in `ir.model.access.csv` and `dfr_audit_log_security.xml` (for menu access).
    *   Create access for `dfr.audit.log` is granted to `base.group_user` or `base.group_system` to allow the `AuditLogService` to create logs in the context of the user performing the action, or as a system action. This assumes the service methods properly manage user context or use `sudo()` appropriately.
    *   Write and Unlink permissions on `dfr.audit.log` records are highly restricted (ideally only for a super-admin/system maintenance role under strict conditions, if ever) to ensure log immutability.
*   **Data Integrity**: The `technical_details` field is designed to store JSON, which helps in structuring detailed information like field changes.
*   **PII**: Audit logs may contain PII (e.g., user IDs, IP addresses, potentially data values in `technical_details`). Access restrictions are paramount. The design does not currently include explicit PII masking within the audit log viewer itself, relying on role-based access to the raw logs.

### 3.5 Error Handling
*   The `AuditLogService` methods should include basic error handling (e.g., `try-except` blocks) to prevent failures in the audit logging process from crashing the primary operation being audited.
*   Logging failures themselves (e.g., database error while writing to `dfr.audit.log`) should be logged to Odoo's standard server logs for diagnosis by system administrators.
*   The `status` field in `dfr.audit.log` can indicate if the *audited action* itself failed, not necessarily if the audit logging action failed.

### 3.6 Configuration
*   **Feature Toggles** (managed via `ir.config_parameter` or custom settings model in `dfr_common_core`):
    *   `dfr_audit.enable_detailed_login_auditing`: Boolean, default `True`. Controls whether `res_users_audit.py` logs login attempts.
    *   `dfr_audit.enable_old_new_value_diff`: Boolean, default `True`. Controls whether the `log_record_change` service attempts to compute and store detailed old/new value diffs in `technical_details`. If `False`, only a generic change message might be stored.
*   **Sequence for Log ID**: Configured in `data/dfr_audit_log_data.xml`.

## 4. Requirements Traceability Matrix
| Requirement ID | Designed Component(s)                                                                 |
|----------------|---------------------------------------------------------------------------------------|
| REQ-SADG-005   | `dfr.audit.log` model, `audit_log_service`, `res_users_audit`, Views, Security Files      |
| REQ-SADG-006   | `dfr.audit.log` model (technical_details field), `audit_log_service.log_record_change`  |
| REQ-FHR-010    | `dfr.audit.log` model, `audit_log_service` (called by Farmer module for relevant events) |
| REQ-SYSADM-007 | `dfr_audit_log_views.xml`, `dfr_audit_log_menus.xml` (Audit Log Viewer Admin Action)      |

*(Note: REQ-FHR-010 is primarily fulfilled by the calling module, e.g., Farmer & Household Registration Management, which would use the `audit_log_service` to log its specific events. This audit module provides the *capability* to store those detailed logs.)*

## 5. Future Considerations / Potential Enhancements
*   **Log Archival/Rotation**: For very high volume systems, strategies for archiving or rotating older audit logs might be needed. This is currently out of scope but can be built upon this module.
*   **Advanced Reporting/Analytics on Audit Data**: Custom reports or dashboards providing insights from audit data.
*   **Tamper-Evident Logging**: Integration with technologies that provide stronger guarantees of log immutability (e.g., blockchain, write-once storage), if required by extreme security needs.
*   **Granular Configuration of Audited Events**: An admin UI to turn on/off auditing for specific models or event types dynamically, beyond simple feature toggles.

This SDS provides a comprehensive design for the `DFR_MOD_AUDIT_LOG` module, ensuring all specified requirements and architectural considerations are addressed for successful code generation.