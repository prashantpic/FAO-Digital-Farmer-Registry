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
        """
        user = request.dfr_api_user # Set by _authenticate_request
        payload = request.jsonrequest
        last_sync_ts_server = payload.get('last_sync_timestamp_server')
        # last_sync_ts_mobile = payload.get('last_sync_timestamp_mobile') # As per SDS, not explicitly used in this snippet
        records_to_push = payload.get('records_to_push', [])
        
        # Delegate to a Farmer Sync Service
        # Ensure 'dfr.farmer.sync.service' is a valid model name that provides these methods
        farmer_sync_service = request.env['dfr.farmer.sync.service'] 
        
        push_results = farmer_sync_service.process_mobile_farmer_data(user, records_to_push)
        records_to_pull, current_server_ts = farmer_sync_service.get_updated_farmer_data_for_mobile(user, last_sync_ts_server)

        # audit_log_service.log_sync_event(user, 'farmers', len(records_to_push), len(records_to_pull))
        
        return ApiHelper.format_success_response(data={
            'push_results': push_results,
            'records_to_pull': records_to_pull,
            'current_server_timestamp': current_server_ts
        })

    @BaseApiController.route('/api/dfr/v1/sync/form-definitions', methods=['GET'], csrf=False)
    @BaseApiController._authenticate_request(required_groups=[ENUMERATOR_GROUP])
    def sync_form_definitions(self, **kwargs):
        """
        Provides active/updated dynamic form definitions to the mobile app.
        Query Params: ?last_sync_timestamp=1678886400 (optional)
        """
        user = request.dfr_api_user
        last_sync_ts_str = kwargs.get('last_sync_timestamp')
        last_sync_ts = None
        if last_sync_ts_str:
            try:
                last_sync_ts = int(last_sync_ts_str)
            except ValueError:
                # Handle error or log if timestamp is not a valid integer
                _logger.warning(f"Invalid last_sync_timestamp format: {last_sync_ts_str}")
                # Potentially return a BAD_REQUEST error, or proceed without timestamp filtering

        # Delegate to Dynamic Forms Service
        # Ensure 'dfr.dynamic.form.service' is a valid model name
        form_service = request.env['dfr.dynamic.form.service'] 
        form_definitions = form_service.get_form_definitions_for_mobile(user, last_sync_ts)
        current_server_ts = form_service.get_current_server_timestamp() 

        # audit_log_service.log_sync_event(user, 'form_definitions', records_pulled=len(form_definitions))

        return ApiHelper.format_success_response(data={
            'form_definitions': form_definitions,
            'current_server_timestamp': current_server_ts
        })

    @BaseApiController.route('/api/dfr/v1/sync/form-submissions', methods=['POST'], csrf=False)
    @BaseApiController._authenticate_request(required_groups=[ENUMERATOR_GROUP])
    def sync_form_submissions(self, **kwargs):
        """
        Receives a batch of completed dynamic form submissions from the mobile app.
        """
        user = request.dfr_api_user
        payload = request.jsonrequest
        submissions_to_push = payload.get('submissions', [])

        # Delegate to Dynamic Forms Service
        # Ensure 'dfr.dynamic.form.service' is a valid model name
        form_service = request.env['dfr.dynamic.form.service'] 
        submission_results = form_service.process_mobile_form_submissions(user, submissions_to_push)
        
        # audit_log_service.log_sync_event(user, 'form_submissions', records_pushed=len(submissions_to_push))
        
        return ApiHelper.format_success_response(data={
            'submission_results': submission_results
        })
            
    @http.route('/api/dfr/v1/sync/app-version-check', type='http', auth='public', methods=['GET'], csrf=False)
    def app_version_check(self, **kwargs):
        """
        Allows the mobile app to check for the latest recommended/required version.
        This method is wrapped by _handle_exceptions if BaseApiController.route is used.
        If using http.route directly, explicit try-except might be needed for non-BaseApi errors.
        However, SDS for BaseApiController suggests overriding `route` to apply _handle_exceptions.
        For simplicity and adherence to SDS 4.6 specifying this endpoint logic directly,
        we'll use http.route and assume _handle_exceptions is not automatically applied unless
        this controller inherits BaseApiController and uses its route decorator (which it does not for this specific method as per SDS).
        If this method were to use BaseApiController.route, then _handle_exceptions would apply.
        Given it's public and simple, direct http.route is fine, explicit error handling as per SDS.
        """
        try:
            config_param = request.env['ir.config_parameter'].sudo()
            latest_version = config_param.get_param('dfr_api.mobile_app_latest_version', '1.0.0')
            min_required_version = config_param.get_param('dfr_api.mobile_app_min_required_version', '1.0.0')
            update_url = config_param.get_param('dfr_api.mobile_app_update_url', '')
            changelog = config_param.get_param('dfr_api.mobile_app_changelog', 'No recent updates.')
            is_critical_update_str = config_param.get_param('dfr_api.mobile_app_is_critical_update', 'False')
            is_critical_update = is_critical_update_str.lower() == 'true'
            
            # client_version_str = kwargs.get('current_app_version')
            # if client_version_str:
            #    # (Parse versions and decide if `is_critical_update` should be dynamically set based on client version)
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
            # This specific exception handling is if BaseApiController's _handle_exceptions is not used for this route.
            # If it were, this try-except might not be necessary here.
            return ApiHelper.format_error_response('INTERNAL_SERVER_ERROR', str(e), 500)