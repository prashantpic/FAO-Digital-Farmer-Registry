# -*- coding: utf-8 -*-
from odoo import fields, models, _

class DfrNotificationGatewayConfig(models.Model):
    _name = 'dfr.notification.gateway.config'
    _description = 'DFR Notification Gateway Configuration'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help="User-friendly name for the gateway configuration (e.g., 'Country X Primary SMS Gateway')."
    )
    channel_type = fields.Selection(
        [('email', 'Email'),
         ('sms', 'SMS'),
         ('push', 'Push Notification')],
        string='Channel Type',
        required=True,
        help="Type of notification channel this gateway serves."
    )
    provider_name = fields.Char(
        string='Provider Name',
        help="Name of the gateway provider (e.g., 'Twilio', 'SendGrid', 'FCM', 'Odoo Default Email')."
    )
    api_key = fields.Char(
        string='API Key',
        password=True,
        help="API key for the gateway."
    )
    api_secret = fields.Char(
        string='API Secret/Token',
        password=True,
        help="API secret or token for the gateway."
    )
    base_url = fields.Char(
        string='Base URL',
        help="Base URL for the gateway's API (if applicable)."
    )
    sender_id = fields.Char(
        string='Sender ID',
        help="Sender ID for SMS or From Email for email notifications."
    )
    email_from = fields.Char(
        string='"From" Email Address',
        help="'From' email address for email notifications sent through this gateway."
    )
    is_odoo_default_email = fields.Boolean(
        string='Use Odoo Default Email Server',
        default=False,
        help="If True, this configuration represents using Odoo's built-in email sending capabilities. "
             "Other credential fields might be ignored."
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this gateway configuration is active."
    )

    _sql_constraints = [
        ('name_channel_uniq', 'unique(name, channel_type)', 'A gateway configuration name must be unique per channel type.')
    ]