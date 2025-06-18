# -*- coding: utf-8 -*-
# Part of Odoo.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import logging
# Import fuzzywuzzy - ensure it's installed in the Odoo environment
try:
    from fuzzywuzzy import fuzz
except ImportError:
    _logger = logging.getLogger(__name__) # Initialize logger here if import fails early
    _logger.warning("The 'fuzzywuzzy' library is not installed. Deduplication fuzzy matching will be disabled.")
    fuzz = None # Set fuzz to None if import fails

_logger = logging.getLogger(__name__)

# Assume supporting models like dfr.national.id.type, dfr.administrative.area are available

class DfrDeduplicationService(models.AbstractModel):
    _name = 'dfr.deduplication.service'
    _description = 'DFR Deduplication Service'

    @api.model
    def get_deduplication_config(self):
        """
        Retrieves de-duplication configuration parameters.
        Falls back to reasonable defaults if parameters are not set.
        """
        IrConfigParameter = self.env['ir.config_parameter'].sudo() # Use sudo for config params

        # Helper to parse comma-separated field lists
        def parse_cs_fields(param_value):
            if not param_value:
                return []
            return [f.strip() for f in param_value.split(',') if f.strip()]

        # Helper to parse combo fields: "name,date_of_birth;contact_phone" -> [('name', 'date_of_birth'), ('contact_phone',)]
        def parse_combo_fields(param_value):
            if not param_value:
                return []
            combos = []
            for combo_str in param_value.split(';'):
                fields = tuple(f.strip() for f in combo_str.split(',') if f.strip())
                if fields:
                    combos.append(fields)
            return combos

        config = {
            'realtime_enabled': IrConfigParameter.get_param('dfr.deduplication.realtime.enabled', 'True').lower() == 'true',
            'realtime_exact_fields': parse_cs_fields(IrConfigParameter.get_param('dfr.deduplication.realtime_exact_fields', 'national_id_number')),
            'realtime_combo_fields': parse_combo_fields(IrConfigParameter.get_param('dfr.deduplication.realtime_combo_fields', 'name,date_of_birth,administrative_area_id')),
            'fuzzy_fields': { # Field name -> threshold
                'name': int(IrConfigParameter.get_param('dfr.deduplication.fuzzy.name.threshold', '85')),
                # Example for address, if relevant fields exist on farmer model directly
                # 'address_component': int(IrConfigParameter.get_param('dfr.deduplication.fuzzy.address.threshold', '70')),
            },
            'merge_strategy': IrConfigParameter.get_param('dfr.deduplication.merge_strategy', 'newest_wins'), # 'newest_wins', 'oldest_wins', 'master_wins_on_conflict'
        }
        return config

    @api.model
    def find_potential_duplicates(self, farmer_model_name_or_rs, farmer_data, current_farmer_id=None):
        """
        Finds potential duplicate farmer records based on configured rules.

        :param farmer_model_name_or_rs: The name of the farmer model ('dfr.farmer') or a recordset.
        :param farmer_data: dict of data for the farmer being checked.
        :param current_farmer_id: Optional ID of the current farmer being edited/created.
        :return: list of dict, each {'id': farmer_id, 'score': percentage_match, 'match_fields': ['field1', ...]}
        """
        if isinstance(farmer_model_name_or_rs, str):
            Farmer = self.env[farmer_model_name_or_rs]
        else: # Assumes it's a recordset
            Farmer = farmer_model_name_or_rs.browse([]) # Get empty recordset of the right model

        if Farmer._name != 'dfr.farmer':
            _logger.warning("find_potential_duplicates called with incorrect model: %s", Farmer._name)
            return []

        config = self.get_deduplication_config()
        potential_duplicates_dict = {} # Use dict to avoid adding same ID multiple times from different checks

        # 1. Build initial domain filter
        base_domain = [('status', 'not in', ('archived', 'deceased', 'merged_duplicate'))]
        if current_farmer_id:
            base_domain.append(('id', '!=', current_farmer_id))

        # 2. Check for exact matches on single configured fields
        for field_name in config['realtime_exact_fields']:
            if field_name in farmer_data and farmer_data[field_name]:
                exact_match_domain = list(base_domain)
                exact_match_domain.append((field_name, '=', farmer_data[field_name]))
                exact_matches = Farmer.search(exact_match_domain)
                for match in exact_matches:
                    if match.id not in potential_duplicates_dict:
                        potential_duplicates_dict[match.id] = {'id': match.id, 'score': 100, 'match_fields': [field_name]}
                    else: # Already found, add this field to match_fields if not present
                        if field_name not in potential_duplicates_dict[match.id]['match_fields']:
                             potential_duplicates_dict[match.id]['match_fields'].append(field_name)

        # 3. Check for exact matches on combined configured fields
        for combo in config['realtime_combo_fields']:
            combo_domain_parts = []
            valid_combo_check = True
            for field_name in combo:
                if field_name in farmer_data and farmer_data[field_name]:
                    # Special handling for m2o fields in farmer_data (they might be IDs)
                    field_obj = Farmer._fields.get(field_name)
                    if field_obj and field_obj.type == 'many2one':
                         combo_domain_parts.append((field_name, '=', farmer_data[field_name]))
                    else:
                         combo_domain_parts.append((field_name, '=', farmer_data[field_name]))
                else: # One field in combo is missing value, skip this combo for this check
                    valid_combo_check = False
                    break
            if valid_combo_check and combo_domain_parts:
                exact_combo_domain = list(base_domain) + combo_domain_parts
                exact_combo_matches = Farmer.search(exact_combo_domain)
                for match in exact_combo_matches:
                    combo_field_names = list(combo)
                    if match.id not in potential_duplicates_dict:
                        potential_duplicates_dict[match.id] = {'id': match.id, 'score': 100, 'match_fields': combo_field_names}
                    else:
                         for cf in combo_field_names:
                             if cf not in potential_duplicates_dict[match.id]['match_fields']:
                                 potential_duplicates_dict[match.id]['match_fields'].append(cf)


        # 4. Perform fuzzy matching if enabled and library available
        if fuzz and config['fuzzy_fields']:
            fuzzy_domain = list(base_domain)
            # Filter out already exact-matched records from fuzzy search
            if potential_duplicates_dict:
                 fuzzy_domain.append(('id', 'not in', list(potential_duplicates_dict.keys())))

            # Further optimize fuzzy search: e.g., match on first letter of name, or admin area
            if 'name' in farmer_data and farmer_data['name']:
                 # fuzzy_domain.append(('name', '=ilike', farmer_data['name'][0] + '%')) # Example: match first letter
                 pass # Avoid too broad searches without specific pre-filtering here
            if 'administrative_area_id' in farmer_data and farmer_data['administrative_area_id']:
                 fuzzy_domain.append(('administrative_area_id', '=', farmer_data['administrative_area_id']))

            # Limit the search results to avoid comparing against the entire database
            # A config parameter for search limit might be useful
            potential_fuzzy_candidates = Farmer.search(fuzzy_domain, limit=100) # Arbitrary limit

            for candidate in potential_fuzzy_candidates:
                candidate_match_fields = []
                total_score_weighted = 0
                total_weight = 0

                for field_name, threshold in config['fuzzy_fields'].items():
                    if field_name in farmer_data and farmer_data[field_name] and candidate[field_name]:
                        # Ensure values are strings for fuzzywuzzy
                        value1 = str(farmer_data[field_name]).lower()
                        value2 = str(candidate[field_name]).lower()
                        score = 0
                        if field_name == 'name': # Use token_set_ratio for names
                            score = fuzz.token_set_ratio(value1, value2)
                        else: # Use simple ratio for other fields
                            score = fuzz.ratio(value1, value2)

                        if score >= threshold:
                            # Simple weighting: name is more important? For now, equal weight for matched fields.
                            field_weight = 1 # Could be configured per field
                            total_score_weighted += score * field_weight
                            total_weight += field_weight
                            candidate_match_fields.append(f"{field_name} ({score}%)")

                if candidate_match_fields and total_weight > 0:
                    average_score = total_score_weighted / total_weight
                    # Add if not already found by exact match OR if fuzzy score is higher/provides more info
                    if candidate.id not in potential_duplicates_dict or potential_duplicates_dict[candidate.id]['score'] < average_score :
                        potential_duplicates_dict[candidate.id] = {
                            'id': candidate.id,
                            'score': int(average_score),
                            'match_fields': candidate_match_fields,
                        }

        # Convert dict to list and sort
        final_duplicates_list = sorted(list(potential_duplicates_dict.values()), key=lambda x: x['score'], reverse=True)
        return final_duplicates_list

    @api.model
    def perform_record_merge(self, master_farmer_id, duplicate_farmer_ids, field_retention_rules=None):
        """
        Merges duplicate farmer records into a master record.
        """
        if not master_farmer_id or not duplicate_farmer_ids:
            raise ValidationError(_("Master record and at least one duplicate record must be specified for merging."))

        Farmer = self.env['dfr.farmer']
        master_record = Farmer.browse(master_farmer_id)
        if not master_record.exists():
             raise ValidationError(_("Master record with ID %s does not exist.") % master_farmer_id)

        # Filter out master_id from duplicate_ids if present, and ensure duplicates exist
        duplicate_ids_filtered = [dup_id for dup_id in duplicate_farmer_ids if dup_id != master_farmer_id]
        duplicate_records = Farmer.browse(duplicate_ids_filtered).exists() # .exists() returns recordset of existing records

        if not duplicate_records:
            raise ValidationError(_("No valid duplicate records found to merge (IDs: %s).") % duplicate_ids_filtered)


        _logger.info("Merging duplicate farmers %s into master farmer %s (%s)", duplicate_records.ids, master_record.id, master_record.uid)

        merge_context = self.env.context.copy()
        merge_context['deduplication_merge_in_progress'] = True
        FarmerWithCtx = Farmer.with_context(merge_context)
        master_record = FarmerWithCtx.browse(master_record.id) # Re-browse with context
        duplicate_records = FarmerWithCtx.browse(duplicate_records.ids)


        config = self.get_deduplication_config()
        retention_rules = field_retention_rules or {}
        master_vals_to_update = {}

        all_involved_records = master_record | duplicate_records

        for field_name, field_obj in master_record._fields.items():
            if field_obj.type in ('one2many', 'many2many') or field_obj.compute or field_obj.related or \
               field_obj.readonly and field_name not in retention_rules or \
               field_name in ('id', 'uid', 'company_id', 'active', '__last_update',
                               'create_date', 'create_uid', 'write_date', 'write_uid',
                               'deduplication_master_farmer_id', 'deduplication_potential_duplicate_ids',
                               'message_ids', 'message_follower_ids', 'activity_ids'): # Skip technical/relational/log fields
                continue

            # Gather values from all records for this field
            values_map = {rec.id: rec[field_name] for rec in all_involved_records}
            distinct_values = set(v for v in values_map.values() if v or isinstance(v, (bool, int, float))) # Consider False/0 as values

            if len(distinct_values) <= 1 and master_record[field_name] in distinct_values: # No conflict or master has the only value
                continue

            # Conflict exists or master value is empty and duplicates have values
            chosen_value = master_record[field_name] # Default to master's current value
            chosen_value_source_rec = master_record

            rule = retention_rules.get(field_name, config['merge_strategy'])

            if rule == 'master_wins_on_conflict':
                if master_record[field_name]: # Master has a value, keep it
                    chosen_value = master_record[field_name]
                else: # Master is empty, pick newest non-empty from duplicates
                    newest_rec_with_value = duplicate_records.filtered(lambda r: r[field_name]).sorted(key='write_date', reverse=True)
                    if newest_rec_with_value:
                        chosen_value = newest_rec_with_value[0][field_name]
                        chosen_value_source_rec = newest_rec_with_value[0]

            elif rule == 'newest_wins':
                newest_rec_with_value = all_involved_records.filtered(lambda r: r[field_name] or isinstance(r[field_name], (bool,int,float))).sorted(key='write_date', reverse=True)
                if newest_rec_with_value:
                    chosen_value = newest_rec_with_value[0][field_name]
                    chosen_value_source_rec = newest_rec_with_value[0]

            elif rule == 'oldest_wins':
                oldest_rec_with_value = all_involved_records.filtered(lambda r: r[field_name] or isinstance(r[field_name], (bool,int,float))).sorted(key='write_date', reverse=False)
                if oldest_rec_with_value:
                    chosen_value = oldest_rec_with_value[0][field_name]
                    chosen_value_source_rec = oldest_rec_with_value[0]

            elif isinstance(rule, int) and rule in all_involved_records.ids: # Explicitly choose from specific record ID
                record_to_take_value_from = all_involved_records.filtered(lambda r: r.id == rule)
                if record_to_take_value_from:
                    chosen_value = record_to_take_value_from[field_name]
                    chosen_value_source_rec = record_to_take_value_from

            # Update master if chosen value is different and comes from a different record or rule forces it
            if chosen_value != master_record[field_name] or chosen_value_source_rec != master_record:
                master_vals_to_update[field_name] = chosen_value


        if master_vals_to_update:
             _logger.info("Updating master farmer %s with merged fields: %s", master_record.id, master_vals_to_update)
             master_record.write(master_vals_to_update)

        # Re-parent related records
        # This is a critical and complex part. Need to handle based on specific relations.
        # Example for O2M and M2M fields:
        # For M2M, usually 'adding' values from duplicates to master is safe.
        # For O2M, it's re-assigning the foreign key on the 'many' side.

        # For mail.followers and mail.activity
        # Odoo's merge wizard helper `_merge_method` in `mail.thread` can be an inspiration
        # For simplicity here: try to move followers. Activities are harder to just "move".
        all_follower_ids = set()
        for rec in all_involved_records:
            all_follower_ids.update(rec.message_follower_ids.mapped('partner_id.id')) # Get partner_ids
        if all_follower_ids:
             master_record.message_subscribe(partner_ids=list(all_follower_ids))


        # Handle specific relational fields defined in SDS (this is a simplified example)
        # This should be dynamic based on model relations or explicitly listed
        relations_to_reparent = {
            'dfr.household_member': 'farmer_id',
            'dfr.farm': 'farmer_id',
            # For other models (e.g. dfr.plot might link to farmer directly, dfr.survey_answer etc.)
        }
        for model_name, field_to_update in relations_to_reparent.items():
            RelatedModel = self.env[model_name].with_context(merge_context)
            records_to_move = RelatedModel.search([(field_to_update, 'in', duplicate_records.ids)])
            if records_to_move:
                try:
                    # Check for potential unique constraint violations before write
                    # e.g., if a household_member can only be linked to one household and farmer pair
                    records_to_move.write({field_to_update: master_record.id})
                    _logger.info("Moved %s records of %s from duplicates to master %s", len(records_to_move), model_name, master_record.id)
                except Exception as e:
                    _logger.error("Error moving %s records for master %s: %s. Manual review might be needed.", model_name, master_record.id, e)
                    # Potentially raise UserError to stop merge if critical

        # Log merge event in chatter
        merge_log_message = _("This record is now the master record. Merged from duplicates: %s (UIDs: %s).") % (
            ", ".join(duplicate_records.mapped('name')),
            ", ".join(duplicate_records.mapped('uid'))
        )
        master_record.message_post(body=merge_log_message)

        # Deactivate duplicates
        for dup_rec in duplicate_records:
            dup_rec.message_post(body=_("This record has been merged into master farmer: %s (UID: %s). This record is now archived.") % (master_record.name, master_record.uid))
            dup_rec.write({
                'status': 'merged_duplicate', # Special status for merged records
                'active': False, # Assuming standard Odoo active field for archiving
                'deduplication_master_farmer_id': master_record.id,
            })
        _logger.info("Duplicate farmers %s successfully merged into master %s and archived.", duplicate_records.ids, master_record.id)

        return master_record