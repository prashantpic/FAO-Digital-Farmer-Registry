# -*- coding: utf-8 -*-
{
    'name': "DFR Localization Pack",
    'version': '18.0.1.0.0',
    'summary': "Provides translations for all Digital Farmer Registry (DFR) custom modules.",
    'description': """
This module centralizes localization assets for the DFR platform,
including .po files for multiple languages. It depends on all other
DFR modules to ensure comprehensive translation coverage.
    """,
    'author': "FAO & SSS-AI",
    'license': 'MIT', # Or 'Apache-2.0'
    'category': 'Localization',
    'depends': [
        'base',
        # --- DFR Core Modules ---
        'dfr_common_core', # Placeholder - replace with actual DFR module name
        # --- DFR Functional Modules ---
        'dfr_farmer_registry', # Placeholder
        'dfr_dynamic_forms', # Placeholder
        'dfr_notifications_module', # Placeholder
        'dfr_api_management', # Placeholder
        'dfr_admin_tools', # Placeholder
        'dfr_self_service_portal', # Placeholder
        # ... Add ALL other custom DFR Odoo modules here
    ],
    'data': [
        # Typically empty for a pure localization module if .po files are in i18n/
        # and no specific views/data are defined by this module itself.
    ],
    'installable': True,
    'application': False,
    'auto_install': False, # Or True, depending on desired behavior
}