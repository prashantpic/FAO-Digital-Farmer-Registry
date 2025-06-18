# dfr_addons/dfr_analytics/report/farmer_data_export_reports.py

from odoo import models, fields, api, _
import datetime # For context_timestamp and report date

class FarmerStatisticsPdfReport(models.AbstractModel):
    _name = 'report.dfr_analytics.report_farmer_statistics_pdf' # Matches report_name in XML action
    _description = 'Farmer Statistics PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Prepares data for the Farmer Statistics PDF QWeb template.
        This method is called by the Odoo reporting engine.

        :param docids: List of IDs of records to report on (typically dfr.farmer IDs if called directly,
                       or can be IDs from the model specified in the ir.actions.report, e.g. wizard ID).
                       If called from a wizard that doesn't pass specific record IDs, this might be the wizard's own ID.
        :param data: Dictionary containing data passed from a wizard or action context.
                     Expected to contain 'filters' and potentially other parameters.
        :return: Dictionary of values to be passed to the QWeb template.
        """
        # Extract filters from the 'data' argument if it's passed (e.g., from a wizard)
        # The 'model' in ir.actions.report is 'dfr.report.export.wizard'.
        # So 'docids' would be the ID of the wizard instance if the report is triggered from it.
        # We need to extract filters from this wizard instance or from the 'data' dict.

        report_wizard = None
        filters = {}

        if docids and data and data.get('model') == 'dfr.report.export.wizard':
             report_wizard = self.env['dfr.report.export.wizard'].browse(docids)
             if report_wizard:
                 filters = {
                    'date_from': report_wizard.date_from,
                    'date_to': report_wizard.date_to,
                    'geographic_area_ids': report_wizard.geographic_area_ids.ids,
                    'farmer_status_ids': report_wizard.farmer_status_ids.ids,
                 }
        elif data and data.get('filters'): # Fallback if filters are directly in data
            filters = data.get('filters', {})
        
        # Fetch data using the analytics service
        analytics_service = self.env['dfr.analytics.service']
        farmer_kpis = analytics_service.get_farmer_registration_kpis(filters=filters)
        landholding_kpis = analytics_service.get_landholding_summary_kpis(filters=filters)

        # Combine KPI data
        report_data = {**farmer_kpis, **landholding_kpis}

        # The 'docs' variable in QWeb templates refers to the records being reported on.
        # If this report is a general summary based on filters, 'docs' might not be a list of farmers.
        # If the report action was bound to dfr.farmer, docids would be farmer IDs.
        # Since it's bound to the wizard (as per SDS 5.7.4), docs will be the wizard instance.
        # We pass the wizard instance as 'docs' for consistency, but the main content comes from 'report_data'.
        
        docs_for_report = report_wizard if report_wizard else self.env['dfr.report.export.wizard'] # Fallback
        
        return {
            'doc_ids': docids,
            'doc_model': 'dfr.report.export.wizard', # Model that triggered the report
            'docs': docs_for_report, # The wizard instance(s)
            'report_data': report_data,
            'filters': filters, # Pass filters to display them on the report
            'datetime': datetime, # Make datetime module available in QWeb
            # Helper for timezone conversion in QWeb, using current user's timezone
            'context_timestamp': lambda t: fields.Datetime.context_timestamp(self.with_context(tz=self.env.user.tz), t),
            'user': self.env.user,
        }