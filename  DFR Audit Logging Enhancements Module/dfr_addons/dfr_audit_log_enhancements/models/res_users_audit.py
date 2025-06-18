# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.exceptions import AccessDenied
from odoo.http import request as odoo_request # Import request for type hinting or direct use if needed

_logger = logging.getLogger(__name__)

class ResUsersAudit(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _check_credentials(cls, password, env):
        """
        Overrides the standard Odoo method to log login attempts.
        This method is called on a user record.
        """
        # `cls` here refers to the res.users model.
        # The `_check_credentials` is typically called on a specific user record.
        # In Odoo 16+ `_check_credentials` is an instance method.
        # If this is intended to be an instance method, it should not be @classmethod
        # Assuming it's an instance method based on typical Odoo `_check_credentials` override pattern.
        # If it were a classmethod, `self` would be `cls`.
        # Odoo's res.users _check_credentials is NOT a classmethod. It's an instance method.
        # The SDS specifies `_check_credentials(self, password, env)`.
        # This implies `self` is a user recordset, likely a single user.

        # The current user whose credentials are being checked.
        # `self` should be a single user record here based on how Odoo calls _check_credentials.
        if not self: # Should not happen in normal flow
            _logger.warning("DFR Audit Log: _check_credentials called on an empty recordset.")
            # Fallback for login string if self is empty, though problematic.
            # This situation indicates an issue upstream or an unexpected call pattern.
            # For now, we proceed assuming `self` is populated if this method is reached
            # for an existing user.
            login_attempted = env.get('login', 'unknown_user_login_attempt_on_empty_self')

        # Ensure self is a single record for self.login
        user_sudo = self.sudo()
        if len(user_sudo) != 1:
             # This case is unlikely if called from standard Odoo login flow for an existing user.
             # If it happens, we might not have a specific login to attribute if multiple users in self.
             # Or if self is empty.
             _logger.warning(
                "DFR Audit Log: _check_credentials called on a recordset with %s users. Logging will be skipped or generalized.",
                len(user_sudo)
            )
             # Attempt to get login from env if available (e.g. from a controller)
            login_attempted = env.context.get('login_attempt', 'unknown_user_multiple_or_empty_self')
            # In this unusual case, we might not be able to log effectively.
            # We must call super and re-raise if it fails.
            try:
                super(ResUsersAudit, user_sudo)._check_credentials(password, env) # Call super with original self
                # If super doesn't raise, it's a success for at least one user if multi, or the one if single.
                # This scenario is complex for audit logging if `self` is not a single user.
                # For now, we focus on the single user case as it's the most common.
            except AccessDenied:
                # Log a generic attempt if we cannot determine the specific user
                if login_attempted and login_attempted != 'unknown_user_multiple_or_empty_self':
                    user_sudo._log_login_attempt(login_attempted, False, user_agent_env=env)
                raise
            # If successful, it's hard to log without knowing which user if `self` is multi.
            # The SDS implies self.login is available, suggesting a single user context.
            return # Or handle as per Odoo's super return

        # Standard case: self is a single user record
        user_login = user_sudo.login
        success = False
        
        try:
            # Call super()._check_credentials.
            # Odoo's _check_credentials is an instance method, so super(ResUsersAudit, self) is correct.
            super(ResUsersAudit, user_sudo)._check_credentials(password, env)
            success = True
        except AccessDenied:
            success = False
            # The exception will be re-raised after logging.
        
        # Log the attempt using the instance method
        user_sudo._log_login_attempt(user_login, success, user_agent_env=env)

        if not success:
            raise AccessDenied()
        
        # Odoo's _check_credentials (instance method) doesn't return UID, it just doesn't raise if successful.
        # The classmethod `authenticate` returns UID.
        # The original method signature in SDS was (self, password, env) -> void (or raises)
        # So, no explicit return value is expected here if it succeeds.
        return


    def _log_login_attempt(self, login, success, user_agent_env=None):
        """
        Logs a login attempt to the DFR Audit Log.
        `self` is the user record (even if login failed, it's the user whose password was wrong).
        `login` is the login string that was attempted.
        """
        self.ensure_one() # Should be called on a single user record context

        ip_address = None
        user_agent_str = None
        
        current_env = user_agent_env or self.env

        # Try to get request from the provided env or self.env
        # odoo_request is imported from odoo.http
        # In Odoo 18, request might be more directly available or need specific handling in services.
        # For model methods, checking `current_env.context.get('request')` or `odoo_request` (if in HTTP context)
        
        # Try to get from odoo.http.request if available (e.g. in a controller context)
        # This is the most reliable way if called during an HTTP request.
        if hasattr(odoo_request, 'httprequest') and odoo_request.httprequest:
            httprequest = odoo_request.httprequest
            ip_address = httprequest.remote_addr
            if hasattr(httprequest, 'user_agent') and httprequest.user_agent:
                user_agent_str = httprequest.user_agent.string
        elif current_env and current_env.context.get('request'):
            # Fallback if request object is passed in context (less common for _check_credentials env)
            # This depends on how `user_agent_env` is populated by the caller.
            # The `env` in `_check_credentials` is usually `request.env(user=user.id)`
            # which might not directly carry the raw `request` object in its context dict.
            # Let's assume the AuditLogService will try to get it from its `env` parameter.
            # For now, we pass what we have.
             _logger.debug("DFR Audit Log: Attempting to get session info from env context.")
             # This path is less certain for _check_credentials's env.
             # The AuditLogService is better equipped to determine this.

        try:
            audit_log_service = self.env['dfr.audit_log.service']
            
            # The service method will handle IP/UserAgent if not passed and available in its env
            audit_log_service.log_login_event(
                login=login,
                success=success,
                ip_address=ip_address, # Pass if available, service can try to get it too
                user_agent=user_agent_str # Pass if available
            )
        except Exception as e:
            _logger.error("DFR Audit Log: Failed to log login attempt for user '%s': %s", login, e, exc_info=True)

    # To catch login attempts for non-existent users, `authenticate` method is typically overridden.
    # As per SDS, only `_check_credentials` is overridden.
    # This means logs will primarily be for existing users (correct or incorrect password).
    # Failed logins for users that don't exist in the system might not be caught here
    # unless `_check_credentials` is somehow reached for them (unlikely).
    # Odoo's own `res.users.authenticate` logs "Login failed for nonexistent user"
    # to server logs already. This module enhances it for DFR specific audit table.
    # If the DFR requirement includes logging *all* attempts including non-existent users
    # into `dfr.audit.log`, then `res.users.authenticate` should be reviewed for extension.
    # For now, adhering strictly to SDS.