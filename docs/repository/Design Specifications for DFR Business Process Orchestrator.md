# DFR Business Process Orchestrator - Software Design Specification

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR Business Process Orchestrator module (`dfr_process_orchestrator`). This module is a core component of the FAO-Digital Farmer Registry (DFR) system, acting as a workflow engine within the Odoo 18.0 Community backend. Its primary responsibility is to define, manage, and execute complex, multi-step business processes that span various DFR functional modules. This SDS will guide the development of the Odoo addon, ensuring it meets the specified requirements and integrates seamlessly with other DFR modules.

### 1.2 Scope
The scope of this SDS covers the design and implementation of the `dfr_process_orchestrator` Odoo module. This includes:
- Defining and implementing workflows for farmer lifecycle management (REQ-FHR-011).
- Implementing triggers for the notification system based on system events (REQ-NS-001).
- Orchestrating the processing of farmer self-registrations from the Farmer Self-Service Portal (REQ-FSSP-005).
- Providing general business process automation capabilities and configuration options (REQ-PCA-020).
- Custom models for workflow configuration and logging.
- Wizards for manual workflow intervention.
- Associated views, menus, and security configurations.

This module leverages Odoo's native workflow capabilities (Automated Actions, Server Actions) and Odoo ORM.

### 1.3 Definitions, Acronyms, and Abbreviations
- **DFR**: Digital Farmer Registry
- **SDS**: Software Design Specification
- **ORM**: Object-Relational Mapper
- **UI**: User Interface
- **XML**: Extensible Markup Language
- **CSV**: Comma-Separated Values
- **REQ**: Requirement ID
- **ToT**: Train-the-Trainer

### 1.4 References
- DFR System Requirements Specification (SRS) Document (Implicitly, via requirement IDs)
- DFR Architecture Design Document
- Odoo 18.0 Developer Documentation

### 1.5 Overview
This SDS is organized into sections detailing the module's architecture, data design, component design, and interfaces. It provides specifications for each file within the `dfr_process_orchestrator` module structure.

## 2. System Architecture
The `dfr_process_orchestrator` module operates within the DFR Odoo Application Services Layer. It follows Odoo's Modular Monolith architecture style. It uses Odoo's built-in Workflow Engine (Automated Actions, Server Actions) and ORM to interact with data and trigger actions across different DFR modules.

**Key Architectural Principles:**
- **Decoupling:** Orchestrates processes by coordinating actions in other modules, rather than implementing the core business logic of those modules itself.
- **Configurability:** Aims to make workflow rules and parameters configurable by administrators where feasible.
- **Extensibility:** Built as a standard Odoo module, allowing for future enhancements.

## 3. Data Design
This module introduces custom models for managing orchestration configurations and logging workflow events.

### 3.1 `orchestration.rule.config` Model
- **Purpose:** To store configurable parameters and rules for various orchestration processes, allowing administrators to fine-tune workflow behavior without code changes.
- **Fields:**
    - `name` (Char, required): Descriptive name for the configuration rule.
    - `workflow_key` (Char, required, indexed): A unique key identifying the workflow this rule applies to (e.g., 'farmer_status_change', 'portal_submission_validation').
    - `parameter_key` (Char, required, indexed): A unique key for the specific parameter within the workflow (e.g., 'active_status_notification_template_id', 'supervisor_group_id_for_portal_review').
    - `parameter_value` (Text): The value of the parameter. Can store simple strings, numbers, or JSON for more complex rule definitions (e.g., `{"min_age": 18, "required_documents": ["national_id", "address_proof"]}`).
    - `description` (Text): Explanation of the rule and its purpose.
    - `is_active` (Boolean, default=True): Whether the configuration rule is currently active.
- **Methods:**
    - `get_config_value(cls, workflow_key, parameter_key, default_value=None)`:
        - **Purpose:** Retrieves the value of a specific configuration parameter.
        - **Logic:** Searches for an active `orchestration.rule.config` record matching `workflow_key` and `parameter_key`. If found, returns `parameter_value`. If `parameter_value` is intended to be JSON, it should be deserialized before returning. If not found, returns `default_value`.
        - **Error Handling:** Log a warning if a config is expected but not found and no default is provided.
- **Indexes:** `workflow_key`, `parameter_key` (individually and potentially combined if lookups are frequent on both).

### 3.2 `workflow.log` Model
- **Purpose:** To provide a structured way to log important steps, decisions, outcomes, and errors of orchestrated processes for monitoring, auditing, and troubleshooting.
- **Fields:**
    - `name` (Char, compute='_compute_name', store=True): A computed name for the log entry, e.g., "Workflow [workflow_name] - [Timestamp]".
    - `workflow_name` (Char, required, indexed): Name or key of the workflow being logged (e.g., 'Farmer Approval', 'Notification Dispatch').
    - `related_record_model` (Char): Model of the primary record this log entry relates to (e.g., 'dfr.farmer', 'dfr.form.submission').
    - `related_record_id` (Integer): Database ID of the related record.
    - `related_record_ref` (Reference, selection='_selection_target_model', compute='_compute_related_record_ref', store=True): Odoo Reference field to the related record. Dynamically lists models from other DFR modules.
    - `message` (Text, required): Detailed log message.
    - `level` (Selection, required, default='info', selection=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('debug', 'Debug')], indexed): Severity level of the log entry.
    - `user_id` (Many2one, 'res.users', string='User', default=lambda self: self.env.user): User who triggered or is associated with the event.
    - `create_date` (Datetime, string='Timestamp', readonly=True, default=fields.Datetime.now): Timestamp of log creation (Odoo default).
- **Order:** `create_date desc`
- **Methods:**
    - `@api.depends('workflow_name', 'create_date') def _compute_name(self)`: Computes the `name` field.
    - `@api.model def _selection_target_model(self)`: Returns a list of relevant models for the `related_record_ref` selection. Initially, this can include `dfr.farmer`, `dfr.household`, `dfr.form.submission`. This list should be extensible.
    - `@api.depends('related_record_model', 'related_record_id') def _compute_related_record_ref(self)`: Computes the `related_record_ref` field.
    - `log_event(cls, workflow_name, record, message, level='info', user_id=None)`:
        - **Purpose:** Creates a new `workflow.log` entry.
        - **Parameters:**
            - `workflow_name` (str): Name of the workflow.
            - `record` (Odoo recordset, optional): The primary record associated with the event.
            - `message` (str): The log message.
            - `level` (str, default='info'): Log level ('info', 'warning', 'error', 'debug').
            - `user_id` (int, optional): ID of the user performing the action; defaults to current user.
        - **Logic:** Creates a new `workflow.log` record with the provided details. If `record` is provided, populates `related_record_model` and `related_record_id`.
- **Indexes:** `workflow_name`, `level`, `create_date`.

## 4. Module Structure and Component Design

This section details the design of each file within the `dfr_process_orchestrator` module.

### 4.1 `__init__.py`
- **Purpose:** Standard Odoo module initializer.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from . import models
  from . import wizard
  

### 4.2 `__manifest__.py`
- **Purpose:** Declares the module to Odoo, its metadata, dependencies, and data files.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  {
      'name': "DFR Business Process Orchestrator",
      'summary': """
          Manages and executes complex business processes for the DFR platform,
          including farmer lifecycle, notification triggers, and portal submission workflows.
      """,
      'description': """
          This module serves as a Service Orchestrator (Workflow Engine) for the DFR system.
          - Orchestrates farmer and household lifecycle management (REQ-FHR-011).
          - Triggers notifications based on system events (REQ-NS-001).
          - Manages workflows for farmer self-registrations from the portal (REQ-FSSP-005).
          - Provides general business process automation capabilities (REQ-PCA-020).
      """,
      'author': "FAO DFR Project Team (Developer Name/Company)", # To be updated
      'website': "https://www.fao.org", # To be updated
      'category': 'DigitalFarmerRegistry/Core',
      'version': '18.0.1.0.0',
      'license': 'MIT', # Or Apache-2.0, to be confirmed by REQ-CM-001
      'depends': [
          'base',
          'base_automation', # For Automated Actions
          'mail', # For activities, user notifications
          'dfr_common', # REPO-00-CORE-COMMON (Implicit dependency)
          'dfr_farmer_registry', # DFR_MOD_FARMER_REGISTRY
          'dfr_dynamic_forms', # DFR_MOD_DYNAMIC_FORMS
          'dfr_notifications_engine', # DFR_MOD_NOTIFICATIONS_ENGINE
          # dfr_farmer_portal is not a direct backend dependency here,
          # but workflows will react to data potentially created by it.
          # We ensure the models it might create (like dfr.farmer with a specific source) are available
          # through dfr_farmer_registry.
      ],
      'data': [
          'security/ir.model.access.csv',
          'security/security_groups.xml', # If any specific groups are needed

          'views/orchestration_rule_config_views.xml',
          'views/workflow_log_views.xml',
          'views/manual_workflow_step_wizard_views.xml',
          'views/orchestrator_menus.xml',

          'data/default_orchestration_configs.xml', # Load after models and views
          'data/farmer_lifecycle_workflows.xml',
          'data/notification_trigger_workflows.xml',
          'data/portal_submission_workflows.xml',
          'data/general_orchestration_rules.xml',
      ],
      'installable': True,
      'application': False, # This is a backend orchestrator, not a standalone app
      'auto_install': False,
  }
  
  **Note:** Dependencies on `dfr_common`, `dfr_farmer_registry`, `dfr_dynamic_forms`, `dfr_notifications_engine` are critical. `dfr_farmer_portal` is indirectly related as workflows here process data created via the portal (e.g., `dfr.farmer` records).

### 4.3 `models/__init__.py`
- **Purpose:** Initializes the `models` sub-package.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from . import orchestration_rule_config
  from . import workflow_log
  

### 4.4 `models/orchestration_rule_config.py`
- **Purpose:** Defines the `orchestration.rule.config` model.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from odoo import models, fields, api
  import json
  import logging

  _logger = logging.getLogger(__name__)

  class OrchestrationRuleConfig(models.Model):
      _name = 'orchestration.rule.config'
      _description = 'DFR Orchestration Rule Configuration'
      _order = 'workflow_key, parameter_key'

      name = fields.Char(string='Rule Name', required=True, help="Descriptive name for this configuration rule.")
      workflow_key = fields.Char(
          string='Workflow Key',
          required=True,
          index=True,
          help="Unique key identifying the workflow this rule applies to (e.g., 'farmer_status_change', 'portal_submission_validation')."
      )
      parameter_key = fields.Char(
          string='Parameter Key',
          required=True,
          index=True,
          help="Unique key for the specific parameter within the workflow (e.g., 'active_status_notification_template_id', 'supervisor_group_id_for_portal_review')."
      )
      parameter_value = fields.Text(
          string='Parameter Value',
          help="Value of the parameter. Can be a simple string, number, or a JSON string for complex rules."
      )
      description = fields.Text(string='Description', help="Explanation of the rule and its purpose.")
      is_active = fields.Boolean(string='Active', default=True, help="Whether this configuration rule is currently active.")

      _sql_constraints = [
          ('workflow_parameter_key_uniq', 'unique (workflow_key, parameter_key)',
           'A parameter key must be unique per workflow key!')
      ]

      @api.model
      def get_config_value(self, workflow_key, parameter_key, default_value=None, expect_json=False):
          """
          Retrieves the value of a specific configuration parameter.
          :param workflow_key: The key of the workflow.
          :param parameter_key: The key of the parameter.
          :param default_value: Value to return if the parameter is not found or not active.
          :param expect_json: If True, tries to parse the value as JSON.
          :return: The parameter value, or default_value.
          """
          config_value_record = self.search([
              ('workflow_key', '=', workflow_key),
              ('parameter_key', '=', parameter_key),
              ('is_active', '=', True)
          ], limit=1)

          if config_value_record:
              value_str = config_value_record.parameter_value
              if expect_json:
                  try:
                      return json.loads(value_str)
                  except (json.JSONDecodeError, TypeError) as e:
                      _logger.warning(
                          "Failed to parse JSON for config '%s/%s'. Value: '%s'. Error: %s. Returning default.",
                          workflow_key, parameter_key, value_str, e
                      )
                      return default_value
              return value_str
          
          _logger.debug(
              "Config value for '%s/%s' not found or inactive. Returning default value: %s",
              workflow_key, parameter_key, default_value
          )
          return default_value
  

### 4.5 `models/workflow_log.py`
- **Purpose:** Defines the `workflow.log` model.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from odoo import models, fields, api

  class WorkflowLog(models.Model):
      _name = 'workflow.log'
      _description = 'DFR Workflow Log'
      _order = 'create_date desc'

      name = fields.Char(string='Log Entry Name', compute='_compute_name', store=True, readonly=True)
      workflow_name = fields.Char(string='Workflow Name', required=True, index=True, help="Name or key of the workflow being logged.")
      
      related_record_model = fields.Char(string='Related Model', index=True, help="Model of the primary record this log entry relates to.")
      related_record_id = fields.Integer(string='Related Record ID', index=True, help="Database ID of the related record.")
      
      # Using a selection of models to avoid performance issues with a fully dynamic Reference field
      # This list can be extended by other modules if needed.
      @api.model
      def _selection_target_model(self):
          # Add other relevant DFR models here as the system grows
          return [
              ('dfr.farmer', 'Farmer'),
              ('dfr.household', 'Household'),
              ('dfr.farm', 'Farm'),
              ('dfr.plot', 'Plot'),
              ('dfr.form.submission', 'Form Submission'),
              ('res.users', 'User'),
              # Add other models that might be part of workflows
          ]

      related_record_ref = fields.Reference(
          selection='_selection_target_model', 
          string='Related Record', 
          compute='_compute_related_record_ref', 
          store=True, # Storing for easier searching/filtering if needed
          readonly=True,
          help="Reference to the primary record associated with this log entry."
      )
      
      message = fields.Text(string='Message', required=True, help="Detailed log message.")
      level = fields.Selection([
          ('info', 'Info'),
          ('warning', 'Warning'),
          ('error', 'Error'),
          ('debug', 'Debug') # Debug might be too verbose for production, consider removing or making configurable
          ], string='Level', required=True, default='info', index=True, help="Severity level of the log entry.")
      
      user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, index=True, help="User who triggered or is associated with the event.")
      # create_date is an Odoo default field (Datetime)

      @api.depends('workflow_name', 'create_date')
      def _compute_name(self):
          for log in self:
              ts = fields.Datetime.to_string(log.create_date) if log.create_date else 'No Timestamp'
              log.name = f"Log: {log.workflow_name or 'Unnamed Workflow'} - {ts}"

      @api.depends('related_record_model', 'related_record_id')
      def _compute_related_record_ref(self):
          for log in self:
              if log.related_record_model and log.related_record_id:
                  log.related_record_ref = f"{log.related_record_model},{log.related_record_id}"
              else:
                  log.related_record_ref = False
      
      @api.model
      def log_event(self, workflow_name, message, level='info', record=None, user_id=None):
          """
          Creates a new workflow.log entry.
          :param workflow_name: str, Name of the workflow.
          :param message: str, The log message.
          :param level: str, Log level ('info', 'warning', 'error', 'debug').
          :param record: Odoo recordset, optional, The primary record associated with the event.
          :param user_id: int, optional, ID of the user performing the action; defaults to current user's ID.
          :return: The created workflow.log record.
          """
          vals = {
              'workflow_name': workflow_name,
              'message': message,
              'level': level,
              'user_id': user_id if user_id is not None else self.env.user.id,
          }
          if record and isinstance(record, models.BaseModel) and len(record) == 1: # Ensure it's a single record
              vals['related_record_model'] = record._name
              vals['related_record_id'] = record.id
          
          return self.create(vals)

  

### 4.6 Workflow Definitions (XML Data Files in `data/`)

#### 4.6.1 `data/farmer_lifecycle_workflows.xml` (REQ-FHR-011)
- **Purpose:** Defines Odoo Automated Actions and Server Actions for farmer/household lifecycle management.
- **Key Workflows/Automations:**
    1.  **Farmer Status Change to 'Active'**:
        -   Trigger: On `dfr.farmer` record, when `status` field is updated and `status == 'active'`.
        -   Action: Call a Server Action.
        -   Server Action (`action_farmer_activated`):
            -   Logs event to `workflow.log`.
            -   Checks `orchestration.rule.config` for `farmer_status_change/active_status_notification_template_id`.
            -   If template ID found, calls `dfr.notification.engine` service to send "Welcome/Activation" notification to the farmer.
            -   (Future enhancement: check eligibility for any programs and trigger relevant actions).
    2.  **Farmer Status Change to 'Inactive'**:
        -   Trigger: On `dfr.farmer` record, when `status` field is updated and `status == 'inactive'`.
        -   Action: Call a Server Action.
        -   Server Action (`action_farmer_deactivated`):
            -   Logs event to `workflow.log`.
            -   (Optional: If system rules require, update related household member status or other linked records).
            -   Checks `orchestration.rule.config` for `farmer_status_change/inactive_status_notification_template_id`.
            -   If template ID found, calls `dfr.notification.engine` service to send "Deactivation Confirmation" (if policy dictates sending this).
    3.  **Farmer Status Change to 'Deceased'**:
        -   Trigger: On `dfr.farmer` record, when `status` field is updated and `status == 'deceased'`.
        -   Action: Call a Server Action.
        -   Server Action (`action_farmer_deceased`):
            -   Logs event to `workflow.log`.
            -   Sets an `is_archived` flag (if such a field exists on `dfr.farmer`) to True.
            -   (Optional: Create follow-up activity for an admin to review/archive associated household/plot data if necessary).
    4.  **Farmer Status Change to 'Duplicate'**:
        -   Trigger: On `dfr.farmer` record, when `status` field is updated and `status == 'duplicate'`.
        -   Action: Call a Server Action.
        -   Server Action (`action_farmer_marked_duplicate`):
            -   Logs event to `workflow.log`.
            -   Ensures the record is archived or otherwise removed from active lists.
    5.  **Farmer Status Change from 'Pending Verification' to 'Active' (Approval):**
        -   This is typically a manual action by a Supervisor/Admin, but an Automated Action can react to the change.
        -   Trigger: On `dfr.farmer`, `status` changes from `'pending_verification'` to `'active'`.
        -   Action: Same as "Farmer Status Change to 'Active'" (or a specific "Approval Notification" can be triggered).
- **Sample XML Structure Snippet (for one automation):**
  xml
  <odoo>
      <data noupdate="1"> <!-- noupdate="1" for system automations -->

          <!-- Server Action: Farmer Activated -->
          <record id="action_server_farmer_activated" model="ir.actions.server">
              <field name="name">Server Action: Farmer Activated</field>
              <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
              <field name="state">code</field>
              <field name="code">
if record:
    env['workflow.log'].log_event(
        workflow_name='Farmer Lifecycle',
        message=f"Farmer {record.name} (UID: {record.farmer_uid}) activated.",
        level='info',
        record=record
    )
    # Example: Get notification template ID from config
    # notification_template_id_str = env['orchestration.rule.config'].get_config_value(
    #    'farmer_status_change', 
    #    'active_status_notification_template_id'
    # )
    # if notification_template_id_str:
    #    try:
    #        notification_template_id = int(notification_template_id_str)
    #        # Call dfr_notifications_engine service to send notification
    #        # env['dfr.notification.engine'].send_notification(
    #        #    record, 
    #        #    notification_template_id, 
    #        #    {'farmer_name': record.name}
    #        # )
    #    except ValueError:
    #        env['workflow.log'].log_event(
    #            workflow_name='Farmer Lifecycle',
    #            message=f"Invalid notification template ID configured for farmer activation: {notification_template_id_str}",
    #            level='error',
    #            record=record
    #        )
    #    pass # Add actual notification call here
              </field>
          </record>

          <!-- Automated Action: On Farmer Activation -->
          <record id="automation_farmer_activated" model="base.automation">
              <field name="name">Automated: Farmer Activation Process</field>
              <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
              <field name="trigger">on_write</field>
              <field name="filter_domain">[('status', '=', 'active')]</field>
              <!-- filter_pre_domain ensures this runs only when status *changes* to active -->
              <field name="filter_pre_domain">[('status', '!=', 'active')]</field> 
              <field name="state">code</field> <!-- Use 'action' to call a server action by ID -->
              <field name="action_server_id" ref="action_server_farmer_activated"/>
          </record>

          <!-- Similar structures for other status transitions -->

      </data>
  </odoo>
  

#### 4.6.2 `data/notification_trigger_workflows.xml` (REQ-NS-001)
- **Purpose:** Defines Automated Actions and Server Actions to trigger notifications.
- **Key Workflows/Automations:**
    1.  **Successful Farmer Registration Notification (to Farmer)**:
        -   Trigger: On `dfr.farmer` record creation (after successful validation/approval, usually when status becomes 'active').
        -   Action: Server Action `action_notify_farmer_registration_success`.
        -   Server Action Logic:
            -   Logs event.
            -   Retrieves farmer contact details (phone/email).
            -   Retrieves relevant notification template ID from `orchestration.rule.config` (e.g., `farmer_registration/success_farmer_sms_template_id`).
            -   Calls `dfr.notification.engine` service with farmer record, template ID, and context variables.
    2.  **Farmer Self-Registration Submission Confirmation (to Farmer)**:
        -   Trigger: On `dfr.farmer` record creation where `source == 'portal'` and `status == 'pending_verification'`.
        -   Action: Server Action `action_notify_portal_submission_received`.
        -   Server Action Logic: Similar to above, but uses a "submission received" template.
    3.  **Eligibility Confirmation Notification (to Farmer)**:
        -   Trigger: On `dfr.form.submission` update where a specific field indicating eligibility (e.g., `is_eligible_for_subsidy`) becomes `True`. This might require a custom model field on `dfr.form.submission` or logic within its `write` method to trigger a custom event if Odoo's base_automation cannot precisely target this. Alternatively, the dynamic form engine itself, upon processing a submission that results in eligibility, could call a method in this orchestrator to trigger the notification.
        -   Action: Server Action `action_notify_program_eligibility`.
        -   Server Action Logic:
            -   Logs event.
            -   Identifies the farmer linked to the `dfr.form.submission`.
            -   Retrieves eligibility program details and notification template ID from `orchestration.rule.config` or the form submission itself.
            -   Calls `dfr.notification.engine`.
- **XML Structure:** Similar to `farmer_lifecycle_workflows.xml`, using `base.automation` and `ir.actions.server`.

#### 4.6.3 `data/portal_submission_workflows.xml` (REQ-FSSP-005)
- **Purpose:** Manages the workflow of farmer self-registrations from the portal.
- **Key Workflows/Automations:**
    1.  **New Portal Submission - Initial Assignment/Notification**:
        -   Trigger: On `dfr.farmer` record creation where `source == 'portal'` and `status == 'pending_verification'`.
        -   Action: Server Action `action_process_new_portal_submission`.
        -   Server Action Logic:
            -   Logs event to `workflow.log`.
            -   Retrieves configured supervisor/admin group ID or specific user ID for review from `orchestration.rule.config` (e.g., `portal_submission/review_assignee_group_id`).
            -   Creates an Odoo Activity (`mail.activity`) assigned to that group/user for review of the new farmer record.
            -   (Optional) Sends an internal Odoo notification or email to the assignee(s).
    2.  **Portal Submission Approved**:
        -   Trigger: When a supervisor/admin manually changes the status of a portal-submitted `dfr.farmer` from 'pending_verification' (or 'pending_field_validation') to 'active'.
        -   Action: Leverages the existing 'Farmer Status Change to Active' automation in `farmer_lifecycle_workflows.xml` OR a dedicated server action if different logic is needed for portal-approved farmers.
    3.  **Portal Submission Rejected**:
        -   Trigger: When a supervisor/admin manually changes the status of a portal-submitted `dfr.farmer` to 'rejected'.
        -   Action: Server Action `action_process_portal_submission_rejected`.
        -   Server Action Logic:
            -   Logs event.
            -   Updates the farmer record with rejection reason (if a field exists).
            -   Sends notification to farmer (if policy dictates and template exists).
            -   (Optional) Archives the rejected record.
- **XML Structure:** Similar to `farmer_lifecycle_workflows.xml`.

#### 4.6.4 `data/general_orchestration_rules.xml` (REQ-PCA-020)
- **Purpose:** Defines other general business process automations.
- **Potential Workflows/Automations:**
    1.  **De-duplication Resolution Follow-up**:
        -   Trigger: This is more complex. If `dfr_farmer_registry` flags potential duplicates and creates a task/record for review, an automated action here could:
            -   Be time-based (e.g., daily check on open de-duplication tasks older than X days).
            -   Action: Send a reminder notification to the assigned admin/supervisor.
    2.  **Data Quality Checks (Periodic)**:
        -   Trigger: Scheduled Action (e.g., weekly).
        -   Action: Server Action `action_perform_data_quality_audit`.
        -   Server Action Logic:
            -   Executes predefined queries or checks (e.g., farmers missing critical data, plots with invalid GPS).
            -   Logs findings to `workflow.log` or creates activities for data correction.
    3.  **Stale 'Pending Verification' Records Alert**:
        -   Trigger: Scheduled Action (e.g., daily).
        -   Action: Server Action `action_alert_stale_pending_verifications`.
        -   Server Action Logic:
            -   Finds `dfr.farmer` records with `status == 'pending_verification'` older than a configurable threshold (from `orchestration.rule.config`).
            -   Notifies relevant administrators/supervisors.
- **XML Structure:** Similar, using `base.automation` (for event-driven or time-based) and `ir.cron` (for scheduled server actions) along with `ir.actions.server`.

#### 4.6.5 `data/security_groups.xml`
- **Purpose:** Defines specific security groups if needed for orchestration management.
- **Content (Example - if needed):**
  xml
  <odoo>
      <data>
          <record id="group_dfr_workflow_administrator" model="res.groups">
              <field name="name">DFR Workflow Administrator</field>
              <field name="category_id" ref="base.module_category_administration_settings"/>
              <field name="comment">Group for users managing DFR workflow configurations and logs.</field>
              <!-- Implied Users: Add users to this group to grant permissions -->
              <!-- Users: Add specific users if needed, e.g., <field name="users" eval="[(4, ref('base.user_root')),(4, ref('base.user_admin'))]"/> -->
          </record>
      </data>
  </odoo>
  
  **Note:** Often, existing Odoo groups like "Settings" (`base.group_system`) or specific application admin groups are sufficient. This file might be empty or not needed if standard groups cover access to configuration models.

#### 4.6.6 `data/default_orchestration_configs.xml`
- **Purpose:** Provides initial default configurations for `orchestration.rule.config`.
- **Content (Example):**
  xml
  <odoo>
      <data noupdate="1"> <!-- noupdate="1" so these are not overwritten on module update unless explicitly changed -->
          <record id="config_farmer_activation_sms_template" model="orchestration.rule.config">
              <field name="name">Farmer Activation SMS Template ID</field>
              <field name="workflow_key">farmer_status_change</field>
              <field name="parameter_key">active_status_sms_template_id</field>
              <field name="parameter_value"></field> <!-- Leave empty or set a placeholder default ID if one exists from dfr_notifications_engine demo data -->
              <field name="description">Odoo Mail Template ID (dfr.notification.template) for SMS sent upon farmer activation.</field>
              <field name="is_active">True</field>
          </record>

          <record id="config_portal_review_assignee_group" model="orchestration.rule.config">
              <field name="name">Portal Submission Review Assignee Group</field>
              <field name="workflow_key">portal_submission</field>
              <field name="parameter_key">review_assignee_group_id</field>
              <field name="parameter_value" model="res.groups" eval="ref('dfr_farmer_registry.group_dfr_supervisor', False) or False"/> <!-- Example: ref to a supervisor group from farmer registry module -->
              <field name="description">Group ID (res.groups) to whom portal submissions are assigned for review via an activity.</field>
              <field name="is_active">True</field>
          </record>
          
          <record id="config_stale_pending_verification_days" model="orchestration.rule.config">
              <field name="name">Stale Pending Verification Threshold (Days)</field>
              <field name="workflow_key">data_quality</field>
              <field name="parameter_key">stale_pending_verification_days</field>
              <field name="parameter_value">7</field>
              <field name="description">Number of days after which a 'Pending Verification' record is considered stale and an alert is triggered.</field>
              <field name="is_active">True</field>
          </record>
      </data>
  </odoo>
  

### 4.7 `wizard/__init__.py`
- **Purpose:** Initializes the `wizard` sub-package.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from . import manual_workflow_step_wizard
  

### 4.8 `wizard/manual_workflow_step_wizard.py`
- **Purpose:** Defines a wizard for manual workflow intervention.
- **Content:**
  python
  # -*- coding: utf-8 -*-
  from odoo import models, fields, api, _
  from odoo.exceptions import UserError, ValidationError
  import logging

  _logger = logging.getLogger(__name__)

  class ManualWorkflowStepWizard(models.TransientModel):
      _name = 'manual.workflow.step.wizard'
      _description = 'Manual Workflow Step Execution Wizard'

      # This selection should ideally be populated dynamically or be very generic.
      # For now, providing some common DFR workflow types.
      WORKFLOW_TYPES = [
          ('farmer_lifecycle', 'Farmer Lifecycle'),
          ('portal_submission', 'Portal Submission Review'),
          ('deduplication_review', 'De-duplication Review Task'), 
          # Add other relevant workflow contexts
      ]
      
      workflow_type = fields.Selection(
          selection=WORKFLOW_TYPES,
          string='Workflow Type',
          required=True,
          help="Select the type of workflow you want to interact with."
      )
      
      # Dynamically determine applicable models based on workflow_type if possible,
      # or provide a generic way to select any record.
      # For simplicity, using a generic Reference field here.
      record_ref_model = fields.Char(string="Record Model", help="Technical name of the model (e.g., dfr.farmer).")
      record_ref_id = fields.Integer(string="Record ID", help="ID of the record.")

      record_ref = fields.Reference(
          string='Target Record', 
          selection='_selection_target_model_wizard',
          help="Select the record to apply the manual step to."
          # compute='_compute_record_ref', # If model/id are separate fields
          # inverse='_inverse_record_ref'   # If model/id are separate fields
      )

      # This field would ideally be filtered based on workflow_type and selected record_ref.
      # For now, a generic Many2one to ir.actions.server.
      target_step_action_id = fields.Many2one(
          'ir.actions.server',
          string='Target Workflow Step/Action',
          required=True,
          domain="[('model_id.model', '=', record_ref_model)]", # Basic domain, might need refinement
          help="Select the server action representing the workflow step to execute manually."
      )
      
      reason = fields.Text(string='Reason for Manual Intervention', required=True)

      @api.model
      def _selection_target_model_wizard(self):
          # Reuse the selection from workflow_log or create a broader one
          return self.env['workflow.log']._selection_target_model() # Example reuse

      # If using separate model/id fields to populate record_ref:
      # @api.onchange('record_ref_model', 'record_ref_id')
      # def _onchange_record_identifier(self):
      #    if self.record_ref_model and self.record_ref_id:
      #        try:
      #            self.record_ref = f"{self.record_ref_model},{self.record_ref_id}"
      #        except Exception:
      #            self.record_ref = False # or raise warning
      #    else:
      #        self.record_ref = False

      def action_execute_manual_step(self):
          self.ensure_one()
          if not self.record_ref:
              raise UserError(_("Target record must be selected."))
          if not self.target_step_action_id:
              raise UserError(_("Target workflow step/action must be selected."))

          target_record = self.record_ref
          
          # Log the manual intervention
          self.env['workflow.log'].log_event(
              workflow_name=f"Manual Intervention ({self.workflow_type})",
              message=f"Manually executing step '{self.target_step_action_id.name}' on record {target_record.display_name}. Reason: {self.reason}",
              level='warning',
              record=target_record,
              user_id=self.env.user.id
          )

          _logger.info(
              f"User {self.env.user.name} manually triggered action '{self.target_step_action_id.name}' "
              f"on record {target_record._name} ID {target_record.id}."
          )
          
          # Execute the server action
          # The server action's code will run in the context of the target_record
          try:
              self.target_step_action_id.with_context(active_id=target_record.id, active_ids=[target_record.id], active_model=target_record._name).run()
              
              # Check if the target record has a 'message_post' method (chatter)
              if hasattr(target_record, 'message_post'):
                  target_record.message_post(body=_(
                      "Workflow step '%(action_name)s' manually executed by %(user_name)s. Reason: %(reason)s",
                      action_name=self.target_step_action_id.name,
                      user_name=self.env.user.name,
                      reason=self.reason
                  ))
          except Exception as e:
              _logger.error(f"Error executing manual workflow step '{self.target_step_action_id.name}' on {target_record}: {e}")
              self.env['workflow.log'].log_event(
                  workflow_name=f"Manual Intervention ({self.workflow_type}) - ERROR",
                  message=f"Error executing step '{self.target_step_action_id.name}' on record {target_record.display_name}. Error: {e}",
                  level='error',
                  record=target_record
              )
              raise UserError(_("Failed to execute the workflow step. Error: %s") % e)

          return {'type': 'ir.actions.act_window_close'}

  

### 4.9 View Definitions (XML Files in `views/`)

#### 4.9.1 `views/orchestration_rule_config_views.xml`
- **Purpose:** UI for `orchestration.rule.config` model.
- **Content:** Standard Odoo tree, form, and search views.
  - **Tree View:** Fields: `name`, `workflow_key`, `parameter_key`, `is_active`.
  - **Form View:** Fields: `name`, `workflow_key`, `parameter_key`, `parameter_value` (as text area), `description`, `is_active`.
  - **Search View:** Filters on `workflow_key`, `parameter_key`, `is_active`. Group by `workflow_key`.
- **XML Structure Snippet (Form View):**
  xml
  <record id="view_orchestration_rule_config_form" model="ir.ui.view">
      <field name="name">orchestration.rule.config.form</field>
      <field name="model">orchestration.rule.config</field>
      <field name="arch" type="xml">
          <form string="Orchestration Rule Configuration">
              <sheet>
                  <group>
                      <field name="name"/>
                      <field name="workflow_key"/>
                      <field name="parameter_key"/>
                      <field name="is_active"/>
                  </group>
                  <group string="Parameter Value">
                      <field name="parameter_value" nolabel="1" widget="text"/>
                  </group>
                  <group string="Description">
                      <field name="description" nolabel="1" widget="text"/>
                  </group>
              </sheet>
          </form>
      </field>
  </record>
  
  (Similar definitions for tree and search views)

#### 4.9.2 `views/workflow_log_views.xml`
- **Purpose:** UI for `workflow.log` model.
- **Content:** Standard Odoo tree, form, and search views.
  - **Tree View:** Fields: `create_date` (as 'Timestamp'), `name`, `workflow_name`, `level`, `related_record_ref`, `user_id`, `message` (shortened).
  - **Form View:** Read-only. Fields: `name`, `create_date`, `workflow_name`, `level`, `user_id`, `related_record_ref`, `message` (full).
  - **Search View:** Filters on `workflow_name`, `level`, `user_id`, `create_date` (range), `related_record_ref`. Group by `workflow_name`, `level`, `user_id`.
- **XML Structure:** Similar to above, defining tree, form (read-only recommended), and search views.

#### 4.9.3 `views/manual_workflow_step_wizard_views.xml`
- **Purpose:** UI for `manual.workflow.step.wizard`.
- **Content:**
  - **Form View:** Fields: `workflow_type`, `record_ref_model`, `record_ref_id`, `record_ref` (potentially made invisible if model/id are used for selection and record_ref is computed, or used as primary selector if selection logic is rich enough), `target_step_action_id`, `reason`. Footer with "Execute Step" and "Cancel" buttons.
- **XML Structure Snippet:**
  xml
  <record id="view_manual_workflow_step_wizard_form" model="ir.ui.view">
      <field name="name">manual.workflow.step.wizard.form</field>
      <field name="model">manual.workflow.step.wizard</field>
      <field name="arch" type="xml">
          <form string="Manual Workflow Step Execution">
              <group>
                  <field name="workflow_type"/>
                  <!-- Option 1: Select by Model + ID -->
                  <field name="record_ref_model" 
                         attrs="{'invisible': [('workflow_type', '=', False)]}"
                         placeholder="e.g., dfr.farmer"/>
                  <field name="record_ref_id" 
                         attrs="{'invisible': [('workflow_type', '=', False), ('record_ref_model', '=', False)]}"/>
                  <!-- Option 2: Select by Reference field (preferred if _selection_target_model_wizard is robust) -->
                  <!-- <field name="record_ref" options="{'no_create': True, 'no_open': True}"
                         attrs="{'invisible': [('workflow_type', '=', False)]}"/> -->
              </group>
              <group>
                  <field name="target_step_action_id" 
                         domain="[('model_id.model', '=', record_ref_model)]" 
                         options="{'no_create': True, 'no_open': True}"
                         attrs="{'invisible': ['|', ('workflow_type', '=', False), ('record_ref_model', '=', False), ('record_ref_id', '=', False)]}"/>
                         <!-- Adjust attrs based on how record_ref is handled -->
              </group>
              <group>
                  <field name="reason" widget="text"/>
              </group>
              <footer>
                  <button name="action_execute_manual_step" string="Execute Step" type="object" class="btn-primary"/>
                  <button string="Cancel" class="btn-secondary" special="cancel"/>
              </footer>
          </form>
      </field>
  </record>

  <record id="action_manual_workflow_step_wizard" model="ir.actions.act_window">
      <field name="name">Manual Workflow Step</field>
      <field name="res_model">manual.workflow.step.wizard</field>
      <field name="view_mode">form</field>
      <field name="target">new</field>
  </record>
  

#### 4.9.4 `views/orchestrator_menus.xml`
- **Purpose:** Creates Odoo backend menu items.
- **Content:**
  xml
  <odoo>
      <data>
          <!-- Main DFR Orchestrator Menu (e.g., under Settings or a top-level DFR App Menu) -->
          <menuitem 
              id="menu_dfr_orchestrator_root" 
              name="DFR Process Orchestrator"
              parent="base.menu_administration" <!-- Example: Under Settings/Technical -->
              sequence="90"/> 
              <!-- Or parent="your_dfr_top_level_app_menu_id" if such menu exists -->

          <menuitem
              id="menu_orchestration_rule_config"
              name="Workflow Configurations"
              parent="menu_dfr_orchestrator_root"
              action="action_orchestration_rule_config_tree" 
              sequence="10"/>
          <!-- Define action_orchestration_rule_config_tree linking to tree view of orchestration.rule.config -->
          <record id="action_orchestration_rule_config_tree" model="ir.actions.act_window">
              <field name="name">Workflow Configurations</field>
              <field name="res_model">orchestration.rule.config</field>
              <field name="view_mode">tree,form</field>
          </record>

          <menuitem
              id="menu_workflow_log"
              name="Workflow Logs"
              parent="menu_dfr_orchestrator_root"
              action="action_workflow_log_tree"
              sequence="20"/>
          <!-- Define action_workflow_log_tree linking to tree view of workflow.log -->
          <record id="action_workflow_log_tree" model="ir.actions.act_window">
              <field name="name">Workflow Logs</field>
              <field name="res_model">workflow.log</field>
              <field name="view_mode">tree,form</field>
          </record>

          <menuitem
              id="menu_manual_workflow_step_wizard"
              name="Manual Workflow Intervention"
              parent="menu_dfr_orchestrator_root"
              action="action_manual_workflow_step_wizard" 
              sequence="30"/>
      </data>
  </odoo>
  
  **Note:** `parent` attribute for `menu_dfr_orchestrator_root` should be adjusted based on where this menu should appear (e.g., under Settings, or a DFR-specific top-level application menu if one is created by another module).

### 4.10 Security Definitions

#### 4.10.1 `security/ir.model.access.csv`
- **Purpose:** Defines model-level access rights.
- **Content:**
  csv
  id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  access_orchestration_rule_config_system,orchestration.rule.config.system,model_orchestration_rule_config,base.group_system,1,1,1,1
  access_workflow_log_system,workflow.log.system,model_workflow_log,base.group_system,1,0,0,0
  access_workflow_log_user,workflow.log.user,model_workflow_log,base.group_user,1,0,0,0
  access_manual_workflow_step_wizard_system,manual.workflow.step.wizard.system,model_manual_workflow_step_wizard,base.group_system,1,1,1,1
  
  **Explanation:**
  - `orchestration.rule.config`: Full access for System Administrators (`base.group_system`).
  - `workflow.log`: Read access for general users (`base.group_user`) and System Administrators. Creation is done programmatically. Deletion should be highly restricted or disallowed via UI for audit integrity.
  - `manual.workflow.step.wizard`: Full access for System Administrators to launch and use the wizard.

## 5. Integration with Other DFR Modules
-   **DFR_MOD_FARMER_REGISTRY:**
    -   **Listens to:** Changes in `dfr.farmer` and `dfr.household` status fields, creation of new `dfr.farmer` records (especially those with `source='portal'`).
    -   **Actions:** Triggers server actions that may update `dfr.farmer` status (e.g., setting to 'approved', 'rejected', 'archived').
-   **DFR_MOD_DYNAMIC_FORMS:**
    -   **Listens to:** Updates on `dfr.form.submission` records, particularly fields that might indicate eligibility or require follow-up.
    -   **Actions:** Triggers server actions based on form submission events.
-   **DFR_MOD_NOTIFICATIONS_ENGINE:**
    -   **Actions:** Calls services/methods provided by `dfr_notifications_engine` to send notifications. It passes context (e.g., farmer record, template ID, dynamic data) to the notification engine. Configuration for which template to use for which event is often stored in `orchestration.rule.config`.
-   **DFR_MOD_FARMER_PORTAL:**
    -   This orchestrator processes records that are *initiated* by the portal (e.g., `dfr.farmer` records created with `source='portal'`). It doesn't directly call the portal but manages the backend workflow for data originating from it.
-   **DFR_MOD_CORE_COMMON:**
    -   Uses utility functions or base model features if provided by the common core module.

## 6. Error Handling and Logging
-   Server Actions will use Python `try-except` blocks for critical operations (e.g., calls to other services).
-   Errors encountered during automated actions or server actions will be logged to `workflow.log` with `level='error'`, including tracebacks or relevant error messages.
-   `orchestration.rule.config.get_config_value` logs warnings if expected configurations are missing.
-   Wizards will use Odoo's `UserError` to provide feedback to users on invalid operations or failures.

## 7. Deployment and Configuration Notes
-   Default configurations for critical workflow parameters should be provided in `data/default_orchestration_configs.xml` to ensure basic functionality upon installation.
-   Administrators (National Admins or Super Admins depending on governance) will need permissions to access and modify `orchestration.rule.config` records to tailor workflows.
-   Automated Actions in XML are set with `noupdate="1"` to prevent them from being overwritten during module updates, allowing administrators to customize them post-installation if needed (though direct XML customization is generally discouraged for end-users; UI configuration is preferred).
-   Scheduled actions (if any, for periodic checks) will be defined using `ir.cron` records in XML.

## 8. Future Considerations / Extensibility
-   **More Granular Workflow Steps:** For very complex workflows, consider breaking them into smaller, chainable server actions or even dedicated Odoo `workflow` objects (though Odoo's trend is away from the old `workflow` model towards `base.automation`).
-   **Dynamic Action Selection in Wizards:** The `manual.workflow.step.wizard` could be enhanced to dynamically populate the `target_step_action_id` domain based on the selected `workflow_type` and `record_ref` to only show relevant actions.
-   **Visual Workflow Monitoring:** While `workflow.log` provides textual logs, future enhancements could explore integrations with visual BPMN tools or dashboards if Odoo's capabilities allow, for monitoring in-flight or completed orchestrations. (This is likely beyond the scope of Odoo Community's standard features).
-   **Extensible Target Models for Logging/Wizards:** The `_selection_target_model` methods in `workflow.log` and the wizard should be designed so other DFR modules can easily extend the list of selectable models.