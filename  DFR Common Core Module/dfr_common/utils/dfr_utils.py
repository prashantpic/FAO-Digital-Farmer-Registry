# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

def get_dfr_config_param(env, param_name, default_value=None):
    """
    Safely retrieves a DFR system configuration parameter.
    :param env: Odoo Environment
    :param param_name: str, key of the system parameter
    :param default_value: any, value to return if parameter not found
    :return: value of the system parameter or default_value
    """
    return env['ir.config_parameter'].sudo().get_param(param_name, default_value)

def set_dfr_config_param(env, param_name, param_value):
    """
    Sets a DFR system configuration parameter.
    :param env: Odoo Environment
    :param param_name: str, key of the system parameter
    :param param_value: any, value to set for the parameter
    """
    env['ir.config_parameter'].sudo().set_param(param_name, param_value)

def format_dfr_date(date_obj, date_format=None):
    """
    Consistently formats a date object for DFR display.
    :param date_obj: date or datetime object
    :param date_format: str, optional format string (e.g., '%Y-%m-%d')
    :return: str, formatted date string or empty string if date_obj is None
    """
    if not date_obj:
        return ""
    if date_format:
        return date_obj.strftime(date_format)
    # Default to Odoo's server date format or a DFR standard
    return date_obj.strftime(DEFAULT_SERVER_DATE_FORMAT) # Or a specific DFR format

def format_dfr_datetime(datetime_obj, datetime_format=None):
    """
    Consistently formats a datetime object for DFR display.
    :param datetime_obj: datetime object
    :param datetime_format: str, optional format string (e.g., '%Y-%m-%d %H:%M:%S')
    :return: str, formatted datetime string or empty string if datetime_obj is None
    """
    if not datetime_obj:
        return ""
    if datetime_format:
        return datetime_obj.strftime(datetime_format)
    # Default to Odoo's server datetime format or a DFR standard
    return datetime_obj.strftime(DEFAULT_SERVER_DATETIME_FORMAT) # Or a specific DFR format

# Add other utility functions as identified, e.g.:
# - Data validation helpers (if generic enough)
# - String manipulation utilities specific to DFR needs