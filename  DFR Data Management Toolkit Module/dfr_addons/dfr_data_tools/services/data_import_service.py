# -*- coding: utf-8 -*-
import base64
import csv
import io
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except ImportError:
    _logger.debug("openpyxl library not found. XLSX import will not be available.")
    openpyxl = None

class DataImportService(models.AbstractModel):
    _name = 'data.import.service'
    _description = 'DFR Data Import Service'

    def _log_job_activity(self, job_id, message, level='info', record_identifier=None, line_num=None, raw_row_data=None):
        job_log_model = self.env['data.import.job.log']
        log_vals = {
            'job_id': job_id,
            'log_message': message,
            'log_type': level,
            'line_number': line_num,
            'record_identifier': record_identifier,
            'raw_row_data': str(raw_row_data) if raw_row_data else None,
        }
        job_log_model.create(log_vals)

    def _get_target_model_fields_info(self, target_model_name):
        """ Returns a dict of field_name: ir.model.fields record """
        ModelField = self.env['ir.model.fields']
        field_recs = ModelField.search([
            ('model', '=', target_model_name),
            ('store', '=', True) # Consider only stored fields
        ])
        return {field.name: field for field in field_recs}

    def _parse_csv(self, file_content_bytes):
        try:
            decoded_content = file_content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                decoded_content = file_content_bytes.decode('latin-1') # Fallback
            except UnicodeDecodeError as e:
                raise UserError(_("Could not decode CSV file. Ensure it is UTF-8 or LATIN-1 encoded. Error: %s") % e)
        csv_data = csv.reader(io.StringIO(decoded_content))
        return list(csv_data)

    def _parse_xlsx(self, file_content_bytes):
        if not openpyxl:
            raise UserError(_("The 'openpyxl' library is required to import XLSX files. Please install it (pip install openpyxl)."))
        try:
            workbook = openpyxl.load_workbook(io.BytesIO(file_content_bytes))
            sheet = workbook.active
            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append(list(row))
            return data
        except Exception as e:
            _logger.error("Error parsing XLSX file: %s", e)
            raise UserError(_("Could not parse XLSX file. Error: %s") % e)

    def _map_headers(self, headers, target_model_name, job_id):
        """ Basic header mapping. Logs issues. Returns {csv_column_index: odoo_field_name} """
        model_fields = self.env[target_model_name]._fields
        odoo_field_names = list(model_fields.keys())
        
        mapped_headers = {} # {csv_column_index: odoo_field_name}
        
        for i, header_val in enumerate(headers):
            header = str(header_val).strip() if header_val is not None else ""
            normalized_header = header.lower()
            found_match = False
            
            # Direct match technical name
            if normalized_header in odoo_field_names:
                mapped_headers[i] = normalized_header
                found_match = True
            else:
                # Match by field label (string attribute)
                for odoo_field_name, field_obj in model_fields.items():
                    if field_obj.string and normalized_header == field_obj.string.strip().lower():
                        mapped_headers[i] = odoo_field_name
                        found_match = True
                        break
            
            if not found_match and header: # Log only if header is not empty
                self._log_job_activity(job_id, _("Column '%s' not found in target model '%s' or its field labels. It will be ignored.") % (header, target_model_name), level='warning', line_num=0)
        
        if not mapped_headers:
             self._log_job_activity(job_id, _("No columns could be mapped. Please check headers against target model field names or labels."), level='error', line_num=0)
             raise ValidationError(_("No columns could be mapped. Ensure CSV/XLSX headers match target model field names or field labels."))

        job = self.env['data.import.job'].browse(job_id)
        job.field_mapping_info = _("Mapped headers (Column Index -> Odoo Field Name):\n") + \
                                 "\n".join([f"{headers[idx] if idx < len(headers) else 'Col '+str(idx)} -> {name}" for idx, name in mapped_headers.items()])

        return mapped_headers

    def _apply_transformations(self, data_dict, target_model_name, job_id, line_num):
        """
        Placeholder for custom transformations. (REQ-DM-007 Extensibility Point)
        This method can be overridden in other modules to apply specific data transformations
        before validation and record creation/update.
        :param data_dict: {odoo_field_name: value_from_file}
        :param target_model_name: Name of the target Odoo model
        :param job_id: ID of the current import job
        :param line_num: Line number in the source file
        :return: Transformed data_dict
        """
        # Example: if target_model_name == 'res.partner':
        #    if 'name' in data_dict and data_dict['name']:
        #        data_dict['name'] = data_dict['name'].title() # Capitalize names
        return data_dict

    def _transform_and_validate_row(self, job_id, target_model_obj, row_dict_raw, line_num):
        """
        Apply transformations and validations.
        row_dict_raw is {odoo_field_name: value_from_file}
        Returns validated_data_dict or raises ValidationError.
        """
        # Apply transformations first
        transformed_data = self._apply_transformations(dict(row_dict_raw), target_model_obj._name, job_id, line_num)

        validated_data = {}
        errors = []
        for field_name, value in transformed_data.items():
            field_obj = target_model_obj._fields.get(field_name)
            if not field_obj:
                # This should not happen if _map_headers worked correctly and field_name is valid
                _logger.warning(_("Field %s not found in model %s during validation. Skipping.") % (field_name, target_model_obj._name))
                continue

            # Handle empty strings as None/False for non-char/text fields
            current_value = value
            if isinstance(value, str) and not value.strip() and field_obj.type not in ('char', 'text', 'html'):
                current_value = None 

            if current_value is None: # Handle empty/None values
                if field_obj.required:
                    errors.append(_("Field '%s' (%s) is required but empty.") % (field_obj.string, field_name))
                else:
                    validated_data[field_name] = False # Odoo expects False for empty non-required fields (e.g. boolean, relational)
                continue

            try:
                if field_obj.type == 'char':
                    validated_data[field_name] = str(current_value)
                elif field_obj.type == 'text' or field_obj.type == 'html':
                    validated_data[field_name] = str(current_value)
                elif field_obj.type == 'integer':
                    validated_data[field_name] = int(float(current_value)) # float first to handle "1.0"
                elif field_obj.type == 'float':
                    validated_data[field_name] = float(current_value)
                elif field_obj.type == 'boolean':
                    validated_data[field_name] = str(current_value).strip().lower() in ['true', '1', 'yes', 't']
                elif field_obj.type == 'date':
                    validated_data[field_name] = fields.Date.to_string(fields.Date.from_string(str(current_value)))
                elif field_obj.type == 'datetime':
                    validated_data[field_name] = fields.Datetime.to_string(fields.Datetime.from_string(str(current_value)))
                elif field_obj.type == 'selection':
                    # Ensure value is one of the selection options
                    selection_values = [s[0] for s in field_obj.selection]
                    if str(current_value) in selection_values:
                        validated_data[field_name] = str(current_value)
                    else:
                         # Try to match by label
                        found_by_label = False
                        for s_key, s_label in self.env[target_model_obj._name]._fields[field_name].get_description(self.env)['selection']:
                            if str(current_value).strip().lower() == str(s_label).strip().lower():
                                validated_data[field_name] = s_key
                                found_by_label = True
                                break
                        if not found_by_label:
                            errors.append(_("Field '%s' (%s): Value '%s' is not a valid selection. Valid options: %s") % (field_obj.string, field_name, current_value, selection_values))
                elif field_obj.type == 'many2one':
                    related_model = self.env[field_obj.comodel_name]
                    # Attempt to find by name or external ID (if external IDs are used in source)
                    # This is a common area for custom logic.
                    # For now, assuming value is an ID or exact name.
                    rel_val_str = str(current_value).strip()
                    found_related = None
                    if rel_val_str.isdigit(): # Try by ID first
                        found_related = related_model.browse(int(rel_val_str)).exists()
                    if not found_related: # Try by name
                         found_related = related_model.search([('name', '=ilike', rel_val_str)], limit=1)
                    # Add search by external ID (xmlid) if applicable
                    # if not found_related:
                    #   found_related = self.env.ref(rel_val_str, raise_if_not_found=False)

                    if found_related:
                        validated_data[field_name] = found_related.id
                    else:
                        errors.append(_("Related record for '%s' with value '%s' not found in model '%s'.") % (field_obj.string, current_value, field_obj.comodel_name))
                elif field_obj.type in ['one2many', 'many2many']:
                    # Importing o2m/m2m from simple CSV columns is complex and often requires special handling
                    # (e.g., comma-separated names/IDs, or using Odoo's sub-import features).
                    # This basic importer will skip them or log a warning.
                    self._log_job_activity(job_id, _("Field '%s' (%s) is a relational %s field. Direct import of this type is complex and not fully supported by this basic tool. Value '%s' ignored.") % (field_obj.string, field_name, field_obj.type, current_value), level='warning', line_num=line_num, raw_row_data=row_dict_raw)
                    # To support this, you might expect comma-separated IDs or names, then search/create.
                    # e.g. for m2m with names:
                    # names = [name.strip() for name in str(current_value).split(',')]
                    # related_ids = self.env[field_obj.comodel_name].search([('name', 'in', names)]).ids
                    # validated_data[field_name] = [(6, 0, related_ids)]
                else:
                    validated_data[field_name] = current_value # Passthrough for other types
            except ValueError as e:
                errors.append(_("Field '%s' (%s): Invalid value '%s'. Conversion Error: %s") % (field_obj.string, field_name, current_value, e))
            except Exception as e:
                 errors.append(_("Field '%s' (%s): Unexpected error processing value '%s'. Error: %s") % (field_obj.string, field_name, current_value, e))

        if errors:
            error_msg = "; ".join(errors)
            # Logging is done by the caller (process_uploaded_file) if this raises ValidationError
            raise ValidationError(error_msg)

        return validated_data

    def _create_or_update_record(self, job_id, target_model_obj, validated_data, options, line_num, raw_row_data_for_log):
        """
        Creates or updates a record in the target model.
        For this version, only creation is implemented as per SDS example.
        Update logic (REQ-DM-003) would require external ID matching.
        """
        # Placeholder for update logic:
        # external_id_field = 'x_studio_external_id' # Example, make configurable or use Odoo's standard
        # external_id_value = validated_data.get(external_id_field) # If external_id is part of mapped data
        # existing_record = None
        # if options.get('update_existing') and external_id_value:
        #    # Using Odoo's standard way to load by external ID:
        #    # existing_record = self.env.ref(external_id_value, raise_if_not_found=False)
        #    # Or search by a specific field:
        #    existing_record = target_model_obj.search([(external_id_field, '=', external_id_value)], limit=1)

        # if existing_record and options.get('update_existing'):
        #    try:
        #        existing_record.write(validated_data)
        #        self._log_job_activity(job_id, _("Record updated successfully: ID %s") % existing_record.id, level='info', line_num=line_num, record_identifier=str(existing_record.id))
        #        return True, 1 # Success, updated_count = 1
        #    except Exception as e:
        #        _logger.error(f"Error updating record {existing_record.id} in {target_model_obj._name}: {e}", exc_info=True)
        #        self._log_job_activity(job_id, _("Failed to update record. Error: %s") % e, level='error', line_num=line_num, raw_row_data=raw_row_data_for_log)
        #        return False, 0 # Failure
        # el
        if options.get('create_if_not_exist'):
            try:
                new_record = target_model_obj.create(validated_data)
                self._log_job_activity(job_id, _("Record created successfully with ID: %s") % new_record.id, level='info', line_num=line_num, record_identifier=str(new_record.id))
                return True, 1 # Success, created_count = 1
            except Exception as e:
                _logger.error(f"Error creating record in {target_model_obj._name}: {e}", exc_info=True)
                self._log_job_activity(job_id, _("Failed to create record. Error: %s") % e, level='error', line_num=line_num, raw_row_data=raw_row_data_for_log)
                return False, 0 # Failure
        else:
            self._log_job_activity(job_id, _("Skipped record creation (Create if Not Exist is False and no update logic matched)."), level='warning', line_num=line_num)
            return True, 0 # Skipped, not an error per se

    def process_uploaded_file(self, job_id, file_content_bytes, file_name, target_model_name, options):
        job = self.env['data.import.job'].browse(job_id)
        if not job.exists():
            _logger.error(f"Import Job ID {job_id} not found.")
            # Cannot log to job if it doesn't exist.
            return

        _logger.info(f"Starting import for job {job.name} (ID: {job.id}), file: {file_name}, target: {target_model_name}")
        job.write({'state': 'in_progress', 'import_date': fields.Datetime.now()})
        # self.env.cr.commit() # Commit state change early if using queue_job or threading

        processed_count = 0
        success_count = 0
        error_count = 0
        
        try:
            target_model_obj = self.env[target_model_name]
        except KeyError:
            msg = _("Target model '%s' not found in the system.") % target_model_name
            self._log_job_activity(job_id, msg, level='error')
            job.write({'state': 'error', 'log_summary': msg})
            return


        try:
            if file_name.lower().endswith('.csv'):
                rows = self._parse_csv(file_content_bytes)
            elif file_name.lower().endswith(('.xls', '.xlsx')):
                rows = self._parse_xlsx(file_content_bytes)
            else:
                raise UserError(_("Unsupported file format. Please use CSV or XLSX."))

            if not rows:
                self._log_job_activity(job_id, _("File is empty or could not be parsed."), level='error')
                job.write({'state': 'error', 'log_summary': _("File is empty.")})
                return

            job.total_records_in_file = len(rows) - (1 if options.get('skip_header_row', True) else 0)
            if job.total_records_in_file <= 0:
                 self._log_job_activity(job_id, _("No data records found in file (excluding header)."), level='error')
                 job.write({'state': 'error', 'log_summary': _("No data records found.")})
                 return

            
            headers_row_index = 0
            headers = rows[headers_row_index]
            data_rows = rows[(headers_row_index + 1):] if options.get('skip_header_row', True) else rows

            header_map = self._map_headers(headers, target_model_name, job_id) # {csv_column_index: odoo_field_name}
            
            if not header_map: # map_headers logs error and raises ValidationError if it fails critically
                job.write({'state': 'error', 'log_summary': _("Header mapping failed.")}) # map_headers already logged details
                return

            for i, row_list_data in enumerate(data_rows):
                processed_count += 1
                line_num_in_file = i + (headers_row_index + 2 if options.get('skip_header_row', True) else headers_row_index + 1)
                
                raw_row_dict_for_log = {headers[idx]: val for idx, val in enumerate(row_list_data) if idx < len(headers)}

                data_dict_to_process = {}
                for col_idx, odoo_field_name in header_map.items():
                    if col_idx < len(row_list_data):
                        data_dict_to_process[odoo_field_name] = row_list_data[col_idx]
                    else:
                        # If a mapped column index is out of bounds for the current row
                        data_dict_to_process[odoo_field_name] = None 
                        self._log_job_activity(job_id, _("Missing column data for header '%s' (mapped to '%s') at line %s.") % (headers[col_idx] if col_idx < len(headers) else 'Unknown Header', odoo_field_name, line_num_in_file), level='warning', line_num=line_num_in_file, raw_row_data=raw_row_dict_for_log)

                if not any(str(val).strip() for val in data_dict_to_process.values()): # Skip entirely empty logical rows
                    self._log_job_activity(job_id, _("Skipping empty row."), level='info', line_num=line_num_in_file)
                    # Don't increment error_count, but processed_count was already incremented.
                    # Adjust total_records_in_file if we want to exclude these from progress.
                    # For now, consider it processed but skipped.
                    continue

                try:
                    validated_data = self._transform_and_validate_row(job_id, target_model_obj, data_dict_to_process, line_num_in_file)
                    
                    record_processed_ok, created_updated_count = self._create_or_update_record(
                        job_id, target_model_obj, validated_data, options, line_num_in_file, raw_row_dict_for_log
                    )

                    if record_processed_ok:
                        success_count += created_updated_count # will be 1 for create, 1 for update, 0 for skip
                    else: # _create_or_update_record already logged the specific ORM error
                        error_count += 1

                except ValidationError as ve:
                    self._log_job_activity(job_id, _("Validation Error: %s") % ve.args[0], level='error', line_num=line_num_in_file, raw_row_data=raw_row_dict_for_log)
                    error_count += 1
                except Exception as e:
                    _logger.error(f"Unexpected error processing row {line_num_in_file} for job {job.id}: {e}", exc_info=True)
                    self._log_job_activity(job_id, _("Unexpected system error: %s") % e, level='error', line_num=line_num_in_file, raw_row_data=raw_row_dict_for_log)
                    error_count += 1
                
                if processed_count % 100 == 0: # Commit periodically for large files
                    job.write({
                        'total_records_processed': processed_count,
                        'successful_records': success_count,
                        'failed_records': error_count,
                    })
                    self.env.cr.commit() # Important for long running jobs
                    _logger.info(f"Job {job.id}: Committed progress. Processed {processed_count}/{job.total_records_in_file} records...")


            final_state = 'done' if error_count == 0 else 'error'
            summary_message = _("Import finished. Success: %s, Failed: %s, Processed: %s / %s records.") % (success_count, error_count, processed_count, job.total_records_in_file)
            job.write({
                'state': final_state,
                'total_records_processed': processed_count,
                'successful_records': success_count,
                'failed_records': error_count,
                'log_summary': job.log_summary or summary_message # Update summary if not already populated by compute method with errors
            })
            _logger.info(f"Import job {job.name} (ID: {job.id}) finished. Status: {final_state}. {summary_message}")

        except ValidationError as ve: # Errors from _map_headers or other high-level validation
             _logger.warning(f"ValidationError during import for job {job.id}: {ve.args[0]}")
             self._log_job_activity(job_id, _("Import Process Error: %s") % ve.args[0], level='error')
             job.write({'state': 'error', 'log_summary': ve.args[0]})
        except UserError as ue: # User-friendly errors (e.g. file format)
            _logger.warning(f"UserError during import for job {job.id}: {ue.args[0]}")
            self._log_job_activity(job_id, _("Import Process Error: %s") % ue.args[0], level='error')
            job.write({'state': 'error', 'log_summary': ue.args[0]})
        except Exception as e:
            _logger.error(f"Critical error during import for job {job.id}: {e}", exc_info=True)
            err_msg = _("Critical System Error during import: %s") % e
            self._log_job_activity(job_id, err_msg, level='error')
            job.write({'state': 'error', 'log_summary': err_msg})
        finally:
            self.env.cr.commit() # Ensure final state and logs are committed