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
        self._openapi_spec_path_json = get_module_resource('dfr_api_services', 'static', 'openapi', 'dfr_api_v1.json') # Fallback or alternative

    def _load_specification(self):
        """Loads the OpenAPI specification from file and caches it."""
        if OpenApiGeneratorService._spec_dict is None:
            spec_path = self._openapi_spec_path_yaml # Prioritize YAML
            use_yaml = True
            
            if not spec_path or not os.path.exists(spec_path):
                _logger.info(f"OpenAPI YAML specification file not found at {self._openapi_spec_path_yaml}, trying JSON.")
                spec_path = self._openapi_spec_path_json
                use_yaml = False
            
            if not spec_path or not os.path.exists(spec_path):
                _logger.error(f"OpenAPI specification file not found at {self._openapi_spec_path_yaml} or {self._openapi_spec_path_json}.")
                raise FileNotFoundError("OpenAPI specification file not found.")
            
            _logger.info(f"Loading OpenAPI specification from: {spec_path}")
            try:
                with open(spec_path, 'r', encoding='utf-8') as f:
                    if use_yaml:
                        OpenApiGeneratorService._spec_dict = yaml.safe_load(f)
                    else:
                        OpenApiGeneratorService._spec_dict = json.load(f)
            except yaml.YAMLError as e_yaml:
                _logger.error(f"Error parsing OpenAPI YAML specification: {e_yaml}")
                raise ValueError(f"Error parsing OpenAPI YAML specification: {e_yaml}")
            except json.JSONDecodeError as e_json:
                _logger.error(f"Error parsing OpenAPI JSON specification: {e_json}")
                raise ValueError(f"Error parsing OpenAPI JSON specification: {e_json}")
            except Exception as e:
                _logger.error(f"Error loading OpenAPI specification: {e}")
                raise
        return OpenApiGeneratorService._spec_dict

    def get_openapi_specification_dict(self):
        """Returns the OpenAPI specification as a Python dictionary."""
        return self._load_specification()

    def get_openapi_specification_yaml(self):
        """Returns the OpenAPI specification as a YAML string."""
        spec_dict = self._load_specification()
        try:
            return yaml.dump(spec_dict, sort_keys=False, allow_unicode=True)
        except Exception as e:
            _logger.error(f"Error converting OpenAPI spec to YAML: {e}")
            raise

    def get_openapi_specification_json(self):
        """Returns the OpenAPI specification as a JSON string."""
        spec_dict = self._load_specification()
        try:
            return json.dumps(spec_dict, indent=2)
        except Exception as e:
            _logger.error(f"Error converting OpenAPI spec to JSON: {e}")
            raise