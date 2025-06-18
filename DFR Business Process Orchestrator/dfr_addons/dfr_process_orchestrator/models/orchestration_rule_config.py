# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
import logging

_logger = logging.getLogger(__name__)

class OrchestrationRuleConfig(models.Model):
    _name = 'orchestration.rule.config'
    _description = 'DFR Orchestration Rule Configuration'
    _order = 'workflow_key, parameter_key'

    name = fields.Char(string='Rule Name', required=True, help="Descriptive name for this configuration rule.")
    workflow_key = fields.Char(
        string='Workflow Key',
        required=True,
        index=True,
        help="Unique key identifying the workflow this rule applies to (e.g., 'farmer_status_change', 'portal_submission_validation')."
    )
    parameter_key = fields.Char(
        string='Parameter Key',
        required=True,
        index=True,
        help="Unique key for the specific parameter within the workflow (e.g., 'active_status_notification_template_id', 'supervisor_group_id_for_portal_review')."
    )
    parameter_value = fields.Text(
        string='Parameter Value',
        help="Value of the parameter. Can be a simple string, number, or a JSON string for complex rules."
    )
    description = fields.Text(string='Description', help="Explanation of the rule and its purpose.")
    is_active = fields.Boolean(string='Active', default=True, help="Whether this configuration rule is currently active.")

    _sql_constraints = [
        ('workflow_parameter_key_uniq', 'unique (workflow_key, parameter_key)',
         'A parameter key must be unique per workflow key!')
    ]

    @api.model
    def get_config_value(self, workflow_key, parameter_key, default_value=None, expect_json=False):
        """
        Retrieves the value of a specific configuration parameter.
        :param workflow_key: The key of the workflow.
        :param parameter_key: The key of the parameter.
        :param default_value: Value to return if the parameter is not found or not active.
        :param expect_json: If True, tries to parse the value as JSON.
        :return: The parameter value, or default_value.
        """
        config_value_record = self.search([
            ('workflow_key', '=', workflow_key),
            ('parameter_key', '=', parameter_key),
            ('is_active', '=', True)
        ], limit=1)

        if config_value_record:
            value_str = config_value_record.parameter_value
            if expect_json:
                try:
                    # Ensure value_str is not None or empty before trying to load
                    if value_str:
                        return json.loads(value_str)
                    else:
                        _logger.warning(
                            "JSON config '%s/%s' is empty. Returning default.",
                            workflow_key, parameter_key
                        )
                        return default_value
                except (json.JSONDecodeError, TypeError) as e:
                    _logger.warning(
                        "Failed to parse JSON for config '%s/%s'. Value: '%s'. Error: %s. Returning default.",
                        workflow_key, parameter_key, value_str, e
                    )
                    return default_value
            return value_str
        
        _logger.debug(
            "Config value for '%s/%s' not found or inactive. Returning default value: %s",
            workflow_key, parameter_key, default_value
        )
        return default_value