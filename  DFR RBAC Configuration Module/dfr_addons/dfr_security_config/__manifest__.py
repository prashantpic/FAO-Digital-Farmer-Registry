# -*- coding: utf-8 -*-
{
    'name': 'DFR RBAC Configuration',
    'version': '18.0.1.0.0',
    'summary': 'Security configurations including roles, ACLs, and record rules for the Digital Farmer Registry.',
    'description': """
This module defines DFR-specific user roles (Odoo groups), 
access control lists (ACLs - ir.model.access.csv), and 
record rules (ir.rule) for all DFR application modules.
It centralizes security definitions for the DFR platform.
    """,
    'category': 'DFR/Security', # Assumes 'DFR' is a top-level category defined elsewhere or this will create it.
    'author': 'FAO DFR Project Team',
    'website': 'https://www.fao.org', # Placeholder
    'license': 'MIT', # Or 'Apache-2.0' as per final project decision (REQ-CM-001)
    'depends': [
        'base',
        'dfr_common_core', # For any shared elements like module categories
        # Add all DFR modules whose models are secured by this module.
        # This ensures models are known to Odoo before ACLs/rules are applied.
        # Examples:
        'dfr_farmer_registry', 
        'dfr_dynamic_forms',
        # 'dfr_notifications_engine', # if models from here are secured
        # 'dfr_data_management_tools', # if models from here are secured
    ],
    'data': [
        'security/dfr_security_groups.xml',
        'security/ir.model.access.csv',
        'security/dfr_record_rules.xml',
    ],
    'installable': True,
    'application': False, # This is a configuration module, not a standalone application
    'auto_install': False,
}