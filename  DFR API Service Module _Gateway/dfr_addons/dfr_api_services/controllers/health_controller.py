# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request
# from .base_api_controller import BaseApiController # Not inheriting as per SDS 4.9 for this controller
from ..services.api_helper import ApiHelper

_logger = logging.getLogger(__name__)

class HealthController(http.Controller): 

    @http.route('/api/dfr/v1/health', type='http', auth="public", methods=['GET'], csrf=False)
    def health_check(self, **kwargs):
        db_status = "UNKNOWN"
        try:
            # Optionally, add a quick check for database connectivity
            request.env.cr.execute("SELECT 1")
            db_ok = request.env.cr.fetchone()
            if db_ok and db_ok[0] == 1:
                db_status = "OK"
            else:
                db_status = "ERROR" # Or "DEGRADED"
                # Raise an exception to be caught and reported as 503
                raise Exception("Database connectivity check failed logic.")

            return ApiHelper.format_success_response(data={'status': 'UP', 'database': db_status})
        
        except Exception as e:
            _logger.error(f"Health check failed: {str(e)}")
            # If inheriting BaseApiController, its _handle_exceptions would catch this.
            # Otherwise, handle explicitly:
            return ApiHelper.format_error_response(
                error_code='SERVICE_UNAVAILABLE', 
                error_message=f"Health check failed: {str(e)}", 
                status_code=503, # Service Unavailable
                details={"status": "DOWN", "database": db_status if db_status != "UNKNOWN" else "ERROR"}
            )