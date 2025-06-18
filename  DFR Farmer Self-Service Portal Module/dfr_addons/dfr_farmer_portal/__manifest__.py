# -*- coding: utf-8 -*-
{
    'name': 'DFR Farmer Self-Service Portal',
    'version': '18.0.1.0.0',
    'summary': 'Public portal for farmer pre-registration and dynamic form access.',
    'author': 'FAO DFR Project Team',
    'website': 'https://www.fao.org',
    'license': 'MIT',
    'category': 'Website/Portal',
    'depends': [
        'website',
        'dfr_farmer_registry',
        'dfr_dynamic_forms',
    ],
    'data': [
        'views/assets.xml',
        'views/portal_layout.xml',
        'views/portal_preregistration_templates.xml',
        'views/portal_dynamic_form_templates.xml',
        'views/portal_info_page_template.xml',
        'views/snippets/country_branding_snippet.xml',
        # 'security/ir.model.access.csv', # If specific models are added by this module
        # 'security/security_rules.xml', # If portal-specific groups/rules are needed
    ],
    'assets': {
        'web.assets_frontend': [
            'dfr_farmer_portal/static/src/css/portal_main.css',
            'dfr_farmer_portal/static/src/css/portal_accessibility.css',
            'dfr_farmer_portal/static/src/js/portal_preregistration.js',
            'dfr_farmer_portal/static/src/js/portal_dynamic_form.js',
            'dfr_farmer_portal/static/src/js/portal_accessibility.js',
        ],
    },
    'installable': True,
    'application': False, # It's an addon extending website
    'auto_install': False,
}