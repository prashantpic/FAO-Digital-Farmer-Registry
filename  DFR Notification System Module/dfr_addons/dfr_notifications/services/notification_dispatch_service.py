# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class NotificationDispatchService(models.AbstractModel):
    _name = 'dfr.notification.dispatch.service'
    _description = 'DFR Notification Dispatch Service'

    @api.model
    def send_notification_by_template_name(self, template_technical_name, record_id,
                                           recipient_partner_ids=None, recipient_emails=None,
                                           recipient_phones=None, force_channel_type=None,
                                           custom_context=None):
        """
        Primary public method to send a notification using a template's technical name.
        """
        if not template_technical_name:
            _logger.error("send_notification_by_template_name: template_technical_name is required.")
            return

        template_obj = self.env['dfr.notification.template'].search([
            ('technical_name', '=', template_technical_name),
            ('active', '=', True)
        ], limit=1)

        if not template_obj:
            _logger.error(
                "Notification template with technical_name '%s' not found or is inactive.",
                template_technical_name
            )
            # Log a generic failure attempt if template not found
            self._log_notification_attempt_error(
                template_technical_name=template_technical_name,
                record_id=record_id,
                error_message=_("Template '%s' not found or inactive.") % template_technical_name
            )
            return

        return self.send_notification_by_template_id(
            template_obj, record_id,
            recipient_partner_ids=recipient_partner_ids,
            recipient_emails=recipient_emails,
            recipient_phones=recipient_phones,
            force_channel_type=force_channel_type,
            custom_context=custom_context
        )

    @api.model
    def send_notification_by_template_id(self, template_obj, record_id,
                                         recipient_partner_ids=None, recipient_emails=None,
                                         recipient_phones=None, force_channel_type=None,
                                         custom_context=None):
        """
        Sends a notification using a direct template object.
        """
        if not isinstance(template_obj, models.BaseModel) or not template_obj.exists():
            _logger.error("send_notification_by_template_id: template_obj is invalid.")
            return
        if not record_id:
            _logger.error("send_notification_by_template_id: record_id is required.")
            self._log_notification_attempt_error(
                template_obj=template_obj,
                record_id=record_id, # record_id might be None, but try to log
                error_message=_("Context record_id is required for template %s.") % template_obj.name
            )
            return

        if not template_obj.active:
            _logger.warning("Attempt to send notification using inactive template: %s (ID: %s)", template_obj.name, template_obj.id)
            self._log_notification_attempt_error(
                template_obj=template_obj,
                record_id=record_id,
                error_message=_("Template '%s' (ID: %s) is inactive.") % (template_obj.name, template_obj.id)
            )
            return

        channel_type = force_channel_type or template_obj.channel_type

        # Determine Recipients
        recipients_info_list = []
        if recipient_partner_ids:
            for partner in recipient_partner_ids:
                info = {'partner_id': partner.id, 'record_id_context': record_id}
                if channel_type == 'email' and partner.email:
                    info['email'] = partner.email
                if channel_type == 'sms' and partner.phone: # Assuming 'phone' is the mobile field for SMS
                    info['phone'] = partner.phone
                # For push, we'd need a device token, assuming it's on partner or passed differently
                # For now, push notifications would require explicit device_tokens
                recipients_info_list.append(info)

        if recipient_emails:
            for email in recipient_emails:
                recipients_info_list.append({'email': email, 'record_id_context': record_id})

        if recipient_phones:
            for phone in recipient_phones:
                recipients_info_list.append({'phone': phone, 'record_id_context': record_id})
        
        if not recipients_info_list:
            _logger.warning("No recipients specified for template %s (ID: %s)", template_obj.name, template_obj.id)
            self._log_notification_attempt(
                template_obj, {}, None, 'failed', 
                _("No recipients specified."),
                record_id_context=record_id
            )
            return
        
        # Fetch Context Record
        try:
            record = self.env[template_obj.model_id.model].browse(record_id)
            if not record.exists():
                _logger.error("Context record %s with ID %s not found for template %s.",
                              template_obj.model_id.model, record_id, template_obj.name)
                self._log_notification_attempt_error(
                    template_obj=template_obj,
                    record_id=record_id,
                    error_message=_("Context record %s with ID %s not found.") % (template_obj.model_id.model, record_id)
                )
                return
        except Exception as e:
            _logger.error("Error fetching context record %s with ID %s for template %s: %s",
                          template_obj.model_id.model, record_id, template_obj.name, e)
            self._log_notification_attempt_error(
                template_obj=template_obj,
                record_id=record_id,
                error_message=_("Error fetching context record: %s") % e
            )
            return

        # Iterate through Recipients
        for recipient_info in recipients_info_list:
            # Validate recipient for channel
            if channel_type == 'email' and not recipient_info.get('email'):
                _logger.warning("Skipping recipient (Partner ID: %s) due to missing email for email channel.", recipient_info.get('partner_id'))
                self._log_notification_attempt(template_obj, recipient_info, None, 'failed', _("Missing email address for email channel."), record_id_context=record_id)
                continue
            if channel_type == 'sms' and not recipient_info.get('phone'):
                _logger.warning("Skipping recipient (Partner ID: %s) due to missing phone for SMS channel.", recipient_info.get('partner_id'))
                self._log_notification_attempt(template_obj, recipient_info, None, 'failed', _("Missing phone number for SMS channel."), record_id_context=record_id)
                continue
            if channel_type == 'push' and not recipient_info.get('device_token'): # Assuming device_token needed
                 _logger.warning("Skipping recipient (Partner ID: %s) due to missing device token for Push channel.", recipient_info.get('partner_id'))
                 # Not explicitly logging here as the _dispatch_via_channel should handle lack of token with connector.
                 # However, if passed device_tokens are primary, this check is useful.
                 # For now, it will be handled by the connector call.

            # Render Content
            try:
                rendered_subject, rendered_body = self._render_template_content(template_obj, record, custom_context)
            except Exception as e:
                _logger.error("Error rendering template %s for record %s: %s", template_obj.name, record.id, e)
                self._log_notification_attempt(template_obj, recipient_info, None, 'failed', _("Template rendering error: %s") % e, record_id_context=record_id)
                continue

            # Determine Gateway
            gateway_config = template_obj.gateway_config_id if template_obj.gateway_config_id and template_obj.gateway_config_id.active else None
            if not gateway_config:
                gateway_config = self.env['dfr.notification.gateway.config'].search([
                    ('channel_type', '=', channel_type),
                    ('active', '=', True)
                ], limit=1) # Add order for preference if needed

            if not gateway_config and channel_type == 'email': # Odoo default email can be a fallback if no explicit gateway
                # Check for an "Odoo Default Email" config type or assume it if none found
                odoo_default_email_gw = self.env['dfr.notification.gateway.config'].search([
                    ('channel_type', '=', 'email'),
                    ('is_odoo_default_email', '=', True),
                    ('active', '=', True)
                ], limit=1)
                if odoo_default_email_gw:
                    gateway_config = odoo_default_email_gw
                # If still no gateway_config, _dispatch_via_channel might handle Odoo default email if logic allows it.
                # For safety, we can create a dummy one if `is_odoo_default_email` is a key factor.
                # The SDS implies Odoo Default Email *is* a type of gateway_config.

            if not gateway_config and channel_type != 'email': # For non-email, a gateway is usually mandatory
                _logger.warning("No active gateway found for channel type %s for template %s.", channel_type, template_obj.name)
                self._log_notification_attempt(template_obj, recipient_info, None, 'failed', _("No active gateway for channel %s.") % channel_type, rendered_subject, rendered_body, record_id_context=record_id)
                continue
            
            # If it's email and no specific gateway_config, _dispatch_via_channel will try Odoo's default mail.mail
            # so gateway_config can be None here for email.

            # Dispatch
            self._dispatch_via_channel(template_obj, gateway_config, rendered_subject, rendered_body, recipient_info, record)

    def _render_template_content(self, template_obj, record, custom_context=None):
        """
        Renders subject and body of a template for a given record.
        """
        rendering_context = {
            'object': record,
            'user': self.env.user,
            'env': self.env # Provide access to env for more complex templates
        }
        if custom_context:
            rendering_context.update(custom_context)

        # Language handling:
        # Odoo's _render method itself can handle language context if the record or user has a lang.
        # We can also explicitly pass lang if template_obj.lang is set.
        render_options = {}
        if template_obj.lang:
            render_options['lang'] = template_obj.lang
        
        qweb = self.env['ir.qweb']
        
        rendered_subject = None
        if template_obj.subject_template:
            try:
                rendered_subject = qweb._render(template_obj.subject_template, rendering_context, **render_options)
                if isinstance(rendered_subject, bytes): # QWeb can return bytes
                    rendered_subject = rendered_subject.decode('utf-8')
            except Exception as e:
                _logger.error("Error rendering subject for template %s: %s", template_obj.name, e)
                raise UserError(_("Error rendering subject for template %s: %s") % (template_obj.name, e))

        try:
            rendered_body = qweb._render(template_obj.body_template_qweb, rendering_context, **render_options)
            if isinstance(rendered_body, bytes): # QWeb can return bytes
                rendered_body = rendered_body.decode('utf-8')
        except Exception as e:
            _logger.error("Error rendering body for template %s: %s", template_obj.name, e)
            raise UserError(_("Error rendering body for template %s: %s") % (template_obj.name, e))
            
        return rendered_subject, rendered_body

    def _dispatch_via_channel(self, template_obj, gateway_config, subject, body, recipient_info, record_context):
        """
        Calls the appropriate connector service or Odoo's mail system.
        record_context is the record for which template was rendered (for logging related_record_id).
        """
        channel = template_obj.channel_type
        status = 'failed'  # Default status
        error_message = None
        external_message_id = None # Initialize external message ID

        try:
            if channel == 'email':
                recipient_email = recipient_info.get('email')
                if not recipient_email:
                    error_message = _("Recipient email address not found.")
                elif gateway_config and gateway_config.is_odoo_default_email:
                    mail_values = {
                        'subject': subject,
                        'body_html': body,
                        'email_to': recipient_email,
                        'email_from': gateway_config.email_from or self.env['ir.mail_server']._get_default_bounce_address(),
                        'model': record_context._name if record_context else template_obj.model_id.model,
                        'res_id': record_context.id if record_context else recipient_info.get('record_id_context'),
                    }
                    mail = self.env['mail.mail'].sudo().create(mail_values)
                    mail.send()
                    status = 'sent'
                    external_message_id = mail.message_id # mail.mail message_id is Odoo's internal, not necessarily external gateway's
                elif gateway_config: # Custom email gateway
                    # Ensure the connector service exists
                    if 'dfr.email.connector' not in self.env:
                        raise UserError(_("DFR Email Connector service (dfr.email.connector) not found. Please ensure the DFR External Integration Connectors module is installed and configured."))
                    
                    # Call to external connector
                    conn_status, conn_error, conn_msg_id = self.env['dfr.email.connector'].send_email(
                        gateway_config, recipient_email, subject, body
                    ) # Assuming connector returns (status_str, error_str_or_None, message_id_or_None)
                    status = conn_status if conn_status else 'failed'
                    error_message = conn_error
                    external_message_id = conn_msg_id
                else: # Fallback to Odoo default email if no gateway_config was resolved but it's an email
                    _logger.info("No specific email gateway, attempting Odoo default for recipient %s", recipient_email)
                    mail_values = {
                        'subject': subject,
                        'body_html': body,
                        'email_to': recipient_email,
                        'email_from': self.env['ir.mail_server']._get_default_bounce_address(),
                        'model': record_context._name if record_context else template_obj.model_id.model,
                        'res_id': record_context.id if record_context else recipient_info.get('record_id_context'),
                    }
                    mail = self.env['mail.mail'].sudo().create(mail_values)
                    mail.send()
                    status = 'sent'
                    external_message_id = mail.message_id


            elif channel == 'sms':
                recipient_phone = recipient_info.get('phone')
                if not recipient_phone:
                    error_message = _("Recipient phone number not found.")
                elif not gateway_config:
                    error_message = _("SMS Gateway configuration not found for template %s.") % template_obj.name
                else:
                    if 'dfr.sms.connector' not in self.env:
                        raise UserError(_("DFR SMS Connector service (dfr.sms.connector) not found. Please ensure the DFR External Integration Connectors module is installed and configured."))
                    
                    conn_status, conn_error, conn_msg_id = self.env['dfr.sms.connector'].send_sms(
                        gateway_config, recipient_phone, body
                    )
                    status = conn_status if conn_status else 'failed'
                    error_message = conn_error
                    external_message_id = conn_msg_id

            elif channel == 'push':
                # Push notifications require a device token, which should be in recipient_info
                device_token = recipient_info.get('device_token') # Or however it's structured
                if not device_token:
                    error_message = _("Recipient device token not found for push notification.")
                elif not gateway_config:
                    error_message = _("Push Notification Gateway configuration not found for template %s.") % template_obj.name
                else:
                    if 'dfr.push.connector' not in self.env:
                         raise UserError(_("DFR Push Connector service (dfr.push.connector) not found. Please ensure the DFR External Integration Connectors module is installed and configured."))

                    # Assuming custom_payload can be derived or is part of template. For now, empty.
                    custom_payload_from_template_maybe = {}
                    conn_status, conn_error, conn_msg_id = self.env['dfr.push.connector'].send_push(
                        gateway_config, device_token, subject, body,
                        data_payload=custom_payload_from_template_maybe
                    )
                    status = conn_status if conn_status else 'failed'
                    error_message = conn_error
                    external_message_id = conn_msg_id
            else:
                error_message = _("Unsupported channel type: %s") % channel

        except Exception as e:
            _logger.exception("Dispatch failed for template %s, recipient %s: %s",
                              template_obj.name, recipient_info, e)
            status = 'failed'
            error_message = str(e)

        self._log_notification_attempt(template_obj, recipient_info, gateway_config, status,
                                       error_message, subject, body, external_message_id,
                                       record_id_context=recipient_info.get('record_id_context'))

    def _log_notification_attempt(self, template_obj, recipient_info, gateway_config,
                                 status, error_message=None, subject=None, body_preview=None,
                                 message_id_external=None, record_id_context=None):
        """
        Logs the notification attempt to dfr.notification.log.
        `record_id_context` is the ID of the record object that was used in template rendering.
        """
        log_values = {
            'template_id': template_obj.id if template_obj else None,
            'recipient_partner_id': recipient_info.get('partner_id'),
            'recipient_email': recipient_info.get('email'),
            'recipient_phone': recipient_info.get('phone'),
            'channel_type': template_obj.channel_type if template_obj else None,
            'gateway_config_id': gateway_config.id if gateway_config else None,
            'subject': subject,
            'body_preview': (body_preview[:497] + '...') if body_preview and len(body_preview) > 500 else body_preview,
            'status': status,
            'error_message': error_message,
            'dispatch_timestamp': fields.Datetime.now(),
            'related_record_model': template_obj.model_id.model if template_obj and template_obj.model_id else None,
            'related_record_id': record_id_context,
            'message_id_external': message_id_external,
        }
        try:
            self.env['dfr.notification.log'].sudo().create(log_values)
        except Exception as e:
            _logger.error("Failed to create notification log: %s. Log values: %s", e, log_values)

    def _log_notification_attempt_error(self, template_obj=None, template_technical_name=None, record_id=None, error_message=None):
        """Helper to log errors when template object might not be available."""
        log_values = {
            'recipient_email': None, # Cannot determine without more context
            'recipient_phone': None,
            'channel_type': template_obj.channel_type if template_obj else None,
            'gateway_config_id': None,
            'subject': _("Notification Dispatch Error"),
            'body_preview': error_message,
            'status': 'failed',
            'error_message': error_message,
            'dispatch_timestamp': fields.Datetime.now(),
            'related_record_model': template_obj.model_id.model if template_obj and template_obj.model_id else None,
            'related_record_id': record_id,
        }
        if template_obj:
            log_values['template_id'] = template_obj.id
        elif template_technical_name:
            # Attempt to find template for logging reference, but don't fail if not found
            tmpl = self.env['dfr.notification.template'].search([('technical_name', '=', template_technical_name)], limit=1)
            if tmpl:
                log_values['template_id'] = tmpl.id
                log_values['channel_type'] = tmpl.channel_type
                log_values['related_record_model'] = tmpl.model_id.model if tmpl.model_id else None

        try:
            self.env['dfr.notification.log'].sudo().create(log_values)
        except Exception as e:
            _logger.error("Failed to create notification error log: %s. Log values: %s", e, log_values)