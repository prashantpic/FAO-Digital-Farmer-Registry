{
    'name': 'DFR - External Integration Connectors',
    'version': '18.0.1.0.0',
    'summary': 'Module for connecting to various third-party external APIs.',
    'author': 'FAO DFR Project Team',
    'license': 'MIT',
    'category': 'DigitalFarmerRegistry/Integrations',
    'depends': [
        'base',
        'mail',
        'dfr_common', 
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}