# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request
from .base_api_controller import BaseApiController
from ..services.auth_service import AuthService
from ..services.api_helper import ApiHelper
# from odoo.addons.dfr_security_audit_log.services import audit_log_service # Example import

_logger = logging.getLogger(__name__)

class AuthController(BaseApiController):

    @http.route('/api/dfr/v1/auth/token', type='http', auth='public', methods=['POST'], csrf=False)
    def get_token(self, **kwargs):
        """
        Handles token issuance based on OAuth2-like grant types.
        Currently supports 'password' grant type for mobile app/user login.
        Future: 'client_credentials' for server-to-server.
        """
        try:
            grant_type = kwargs.get('grant_type')
            auth_service = AuthService(request.env)

            if grant_type == 'password':
                username = kwargs.get('username')
                password = kwargs.get('password')
                # client_id = kwargs.get('client_id') # Optional: for client identification
                # client_secret = kwargs.get('client_secret') # Optional

                if not username or not password:
                    # audit_log_service.log_auth_attempt(request, success=False, reason="Missing credentials")
                    return ApiHelper.format_error_response(
                        'INVALID_REQUEST', 'Username and password are required for password grant type.', 400
                    )

                user = auth_service.authenticate_user_credentials(username, password)
                if user:
                    # TODO: Potentially check if user is allowed API access based on a flag or group
                    access_token, refresh_token, expires_in = auth_service.generate_jwt_tokens_for_user(user)
                    # audit_log_service.log_auth_attempt(request, user_id=user.id, success=True)
                    return ApiHelper.format_success_response(data={
                        'access_token': access_token,
                        'token_type': 'Bearer',
                        'expires_in': expires_in,
                        'refresh_token': refresh_token, # Optional
                        'user_id': user.id,
                        'user_name': user.name,
                        'user_role': [group.name for group in user.groups_id if group.is_application] # Example, tailor as needed
                    })
                else:
                    # audit_log_service.log_auth_attempt(request, username=username, success=False, reason="Invalid credentials")
                    return ApiHelper.format_error_response(
                        'INVALID_GRANT', 'Invalid username or password.', 400 # OAuth2 uses 400 for invalid_grant
                    )
            # TODO: Implement 'client_credentials' grant type for trusted server-to-server
            # elif grant_type == 'client_credentials':
            #     client_id = kwargs.get('client_id')
            #     client_secret = kwargs.get('client_secret')
            #     # ... validate client_id and client_secret ...
            #     # ... generate token for the client app ...
            #     pass

            elif grant_type: # Check if grant_type is not None before formatting the message
                # audit_log_service.log_auth_attempt(request, success=False, reason=f"Unsupported grant_type: {grant_type}")
                return ApiHelper.format_error_response(
                    'UNSUPPORTED_GRANT_TYPE', f"Grant type '{grant_type}' is not supported.", 400
                )
            else:
                # audit_log_service.log_auth_attempt(request, success=False, reason="Missing grant_type")
                return ApiHelper.format_error_response(
                    'INVALID_REQUEST', 'grant_type is required.', 400
                )
        except Exception as e:
            _logger.exception("Error in /auth/token endpoint")
            # audit_log_service.log_auth_attempt(request, success=False, reason=f"Server error: {str(e)}")
            # This will be caught by BaseApiController._handle_exceptions if this controller inherits it AND
            # this method is decorated with BaseApiController.route.
            # Since it's using http.route directly, we return the error response explicitly.
            return ApiHelper.format_error_response('INTERNAL_SERVER_ERROR', str(e), 500)