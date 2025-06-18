{
    'name': 'DFR Audit Logging Enhancements',
    'version': '18.0.1.0.0',
    'summary': 'Enhances DFR auditing with detailed logging and viewing capabilities.',
    'description': """
        This module provides comprehensive audit logging for the Digital Farmer Registry (DFR) platform.
        It includes:
        - A dedicated model to store audit logs (dfr.audit.log).
        - Services for other modules to record auditable events.
        - UI for administrators to view and filter audit logs.
        - Enhanced logging for specific events like login attempts.
    """,
    'author': 'SSS-AI (FAO Project)',
    'website': 'https://www.fao.org', # Placeholder
    'category': 'DFR/Administration',
    'depends': [
        'base',
        'mail',
        'dfr_common_core', # DFR_MOD_CORE_COMMON
        'dfr_rbac_config', # DFR_MOD_RBAC_CONFIG
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/dfr_audit_log_security.xml',
        'data/dfr_audit_log_data.xml', # Sequence definition
        'views/dfr_audit_log_views.xml',
        'views/dfr_audit_log_menus.xml',
    ],
    'installable': True,
    'application': False, # It's a supporting module, not a standalone application
    'auto_install': False,
    'license': 'MIT', # Or Apache 2.0 as per REQ-CM-001
}