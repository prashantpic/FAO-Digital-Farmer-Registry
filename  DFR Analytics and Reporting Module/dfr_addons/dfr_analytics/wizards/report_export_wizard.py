# dfr_addons/dfr_analytics/wizards/report_export_wizard.py

import io
import csv
import base64
import openpyxl # For XLSX export
import logging # For logging
import json # For handling JSON in dynamic form multiselect
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ReportExportWizard(models.TransientModel):
    _name = 'dfr.report.export.wizard'
    _description = 'DFR Report Export Wizard'

    report_type = fields.Selection([
        ('farmer_core_data', 'Farmer Core Data'),
        ('farmer_plot_data', 'Farmer Plot Data'),
        ('dynamic_form_data', 'Dynamic Form Data'),
        # Add other predefined report types here as per SDS (not explicitly detailed beyond these)
    ], string="Report Type", required=True, default="farmer_core_data",
       help="Select the type of data you want to export.")

    dynamic_form_id = fields.Many2one(
        'dfr.dynamic.form',
        string="Dynamic Form",
        help="Select the dynamic form to export data from. Required if 'Report Type' is 'Dynamic Form Data'.",
        # attrs as per SDS 5.7.5
        attrs={'invisible': [('report_type', '!=', 'dynamic_form_data')],
               'required': [('report_type', '=', 'dynamic_form_data')]}
    )

    date_from = fields.Date(string="Date From", help="Filter records created on or after this date.")
    date_to = fields.Date(string="Date To", help="Filter records created on or before this date.")

    geographic_area_ids = fields.Many2many(
        'dfr.administrative.area',  # Assuming this model exists as per SDS 5.4.2
        string="Geographic Areas",
        help="Filter records by associated administrative/geographic areas."
    )
    farmer_status_ids = fields.Many2many(
        'dfr.farmer.status',  # Assuming this model exists as per SDS 5.4.2
        string="Farmer Statuses",
        help="Filter records by farmer status."
    )

    export_format = fields.Selection([
        ('csv', 'CSV'),
        ('xlsx', 'Excel XLSX')
    ], string="Export Format", required=True, default='csv', help="Choose the format for the exported file.")

    data_file = fields.Binary(string="Exported File", readonly=True, help="The generated export file for download.")
    file_name = fields.Char(string="File Name", readonly=True, help="The name of the generated export file.")

    def action_export_report(self):
        """
        Generates and provides the report file for download based on wizard parameters.
        This method calls the 'dfr.analytics.service' to prepare data, then formats
        it into CSV or XLSX.
        """
        self.ensure_one()

        filters = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'geographic_area_ids': self.geographic_area_ids.ids,
            'farmer_status_ids': self.farmer_status_ids.ids,
        }

        # Determine the entity_type for the analytics service
        entity_type_for_service = self.report_type
        if self.report_type == 'dynamic_form_data':
            if not self.dynamic_form_id:
                raise UserError(_("Please select a Dynamic Form when 'Report Type' is 'Dynamic Form Data'."))
            # The analytics service expects a specific format for dynamic forms
            entity_type_for_service = f'dynamic_form_{self.dynamic_form_id.id}'

        # fields_to_export: SDS 5.2.2 mentions this parameter for prepare_export_data.
        # However, the wizard UI in SDS 5.7.5 doesn't include a field selector.
        # For now, we assume the analytics_service handles default fields or this will be added later.
        fields_to_export = None

        try:
            _logger.info(
                "Preparing export data for entity_type: %s with filters: %s",
                entity_type_for_service, filters
            )
            report_data_result = self.env['dfr.analytics.service'].prepare_export_data(
                entity_type_for_service,
                filters=filters,
                fields_to_export=fields_to_export
            )

            if not report_data_result:
                raise UserError(_("No data found matching the selected filters."))

            # prepare_export_data for dynamic forms returns a dict {'header': [], 'data': []}
            # For other types, it returns a list of dicts.
            if isinstance(report_data_result, dict) and 'header' in report_data_result and 'data' in report_data_result:
                header = report_data_result['header']
                data_rows = report_data_result['data'] # This should be a list of dicts
            elif isinstance(report_data_result, list):
                if not report_data_result: # Empty list
                    raise UserError(_("No data found matching the selected filters."))
                # Assuming list of dicts, derive header from keys of the first item
                header = list(report_data_result[0].keys())
                data_rows = report_data_result
            else:
                _logger.error("Unexpected data format from prepare_export_data: %s", type(report_data_result))
                raise UserError(_("An unexpected error occurred while preparing data for export."))


            file_content = None
            generated_file_name = f"{self.report_type}_{self.dynamic_form_id.name if self.report_type == 'dynamic_form_data' and self.dynamic_form_id else ''}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


            if self.export_format == 'csv':
                output = io.StringIO()
                # Ensure data_rows is a list of dicts, where keys match header
                writer = csv.DictWriter(output, fieldnames=header, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data_rows)
                file_content = output.getvalue().encode('utf-8')
                generated_file_name += ".csv"

            elif self.export_format == 'xlsx':
                workbook = openpyxl.Workbook()
                worksheet = workbook.active
                worksheet.title = "Report Data"

                # Write header
                worksheet.append(header)

                # Write data rows
                for row_dict in data_rows:
                    # Ensure values are appended in the order of the header
                    row_values = [row_dict.get(col_name, '') for col_name in header]
                    worksheet.append(row_values)

                output_xlsx = io.BytesIO()
                workbook.save(output_xlsx)
                file_content = output_xlsx.getvalue()
                generated_file_name += ".xlsx"

            self.write({
                'data_file': base64.b64encode(file_content),
                'file_name': generated_file_name,
            })
            _logger.info("Successfully generated export file: %s", generated_file_name)

        except UserError as e:
            _logger.warning("UserError during report generation: %s", e.args[0])
            raise  # Re-raise Odoo UserErrors to display them to the user
        except Exception as e:
            _logger.exception("An unexpected error occurred during report generation:")
            raise UserError(_("An unexpected error occurred during report generation. Please contact support. Details: %s") % str(e))

        # Return action to reload the wizard form view (as per SDS 5.4.2)
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }