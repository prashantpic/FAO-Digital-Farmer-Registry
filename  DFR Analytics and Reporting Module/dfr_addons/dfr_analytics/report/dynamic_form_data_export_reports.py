# dfr_addons/dfr_analytics/report/dynamic_form_data_export_reports.py

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime # For context_timestamp and report date

class DynamicFormSummaryPdfReport(models.AbstractModel):
    _name = 'report.dfr_analytics.report_dynamic_form_summary_pdf' # Matches report_name in XML action
    _description = 'Dynamic Form Submission Summary PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Prepares data for the Dynamic Form Summary PDF QWeb template.
        This method is called by the Odoo reporting engine.

        :param docids: List of IDs of records to report on (typically dfr.report.export.wizard IDs).
        :param data: Dictionary containing data passed from a wizard or action context.
        :return: Dictionary of values to be passed to the QWeb template.
        """
        report_wizard = None
        filters = {}
        form_id_for_report = None
        form_record = None

        if docids and data and data.get('model') == 'dfr.report.export.wizard':
            report_wizard = self.env['dfr.report.export.wizard'].browse(docids)
            if report_wizard:
                if not report_wizard.dynamic_form_id and report_wizard.report_type == 'dynamic_form_data':
                    # SDS doesn't specify PDF for "all forms", assuming one specific form is chosen via wizard.
                    # The wizard view for PDF reports might need modification if "all forms" summary is required.
                    # For now, we expect a dynamic_form_id to be selected on the wizard for this PDF.
                    raise UserError(_("Please select a specific Dynamic Form in the wizard to generate this PDF summary."))
                
                form_id_for_report = report_wizard.dynamic_form_id.id if report_wizard.dynamic_form_id else None
                form_record = report_wizard.dynamic_form_id
                
                filters = {
                    'date_from': report_wizard.date_from,
                    'date_to': report_wizard.date_to,
                    'geographic_area_ids': report_wizard.geographic_area_ids.ids,
                    'farmer_status_ids': report_wizard.farmer_status_ids.ids, # These may or may not apply to form submissions directly
                                                                              # The analytics service needs to handle how these filters apply
                }
        elif data and data.get('form_id'): # Fallback if form_id is directly in data (less likely with wizard model)
            form_id_for_report = data.get('form_id')
            form_record = self.env['dfr.dynamic.form'].browse(form_id_for_report) if form_id_for_report else None
            filters = data.get('filters', {})
        else:
             # This report is expected to be called from the wizard with a form selected.
             raise UserError(_("This report must be generated via the Report Export Wizard with a Dynamic Form selected."))


        if not form_id_for_report:
            raise UserError(_("No Dynamic Form specified for the summary report. Please select a form in the wizard."))

        # Fetch data using the analytics service
        analytics_service = self.env['dfr.analytics.service']
        submission_kpis = analytics_service.get_dynamic_form_submission_kpis(
            form_id=form_id_for_report,
            filters=filters
        )
        
        docs_for_report = report_wizard if report_wizard else self.env['dfr.report.export.wizard']

        return {
            'doc_ids': docids,
            'doc_model': 'dfr.report.export.wizard', # Model that triggered the report
            'docs': docs_for_report, # The wizard instance(s)
            'report_data': submission_kpis,
            'filters': filters, # Pass filters to display them on the report
            'form': form_record, # Pass the dynamic form record itself
            'datetime': datetime, # Make datetime module available in QWeb
            'context_timestamp': lambda t: fields.Datetime.context_timestamp(self.with_context(tz=self.env.user.tz), t),
            'user': self.env.user,
        }