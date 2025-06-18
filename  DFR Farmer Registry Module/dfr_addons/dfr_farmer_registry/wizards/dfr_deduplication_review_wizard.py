# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import json # For field_merge_choices_json if used
import logging

_logger = logging.getLogger(__name__)

class DfrDeduplicationReviewWizard(models.TransientModel):
    _name = 'dfr.deduplication.review.wizard'
    _description = 'DFR Deduplication Review Wizard'

    # --- Fields ---
    farmer_ids_to_review = fields.Many2many(
        'dfr.farmer',
        string='Farmers for Review Context', # Changed name for clarity - these are from context
        help="Farmers initially selected from the view for deduplication review context."
    )
    # This field will hold one specific farmer that the wizard is focused on,
    # often the one from which related potential duplicates are listed.
    selected_farmer_id = fields.Many2one(
        'dfr.farmer',
        string='Primary Farmer Under Review',
        required=True,
        domain="[('id', 'in', farmer_ids_to_review)]", # Limit selection to initial set
        help="The farmer record that is the main subject of this review session."
    )
    # This field will list potential duplicates specifically OF the selected_farmer_id
    potential_duplicate_ids_of_selected = fields.Many2many(
        'dfr.farmer',
        relation='dfr_dedup_wizard_potential_rel', # Explicit relation name
        column1='wizard_id',
        column2='farmer_id',
        string='Potential Duplicates of Primary',
        help="Potential duplicates identified for the 'Primary Farmer Under Review'."
    )
    # This field allows user to pick ONE of the potential_duplicate_ids_of_selected to compare/merge
    farmer_to_compare_merge_id = fields.Many2one(
        'dfr.farmer',
        string='Compare/Merge With This Duplicate',
        domain="[('id', 'in', potential_duplicate_ids_of_selected)]", # Must be one of the listed duplicates
        help="Select one potential duplicate record from the list above to compare or merge with the Primary Farmer."
    )
    comparison_data_html = fields.Html(
        string='Comparison Data',
        readonly=True,
        help="Side-by-side comparison of field values between Primary Farmer and the 'Compare/Merge With' record."
    )
    # master_record_selection: Simplified, the selected_farmer_id is initially master,
    # user can choose to make farmer_to_compare_merge_id the master via an action potentially.
    # For now, selected_farmer_id is the default master.
    # SDS: master_record_selection fields.Selection([('current', 'Keep Current as Master'), ('other', 'Keep Other as Master')], string="Select Master Record", default='current')
    # This is tricky with two M2Os. A simpler UI might be better. Let 'selected_farmer_id' be default master.
    # Let's retain for now and see how it fits.

    # field_merge_choices_json: For advanced field-level merge choices.
    # This would require a dynamic UI component, complex for initial version.
    # For now, merge service will use configured strategy.
    # field_merge_choices_json = fields.Text(string='Field Merge Choices (JSON)')

    # --- Default Methods ---
    @api.model
    def default_get(self, fields_list):
        res = super(DfrDeduplicationReviewWizard, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_model == 'dfr.farmer' and active_ids:
            farmers_in_context = self.env['dfr.farmer'].browse(active_ids)
            res['farmer_ids_to_review'] = [(6, 0, farmers_in_context.ids)]

            if len(farmers_in_context) == 1:
                primary_farmer = farmers_in_context[0]
                res['selected_farmer_id'] = primary_farmer.id
                # Populate potential_duplicate_ids_of_selected based on the primary farmer's links
                # This ensures the wizard opens with relevant data for a single farmer review
                res['potential_duplicate_ids_of_selected'] = [(6, 0, primary_farmer.deduplication_potential_duplicate_ids.ids)]
            elif len(farmers_in_context) > 1:
                # If multiple selected, default first one as primary. User can change.
                # Or, could have a different mode of wizard for batch review vs single deep dive.
                # For now, focus on single primary deep dive.
                res['selected_farmer_id'] = farmers_in_context[0].id
                res['potential_duplicate_ids_of_selected'] = [(6, 0, farmers_in_context[0].deduplication_potential_duplicate_ids.ids)]
                # User might need to pick one from farmer_ids_to_review as the primary subject.
        return res

    # --- Onchange Methods ---
    @api.onchange('selected_farmer_id')
    def _onchange_selected_farmer_id(self):
        if self.selected_farmer_id:
            self.potential_duplicate_ids_of_selected = [(6, 0, self.selected_farmer_id.deduplication_potential_duplicate_ids.ids)]
            self.farmer_to_compare_merge_id = False # Reset comparison target
            self.comparison_data_html = False # Clear comparison
        else:
            self.potential_duplicate_ids_of_selected = False
            self.farmer_to_compare_merge_id = False
            self.comparison_data_html = False

    @api.onchange('farmer_to_compare_merge_id')
    def _onchange_farmer_to_compare_merge_id(self):
        if self.selected_farmer_id and self.farmer_to_compare_merge_id:
            self.action_load_comparison_data()
        else:
            self.comparison_data_html = False

    # --- Action Methods ---
    def action_load_comparison_data(self):
        self.ensure_one()
        if not self.selected_farmer_id or not self.farmer_to_compare_merge_id:
            self.comparison_data_html = _("<p>Please select both a Primary Farmer and a Duplicate to compare.</p>")
            return

        master = self.selected_farmer_id
        duplicate = self.farmer_to_compare_merge_id

        # Define fields to compare (expand this list as per importance)
        # Should be configurable or based on farmer model's tracked/important fields.
        fields_to_compare = [
            'uid', 'name', 'date_of_birth', 'sex', 'contact_phone', 'contact_email',
            'national_id_type_id', 'national_id_number',
            'administrative_area_id', 'status', 'kyc_status',
            'consent_status', 'create_date', 'write_date',
            # Add more fields like education_level_id, role_in_household etc.
        ]

        html_table = """
            <div class="table-responsive">
                <table class="o_list_table table table-sm table-hover table-striped o_comparison_table">
                    <thead>
                        <tr>
                            <th class="o_comparison_header">Field</th>
                            <th class="o_comparison_header">Primary: %s (ID: %s)</th>
                            <th class="o_comparison_header">Duplicate: %s (ID: %s)</th>
                        </tr>
                    </thead>
                    <tbody>
        """ % (
            master.name or master.uid, master.id,
            duplicate.name or duplicate.uid, duplicate.id
        )

        FarmerModel = self.env['dfr.farmer']
        for field_name in fields_to_compare:
            field_obj = FarmerModel._fields.get(field_name)
            if not field_obj:
                continue

            master_val_raw = master[field_name]
            duplicate_val_raw = duplicate[field_name]

            # Use convert_to_display_name for M2O, Selection etc.
            master_display = field_obj.convert_to_display_name(master_val_raw, master) if master_val_raw else ''
            duplicate_display = field_obj.convert_to_display_name(duplicate_val_raw, duplicate) if duplicate_val_raw else ''
            
            # Simple value comparison; for M2O, it compares IDs by default.
            # For display, convert_to_display_name handles it. Raw comparison is fine here.
            is_different = master_val_raw != duplicate_val_raw
            row_class = 'table-warning font-weight-bold' if is_different else ''
            
            html_table += """
                <tr class="%s">
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
            """ % (row_class, field_obj.string or field_name, master_display, duplicate_display)

        html_table += "</tbody></table></div>"
        self.comparison_data_html = html_table
        
        # This return is for onchange calls to update the view
        return {'value': {'comparison_data_html': self.comparison_data_html}}


    def action_merge_records(self):
        """ Merges farmer_to_compare_merge_id INTO selected_farmer_id. """
        self.ensure_one()
        if not self.selected_farmer_id or not self.farmer_to_compare_merge_id:
            raise UserError(_("Please select a Primary Farmer and a Duplicate record from the list to merge."))

        master_id = self.selected_farmer_id.id
        duplicate_ids_to_merge = [self.farmer_to_compare_merge_id.id]

        _logger.info("Deduplication Wizard: Attempting to merge duplicate farmer ID %s into master farmer ID %s.",
                     duplicate_ids_to_merge, master_id)

        try:
            # field_retention_rules might be built here if an advanced UI for field selection was implemented
            # For now, it's None, relying on service's default merge strategy from config.
            merged_master_record = self.env['dfr.deduplication.service'].perform_record_merge(
                master_farmer_id=master_id,
                duplicate_farmer_ids=duplicate_ids_to_merge,
                field_retention_rules=None # json.loads(self.field_merge_choices_json) if self.field_merge_choices_json else None
            )
            
            message = _("Successfully merged Farmer %s (ID: %s) into %s (ID: %s).") % (
                self.farmer_to_compare_merge_id.name, self.farmer_to_compare_merge_id.id,
                self.selected_farmer_id.name, self.selected_farmer_id.id
            )
            # Return action to view the master record or refresh list
            # Closing the wizard and showing a notification might be enough
            self.env.user.notify_success(message=message)

            # Action to open the merged master farmer record
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'dfr.farmer',
                'res_id': merged_master_record.id,
                'view_mode': 'form',
                'target': 'main', # Open in main content area
                'flags': {'initial_mode': 'view'},
            }

        except Exception as e:
            _logger.error("Deduplication merge failed via wizard: %s", e)
            raise UserError(_("Error during merge process: %s") % str(e))


    def action_mark_as_not_duplicate(self):
        """ Marks farmer_to_compare_merge_id as NOT a duplicate of selected_farmer_id. """
        self.ensure_one()
        if not self.selected_farmer_id or not self.farmer_to_compare_merge_id:
            raise UserError(_("Please select a Primary Farmer and a specific Duplicate record from the list."))

        primary_farmer = self.selected_farmer_id
        record_to_unflag = self.farmer_to_compare_merge_id

        # Remove the 'not duplicate' record from the primary's potential duplicates list
        if record_to_unflag in primary_farmer.deduplication_potential_duplicate_ids:
            primary_farmer.write({'deduplication_potential_duplicate_ids': [(3, record_to_unflag.id)]})
            primary_farmer.message_post(body=_("Record %s (UID: %s) marked as NOT a duplicate of this farmer.") % (record_to_unflag.name, record_to_unflag.uid))
            _logger.info("Farmer %s (ID: %s) marked as NOT a duplicate of %s (ID: %s). Link removed from primary.",
                         record_to_unflag.uid, record_to_unflag.id, primary_farmer.uid, primary_farmer.id)

        # Also, remove the primary farmer from the 'not duplicate' record's potential duplicates list
        if primary_farmer in record_to_unflag.deduplication_potential_duplicate_ids:
            record_to_unflag.write({'deduplication_potential_duplicate_ids': [(3, primary_farmer.id)]})
            record_to_unflag.message_post(body=_("This farmer marked as NOT a duplicate of %s (UID: %s).") % (primary_farmer.name, primary_farmer.uid))
            _logger.info("Primary farmer %s (ID: %s) link removed from %s (ID: %s) potential duplicates.",
                         primary_farmer.uid, primary_farmer.id, record_to_unflag.uid, record_to_unflag.id)


        # If the unflagged record's status was 'potential_duplicate' AND it no longer has any potential duplicates linked,
        # revert its status.
        if record_to_unflag.status == 'potential_duplicate' and not record_to_unflag.deduplication_potential_duplicate_ids:
            # Revert to 'pending_verification' or 'active' based on KYC status
            new_status = 'active' if record_to_unflag.kyc_status == 'verified' else 'pending_verification'
            record_to_unflag.write({'status': new_status})
            record_to_unflag.message_post(body=_("Status updated to '%s' as no other potential duplicates are linked.") %
                                          dict(record_to_unflag._fields['status'].selection).get(new_status))
            _logger.info("Farmer %s (ID: %s) status updated to '%s'.", record_to_unflag.uid, record_to_unflag.id, new_status)

        # Refresh the wizard's view of potential duplicates for the primary farmer
        self.potential_duplicate_ids_of_selected = [(6, 0, primary_farmer.deduplication_potential_duplicate_ids.ids)]
        self.farmer_to_compare_merge_id = False # Clear selection
        self.comparison_data_html = False # Clear comparison view

        message = _("Farmer %s (ID: %s) has been marked as NOT a duplicate of %s (ID: %s).") % (
            record_to_unflag.name, record_to_unflag.id,
            primary_farmer.name, primary_farmer.id
        )
        self.env.user.notify_info(message=message)

        # Return a re-browse action for the wizard itself to refresh its state.
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }