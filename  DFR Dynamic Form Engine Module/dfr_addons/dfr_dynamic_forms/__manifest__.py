# -*- coding: utf-8 -*-
{
    'name': "DFR Dynamic Form Engine",
    'summary': """
        Module for creating and managing dynamic data collection forms.
    """,
    'description': """
        The DFR Dynamic Form Engine Module enables administrators to design, manage, 
        and version custom data collection forms. It handles form submissions from 
        various clients (mobile, portal, admin) and links them to farmer profiles. 
        The module supports various field types, validation rules, and conditional 
        logic for displaying fields.
    """,
    'author': "FAO",
    'website': "https://www.fao.org",
    'category': "Digital Farmer Registry/Application",
    'version': "18.0.1.0.0",
    'license': "MIT",  # Or 'Apache-2.0' as per project decision
    'depends': [
        'base',
        'mail',
        'dfr_common',
        'dfr_farmer_registry',
        'dfr_rbac_config',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/dfr_dynamic_forms_security.xml',
        'data/ir_sequence_data.xml',
        # 'data/dfr_form_field_types_data.xml', # As per SDS, likely minimal or merged
        'views/dfr_form_views.xml',
        'views/dfr_form_submission_views.xml',
        'views/form_version_wizard_views.xml',
        'views/dfr_dynamic_forms_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dfr_dynamic_forms/static/src/scss/form_builder.scss',
            'dfr_dynamic_forms/static/src/js/form_builder_widget.js',
            'dfr_dynamic_forms/static/src/xml/form_builder_templates.xml',
        ],
    },
    'installable': True,
    'application': False, # It's a module providing features, not a standalone Odoo App
    'auto_install': False,
}