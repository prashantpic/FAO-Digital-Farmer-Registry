# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class DfrNotificationTemplate(models.Model):
    _name = 'dfr.notification.template'
    _description = 'DFR Notification Template'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
    technical_name = fields.Char(
        string='Technical Name',
        required=True,
        copy=False,
        help="A unique technical identifier for the template, used by automated actions."
    )
    channel_type = fields.Selection(
        [('email', 'Email'),
         ('sms', 'SMS'),
         ('push', 'Push Notification')],
        string='Channel Type',
        required=True
    )
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        help="The Odoo model that provides the context for this template."
    )
    model_name = fields.Char(
        string='Model Name',
        related='model_id.model',
        store=True,
        readonly=True
    )
    subject_template = fields.Text(
        string='Subject Template',
        translate=True,
        help="QWeb/Jinja2 template for the notification subject (primarily for email/push)."
    )
    body_template_qweb = fields.Text(
        string='Body QWeb Template',
        required=True,
        translate=True,
        help="QWeb/Jinja2 template for the notification body."
    )
    lang = fields.Char(
        string='Language',
        help="Optional language code (e.g., 'en_US'). If set, this template is specific to this language. "
             "If not set, it's a default template."
    )
    gateway_config_id = fields.Many2one(
        'dfr.notification.gateway.config',
        string='Preferred Gateway',
        domain="[('channel_type', '=', channel_type), ('active', '=', True)]",
        help="Optional preferred gateway for this template. If not set, a default gateway for the channel type will be used."
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether the template is active and can be used."
    )

    _sql_constraints = [
        ('technical_name_uniq', 'unique(technical_name)', 'Technical name must be unique!')
    ]

    def render_template(self, record_ids):
        """
        Renders the notification template for the given records.

        :param record_ids: List of record IDs or a recordset of the self.model_id.model
        :return: dict: A dictionary where keys are record IDs and values are tuples (rendered_subject, rendered_body).
                       Returns an empty dictionary if rendering fails for all records or if input is invalid.
        """
        self.ensure_one()  # This method should be called on a single template record

        if not record_ids:
            return {}

        records_to_render = None
        if isinstance(record_ids, models.BaseModel):
            records_to_render = record_ids
            if records_to_render._name != self.model_id.model:
                raise UserError(_("The provided records are not of the model '%s' defined in the template.", self.model_id.model))
        elif isinstance(record_ids, (list, tuple)):
            try:
                records_to_render = self.env[self.model_id.model].browse([int(rid) for rid in record_ids])
            except ValueError:
                 raise UserError(_("Invalid record IDs provided. Must be a list of integers."))
        else:
            raise UserError(_("Invalid 'record_ids' parameter. Expected a list of IDs or a recordset."))

        if not records_to_render.exists():
             _logger.warning("No valid records found for rendering template '%s' (ID: %s) with given IDs.", self.name, self.id)
             return {}

        results = {}
        qweb = self.env['ir.qweb']

        for record in records_to_render:
            try:
                render_context = {
                    'object': record,
                    'user': self.env.user,
                    'ctx': self.env.context, # Include current context
                }
                
                # Determine language for rendering
                # Priority: record's lang (if partner and lang field exists) > template's lang > context lang
                lang_code = self.env.context.get('lang') # Default to context lang
                if self.lang:
                    lang_code = self.lang
                
                # If recipient partner has a lang field (e.g. res.partner.lang)
                # This part is heuristic, actual field name might vary.
                # The service layer is a better place for complex lang determination per recipient.
                # For this model method, using template lang or context lang is safer.
                
                current_record_render_context = render_context.copy()
                if lang_code:
                    current_record_render_context['lang'] = lang_code
                    # For QWeb, language needs to be in the context when calling _render
                    # or passed via render_params if _render supports it directly for translations.
                    # Using with_context is safer for Odoo's translation machinery.
                    record_specific_env = self.env(context=dict(self.env.context, lang=lang_code))
                    qweb_to_use = record_specific_env['ir.qweb']
                else:
                    qweb_to_use = qweb


                rendered_subject = None
                if self.subject_template:
                    rendered_subject = qweb_to_use._render(self.subject_template, current_record_render_context, raise_if_not_found=False)
                    if isinstance(rendered_subject, bytes):
                        rendered_subject = rendered_subject.decode('utf-8')


                rendered_body = qweb_to_use._render(self.body_template_qweb, current_record_render_context, raise_if_not_found=False)
                if isinstance(rendered_body, bytes):
                    rendered_body = rendered_body.decode('utf-8')
                
                results[record.id] = (rendered_subject, rendered_body)

            except Exception as e:
                _logger.error(
                    "Failed to render template '%s' (ID: %s) for record %s (ID: %s). Error: %s",
                    self.name, self.id, record._name, record.id, e, exc_info=True
                )
                results[record.id] = (None, _("Error rendering template: %s") % e)
        
        return results