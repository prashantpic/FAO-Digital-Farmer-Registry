# -*- coding: utf-8 -*-
{
    'name': 'DFR Data Management Toolkit',
    'version': '18.0.1.0.0',
    'summary': 'Provides tools for bulk data import/export and migration for DFR.',
    'author': 'DFR Project Team',
    'website': 'https://www.example.com', # To be updated
    'category': 'DigitalFarmerRegistry/Tools',
    'license': 'AGPL-3', # Or MIT/Apache 2.0 as per REQ-CM-001
    'depends': [
        'base',
        'web',
        'mail', # For activity tracking on import jobs
        'dfr_farmer_registry', # Dependency for target models
        'dfr_core_common', # For any shared utilities
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/dfr_data_tools_security.xml', # If custom groups are needed
        'views/dfr_data_tools_menus.xml',
        'views/bulk_data_import_wizard_views.xml',
        'views/data_import_job_views.xml',
        'views/data_import_job_log_views.xml',
        # 'controllers/main.py', # As per instruction to add, though unconventional for controller loading.
                               # Odoo usually discovers controllers automatically from subpackages.
                               # If this causes issues, it might need to be removed.
                               # For strict adherence to the generation plan, it's included.
    ],
    'assets': {
        'web.assets_backend': [
            'dfr_data_tools/static/src/js/import_progress_widget.js',
            'dfr_data_tools/static/src/xml/import_progress_templates.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}