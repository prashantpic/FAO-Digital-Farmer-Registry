{
    'name': 'DFR API Services (Gateway)',
    'version': '18.0.1.0.0',
    'summary': 'Provides RESTful API endpoints for the Digital Farmer Registry.',
    'description': """
        Central Odoo module acting as an API Gateway, exposing secure RESTful API endpoints
        for the mobile enumerator application and authorized external systems. Handles
        request routing, authentication (OAuth2/JWT), authorization, and data
        serialization (JSON).
    """,
    'category': 'DFR/Services',
    'author': 'FAO DFR Project Team',
    'website': 'https://www.fao.org', # Placeholder
    'license': 'Apache-2.0', # Or MIT, as per project decision REQ-CM-001
    'depends': [
        'base',
        'web',
        # DFR Core Modules - actual names to be confirmed
        'dfr_common', # Assuming a common module exists
        'dfr_farmer_registry',
        'dfr_dynamic_forms',
        'dfr_rbac_config', # For role definitions used in authorization
        'dfr_security_audit_log', # For logging API actions
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter_data.xml',
        'views/swagger_ui_template.xml', # If QWeb template is used for Swagger UI
        # Add other XML data files if any (e.g., for API client configuration models)
    ],
    'assets': {
        # Potentially, if Swagger UI assets are self-hosted
        # 'web.assets_backend': [
        #     'dfr_api_services/static/src/js/...',
        # ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}