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