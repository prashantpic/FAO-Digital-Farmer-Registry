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
        Supports pagination via offset and limit.
        """
        user = request.dfr_api_user # External system's service account user
        
        search_criteria = {k: v for k, v in kwargs.items() if v and k not in ['offset', 'limit', 'token']} # Filter out pagination/token params
        
        try:
            offset = int(kwargs.get('offset', 0))
            limit = int(kwargs.get('limit', 20))
        except ValueError:
            return ApiHelper.format_error_response('BAD_REQUEST', 'Offset and limit must be integers.', 400)

        # Delegate to Farmer Registry Service
        # Ensure 'dfr.farmer.registry.service' is a valid model name
        farmer_service = request.env['dfr.farmer.registry.service'] 
        farmers_data, total_count = farmer_service.search_farmers_external(user, search_criteria, 
                                                                      offset=offset, 
                                                                      limit=limit)
        
        # audit_log_service.log_external_access(user, 'farmer_lookup', criteria=search_criteria)

        return ApiHelper.format_success_response(data={
            'farmers': farmers_data,
            'total_count': total_count,
            'offset': offset,
            'limit': limit
        })

    @BaseApiController.route('/api/dfr/v1/external/farmers/<string:farmer_uid>', methods=['GET'], csrf=False)
    @BaseApiController._authenticate_request(required_groups=[EXTERNAL_SYSTEM_GROUP])
    def retrieve_farmer_data(self, farmer_uid, **kwargs):
        """
        Allows authorized external systems to retrieve detailed farmer data.
        Path Param: farmer_uid (the DFR UID for the farmer)
        Query Params: ?include_forms=form_def_id1,form_def_id2 (optional)
        """
        user = request.dfr_api_user
        include_forms_str = kwargs.get('include_forms')
        form_definition_ids_to_include = []
        if include_forms_str:
            form_definition_ids_to_include = [fid.strip() for fid in include_forms_str.split(',') if fid.strip()]

        # Delegate to services
        # Ensure 'dfr.farmer.registry.service' and 'dfr.dynamic.form.service' are valid model names
        farmer_service = request.env['dfr.farmer.registry.service'] 
        dynamic_form_service = request.env['dfr.dynamic.form.service'] 
        
        farmer_data = farmer_service.get_farmer_details_external(user, farmer_uid)
        if not farmer_data:
            # This specific error (404) is handled by _handle_exceptions if a werkzeug.exceptions.NotFound is raised
            # For a programmatic "not found" based on service result, we return it directly.
            # The BaseApiController._handle_exceptions would catch werkzeug.exceptions.NotFound,
            # but a service returning None isn't an exception itself.
            return ApiHelper.format_error_response('NOT_FOUND', f"Farmer with UID {farmer_uid} not found.", 404)

        form_submissions_data = []
        # Assuming farmer_data, if found, contains the Odoo record ID, e.g., farmer_data['id']
        # This part of the logic depends on the actual structure of farmer_data returned by the service.
        # The SDS says "farmer_data.get('id')" and "farmer_data['id']", implying it's a dict with an 'id' key.
        if form_definition_ids_to_include and farmer_data and farmer_data.get('id'): 
            farmer_odoo_id = farmer_data.get('id') 
            form_submissions_data = dynamic_form_service.get_farmer_form_submissions_external(
                user, 
                farmer_odoo_id, 
                form_definition_ids_to_include
            )
        
        # audit_log_service.log_external_access(user, 'farmer_retrieve', farmer_uid=farmer_uid)

        return ApiHelper.format_success_response(data={
            'farmer_profile': farmer_data,
            'form_submissions': form_submissions_data
        })