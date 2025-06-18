# -*- coding: utf-8 -*-
import functools
import json
import logging
import werkzeug

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, UserError, ValidationError

from ..services.auth_service import AuthService
from ..services.api_helper import ApiHelper

_logger = logging.getLogger(__name__)

class BaseApiController(http.Controller):

    # Decorator for JWT authentication and authorization
    def _authenticate_request(self, required_groups=None):
        """
        Decorator to authenticate API requests using JWT.
        Optionally checks if the authenticated user belongs to one of the required_groups.
        required_groups: A list of XML IDs of Odoo security groups.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                auth_header = request.httprequest.headers.get('Authorization')
                token = None
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

                if not token:
                    # AuditLogService.log_api_access_attempt(request, success=False, reason="Missing token")
                    return ApiHelper.format_error_response(
                        error_code='UNAUTHORIZED',
                        error_message='Authentication token is missing.',
                        status_code=401
                    )

                auth_service = AuthService(request.env)
                # Pass request.env to get_user_from_token for user browsing in correct environment
                user = auth_service.get_user_from_token(request.env, token)

                if not user:
                    # AuditLogService.log_api_access_attempt(request, success=False, reason="Invalid token")
                    return ApiHelper.format_error_response(
                        error_code='INVALID_TOKEN',
                        error_message='Invalid or expired authentication token.',
                        status_code=401
                    )
                
                # Set Odoo environment UID to the authenticated user for ORM operations
                # and store the user record on the request for easy access in controllers.
                request.env.uid = user.id 
                request.dfr_api_user = user # Custom attribute to store the user record

                # Authorization check
                if required_groups:
                    is_authorized = False
                    if not isinstance(required_groups, list):
                        _logger.error(f"required_groups must be a list, got {type(required_groups)}")
                        # AuditLogService.log_api_access_denied(request, user, reason="Server configuration error: required_groups not a list")
                        return ApiHelper.format_error_response(
                            error_code='INTERNAL_SERVER_ERROR',
                            error_message='Server configuration error related to authorization.',
                            status_code=500
                        )
                    
                    for group_xml_id in required_groups:
                        try:
                            if user.has_group(group_xml_id):
                                is_authorized = True
                                break
                        except Exception as e:
                            _logger.error(f"Error checking group {group_xml_id} for user {user.login}: {e}")
                            # AuditLogService.log_api_access_denied(request, user, reason=f"Server error checking group {group_xml_id}")
                            return ApiHelper.format_error_response(
                                error_code='INTERNAL_SERVER_ERROR',
                                error_message='Error during authorization check.',
                                status_code=500
                            )
                    if not is_authorized:
                        _logger.warning(f"User {user.login} (ID: {user.id}) does not have required groups: {required_groups} for {request.httprequest.path}")
                        # AuditLogService.log_api_access_denied(request, user, required_groups=required_groups)
                        return ApiHelper.format_error_response(
                            error_code='FORBIDDEN',
                            error_message='User does not have the required permissions.',
                            status_code=403
                        )
                
                # Log successful access if needed by AuditLogService
                # AuditLogService.log_api_access_success(request, user, path=request.httprequest.path)
                
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def _handle_exceptions(self, func):
        """Decorator to handle common exceptions and return standardized API errors."""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except AccessError as e:
                _logger.warning(f"AccessError in API ({request.httprequest.path}): {e}. User: {request.env.user.login if request.env.user else 'Unknown'}")
                # AuditLogService.log_api_error(request, error_type='AccessError', message=str(e))
                return ApiHelper.format_error_response('FORBIDDEN', str(e), 403)
            except (UserError, ValidationError) as e:
                _logger.warning(f"UserError/ValidationError in API ({request.httprequest.path}): {e}. User: {request.env.user.login if request.env.user else 'Unknown'}")
                # AuditLogService.log_api_error(request, error_type=type(e).__name__, message=str(e))
                return ApiHelper.format_error_response('BAD_REQUEST', str(e), 400)
            except werkzeug.exceptions.NotFound as e:
                _logger.info(f"Resource not found: {request.httprequest.url}. Error: {e}")
                # AuditLogService.log_api_error(request, error_type='NotFound', message='Resource not found')
                return ApiHelper.format_error_response('NOT_FOUND', 'The requested resource was not found.', 404)
            except Exception as e:
                _logger.exception(f"Unhandled exception in API controller ({request.httprequest.path}): {e}. User: {request.env.user.login if request.env.user else 'Unknown'}")
                # AuditLogService.log_api_error(request, error_type='Exception', message=str(e), traceback=True)
                return ApiHelper.format_error_response('INTERNAL_SERVER_ERROR', 'An unexpected error occurred.', 500)
        return wrapper

    def route(self, route=None, **kw):
        """
        Override http.route to apply exception handling to all routed methods
        by default. Authentication is applied explicitly where needed.
        """
        original_route_decorator = http.route(route, **kw)
        
        def decorator(f):
            # Apply exception handling first
            handler_f = self._handle_exceptions(f)
            # Then apply Odoo's routing to the exception-handled function
            return original_route_decorator(handler_f)
        return decorator