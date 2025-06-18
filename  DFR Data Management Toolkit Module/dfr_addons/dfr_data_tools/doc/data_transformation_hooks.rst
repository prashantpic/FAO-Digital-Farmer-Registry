.. _dfr_data_tools_data_transformation_hooks:

===================================
Data Transformation Extensibility
===================================

Introduction
============
While the DFR Data Management Toolkit provides basic data validation and type conversion (as outlined in the `_transform_and_validate_row` method of the `DataImportService`), complex data migration scenarios often require custom transformations (as per REQ-DM-007). This could involve:

- Data cleansing (e.g., standardizing text, removing invalid characters).
- Combining multiple source fields into one target field (e.g., `first_name` + `last_name` -> `name`).
- Splitting a single source field into multiple target fields.
- Looking up related records based on complex or non-standard criteria from the source file.
- Applying specific business rules or calculations not covered by standard Odoo model constraints or basic validation.

The `DataImportService` within the `dfr_data_tools` module is designed with extensibility in mind to accommodate such custom data transformations.

Extensibility Mechanism
=======================
The primary hook point for custom data transformations is intended to be focused around the `_transform_and_validate_row` method within the `DataImportService` (`data.import.service` model). While the provided SDS example structure for `DataImportService` includes a placeholder `_apply_transformations` method, its direct call and integration within `_transform_and_validate_row` is conceptual.

The more direct and common Odoo way to introduce custom logic for a specific service or model method is through **inheritance and override**.

**Core `_transform_and_validate_row` method (Conceptual from SDS):**
This method is responsible for taking a dictionary of `odoo_field_name: value_from_file` and performing validation and basic type conversion. Custom transformations would ideally be injected *within* this process or as a distinct step called by it.

```python
# In dfr_data_tools/services/data_import_service.py
class DataImportService(models.AbstractModel):
    _name = 'data.import.service'
    # ... other methods ...

    def _transform_and_validate_row(self, job_id, target_model_obj, row_dict, line_num):
        """
        Apply transformations and validations.
        row_dict is {odoo_field_name: value_from_file}
        Returns validated_data_dict or raises ValidationError.
        """
        # (A) Point for pre-validation transformations
        # row_dict = self._apply_custom_pre_transformations(row_dict, target_model_obj.model, job_id)


        validated_data = {}
        errors = []
        for field_name, value in row_dict.items():
            field_obj = target_model_obj._fields.get(field_name)
            # ... (basic type validation and conversion as per SDS example) ...
            # (B) Point for field-specific transformations during validation loop
            # value = self._apply_custom_field_transformation(field_name, value, target_model_obj.model, job_id)
            # ... (rest of validation) ...
        
        # (C) Point for post-validation transformations on `validated_data`
        # validated_data = self._apply_custom_post_transformations(validated_data, target_model_obj.model, job_id)

        if errors:
            # ... (error handling) ...
            raise ValidationError(error_msg)

        return validated_data

    # Placeholder methods that could be overridden:
    # def _apply_custom_pre_transformations(self, data_dict, target_model_name, job_id):
    #     return data_dict
    #
    # def _apply_custom_field_transformation(self, field_name, value, target_model_name, job_id):
    #     return value
    #
    # def _apply_custom_post_transformations(self, data_dict, target_model_name, job_id):
    #     return data_dict

```

**How to Extend (Recommended Odoo Practice):**
To implement custom transformations, you would typically:
1.  Create a new Odoo module (e.g., `dfr_custom_transformations_module`).
2.  Make this new module dependent on `dfr_data_tools`.
3.  In your new module, inherit from `data.import.service` and override the `_transform_and_validate_row` method (or more specific transformation sub-methods if they are explicitly defined as hooks).

Example: Overriding `_transform_and_validate_row` for Custom Logic
-----------------------------------------------------------------
```python
# In your_custom_module/services/custom_data_import_service.py
from odoo import models, _logger
from odoo.exceptions import ValidationError

class CustomDataImportService(models.AbstractModel):
    _inherit = 'data.import.service'

    def _transform_and_validate_row(self, job_id, target_model_obj, row_dict, line_num):
        target_model_name = target_model_obj.model

        # --- Custom Pre-Transformation Step ---
        if target_model_name == 'dfr.farmer':
            # Example: Combine first_name and last_name from source into 'name'
            # Assuming source file has 'given_name' and 'family_name' columns mapped to these keys in row_dict
            if 'given_name' in row_dict or 'family_name' in row_dict:
                full_name_parts = []
                if row_dict.get('given_name'):
                    full_name_parts.append(str(row_dict['given_name']))
                if row_dict.get('family_name'):
                    full_name_parts.append(str(row_dict['family_name']))
                row_dict['name'] = " ".join(full_name_parts).strip()
                # Optionally remove original fields if not actual fields on target model
                # and were just intermediate from CSV
                # if 'given_name' not in target_model_obj._fields: del row_dict['given_name']
                # if 'family_name' not in target_model_obj._fields: del row_dict['family_name']

        # Call the original (super) method to perform base validation and type conversion
        # This original method will use the modified row_dict
        try:
            validated_data = super(CustomDataImportService, self)._transform_and_validate_row(
                job_id, target_model_obj, row_dict, line_num
            )
        except ValidationError as ve:
            # Allow super() to raise validation errors which are already logged by it
            raise ve
        except Exception as e:
            # Catch other unexpected errors from super() if necessary
            _logger.error(f"Unexpected error in super()._transform_and_validate_row for job {job_id}, line {line_num}: {e}")
            self._log_job_activity(job_id, f"Critical error during base validation: {e}", level='error', line_num=line_num, raw_row_data=row_dict)
            raise ValidationError(f"Critical error during base validation: {e}")


        # --- Custom Post-Transformation/Validation Step on `validated_data` ---
        if target_model_name == 'dfr.farmer':
            # Example: Standardize gender field based on a specific source convention
            # This assumes 'gender_source_field' was mapped and processed by super() into 'gender'
            # or it's directly in validated_data if it passed basic validation.
            # Let's assume 'gender_selection_field' is the target Odoo selection field.
            if 'gender_source_field' in validated_data: # Or check in original row_dict if it was mapped to an Odoo field
                source_gender = str(validated_data.get('gender_source_field', '')).strip().lower()
                if source_gender == 'm' or source_gender == '1':
                    validated_data['gender_selection_field'] = 'male'
                elif source_gender == 'f' or source_gender == '2':
                    validated_data['gender_selection_field'] = 'female'
                elif source_gender: # If not empty but unrecognized
                    self._log_job_activity(job_id, f"Unrecognized gender value '{source_gender}'. Setting to 'other'.", level='warning', line_num=line_num)
                    validated_data['gender_selection_field'] = 'other'
                # Remove the source field if it's not a direct field on the target model
                # if 'gender_source_field' != 'gender_selection_field':
                #    del validated_data['gender_source_field']


        _logger.info(f"Applied custom transformations for {target_model_name} on line {line_num}")
        return validated_data

```
Ensure this new Python file is imported in your custom module's `services/__init__.py`.

Developing Custom Transformations
=================================

-   **Accessing Row Data**: The `row_dict` parameter (before `super()` call) provides the current row's data as mapped from CSV headers to Odoo field names. The `validated_data` (after `super()` call) contains data that has passed basic type conversions.
-   **Target Model Context**: Use `target_model_name` or `target_model_obj` to apply logic conditionally for different models.
-   **Job Context**: The `job_id` is available, allowing you to use `self._log_job_activity(...)` for custom warnings or info messages related to your transformations.
-   **Idempotency**: Aim for idempotent transformations where possible.
-   **Error Handling**:
    -   If a custom transformation determines a row is invalid, raise a `ValidationError("Your custom error message")`. This will be caught by the main processing loop in `DataImportService`, and the row will be logged as an error.
    -   For non-critical issues (e.g., a value couldn't be fully standardized but a default can be used), log a warning using `self._log_job_activity(...)`.
-   **Field Naming**: Be very clear about source field names (as they appear in `row_dict` after initial mapping by `_map_headers`) and target Odoo field names you are populating.

Example Transformation: Lookup Related Record with Complex Key
--------------------------------------------------------------
```python
# (Inside your overridden _transform_and_validate_row, likely before calling super()
# if the looked-up ID is needed for further validation by super, or after if it's a final step)

if target_model_name == 'dfr.plot' and 'legacy_cooperative_identifier_from_source_file' in row_dict:
    legacy_code = row_dict.pop('legacy_cooperative_identifier_from_source_file') # Use .pop if it's not an Odoo field
    Cooperative = self.env['dfr.cooperative'] # Assuming such a model exists
    
    # Example: Cooperative identified by a combination of region_code and coop_number from source
    region_code = row_dict.pop('coop_region_code_source', None)
    coop_number = row_dict.pop('coop_local_num_source', None)

    if region_code and coop_number:
        cooperative_rec = Cooperative.search([
            ('region_code_field_on_coop', '=', region_code), # Technical field name on dfr.cooperative
            ('local_number_field_on_coop', '=', coop_number)  # Technical field name on dfr.cooperative
        ], limit=1)

        if cooperative_rec:
            row_dict['cooperative_id'] = cooperative_rec.id # 'cooperative_id' is the M2O field on dfr.plot
        else:
            # Handle error: cooperative not found.
            # This will likely cause a ValidationError in super() if cooperative_id is required
            # or if it fails m2o resolution. Or, raise error here directly.
            error_msg = f"Cooperative with region '{region_code}' and number '{coop_number}' not found."
            self._log_job_activity(job_id, error_msg, level='error', line_num=line_num, raw_row_data=str(row_dict))
            # Decide: either let super() handle it or raise ValidationError(error_msg) here
            row_dict['cooperative_id'] = False # Set to False to ensure it fails m2o if required
    else:
        # Not enough info to lookup cooperative
        self._log_job_activity(job_id, "Missing region_code or coop_number for cooperative lookup.", level='warning', line_num=line_num)
        row_dict['cooperative_id'] = False

# Now, when super()._transform_and_validate_row is called, it will see row_dict['cooperative_id']
```

By overriding relevant methods (primarily `_transform_and_validate_row` or more granular sub-methods if they are exposed as hooks), developers can inject sophisticated, model-specific data preparation logic into the import pipeline. This approach ensures better maintainability and separation of concerns, as custom logic resides in dedicated modules rather than altering the core `dfr_data_tools` module.