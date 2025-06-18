# dfr_addons/dfr_analytics/models/analytics_service.py
import logging
import json
from datetime import datetime, date, timedelta
from collections import defaultdict

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AnalyticsService(models.AbstractModel):
    _name = 'dfr.analytics.service'
    _description = 'DFR Analytics Data Service'

    @api.model
    def _build_common_domain(self, filters, date_field='create_date'):
        """
        Constructs a common Odoo domain based on provided filters.
        :param filters: dict, filters to apply.
                        Expected keys: 'date_from', 'date_to',
                                       'geographic_area_ids', 'farmer_status_ids'
        :param date_field: str, name of the date field to filter on.
        :return: list, Odoo domain.
        """
        domain = []
        if filters:
            if filters.get('date_from'):
                domain.append((date_field, '>=', filters['date_from']))
            if filters.get('date_to'):
                # Inclusive of the 'date_to'
                date_to_dt = fields.Date.from_string(filters['date_to'])
                domain.append((date_field, '<=', date_to_dt))
            if filters.get('geographic_area_ids'):
                # Assuming 'administrative_area_id' is the field on farmer/plot linking to dfr.administrative.area
                # This might need adjustment if the field name or logic is different
                # For plots, it could be plot.farmer_id.administrative_area_id
                # For submissions, it could be submission.farmer_id.administrative_area_id
                # This current filter might be too simplistic for related models.
                # For now, assuming a direct link or the caller handles specific model paths.
                domain.append(('administrative_area_id', 'in', filters['geographic_area_ids']))
            if filters.get('farmer_status_ids'):
                 # Assuming 'farmer_status_id' is the field on dfr.farmer
                 # This filter primarily applies to farmer-centric queries.
                 domain.append(('farmer_status_id', 'in', filters['farmer_status_ids']))
        return domain

    @api.model
    def get_farmer_registration_kpis(self, filters=None):
        """
        Fetches data for farmer registration KPIs as per SDS 5.2.2.
        """
        Farmer = self.env['dfr.farmer']
        domain = self._build_common_domain(filters, date_field='registration_date') # Assuming 'registration_date' or 'create_date'

        total_registrations = Farmer.search_count(domain)

        # Gender disaggregation (assuming 'gender' selection field on dfr.farmer)
        gender_read_group = Farmer.read_group(domain, ['gender'], ['gender'])
        gender_disaggregation = {
            item['gender'][1] if isinstance(item['gender'], tuple) else item['gender'] or _('Undefined'): item['gender_count']
            for item in gender_read_group if item.get('gender') # Ensure gender exists
        }

        # Age distribution (assuming 'date_of_birth' field)
        age_distribution = defaultdict(int)
        age_groups = { # Define age groups (upper bound exclusive, lower bound inclusive)
            _('0-17'): (0, 18),
            _('18-25'): (18, 26),
            _('26-35'): (26, 36),
            _('36-45'): (36, 46),
            _('46-55'): (46, 56),
            _('56-65'): (56, 66),
            _('66+'): (66, 150), # Assuming max age
            _('Undefined Age'): (None, None)
        }
        farmers_with_dob = Farmer.search_read(domain, ['date_of_birth'], limit=10000) # Limit for performance, consider batching for very large sets
        today = date.today()
        for farmer_data in farmers_with_dob:
            dob = farmer_data.get('date_of_birth')
            age = None
            if dob:
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            found_group = False
            for group_name, (min_age, max_age) in age_groups.items():
                if group_name == _('Undefined Age'): continue # Handle this last
                if min_age is not None and max_age is not None and age is not None and min_age <= age < max_age:
                    age_distribution[group_name] += 1
                    found_group = True
                    break
            if not found_group:
                age_distribution[_('Undefined Age')] +=1


        # Registration trends (group by month on 'registration_date' or 'create_date')
        trend_domain = domain[:] # Create a copy
        # Ensure we only process if there's a valid date field for grouping
        # The specific date field for trends needs to be consistent (e.g., 'registration_date')
        # Using DATE_TRUNC depends on PostgreSQL
        trend_read_group = Farmer.read_group(
            trend_domain,
            ['id', 'registration_date:month'],
            ['registration_date:month'],
            orderby='registration_date:month'
        )
        registration_trends = [
            {'period': item['registration_date:month'], 'count': item['registration_date_count']}
            for item in trend_read_group if item.get('registration_date:month')
        ]


        return {
            'total_registrations': total_registrations,
            'gender_disaggregation': dict(gender_disaggregation),
            'age_distribution': dict(age_distribution),
            'registration_trends': registration_trends,
        }

    @api.model
    def get_landholding_summary_kpis(self, filters=None):
        """
        Fetches data for landholding summary KPIs as per SDS 5.2.2.
        Filters here might apply to farmers, and then we find their plots.
        """
        Plot = self.env['dfr.plot']
        farmer_domain = self._build_common_domain(filters, date_field='farmer_id.registration_date') # Filter farmers
        farmer_ids = self.env['dfr.farmer'].search(farmer_domain).ids
        plot_domain = [('farmer_id', 'in', farmer_ids)]


        # Total plots and land area
        plot_data = Plot.read_group(plot_domain, ['plot_size'], ['farmer_id']) # Group by farmer to sum plot sizes
                                                                               # Then sum these sums if needed, or simply sum all plot_size
        all_plots_data = Plot.search_read(plot_domain, ['plot_size'])
        total_plots = len(all_plots_data)
        total_land_area = sum(p['plot_size'] or 0.0 for p in all_plots_data)
        average_plot_size = (total_land_area / total_plots) if total_plots > 0 else 0.0

        # Land distribution by size
        land_distribution = defaultdict(int)
        size_groups = { # Define size groups in hectares (upper bound exclusive)
            _('<0.5 Ha'): (0, 0.5),
            _('0.5-1 Ha'): (0.5, 1.0),
            _('1-2 Ha'): (1.0, 2.0),
            _('2-5 Ha'): (2.0, 5.0),
            _('5-10 Ha'): (5.0, 10.0),
            _('10+ Ha'): (10.0, float('inf')),
            _('Undefined Size'): (None, None)
        }
        for plot_item in all_plots_data:
            size = plot_item.get('plot_size')
            found_group = False
            for group_name, (min_size, max_size) in size_groups.items():
                if group_name == _('Undefined Size'): continue
                if min_size is not None and max_size is not None and size is not None and min_size <= size < max_size:
                    land_distribution[group_name] += 1
                    found_group = True
                    break
            if not found_group:
                land_distribution[_('Undefined Size')] += 1

        return {
            'total_plots': total_plots,
            'total_land_area': round(total_land_area, 2),
            'average_plot_size': round(average_plot_size, 2),
            'land_distribution_by_size': dict(land_distribution),
        }

    @api.model
    def get_dynamic_form_submission_kpis(self, form_id=None, filters=None):
        """
        Fetches data for dynamic form submission KPIs as per SDS 5.2.2.
        Filters will apply to submissions, potentially via farmer linkage.
        """
        Submission = self.env['dfr.form.submission']
        Form = self.env['dfr.dynamic.form']
        Response = self.env['dfr.form.response']

        # Build domain for submissions. Filters might relate to farmer props.
        # Example: if filters are farmer-based, find relevant farmers first.
        base_submission_domain = []
        if filters:
            farmer_domain_for_filters = self._build_common_domain(filters, date_field='farmer_id.registration_date')
            if farmer_domain_for_filters: # If any farmer-specific filters are active
                relevant_farmer_ids = self.env['dfr.farmer'].search(farmer_domain_for_filters).ids
                base_submission_domain.append(('farmer_id', 'in', relevant_farmer_ids))
            # Direct date filters for submissions if applicable (e.g. submission date)
            if filters.get('date_from'):
                base_submission_domain.append(('submission_date', '>=', filters['date_from'])) # Assuming 'submission_date' field
            if filters.get('date_to'):
                base_submission_domain.append(('submission_date', '<=', filters['date_to']))


        submission_domain = list(base_submission_domain) # Make a copy
        if form_id:
            submission_domain.append(('dynamic_form_id', '=', form_id))

        total_submissions = Submission.search_count(submission_domain)
        form_name = _('All Forms')
        specific_form_instance = None
        if form_id:
            specific_form_instance = Form.browse(form_id)
            if specific_form_instance.exists():
                form_name = specific_form_instance.name
            else:
                 raise UserError(_("Dynamic Form with ID %s not found.") % form_id)


        submissions_per_form = {}
        if not form_id: # Overview for all forms
            form_read_group_domain = list(base_submission_domain)
            form_read_group = Submission.read_group(
                form_read_group_domain,
                ['dynamic_form_id'],
                ['dynamic_form_id']
            )
            submissions_per_form = {
                item['dynamic_form_id'][1]: item['dynamic_form_id_count'] # [1] is the name
                for item in form_read_group if item.get('dynamic_form_id')
            }

        response_distribution = {}
        if form_id and specific_form_instance:
            submission_ids = Submission.search(submission_domain).ids
            # Find selection fields for this form
            selection_fields = specific_form_instance.field_ids.filtered(
                lambda f: f.field_type in ['selection', 'multiselection'])

            for field_def in selection_fields:
                field_responses = defaultdict(int)
                # Query responses for this field across relevant submissions
                responses_data = Response.search_read(
                    [('submission_id', 'in', submission_ids), ('form_field_id', '=', field_def.id)],
                    ['value']
                )
                for res_data in responses_data:
                    value = res_data.get('value')
                    if field_def.field_type == 'multiselection':
                        try:
                            # Assuming multiselection stores as JSON list string: '["val1", "val2"]'
                            parsed_values = json.loads(value) if value and isinstance(value, str) else []
                            if isinstance(parsed_values, list):
                                for v_item in parsed_values:
                                    field_responses[v_item or _('Empty')] += 1
                            else: # Not a list, treat as single value
                                field_responses[parsed_values or _('Empty')] += 1
                        except json.JSONDecodeError:
                            # If not JSON, treat as a single string value (could be comma-separated by convention)
                            field_responses[value or _('Empty')] += 1
                    else: # selection
                        field_responses[value or _('Empty')] += 1
                response_distribution[field_def.field_label or field_def.field_name] = dict(field_responses)

        return {
            'total_submissions': total_submissions,
            'submissions_per_form': submissions_per_form, # Populated if form_id is None
            'response_distribution': response_distribution, # Populated if form_id is provided
            'form_name': form_name,
        }

    @api.model
    def get_farmer_plot_geo_data(self, filters=None):
        """
        Fetches farmer homestead and plot geographical data as per SDS 5.2.2.
        Filters apply to farmers.
        """
        Farmer = self.env['dfr.farmer']
        Plot = self.env['dfr.plot']

        farmer_domain = self._build_common_domain(filters, date_field='registration_date')
        farmers = Farmer.search(farmer_domain)

        geo_data = []
        # Farmer homesteads (assuming gps_longitude, gps_latitude fields on dfr.farmer)
        for farmer in farmers.filtered(lambda f: f.gps_latitude and f.gps_longitude):
            geo_data.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [farmer.gps_longitude, farmer.gps_latitude]},
                'properties': {
                    'id': farmer.id,
                    'farmer_uid': farmer.farmer_uid,
                    'name': farmer.name,
                    'type': 'farmer_homestead',
                    'popup': f"<strong>{_('Farmer')}:</strong> {farmer.name}<br/><strong>UID:</strong> {farmer.farmer_uid}"
                }
            })

        # Plots (assuming geojson_polygon or gps_longitude/latitude on dfr.plot)
        plot_ids = Plot.search([('farmer_id', 'in', farmers.ids)])
        for plot in plot_ids:
            properties = {
                'id': plot.id,
                'plot_uid': plot.plot_uid,
                'farmer_name': plot.farmer_id.name if plot.farmer_id else _('N/A'),
                'plot_size': plot.plot_size or 0.0,
                'type': 'plot',
            }
            properties['popup'] = f"<strong>{_('Plot')}:</strong> {plot.plot_uid or _('N/A')}<br/>" \
                                  f"<strong>{_('Farmer')}:</strong> {properties['farmer_name']}<br/>" \
                                  f"<strong>{_('Size (Ha)')}:</strong> {properties['plot_size']}"

            geometry = None
            if plot.geojson_polygon:
                try:
                    geometry_data = json.loads(plot.geojson_polygon)
                    # Basic validation of GeoJSON structure for Polygon
                    if isinstance(geometry_data, dict) and \
                       geometry_data.get('type') == 'Polygon' and \
                       isinstance(geometry_data.get('coordinates'), list):
                        geometry = geometry_data
                    else:
                        _logger.warning("Invalid GeoJSON Polygon structure for plot %s: %s", plot.id, plot.geojson_polygon)
                except json.JSONDecodeError:
                    _logger.warning("Failed to parse GeoJSON for plot %s: %s", plot.id, plot.geojson_polygon)
            elif plot.gps_latitude and plot.gps_longitude: # Fallback to point if no polygon
                geometry = {'type': 'Point', 'coordinates': [plot.gps_longitude, plot.gps_latitude]}

            if geometry:
                 geo_data.append({
                     'type': 'Feature',
                     'geometry': geometry,
                     'properties': properties
                 })
        return geo_data


    @api.model
    def prepare_export_data(self, entity_type, filters=None, fields_to_export=None):
        """ Prepares data for CSV/XLSX export as per SDS 5.2.2. """
        header = []
        data_rows_list_of_dicts = []

        # Common filter logic based on entity type might be complex
        # For simplicity, apply general filters and let entity-specific logic refine if needed.
        # This will be tricky as filters (e.g., farmer_status_ids) are farmer-centric.
        # We need to correctly apply them to plots or submissions related to those farmers.

        if entity_type == 'farmer_core_data':
            Model = self.env['dfr.farmer']
            domain = self._build_common_domain(filters, date_field='registration_date')
            default_fields = ['farmer_uid', 'name', 'gender', 'date_of_birth', 'contact_phone', 'registration_date', 'farmer_status_id.name', 'administrative_area_id.display_name']
            fields_to_read = fields_to_export or default_fields
            
            # For header, get field descriptions
            field_objects = {fname: Model._fields[fname] for fname in fields_to_read if '.' not in fname and fname in Model._fields}
            header = [field_objects[fname].string if fname in field_objects else fname.replace('_', ' ').title() for fname in fields_to_read]
            
            records = Model.search_read(domain, fields_to_read)
            # Post-process many2one fields [id, name] to just name, and format dates/datetimes
            for rec in records:
                for f_name in fields_to_read:
                    if isinstance(rec.get(f_name), tuple) and len(rec[f_name]) == 2: # m2o field
                        rec[f_name] = rec[f_name][1] # Get name part
                    elif isinstance(rec.get(f_name), (datetime, date)):
                        rec[f_name] = fields.Datetime.to_string(rec[f_name]) if isinstance(rec[f_name], datetime) else fields.Date.to_string(rec[f_name])
            data_rows_list_of_dicts = records


        elif entity_type == 'farmer_plot_data':
            PlotModel = self.env['dfr.plot']
            farmer_domain = self._build_common_domain(filters, date_field='farmer_id.registration_date')
            relevant_farmer_ids = self.env['dfr.farmer'].search(farmer_domain).ids
            plot_domain = [('farmer_id', 'in', relevant_farmer_ids)]

            default_fields = ['plot_uid', 'farmer_id.name', 'plot_size', 'land_tenure_type', 'primary_crop', 'gps_latitude', 'gps_longitude', 'create_date']
            fields_to_read = fields_to_export or default_fields

            field_objects_plot = {fname: PlotModel._fields[fname] for fname in fields_to_read if '.' not in fname and fname in PlotModel._fields}
            # For related fields, we might need to introspect further or use hardcoded labels
            header = []
            for fname in fields_to_read:
                if '.' in fname: # e.g. farmer_id.name
                    parts = fname.split('.')
                    # This is simplified; proper related field label fetching is more complex
                    header.append(f"{parts[0].replace('_',' ').title()} {parts[1].replace('_',' ').title()}")
                elif fname in field_objects_plot:
                    header.append(field_objects_plot[fname].string)
                else:
                    header.append(fname.replace('_',' ').title())

            records = PlotModel.search_read(plot_domain, fields_to_read)
            for rec in records:
                for f_name in fields_to_read:
                    if isinstance(rec.get(f_name), tuple) and len(rec[f_name]) == 2:
                        rec[f_name] = rec[f_name][1]
                    elif isinstance(rec.get(f_name), (datetime, date)):
                        rec[f_name] = fields.Datetime.to_string(rec[f_name]) if isinstance(rec[f_name], datetime) else fields.Date.to_string(rec[f_name])
            data_rows_list_of_dicts = records


        elif entity_type.startswith('dynamic_form_'):
            try:
                form_id = int(entity_type.replace('dynamic_form_', ''))
            except ValueError:
                raise UserError(_("Invalid dynamic form type for export: %s") % entity_type)

            Form = self.env['dfr.dynamic.form']
            form_instance = Form.browse(form_id)
            if not form_instance.exists():
                raise UserError(_("Dynamic Form with ID %s not found.") % form_id)

            Submission = self.env['dfr.form.submission']
            Response = self.env['dfr.form.response']

            # Build submission domain, potentially linking through filtered farmers
            submission_domain = []
            if filters:
                farmer_domain_for_filters = self._build_common_domain(filters, date_field='farmer_id.registration_date')
                if farmer_domain_for_filters:
                    relevant_farmer_ids = self.env['dfr.farmer'].search(farmer_domain_for_filters).ids
                    submission_domain.append(('farmer_id', 'in', relevant_farmer_ids))
                if filters.get('date_from'):
                    submission_domain.append(('submission_date', '>=', filters['date_from']))
                if filters.get('date_to'):
                    submission_domain.append(('submission_date', '<=', filters['date_to']))

            submission_domain.append(('dynamic_form_id', '=', form_id))
            submissions = Submission.search(submission_domain, order='submission_date desc')

            # Prepare header: common submission fields + dynamic form fields
            header = [_('Submission ID'), _('Submission Date'), _('Farmer UID'), _('Farmer Name')]
            form_fields_ordered = form_instance.field_ids.sorted(key=lambda f: f.sequence) # Assuming 'sequence' field for order
            dynamic_field_labels = [f.field_label or f.field_name for f in form_fields_ordered]
            header.extend(dynamic_field_labels)

            # Fetch all responses for these submissions efficiently
            all_responses_data = Response.search_read(
                [('submission_id', 'in', submissions.ids)],
                ['submission_id', 'form_field_id', 'value']
            )
            # Organize responses by submission_id and then by form_field_id
            responses_by_submission = defaultdict(dict)
            for res in all_responses_data:
                responses_by_submission[res['submission_id'][0]][res['form_field_id'][0]] = res['value']

            field_id_to_label_map = {f.id: (f.field_label or f.field_name) for f in form_fields_ordered}

            for sub in submissions:
                row_dict = {
                    _('Submission ID'): sub.name or sub.id,
                    _('Submission Date'): fields.Datetime.to_string(sub.submission_date) if sub.submission_date else '',
                    _('Farmer UID'): sub.farmer_id.farmer_uid if sub.farmer_id else '',
                    _('Farmer Name'): sub.farmer_id.name if sub.farmer_id else '',
                }
                submission_specific_responses = responses_by_submission.get(sub.id, {})
                for field_def in form_fields_ordered:
                    field_label = field_id_to_label_map[field_def.id]
                    raw_value = submission_specific_responses.get(field_def.id, '')
                    # Handle multiselection formatting for CSV/XLSX (e.g., join list)
                    if field_def.field_type == 'multiselection' and raw_value:
                        try:
                            value_list = json.loads(raw_value)
                            if isinstance(value_list, list):
                                row_dict[field_label] = ', '.join(map(str, value_list))
                            else: # Not a list, store as is
                                row_dict[field_label] = str(raw_value)
                        except json.JSONDecodeError: # Not valid JSON
                            row_dict[field_label] = str(raw_value)
                    elif isinstance(raw_value, (datetime, date)): # Should be string from 'value' field
                        row_dict[field_label] = str(raw_value)
                    else:
                        row_dict[field_label] = raw_value
                data_rows_list_of_dicts.append(row_dict)
        else:
            raise UserError(_("Unknown entity type for export: %s") % entity_type)

        return {'header': header, 'data': data_rows_list_of_dicts}