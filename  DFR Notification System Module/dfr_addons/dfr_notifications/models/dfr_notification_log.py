# -*- coding: utf-8 -*-
from odoo import fields, models, _

class DfrNotificationLog(models.Model):
    _name = 'dfr.notification.log'
    _description = 'DFR Notification Log'
    _order = 'dispatch_timestamp desc'

    template_id = fields.Many2one(
        'dfr.notification.template',
        string='Template Used',
        ondelete='set null'
    )
    recipient_partner_id = fields.Many2one(
        'res.partner',
        string='Recipient Partner',
        ondelete='set null',
        help="The res.partner record of the recipient, if applicable."
    )
    recipient_email = fields.Char(
        string='Recipient Email'
    )
    recipient_phone = fields.Char(
        string='Recipient Phone'
    )
    channel_type = fields.Selection(
        [('email', 'Email'),
         ('sms', 'SMS'),
         ('push', 'Push Notification')],
        string='Channel Type',
        required=True
    )
    gateway_config_id = fields.Many2one(
        'dfr.notification.gateway.config',
        string='Gateway Used',
        ondelete='set null'
    )
    subject = fields.Char(
        string='Subject',
        help="The rendered subject of the notification."
    )
    body_preview = fields.Text(
        string='Body Preview',
        help="A preview or snippet of the rendered body."
    )
    status = fields.Selection(
        [('pending', 'Pending'),
         ('sent', 'Sent'),
         ('failed', 'Failed'),
         ('delivered', 'Delivered'), # Statuses reliant on gateway feedback
         ('read', 'Read')],          # Statuses reliant on gateway feedback
        string='Status',
        required=True,
        default='pending'
    )
    error_message = fields.Text(
        string='Error Message',
        help="Any error message if dispatch failed."
    )
    dispatch_timestamp = fields.Datetime(
        string='Dispatch Timestamp',
        default=fields.Datetime.now,
        required=True
    )
    related_record_model = fields.Char(
        string='Related Record Model',
        help="Model name of the record that triggered the notification (e.g., res.partner)."
    )
    related_record_id = fields.Integer(
        string='Related Record ID',
        help="ID of the record that triggered the notification."
    )
    message_id_external = fields.Char(
        string='External Message ID',
        help="Optional: External message ID provided by the gateway."
    )