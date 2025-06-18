# -*- coding: utf-8 -*-
{
    'name': "DFR Odoo Admin Portal Master UI",
    'summary': """
        Master UI coordinator for the Digital Farmer Registry (DFR) Admin Portal.
        Aggregates UI elements from various DFR backend modules.
    """,
    'description': """
        This module acts as a meta-module or a top-level addon that declares
        dependencies on all functional DFR backend modules, thereby pulling them
        into a single, deployable administrative interface. It ensures that all
        administrative functionalities are presented consistently within the Odoo backend.
        It defines the main DFR application menu structure and provides global
        styling for a unified look and feel.
    """,
    'author': "FAO & SSS-IT",
    'website': "https://www.fao.org", # Replace with actual project website if available
    'category': 'Digital Farmer Registry/Admin Portal',
    'version': '18.0.1.0.0', # Aligns with Odoo 18.0, Semantic Versioning
    'license': 'MIT', # Or 'Apache-2.0' as per final decision REQ-CM-001

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
        'web_responsive', # Recommended for better backend UI responsiveness
        # Core DFR Dependencies (module names as defined in their respective repos)
        'dfr_common', # REPO-CORE-COMMON (DFR_MOD_CORE_COMMON)
        'dfr_farmer_registry', # REPO-02-FARMREG (DFR_MOD_FARMER_REGISTRY)
        'dfr_dynamic_forms', # REPO-03-DYNFORM (DFR_MOD_DYNAMIC_FORMS)
        'dfr_rbac_config', # REPO-04-RBAC (DFR_MOD_RBAC_CONFIG)
        'dfr_admin_settings', # REPO-05-ADMINSET (DFR_MOD_ADMIN_SETTINGS)
        'dfr_analytics_dashboards', # REPO-06-ANALYTICS (DFR_MOD_ANALYTICS_DASHBOARDS)
        'dfr_notifications_engine', # REPO-07-NOTIF (DFR_MOD_NOTIFICATIONS_ENGINE)
        'dfr_rest_api_config_ui', # REPO-08-APICFGUI (DFR_MOD_REST_API_CONFIG_UI) - if it has backend UI
        'dfr_external_connectors_config_ui', # REPO-09-EXTCONUI (DFR_MOD_EXTERNAL_CONNECTORS_CONFIG_UI) - if it has backend UI
        'dfr_data_management_tools', # REPO-10-DATAMGT (DFR_MOD_DATA_MANAGEMENT_TOOLS)
        'dfr_localization_pack_admin_ui', # REPO-11-LOCALUI (DFR_MOD_LOCALIZATION_PACK_ADMIN_UI)
        'dfr_security_audit_log_ui', # REPO-12-AUDITUI (DFR_MOD_SECURITY_AUDIT_LOG_UI)
        # 'dfr_business_process_orchestrator_ui', # REPO-13-BPMUI (DFR_BUSINESS_PROCESS_ORCHESTRATOR_UI) - if it has backend UI elements to include
    ],

    # always loaded
    'data': [
        'security/dfr_portal_security.xml',
        'security/ir.model.access.csv',
        'views/dfr_main_menus.xml',
        'views/dfr_master_actions.xml',
        'views/dfr_master_dashboard_view.xml', # Optional, if a master dashboard is designed
    ],

    'assets': {
        'web.assets_backend': [
            'dfr_admin_portal_master/static/src/css/dfr_portal_master_theme.css',
            'dfr_admin_portal_master/static/src/js/dfr_portal_master_widgets.js',
            'dfr_admin_portal_master/static/src/xml/dfr_portal_master_templates.owl.xml', # For OWL components
        ],
    },

    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': True, # Makes it appear as a main application in Odoo
    'auto_install': False,
}