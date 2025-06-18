# DFR RBAC Configuration Module - Software Design Specification

## 1. Introduction

This document provides the Software Design Specification (SDS) for the DFR RBAC Configuration Module (`DFR_MOD_RBAC_CONFIG`). This Odoo module is responsible for defining all DFR-specific security configurations, including user roles (security groups), model-level access control lists (ACLs), and record-level access rules. It primarily consists of declarative XML and CSV configuration files.

This module implements requirements REQ-5-001, REQ-5-002, REQ-5-004, and REQ-SADG-001.

## 2. Module Overview

*   **Module Name:** `dfr_security_config`
*   **Namespace:** `odoo.addons.dfr_security_config`
*   **Output Path:** `dfr_addons/dfr_security_config`
*   **Description:** Defines DFR-specific user roles (Odoo groups), access control lists (ACLs - `ir.model.access.csv`), and record rules (`ir.rule`) for all DFR modules.
*   **Framework:** Odoo 18.0 Community
*   **Technology:** Odoo Security Framework
*   **Language:** XML, CSV
*   **Dependencies:**
    *   `base` (Odoo core)
    *   `dfr_common_core` (for any shared categories or base configurations if applicable)
    *   `dfr_farmer_registry` (for securing Farmer, Household, Plot models, etc.)
    *   `dfr_dynamic_forms` (for securing Dynamic Form Template, Submission models, etc.)
    *   *Note: Add dependencies for any other DFR modules that define models requiring security configurations defined within this module.*

## 3. File Structure and Detailed Design

The file structure for this module is as follows. Detailed specifications for each file are provided below.


dfr_addons/dfr_security_config/
├── __init__.py
├── __manifest__.py
└── security/
    ├── __init__.py
    ├── dfr_security_groups.xml
    ├── ir.model.access.csv
    └── dfr_record_rules.xml


### 3.1. `__init__.py`

*   **Path:** `dfr_addons/dfr_security_config/__init__.py`
*   **Description:** Python package initializer for the `dfr_security_config` Odoo module.
*   **Purpose:** Marks the directory as an Odoo module package.
*   **Logic:** This file will be empty as this module primarily contains data files.
    python
    # -*- coding: utf-8 -*-
    # Part of Odoo. See LICENSE file for full copyright and licensing details.
    

### 3.2. `__manifest__.py`

*   **Path:** `dfr_addons/dfr_security_config/__manifest__.py`
*   **Description:** Odoo module manifest file.
*   **Purpose:** Describes the module to Odoo, including metadata, dependencies, and data files.
*   **Content:**
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'DFR RBAC Configuration',
        'version': '18.0.1.0.0',
        'summary': 'Security configurations including roles, ACLs, and record rules for the Digital Farmer Registry.',
        'description': """
    This module defines DFR-specific user roles (Odoo groups), 
    access control lists (ACLs - ir.model.access.csv), and 
    record rules (ir.rule) for all DFR application modules.
    It centralizes security definitions for the DFR platform.
        """,
        'category': 'DFR/Security', # Assumes 'DFR' is a top-level category defined elsewhere or this will create it.
        'author': 'FAO DFR Project Team',
        'website': 'https://www.fao.org', # Placeholder
        'license': 'MIT', # Or 'Apache-2.0' as per final project decision (REQ-CM-001)
        'depends': [
            'base',
            'dfr_common_core', # For any shared elements like module categories
            # Add all DFR modules whose models are secured by this module.
            # This ensures models are known to Odoo before ACLs/rules are applied.
            # Examples:
            'dfr_farmer_registry', 
            'dfr_dynamic_forms',
            # 'dfr_notifications_engine', # if models from here are secured
            # 'dfr_data_management_tools', # if models from here are secured
        ],
        'data': [
            'security/dfr_security_groups.xml',
            'security/ir.model.access.csv',
            'security/dfr_record_rules.xml',
        ],
        'installable': True,
        'application': False, # This is a configuration module, not a standalone application
        'auto_install': False,
    }
    

### 3.3. `security/__init__.py`

*   **Path:** `dfr_addons/dfr_security_config/security/__init__.py`
*   **Description:** Python package initializer for the `security` sub-directory.
*   **Purpose:** Marks the `security` directory as a Python package.
*   **Logic:** This file will be empty.
    python
    # -*- coding: utf-8 -*-
    # Part of Odoo. See LICENSE file for full copyright and licensing details.
    

### 3.4. `security/dfr_security_groups.xml`

*   **Path:** `dfr_addons/dfr_security_config/security/dfr_security_groups.xml`
*   **Description:** Defines DFR-specific user security groups (roles). Implements REQ-5-001.
*   **Purpose:** Establishes distinct user roles for the DFR system.
*   **Content Structure:**
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent accidental overwrites on module update for groups -->

            <!-- DFR Module Category -->
            <record model="ir.module.category" id="module_category_dfr">
                <field name="name">DFR</field>
                <field name="description">Digital Farmer Registry specific functionalities and configurations.</field>
                <field name="sequence">25</field> <!-- Adjust sequence as needed -->
            </record>

            <!-- DFR User Roles (Security Groups) -->
            <record id="group_dfr_super_admin" model="res.groups">
                <field name="name">DFR Super Administrator</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Platform-wide administrative functions, core codebase oversight.</field>
                <!-- Implied groups: Typically Super Admin implies admin rights -->
                <field name="implied_ids" eval="[(4, ref('base.group_system'))]"/> 
            </record>

            <record id="group_dfr_national_admin" model="res.groups">
                <field name="name">DFR National Administrator</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Country-wide administration, user management, configuration for a specific country instance.</field>
                <!-- National Admins might imply some lower-level DFR access or specific Odoo application access groups -->
                 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

            <record id="group_dfr_supervisor" model="res.groups">
                <field name="name">DFR Supervisor</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Supervises enumerators, reviews data, manages assignments within their scope.</field>
                 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

            <record id="group_dfr_enumerator" model="res.groups">
                <field name="name">DFR Enumerator</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Collects farmer data in the field using the mobile application.</field>
                 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

            <record id="group_dfr_farmer_portal_user" model="res.groups">
                <field name="name">DFR Farmer (Portal User)</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Access for farmers via the Farmer Self-Service Portal.</field>
                <field name="implied_ids" eval="[(4, ref('base.group_portal'))]"/> <!-- Implies Odoo portal user group -->
            </record>

            <record id="group_dfr_support_team" model="res.groups">
                <field name="name">DFR Support Team</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Provides technical assistance and troubleshooting.</field>
                 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

            <record id="group_dfr_it_team" model="res.groups">
                <field name="name">DFR IT Team</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">System maintenance, deployment, Odoo updates, data migration execution.</field>
                 <field name="implied_ids" eval="[(4, ref('base.group_system'))]"/> <!-- Typically IT team needs high system access -->
            </record>

            <record id="group_dfr_policy_analyst" model="res.groups">
                <field name="name">DFR Policy Maker/Analyst</field>
                <field name="category_id" ref="module_category_dfr"/>
                <field name="comment">Accesses aggregated data and analytics for decision-making.</field>
                 <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

        </data>
    </odoo>
    

### 3.5. `security/ir.model.access.csv`

*   **Path:** `dfr_addons/dfr_security_config/security/ir.model.access.csv`
*   **Description:** Defines model-level Access Control List (ACL) permissions (CRUD) for DFR models. Implements REQ-5-004 and parts of REQ-SADG-001.
*   **Purpose:** Specifies which roles can perform CRUD operations on DFR data entities.
*   **Content Structure:**
    csv
    id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
    
    # --- DFR Farmer Registry Models ---
    # Model: dfr_farmer_registry.farmer (Assuming model name in dfr_farmer_registry module is 'dfr.farmer')
    access_dfr_farmer_super_admin,dfr.farmer.super_admin,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_super_admin,1,1,1,1
    access_dfr_farmer_national_admin,dfr.farmer.national_admin,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_national_admin,1,1,1,1
    access_dfr_farmer_supervisor,dfr.farmer.supervisor,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_supervisor,1,1,1,0
    access_dfr_farmer_enumerator,dfr.farmer.enumerator,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_enumerator,1,1,1,0
    access_dfr_farmer_portal_user_read,dfr.farmer.portal_user.read,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_farmer_portal_user,1,0,0,0
    access_dfr_farmer_support_team_read,dfr.farmer.support.read,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_support_team,1,0,0,0
    access_dfr_farmer_policy_analyst_read,dfr.farmer.policy.read,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_policy_analyst,1,0,0,0
    access_dfr_farmer_it_team,dfr.farmer.it_team,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_it_team,1,1,1,1

    # Model: dfr_farmer_registry.household (Assuming model name 'dfr.household')
    access_dfr_household_super_admin,dfr.household.super_admin,model_dfr_farmer_registry_household,dfr_security_config.group_dfr_super_admin,1,1,1,1
    access_dfr_household_national_admin,dfr.household.national_admin,model_dfr_farmer_registry_household,dfr_security_config.group_dfr_national_admin,1,1,1,1
    access_dfr_household_supervisor,dfr.household.supervisor,model_dfr_farmer_registry_household,dfr_security_config.group_dfr_supervisor,1,1,1,0
    access_dfr_household_enumerator,dfr.household.enumerator,model_dfr_farmer_registry_household,dfr_security_config.group_dfr_enumerator,1,1,1,0
    # ... other roles for household

    # Model: dfr_farmer_registry.plot (Assuming model name 'dfr.plot')
    access_dfr_plot_super_admin,dfr.plot.super_admin,model_dfr_farmer_registry_plot,dfr_security_config.group_dfr_super_admin,1,1,1,1
    access_dfr_plot_national_admin,dfr.plot.national_admin,model_dfr_farmer_registry_plot,dfr_security_config.group_dfr_national_admin,1,1,1,1
    access_dfr_plot_supervisor,dfr.plot.supervisor,model_dfr_farmer_registry_plot,dfr_security_config.group_dfr_supervisor,1,1,1,0
    access_dfr_plot_enumerator,dfr.plot.enumerator,model_dfr_farmer_registry_plot,dfr_security_config.group_dfr_enumerator,1,1,1,0
    # ... other roles for plot

    # --- DFR Dynamic Forms Models ---
    # Model: dfr_dynamic_forms.form_template (Assuming model name 'dfr.form.template')
    access_dfr_form_template_super_admin,dfr.form_template.super_admin,model_dfr_dynamic_forms_form_template,dfr_security_config.group_dfr_super_admin,1,1,1,1
    access_dfr_form_template_national_admin,dfr.form_template.national_admin,model_dfr_dynamic_forms_form_template,dfr_security_config.group_dfr_national_admin,1,1,1,1
    access_dfr_form_template_supervisor_read,dfr.form_template.supervisor.read,model_dfr_dynamic_forms_form_template,dfr_security_config.group_dfr_supervisor,1,0,0,0
    access_dfr_form_template_enumerator_read,dfr.form_template.enumerator.read,model_dfr_dynamic_forms_form_template,dfr_security_config.group_dfr_enumerator,1,0,0,0
    # ... other roles for form_template

    # Model: dfr_dynamic_forms.form_submission (Assuming model name 'dfr.form.submission')
    access_dfr_form_submission_super_admin,dfr.form_submission.super_admin,model_dfr_dynamic_forms_form_submission,dfr_security_config.group_dfr_super_admin,1,1,1,1
    access_dfr_form_submission_national_admin,dfr.form_submission.national_admin,model_dfr_dynamic_forms_form_submission,dfr_security_config.group_dfr_national_admin,1,1,1,1
    access_dfr_form_submission_supervisor,dfr.form_submission.supervisor,model_dfr_dynamic_forms_form_submission,dfr_security_config.group_dfr_supervisor,1,1,0,0 
    access_dfr_form_submission_enumerator_rc,dfr.form_submission.enumerator.rc,model_dfr_dynamic_forms_form_submission,dfr_security_config.group_dfr_enumerator,1,0,1,0
    access_dfr_form_submission_farmer_portal_user_rc,dfr.form_submission.farmer_portal.rc,model_dfr_dynamic_forms_form_submission,dfr_security_config.group_dfr_farmer_portal_user,1,0,1,0 
    # ... other roles for form_submission

    # --- DFR Common Core Models (Example: Administrative Area if managed directly by DFR roles) ---
    # Model: dfr_common_core.administrative_area (Assuming model name 'dfr.administrative.area')
    # access_dfr_admin_area_national_admin,dfr.admin_area.national_admin,model_dfr_common_core_administrative_area,dfr_security_config.group_dfr_national_admin,1,1,1,1
    # access_dfr_admin_area_all_users_read,dfr.admin_area.all_users_read,model_dfr_common_core_administrative_area,base.group_user,1,0,0,0

    # --- Other DFR module models as they are defined ---
    # Example: Notification Templates if there's a model 'dfr.notification.template'
    # access_dfr_notification_template_national_admin,dfr.notification_template.national_admin,model_dfr_notification_template,dfr_security_config.group_dfr_national_admin,1,1,1,1

    # Note: Ensure `model_module_name_model_name_with_underscores` matches Odoo's convention for `ir.model`'s `model` field.
    # The `model_id/id` column should reference the XML ID of the `ir.model` record for the target model.
    # For example, for a model `dfr.farmer` in module `dfr_farmer_registry`, the `ir.model` XML ID is typically `model_dfr_farmer_registry_dfr_farmer`.
    # It is crucial that the `depends` in `__manifest__.py` includes all modules whose models are listed here.
    
    **Guidance for `ir.model.access.csv`:**
    *   The exact `model_id/id` values (e.g., `model_dfr_farmer_registry_farmer`) need to correspond to the `ir.model` records generated by Odoo for each model. These are typically `model_<module_name>_<model_name_with_underscores>`.
    *   This file needs to be comprehensive, covering all custom DFR models.
    *   Permissions should follow the principle of least privilege.

### 3.6. `security/dfr_record_rules.xml`

*   **Path:** `dfr_addons/dfr_security_config/security/dfr_record_rules.xml`
*   **Description:** Defines record-level security rules (`ir.rule`) for DFR models. Implements hierarchical access and data scoping as per REQ-SADG-001 and REQ-5-002.
*   **Purpose:** Restricts access to specific records based on user attributes or data context.
*   **Content Structure:**
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data>

            <!-- Record Rule: DFR National Admin - Country Scope -->
            <!-- This rule assumes each country instance uses a separate Odoo company. -->
            <!-- If not, an alternative like user.country_id would be needed on relevant models. -->
            <record id="rule_dfr_national_admin_country_scope_farmer" model="ir.rule">
                <field name="name">DFR National Admin: Country Scope (Farmer)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/> <!-- Adjust ref based on actual model XML ID -->
                <field name="domain_force">[('company_id','=',user.company_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_national_admin'))]"/>
                <field name="perm_read" eval="True"/>
                <field name="perm_write" eval="True"/>
                <field name="perm_create" eval="True"/>
                <field name="perm_unlink" eval="True"/>
            </record>
            <!-- Add similar country scope rules for National Admin for other key DFR models: -->
            <!-- dfr_farmer_registry.household, dfr_farmer_registry.plot, dfr_dynamic_forms.form_submission, etc. -->
             <record id="rule_dfr_national_admin_country_scope_household" model="ir.rule">
                <field name="name">DFR National Admin: Country Scope (Household)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_household"/>
                <field name="domain_force">[('company_id','=',user.company_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_national_admin'))]"/>
            </record>
             <record id="rule_dfr_national_admin_country_scope_plot" model="ir.rule">
                <field name="name">DFR National Admin: Country Scope (Plot)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_plot"/>
                <field name="domain_force">[('company_id','=',user.company_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_national_admin'))]"/>
            </record>
            <record id="rule_dfr_national_admin_country_scope_form_submission" model="ir.rule">
                <field name="name">DFR National Admin: Country Scope (Form Submission)</field>
                <field name="model_id" ref="dfr_dynamic_forms.model_dfr_form_submission"/>
                <field name="domain_force">[('company_id','=',user.company_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_national_admin'))]"/>
            </record>


            <!-- Record Rule: DFR Supervisor - Administrative Area Scope -->
            <!-- This rule assumes Supervisors have an 'administrative_area_ids' field on their user record (res.users) -->
            <!-- or that target models have a link to an administrative area manageable by the supervisor. -->
            <!-- This example assumes target models (e.g., farmer) have an 'administrative_area_id'. -->
            <record id="rule_dfr_supervisor_admin_area_scope_farmer" model="ir.rule">
                <field name="name">DFR Supervisor: Admin Area Scope (Farmer)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
                <!-- Example: user.dfr_supervisor_administrative_area_ids is a many2many field on res.users -->
                <field name="domain_force">['|', ('administrative_area_id', '=', False), ('administrative_area_id', 'child_of', user.dfr_supervisor_administrative_area_ids.ids)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_supervisor'))]"/>
            </record>
            <!-- Add similar admin area scope rules for Supervisor for other DFR models. -->


            <!-- Record Rule: DFR Enumerator - Assigned Administrative Area Scope -->
            <!-- This rule assumes Enumerators have an 'administrative_area_id' (many2one) field on their user record. -->
            <!-- And target models (e.g., farmer) also have an 'administrative_area_id'. -->
            <record id="rule_dfr_enumerator_assigned_area_scope_farmer" model="ir.rule">
                <field name="name">DFR Enumerator: Assigned Area Scope (Farmer)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
                <!-- Example: user.dfr_enumerator_administrative_area_id is a many2one field on res.users -->
                <field name="domain_force">['|', ('administrative_area_id', '=', False), ('administrative_area_id', '=', user.dfr_enumerator_administrative_area_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_enumerator'))]"/>
            </record>
            <!-- Add similar assigned area scope rules for Enumerator for other DFR models. -->

            <!-- Record Rule: Farmer Portal User - Own Data Access -->
            <!-- Example: Farmer can only see their own farmer record linked to their portal user. -->
            <!-- This assumes dfr.farmer has a 'user_id' field linking to res.users (portal user). -->
            <record id="rule_dfr_farmer_portal_user_own_farmer_record" model="ir.rule">
                <field name="name">DFR Farmer Portal User: Own Farmer Record</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
                <field name="domain_force">[('user_id','=',user.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_farmer_portal_user'))]"/>
                <field name="perm_read" eval="True"/>
                <field name="perm_write" eval="False"/> <!-- Typically portal users don't directly edit core data -->
                <field name="perm_create" eval="False"/>
                <field name="perm_unlink" eval="False"/>
            </record>
            <!-- Example: Farmer Portal User can see their own form submissions. -->
            <record id="rule_dfr_farmer_portal_user_own_submissions" model="ir.rule">
                <field name="name">DFR Farmer Portal User: Own Form Submissions</field>
                <field name="model_id" ref="dfr_dynamic_forms.model_dfr_form_submission"/>
                <!-- This assumes form_submission has a many2one to dfr.farmer, and dfr.farmer has user_id -->
                <field name="domain_force">[('farmer_id.user_id','=',user.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_farmer_portal_user'))]"/>
            </record>

            <!-- Policy Analyst: Read-only access, possibly to all data within their country context if using company_id for scoping -->
            <record id="rule_dfr_policy_analyst_country_scope_farmer_read" model="ir.rule">
                <field name="name">DFR Policy Analyst: Country Scope Read (Farmer)</field>
                <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer"/>
                <field name="domain_force">[('company_id','=',user.company_id.id)]</field>
                <field name="groups" eval="[(4, ref('dfr_security_config.group_dfr_policy_analyst'))]"/>
                <field name="perm_read" eval="True"/>
                <field name="perm_write" eval="False"/>
                <field name="perm_create" eval="False"/>
                <field name="perm_unlink" eval="False"/>
            </record>
            <!-- Add similar read-only country scope rules for Policy Analyst for other relevant DFR models -->


            <!-- Super Admin and IT Team typically bypass most restrictive record rules or have specific global "allow" rules. -->
            <!-- Odoo's group_system (often implied by Super Admin / IT Team) usually bypasses record rules by default, -->
            <!-- unless a rule explicitly includes them with a restrictive domain. -->
            <!-- If specific "see all data" rules are needed for them, they can be added, but often not required if they are system admins. -->

            <!-- Ensure model_id refs are correct (e.g., dfr_farmer_registry.model_dfr_farmer, dfr_dynamic_forms.model_dfr_form_template). -->
            <!-- Domain logic for supervisor/enumerator scope will depend on how users are linked to administrative areas or assignments in other DFR modules. -->
            <!-- Placeholders like `user.dfr_supervisor_administrative_area_ids` and `user.dfr_enumerator_administrative_area_id` indicate fields that would need to be added to `res.users` model (potentially in dfr_common_core or another module that extends users). -->

        </data>
    </odoo>
    
    **Guidance for `dfr_record_rules.xml`:**
    *   The `model_id` field must use the `ref` attribute to point to the XML ID of the `ir.model` record (e.g., `dfr_farmer_registry.model_dfr_farmer`).
    *   The `domain_force` expressions are critical and will define the actual row-level security.
    *   **Company-based Scoping:** The primary method for National Admin scoping is assumed to be Odoo's multi-company feature, where each country is a `res.company`. Models should then have a `company_id` field.
    *   **Hierarchical Scoping (Supervisor/Enumerator):** This often requires custom fields on `res.users` or related assignment models to link users to specific administrative units or teams. The domains in the rules will then reference these user-specific fields. The example domains for Supervisor and Enumerator assume such fields exist (e.g., `user.dfr_supervisor_administrative_area_ids`, `user.dfr_enumerator_administrative_area_id`). These fields would be defined in another module (e.g., `dfr_common_core` or a specific user extension module).
    *   Ensure that `perm_read`, `perm_write`, etc. are set correctly on rules. A rule only applies to the operations for which its permission flags are true.

## 4. Data Models

This module does not define new data models. It configures access to existing models defined in other DFR modules.

## 5. Business Logic

This module does not contain business logic in Python code. The "logic" is declarative, defined in the XML and CSV files that configure Odoo's security mechanisms.

## 6. User Interface (UI)

This module does not introduce new user interfaces. It impacts what users can see and do within existing Odoo interfaces based on their assigned roles and permissions.

## 7. API Design

This module does not expose any external APIs. Its configurations are loaded and enforced by the Odoo framework.

## 8. Integration Points

*   **Odoo Framework:** Deeply integrates with Odoo's security mechanisms (`res.groups`, `ir.model.access`, `ir.rule`).
*   **Other DFR Modules:** Depends on other DFR modules (e.g., `dfr_farmer_registry`, `dfr_dynamic_forms`) to know which models need to be secured. The `__manifest__.py` must list these as dependencies.

## 9. Non-Functional Requirements

*   **Security:** This module is central to enforcing security policies.
*   **Maintainability:** Configurations are declarative and separated, easing updates.
*   **Correctness:** Accuracy in defining ACLs and record rules is paramount.

## 10. Deployment Considerations

*   This module must be installed in each Odoo instance for DFR.
*   The order of installation is important; this module should generally be installed after the modules defining the data models it secures. Odoo's dependency system in `__manifest__.py` handles this.
*   User assignment to the defined DFR groups will be performed by administrators post-installation.

## 11. Future Considerations / Extensions

*   If more granular roles or more complex scoping rules are needed, this module would be updated.
*   Integration with potential future DFR modules would require adding ACLs and possibly record rules for their models.