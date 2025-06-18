# -*- coding: utf-8 -*-
{
    'name': "DFR Notification System",
    'version': '18.0.1.0.0',
    'category': 'DFR/Notifications',
    'summary': """
        Manages and dispatches automated notifications (SMS, email, push) 
        for the Digital Farmer Registry (DFR) system.
    """,
    'description': """
        This module provides the core functionality for the DFR Notification System.
        Key features include:
        - Management of notification templates (Email, SMS, Push).
        - Configuration of notification gateways.
        - Dispatching notifications based on system events and templates.
        - Logging of all notification attempts.
        - Integration with DFR External Integration Connectors for actual sending.
    """,
    'author': "DFR Development Team",
    'website': "https://www.example.com",  # Replace with actual website
    'depends': [
        'base',
        'mail',
        'dfr_core_common',  # Assuming dfr_core_common is the module name for DFR_MOD_CORE_COMMON
        'dfr_external_integration_connectors',  # Assuming dfr_external_integration_connectors is for DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS
    ],
    'data': [
        # Security
        'security/dfr_notifications_groups.xml',
        'security/ir.model.access.csv',
        # Data
        'data/dfr_notification_template_data.xml',
        'data/ir_actions_server_data.xml',
        # Views
        'views/dfr_notification_template_views.xml',
        'views/dfr_notification_gateway_config_views.xml',
        'views/dfr_notification_log_views.xml',
        'views/dfr_notifications_menus.xml',
    ],
    'installable': True,
    'application': True, # It has its own menu and configuration sections
    'auto_install': False,
    'license': 'OEEL-1', # Or AGPL-3 or other appropriate license
}