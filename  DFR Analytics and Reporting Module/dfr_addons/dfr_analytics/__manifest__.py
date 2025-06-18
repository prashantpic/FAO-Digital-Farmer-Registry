# dfr_addons/dfr_analytics/__manifest__.py
{
    'name': 'DFR Analytics and Reporting',
    'version': '18.0.1.0.0',
    'summary': 'Provides dashboards, KPIs, map visualizations, and exportable reports for the DFR system.',
    'author': 'FAO DFR Project Team',
    'website': 'https://www.fao.org', # Replace with actual project website
    'category': 'DigitalFarmerRegistry/Reporting',
    'license': 'MIT', # Or Apache 2.0 as per final decision
    'depends': [
        'web',
        'board', # Odoo dashboard module
        'dfr_common', # Assuming a common core module
        'dfr_farmer_registry',
        'dfr_dynamic_forms',
        'dfr_rbac_config',
        # Add 'web_map' or 'web_google_maps' if decided to use instead of custom Leaflet
    ],
    'external_dependencies': {
        'python': ['openpyxl'], # Required for XLSX export
    },
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/analytics_dashboard_views.xml',
        'views/map_visualization_views.xml',
        'views/report_actions_views.xml',
        'wizards/report_export_wizard_views.xml',
        'report/report_templates.xml',
        # Add menu entries XML files if separate, otherwise they are in views
    ],
    'assets': {
        'web.assets_backend': [
            'dfr_analytics/static/src/scss/analytics_styles.scss',
            # Leaflet.js library files (assuming bundled directly)
            'dfr_analytics/static/lib/leaflet/leaflet.css',
            'dfr_analytics/static/lib/leaflet/leaflet.js',
            # Custom JS components
            'dfr_analytics/static/src/js/kpi_widget.js',
            'dfr_analytics/static/src/js/chart_widget.js',
            'dfr_analytics/static/src/js/map_view_component.js',
            'dfr_analytics/static/src/js/dashboard_manager.js',
            # OWL templates
            'dfr_analytics/static/src/xml/dashboard_templates.xml',
            'dfr_analytics/static/src/xml/map_view_templates.xml',
        ],
    },
    'installable': True,
    'application': False, # This is an addon, not a standalone application
    'auto_install': False,
}