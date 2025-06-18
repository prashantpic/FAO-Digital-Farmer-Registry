# Software Design Specification: DFR Dynamic Form Engine Module (dfr_dynamic_forms)

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR Dynamic Form Engine Module (`dfr_dynamic_forms`). This Odoo module enables administrators to design, manage, and version custom data collection forms. It handles form submissions from various clients (mobile, portal, admin) and links them to farmer profiles. The module supports various field types, validation rules, and conditional logic for displaying fields.

### 1.2 Scope
The scope of this SDS covers the design of all Odoo models, services, wizards, views, static resources, and security configurations within the `dfr_dynamic_forms` module. This module is an integral part of the Digital Farmer Registry (DFR) platform and interacts with other DFR modules, particularly `dfr_common`, `dfr_farmer_registry`, and `dfr_rbac_config`.

### 1.3. Requirements Traceability
This module addresses the following key requirements:
*   **REQ-3-001:** Dynamic Form Engine with no-code/low-code interface, supporting diverse field types.
*   **REQ-3-002:** Support for input validation rules (required, min/max length, numeric range, regex).
*   **REQ-3-003:** Support for conditional logic (show/hide fields).
*   **REQ-3-004:** Form versioning to manage changes and preserve data integrity.
*   **REQ-3-008:** Linking dynamic form submissions to farmer profiles and storing data in separate models.
*   **REQ-3-012:** Development as a custom Odoo module, considering OCA modules for foundation.

### 1.4. Evaluation of OCA Modules
As per **REQ-3-012**, suitable Odoo Community Association (OCA) modules such as `survey` (for form rendering logic) and `formio` (for form building/rendering capabilities) will be evaluated during the detailed design and implementation phases.
*   **OCA `survey` module:** Components related to form rendering, answer storage, and possibly basic UI elements for question types might be adaptable. Its versioning and advanced conditional logic might be less suitable directly.
*   **OCA `formio` module (if Odoo-compatible wrappers exist):** If a stable Odoo integration/wrapper for Form.io exists and is compatible with Odoo 18.0 Community, its advanced form builder UI and rendering capabilities could be leveraged. However, direct integration might be complex and bring external dependencies not fitting the "core Odoo addon" approach.

The design presented here prioritizes a custom implementation within Odoo's framework to ensure tight integration, maintainability, and adherence to the specific DFR requirements. However, if specific components from these OCA modules can be used to accelerate development without compromising the core architecture or licensing, they will be incorporated. The primary approach is to build custom models and views, potentially enhanced by custom JavaScript/OWL widgets for the form builder UI.

## 2. System Architecture
The `dfr_dynamic_forms` module follows a Modular Monolith style, fitting within the overall DFR Odoo platform. It leverages Odoo's Model-View-Controller (MVC) / Model-View-Template (MVT) pattern.

**Key Architectural Layers Involved:**
*   **DFR Odoo Domain Models Layer:** Defines the data structures (`dfr.form`, `dfr.form.version`, `dfr.form.field`, `dfr.form.submission`, `dfr.form.response`).
*   **DFR Odoo Application Services Layer:** Encapsulates business logic for form definition, submission processing, and validation.
*   **DFR Odoo Presentation Layer:** Provides administrative UIs for form building and submission management.

## 3. Data Design

### 3.1. Data Models

#### 3.1.1. `dfr.form` (Dynamic Form Master)
*   **Description:** Represents a master dynamic form template. Manages high-level form properties and acts as a parent for its different versions.
*   **Odoo Model Name:** `dfr.form`
*   **Inherits:** `mail.thread`, `mail.activity.mixin`
*   **Fields:**
    *   `name` (Type: `fields.Char`, Required: True, String: "Form Title"): The main title or name of the form.
    *   `description` (Type: `fields.Text`, String: "Description"): A detailed description of the form's purpose.
    *   `active` (Type: `fields.Boolean`, String: "Active", Default: `True`): Indicates if the form master is active.
    *   `form_version_ids` (Type: `fields.One2many`, Comodel: `dfr.form.version`, Inverse Name: `form_master_id`, String: "Versions"): List of all versions associated with this form master.
    *   `current_published_version_id` (Type: `fields.Many2one`, Comodel: `dfr.form.version`, String: "Current Published Version", Compute: `_compute_current_published_version`, Store: `True`): The currently active and published version of this form.
    *   `country_id` (Type: `fields.Many2one`, Comodel: `res.country`, String: "Country", Help: "Country for which this form is applicable, if specific. Used for access control or filtering if needed.")
*   **Methods:**
    *   `_compute_current_published_version(self)`:
        *   **Logic:** Iterates through `form_version_ids` to find the version with `status = 'published'`. Sets `current_published_version_id` accordingly. If multiple are published (which shouldn't happen ideally through workflow), it could pick the latest `publish_date`.
        *   **Dependencies:** `form_version_ids.status`, `form_version_ids.publish_date`
    *   `action_create_new_version(self)`:
        *   **Logic:** Opens a wizard (`dfr.form.version.wizard`) pre-filled with `form_master_id = self.id`.
        *   **Returns:** Odoo action dictionary to open the wizard view.
    *   `action_view_versions(self)`:
        *   **Logic:** Returns an Odoo action to display the tree/kanban view of `dfr.form.version` records filtered by `form_master_id = self.id`.
        *   **Returns:** Odoo action dictionary.
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-004`

#### 3.1.2. `dfr.form.version` (Dynamic Form Version)
*   **Description:** Represents a specific, immutable version of a dynamic form template, including its fields structure and publication status.
*   **Odoo Model Name:** `dfr.form.version`
*   **Inherits:** `mail.thread`
*   **Fields:**
    *   `form_master_id` (Type: `fields.Many2one`, Comodel: `dfr.form`, Required: True, Ondelete: `cascade`, String: "Form Master"): Link to the parent `dfr.form`.
    *   `version_number` (Type: `fields.Char`, Required: True, Readonly: True, String: "Version Number", Default: `lambda self: self.env['ir.sequence'].next_by_code('dfr.form.version.sequence') or 'New'`): Unique version identifier for the form, typically sequential.
    *   `name` (Type: `fields.Char`, Related: `form_master_id.name`, Store: True, String: "Form Name"): Inherited from the form master.
    *   `description` (Type: `fields.Text`, String: "Version Description"): Specific description for this version (e.g., changes from previous).
    *   `status` (Type: `fields.Selection`, Selection: `[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')]`, Default: `'draft'`, String: "Status", Tracking: True): Lifecycle status of the form version.
    *   `publish_date` (Type: `fields.Datetime`, Readonly: True, String: "Publish Date"): Timestamp when the version was published.
    *   `archive_date` (Type: `fields.Datetime`, Readonly: True, String: "Archive Date"): Timestamp when the version was archived.
    *   `field_ids` (Type: `fields.One2many`, Comodel: `dfr.form.field`, Inverse Name: `form_version_id`, String: "Fields", Copy: True): List of fields defined for this form version. Fields are copied when a version is copied.
    *   `submission_count` (Type: `fields.Integer`, Compute: `_compute_submission_count`, String: "Submissions", Store: False): Number of submissions made using this form version.
    *   `can_be_published` (Type: `fields.Boolean`, Compute: `_compute_can_be_published`, String: "Can Publish?"): True if the current status allows publishing.
    *   `can_be_archived` (Type: `fields.Boolean`, Compute: `_compute_can_be_archived`, String: "Can Archive?"): True if the current status allows archiving.
    *   `is_editable` (Type: `fields.Boolean`, Compute: `_compute_is_editable`, String: "Is Editable?", Help: "Indicates if the form version (fields) can still be edited. Typically true only in 'draft' state."):
*   **Methods:**
    *   `action_publish(self)`:
        *   **Logic:** Sets `status` to `'published'` and `publish_date` to now. Ensures no other version of the same master is published (archives others or raises error). Updates `current_published_version_id` on `dfr.form`.
        *   **Returns:** `True` on success.
    *   `action_archive(self)`:
        *   **Logic:** Sets `status` to `'archived'` and `archive_date` to now. If this was the `current_published_version_id`, clears it on `dfr.form`.
        *   **Returns:** `True` on success.
    *   `action_set_to_draft(self)`:
        *   **Logic:** If archived, allows setting back to draft (e.g., for corrections before re-publishing). Clears `archive_date`.
        *   **Returns:** `True` on success.
    *   `_compute_submission_count(self)`:
        *   **Logic:** Counts `dfr.form.submission` records linked to `self.id`.
    *   `_compute_can_be_published(self)`:
        *   **Logic:** Sets to `True` if `status == 'draft'`.
    *   `_compute_can_be_archived(self)`:
        *   **Logic:** Sets to `True` if `status == 'published'` or `status == 'draft'`.
    *   `_compute_is_editable(self)`:
        *   **Logic:** Sets to `True` if `status == 'draft'`.
    *   `copy(self, default=None)`:
        *   **Logic:** Overrides default copy to create a new draft version. Sets `status` to `'draft'`, clears `publish_date`, `archive_date`. Generates a new `version_number`. `field_ids` should be deep copied.
        *   **Returns:** New `dfr.form.version` record.
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-004`

#### 3.1.3. `dfr.form.field` (Dynamic Form Field)
*   **Description:** Represents a single field within a dynamic form version, defining its type, label, validation, and conditional logic.
*   **Odoo Model Name:** `dfr.form.field`
*   **Order:** `sequence, id`
*   **Fields:**
    *   `form_version_id` (Type: `fields.Many2one`, Comodel: `dfr.form.version`, Required: True, Ondelete: `cascade`, String: "Form Version"): Link to the parent form version.
    *   `name` (Type: `fields.Char`, Required: True, String: "Technical Name", Help: "Technical name for the field (e.g., 'farmer_age', 'crop_type'). Must be unique within a form version. Used for data storage and logic."):
    *   `label` (Type: `fields.Char`, Required: True, Translate: True, String: "Label"): User-visible label for the field.
    *   `field_type` (Type: `fields.Selection`, Required: True, Default: `'text'`, String: "Field Type", Selection: `[('text', 'Text'), ('number', 'Number'), ('date', 'Date'), ('datetime', 'Datetime'), ('selection', 'Selection (Dropdown)'), ('multi_selection', 'Multi-Selection (Tags)'), ('boolean', 'Boolean (Checkbox)'), ('gps_point', 'GPS Point (Latitude, Longitude)'), ('image', 'Image/File Attachment'), ('computed_text', 'Computed Text (Read-only)')]`)
    *   `sequence` (Type: `fields.Integer`, Default: `10`, String: "Sequence"): Order of display within the form.
    *   `is_required` (Type: `fields.Boolean`, Default: `False`, String: "Is Required (Form Level)", Help="Simple 'required' flag for UI indication. More complex validation via rules."):
    *   `help_text` (Type: `fields.Text`, Translate: True, String: "Help Text"): Additional instructions or help for the user.
    *   `selection_options` (Type: `fields.Text`, String: "Selection Options", Help: "For 'selection'/'multi_selection' types. One option per line in format 'value:Label'. Example: 'opt1:Option 1\\nopt2:Option 2'. The 'value' part is stored."):
    *   `validation_rule_required` (Type: `fields.Boolean`, String: "Validation: Is Required"): Explicit validation rule for required.
    *   `validation_rule_min_length` (Type: `fields.Integer`, String: "Validation: Min Length"): For text fields.
    *   `validation_rule_max_length` (Type: `fields.Integer`, String: "Validation: Max Length"): For text fields.
    *   `validation_rule_min_value` (Type: `fields.Float`, String: "Validation: Min Value"): For number fields.
    *   `validation_rule_max_value` (Type: `fields.Float`, String: "Validation: Max Value"): For number fields.
    *   `validation_rule_regex` (Type: `fields.Char`, String: "Validation: Regex Pattern"): Custom regex for validation.
    *   `validation_error_message` (Type: `fields.Char`, Translate: True, String: "Custom Validation Error Message"): Custom message to show if validation fails.
    *   `conditional_logic_json` (Type: `fields.Text`, String: "Conditional Logic (JSON)", Help: "JSON defining conditions to show/hide this field. Example: [{'field_name': 'other_field_technical_name', 'operator': '=', 'value': 'some_value', 'value_type': 'text'}] where value_type can be 'text', 'number', 'boolean'. Other operators: '!=', '>', '<', '>=', '<='."):
    *   `placeholder` (Type: `fields.Char`, Translate: True, String: "Placeholder"): Placeholder text for input fields.
    *   `default_value_text` (Type: `fields.Char`, String: "Default Text Value"): Pre-filled value for text types.
    *   `default_value_number` (Type: `fields.Float`, String: "Default Number Value"): Pre-filled value for number types.
    *   `default_value_boolean` (Type: `fields.Boolean`, String: "Default Boolean Value"): Pre-filled value for boolean types.
*   **Methods:**
    *   `get_selection_options_parsed(self)`:
        *   **Logic:** Parses the `selection_options` text field into a list of `(value, label)` tuples. Handles empty lines or malformed entries gracefully.
        *   **Returns:** `list` of `(str, str)` tuples.
    *   `_validate_conditional_logic_json(self)`:
        *   **Decorator:** `@api.constrains('conditional_logic_json')`
        *   **Logic:** If `conditional_logic_json` is set, attempts to parse it as JSON. Validates the structure (e.g., list of condition dicts, presence of 'field_name', 'operator', 'value'). Raises `ValidationError` if invalid.
*   **SQL Constraints:**
    *   `unique_name_per_form_version`: `UNIQUE(form_version_id, name)` - Ensures technical field names are unique within the same form version.
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-002`, `REQ-3-003`

#### 3.1.4. `dfr.form.submission` (Dynamic Form Submission)
*   **Description:** Represents an instance of a completed dynamic form, submitted by a user for a specific farmer.
*   **Odoo Model Name:** `dfr.form.submission`
*   **Inherits:** `mail.thread`, `mail.activity.mixin`
*   **Fields:**
    *   `name` (Type: `fields.Char`, Compute: `_compute_name`, Store: True, String: "Submission Reference"): A human-readable reference for the submission.
    *   `farmer_id` (Type: `fields.Many2one`, Comodel: `dfr.farmer` (from `dfr_farmer_registry`), Required: True, Ondelete: `restrict`, String: "Farmer"): The farmer to whom this submission pertains.
    *   `form_version_id` (Type: `fields.Many2one`, Comodel: `dfr.form.version`, Required: True, Ondelete: `restrict`, String: "Form Version"): The specific version of the form that was submitted.
    *   `submission_date` (Type: `fields.Datetime`, Required: True, Default: `fields.Datetime.now`, Readonly: True, String: "Submission Date"): Timestamp of submission.
    *   `submitted_by_user_id` (Type: `fields.Many2one`, Comodel: `res.users`, String: "Submitted By", Default: `lambda self: self.env.user`, Readonly: True): The Odoo user who submitted the form (if through backend/mobile app by logged-in user).
    *   `submission_source` (Type: `fields.Selection`, Selection: `[('admin', 'Admin Portal'), ('mobile', 'Mobile App'), ('portal', 'Farmer Portal')]`, String: "Source", Default: `'admin'`): Indicates the source of the submission.
    *   `response_ids` (Type: `fields.One2many`, Comodel: `dfr.form.response`, Inverse Name: `submission_id`, String: "Responses", Copy: True): The actual data/answers provided in the form.
    *   `state` (Type: `fields.Selection`, Selection: `[('draft', 'Draft'), ('submitted', 'Submitted'), ('validated', 'Validated'), ('rejected', 'Rejected')]`, Default: `'submitted'`, Tracking: True, String: "Status"): Workflow status of the submission.
    *   `notes` (Type: `fields.Text`, String: "Internal Notes"): Internal remarks or notes about the submission.
*   **Methods:**
    *   `_compute_name(self)`:
        *   **Logic:** Generates a name like "Form [Form Name] / [Farmer Name] / [Date]".
        *   **Dependencies:** `farmer_id.name`, `form_version_id.name`, `submission_date`.
    *   `action_validate_submission(self)`:
        *   **Logic:** Sets `state` to `'validated'`. Potentially triggers notifications or other workflows.
    *   `action_reject_submission(self)`:
        *   **Logic:** Sets `state` to `'rejected'`.
*   **Requirement Mapping:** `REQ-3-008`

#### 3.1.5. `dfr.form.response` (Dynamic Form Response)
*   **Description:** Stores the actual answer/value for a specific field within a form submission.
*   **Odoo Model Name:** `dfr.form.response`
*   **Fields:**
    *   `submission_id` (Type: `fields.Many2one`, Comodel: `dfr.form.submission`, Required: True, Ondelete: `cascade`, String: "Submission"): Link to the parent submission.
    *   `field_id` (Type: `fields.Many2one`, Comodel: `dfr.form.field`, Required: True, Ondelete: `restrict`, String: "Form Field"): The specific field this response corresponds to.
    *   `field_label` (Type: `fields.Char`, Related: `field_id.label`, String: "Field Label", Readonly: True, Store: True): Copied for easier reporting.
    *   `field_type` (Type: `fields.Selection`, Related: `field_id.field_type`, String: "Field Type", Readonly: True, Store: True): Copied for easier reporting and value interpretation.
    *   `value_text` (Type: `fields.Text`, String: "Text Value"): For `text`, `computed_text` field types.
    *   `value_number` (Type: `fields.Float`, String: "Number Value", Digits: `(16, 4)`): For `number` field type.
    *   `value_date` (Type: `fields.Date`, String: "Date Value"): For `date` field type.
    *   `value_datetime` (Type: `fields.Datetime`, String: "Datetime Value"): For `datetime` field type.
    *   `value_boolean` (Type: `fields.Boolean`, String: "Boolean Value"): For `boolean` field type.
    *   `value_selection` (Type: `fields.Char`, String: "Selection Value (Key)"): For `selection` field type (stores the key of the selected option).
    *   `value_multi_selection_ids` (Type: `fields.Many2many`, Comodel: `dfr.form.selection.option.answer`, Relation: `dfr_form_response_selection_option_rel`, Column1: `response_id`, Column2: `option_id`, String: "Multi-Selection Values"): For `multi_selection` field type.
    *   `value_gps_latitude` (Type: `fields.Float`, String: "GPS Latitude", Digits: `(10, 7)`): For `gps_point` field type.
    *   `value_gps_longitude` (Type: `fields.Float`, String: "GPS Longitude", Digits: `(10, 7)`): For `gps_point` field type.
    *   `value_attachment_name` (Type: `fields.Char`, String: "Attachment Name"): Stores the filename for `image`/`file` types.
    *   `value_attachment_data` (Type: `fields.Binary`, String: "Attachment Data"): Stores the binary data for `image`/`file` types. (Alternatively, could use `ir.attachment` and a Many2one here).
        *   **Note:** Using `ir.attachment` is generally preferred for better file management in Odoo. If so, this field would be `value_attachment_id` (Type: `fields.Many2one`, Comodel: `ir.attachment`). The current structure specifies direct binary. Decision based on project preference. For this SDS, assuming `ir.attachment` is preferred.
    *   `value_attachment_id` (Type: `fields.Many2one`, Comodel: `ir.attachment`, String: "Attachment Value"): For `image` type.
*   **Methods:**
    *   `get_display_value(self)`:
        *   **Logic:** Based on `self.field_type`, retrieves and formats the appropriate `value_*` field for display. For selections, it might fetch the label corresponding to the stored key. For multi-selections, it concatenates labels.
        *   **Returns:** `str` representation of the value.
*   **Requirement Mapping:** `REQ-3-008`

#### 3.1.6. `dfr.form.selection.option.answer` (Helper Model for Multi-Selection Answers)
*   **Description:** A helper model to store the actual selected option keys and their display labels for `multi_selection` field types in form responses. This allows a clean Many2many relationship.
*   **Odoo Model Name:** `dfr.form.selection.option.answer`
*   **Fields:**
    *   `name` (Type: `fields.Char`, Required: True, String: "Option Value (Key)"): The internal key/value of the selection option (e.g., 'opt1').
    *   `display_name` (Type: `fields.Char`, String: "Option Label", Compute: `_compute_display_name`, Store: True): The user-friendly label for the option (e.g., 'Option 1'). Can be made editable or computed based on `name` if a global option list is not used.
*   **Methods:**
    *   `_compute_display_name(self)`:
        *   **Logic:** If labels are not stored directly, this could try to find a label or simply use `name`. For simplicity, it's better if `display_name` is also stored/set when these records are created/used.
*   **Requirement Mapping:** `REQ-3-008` (implicitly supports multi-selection storage)

## 4. Application Services Design

### 4.1. `FormDefinitionService` (`form_definition_service.py`)
*   **Description:** Handles business logic for creating, versioning, publishing, and retrieving dynamic form definitions.
*   **Methods:**
    *   `create_form_master(self, env, form_data)`:
        *   **Input:** `env` (Odoo environment), `form_data` (dict: {'name': str, 'description': str, 'country_id': int (optional)}).
        *   **Logic:** Creates a new `dfr.form` record.
        *   **Output:** `dfr.form` recordset.
    *   `create_new_form_version(self, env, form_master_id, version_data=None, source_version_id=None)`:
        *   **Input:** `env`, `form_master_id` (int), `version_data` (dict: {'description': str} optional), `source_version_id` (int, optional: ID of `dfr.form.version` to copy fields from).
        *   **Logic:**
            1.  Creates a new `dfr.form.version` record linked to `form_master_id`.
            2.  Sets `version_number` using `ir.sequence`.
            3.  If `source_version_id` is provided, iterates through its `field_ids` and creates copies linked to the new version.
        *   **Output:** `dfr.form.version` recordset.
    *   `publish_form_version(self, env, form_version_id)`:
        *   **Input:** `env`, `form_version_id` (int).
        *   **Logic:** Calls `action_publish()` on the `dfr.form.version` record. Handles potential exceptions.
        *   **Output:** `bool` (success).
    *   `archive_form_version(self, env, form_version_id)`:
        *   **Input:** `env`, `form_version_id` (int).
        *   **Logic:** Calls `action_archive()` on the `dfr.form.version` record.
        *   **Output:** `bool` (success).
    *   `get_form_definition_for_rendering(self, env, form_version_id)`:
        *   **Input:** `env`, `form_version_id` (int).
        *   **Logic:**
            1.  Fetches the `dfr.form.version` record.
            2.  Iterates through its `field_ids`, ordering by `sequence`.
            3.  For each field, constructs a dictionary containing relevant properties: `name`, `label`, `field_type`, `is_required` (from form level), `help_text`, `placeholder`, `selection_options` (parsed), `validation_rules` (consolidated from individual rule fields), `conditional_logic_json` (parsed if valid), `default_value_*`.
            4.  Returns a dictionary like: `{'form_name': str, 'form_version': str, 'fields': [field_dict1, field_dict2, ...]}`.
        *   **Output:** `dict` representing the form structure.
    *   `add_field_to_version(self, env, form_version_id, field_data)`:
        *   **Input:** `env`, `form_version_id` (int), `field_data` (dict containing data for `dfr.form.field`).
        *   **Logic:** Ensures `form_version_id` is in 'draft' state. Creates a new `dfr.form.field` record linked to the version.
        *   **Output:** `dfr.form.field` recordset.
    *   `update_field_in_version(self, env, field_id, field_data)`:
        *   **Input:** `env`, `field_id` (int), `field_data` (dict with fields to update).
        *   **Logic:** Ensures the parent `form_version_id` is in 'draft' state. Updates the `dfr.form.field` record.
        *   **Output:** `bool` (success).
    *   `remove_field_from_version(self, env, field_id)`:
        *   **Input:** `env`, `field_id` (int).
        *   **Logic:** Ensures the parent `form_version_id` is in 'draft' state. Deletes the `dfr.form.field` record.
        *   **Output:** `bool` (success).
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-004`

### 4.2. `FormSubmissionService` (`form_submission_service.py`)
*   **Description:** Processes and stores dynamic form submissions.
*   **Methods:**
    *   `process_submission(self, env, farmer_uid_or_id, form_version_id, responses_data, submitted_by_user_id=None, submission_source='admin')`:
        *   **Input:** `env`, `farmer_uid_or_id` (str UID or int ID of `dfr.farmer`), `form_version_id` (int), `responses_data` (dict: `{field_technical_name: value}`), `submitted_by_user_id` (int, optional), `submission_source` (str).
        *   **Logic:**
            1.  Retrieve `dfr.farmer` record using `farmer_uid_or_id`. Raise error if not found.
            2.  Retrieve `dfr.form.version` record. Raise error if not found or not published.
            3.  Call `FormValidationService.validate_submission_responses()` with `form_version_id` and `responses_data`. If invalid, raise `ValidationError` with error details.
            4.  Create `dfr.form.submission` record, linking `farmer_id`, `form_version_id`, `submitted_by_user_id`, `submission_source`.
            5.  Iterate `responses_data`. For each `field_technical_name` and `value`:
                *   Find the corresponding `dfr.form.field` record in `form_version_id.field_ids`.
                *   Create a `dfr.form.response` record linked to the submission and field.
                *   Populate the correct `value_*` field in `dfr.form.response` based on `field.field_type`. Handle multi-selection by finding/creating `dfr.form.selection.option.answer` records and linking them. Handle attachments by creating `ir.attachment` records if `value_attachment_id` is used.
        *   **Output:** `dfr.form.submission` recordset.
    *   `get_farmer_submissions(self, env, farmer_id, form_master_id=None)`:
        *   **Input:** `env`, `farmer_id` (int), `form_master_id` (int, optional).
        *   **Logic:** Searches `dfr.form.submission` records for the given `farmer_id`. If `form_master_id` is provided, further filters by `form_version_id.form_master_id`.
        *   **Output:** `dfr.form.submission` recordset.
*   **Requirement Mapping:** `REQ-3-008`

### 4.3. `FormValidationService` (`form_validation_service.py`)
*   **Description:** Handles complex validation logic for dynamic form fields.
*   **Methods:**
    *   `validate_field_response(self, env, form_field_record, response_value)`:
        *   **Input:** `env`, `form_field_record` (`dfr.form.field` recordset), `response_value`.
        *   **Logic:**
            1.  Check `form_field_record.validation_rule_required`: if True and `response_value` is empty/None, return (False, "Field is required").
            2.  Based on `form_field_record.field_type`:
                *   **Text:** Check `min_length`, `max_length`. Check `regex` if provided.
                *   **Number:** Check `min_value`, `max_value`. Ensure `response_value` is a valid number.
                *   **Date/Datetime:** Ensure `response_value` is a valid date/datetime format.
                *   **Selection/Multi-Selection:** Ensure `response_value`(s) are among `form_field_record.get_selection_options_parsed()` keys.
            3.  If any rule fails, return (False, `form_field_record.validation_error_message` or a default error message).
            4.  If all pass, return (True, None).
        *   **Output:** `tuple (bool, str|None)`
    *   `validate_submission_responses(self, env, form_version_record, responses_dict)`:
        *   **Input:** `env`, `form_version_record` (`dfr.form.version` recordset), `responses_dict` (dict: `{field_technical_name: value}`).
        *   **Logic:**
            1.  Initialize `all_valid = True`, `errors = {}`.
            2.  Iterate through `form_version_record.field_ids`. For each `field_record`:
                *   Get the `response_value` from `responses_dict` using `field_record.name`.
                *   Call `self.validate_field_response(env, field_record, response_value)`.
                *   If invalid, set `all_valid = False` and add error message to `errors[field_record.name]`.
        *   **Output:** `tuple (bool, dict)` where dict is `{field_technical_name: error_message}`.
*   **Requirement Mapping:** `REQ-3-002`

## 5. Wizard Design

### 5.1. `FormVersionWizard` (`form_version_wizard.py`)
*   **Description:** Odoo wizard (TransientModel) for creating a new version of a dynamic form.
*   **Odoo Model Name:** `dfr.form.version.wizard`
*   **Fields:**
    *   `form_master_id` (Type: `fields.Many2one`, Comodel: `dfr.form`, Required: True, String: "Form Master"): The master form for which to create a new version. Defaulted from context if action is called from `dfr.form`.
    *   `source_version_id` (Type: `fields.Many2one`, Comodel: `dfr.form.version`, String: "Copy Fields From (Optional)", Domain: `"[('form_master_id', '=', form_master_id)]"`): Optional existing version to copy fields from.
    *   `new_version_description` (Type: `fields.Text`, String: "New Version Description"): Description for the new version.
*   **Methods:**
    *   `action_create_version(self)`:
        *   **Logic:**
            1.  Validates input (e.g., `form_master_id` is set).
            2.  Calls `FormDefinitionService.create_new_form_version()` with `self.form_master_id.id`, `version_data={'description': self.new_version_description}`, and `source_version_id=self.source_version_id.id` if set.
            3.  If successful, returns an action to open the form view of the newly created `dfr.form.version`.
        *   **Output:** Odoo action dictionary.
*   **Requirement Mapping:** `REQ-3-004`

## 6. User Interface Design

### 6.1. Views

#### 6.1.1. `dfr_form_views.xml`
*   **Purpose:** Defines Odoo backend UI for managing `dfr.form` (masters) and `dfr.form.version` (versions), including the form builder.
*   **Models Covered:** `dfr.form`, `dfr.form.version`, `dfr.form.field`.
*   **Key UI Elements:**
    *   **`dfr.form` Views:**
        *   Tree view: Lists form masters with columns like Name, Current Published Version, Country.
        *   Form view: Displays master form details, smart buttons to "View Versions" and "Create New Version".
        *   Search view: Allows searching by name, country.
    *   **`dfr.form.version` Views:**
        *   Tree view: Lists form versions with columns like Form Name (master), Version Number, Status, Publish Date, Submission Count.
        *   Form view (Form Builder):
            *   Header: Displays version details (master name, version number, status), action buttons (Publish, Archive, Set to Draft, Copy Version). Fields are editable only if `is_editable` is True.
            *   Notebook/Tabs:
                *   "Fields": Main design area. Displays `field_ids` (One2many list).
                    *   Each row in the `field_ids` list allows editing `label`, `name` (technical), `field_type`, `sequence`, `is_required`.
                    *   Buttons/icons per field row for: "Edit Details" (opens modal for advanced properties like help text, placeholder, defaults, validation rules, conditional logic), "Delete Field".
                    *   Button to "Add Field".
                    *   **Potential for Custom Widget:** This "Fields" tab could be replaced/enhanced by `form_builder_widget.js` for drag-and-drop, rich previews, etc.
                *   "Settings": Version description, status details.
        *   Search view: Allows searching by form master name, version number, status.
    *   **`dfr.form.field` Views (mostly for modal dialogs invoked from form builder):**
        *   Form view (modal): For detailed editing of a field's properties: label, technical name, type, help text, placeholder, default values, selection options (textarea), validation rules (separate boolean/integer/char fields for each rule type), conditional logic (textarea for JSON or a more structured UI if a custom widget is built).
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-002`, `REQ-3-003`, `REQ-3-004`

#### 6.1.2. `dfr_form_submission_views.xml`
*   **Purpose:** Defines Odoo backend UI for viewing and managing form submissions.
*   **Models Covered:** `dfr.form.submission`, `dfr.form.response`.
*   **Key UI Elements:**
    *   **`dfr.form.submission` Views:**
        *   Tree view: Lists submissions with columns like Submission Reference, Farmer, Form Version, Submission Date, Status.
        *   Form view:
            *   Header: Submission metadata (reference, farmer, form version, date, submitter, source, status). Buttons for `action_validate_submission`, `action_reject_submission`.
            *   Notebook/Tabs:
                *   "Responses": Displays `response_ids` (One2many list). Each row shows `field_label`, `field_type`, and the `get_display_value()` of the response. Responses should be read-only.
                *   "Notes": Text field for internal notes.
                *   "Chatter": For activities and audit trail.
        *   Search view: Allows searching by farmer, form version, submission date, status.
        *   Pivot/Graph views: For basic analytics on submissions (e.g., count by form, by status).
*   **Requirement Mapping:** `REQ-3-008`, `REQ-3-010` (implicitly, as data for dashboards/exports comes from these models/views)

#### 6.1.3. `form_version_wizard_views.xml`
*   **Purpose:** Defines the UI for the `dfr.form.version.wizard`.
*   **Models Covered:** `dfr.form.version.wizard`.
*   **Key UI Elements:**
    *   Form view (modal):
        *   Field for `form_master_id` (Many2one, readonly if opened from master form).
        *   Field for `source_version_id` (Many2one, optional, domain filtered by `form_master_id`).
        *   Field for `new_version_description` (Text).
        *   Buttons: "Create Version", "Cancel".
*   **Requirement Mapping:** `REQ-3-004`

### 6.2. Menus (`dfr_dynamic_forms_menus.xml`)
*   **Purpose:** Provides navigation entries in the Odoo backend.
*   **Structure:**
    *   Main Menu: "Digital Farmer Registry" (likely from `dfr_common` or `dfr_farmer_registry`)
        *   Sub-Menu: "Dynamic Forms"
            *   Menu Item: "Forms" (Action: `action_dfr_form_master_tree` - opens `dfr.form` tree view)
            *   Menu Item: "All Form Versions" (Action: `action_dfr_form_version_tree` - opens `dfr.form.version` tree view, ungrouped)
            *   Menu Item: "Submissions" (Action: `action_dfr_form_submission_tree` - opens `dfr.form.submission` tree view)
*   **Requirement Mapping:** `REQ-3-001`

## 7. Frontend Components (Static Resources)

### 7.1. `form_builder_widget.js`
*   **Purpose:** Custom Odoo JavaScript widget to enhance the form building experience within the `dfr.form.version` form view.
*   **Main Functionalities:**
    *   Render a visual representation of the form fields (`_renderFields`).
    *   Allow adding new fields, potentially from a palette of field types (`_onAddField`).
    *   Allow editing existing field properties through modals or inline editors (`_onEditField`).
        *   Modal for Conditional Logic (`_configureConditionalLogic`): UI to build JSON for `conditional_logic_json`. This could involve selecting a trigger field, operator, and value.
        *   Modal for Validation Rules (`_configureValidationRules`): UI to set values for `validation_rule_*` fields.
    *   Allow deleting fields (`_onDeleteField`).
    *   Support drag-and-drop reordering of fields (updates `sequence` field).
*   **Interaction with Backend:**
    *   Uses Odoo RPC calls to `FormDefinitionService` or directly to model methods (`create`, `write`, `unlink` on `dfr.form.field`) to persist changes.
    *   Fetches initial field data when the widget loads.
*   **Requirement Mapping:** `REQ-3-001`, `REQ-3-002`, `REQ-3-003`

### 7.2. `form_builder_templates.xml`
*   **Purpose:** OWL templates for rendering the UI of `form_builder_widget.js`.
*   **Key Templates:**
    *   Main form builder container.
    *   Template for rendering a single field item in the list (with edit/delete controls).
    *   Template for the field type palette (if implemented).
    *   Templates for modal dialogs (e.g., field property editor, conditional logic builder, validation rule editor).
*   **Requirement Mapping:** `REQ-3-001`

### 7.3. `form_builder.scss`
*   **Purpose:** Custom SCSS/CSS for styling the form builder widget and its components.
*   **Styling Targets:**
    *   Overall layout of the form builder area.
    *   Appearance of field items, drag handles.
    *   Styling of modal dialogs and input elements within them.
*   **Requirement Mapping:** `REQ-3-001`

## 8. Security Design

### 8.1. `ir.model.access.csv`
*   **Purpose:** Defines model-level CRUD (Create, Read, Update, Delete) permissions for dynamic form related models based on user groups/roles.
*   **General Approach:**
    *   **National Administrator Group (from `dfr_rbac_config`):**
        *   `dfr.form`: Full CRUD.
        *   `dfr.form.version`: Full CRUD.
        *   `dfr.form.field`: Full CRUD.
        *   `dfr.form.submission`: Full CRUD.
        *   `dfr.form.response`: Full CRUD.
    *   **Supervisor Group (from `dfr_rbac_config`):**
        *   `dfr.form`, `dfr.form.version`, `dfr.form.field`: Read-only.
        *   `dfr.form.submission`: Read, Update (e.g., to change state, add notes). Create/Delete might be restricted.
        *   `dfr.form.response`: Read-only.
    *   **Enumerator Group (from `dfr_rbac_config`):**
        *   `dfr.form`, `dfr.form.version`, `dfr.form.field`: Read-only (for rendering forms).
        *   `dfr.form.submission`: Create (via specific services/controllers), Read (own/assigned). Update/Delete typically restricted.
        *   `dfr.form.response`: Create (as part of submission), Read (own/assigned).
    *   Other roles (e.g., Farmer Portal User, Public User) will likely not have direct model access here but through controllers/API layers with specific permissions.
*   **Requirement Mapping:** `REQ-3-001` and implicitly for all operations on these models.

### 8.2. `dfr_dynamic_forms_security.xml`
*   **Purpose:** Defines record rules for fine-grained access control if needed.
*   **Potential Record Rules:**
    *   If `dfr.form` has a `country_id`, a record rule could restrict National Administrators to only see/manage forms associated with their country.
        *   `Domain Filter`: `[('country_id', '=', user.country_id.id)]` (assuming `user.country_id` is available).
    *   Rules for `dfr.form.submission` visibility based on enumerator assignment or geographic area if such logic is implemented within this module's scope (otherwise handled by RBAC in conjunction with farmer data access).
*   **Requirement Mapping:** `REQ-3-001`

## 9. Data Initialization

### 9.1. `data/ir_sequence_data.xml`
*   **Purpose:** To define Odoo sequences for automatic number generation.
*   **Content:**
    *   Definition for `ir.sequence` with code `dfr.form.version.sequence` to generate version numbers for `dfr.form.version`.
        *   Example: `prefix = "V"`, `padding = 3`.
*   **Requirement Mapping:** `REQ-3-004`

### 9.2. `data/dfr_form_field_types_data.xml`
*   **Purpose:** This file is generally not needed if `field_type` is a simple selection on `dfr.form.field`. If, in the future, field types become more complex entities themselves (e.g., managed as separate `dfr.form.field.type` model with icons, specific behaviors defined via data), this file would populate those. For the current design based on the file structure, this file is likely minimal or primarily for other sequences if needed, beyond the version sequence.
*   **Current Use:** As specified in `file_structure_json`, if it's only for sequences, its content should be merged into `ir_sequence_data.xml` or clarified. Assuming minimal use or just sequences for now.
*   **Requirement Mapping:** `REQ-3-001`

## 10. Module Dependencies (`__manifest__.py`)
*   `'name'`: "DFR Dynamic Form Engine"
*   `'summary'`: "Module for creating and managing dynamic data collection forms."
*   `'version'`: "18.0.1.0.0"
*   `'category'`: "Digital Farmer Registry/Application"
*   `'author'`: "FAO"
*   `'license'`: "MIT" or "Apache-2.0" (as per project decision)
*   `'depends'`: `['base', 'mail', 'dfr_common', 'dfr_farmer_registry', 'dfr_rbac_config']`
*   `'data'`:
    *   `security/ir.model.access.csv`
    *   `security/dfr_dynamic_forms_security.xml`
    *   `data/ir_sequence_data.xml`
    *   `views/dfr_form_views.xml`
    *   `views/dfr_form_submission_views.xml`
    *   `views/form_version_wizard_views.xml`
    *   `views/dfr_dynamic_forms_menus.xml`
*   `'assets'`:
    *   `web.assets_backend`:
        *   `dfr_dynamic_forms/static/src/js/form_builder_widget.js`
        *   `dfr_dynamic_forms/static/src/xml/form_builder_templates.xml`
        *   `dfr_dynamic_forms/static/src/scss/form_builder.scss`
*   `'installable'`: True
*   `'application'`: False
*   `'auto_install'`: False

## 11. Error Handling and Logging
*   **Error Handling:**
    *   Service layer methods should raise Odoo standard exceptions (e.g., `UserError`, `ValidationError`) for business rule violations or invalid operations. These are then handled by Odoo's UI to display user-friendly messages.
    *   Unexpected errors should be logged comprehensively.
*   **Logging:**
    *   Use Odoo's standard logging mechanism (`_logger = logging.getLogger(__name__)`).
    *   Log important events, service method entry/exit at DEBUG level if needed, and any errors/exceptions at ERROR level.
    *   Audit tracking for creation/modification of key records (`dfr.form`, `dfr.form.version`, `dfr.form.submission`) will be handled by inheriting `mail.thread` and `mail.activity.mixin`.

## 12. Future Considerations / Scalability
*   **Complex Conditional Logic UI:** The `conditional_logic_json` field is simple for storage but complex for users. The `form_builder_widget.js` should aim to provide a guided UI to construct this JSON, abstracting its complexity.
*   **Computed Fields (`computed_text`):** The logic for 'computed_text' fields needs to be defined. This might involve Python expressions evaluated server-side or simple JavaScript client-side based on other field values. The current SDS focuses on storage and definition; computation logic will need further specification if complex server-side computation is required.
*   **Performance of Form Rendering:** For very long forms or complex conditional logic, client-side rendering performance (JavaScript, OWL) will be a key consideration.
*   **API for Form Definitions & Submissions:** While this module focuses on backend management, its services (`FormDefinitionService`, `FormSubmissionService`) will be consumed by the DFR REST API module (`DFR_MOD_REST_API`) to expose form structures to mobile/portal clients and accept submissions. The `get_form_definition_for_rendering` method is key for this.

This SDS provides a comprehensive plan for developing the `dfr_dynamic_forms` module, aligning with the provided file structure and user requirements.