# -*- coding: utf-8 -*-
import json
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class AuditLogService(models.AbstractModel):
    _name = 'dfr.audit_log.service'
    _description = 'DFR Audit Log Service'

    @api.model
    def _get_request_session_info(self, env):
        """
        Helper method to extract IP address and User Agent from the current request in env.
        """
        try:
            httprequest = env.context.get('request') and env.context.get('request').httprequest
            if not httprequest and hasattr(env, 'request') and env.request: # For Odoo 15+ controller context
                httprequest = env.request.httprequest

            if httprequest:
                ip_address = httprequest.remote_addr
                user_agent = httprequest.user_agent.string if httprequest.user_agent else None
                if ip_address and user_agent:
                    return f"IP: {ip_address}, UA: {user_agent}"
                elif ip_address:
                    return f"IP: {ip_address}"
                elif user_agent:
                    return f"UA: {user_agent}"
        except Exception as e:
            _logger.warning("Could not retrieve request session info: %s", e)
        return None

    @api.model
    def log_event(self, env, event_type, description, model_name=None, res_id=None,
                  user_id=None, technical_details=None, status='success', session_info=None):
        """
        Creates an audit log entry.
        """
        if not event_type or not description:
            _logger.error("Audit log event_type and description are required.")
            return None

        vals = {
            'timestamp': fields.Datetime.now(),
            'event_type': event_type,
            'description': description,
            'status': status,
        }

        if user_id is None:
            vals['user_id'] = env.user.id
        else:
            vals['user_id'] = user_id
        
        if model_name:
            model_record = env['ir.model'].sudo().search([('model', '=', model_name)], limit=1)
            if model_record:
                vals['model_id'] = model_record.id
                if res_id:
                    # Odoo's Reference field expects format: 'model,res_id'
                    vals['res_id'] = f"{model_name},{res_id}"
            else:
                _logger.warning(f"Audit log: Model '{model_name}' not found.")
        
        if session_info is None:
            vals['session_info'] = self._get_request_session_info(env)
        else:
            vals['session_info'] = session_info

        if technical_details:
            if isinstance(technical_details, dict):
                try:
                    vals['technical_details'] = json.dumps(technical_details, indent=2, sort_keys=True, default=str)
                except TypeError as e:
                    _logger.error(f"Error serializing technical_details to JSON: {e}. Storing as string.")
                    vals['technical_details'] = str(technical_details)
            else:
                vals['technical_details'] = str(technical_details)
        
        try:
            # Using sudo() to ensure log creation regardless of the calling user's direct permissions
            # on dfr.audit.log. This is a security consideration: audit logs should always be created.
            # The user performing the action is captured in user_id.
            audit_log_record = env['dfr.audit.log'].sudo().create(vals)
            _logger.info(f"Audit event logged: {event_type} - {description}")
            return audit_log_record
        except Exception as e:
            _logger.error("Failed to create audit log entry: %s. Values: %s", e, vals, exc_info=True)
            return None

    @api.model
    def log_record_change(self, env, model_name, res_id, change_type, description,
                          old_values=None, new_values=None, user_id=None, session_info=None):
        """
        Logs changes to a record (create, update, delete).
        """
        event_type_mapping = {
            'create': 'record_create',
            'update': 'record_update',
            'delete': 'record_delete',
        }
        event_type = event_type_mapping.get(change_type, 'custom_action') # Fallback if change_type is not standard

        tech_details = {}
        if old_values:
            tech_details['raw_old'] = old_values
        if new_values:
            tech_details['raw_new'] = new_values
        
        if change_type == 'update' and old_values and new_values:
            changed_fields = {}
            all_keys = set(old_values.keys()) | set(new_values.keys())
            for key in all_keys:
                old_val = old_values.get(key)
                new_val = new_values.get(key)
                if old_val != new_val: # Simplified diff; consider more robust diffing if needed
                    changed_fields[key] = {'old': old_val, 'new': new_val}
            if changed_fields:
                tech_details['changed_fields'] = changed_fields
        
        return self.log_event(
            env,
            event_type=event_type,
            description=description,
            model_name=model_name,
            res_id=res_id,
            user_id=user_id,
            technical_details=tech_details if tech_details else None,
            session_info=session_info
        )

    @api.model
    def log_login_event(self, env, login, success, ip_address=None, user_agent=None):
        """
        Logs a login attempt.
        """
        event_type = 'login_success' if success else 'login_fail'
        status = 'success' if success else 'failure'
        
        user_record = env['res.users'].sudo().search([('login', '=', login)], limit=1)
        user_id_to_log = user_record.id if user_record else None

        if success:
            description = _("Successful login attempt for user '%s'.") % login
            if not user_id_to_log: # Should not happen for successful login
                 _logger.warning(f"Successful login for '{login}' but user record not found.")
        else:
            description = _("Failed login attempt for user '%s'.") % login
            if not user_id_to_log:
                # For failed logins, user_id might be None if the user does not exist.
                # It's also possible Odoo creates a log for a system user in some failure scenarios.
                # Here, we log with user_id=None if the user isn't found by login.
                pass


        session_parts = []
        if ip_address:
            session_parts.append(f"IP: {ip_address}")
        if user_agent:
            session_parts.append(f"UA: {user_agent}")
        session_info_str = ", ".join(session_parts) if session_parts else None

        technical_details = {'login_username': login}

        return self.log_event(
            env,
            event_type=event_type,
            description=description,
            user_id=user_id_to_log, # Can be None if user not found (e.g. failed login for non-existent user)
            technical_details=technical_details,
            status=status,
            session_info=session_info_str,
            model_name='res.users', # Login event is related to res.users
            res_id=user_id_to_log if user_id_to_log else None # Associate with user if found
        )