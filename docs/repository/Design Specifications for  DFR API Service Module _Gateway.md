# DFR API Service Module (Gateway) - Software Design Specification

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR API Service Module (Gateway). This module serves as the central API gateway for the Digital Farmer Registry (DFR) platform. It exposes secure RESTful API endpoints for consumption by the mobile enumerator application and authorized external systems. Its responsibilities include request routing, robust authentication (OAuth2/JWT), fine-grained authorization based on user roles, and data serialization/deserialization (JSON).

### 1.2 Scope
The scope of this SDS covers the design and implementation of the `dfr_api_services` Odoo module. This includes:
-   Definition and implementation of all API endpoints as specified.
-   Authentication and authorization mechanisms for API access.
-   Data transformation and validation for API requests and responses.
-   Generation and serving of OpenAPI v3.x documentation.
-   Integration with other DFR modules (`DFR_MOD_FARMER_REGISTRY`, `DFR_MOD_DYNAMIC_FORMS`, `DFR_MOD_RBAC_CONFIG`, `DFR_MOD_SECURITY_AUDIT_LOG`, `DFR_MOD_CORE_COMMON`) to fulfill API requests.

### 1.3 Definitions, Acronyms, and Abbreviations
-   **API:** Application Programming Interface
-   **DFR:** Digital Farmer Registry
-   **SDS:** Software Design Specification
-   **JSON:** JavaScript Object Notation
-   **REST:** Representational State Transfer
-   **HTTP:** Hypertext Transfer Protocol
-   **HTTPS:** HTTP Secure
-   **OAuth2:** Open Authorization 2.0 framework (RFC 6749)
-   **JWT:** JSON Web Token (RFC 7519)
-   **CRUD:** Create, Read, Update, Delete
-   **ORM:** Object-Relational Mapper
-   **OCA:** Odoo Community Association
-   **QWeb:** Odoo's primary templating engine
-   **PyJWT:** Python library for JWT encoding/decoding
-   **RBAC:** Role-Based Access Control
-   **OpenAPI:** OpenAPI Specification (formerly Swagger Specification)
-   **UID:** Unique Identifier

## 2. References
-   **User Requirements Document (SRS):**
    -   REQ-PCA-007: Secure RESTful API layer requirement.
    -   REQ-API-001: RESTful API conventions and error handling.
    -   REQ-API-002: OpenAPI v3.x documentation requirement.
    -   REQ-API-003: OAuth2/JWT authentication requirement.
    -   REQ-API-005: Mobile app synchronization endpoints.
    -   REQ-SADG-002: API security (HTTPS, OAuth2/JWT, OpenAPI).
    -   REQ-4-006: Mobile sync details (linked to REQ-API-005).
    -   REQ-3-006, REQ-3-008: Dynamic form sync details (linked to REQ-API-005).
    -   REQ-API-004: External farmer lookup and retrieval.
    -   REQ-DIO-009: Health check endpoint requirement.
-   **System Architecture Document**
-   **Sequence Diagrams** (especially SD-DFR-012 Mobile App Update Check and Enforcement, which implies a version check API if not covered by general sync)
-   **Odoo 18.0 Development Documentation**
-   **OpenAPI Specification v3.1.0**
-   **RFC 6749 (OAuth 2.0)**
-   **RFC 7519 (JSON Web Tokens - JWT)**

## 3. Module Architecture Overview
The DFR API Service Module (`dfr_api_services`) is designed as an Odoo 18.0 Community addon. It acts as a dedicated gateway layer, abstracting the backend services and providing a consistent, secure RESTful interface.

**Key Architectural Principles:**
-   **Modularity:** Developed as a distinct Odoo module, clearly separating API concerns.
-   **Statelessness:** API endpoints are stateless, adhering to REST principles. All necessary state for request processing is part of the request or retrieved by the server based on authenticated identity.
-   **Security:** All endpoints (except potentially the OpenAPI spec/docs and health check) require authentication (OAuth2/JWT). Authorization is enforced based on Odoo user roles and permissions. All traffic is over HTTPS.
-   **Standardization:** Uses JSON for data exchange and OpenAPI v3.x for documentation.
-   **Service-Oriented:** Controllers within this module will primarily delegate business logic to services in other DFR modules (e.g., `DFR_MOD_FARMER_REGISTRY`, `DFR_MOD_DYNAMIC_FORMS`) or its own internal services (e.g., `AuthService`).

**Interaction with other DFR Modules:**
-   **`DFR_MOD_FARMER_REGISTRY`:** For creating, reading, updating, and deleting farmer, household, and plot data.
-   **`DFR_MOD_DYNAMIC_FORMS`:** For retrieving form definitions and submitting form responses.
-   **`DFR_MOD_RBAC_CONFIG`:** For fetching user roles and permissions to enforce authorization.
-   **`DFR_MOD_SECURITY_AUDIT_LOG`:** For logging significant API access and data modification events.
-   **`DFR_MOD_CORE_COMMON`:** For any shared utilities or base model functionalities if applicable.

**Third-Party Libraries Evaluation:**
-   **PyJWT:** Will be used for JWT generation and validation.
-   **OCA `base_rest`:** This module was evaluated. While it offers good foundational features for building REST APIs in Odoo, including OpenAPI generation capabilities, the decision for this project is to implement a custom API layer to ensure tight integration with specific DFR authentication flows (OAuth2/JWT focus) and to have finer-grained control over request/response structures and error handling. However, principles and patterns from `base_rest` may inform the custom implementation.

## 4. Detailed Design

This section details the design of each file within the `dfr_addons/dfr_api_services` module.

### 4.1 `__manifest__.py`
-   **Path:** `dfr_addons/dfr_api_services/__manifest__.py`
-   **Description:** Odoo module manifest file.
-   **Purpose:** Declares the Odoo module, its version, author, dependencies, and data files. Essential for Odoo module lifecycle management.
-   **Technical Design & Logic:**
    python
    {
        'name': 'DFR API Services (Gateway)',
        'version': '18.0.1.0.0',
        'summary': 'Provides RESTful API endpoints for the Digital Farmer Registry.',
        'description': """
            Central Odoo module acting as an API Gateway, exposing secure RESTful API endpoints
            for the mobile enumerator application and authorized external systems. Handles
            request routing, authentication (OAuth2/JWT), authorization, and data
            serialization (JSON).
        """,
        'category': 'DFR/Services',
        'author': 'FAO DFR Project Team',
        'website': 'https://www.fao.org', # Placeholder
        'license': 'Apache-2.0', # Or MIT, as per project decision REQ-CM-001
        'depends': [
            'base',
            'web',
            # DFR Core Modules - actual names to be confirmed
            'dfr_common', # Assuming a common module exists
            'dfr_farmer_registry',
            'dfr_dynamic_forms',
            'dfr_rbac_config', # For role definitions used in authorization
            'dfr_security_audit_log', # For logging API actions
        ],
        'data': [
            'security/ir.model.access.csv',
            'data/ir_config_parameter_data.xml',
            'views/swagger_ui_template.xml', # If QWeb template is used for Swagger UI
            # Add other XML data files if any (e.g., for API client configuration models)
        ],
        'assets': {
            # Potentially, if Swagger UI assets are self-hosted
            # 'web.assets_backend': [
            #     'dfr_api_services/static/src/js/...',
            # ],
        },
        'application': False,
        'installable': True,
        'auto_install': False,
    }
    
    *   **Dependencies:** Ensure `dfr_common`, `dfr_farmer_registry`, `dfr_dynamic_forms`, `dfr_rbac_config`, `dfr_security_audit_log` are accurate module names.
    *   **Data files:** `ir.model.access.csv` for any models defined by this module. `ir_config_parameter_data.xml` for API related configurations. `swagger_ui_template.xml` for serving Swagger UI.

### 4.2 `__init__.py`
-   **Path:** `dfr_addons/dfr_api_services/__init__.py`
-   **Description:** Python package initializer for the `dfr_api_services` module.
-   **Purpose:** Initializes the Python package for this Odoo module, making its components (controllers, services) discoverable by Odoo.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import controllers
    from . import services
    # from . import models # if any models are defined directly in this module
    

### 4.3 `controllers/__init__.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/__init__.py`
-   **Description:** Python package initializer for the `controllers` submodule.
-   **Purpose:** Initializes the `controllers` Python package, making individual controller classes available.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import base_api_controller
    from . import auth_controller
    from . import mobile_sync_controller
    from . import external_data_controller
    from . import openapi_controller
    from . import health_controller
    

### 4.4 `controllers/base_api_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/base_api_controller.py`
-   **Description:** Base controller class for DFR API endpoints.
-   **Purpose:** Provides a common base for API controllers, ensuring consistent response structures, error handling, and shared authentication/authorization logic.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import functools
    import json
    import logging
    import werkzeug

    from odoo import http
    from odoo.http import request
    from odoo.exceptions import AccessError, UserError, ValidationError

    from ..services.auth_service import AuthService # Assuming AuthService is defined
    from ..services.api_helper import ApiHelper # Assuming ApiHelper is defined

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
                        return ApiHelper.format_error_response(
                            error_code='UNAUTHORIZED',
                            error_message='Authentication token is missing.',
                            status_code=401
                        )

                    auth_service = AuthService(request.env)
                    user = auth_service.get_user_from_token(request.env, token)

                    if not user:
                        return ApiHelper.format_error_response(
                            error_code='INVALID_TOKEN',
                            error_message='Invalid or expired authentication token.',
                            status_code=401
                        )
                    
                    # Store user in request for controllers to use
                    request.env.uid = user.id 
                    request.dfr_api_user = user

                    # Authorization check
                    if required_groups:
                        is_authorized = False
                        for group_xml_id in required_groups:
                            if user.has_group(group_xml_id):
                                is_authorized = True
                                break
                        if not is_authorized:
                            # Log the attempt
                            # AuditLogService.log_api_access_denied(...)
                            return ApiHelper.format_error_response(
                                error_code='FORBIDDEN',
                                error_message='User does not have the required permissions.',
                                status_code=403
                            )
                    
                    # Log successful access if needed by AuditLogService
                    # AuditLogService.log_api_access_success(...)
                    
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
                    _logger.warning(f"AccessError in API: {e}")
                    # AuditLogService.log_api_error(...)
                    return ApiHelper.format_error_response('FORBIDDEN', str(e), 403)
                except (UserError, ValidationError) as e:
                    _logger.warning(f"UserError/ValidationError in API: {e}")
                    # AuditLogService.log_api_error(...)
                    return ApiHelper.format_error_response('BAD_REQUEST', str(e), 400)
                except werkzeug.exceptions.NotFound:
                    _logger.info(f"Resource not found: {request.httprequest.url}")
                    return ApiHelper.format_error_response('NOT_FOUND', 'The requested resource was not found.', 404)
                except Exception as e:
                    _logger.exception(f"Unhandled exception in API controller: {e}")
                    # AuditLogService.log_api_error(...)
                    return ApiHelper.format_error_response('INTERNAL_SERVER_ERROR', 'An unexpected error occurred.', 500)
            return wrapper

        def route(self, route=None, **kw):
            """
            Override http.route to apply exception handling to all routed methods
            if they don't have a more specific handler.
            """
            def decorator(f):
                # Apply exception handling first, then the original route decorator
                handler_f = self._handle_exceptions(f)
                # Apply Odoo's routing
                return http.route(route, **kw)(handler_f)
            return decorator

    
    *   **`_authenticate_request` decorator:**
        *   Extracts 'Bearer' token from `Authorization` header.
        *   Calls `AuthService.get_user_from_token()` to validate token and get Odoo user.
        *   If `required_groups` are specified, checks if the user `has_group()` for any of them.
        *   Sets `request.dfr_api_user` for downstream use.
        *   Returns 401 or 403 errors using `ApiHelper`.
        *   Integration point for `DFR_MOD_SECURITY_AUDIT_LOG` to log access attempts.
    *   **`_handle_exceptions` decorator:**
        *   Wraps controller methods in a try-except block.
        *   Catches `AccessError`, `UserError`, `ValidationError`, `werkzeug.exceptions.NotFound`, and generic `Exception`.
        *   Uses `ApiHelper` to format standard error responses.
        *   Logs exceptions.
        *   Integration point for `DFR_MOD_SECURITY_AUDIT_LOG` to log errors.
    *   **`route` method override:** A potential pattern to automatically apply `_handle_exceptions` to all routed methods. This simplifies controller method definitions. Individual methods can still use `_authenticate_request` directly.

### 4.5 `controllers/auth_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/auth_controller.py`
-   **Description:** Odoo HTTP controller for API authentication endpoints.
-   **Purpose:** Manages API authentication, specifically the `/api/dfr/v1/auth/token` endpoint.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import json
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
                            'user_role': [group.name for group in user.groups_id] # Example, tailor as needed
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

                else:
                    # audit_log_service.log_auth_attempt(request, success=False, reason=f"Unsupported grant_type: {grant_type}")
                    return ApiHelper.format_error_response(
                        'UNSUPPORTED_GRANT_TYPE', f"Grant type '{grant_type}' is not supported.", 400
                    )
            except Exception as e:
                _logger.exception("Error in /auth/token endpoint")
                # audit_log_service.log_auth_attempt(request, success=False, reason=f"Server error: {str(e)}")
                return ApiHelper.format_error_response('INTERNAL_SERVER_ERROR', str(e), 500)

    
    *   Uses `type='http'` and `auth='public'` because authentication happens within the method. `csrf=False` as it's an API.
    *   Handles `password` grant type primarily.
    *   Calls `AuthService` for credential validation and token generation.
    *   Logs authentication attempts (success/failure) via `DFR_MOD_SECURITY_AUDIT_LOG`.

### 4.6 `controllers/mobile_sync_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/mobile_sync_controller.py`
-   **Description:** Odoo HTTP controller for mobile application data synchronization.
-   **Purpose:** Provides endpoints for the mobile app to sync farmer data, form definitions, and submissions.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import json
    import logging
    from odoo import http
    from odoo.http import request
    from .base_api_controller import BaseApiController
    from ..services.api_helper import ApiHelper
    # from odoo.addons.dfr_security_audit_log.services import audit_log_service # Example

    _logger = logging.getLogger(__name__)

    # Placeholder for required groups (XML IDs)
    ENUMERATOR_GROUP = 'dfr_rbac_config.group_dfr_enumerator' # Example, adjust as per DFR_MOD_RBAC_CONFIG

    class MobileSyncController(BaseApiController):

        @BaseApiController.route('/api/dfr/v1/sync/farmers', methods=['POST'], csrf=False)
        @BaseApiController._authenticate_request(required_groups=[ENUMERATOR_GROUP])
        def sync_farmers_data(self, **kwargs):
            """
            Handles bi-directional synchronization of farmer, household, and plot data.
            Request:
            {
                "last_sync_timestamp_server": 1678886400, // Unix timestamp of last data pulled from server
                "last_sync_timestamp_mobile": 1678886500, // Unix timestamp of last data successfully pushed to server
                "records_to_push": [ // Farmer records created/updated on mobile
                    { "local_id": "uuid-mobile-1", "operation": "create", "data": { ...farmer_data... } },
                    { "server_id": "uuid-server-2", "operation": "update", "data": { ...farmer_data_changes... } },
                    { "server_id": "uuid-server-3", "operation": "delete" }
                ]
            }
            Response:
            {
                "success": true,
                "data": {
                    "push_results": [
                        { "local_id": "uuid-mobile-1", "server_id": "new-uuid-server-1", "status": "created" },
                        { "server_id": "uuid-server-2", "status": "updated" },
                        { "server_id": "uuid-server-3", "status": "deleted" },
                        { "local_id": "uuid-mobile-x", "status": "conflict", "message": "..." }
                    ],
                    "records_to_pull": [ // Farmer records updated on server since last_sync_timestamp_server
                        { "server_id": "uuid-server-4", "data": { ... } },
                        // ...
                    ],
                    "current_server_timestamp": 1678886600
                }
            }
            """
            try:
                user = request.dfr_api_user # Set by _authenticate_request
                payload = request.jsonrequest
                last_sync_ts_server = payload.get('last_sync_timestamp_server')
                records_to_push = payload.get('records_to_push', [])
                
                # Delegate to a Farmer Sync Service (potentially in dfr_farmer_registry or a new sync service module)
                farmer_sync_service = request.env['dfr.farmer.sync.service'] # Placeholder for actual service model
                
                push_results = farmer_sync_service.process_mobile_farmer_data(user, records_to_push)
                records_to_pull, current_server_ts = farmer_sync_service.get_updated_farmer_data_for_mobile(user, last_sync_ts_server)

                # audit_log_service.log_sync_event(user, 'farmers', len(records_to_push), len(records_to_pull))
                
                return ApiHelper.format_success_response(data={
                    'push_results': push_results,
                    'records_to_pull': records_to_pull,
                    'current_server_timestamp': current_server_ts
                })
            except Exception as e: # More specific exceptions should be caught by BaseApiController._handle_exceptions
                _logger.exception("Error during farmer data sync")
                # audit_log_service.log_sync_event(user, 'farmers', error=str(e))
                # This will be caught by BaseApiController._handle_exceptions if not caught here explicitly
                raise 

        @BaseApiController.route('/api/dfr/v1/sync/form-definitions', methods=['GET'], csrf=False)
        @BaseApiController._authenticate_request(required_groups=[ENUMERATOR_GROUP])
        def sync_form_definitions(self, **kwargs):
            """
            Provides active/updated dynamic form definitions to the mobile app.
            Query Params: ?last_sync_timestamp=1678886400 (optional)
            """
            try:
                user = request.dfr_api_user
                last_sync_ts = kwargs.get('last_sync_timestamp')
                if last_sync_ts:
                    last_sync_ts = int(last_sync_ts)

                # Delegate to Dynamic Forms Service
                form_service = request.env['dfr.dynamic.form.service'] # Placeholder
                form_definitions = form_service.get_form_definitions_for_mobile(user, last_sync_ts)
                current_server_ts = form_service.get_current_server_timestamp() # Or a general utility

                # audit_log_service.log_sync_event(user, 'form_definitions', records_pulled=len(form_definitions))

                return ApiHelper.format_success_response(data={
                    'form_definitions': form_definitions,
                    'current_server_timestamp': current_server_ts
                })
            except Exception as e:
                _logger.exception("Error during form definitions sync")
                # audit_log_service.log_sync_event(user, 'form_definitions', error=str(e))
                raise

        @BaseApiController.route('/api/dfr/v1/sync/form-submissions', methods=['POST'], csrf=False)
        @BaseApiController._authenticate_request(required_groups=[ENUMERATOR_GROUP])
        def sync_form_submissions(self, **kwargs):
            """
            Receives a batch of completed dynamic form submissions from the mobile app.
            Request:
            {
                "submissions": [
                    { "local_submission_id": "uuid-mobile-sub-1", "form_definition_id": "server-form-def-uuid", "farmer_id": "server-farmer-uuid", "submission_date": "iso_timestamp", "responses": [ { "field_id": "server-field-uuid", "value": "..." } ] },
                    // ...
                ]
            }
            Response:
            {
                "success": true,
                "data": {
                    "submission_results": [
                        { "local_submission_id": "uuid-mobile-sub-1", "server_submission_id": "new-server-sub-uuid", "status": "created" },
                        { "local_submission_id": "uuid-mobile-sub-2", "status": "failed", "message": "Validation error..."}
                    ]
                }
            }
            """
            try:
                user = request.dfr_api_user
                payload = request.jsonrequest
                submissions_to_push = payload.get('submissions', [])

                # Delegate to Dynamic Forms Service
                form_service = request.env['dfr.dynamic.form.service'] # Placeholder
                submission_results = form_service.process_mobile_form_submissions(user, submissions_to_push)
                
                # audit_log_service.log_sync_event(user, 'form_submissions', records_pushed=len(submissions_to_push))
                
                return ApiHelper.format_success_response(data={
                    'submission_results': submission_results
                })
            except Exception as e:
                _logger.exception("Error during form submissions sync")
                # audit_log_service.log_sync_event(user, 'form_submissions', error=str(e))
                raise
                
        @BaseApiController.route('/api/dfr/v1/sync/app-version-check', methods=['GET'], csrf=False)
        # No specific authentication for this, or a very light one if needed.
        # Public access might be okay for version check.
        def app_version_check(self, **kwargs):
            """
            Allows the mobile app to check for the latest recommended/required version.
            Query Params: ?current_app_version=1.0.0 (optional, client's current version)
            Response:
            {
                "success": true,
                "data": {
                    "latest_version": "1.2.0",
                    "minimum_required_version": "1.1.0",
                    "update_url": "http://example.com/app.apk or store_link",
                    "is_critical_update": true, // If true, app should enforce update
                    "changelog": "New features and bug fixes..."
                }
            }
            """
            try:
                # Logic to fetch latest version info, possibly from ir.config_parameter
                # or a dedicated model for app version management.
                config_param = request.env['ir.config_parameter'].sudo()
                latest_version = config_param.get_param('dfr_api.mobile_app_latest_version', '1.0.0')
                min_required_version = config_param.get_param('dfr_api.mobile_app_min_required_version', '1.0.0')
                update_url = config_param.get_param('dfr_api.mobile_app_update_url', '')
                changelog = config_param.get_param('dfr_api.mobile_app_changelog', 'No recent updates.')
                is_critical_update = config_param.get_param('dfr_api.mobile_app_is_critical_update', 'False').lower() == 'true'

                # Compare with client's version if provided
                # client_version_str = kwargs.get('current_app_version')
                # if client_version_str:
                #    # (Parse versions and decide if `is_critical_update` should be dynamically set)
                #    pass

                return ApiHelper.format_success_response(data={
                    "latest_version": latest_version,
                    "minimum_required_version": min_required_version,
                    "update_url": update_url,
                    "is_critical_update": is_critical_update,
                    "changelog": changelog
                })
            except Exception as e:
                _logger.exception("Error during app version check")
                raise

    
    *   Each method is decorated with `@BaseApiController._authenticate_request` specifying required Odoo groups.
    *   Uses `request.jsonrequest` to get JSON payload.
    *   Delegates actual data processing to placeholder services (`dfr.farmer.sync.service`, `dfr.dynamic.form.service`). These services would reside in `DFR_MOD_FARMER_REGISTRY` and `DFR_MOD_DYNAMIC_FORMS` respectively, or a dedicated sync service module.
    *   Includes logging and audit trail integration points.
    *   `sync_farmers_data` request/response structure defined for bi-directional sync.
    *   `app_version_check` endpoint added as per SD-DFR-012 implications.

### 4.7 `controllers/external_data_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/external_data_controller.py`
-   **Description:** Odoo HTTP controller for endpoints accessed by authorized external systems.
-   **Purpose:** Exposes endpoints for external systems to query and retrieve farmer data.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import json
    import logging
    from odoo import http
    from odoo.http import request
    from .base_api_controller import BaseApiController
    from ..services.api_helper import ApiHelper
    # from odoo.addons.dfr_security_audit_log.services import audit_log_service # Example

    _logger = logging.getLogger(__name__)

    # Placeholder for required groups for external system access
    EXTERNAL_SYSTEM_GROUP = 'dfr_rbac_config.group_dfr_external_system_readonly' # Example

    class ExternalDataController(BaseApiController):

        @BaseApiController.route('/api/dfr/v1/external/farmers/lookup', methods=['GET'], csrf=False)
        @BaseApiController._authenticate_request(required_groups=[EXTERNAL_SYSTEM_GROUP])
        def lookup_farmer(self, **kwargs):
            """
            Allows authorized external systems to lookup farmer data.
            Query Params: uid, national_id, name, village, etc. (as defined in OpenAPI spec)
            """
            try:
                user = request.dfr_api_user # External system's service account user
                
                # Extract search criteria from kwargs
                search_criteria = {k: v for k, v in kwargs.items() if v} # Simple example
                
                # Delegate to Farmer Registry Service
                farmer_service = request.env['dfr.farmer.registry.service'] # Placeholder
                farmers_data, total_count = farmer_service.search_farmers_external(user, search_criteria, 
                                                                              offset=int(kwargs.get('offset', 0)), 
                                                                              limit=int(kwargs.get('limit', 20)))
                
                # audit_log_service.log_external_access(user, 'farmer_lookup', criteria=search_criteria)

                return ApiHelper.format_success_response(data={
                    'farmers': farmers_data,
                    'total_count': total_count,
                    'offset': int(kwargs.get('offset', 0)),
                    'limit': int(kwargs.get('limit', 20))
                })
            except Exception as e:
                _logger.exception("Error during external farmer lookup")
                # audit_log_service.log_external_access(user, 'farmer_lookup', error=str(e))
                raise

        @BaseApiController.route('/api/dfr/v1/external/farmers/<string:farmer_uid>', methods=['GET'], csrf=False)
        @BaseApiController._authenticate_request(required_groups=[EXTERNAL_SYSTEM_GROUP])
        def retrieve_farmer_data(self, farmer_uid, **kwargs):
            """
            Allows authorized external systems to retrieve detailed farmer data.
            Path Param: farmer_uid (the DFR UID for the farmer)
            Query Params: ?include_forms=form_def_id1,form_def_id2 (optional)
            """
            try:
                user = request.dfr_api_user
                include_forms_str = kwargs.get('include_forms')
                form_definition_ids_to_include = []
                if include_forms_str:
                    form_definition_ids_to_include = [fid.strip() for fid in include_forms_str.split(',')]

                # Delegate to service
                farmer_service = request.env['dfr.farmer.registry.service'] # Placeholder
                dynamic_form_service = request.env['dfr.dynamic.form.service'] # Placeholder
                
                farmer_data = farmer_service.get_farmer_details_external(user, farmer_uid)
                if not farmer_data:
                    return ApiHelper.format_error_response('NOT_FOUND', f"Farmer with UID {farmer_uid} not found.", 404)

                form_submissions_data = []
                if form_definition_ids_to_include and farmer_data.get('id'): # Assuming farmer_data has internal id
                    # Assuming farmer_data has the Odoo record ID for linking
                    form_submissions_data = dynamic_form_service.get_farmer_form_submissions_external(
                        user, 
                        farmer_data['id'], # This should be the Odoo record ID of the farmer
                        form_definition_ids_to_include
                    )
                
                # audit_log_service.log_external_access(user, 'farmer_retrieve', farmer_uid=farmer_uid)

                return ApiHelper.format_success_response(data={
                    'farmer_profile': farmer_data,
                    'form_submissions': form_submissions_data
                })
            except Exception as e:
                _logger.exception(f"Error retrieving data for farmer UID {farmer_uid}")
                # audit_log_service.log_external_access(user, 'farmer_retrieve', farmer_uid=farmer_uid, error=str(e))
                raise

    
    *   Endpoints protected by `_authenticate_request`, likely requiring a specific group for external systems.
    *   Delegates to services in `DFR_MOD_FARMER_REGISTRY` and `DFR_MOD_DYNAMIC_FORMS`.
    *   `retrieve_farmer_data` takes `farmer_uid` (DFR unique identifier) as path parameter.
    *   Includes pagination parameters (`offset`, `limit`) for `lookup_farmer`.
    *   Includes parameter `include_forms` for `retrieve_farmer_data` to specify which dynamic form data to fetch.

### 4.8 `controllers/openapi_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/openapi_controller.py`
-   **Description:** Odoo HTTP controller to serve OpenAPI v3.x spec and Swagger UI.
-   **Purpose:** Provides endpoints for API documentation.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import os
    import yaml # PyYAML needs to be an Odoo dependency or Python system dependency
    import json
    from odoo import http
    from odoo.http import request
    from odoo.modules import get_module_resource

    from .base_api_controller import BaseApiController # For consistent error handling if needed
    from ..services.openapi_generator import OpenApiGeneratorService
    from ..services.api_helper import ApiHelper


    class OpenApiController(http.Controller): # Does not need to inherit BaseApiController unless shared logic is useful

        @http.route('/api/dfr/v1/openapi.yaml', type='http', auth="public", methods=['GET'], csrf=False)
        def get_openapi_spec_yaml(self, **kwargs):
            try:
                generator = OpenApiGeneratorService(request.env)
                spec = generator.get_openapi_specification_yaml() # Assumes service returns YAML string
                return request.make_response(
                    spec,
                    headers=[('Content-Type', 'application/yaml')]
                )
            except Exception as e:
                return request.make_response(
                    ApiHelper.format_error_response(
                        'INTERNAL_SERVER_ERROR', 
                        f"Error generating OpenAPI YAML: {str(e)}", 
                        500).get_data(as_text=True), # Get JSON string from response
                    headers=[('Content-Type', 'application/json')],
                    status=500
                )

        @http.route('/api/dfr/v1/openapi.json', type='http', auth="public", methods=['GET'], csrf=False)
        def get_openapi_spec_json(self, **kwargs):
            try:
                generator = OpenApiGeneratorService(request.env)
                spec_dict = generator.get_openapi_specification_dict() # Assumes service returns dict
                return request.make_response(
                    json.dumps(spec_dict, indent=2),
                    headers=[('Content-Type', 'application/json')]
                )
            except Exception as e:
                 return request.make_response(
                    ApiHelper.format_error_response(
                        'INTERNAL_SERVER_ERROR', 
                        f"Error generating OpenAPI JSON: {str(e)}", 
                        500).get_data(as_text=True),
                    headers=[('Content-Type', 'application/json')],
                    status=500
                )


        @http.route('/api/dfr/v1/docs', type='http', auth="public", methods=['GET'], csrf=False)
        def swagger_ui(self, **kwargs):
            # Option 1: Render a QWeb template that loads Swagger UI
            try:
                # Assuming the OpenAPI spec is served at /api/dfr/v1/openapi.json
                # The QWeb template will point to this URL.
                return request.env['ir.ui.view']._render_template(
                    "dfr_api_services.swagger_ui_template",
                    {'openapi_spec_url': '/api/dfr/v1/openapi.json'} # or .yaml
                )
            except Exception as e:
                 # Basic error page or text response
                return request.make_response(
                    f"Error loading Swagger UI: {str(e)}",
                    headers=[('Content-Type', 'text/plain')],
                    status=500
                )
            # Option 2: Redirect to a statically hosted Swagger UI if preferred,
            # or if using a library that provides its own handler.
    
    *   Serves YAML (`/api/dfr/v1/openapi.yaml`) and JSON (`/api/dfr/v1/openapi.json`) specs.
    *   Serves Swagger UI HTML page (`/api/dfr/v1/docs`) using a QWeb template.
    *   Uses `OpenApiGeneratorService` to get the spec.

### 4.9 `controllers/health_controller.py`
-   **Path:** `dfr_addons/dfr_api_services/controllers/health_controller.py`
-   **Description:** Odoo HTTP controller for API health check.
-   **Purpose:** Provides a simple health check endpoint.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import json
    from odoo import http
    from odoo.http import request
    from .base_api_controller import BaseApiController # For consistent error handling if needed
    from ..services.api_helper import ApiHelper


    class HealthController(http.Controller): # Does not need to inherit BaseApiController

        @http.route('/api/dfr/v1/health', type='http', auth="public", methods=['GET'], csrf=False)
        def health_check(self, **kwargs):
            try:
                # Optionally, add a quick check for database connectivity
                request.env.cr.execute("SELECT 1")
                db_ok = request.env.cr.fetchone()
                if not db_ok or db_ok[0] != 1:
                    raise Exception("Database connectivity check failed")

                return ApiHelper.format_success_response(data={'status': 'UP', 'database': 'OK'})
            
            except Exception as e:
                # If inheriting BaseApiController, its _handle_exceptions would catch this.
                # Otherwise, handle explicitly:
                return ApiHelper.format_error_response(
                    'SERVICE_UNAVAILABLE', 
                    f"Health check failed: {str(e)}", 
                    503, # Service Unavailable
                    details={"status": "DOWN", "database": "ERROR"}
                )
    
    *   Simple endpoint returning `{"status": "UP"}`.
    *   Includes an optional database connectivity check.

### 4.10 `services/__init__.py`
-   **Path:** `dfr_addons/dfr_api_services/services/__init__.py`
-   **Description:** Python package initializer for the `services` submodule.
-   **Purpose:** Initializes the `services` package.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import auth_service
    from . import api_helper
    from . import openapi_generator
    # Import other service files if any
    

### 4.11 `services/auth_service.py`
-   **Path:** `dfr_addons/dfr_api_services/services/auth_service.py`
-   **Description:** Service layer for authentication logic.
-   **Purpose:** Encapsulates JWT generation, validation, and user authentication.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import jwt # PyJWT library
    import datetime
    import logging
    from odoo import api, models, fields, SUPERUSER_ID
    from odoo.exceptions import AccessDenied

    _logger = logging.getLogger(__name__)

    class AuthService:
        def __init__(self, env):
            self.env = env
            self._jwt_secret_key = self.env['ir.config_parameter'].sudo().get_param('dfr_api.jwt_secret_key', 'default-super-secret-key-replace-me')
            self._jwt_algorithm = 'HS256' # Standard algorithm
            try:
                self._access_token_expiry_seconds = int(self.env['ir.config_parameter'].sudo().get_param('dfr_api.access_token_expiry_seconds', 3600)) # 1 hour default
                self._refresh_token_expiry_seconds = int(self.env['ir.config_parameter'].sudo().get_param('dfr_api.refresh_token_expiry_seconds', 86400 * 7)) # 7 days default
            except ValueError:
                _logger.warning("Invalid JWT expiry settings in ir.config_parameter, using defaults.")
                self._access_token_expiry_seconds = 3600
                self._refresh_token_expiry_seconds = 86400 * 7


        def _generate_jwt_token(self, user_id, user_login, user_groups_xml_ids, expiry_seconds, token_type='access'):
            """Generates a JWT token for a given user ID."""
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            payload = {
                'iat': now,
                'exp': now + datetime.timedelta(seconds=expiry_seconds),
                'sub': user_id,         # Subject (user ID)
                'login': user_login,    # User login
                'groups': user_groups_xml_ids, # List of group XML IDs
                'type': token_type,     # 'access' or 'refresh'
                # Add other claims as needed, e.g., company_id, specific permissions
            }
            return jwt.encode(payload, self._jwt_secret_key, algorithm=self._jwt_algorithm)

        def generate_jwt_tokens_for_user(self, user):
            """Generates access and refresh tokens for a user."""
            user_groups_xml_ids = [group.xml_id for group in user.groups_id if group.xml_id]

            access_token = self._generate_jwt_token(
                user.id, user.login, user_groups_xml_ids, self._access_token_expiry_seconds, 'access'
            )
            refresh_token = self._generate_jwt_token(
                user.id, user.login, [], self._refresh_token_expiry_seconds, 'refresh' # Refresh token usually has fewer claims
            )
            return access_token, refresh_token, self._access_token_expiry_seconds

        def validate_and_decode_jwt_token(self, token, token_type='access'):
            """Validates and decodes a JWT token. Returns payload or None."""
            try:
                payload = jwt.decode(token, self._jwt_secret_key, algorithms=[self._jwt_algorithm])
                if payload.get('type') != token_type:
                    _logger.warning(f"Invalid token type. Expected '{token_type}', got '{payload.get('type')}'")
                    return None
                # Additional checks can be added here (e.g., check if user is still active)
                return payload
            except jwt.ExpiredSignatureError:
                _logger.info("Token has expired.")
                return None
            except jwt.InvalidTokenError as e:
                _logger.warning(f"Invalid token: {e}")
                return None

        def authenticate_user_credentials(self, login, password):
            """Authenticates Odoo user credentials."""
            try:
                # Using check_credentials directly is sensitive; ensure it's what's needed.
                # Odoo's core login uses _login which does more.
                # For API, simpler check might be okay if login() method handles it properly.
                uid = self.env['res.users']._login(self.env.cr.dbname, login, password, {'interactive': False})
                if uid:
                    return self.env['res.users'].browse(uid)
            except AccessDenied:
                _logger.info(f"Authentication failed for user {login}: AccessDenied")
            except Exception as e:
                _logger.error(f"Error during credential authentication for {login}: {e}")
            return None

        def get_user_from_token(self, env_for_user, token_string, token_type='access'):
            """Validates token and returns the Odoo user record."""
            payload = self.validate_and_decode_jwt_token(token_string, token_type)
            if payload and 'sub' in payload:
                user_id = payload['sub']
                user = env_for_user['res.users'].browse(user_id).exists()
                if user and user.active: # Ensure user is active
                    return user
                _logger.warning(f"User {user_id} from token not found or inactive.")
            return None

    
    *   Uses `PyJWT`.
    *   Configuration for secret key and expiry times fetched from `ir.config_parameter`.
    *   `generate_jwt_tokens_for_user`: Generates both access and refresh tokens. Payload includes `sub` (user ID), `iat`, `exp`, `login`, `groups` (XML IDs for easier checking in decorator), and `type`.
    *   `validate_and_decode_jwt_token`: Verifies signature, expiry, and token type.
    *   `authenticate_user_credentials`: Validates Odoo username/password. Uses `_login` for robust check.
    *   `get_user_from_token`: Decodes token and fetches the Odoo `res.users` record.

### 4.12 `services/api_helper.py`
-   **Path:** `dfr_addons/dfr_api_services/services/api_helper.py`
-   **Description:** Utility service for API controllers.
-   **Purpose:** Provides common utility functions for API response formatting and potentially request validation.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import json
    import werkzeug
    from odoo.http import Response # For Odoo 16+, for earlier request.make_response

    class ApiHelper:

        @staticmethod
        def _json_response(data, status_code=200):
            """Helper to create a JSON response."""
            return Response(
                json.dumps(data),
                content_type='application/json;charset=utf-8',
                status=status_code
            )

        @staticmethod
        def format_success_response(data=None, message=None, status_code=200, http_headers=None):
            response_data = {'success': True}
            if message:
                response_data['message'] = message
            if data is not None: # Allow data to be None, empty list, etc.
                response_data['data'] = data
            
            # For Odoo 16+, Response class is preferred
            # For older versions, use request.make_response
            # from odoo.http import request
            # return request.make_response(json.dumps(response_data), headers=http_headers or [('Content-Type', 'application/json')])
            
            return ApiHelper._json_response(response_data, status_code=status_code)


        @staticmethod
        def format_error_response(error_code, error_message, status_code, details=None, http_headers=None):
            error_payload = {
                'code': error_code,
                'message': error_message,
            }
            if details:
                error_payload['details'] = details
            
            response_data = {
                'success': False,
                'error': error_payload
            }
            # from odoo.http import request
            # return request.make_response(json.dumps(response_data), status=status_code, headers=http_headers or [('Content-Type', 'application/json')])
            return ApiHelper._json_response(response_data, status_code=status_code)

        @staticmethod
        def validate_request_payload(payload, schema_validator_func):
            """
            Validates a payload against a given schema validation function.
            schema_validator_func should be a function that takes payload and returns (is_valid, errors_dict).
            Example schema libs: Cerberus, Marshmallow, jsonschema
            """
            is_valid, errors = schema_validator_func(payload)
            return is_valid, errors
    
    *   Provides static methods `format_success_response` and `format_error_response` to create standardized JSON structures.
    *   `validate_request_payload` is a placeholder for integrating a schema validation library if needed, though for simple cases, direct checks in controllers might suffice.

### 4.13 `services/openapi_generator.py`
-   **Path:** `dfr_addons/dfr_api_services/services/openapi_generator.py`
-   **Description:** Service for generating or providing the OpenAPI spec.
-   **Purpose:** Provides the OpenAPI specification.
-   **Technical Design & Logic:**
    python
    # -*- coding: utf-8 -*-
    import os
    import yaml # Requires PyYAML
    import json
    import logging
    from odoo.modules import get_module_resource

    _logger = logging.getLogger(__name__)

    class OpenApiGeneratorService:
        _spec_dict = None # Cached spec

        def __init__(self, env):
            self.env = env
            # Path to the static OpenAPI spec file
            self._openapi_spec_path_yaml = get_module_resource('dfr_api_services', 'static', 'openapi', 'dfr_api_v1.yaml')
            self._openapi_spec_path_json = get_module_resource('dfr_api_services', 'static', 'openapi', 'dfr_api_v1.json') # If JSON preferred

        def _load_specification(self):
            """Loads the OpenAPI specification from file and caches it."""
            if OpenApiGeneratorService._spec_dict is None:
                spec_path = self._openapi_spec_path_yaml # Prioritize YAML
                use_yaml = True
                if not spec_path or not os.path.exists(spec_path):
                    spec_path = self._openapi_spec_path_json
                    use_yaml = False
                
                if not spec_path or not os.path.exists(spec_path):
                    _logger.error("OpenAPI specification file not found.")
                    raise FileNotFoundError("OpenAPI specification file not found.")
                
                try:
                    with open(spec_path, 'r', encoding='utf-8') as f:
                        if use_yaml:
                            OpenApiGeneratorService._spec_dict = yaml.safe_load(f)
                        else:
                            OpenApiGeneratorService._spec_dict = json.load(f)
                except Exception as e:
                    _logger.error(f"Error loading/parsing OpenAPI specification: {e}")
                    raise
            return OpenApiGeneratorService._spec_dict

        def get_openapi_specification_dict(self):
            """Returns the OpenAPI specification as a Python dictionary."""
            return self._load_specification()

        def get_openapi_specification_yaml(self):
            """Returns the OpenAPI specification as a YAML string."""
            spec_dict = self._load_specification()
            return yaml.dump(spec_dict, sort_keys=False)

        def get_openapi_specification_json(self):
            """Returns the OpenAPI specification as a JSON string."""
            spec_dict = self._load_specification()
            return json.dumps(spec_dict, indent=2)
    
    *   Loads the static OpenAPI spec file (`dfr_api_v1.yaml` or `dfr_api_v1.json`) from the `static/openapi/` directory.
    *   Caches the loaded spec to avoid repeated file I/O.
    *   Provides methods to get the spec as a dictionary, YAML string, or JSON string.

### 4.14 `security/ir.model.access.csv`
-   **Path:** `dfr_addons/dfr_api_services/security/ir.model.access.csv`
-   **Description:** Odoo security file for model-level access rights.
-   **Purpose:** Defines CRUD access for any custom Odoo models created within this module.
-   **Technical Design & Logic:**
    csv
    id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
    # access_dfr_api_client_config_user,dfr.api.client.config.user,model_dfr_api_client_config,base.group_user,1,0,0,0
    # access_dfr_api_client_config_admin,dfr.api.client.config.admin,model_dfr_api_client_config,base.group_system,1,1,1,1
    # (Above are examples if a model dfr.api.client.config for storing API client credentials/settings were defined in this module)
    # If no models are defined here, this file might only contain access rights for ir.config_parameter if specific groups need to manage them.
    # However, ir.config_parameter is usually managed by base.group_system.
    
    *   This file will be minimal or empty if the API gateway itself doesn't define new Odoo models for persistent storage that requires typical user/group access control. API access control is primarily handled at the controller level via authentication and RBAC checks.
    *   If models for API client registration or API key management were part of this module, their access rights would be defined here.

### 4.15 `static/src/xml/swagger_ui_template.xml` (or `views/swagger_ui_template.xml`)
-   **Path:** `dfr_addons/dfr_api_services/views/swagger_ui_template.xml` (More conventional Odoo path for views)
-   **Description:** QWeb template for rendering Swagger UI.
-   **Purpose:** Provides HTML structure for Swagger UI.
-   **Technical Design & Logic:**
    xml
    <?xml version="1.0" encoding="UTF-8"?>
    <odoo>
        <template id="swagger_ui_template" name="DFR API Swagger UI">
            <html lang="en">
                <head>
                    <meta charset="UTF-8"/>
                    <title>DFR API Documentation</title>
                    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/>
                    <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5/favicon-32x32.png"/>
                    <style>
                        html {
                            box-sizing: border-box;
                            overflow: -moz-scrollbars-vertical;
                            overflow-y: scroll;
                        }
                        *,
                        *:before,
                        *:after {
                            box-sizing: inherit;
                        }
                        body {
                            margin: 0;
                            background: #fafafa;
                        }
                    </style>
                </head>
                <body>
                    <div id="swagger-ui"></div>
                    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>
                    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
                    <script t-attf-text="true">
                        window.onload = function() {
                          // Begin Swagger UI call region
                          const ui = SwaggerUIBundle({
                            url: &quot;${openapi_spec_url}&quot;, // URL passed from controller
                            dom_id: '#swagger-ui',
                            deepLinking: true,
                            presets: [
                              SwaggerUIBundle.presets.apis,
                              SwaggerUIStandalonePreset
                            ],
                            plugins: [
                              SwaggerUIBundle.plugins.DownloadUrl
                            ],
                            layout: &quot;StandaloneLayout&quot;
                          });
                          // End Swagger UI call region
                          window.ui = ui;
                        };
                    </script>
                </body>
            </html>
        </template>
    </odoo>
    
    *   Standard HTML structure loading Swagger UI assets from a CDN (unpkg).
    *   The `openapi_spec_url` (e.g., `/api/dfr/v1/openapi.json`) is passed from the controller rendering this template.

### 4.16 `static/openapi/dfr_api_v1.yaml`
-   **Path:** `dfr_addons/dfr_api_services/static/openapi/dfr_api_v1.yaml`
-   **Description:** Static OpenAPI v3.x specification file.
-   **Purpose:** Authoritative definition of the DFR API contract.
-   **Technical Design & Logic (Snippet):**
    yaml
    openapi: 3.1.0 # As per tech stack
    info:
      title: DFR API
      version: v1.0.0
      description: API for the Digital Farmer Registry Platform
      contact:
        name: FAO DFR Project Team
        url: https://www.fao.org # Placeholder
      license:
        name: Apache 2.0 # Or MIT
        url: http://www.apache.org/licenses/LICENSE-2.0.html # Or MIT URL

    servers:
      - url: /api/dfr/v1 # Relative to the Odoo instance base URL
        description: Main DFR API Server

    components:
      securitySchemes:
        bearerAuth: # JWT Bearer Authentication
          type: http
          scheme: bearer
          bearerFormat: JWT
        # oauth2Password: # Example for OAuth2 Password Grant (can be more detailed)
        #   type: oauth2
        #   flows:
        #     password:
        #       tokenUrl: /api/dfr/v1/auth/token
        #       scopes: {} # Define scopes if used

      schemas:
        ErrorResponse:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: object
              properties:
                code:
                  type: string
                  example: "INVALID_REQUEST"
                message:
                  type: string
                  example: "The request payload is malformed."
                details:
                  type: object
                  additionalProperties: true
                  nullable: true
        
        AuthTokenRequest:
          type: object
          properties:
            grant_type:
              type: string
              enum: [password, client_credentials, refresh_token] # Extend as needed
              description: OAuth2 grant type.
            username:
              type: string
              description: User's login username (for password grant).
            password:
              type: string
              format: password
              description: User's password (for password grant).
            client_id:
              type: string
              description: OAuth2 client ID.
            client_secret:
              type: string
              description: OAuth2 client secret.
            refresh_token:
              type: string
              description: Refresh token (for refresh_token grant).
          required:
            - grant_type

        AuthTokenResponse:
          type: object
          properties:
            access_token:
              type: string
            token_type:
              type: string
              example: Bearer
            expires_in:
              type: integer
              format: int32
              description: Lifetime in seconds of the access token.
            refresh_token:
              type: string
              nullable: true
            user_id:
              type: integer # Odoo user ID
              nullable: true
            user_name:
              type: string
              nullable: true
            user_role: # Example of roles
              type: array
              items:
                type: string
              nullable: true


        FarmerRecordToPush:
          type: object
          properties:
            local_id: 
              type: string
              format: uuid
              description: Mobile app's local UUID for new records.
              nullable: true
            server_id:
              type: string
              format: uuid
              description: Server's UUID for existing records being updated/deleted.
              nullable: true
            operation:
              type: string
              enum: [create, update, delete]
            data: # Actual farmer data schema from DFR_MOD_FARMER_REGISTRY
              type: object 
              description: "Farmer data object. Schema defined by Farmer Registry module." 
              # example: { "name": "John Doe", "national_id": "12345" } 
          required:
            - operation
        
        PushResult:
          type: object
          properties:
            local_id:
              type: string
              format: uuid
              nullable: true
            server_id:
              type: string
              format: uuid
              nullable: true
            status:
              type: string
              enum: [created, updated, deleted, conflict, failed]
            message:
              type: string
              nullable: true
              description: Error or conflict message.

        FarmerRecordToPull: # Schema for farmer data pulled from server
          type: object
          properties:
            server_id:
              type: string
              format: uuid
            data: # Actual farmer data schema from DFR_MOD_FARMER_REGISTRY
              type: object 
              description: "Farmer data object. Schema defined by Farmer Registry module."

        MobileSyncFarmersRequest:
          type: object
          properties:
            last_sync_timestamp_server:
              type: integer
              format: int64
              description: Unix timestamp of last data pulled from server by this client.
            last_sync_timestamp_mobile:
              type: integer
              format: int64
              description: Unix timestamp of last data successfully pushed to server by this client.
            records_to_push:
              type: array
              items:
                $ref: '#/components/schemas/FarmerRecordToPush'
        
        MobileSyncFarmersResponse:
          type: object
          properties:
            push_results:
              type: array
              items:
                $ref: '#/components/schemas/PushResult'
            records_to_pull:
              type: array
              items:
                $ref: '#/components/schemas/FarmerRecordToPull'
            current_server_timestamp:
              type: integer
              format: int64

        # ... Other schemas for Form Definitions, Submissions, etc.

    paths:
      /auth/token:
        post:
          summary: Obtain an API access token
          tags:
            - Authentication
          operationId: DFR_API_AUTH_TOKEN
          requestBody:
            required: true
            content:
              application/x-www-form-urlencoded: # Common for token endpoints
                schema:
                  $ref: '#/components/schemas/AuthTokenRequest'
              application/json: # Also support JSON
                 schema:
                  $ref: '#/components/schemas/AuthTokenRequest'
          responses:
            '200':
              description: Successfully authenticated and token issued
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      success:
                        type: boolean
                        example: true
                      data:
                        $ref: '#/components/schemas/AuthTokenResponse'
            '400':
              description: Invalid request (e.g., missing params, unsupported grant type, invalid credentials)
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'
            '500':
              description: Internal Server Error
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'

      /sync/farmers:
        post:
          summary: Synchronize farmer data with the mobile app
          tags:
            - Mobile Sync
          operationId: DFR_API_MOBILE_SYNC_FARMERS
          security:
            - bearerAuth: [] # Requires JWT Bearer token
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/MobileSyncFarmersRequest'
          responses:
            '200':
              description: Farmer data synchronized successfully
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      success:
                        type: boolean
                        example: true
                      data:
                        $ref: '#/components/schemas/MobileSyncFarmersResponse'
            '400':
              description: Bad Request (e.g., validation errors in pushed data)
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'
            '401':
              description: Unauthorized (invalid/missing token)
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'
            '403':
              description: Forbidden (insufficient permissions)
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'
            '500':
              description: Internal Server Error
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'

      # ... Definitions for /sync/form-definitions, /sync/form-submissions
      # ... Definitions for /external/farmers/lookup, /external/farmers/{farmerId}
      # ... Definitions for /health
      # ... Definition for /sync/app-version-check

      /health:
        get:
          summary: API Health Check
          tags:
            - General
          operationId: DFR_API_HEALTH_CHECK
          responses:
            '200':
              description: API is healthy
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      success:
                        type: boolean
                        example: true
                      data:
                        type: object
                        properties:
                          status:
                            type: string
                            example: "UP"
                          database:
                            type: string
                            example: "OK" # If DB check is included
            '503':
              description: Service Unavailable (API is down or failing health checks)
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ErrorResponse'
    
    *   This is a detailed YAML file. It will define:
        *   `info`: API title, version, description.
        *   `servers`: Base URL(s).
        *   `components.schemas`: Reusable data models for requests and responses (e.g., Farmer, FormDefinition, FormSubmission, Error).
        *   `components.securitySchemes`: Definitions for `bearerAuth` (JWT) and potentially `oauth2Password`.
        *   `paths`: Each endpoint with its HTTP method, summary, tags, parameters (path, query, header), requestBody, responses (including error responses referencing common error schema), and security requirements.
    *   This file needs to be meticulously maintained to reflect the actual API.

### 4.17 `data/ir_config_parameter_data.xml`
-   **Path:** `dfr_addons/dfr_api_services/data/ir_config_parameter_data.xml`
-   **Description:** Odoo XML data file for setting API-specific system parameters.
-   **Purpose:** Provides default configuration values for API services.
-   **Technical Design & Logic:**
    xml
    <?xml version="1.0" encoding="utf-8"?>
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" means these records are only created if they don't exist -->
            
            <!-- JWT Configuration -->
            <record id="dfr_api_jwt_secret_key" model="ir.config_parameter">
                <field name="key">dfr_api.jwt_secret_key</field>
                <!-- IMPORTANT: This is a placeholder. Generate a strong, unique secret for each deployment 
                     and set it via environment variable or secure configuration management. -->
                <field name="value">!!REPLACE_THIS_IN_PRODUCTION_WITH_A_STRONG_RANDOM_SECRET_KEY!!</field>
            </record>
            <record id="dfr_api_access_token_expiry_seconds" model="ir.config_parameter">
                <field name="key">dfr_api.access_token_expiry_seconds</field>
                <field name="value">3600</field> <!-- 1 hour -->
            </record>
            <record id="dfr_api_refresh_token_expiry_seconds" model="ir.config_parameter">
                <field name="key">dfr_api.refresh_token_expiry_seconds</field>
                <field name="value">604800</field> <!-- 7 days -->
            </record>

            <!-- Mobile App Version Configuration -->
            <record id="dfr_api_mobile_app_latest_version" model="ir.config_parameter">
                <field name="key">dfr_api.mobile_app_latest_version</field>
                <field name="value">1.0.0</field>
            </record>
            <record id="dfr_api_mobile_app_min_required_version" model="ir.config_parameter">
                <field name="key">dfr_api.mobile_app_min_required_version</field>
                <field name="value">1.0.0</field>
            </record>
            <record id="dfr_api_mobile_app_update_url" model="ir.config_parameter">
                <field name="key">dfr_api.mobile_app_update_url</field>
                <field name="value"></field> <!-- e.g., Play Store link or direct APK link -->
            </record>
             <record id="dfr_api_mobile_app_is_critical_update" model="ir.config_parameter">
                <field name="key">dfr_api.mobile_app_is_critical_update</field>
                <field name="value">False</field> <!-- Set to True to force update -->
            </record>
            <record id="dfr_api_mobile_app_changelog" model="ir.config_parameter">
                <field name="key">dfr_api.mobile_app_changelog</field>
                <field name="value">Initial release.</field>
            </record>

            <!-- Add other API related configurations here -->

        </data>
    </odoo>
    
    *   Defines `ir.config_parameter` records for JWT secret, token expiry times, and mobile app versioning.
    *   **Security Note:** The `dfr_api.jwt_secret_key` must be overridden in production environments using environment variables or secure configuration files and not rely on this default.

## 5. Configuration
-   **JWT Secret Key (`dfr_api.jwt_secret_key`):** A strong, random secret key used to sign JWTs. **Must be overridden in production via environment variables or Odoo configuration file.**
-   **Access Token Expiry (`dfr_api.access_token_expiry_seconds`):** Lifetime of access tokens in seconds. Default: 3600 (1 hour).
-   **Refresh Token Expiry (`dfr_api.refresh_token_expiry_seconds`):** Lifetime of refresh tokens in seconds. Default: 604800 (7 days). (If refresh tokens are implemented).
-   **Mobile App Versioning:**
    -   `dfr_api.mobile_app_latest_version`: Latest available version of the mobile app.
    -   `dfr_api.mobile_app_min_required_version`: Minimum version required for the app to function/sync.
    -   `dfr_api.mobile_app_update_url`: URL for downloading the app update.
    -   `dfr_api.mobile_app_is_critical_update`: Boolean, if true, app might enforce update.
    -   `dfr_api.mobile_app_changelog`: Text describing changes in the latest version.
-   These parameters are managed via Odoo's System Parameters (`ir.config_parameter`) and can be set in the `ir_config_parameter_data.xml` for defaults, and overridden via the Odoo UI or configuration files for deployment-specific values.

## 6. Security Considerations
-   **Authentication:** All sensitive endpoints are protected by JWT Bearer authentication. The token generation endpoint itself might use basic auth over HTTPS or other OAuth2 flows for client authentication.
-   **Authorization:** After successful authentication, user roles and permissions (derived from Odoo groups, potentially those defined in `DFR_MOD_RBAC_CONFIG`) are checked for each request to ensure the user has the right to perform the requested operation on the requested resource. This is handled by the `_authenticate_request` decorator or similar logic.
-   **HTTPS:** All API communication MUST be over HTTPS (TLS 1.2+ enforced) to protect data in transit. This is typically handled by a reverse proxy like Nginx.
-   **Input Validation:** All incoming data from API requests (query parameters, request bodies) must be rigorously validated on the server-side to prevent injection attacks, invalid data entry, etc.
-   **Output Encoding:** Ensure JSON responses are properly encoded to prevent XSS if API responses are ever rendered directly in a browser context (though typically they are consumed by applications). Odoo's JSONRPC and `ApiHelper` should handle this.
-   **Error Handling:** Generic error messages are returned to clients, while detailed error information is logged server-side to avoid leaking sensitive system information.
-   **Rate Limiting:** Consider implementing rate limiting on API endpoints (especially public or authentication endpoints) to prevent abuse and DoS attacks. This can be done at the reverse proxy level (Nginx) or within Odoo if necessary (e.g., using OCA modules or custom logic). This is not explicitly detailed for initial implementation but is a common security best practice.
-   **Audit Logging:** Significant API events (authentication success/failure, data sync operations, errors) should be logged by integrating with `DFR_MOD_SECURITY_AUDIT_LOG`.
-   **Secrets Management:** JWT secret key and any other sensitive configuration should be managed securely, ideally outside of version control and injected via environment variables or secure configuration stores in production.

## 7. Deployment Considerations
-   This module is an Odoo addon and will be deployed as part of the DFR Odoo instance.
-   The Odoo instance should be configured behind a reverse proxy (e.g., Nginx) responsible for:
    -   SSL/TLS termination (enforcing HTTPS).
    -   Load balancing if multiple Odoo worker processes are used.
    -   Potentially, basic rate limiting or IP whitelisting for API access.
-   Ensure the `PyJWT` library is installed in the Odoo environment.
-   The OpenAPI specification file (`dfr_api_v1.yaml`) must be deployed with the module in the `static/openapi/` directory.
-   The QWeb template for Swagger UI (`swagger_ui_template.xml`) must be loaded via the manifest's data section.
-   Production JWT secret keys must be set securely and not use the default placeholder.

## 8. API Data Schemas and Flows (High-Level)

Refer to `static/openapi/dfr_api_v1.yaml` for the detailed API contract. Key flows include:

### 8.1 Authentication Flow (Password Grant Example)
1.  Client (Mobile App) POSTs `username`, `password`, `grant_type='password'` (and `client_id` if used) to `/auth/token`.
2.  `AuthController` receives the request.
3.  `AuthService.authenticate_user_credentials` validates credentials against Odoo users.
4.  If valid, `AuthService.generate_jwt_tokens_for_user` creates an access token (and optionally a refresh token).
5.  `AuthController` returns tokens to the client.

### 8.2 Mobile Data Sync Flow (Farmers Example)
1.  Mobile App (Authenticated with JWT Bearer token) POSTs to `/sync/farmers`.
    *   Request includes `last_sync_timestamp_server`, `last_sync_timestamp_mobile`, and `records_to_push` (created/updated/deleted farmer records from mobile).
2.  `MobileSyncController.sync_farmers_data` receives request.
3.  Authentication/Authorization check via `_authenticate_request`.
4.  Controller calls a service (e.g., in `DFR_MOD_FARMER_REGISTRY`) to:
    *   Process `records_to_push`:
        *   Create new farmer records in Odoo.
        *   Update existing farmer records, handling potential conflicts (e.g., based on timestamps or a defined strategy).
        *   Mark records for deletion.
    *   Fetch `records_to_pull`: Query farmer records modified on the server since `last_sync_timestamp_server` that are relevant to the authenticated enumerator (e.g., based on assigned area).
5.  Controller returns `push_results` (acknowledgements for pushed data), `records_to_pull`, and `current_server_timestamp`.
6.  Mobile app updates its local database with pulled records and stores the new `current_server_timestamp` for the next sync.

Similar flows apply to form definitions and form submissions synchronization.

### 8.3 External Farmer Lookup Flow
1.  External System (Authenticated with JWT Bearer token) GETs `/external/farmers/lookup` with query parameters (e.g., `?national_id=123`).
2.  `ExternalDataController.lookup_farmer` receives request.
3.  Authentication/Authorization check (verifying external system's permissions).
4.  Controller calls a service (e.g., in `DFR_MOD_FARMER_REGISTRY`) to search for farmers based on criteria, applying any RBAC data scoping rules for the authenticated external client.
5.  Controller returns a list of matching farmer records (selected fields only, as per permissions).

This SDS provides a comprehensive guide for the development of the DFR API Service Module. The OpenAPI specification (`dfr_api_v1.yaml`) will serve as the ground truth for API endpoint details.