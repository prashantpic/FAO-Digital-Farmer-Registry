# -*- coding: utf-8 -*-
import os
import yaml 
import json
import logging

from odoo import http
from odoo.http import request
from odoo.modules import get_module_resource

from ..services.openapi_generator import OpenApiGeneratorService
from ..services.api_helper import ApiHelper

_logger = logging.getLogger(__name__)

class OpenApiController(http.Controller):

    @http.route('/api/dfr/v1/openapi.yaml', type='http', auth="public", methods=['GET'], csrf=False)
    def get_openapi_spec_yaml(self, **kwargs):
        try:
            generator = OpenApiGeneratorService(request.env)
            spec_yaml_str = generator.get_openapi_specification_yaml()
            return request.make_response(
                spec_yaml_str,
                headers=[('Content-Type', 'application/yaml')]
            )
        except FileNotFoundError as e:
            _logger.error(f"OpenAPI YAML specification file not found: {e}")
            return ApiHelper.format_error_response(
                'NOT_FOUND', 
                "OpenAPI specification file could not be found.", 
                404
            )
        except Exception as e:
            _logger.exception(f"Error generating OpenAPI YAML: {e}")
            return ApiHelper.format_error_response(
                'INTERNAL_SERVER_ERROR', 
                f"Error generating OpenAPI YAML: {str(e)}", 
                500
            )

    @http.route('/api/dfr/v1/openapi.json', type='http', auth="public", methods=['GET'], csrf=False)
    def get_openapi_spec_json(self, **kwargs):
        try:
            generator = OpenApiGeneratorService(request.env)
            spec_dict = generator.get_openapi_specification_dict()
            spec_json_str = json.dumps(spec_dict, indent=2)
            return request.make_response(
                spec_json_str,
                headers=[('Content-Type', 'application/json')]
            )
        except FileNotFoundError as e:
            _logger.error(f"OpenAPI JSON specification file not found: {e}")
            return ApiHelper.format_error_response(
                'NOT_FOUND', 
                "OpenAPI specification file could not be found.", 
                404
            )
        except Exception as e:
            _logger.exception(f"Error generating OpenAPI JSON: {e}")
            return ApiHelper.format_error_response(
                'INTERNAL_SERVER_ERROR', 
                f"Error generating OpenAPI JSON: {str(e)}", 
                500
            )

    @http.route('/api/dfr/v1/docs', type='http', auth="public", methods=['GET'], csrf=False)
    def swagger_ui(self, **kwargs):
        try:
            # The QWeb template will use this URL to fetch the spec
            openapi_spec_url = '/api/dfr/v1/openapi.json' # Or .yaml
            
            # Ensure the template exists
            view = request.env['ir.ui.view'].sudo().search([('key', '=', 'dfr_api_services.swagger_ui_template')], limit=1)
            if not view:
                _logger.error("Swagger UI QWeb template 'dfr_api_services.swagger_ui_template' not found.")
                return request.make_response(
                    "Error: Swagger UI template not found. Please ensure the 'dfr_api_services' module is correctly installed.",
                    headers=[('Content-Type', 'text/plain')],
                    status=500
                )

            return request.env['ir.ui.view']._render_template(
                "dfr_api_services.swagger_ui_template",
                {'openapi_spec_url': openapi_spec_url}
            )
        except Exception as e:
            _logger.exception(f"Error loading Swagger UI: {e}")
            # Basic error page or text response
            return request.make_response(
                f"Error loading API Documentation: {str(e)}",
                headers=[('Content-Type', 'text/plain')],
                status=500
            )