# DFR Common Core Module (dfr_common) - Software Design Specification

## 1. Introduction

### 1.1 Purpose
This document provides the Software Design Specification (SDS) for the DFR Common Core Module (`dfr_common`). This module is a foundational Odoo 18.0 Community addon for the Digital Farmer Registry (DFR) platform. It provides shared utilities, base Odoo models and mixins, core configurations, implementations related to Digital Public Infrastructure (DPI) principles, and other foundational architectural elements. The primary purpose of `dfr_common` is to ensure consistency, reusability, and maintainability across all other DFR Odoo modules. It does not expose external APIs but offers internal services and definitions for other DFR modules.

### 1.2 Scope
The scope of this SDS is limited to the `dfr_common` Odoo module. This includes:
-   Module structure and manifest.
-   Base abstract models and mixins for UID generation and audit trails.
-   Common utility functions and constants.
-   Configuration settings specific to the DFR common core.
-   Security definitions for models within this module.
-   Data files for default configurations.
-   Internationalization setup.

### 1.3 Referenced Requirements
This module addresses the following requirements:
-   REQ-PCA-002: Unified, modular, reusable platform architecture.
-   REQ-PCA-003: Clear separation between core platform functionality and country-specific configurations.
-   REQ-PCA-008: Shared core Odoo codebase: structure, versioning, licensing.
-   REQ-PCA-011: Adherence to DPI principles.
-   REQ-PCA-016: Codebase designed for maintainability (modularity, documentation, coding standards, configuration separation).
-   REQ-FHR-002: Generation of unique farmer and household UIDs (via UID mixin).
-   REQ-FHR-010: Comprehensive audit trail (via audit mixin).
-   REQ-CM-001: Open-source licensing (MIT or Apache 2.0).
-   REQ-CM-004: Codebase governance framework (provides structure for configurations).
-   REQ-CM-013: Separation of configuration from code.

## 2. System Overview

### 2.1 Module Architecture
`dfr_common` is designed as a core library module within the DFR's modular monolith architecture. It sits at a foundational level, providing services and base components to other DFR-specific Odoo modules. It contributes to the `dfr_cross_cutting` and `dfr_odoo_domain_models` architectural layers.

Key components within this module:
-   **Models**: Abstract models and mixins (`DfrAbstractModel`, `DfrAuditMixin`, `DfrUidMixin`) for DFR entities, and configuration models (`DfrConfigSettings`).
-   **Utils**: Shared constants and utility functions.
-   **Security**: Access control for its own models.
-   **Data**: Default configuration parameters.
-   **Views**: UI for managing common configurations.

### 2.2 Key Features
-   Provision of a base abstract model for DFR entities.
-   Reusable mixin for unique DFR UID generation.
-   Reusable mixin for enhanced audit logging, leveraging Odoo's `mail.thread`.
-   Centralized management of DFR-common configuration settings.
-   Shared utility functions and constants.
-   Definition and display of DPI principles and licensing information within Odoo settings.
-   Implementation of the chosen open-source license (MIT or Apache 2.0).

## 3. Detailed Design

This section details the design for each file within the `dfr_common` module.

### 3.1 `dfr_common/__init__.py`
-   **Purpose**: Initializes the Python package for the `dfr_common` Odoo module.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import models
    from . import utils
    from . import security # Though security is often loaded via manifest, good to have if python logic is ever needed
    
-   **Relevant Requirements**: REQ-PCA-002

### 3.2 `dfr_common/__manifest__.py`
-   **Purpose**: Odoo module manifest file.
-   **Content**:
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'DFR Common Core',
        'version': '18.0.1.0.0', # Adheres to REQ-PCA-008 (Semantic Versioning)
        'summary': 'Provides shared utilities, base models, and core configurations for the DFR platform.',
        'description': """
    DFR Common Core Module
    ======================
    This module is the foundation for other DFR-specific Odoo modules.
    It includes:
    - Base abstract models and mixins for common DFR entity behaviors (UIDs, audit trails).
    - Shared utility functions and constants.
    - Core configuration settings and mechanisms.
    - Implementation of DPI principles information.
    - Adherence to open-source licensing (MIT or Apache-2.0).
        """,
        'author': 'FAO DFR Project Team',
        'website': 'https://www.fao.org/e-agriculture', # Placeholder
        'license': 'MIT',  # Or 'Apache-2.0', as per REQ-CM-001 and REQ-PCA-008
        'category': 'Digital Farmer Registry/Core',
        'depends': ['base', 'mail'], # 'mail' for mail.thread and mail.activity.mixin
        'data': [
            'security/ir.model.access.csv',
            'views/dfr_config_settings_views.xml',
            'data/dfr_config_parameters.xml',
        ],
        'installable': True,
        'application': False,
        'auto_install': False,
    }
    
-   **Relevant Requirements**: REQ-PCA-002, REQ-PCA-008, REQ-CM-001

### 3.3 `dfr_common/LICENSE`
-   **Purpose**: Contains the full text of the chosen open-source license.
-   **Content**: Verbatim text of the MIT License (or Apache License 2.0, if chosen).
    Example (MIT):
    
    MIT License

    Copyright (c) [Year] [Copyright Holder - e.g., Food and Agriculture Organization of the United Nations (FAO)]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
-   **Relevant Requirements**: REQ-PCA-008, REQ-CM-001

### 3.4 `dfr_common/models/__init__.py`
-   **Purpose**: Initializes the Python package for the `models` directory.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import dfr_uid_mixin
    from . import dfr_audit_mixin
    from . import dfr_abstract_model
    from . import dfr_config_settings
    
-   **Relevant Requirements**: REQ-PCA-002

### 3.5 `dfr_common/models/dfr_abstract_model.py`
-   **Purpose**: Defines a base abstract Odoo model for DFR entities.
-   **Class**: `DfrAbstractModel`
    python
    # -*- coding: utf-8 -*-
    from odoo import models, fields, api
    from odoo.tools.translate import _

    class DfrAbstractModel(models.AbstractModel):
        """
        Abstract base model for DFR entities.
        Inherits UID generation and audit trail capabilities.
        Provides a common foundation for DFR-specific models.
        """
        _name = 'dfr.abstract.model'
        _description = 'DFR Abstract Base Model'
        # Inherits from DfrUidMixin and DfrAuditMixin.
        # These mixins should be defined in this module and imported.
        _inherit = ['dfr.uid.mixin', 'dfr.audit.mixin']

        # Example of a common helper method if needed
        # def get_dfr_context_info(self):
        #     """ Returns common DFR context information. """
        #     self.ensure_one()
        #     # Example: could fetch country-specific context if this model is used in a country-specific way
        #     # For now, a placeholder or a common utility access.
        #     return {'dfr_module': self._name}

        # Add any other common fields or methods that should be part of all DFR models,
        # e.g., fields for managing record status, activity states, etc., if they are truly universal.
        # However, try to keep this abstract model lean and use mixins for distinct functionalities.
    
-   **Relevant Requirements**: REQ-PCA-002, REQ-PCA-016

### 3.6 `dfr_common/models/dfr_audit_mixin.py`
-   **Purpose**: Defines an Odoo model mixin for enhanced audit trails.
-   **Class**: `DfrAuditMixin`
    python
    # -*- coding: utf-8 -*-
    from odoo import models, fields, api
    from odoo.tools.translate import _

    class DfrAuditMixin(models.AbstractModel):
        """
        Mixin class to enhance audit trail capabilities for DFR models.
        Leverages Odoo's mail.thread for chatter and message logging.
        Can be extended with custom methods to log specific DFR auditable events.
        """
        _name = 'dfr.audit.mixin'
        _description = 'DFR Audit Trail Mixin'
        _inherit = ['mail.thread', 'mail.activity.mixin'] # Standard Odoo mixins for chatter and activities

        # Fields to track for changes automatically by mail.thread
        # This would be defined in the concrete models inheriting this mixin,
        # for example: _track = {'name': {}, 'status': {}}

        def log_dfr_specific_event(self, event_description, event_data=None):
            """
            Logs a DFR-specific event to the record's chatter.
            :param event_description: str, A human-readable description of the event.
            :param event_data: dict, Optional dictionary of key-value pairs for additional event details.
            """
            self.ensure_one()
            body = f"<p><strong>{_('DFR Event')}:</strong> {event_description}</p>"
            if event_data:
                body += "<ul>"
                for key, value in event_data.items():
                    body += f"<li><strong>{key}:</strong> {value}</li>"
                body += "</ul>"
            self.message_post(body=body)

        # Override write method if specific pre/post audit logic is needed beyond mail.thread
        # def write(self, vals):
        #     # Pre-write audit logic if needed
        #     res = super(DfrAuditMixin, self).write(vals)
        #     # Post-write audit logic, e.g., log specific changes
        #     return res

        # Override create method if specific post-creation audit logic is needed
        # @api.model_create_multi
        # def create(self, vals_list):
        #     records = super(DfrAuditMixin, self).create(vals_list)
        #     # Post-create audit logic for each record
        #     return records
    
-   **Relevant Requirements**: REQ-PCA-016, REQ-FHR-010

### 3.7 `dfr_common/models/dfr_uid_mixin.py`
-   **Purpose**: Defines an Odoo model mixin for DFR UID generation.
-   **Class**: `DfrUidMixin`
    python
    # -*- coding: utf-8 -*-
    import uuid
    from odoo import models, fields, api
    from odoo.tools.translate import _

    class DfrUidMixin(models.AbstractModel):
        """
        Mixin class for DFR models to automatically generate a unique DFR UID upon creation.
        Uses UUID v4 for generating UIDs to ensure global uniqueness.
        The 'dfr_uid' field should be unique per model that inherits this mixin.
        """
        _name = 'dfr.uid.mixin'
        _description = 'DFR Unique Identifier Mixin'

        dfr_uid = fields.Char(
            string='DFR UID',
            readonly=True,
            copy=False,
            index=True, # Important for search performance
            help="Unique Digital Farmer Registry Identifier for this record (UUID based)."
        )

        # SQL constraint to ensure uniqueness at the database level for inheriting models.
        # Note: The constraint name needs to be unique across the database or specific to the table.
        # Odoo usually handles this by prefixing with table name.
        # For an abstract mixin, this is illustrative; the concrete model would typically enforce it.
        # However, if we want to suggest a pattern:
        # _sql_constraints = [
        #    ('dfr_uid_uniq_on_model', 'unique (dfr_uid)', 'DFR UID must be unique for this record type!')
        # ]
        # This generic constraint name might clash if multiple models inherit it directly.
        # Odoo's ORM might handle this correctly by applying it to the inheriting model's table.
        # It's safer to define this in concrete models or ensure the ORM handles it.
        # For now, we rely on the `create` override to ensure uniqueness at generation.
        # A global unique index across all DFR UIDs if they were in one table is different.
        # Here, it's unique per model.

        @api.model_create_multi
        def create(self, vals_list):
            """
            Overrides create to generate a DFR UID if not provided.
            """
            for vals in vals_list:
                if 'dfr_uid' not in vals or not vals['dfr_uid']:
                    vals['dfr_uid'] = str(uuid.uuid4())
            return super(DfrUidMixin, self).create(vals_list)

        def name_get(self):
            """
            Appends DFR UID to the display name if available.
            This is a common pattern but might be too generic for a base mixin.
            Consider if this is desired for all models inheriting this.
            If not, this method should be in DfrAbstractModel or specific models.
            """
            res = []
            for record in self:
                name = super(DfrUidMixin, record).name_get()[0][1] # Get the original name
                if record.dfr_uid:
                    name = f"{name} [{record.dfr_uid}]"
                res.append((record.id, name))
            return res
    
    **Note on `_sql_constraints`**: For mixins, SQL constraints defined directly might not apply as expected or might cause issues. It's generally better to define them on the concrete models that inherit the mixin, ensuring the constraint name is unique or correctly scoped by Odoo to the model's table. The `index=True` on `dfr_uid` is important.
-   **Relevant Requirements**: REQ-PCA-016, REQ-FHR-002

### 3.8 `dfr_common/models/dfr_config_settings.py`
-   **Purpose**: Extends Odoo's base configuration wizard for DFR-common settings.
-   **Class**: `DfrConfigSettings`
    python
    # -*- coding: utf-8 -*-
    from odoo import models, fields, api
    from odoo.tools.translate import _
    from ..utils import constants # Assuming constants.py is in dfr_common/utils/

    class DfrConfigSettings(models.TransientModel):
        """
        Extends res.config.settings to manage DFR common configurations.
        Allows administrators to view DPI principles, license info, and set
        common parameters like the Codebase Governance Document URL.
        """
        _inherit = 'res.config.settings'

        # DPI Principles (Display Only)
        dfr_common_dpi_principles_info = fields.Text(
            string="DFR DPI Principles",
            readonly=True,
            compute='_compute_dfr_common_dpi_principles_info',
            help="Information about Digital Public Infrastructure (DPI) principles adhered to by the DFR platform."
        )

        # License Information (Display Only)
        dfr_common_platform_license = fields.Char(
            string="DFR Platform License",
            readonly=True,
            compute='_compute_dfr_common_platform_license',
            help="The primary open-source license under which the DFR platform is distributed."
        )

        # Configurable Parameters
        dfr_common_codebase_governance_url = fields.Char(
            string="Codebase Governance Document URL",
            config_parameter='dfr_common.governance_url', # Stored in ir.config_parameter
            help="URL to the DFR Codebase Governance Framework document."
        )

        # Example of another configurable setting
        dfr_common_example_setting = fields.Boolean(
            string="Enable DFR Common Example Feature",
            config_parameter='dfr_common.example_feature_enabled',
            help="An example boolean setting for the DFR common module."
        )

        @api.depends('dfr_common_codebase_governance_url') # Dummy dependency to trigger compute if needed
        def _compute_dfr_common_dpi_principles_info(self):
            for record in self:
                principles = [
                    f"<strong>{_('Openness')}</strong>: {constants.DPI_PRINCIPLE_OPENNESS}",
                    f"<strong>{_('Reusability')}</strong>: {constants.DPI_PRINCIPLE_REUSABILITY}",
                    f"<strong>{_('Inclusion')}</strong>: {constants.DPI_PRINCIPLE_INCLUSION}",
                    f"<strong>{_('Data Sovereignty')}</strong>: {constants.DPI_PRINCIPLE_DATA_SOVEREIGNTY}",
                ]
                record.dfr_common_dpi_principles_info = "<ul>" + "".join(f"<li>{p}</li>" for p in principles) + "</ul>"


        @api.depends('dfr_common_codebase_governance_url') # Dummy dependency
        def _compute_dfr_common_platform_license(self):
            for record in self:
                # Fetch from manifest or constants.py for consistency
                record.dfr_common_platform_license = constants.DEFAULT_LICENSE
    
-   **Relevant Requirements**: REQ-PCA-003, REQ-PCA-011, REQ-PCA-016, REQ-CM-001, REQ-CM-004, REQ-CM-013

### 3.9 `dfr_common/utils/__init__.py`
-   **Purpose**: Initializes the Python package for the `utils` directory.
-   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import constants
    from . import dfr_utils
    
-   **Relevant Requirements**: REQ-PCA-016

### 3.10 `dfr_common/utils/constants.py`
-   **Purpose**: Defines shared constants for the DFR platform.
-   **Content**:
    python
    # -*- coding: utf-8 -*-

    # DPI Principles (REQ-PCA-011)
    DPI_PRINCIPLE_OPENNESS = "Open Source, Open Standards, Open Data, Open Innovation"
    DPI_PRINCIPLE_REUSABILITY = "Modular design, Shared core codebase, Interoperable components"
    DPI_PRINCIPLE_INCLUSION = "Accessibility (WCAG), Multilingual support, User-centric design"
    DPI_PRINCIPLE_DATA_SOVEREIGNTY = "Country ownership of data, Data localization support, Secure data management"

    # Licensing (REQ-CM-001)
    # This should match the license chosen in __manifest__.py and LICENSE file
    DEFAULT_LICENSE_NAME = "MIT License"
    DEFAULT_LICENSE_SPDX = "MIT" # Or "Apache-2.0"

    # Example Common Statuses (Illustrative - specific statuses would be in respective modules)
    # STATUS_DRAFT = 'draft'
    # STATUS_ACTIVE = 'active'
    # STATUS_INACTIVE = 'inactive'

    # Default configuration parameter keys
    GOVERNANCE_URL_PARAM = 'dfr_common.governance_url'
    EXAMPLE_FEATURE_ENABLED_PARAM = 'dfr_common.example_feature_enabled'

    # Add other shared constants as needed
    
-   **Relevant Requirements**: REQ-PCA-011, REQ-PCA-016, REQ-CM-001

### 3.11 `dfr_common/utils/dfr_utils.py`
-   **Purpose**: Provides common utility functions.
-   **Content**:
    python
    # -*- coding: utf-8 -*-
    from odoo import api, SUPERUSER_ID
    from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
    from datetime import datetime

    def get_dfr_config_param(env, param_name, default_value=None):
        """
        Safely retrieves a DFR system configuration parameter.
        :param env: Odoo Environment
        :param param_name: str, key of the system parameter
        :param default_value: any, value to return if parameter not found
        :return: value of the system parameter or default_value
        """
        return env['ir.config_parameter'].sudo().get_param(param_name, default_value)

    def set_dfr_config_param(env, param_name, param_value):
        """
        Sets a DFR system configuration parameter.
        :param env: Odoo Environment
        :param param_name: str, key of the system parameter
        :param param_value: any, value to set for the parameter
        """
        env['ir.config_parameter'].sudo().set_param(param_name, param_value)

    def format_dfr_date(date_obj, date_format=None):
        """
        Consistently formats a date object for DFR display.
        :param date_obj: date or datetime object
        :param date_format: str, optional format string (e.g., '%Y-%m-%d')
        :return: str, formatted date string or empty string if date_obj is None
        """
        if not date_obj:
            return ""
        if date_format:
            return date_obj.strftime(date_format)
        # Default to Odoo's server date format or a DFR standard
        return date_obj.strftime(DEFAULT_SERVER_DATE_FORMAT) # Or a specific DFR format

    def format_dfr_datetime(datetime_obj, datetime_format=None):
        """
        Consistently formats a datetime object for DFR display.
        :param datetime_obj: datetime object
        :param datetime_format: str, optional format string (e.g., '%Y-%m-%d %H:%M:%S')
        :return: str, formatted datetime string or empty string if datetime_obj is None
        """
        if not datetime_obj:
            return ""
        if datetime_format:
            return datetime_obj.strftime(datetime_format)
        # Default to Odoo's server datetime format or a DFR standard
        return datetime_obj.strftime(DEFAULT_SERVER_DATETIME_FORMAT) # Or a specific DFR format

    # Add other utility functions as identified, e.g.:
    # - Data validation helpers (if generic enough)
    # - String manipulation utilities specific to DFR needs
    
-   **Relevant Requirements**: REQ-PCA-016, REQ-CM-013

### 3.12 `dfr_common/security/ir.model.access.csv`
-   **Purpose**: Defines model access rights for models in `dfr_common`.
-   **Content**:
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    # Access rights for res.config.settings are typically managed by Odoo's base module (e.g., group_system).
    # If specific DFR roles need to access *only* the DFR settings part,
    # it's complex as res.config.settings is a single model.
    # Usually, access to settings is granted to broader admin groups like 'base.group_system' or 'base.group_user' (for their own prefs).
    # If this module introduces new persistent models (not mixins or transient res.config.settings),
    # their ACLs would be defined here. For now, assuming no new persistent models in dfr_common.

    # Example: If dfr_common had a model 'dfr.common.log_entry'
    # access_dfr_common_log_entry_admin,dfr.common.log_entry.admin,model_dfr_common_log_entry,base.group_system,1,1,1,1
    # access_dfr_common_log_entry_user,dfr.common.log_entry.user,model_dfr_common_log_entry,base.group_user,1,0,0,0
    
    **Note**: Since `dfr_config_settings.py` inherits `res.config.settings` (a `TransientModel`), specific ACLs for it are usually not defined here unless overriding existing ones. Access to "Settings" menu is controlled by groups like `base.group_system`. The fields added via inheritance will be visible to users who can access the settings model.
-   **Relevant Requirements**: REQ-PCA-016

### 3.13 `dfr_common/data/dfr_config_parameters.xml`
-   **Purpose**: Defines default values for `ir.config_parameter`.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent overriding on module update unless specified -->

            <record id="dfr_common_default_governance_url" model="ir.config_parameter">
                <field name="key">dfr_common.governance_url</field>
                <field name="value">#To_Be_Defined_Post_Setup</field>
            </record>

            <record id="dfr_common_default_example_feature_enabled" model="ir.config_parameter">
                <field name="key">dfr_common.example_feature_enabled</field>
                <field name="value">False</field> <!-- Default to False or True as appropriate -->
            </record>

        </data>
    </odoo>
    
-   **Relevant Requirements**: REQ-CM-013, REQ-PCA-003

### 3.14 `dfr_common/views/dfr_config_settings_views.xml`
-   **Purpose**: Odoo XML views for the DFR-common configuration settings interface.
-   **Content**:
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data>
            <record id="dfr_common_config_settings_view_form" model="ir.ui.view">
                <field name="name">dfr.common.config.settings.view.form</field>
                <field name="model">res.config.settings</field>
                <field name="inherit_id" ref="base.res_config_settings_view_form"/> <!-- Inherit base settings view -->
                <field name="arch" type="xml">
                    <xpath expr="//div[hasclass('settings')]" position="inside">
                        <div class="app_settings_block" data-string="DFR Common Core" string="DFR Common Core" data-key="dfr_common" groups="base.group_system">
                            <h2>DFR Common Platform Settings</h2>
                            <div class="row mt16 o_settings_container">
                                <div class="col-12 col-lg-6 o_setting_box">
                                    <div class="o_setting_left_pane">
                                        <!-- Example Boolean Setting -->
                                        <field name="dfr_common_example_setting"/>
                                    </div>
                                    <div class="o_setting_right_pane">
                                        <label for="dfr_common_example_setting"/>
                                        <div class="text-muted">
                                            Enable or disable the DFR common example feature.
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-lg-6 o_setting_box">
                                    <div class="o_setting_left_pane"/>
                                    <div class="o_setting_right_pane">
                                        <label for="dfr_common_codebase_governance_url"/>
                                        <div class="text-muted">
                                            Provide the URL to the official DFR Codebase Governance Framework document.
                                        </div>
                                        <div class="content-group">
                                            <div class="mt16">
                                                <field name="dfr_common_codebase_governance_url" class="oe_input" placeholder="e.g., https://example.com/dfr_governance.pdf"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <h2>DFR Platform Information</h2>
                             <div class="row mt16 o_settings_container">
                                <div class="col-12 col-lg-6 o_setting_box">
                                    <div class="o_setting_left_pane"/>
                                    <div class="o_setting_right_pane">
                                        <span class="o_form_label">DFR Platform License</span>
                                        <div class="text-muted">
                                            The DFR platform is distributed under the following open-source license:
                                        </div>
                                        <div class="content-group">
                                            <div class="mt16">
                                                <field name="dfr_common_platform_license" readonly="1"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-lg-6 o_setting_box">
                                     <div class="o_setting_left_pane"/>
                                     <div class="o_setting_right_pane">
                                        <span class="o_form_label">DFR DPI Principles</span>
                                        <div class="text-muted">
                                            The DFR platform adheres to the following Digital Public Infrastructure (DPI) principles:
                                        </div>
                                        <div class="content-group">
                                            <div class="mt16">
                                                <!-- This field uses HTML, so needs to be rendered carefully -->
                                                <field name="dfr_common_dpi_principles_info" widget="html" readonly="1"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </xpath>
                </field>
            </record>

            <!-- Action to open DFR Common settings -->
            <record id="dfr_common_config_settings_action" model="ir.actions.act_window">
                <field name="name">DFR Common Settings</field>
                <field name="type">ir.actions.act_window</field>
                <field name="res_model">res.config.settings</field>
                <field name="view_mode">form</field>
                <field name="target">inline</field>
                <field name="context">{'module' : 'dfr_common', 'bin_size': False}</field>
            </record>

            <!-- Menu item for DFR Common settings -->
            <!-- This could be under a main "DFR" settings menu if one is created by another module -->
            <menuitem id="menu_dfr_common_settings"
                      name="DFR Common"
                      parent="base.menu_administration" <!-- Or a more specific DFR parent menu -->
                      sequence="50"
                      action="dfr_common_config_settings_action"
                      groups="base.group_system"/>
        </data>
    </odoo>
    
-   **Relevant Requirements**: REQ-CM-013, REQ-PCA-016, REQ-PCA-011

### 3.15 `dfr_common/i18n/dfr_common.pot`
-   **Purpose**: Translation template file for translatable strings.
-   **Content**: This file will be automatically generated by Odoo's `makepot` tool or can be manually created by extracting all translatable strings (e.g., `_("My String")` in Python, `string="My String"` in XML) from the module. It will contain `msgid` entries for each string and empty `msgstr ""` lines.
    Example structure:
    pot
    # Translation of DFR Common Core (dfr_common)
    # This file contains the translation of the DFR Common Core module.
    #
    msgid ""
    msgstr ""
    "Project-Id-Version: DFR Common Core 18.0\n"
    "POT-Creation-Date: YYYY-MM-DD HH:MM+ZZZZ\n"
    "PO-Revision-Date: YYYY-MM-DD HH:MM+ZZZZ\n"
    "Last-Translator: \n"
    "Language-Team: \n"
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: \n"
    "Generated-By: Odoo\n"

    #. module: dfr_common
    #: model:ir.model.fields,field_description:dfr_common.field_res_config_settings__dfr_common_codebase_governance_url
    msgid "Codebase Governance Document URL"
    msgstr ""

    #. module: dfr_common
    #: model:ir.model.fields,field_description:dfr_common.field_res_config_settings__dfr_common_platform_license
    msgid "DFR Platform License"
    msgstr ""

    # ... other translatable strings ...
    
-   **Relevant Requirements**: REQ-PCA-016

### 3.16 `dfr_common/static/description/icon.png`
-   **Purpose**: Standard Odoo module icon.
-   **Content**: A PNG image file, typically 96x96 pixels. The icon should be visually representative of a "common" or "core" DFR component.
-   **Relevant Requirements**: REQ-PCA-002

## 4. Data Design
-   Configuration data is stored in Odoo's `ir.config_parameter` model, managed via the `dfr_config_settings.py` model and views. Default values are loaded from `data/dfr_config_parameters.xml`.
-   The UID mixin (`dfr_uid_mixin.py`) adds a `dfr_uid` field to inheriting models. This field should be indexed on those models for performance.

## 5. Security Considerations
-   Access to DFR Common configuration settings (`res.config.settings` view extension) is typically restricted to users in the `base.group_system` (Administrators) group. This is managed by the `groups` attribute on the menu item and potentially on the view elements if finer control is needed.
-   No new persistent models are introduced directly by `dfr_common` that would require extensive custom ACLs in `ir.model.access.csv`, other than ensuring appropriate groups can access `res.config.settings`. Mixins inherit the security of their host models.

## 6. Configuration Management
-   Configuration parameters are managed via `res.config.settings` interface.
-   Parameters are stored in `ir.config_parameter`.
-   Default values are loaded via XML data files.
-   Utility functions in `dfr_utils.py` provide programmatic access to these configurations.
-   This approach fulfills REQ-CM-013 (Configuration separation from code) and REQ-PCA-003 (Separation of core and country-specific configuration, as these parameters can be set per database/country instance).

## 7. Internationalization (i18n)
-   All user-facing strings in Python code (model descriptions, field strings, messages) and XML views (labels, help texts) will use Odoo's translation mechanism (e.g., `_("Translatable String")` in Python, `string="Translatable String"` in XML).
-   A `.pot` file (`dfr_common/i18n/dfr_common.pot`) will be generated to serve as the template for translations into other languages.

## 8. Licensing
-   The module will be licensed under the MIT License or Apache 2.0 License, as finalized for the project.
-   The `__manifest__.py` file will declare the chosen license.
-   The `LICENSE` file will contain the full text of the chosen license.
-   Any third-party libraries used directly by this module (currently none specified beyond Odoo's own dependencies) would need to be compatible with the chosen license and listed in a project-wide open-source use declaration.

## 9. Module README (`dfr_common/README.md`)
-   **Purpose**: To provide an overview of the `dfr_common` module, its purpose, key features, and basic usage instructions for developers integrating with or extending it.
-   **Content Outline**:
    1.  **DFR Common Core Module (`dfr_common`)**
        *   Brief description (from manifest).
    2.  **Purpose**
        *   Explain its role as a foundational module.
    3.  **Key Features**
        *   `DfrAbstractModel`: Base model for DFR entities.
        *   `DfrUidMixin`: For unique DFR UID generation.
        *   `DfrAuditMixin`: For enhanced audit trails using `mail.thread`.
        *   `DfrConfigSettings`: For managing common DFR configurations.
        *   Shared utilities and constants.
    4.  **Installation**
        *   Standard Odoo module installation (dependency of other DFR modules).
    5.  **Configuration**
        *   How to access common settings (Settings > DFR Common).
        *   Key configurable parameters (e.g., Governance URL).
    6.  **Usage for Developers**
        *   How to inherit from `DfrAbstractModel`.
        *   How to use `DfrUidMixin` and `DfrAuditMixin`.
        *   How to access shared utilities from `dfr_common.utils`.
    7.  **Models Overview**
        *   Brief description of each key model/mixin.
    8.  **License**
        *   State the license (MIT or Apache 2.0).
    9.  **Contributing**
        *   (If applicable) Link to general project contribution guidelines.
-   **Relevant Requirements**: REQ-PCA-016 (well-documented)