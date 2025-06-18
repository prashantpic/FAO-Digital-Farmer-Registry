# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'DFR Farmer Registry',
    'version': '18.0.1.0.0',
    'summary': 'Core module for managing farmer, household, farm, and plot data in the Digital Farmer Registry.',
    'description': """
        This module manages the foundational data for the Digital Farmer Registry (DFR),
        including farmer profiles, households, farms, and land plots.
        It implements key functionalities like unique identifier generation,
        status workflows, KYC process, consent management, and de-duplication.
    """,
    'author': 'FAO & SSS-IT',
    'website': 'https://www.fao.org', # Or project specific
    'category': 'DigitalFarmerRegistry/Core',
    'license': 'AGPL-3', # Or MIT/Apache 2.0 as per final decision
    'depends': [
        'base',
        'mail', # For mail.thread and mail.activity.mixin
        'uom', # For plot size unit of measure
        'dfr_common_core', # Assuming shared utilities, base models, and common lookups
        # 'dfr_rbac_config', # If RBAC groups are defined in a separate module
        # 'dfr_audit_log', # If enhanced audit logging is a separate module
        # 'gis', # If OCA GIS module is used for map widgets/spatial data types
    ],
    'data': [
        'security/ir.model.access.csv',
        # Define supporting models if they reside in this module
        'data/dfr_national_id_type_data.xml', # Assumes dfr.national.id.type model defined in models/
        # 'data/dfr_consent_purpose_data.xml', # If dfr.consent.purpose is defined here (and its model)
        # 'data/dfr_relationship_type_data.xml', # If defined here (and its model)
        # 'data/dfr_land_tenure_type_data.xml', # If defined here (and its model)
        # 'data/dfr_crop_livestock_type_data.xml', # If defined here (and its model)

        'data/dfr_sequences.xml', # If using sequences (optional if UUIDs are primary)
        'data/dfr_automated_actions.xml', # Automated workflows

        'views/dfr_farmer_views.xml',
        'views/dfr_household_views.xml',
        'views/dfr_farm_views.xml',
        'views/dfr_plot_views.xml',
        'views/dfr_menu_views.xml',

        'wizards/dfr_deduplication_review_wizard_views.xml',
        'wizards/dfr_farmer_kyc_wizard_views.xml',

        # Add views for supporting models if created in this module and menu items exist
        # 'views/dfr_national_id_type_views.xml',
        # 'views/dfr_consent_purpose_views.xml',
    ],
    'demo': [
        # 'demo/dfr_farmer_demo.xml', # Optional: Sample data
    ],
    'installable': True,
    'application': False, # It's a core module, not a standalone app
    'auto_install': False,
}