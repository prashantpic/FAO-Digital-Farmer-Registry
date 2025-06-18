# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

class DfrAuditMixin(models.AbstractModel):
    """
    Mixin class to enhance audit trail capabilities for DFR models.
    Leverages Odoo's mail.thread for chatter and message logging.
    Can be extended with custom methods to log specific DFR auditable events.
    """
    _name = 'dfr.audit.mixin'
    _description = 'DFR Audit Trail Mixin'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Standard Odoo mixins for chatter and activities

    # Fields to track for changes automatically by mail.thread
    # This would be defined in the concrete models inheriting this mixin,
    # for example: _track = {'name': {}, 'status': {}}

    def log_dfr_specific_event(self, event_description, event_data=None):
        """
        Logs a DFR-specific event to the record's chatter.
        :param event_description: str, A human-readable description of the event.
        :param event_data: dict, Optional dictionary of key-value pairs for additional event details.
        """
        self.ensure_one()
        body = f"<p><strong>{_('DFR Event')}:</strong> {event_description}</p>"
        if event_data:
            body += "<ul>"
            for key, value in event_data.items():
                body += f"<li><strong>{key}:</strong> {value}</li>"
            body += "</ul>"
        self.message_post(body=body)

    # Override write method if specific pre/post audit logic is needed beyond mail.thread
    # def write(self, vals):
    #     # Pre-write audit logic if needed
    #     res = super(DfrAuditMixin, self).write(vals)
    #     # Post-write audit logic, e.g., log specific changes
    #     return res

    # Override create method if specific post-creation audit logic is needed
    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super(DfrAuditMixin, self).create(vals_list)
    #     # Post-create audit logic for each record
    #     return records