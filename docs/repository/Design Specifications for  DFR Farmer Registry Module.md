# Software Design Specification: DFR Farmer Registry Module (dfr_farmer_registry)

## 1. Introduction

The DFR Farmer Registry Module (`dfr_farmer_registry`) is a core component of the Digital Farmer Registry (DFR) system, built as an Odoo 18.0 Community addon. Its primary responsibility is to manage the foundational data related to farmers, their households, farms, and associated land plots. This module implements essential functionalities such as Create, Read, Update, Delete (CRUD) operations for these entities, generation of unique identifiers (UIDs), management of farmer and household status workflows, Know Your Customer (KYC) processes, farmer consent management, and de-duplication logic to ensure data integrity.

The data managed by this module is exposed to users via the Odoo Admin Portal and can be accessed programmatically through the API Gateway module for mobile application synchronization and external system integrations.

**Relevant Requirements:** REQ-FHR-001, REQ-FHR-002, REQ-FHR-006, REQ-FHR-011, REQ-FHR-012, REQ-FHR-015, REQ-FHR-018.

## 2. Module Structure

The module will follow the standard Odoo addon structure:


dfr_addons/dfr_farmer_registry/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── dfr_farmer.py
│   ├── dfr_household.py
│   ├── dfr_household_member.py
│   ├── dfr_farm.py
│   └── dfr_plot.py
├── services/
│   ├── __init__.py
│   ├── dfr_deduplication_service.py
│   ├── dfr_consent_service.py
│   └── dfr_kyc_service.py
├── wizards/
│   ├── __init__.py
│   ├── dfr_deduplication_review_wizard.py
│   └── dfr_farmer_kyc_wizard.py
├── data/
│   ├── dfr_sequences.xml
│   ├── dfr_farmer_status_data.xml
│   ├── dfr_national_id_type_data.xml
│   └── dfr_automated_actions.xml
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── dfr_farmer_views.xml
│   ├── dfr_household_views.xml
│   ├── dfr_farm_views.xml
│   ├── dfr_plot_views.xml
│   ├── dfr_menu_views.xml
│   ├── dfr_deduplication_review_wizard_views.xml
│   └── dfr_farmer_kyc_wizard_views.xml
└── static/
    └── description/
        └── icon.png


## 3. Data Models (`models/`)

This section details the Odoo models that define the data structures and core business logic for the farmer registry. All models will inherit from `mail.thread` and `mail.activity.mixin` for communication and activity tracking, and from a base model provided by `dfr_common_core` if it includes shared audit fields or UID logic.

### 3.1. `dfr_farmer.py` (Model: `dfr.farmer`)

*   **Purpose:** Represents and manages individual farmer data.
*   **Inherits:** `mail.thread`, `mail.activity.mixin` (and potentially `dfr.base.model` from `dfr_common_core`).
*   **Requirements:** REQ-FHR-001, REQ-FHR-002, REQ-FHR-003, REQ-FHR-006, REQ-FHR-008, REQ-FHR-010, REQ-FHR-011, REQ-FHR-012, REQ-FHR-018.

*   **Fields:**
    *   `uid`: `fields.Char(string='Farmer UID', required=True, readonly=True, copy=False, index=True, help="Unique Farmer Identifier")` - Generated automatically.
    *   `name`: `fields.Char(string='Full Name', required=True, tracking=True)`
    *   `date_of_birth`: `fields.Date(string='Date of Birth', tracking=True)`
    *   `sex`: `fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Sex', tracking=True)`
    *   `role_in_household`: `fields.Selection([...], string='Role in Household', tracking=True)` - Options to be defined (e.g., 'Head', 'Spouse', 'Child').
    *   `education_level_id`: `fields.Many2one('dfr.education.level', string='Education Level', tracking=True)` (Assumes a `dfr.education.level` model for configurable levels).
    *   `contact_phone`: `fields.Char(string='Phone Number', tracking=True)`
    *   `contact_email`: `fields.Char(string='Email Address', tracking=True)`
    *   `national_id_type_id`: `fields.Many2one('dfr.national.id.type', string='National ID Type', tracking=True)` (Assumes a `dfr.national.id.type` model).
    *   `national_id_number`: `fields.Char(string='National ID Number', tracking=True)`
    *   `kyc_status`: `fields.Selection([('not_started', 'Not Started'), ('pending_review', 'Pending Review'), ('verified', 'Verified'), ('rejected', 'Rejected')], string='KYC Status', default='not_started', required=True, tracking=True)`
    *   `kyc_verification_date`: `fields.Date(string='KYC Verification Date', readonly=True, tracking=True)`
    *   `kyc_reviewer_id`: `fields.Many2one('res.users', string='KYC Reviewer', readonly=True, tracking=True)`
    *   `kyc_review_notes`: `fields.Text(string='KYC Review Notes', tracking=True)`
    *   `status`: `fields.Selection([('pending_verification', 'Pending Verification'), ('active', 'Active'), ('inactive', 'Inactive'), ('deceased', 'Deceased'), ('duplicate', 'Potential Duplicate'), ('archived', 'Archived')], string='Farmer Status', default='pending_verification', required=True, tracking=True, help="Lifecycle status of the farmer record.")`
    *   `household_ids`: `fields.One2many('dfr.household_member', 'farmer_id', string='Households')`
    *   `farm_ids`: `fields.One2many('dfr.farm', 'farmer_id', string='Farms')`
    *   `administrative_area_id`: `fields.Many2one('dfr.administrative.area', string='Administrative Area', tracking=True)` (Assumes `dfr.administrative.area` model from `dfr_common_core` or similar).
    *   `gps_latitude_homestead`: `fields.Float(string='Homestead Latitude', digits=(10, 7), tracking=True)`
    *   `gps_longitude_homestead`: `fields.Float(string='Homestead Longitude', digits=(10, 7), tracking=True)`
    *   `consent_status`: `fields.Selection([('pending', 'Pending'), ('given', 'Given'), ('withdrawn', 'Withdrawn')], string='Consent Status', default='pending', required=True, tracking=True)`
    *   `consent_date`: `fields.Datetime(string='Consent Date', readonly=True, tracking=True)`
    *   `consent_version_agreed`: `fields.Char(string='Consent Version Agreed', tracking=True)`
    *   `consent_purpose_ids`: `fields.Many2many('dfr.consent.purpose', string='Consent Purposes', tracking=True)` (Assumes a `dfr.consent.purpose` model).
    *   `consent_withdrawal_date`: `fields.Datetime(string='Consent Withdrawal Date', readonly=True, tracking=True)`
    *   `consent_withdrawal_reason`: `fields.Text(string='Consent Withdrawal Reason', tracking=True)`
    *   `deduplication_potential_duplicate_ids`: `fields.Many2many('dfr.farmer', 'dfr_farmer_duplicate_rel', 'farmer_id', 'duplicate_id', string='Potential Duplicates', help="Other farmers identified as potential duplicates.")`
    *   `deduplication_master_farmer_id`: `fields.Many2one('dfr.farmer', string='Merged Into Master', readonly=True, copy=False, help="If this record was merged, points to the master record.")`

*   **SQL Constraints:**
    *   `_sql_constraints = [('national_id_number_uniq', 'unique(national_id_number, national_id_type_id, company_id)', 'National ID Number must be unique per ID type within the country!')]` - Conditionally applied if `national_id_number` is present. `company_id` ensures uniqueness per country instance.
    *   `_sql_constraints = [('uid_uniq', 'unique(uid, company_id)', 'Farmer UID must be unique within the country!')]`

*   **Methods:**
    *   `_compute_default_uid(self)`:
        *   **Logic:** Called at creation if UID is not provided. Generates a UID using `ir.sequence` (defined in `dfr_sequences.xml`, e.g., `dfr.farmer.uid.sequence`) or Python `uuid.uuid4().hex`. Stores it in the `uid` field.
        *   **REQ:** REQ-FHR-002.
    *   `create(self, vals_list)`:
        *   **Logic:** Overrides default create. Calls `_compute_default_uid` if `uid` is not in `vals`. Calls `super().create()`. Logs creation.
        *   **REQ:** REQ-FHR-001, REQ-FHR-010.
    *   `write(self, vals)`:
        *   **Logic:** Overrides default write. Logs changes to tracked fields. Calls `super().write()`.
        *   **REQ:** REQ-FHR-010.
    *   `unlink(self)`:
        *   **Logic:** Overrides default unlink. Implements logical delete (sets `status` to 'archived' or an `active` boolean field to `False`) rather than physical delete, or checks permissions before allowing physical delete. Logs deletion.
        *   **REQ:** REQ-FHR-010.
    *   `action_request_kyc_review(self)`:
        *   **Logic:** Sets `kyc_status` to 'pending_review'. Creates an activity for the KYC review team.
        *   **Called by:** Button on farmer form view.
        *   **REQ:** REQ-FHR-006.
    *   `action_process_kyc_manual(self, outcome, notes, reviewer_id)`: (May be part of KYC Service, called by wizard)
        *   **Logic:** Updates `kyc_status` (to 'verified' or 'rejected'), `kyc_verification_date`, `kyc_reviewer_id`, `kyc_review_notes`. If 'verified', may trigger farmer status change to 'active' if 'pending_verification'.
        *   **REQ:** REQ-FHR-006, REQ-FHR-011.
    *   `action_set_status_active(self)`:
        *   **Logic:** Sets `status` to 'active'. Logs event.
        *   **REQ:** REQ-FHR-011.
    *   `action_set_status_inactive(self)`:
        *   **Logic:** Sets `status` to 'inactive'. Logs event.
        *   **REQ:** REQ-FHR-011.
    *   `action_set_status_deceased(self)`:
        *   **Logic:** Sets `status` to 'deceased'. Logs event.
        *   **REQ:** REQ-FHR-011.
    *   `_onchange_check_potential_duplicates(self)`: `@api.onchange('name', 'national_id_number', ...)`
        *   **Logic:** When key identifying fields change, calls `self.env['dfr.deduplication.service'].find_potential_duplicates(self._get_current_farmer_data())`. If potential duplicates are found, shows a warning to the user (Odoo's warning mechanism). Does not prevent saving but flags the record or suggests review.
        *   **REQ:** REQ-FHR-012.
    *   `action_open_deduplication_review(self)`:
        *   **Logic:** Opens the `dfr.deduplication.review.wizard` for the selected farmer(s) who are flagged as potential duplicates or need manual review.
        *   **REQ:** REQ-FHR-015.
    *   `action_record_consent(self, consent_version_agreed, consent_purpose_ids)`: (May be part of Consent Service, called by wizard/button)
        *   **Logic:** Updates `consent_status` to 'given', `consent_date` to now, `consent_version_agreed`, `consent_purpose_ids`. Logs the consent action.
        *   **REQ:** REQ-FHR-018.
    *   `action_withdraw_consent(self, withdrawal_reason)`: (May be part of Consent Service, called by wizard/button)
        *   **Logic:** Updates `consent_status` to 'withdrawn', `consent_withdrawal_date` to now, `consent_withdrawal_reason`. Logs the withdrawal.
        *   **REQ:** REQ-FHR-018.

### 3.2. `dfr_household.py` (Model: `dfr.household`)

*   **Purpose:** Represents and manages household data.
*   **Inherits:** `mail.thread`, `mail.activity.mixin`.
*   **Requirements:** REQ-FHR-001, REQ-FHR-002, REQ-FHR-004, REQ-FHR-011.

*   **Fields:**
    *   `uid`: `fields.Char(string='Household UID', required=True, readonly=True, copy=False, index=True, help="Unique Household Identifier")`
    *   `name`: `fields.Char(string='Household Name', compute='_compute_household_name', store=True, help="Typically derived from Head of Household's name")`
    *   `head_of_household_id`: `fields.Many2one('dfr.farmer', string='Head of Household', tracking=True, domain="[('status', '=', 'active')]")`
    *   `member_ids`: `fields.One2many('dfr.household_member', 'household_id', string='Household Members')`
    *   `status`: `fields.Selection([('active', 'Active'), ('inactive', 'Inactive'), ('dissolved', 'Dissolved')], string='Household Status', default='active', required=True, tracking=True)`
    *   `farm_ids`: `fields.One2many('dfr.farm', 'household_id', string='Farms')`
    *   `administrative_area_id`: `fields.Many2one(related='head_of_household_id.administrative_area_id', string='Administrative Area', store=True, readonly=True)`

*   **SQL Constraints:**
    *   `_sql_constraints = [('uid_uniq', 'unique(uid, company_id)', 'Household UID must be unique within the country!')]`

*   **Methods:**
    *   `_compute_default_uid(self)`:
        *   **Logic:** Generates UID using `ir.sequence` (e.g., `dfr.household.uid.sequence`) or `uuid.uuid4().hex`.
        *   **REQ:** REQ-FHR-002.
    *   `create(self, vals_list)`:
        *   **Logic:** Overrides. Calls `_compute_default_uid`. Logs creation.
        *   **REQ:** REQ-FHR-001, REQ-FHR-010.
    *   `write(self, vals)`:
        *   **Logic:** Overrides. Logs changes.
        *   **REQ:** REQ-FHR-010.
    *   `_compute_household_name(self)`: `@api.depends('head_of_household_id')`
        *   **Logic:** Sets household name, e.g., "Household of [Head's Name]".
    *   `action_set_status_active(self)`: Sets `status` to 'active'.
    *   `action_set_status_inactive(self)`: Sets `status` to 'inactive'.
    *   `action_set_status_dissolved(self)`: Sets `status` to 'dissolved'.

### 3.3. `dfr_household_member.py` (Model: `dfr.household_member`)

*   **Purpose:** Represents individual members linked to a household.
*   **Inherits:** `mail.thread`.
*   **Requirements:** REQ-FHR-001, REQ-FHR-004.

*   **Fields:**
    *   `household_id`: `fields.Many2one('dfr.household', string='Household', required=True, ondelete='cascade', index=True)`
    *   `farmer_id`: `fields.Many2one('dfr.farmer', string='Registered Farmer Profile (if applicable)', help="Link to dfr.farmer if this member is also a registered farmer.")`
    *   `name`: `fields.Char(string='Full Name', required=True)`
    *   `date_of_birth`: `fields.Date(string='Date of Birth')`
    *   `age`: `fields.Integer(string='Age', compute='_compute_age', store=True, help="Calculated from DOB if available.")`
    *   `sex`: `fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Sex')`
    *   `relationship_to_head_id`: `fields.Many2one('dfr.relationship.type', string='Relationship to Head')` (Assumes `dfr.relationship.type` model).
    *   `role_in_household`: `fields.Selection([...], string='Role in Household')`
    *   `education_level_id`: `fields.Many2one('dfr.education.level', string='Education Level')`
    *   `is_farmer_record_linked`: `fields.Boolean(string="Is Linked Farmer?", compute='_compute_is_farmer_record_linked', store=True)`

*   **Methods:**
    *   `_compute_age(self)`: `@api.depends('date_of_birth')`
        *   **Logic:** Calculates age based on `date_of_birth` and current date.
    *   `_compute_is_farmer_record_linked(self)`: `@api.depends('farmer_id')`
        *   **Logic:** True if `farmer_id` is set.

### 3.4. `dfr_farm.py` (Model: `dfr.farm`)

*   **Purpose:** Represents a farm unit associated with a farmer or household.
*   **Inherits:** `mail.thread`.
*   **Requirements:** REQ-FHR-001, REQ-FHR-005.

*   **Fields:**
    *   `name`: `fields.Char(string='Farm Name/Identifier', required=True)`
    *   `farmer_id`: `fields.Many2one('dfr.farmer', string='Managing Farmer')`
    *   `household_id`: `fields.Many2one('dfr.household', string='Associated Household')`
    *   `plot_ids`: `fields.One2many('dfr.plot', 'farm_id', string='Plots')`
    *   `total_area`: `fields.Float(string='Total Farm Area', compute='_compute_total_area', store=True)`
    *   `administrative_area_id`: `fields.Many2one('dfr.administrative.area', string='Farm Main Location')` (Potentially derived from plots or set manually).

*   **SQL Constraints:**
    *   `_sql_constraints = [('farmer_or_household_required', 'CHECK (farmer_id IS NOT NULL OR household_id IS NOT NULL)', 'A farm must be associated with either a farmer or a household.')]`

*   **Methods:**
    *   `_compute_total_area(self)`: `@api.depends('plot_ids.size')`
        *   **Logic:** Sums the `size` of all linked plots.

### 3.5. `dfr_plot.py` (Model: `dfr.plot`)

*   **Purpose:** Represents an individual agricultural land plot.
*   **Inherits:** `mail.thread`.
*   **Requirements:** REQ-FHR-001, REQ-FHR-005, REQ-FHR-007.

*   **Fields:**
    *   `farm_id`: `fields.Many2one('dfr.farm', string='Farm', required=True, ondelete='cascade', index=True)`
    *   `name`: `fields.Char(string='Plot Name/Identifier', required=True)`
    *   `size`: `fields.Float(string='Plot Size (e.g., hectares)', digits=(12, 4))`
    *   `size_unit_id`: `fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', <ID of Area UoM Category>)]")`
    *   `land_tenure_type_id`: `fields.Many2one('dfr.land.tenure.type', string='Land Tenure Type')` (Assumes `dfr.land.tenure.type` model).
    *   `primary_crop_livestock_ids`: `fields.Many2many('dfr.crop.livestock.type', string='Primary Crops/Livestock')` (Assumes `dfr.crop.livestock.type` model).
    *   `gps_latitude`: `fields.Float(string='GPS Latitude', digits=(10, 7))`
    *   `gps_longitude`: `fields.Float(string='GPS Longitude', digits=(10, 7))`
    *   `gps_polygon`: `fields.Text(string='GPS Polygon Coordinates (GeoJSON)')` (For storing polygon data if advanced spatial queries are not immediately needed in Odoo, PostGIS better).
    *   `administrative_area_id`: `fields.Many2one('dfr.administrative.area', string='Administrative Area', required=True)`
    *   `ownership_details`: `fields.Text(string='Land Ownership Details')`

*   **Notes:**
    *   For PostGIS integration (if REQ-FHR-005 requires advanced spatial queries), specific GeoOdoo fields (e.g., `fields.GeoPoint`, `fields.GeoPolygon` from OCA `gis` addons) would be used instead of separate float fields or GeoJSON text. This SDS assumes standard Odoo fields for now, with GeoJSON as a fallback for polygons.

### 3.6. Supporting Models (assumed, potentially in `dfr_common_core` or defined here if specific)

*   `dfr.education.level`: `name (Char)`
*   `dfr.national.id.type`: `name (Char), country_id (Many2one 'res.country')`
*   `dfr.consent.purpose`: `name (Char), description (Text)`
*   `dfr.relationship.type`: `name (Char)`
*   `dfr.land.tenure.type`: `name (Char)`
*   `dfr.crop.livestock.type`: `name (Char), type (Selection [('crop', 'Crop'), ('livestock', 'Livestock')])`
*   `dfr.administrative.area`: `name (Char), parent_id (Many2one 'dfr.administrative.area'), level (Integer)` (Likely from `dfr_common_core`)

## 4. Services (`services/`)

### 4.1. `dfr_deduplication_service.py` (Service: `dfr.deduplication.service`)

*   **Purpose:** Provides business logic for farmer de-duplication.
*   **Requirements:** REQ-FHR-012, REQ-FHR-013, REQ-FHR-014, REQ-FHR-015.
*   **Third-party Libraries:** `FuzzyWuzzy` (Python library, `fuzzywuzzy` package).

*   **Methods:**
    *   `get_deduplication_config(self)`:
        *   **Return:** `dict` (e.g., `{'realtime_enabled': True, 'realtime_fields': ['national_id_number', ('name', 'date_of_birth')], 'fuzzy_fields': {'name': 85, 'address_component': 70}, 'merge_strategy': 'newest_wins'}`)
        *   **Logic:** Retrieves de-duplication configuration parameters from `ir.config_parameter` or a dedicated DFR configuration model. This includes fields for exact matching, fields for fuzzy matching with their respective thresholds, and default merge strategy.
    *   `find_potential_duplicates(self, farmer_model, farmer_data, current_farmer_id=None)`:
        *   **Parameters:**
            *   `farmer_model`: Odoo recordset of `dfr.farmer` or its name.
            *   `farmer_data`: `dict` containing data of the farmer being checked (e.g., from an onchange event or a new record).
            *   `current_farmer_id`: `int` (optional ID of the farmer record being edited, to exclude it from results).
        *   **Return:** `list` of `dict`, each with `{'id': farmer_id, 'score': percentage_match, 'match_fields': ['field1', 'field2']}`.
        *   **Logic:**
            1.  Fetch de-duplication config using `get_deduplication_config()`.
            2.  Build Odoo domain to find exact matches based on `realtime_fields` (e.g., National ID). Exclude `current_farmer_id`.
            3.  If no exact matches or fuzzy matching is enabled:
                *   Iterate through existing farmer records (or a subset based on initial filters like administrative area).
                *   For each existing record, compare `farmer_data` with it using `FuzzyWuzzy` (e.g., `fuzz.ratio`, `fuzz.token_set_ratio`) on configured `fuzzy_fields`.
                *   If similarity score exceeds the configured threshold for any field, add it to potential duplicates list with score and matched fields.
            4.  Sort results by score (descending).
        *   **REQ:** REQ-FHR-012, REQ-FHR-013, REQ-FHR-014.
    *   `perform_record_merge(self, master_farmer_id, duplicate_farmer_ids, field_retention_rules=None)`:
        *   **Parameters:**
            *   `master_farmer_id`: `int` (ID of the farmer record to keep).
            *   `duplicate_farmer_ids`: `list` of `int` (IDs of farmer records to merge into master and then archive/deactivate).
            *   `field_retention_rules`: `dict` (optional, specifies which record's value to keep for specific conflicting fields, e.g., `{'name': 'master', 'contact_phone': 'duplicate_id_X'}`). If None, use default strategy from config (e.g., 'newest_wins' based on write_date, or 'master_wins').
        *   **Return:** `recordset` of the master `dfr.farmer` record.
        *   **Logic:**
            1.  Fetch master and duplicate farmer records.
            2.  Iterate through fields of `dfr.farmer`. If a field has different values between master and any duplicate:
                *   Apply `field_retention_rules` or default merge strategy to decide which value to keep on the master record.
                *   Update master record if necessary.
            3.  Re-parent related records from duplicates to the master:
                *   `dfr.household_member`: Update `farmer_id`.
                *   `dfr.farm`: Update `farmer_id`.
                *   (Consider other related models: dynamic form submissions, consent records, etc. - these might be handled by specific services or generic logic).
            4.  For each duplicate farmer record:
                *   Set its status to 'archived' or 'merged_duplicate'.
                *   Set its `deduplication_master_farmer_id` to `master_farmer_id`.
                *   Log the merge action extensively in the chatter of both master and duplicate records.
            5.  Return the updated master farmer record.
        *   **REQ:** REQ-FHR-015.

### 4.2. `dfr_consent_service.py` (Service: `dfr.consent.service`)

*   **Purpose:** Manages farmer consent lifecycle.
*   **Requirements:** REQ-FHR-018, REQ-SADG-008.

*   **Methods:**
    *   `record_consent(self, farmer_id, consent_status, consent_date, consent_version_agreed, consent_purpose_ids, consent_text_agreed_to_id=None)`:
        *   **Parameters:**
            *   `farmer_id`: `int`.
            *   `consent_status`: `str` (e.g., 'given').
            *   `consent_date`: `datetime`.
            *   `consent_version_agreed`: `str` (e.g., "Policy v1.2 dated YYYY-MM-DD").
            *   `consent_purpose_ids`: `list` of `int` (IDs of `dfr.consent.purpose` records).
            *   `consent_text_agreed_to_id`: `int` (optional, ID of a `dfr.consent.text.version` model if consent texts are versioned in DB).
        *   **Return:** `bool` (Success/Failure).
        *   **Logic:**
            1.  Fetch the `dfr.farmer` record.
            2.  Update farmer's consent fields: `consent_status`, `consent_date`, `consent_version_agreed`, `consent_purpose_ids`. If `consent_text_agreed_to_id` is provided, link it.
            3.  Log the consent action in the farmer's chatter (Odoo automatically tracks changes to `tracking=True` fields). Add a specific message detailing the consent granted.
    *   `withdraw_consent(self, farmer_id, withdrawal_date, withdrawal_reason)`:
        *   **Parameters:**
            *   `farmer_id`: `int`.
            *   `withdrawal_date`: `datetime`.
            *   `withdrawal_reason`: `str`.
        *   **Return:** `bool` (Success/Failure).
        *   **Logic:**
            1.  Fetch the `dfr.farmer` record.
            2.  Update farmer's consent fields: `consent_status` to 'withdrawn', `consent_withdrawal_date`, `consent_withdrawal_reason`.
            3.  Log the consent withdrawal action in the farmer's chatter. Add a specific message.
    *   `get_farmer_consent_history(self, farmer_id)`:
        *   **Return:** `list` of `dict` representing consent changes (potentially by querying `mail.message` related to consent fields or a dedicated consent log model).
        *   **Logic:** To be implemented if detailed consent event history beyond chatter is needed. For now, relies on `mail.thread` tracking on `dfr.farmer` consent fields.
    *   `is_consent_valid_for_purpose(self, farmer_id, purpose_key_or_id)`:
        *   **Return:** `bool`.
        *   **Logic:** Checks if the farmer has `consent_status` = 'given' and the specified `purpose_key_or_id` is among their `consent_purpose_ids`.

### 4.3. `dfr_kyc_service.py` (Service: `dfr.kyc.service`)

*   **Purpose:** Manages the farmer Know Your Customer (KYC) process.
*   **Requirements:** REQ-FHR-006.

*   **Methods:**
    *   `initiate_kyc_verification_request(self, farmer_id, submitted_document_ids=None)`:
        *   **Parameters:**
            *   `farmer_id`: `int`.
            *   `submitted_document_ids`: `list` of `int` (IDs of `ir.attachment` for KYC documents, optional).
        *   **Return:** `bool` (Success/Failure).
        *   **Logic:**
            1.  Fetch the `dfr.farmer` record.
            2.  Set `kyc_status` to 'pending_review'.
            3.  If `submitted_document_ids` are provided, link them to the farmer record (e.g., via message_post with attachments or a dedicated relation).
            4.  Create an activity for the KYC review user group/person.
            5.  Log initiation in farmer's chatter.
    *   `process_kyc_manual_review(self, farmer_id, reviewer_id, review_outcome, review_notes)`:
        *   **Parameters:**
            *   `farmer_id`: `int`.
            *   `reviewer_id`: `int` (ID of `res.users` who performed the review).
            *   `review_outcome`: `str` ('verified' or 'rejected').
            *   `review_notes`: `str`.
        *   **Return:** `bool` (Success/Failure).
        *   **Logic:**
            1.  Fetch the `dfr.farmer` record.
            2.  Update `kyc_status` to `review_outcome`.
            3.  Set `kyc_verification_date` to current date.
            4.  Set `kyc_reviewer_id` to `reviewer_id`.
            5.  Set `kyc_review_notes` to `review_notes`.
            6.  Log KYC review outcome in farmer's chatter.
            7.  If `review_outcome` is 'verified' and farmer status is 'pending_verification', consider calling `farmer_record.action_set_status_active()`.
    *   `check_external_kyc_api(self, farmer_id, national_id_number, national_id_type)`: (Placeholder for future integration)
        *   **Logic:** If an external National ID validation API is configured, this method would call it and update `kyc_status` based on the API response. For now, focuses on manual workflow.

## 5. Wizards (`wizards/`)

### 5.1. `dfr_deduplication_review_wizard.py` (Wizard Model: `dfr.deduplication.review.wizard`)

*   **Purpose:** Provides a UI for administrators to review and manage potential duplicate farmer records.
*   **Model Type:** `models.TransientModel`.
*   **Requirements:** REQ-FHR-015.

*   **Fields:**
    *   `farmer_ids_to_review`: `fields.Many2many('dfr.farmer', string='Farmers for Review', domain="[('status', '=', 'duplicate')]")` (Contextually populated with records flagged as duplicates).
    *   `selected_farmer_id`: `fields.Many2one('dfr.farmer', string='Selected Farmer')` (Used for single record review).
    *   `potential_duplicate_farmer_id`: `fields.Many2one('dfr.farmer', string='Potential Duplicate Of')` (Displayed during comparison).
    *   `comparison_data_html`: `fields.Html(string='Comparison Data', readonly=True)` (Dynamically generated HTML table comparing fields of two farmers).
    *   `master_record_selection`: `fields.Selection([('current', 'Keep Current as Master'), ('other', 'Keep Other as Master')], string="Select Master Record", default='current')`
    *   `field_merge_choices_json`: `fields.Text(string='Field Merge Choices (JSON)')` (Stores user choices for field conflicts).

*   **Methods (Actions):**
    *   `action_load_comparison_data(self)`:
        *   **Logic:** If two farmers are selected (e.g., `selected_farmer_id` and one from a related list or another selection), fetches their data for key fields and generates HTML for `comparison_data_html` to show side-by-side values.
    *   `action_merge_records(self)`:
        *   **Logic:**
            1.  Identifies the master record and duplicate record(s) based on user selection or context.
            2.  Gathers `field_merge_choices_json` if UI allows per-field selection.
            3.  Calls `self.env['dfr.deduplication.service'].perform_record_merge(master_id, [duplicate_id], field_retention_rules)`.
            4.  Returns an action to close the wizard or refresh the farmer list view.
    *   `action_mark_as_not_duplicate(self)`:
        *   **Logic:** For the selected farmer(s) currently marked with status 'duplicate', changes their status back to a previous state (e.g., 'pending_verification' or 'active') if deemed not actual duplicates. Clears any links to `deduplication_potential_duplicate_ids`.
    *   `default_get(self, fields_list)`:
        *   **Logic:** Populates `farmer_ids_to_review` or `selected_farmer_id` from context if wizard is launched from farmer list/form view.

### 5.2. `dfr_farmer_kyc_wizard.py` (Wizard Model: `dfr.farmer.kyc.wizard`)

*   **Purpose:** UI for manual KYC verification process.
*   **Model Type:** `models.TransientModel`.
*   **Requirements:** REQ-FHR-006.

*   **Fields:**
    *   `farmer_id`: `fields.Many2one('dfr.farmer', string='Farmer', required=True, readonly=True)`
    *   `current_kyc_status`: `fields.Selection(related='farmer_id.kyc_status', readonly=True)`
    *   `national_id_display`: `fields.Char(related='farmer_id.national_id_number', string='National ID', readonly=True)`
    *   `verification_outcome`: `fields.Selection([('verified', 'Verified'), ('rejected', 'Rejected')], string='Verification Outcome', required=True)`
    *   `review_notes`: `fields.Text(string='Review Notes')`
    *   `attachment_ids`: `fields.Many2many('ir.attachment', string='Supporting Documents')` (Can be populated from farmer or allow new uploads).

*   **Methods (Actions):**
    *   `action_submit_kyc_review(self)`:
        *   **Logic:**
            1.  Calls `self.env['dfr.kyc.service'].process_kyc_manual_review(self.farmer_id.id, self.env.user.id, self.verification_outcome, self.review_notes)`.
            2.  (Optional) Manages `attachment_ids` if new ones were added through the wizard.
            3.  Returns an action to close the wizard and refresh the farmer view.
    *   `default_get(self, fields_list)`:
        *   **Logic:** Populates `farmer_id` from context (active_id).

## 6. Data Files (`data/`)

### 6.1. `dfr_sequences.xml`

*   **Purpose:** Defines Odoo `ir.sequence` records for generating UIDs.
*   **Requirements:** REQ-FHR-002.
*   **Content Example:**
    xml
    <odoo>
        <data noupdate="1">
            <record id="seq_dfr_farmer_uid" model="ir.sequence">
                <field name="name">DFR Farmer UID</field>
                <field name="code">dfr.farmer.uid.sequence</field>
                <field name="prefix">FARM-</field>
                <field name="padding">6</field>
                <field name="company_id" eval="False"/> <!-- Shared sequence -->
            </record>
            <record id="seq_dfr_household_uid" model="ir.sequence">
                <field name="name">DFR Household UID</field>
                <field name="code">dfr.household.uid.sequence</field>
                <field name="prefix">HOU-</field>
                <field name="padding">6</field>
                <field name="company_id" eval="False"/>
            </record>
        </data>
    </odoo>
    
    *   **Note:** UUIDs might be preferred over sequences for global uniqueness and offline generation without collision. If UUIDs are used directly in Python, this file might only be for other sequential numbers if any. The requirement mentions "Odoo sequences or UUIDs". This design will prioritize Python-generated UUIDs for `uid` fields, making this sequence file less critical for UIDs but potentially useful for other human-readable references if needed. If strictly sequences, the `_compute_default_uid` methods in models will use `self.env['ir.sequence'].next_by_code(...)`. For this SDS, assume `uid` fields will be populated with UUIDs by default in the `create` methods of models, and these sequences are optional fallbacks or for other purposes.

### 6.2. `dfr_farmer_status_data.xml`

*   **Purpose:** Pre-defines farmer status records if they are managed in a separate model (e.g., `dfr.farmer.status`). If statuses are just `fields.Selection` keys, this file is not strictly needed.
*   **Requirements:** REQ-FHR-011.
*   **Content Example (if a `dfr.farmer.status` model exists):**
    xml
    <odoo>
        <data noupdate="1">
            <record id="farmer_status_pending" model="dfr.farmer.status">
                <field name="key">pending_verification</field>
                <field name="name">Pending Verification</field>
            </record>
            <record id="farmer_status_active" model="dfr.farmer.status">
                <field name="key">active</field>
                <field name="name">Active</field>
            </record>
            <!-- ... other statuses -->
        </data>
    </odoo>
    
    *   **Note:** For this SDS, farmer statuses are defined as `fields.Selection` directly in `dfr_farmer.py`, so this specific data file is not essential unless more complex status attributes are needed.

### 6.3. `dfr_national_id_type_data.xml`

*   **Purpose:** Pre-defines records for a `dfr.national.id.type` model if National ID types are configurable.
*   **Requirements:** REQ-FHR-006.
*   **Content Example (if `dfr.national.id.type` model exists):**
    xml
    <odoo>
        <data noupdate="1">
            <record id="nat_id_type_card" model="dfr.national.id.type">
                <field name="name">National ID Card</field>
                <field name="country_code_filter">SB,VU</field> <!-- Example filter -->
            </record>
            <record id="nat_id_type_passport" model="dfr.national.id.type">
                <field name="name">Passport</field>
            </record>
        </data>
    </odoo>
    
    *   **Note:** A model `dfr.national.id.type` (name: Char) would be defined in `models/` to support this.

### 6.4. `dfr_automated_actions.xml`

*   **Purpose:** Defines `ir.actions.server` or `base.automation` records for automating parts of workflows.
*   **Requirements:** REQ-FHR-011.
*   **Content Example:**
    xml
    <odoo>
        <data>
            <record id="action_notify_admin_on_kyc_rejection" model="base.automation">
                <field name="name">Notify Admin on KYC Rejection</field>
                <field name="model_id" ref="model_dfr_farmer"/>
                <field name="trigger">on_write</field>
                <field name="filter_domain">[('kyc_status', '=', 'rejected')]</field>
                <!-- Further fields for action: send email, create activity etc. -->
                <field name="state">code</field>
                <field name="code">
# Python code to execute
# E.g., record.message_post(body="KYC Rejected for Farmer: %s" % record.name)
# Or create an activity for a specific user group
                </field>
            </record>
        </data>
    </odoo>
    

## 7. Security (`security/`)

### 7.1. `ir.model.access.csv`

*   **Purpose:** Defines model-level CRUD permissions for different user groups.
*   **Requirements:** REQ-FHR-001, REQ-FHR-008.
*   **Content Structure:**
    `id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`
*   **Example Rows:**
    *   `access_dfr_farmer_user,dfr.farmer.user,model_dfr_farmer,dfr_rbac_config.group_dfr_enumerator,1,1,1,0` (Enumerator can CRUD, not delete)
    *   `access_dfr_farmer_supervisor,dfr.farmer.supervisor,model_dfr_farmer,dfr_rbac_config.group_dfr_supervisor,1,1,1,1` (Supervisor full CRUD)
    *   `access_dfr_farmer_admin,dfr.farmer.admin,model_dfr_farmer,dfr_rbac_config.group_dfr_national_admin,1,1,1,1` (Admin full CRUD)
    *   Similar entries for `dfr.household`, `dfr.household_member`, `dfr.farm`, `dfr.plot`.
    *   Public users/portal users typically have no direct backend access to these models; access for self-registration data would be through controllers/API layer if applicable here, or via portal record rules on limited fields.

## 8. Views (`views/`)

This section outlines the XML definitions for Odoo views, structuring the user interface in the Odoo Admin Portal.

### 8.1. `dfr_farmer_views.xml`

*   **Purpose:** UI for `dfr.farmer` model.
*   **Requirements:** REQ-FHR-001, REQ-FHR-006, REQ-FHR-008, REQ-FHR-011, REQ-FHR-012, REQ-FHR-015, REQ-FHR-018.
*   **Contains:**
    *   **List View (`dfr_farmer_tree`):** Displays key farmer info (UID, Name, Status, KYC Status, Administrative Area).
    *   **Form View (`dfr_farmer_form`):**
        *   Header with status bar for `status` and `kyc_status`. Buttons for status transitions (`action_set_status_active`, etc.) and KYC actions (`action_request_kyc_review`, or launch KYC wizard).
        *   Sheet with Notebook:
            *   Page "Personal Information": `name`, `date_of_birth`, `sex`, `contact_phone`, `contact_email`, `administrative_area_id`, homestead GPS fields.
            *   Page "National ID & KYC": `national_id_type_id`, `national_id_number`, `kyc_status` (readonly, controlled by actions/wizard), `kyc_verification_date`, `kyc_reviewer_id`, `kyc_review_notes`. Button to launch `dfr.farmer.kyc.wizard`.
            *   Page "Consent": `consent_status`, `consent_date`, `consent_version_agreed`, `consent_purpose_ids`, `consent_withdrawal_date`, `consent_withdrawal_reason`. Buttons for consent actions (e.g., launch consent wizard if one is made, or direct model methods).
            *   Page "Households": `household_ids` (list of HouseholdMember records where this farmer is a member).
            *   Page "Farms": `farm_ids` (list of farms associated with this farmer).
            *   Page "De-duplication": `deduplication_potential_duplicate_ids`, `deduplication_master_farmer_id`. Button `action_open_deduplication_review`.
        *   Chatter for audit trail (`mail.thread` fields).
    *   **Search View (`dfr_farmer_search`):** Filters by Name, UID, National ID, Status, KYC Status, Admin Area.
    *   **Action (`action_dfr_farmer_list`):** Window action for `dfr.farmer`.

### 8.2. `dfr_household_views.xml`

*   **Purpose:** UI for `dfr.household` model.
*   **Requirements:** REQ-FHR-001, REQ-FHR-004, REQ-FHR-011.
*   **Contains:**
    *   **List View (`dfr_household_tree`):** UID, Name (Computed from Head), Head of Household, Status, Admin Area.
    *   **Form View (`dfr_household_form`):**
        *   Header with status bar for `status`. Buttons for status transitions.
        *   Sheet: `uid`, `head_of_household_id`, `member_ids` (inline tree/form view for `dfr.household_member`), `farm_ids`, `administrative_area_id`.
        *   Chatter.
    *   **Search View (`dfr_household_search`):** Filters by UID, Head of Household, Status.
    *   **Action (`action_dfr_household_list`):** Window action.

### 8.3. `dfr_farm_views.xml`

*   **Purpose:** UI for `dfr.farm` model.
*   **Requirements:** REQ-FHR-001, REQ-FHR-005.
*   **Contains:**
    *   **List View (`dfr_farm_tree`):** Name, Managing Farmer, Associated Household, Total Area.
    *   **Form View (`dfr_farm_form`):**
        *   Sheet: `name`, `farmer_id`, `household_id`, `administrative_area_id`, `plot_ids` (inline tree/form view for `dfr.plot`).
        *   Chatter.
    *   **Search View (`dfr_farm_search`):** Filters by Name, Farmer, Household.
    *   **Action (`action_dfr_farm_list`):** Window action.

### 8.4. `dfr_plot_views.xml`

*   **Purpose:** UI for `dfr.plot` model.
*   **Requirements:** REQ-FHR-001, REQ-FHR-005, REQ-FHR-007.
*   **Contains:**
    *   **List View (`dfr_plot_tree`):** Name, Farm, Size, Primary Crop/Livestock, Admin Area.
    *   **Form View (`dfr_plot_form`):**
        *   Sheet: `name`, `farm_id`, `size`, `size_unit_id`, `land_tenure_type_id`, `primary_crop_livestock_ids`, `gps_latitude`, `gps_longitude`, `gps_polygon`, `administrative_area_id`, `ownership_details`.
        *   (Optional) Map view integration using OCA `web_map` or `web_widget_google_maps_drawing` for `gps_latitude`, `gps_longitude`, `gps_polygon` fields.
        *   Chatter.
    *   **Search View (`dfr_plot_search`):** Filters by Name, Farm, Admin Area.
    *   **Action (`action_dfr_plot_list`):** Window action.

### 8.5. `dfr_menu_views.xml`

*   **Purpose:** Defines the module's main menu and sub-menus in Odoo.
*   **Requirements:** REQ-FHR-001.
*   **Content:**
    *   Main Menu: "DFR Farmer Registry" (`menu_dfr_root`).
    *   Sub-menus under `menu_dfr_root`:
        *   "Farmers" (links to `action_dfr_farmer_list`).
        *   "Households" (links to `action_dfr_household_list`).
        *   "Farms" (links to `action_dfr_farm_list`).
        *   "Plots" (links to `action_dfr_plot_list`).
        *   Configuration sub-menu (if supporting models like National ID Type, Consent Purpose, etc., are defined within this module and need admin UI):
            *   "National ID Types"
            *   "Consent Purposes"
            *   ...etc.

### 8.6. `dfr_deduplication_review_wizard_views.xml`

*   **Purpose:** UI for `dfr.deduplication.review.wizard`.
*   **Requirements:** REQ-FHR-015.
*   **Contains:**
    *   **Form View (`dfr_deduplication_review_wizard_form`):**
        *   Fields: `farmer_ids_to_review` (if launched from list), `selected_farmer_id`, `potential_duplicate_farmer_id`, `comparison_data_html`, `master_record_selection`.
        *   A section to dynamically display conflicting fields and allow choice for merge (driven by `field_merge_choices_json`).
        *   Footer buttons: "Compare Records" (`action_load_comparison_data`), "Merge Selected" (`action_merge_records`), "Mark as Not Duplicate" (`action_mark_as_not_duplicate`), "Cancel".
    *   **Action (`action_dfr_deduplication_review_wizard`):** Window action for the wizard.

### 8.7. `dfr_farmer_kyc_wizard_views.xml`

*   **Purpose:** UI for `dfr.farmer.kyc.wizard`.
*   **Requirements:** REQ-FHR-006.
*   **Contains:**
    *   **Form View (`dfr_farmer_kyc_wizard_form`):**
        *   Fields: `farmer_id`, `current_kyc_status`, `national_id_display`, `verification_outcome`, `review_notes`, `attachment_ids`.
        *   Footer buttons: "Submit Review" (`action_submit_kyc_review`), "Cancel".
    *   **Action (`action_dfr_farmer_kyc_wizard`):** Window action for the wizard.

## 9. Static Assets (`static/description/`)

### 9.1. `icon.png`

*   **Purpose:** Module icon displayed in Odoo Apps.
*   **Requirements:** REQ-FHR-001.
*   **Format:** PNG, typically 90x90 or 128x128 pixels.

## 10. Module Initialization

### 10.1. `__init__.py` (Root)

*   **Purpose:** Initializes the Odoo module as a Python package.
*   **Content:** Imports sub-packages: `from . import models`, `from . import services`, `from . import wizards`.

### 10.2. `__manifest__.py`

*   **Purpose:** Odoo module manifest.
*   **Requirements:** REQ-FHR-001.
*   **Content:**
    python
    {
        'name': 'DFR Farmer Registry',
        'version': '18.0.1.0.0',
        'summary': 'Core module for managing farmer, household, farm, and plot data in the Digital Farmer Registry.',
        'author': 'FAO & SSS-IT',
        'website': 'https://www.fao.org', # Or project specific
        'category': 'DigitalFarmerRegistry/Core',
        'license': 'AGPL-3', # Or MIT/Apache 2.0 as per final decision
        'depends': [
            'base',
            'mail',
            'dfr_common_core', # Assuming shared utilities, base models
            # 'dfr_rbac_config', # If RBAC groups are defined in a separate module
            # 'dfr_audit_log', # If enhanced audit logging is a separate module
        ],
        'data': [
            'security/ir.model.access.csv',
            'data/dfr_sequences.xml', # If using sequences
            'data/dfr_national_id_type_data.xml', # If model defined
            # 'data/dfr_farmer_status_data.xml', # If model defined
            'data/dfr_automated_actions.xml',
            'views/dfr_farmer_views.xml',
            'views/dfr_household_views.xml',
            'views/dfr_farm_views.xml',
            'views/dfr_plot_views.xml',
            'views/dfr_menu_views.xml',
            'wizards/dfr_deduplication_review_wizard_views.xml',
            'wizards/dfr_farmer_kyc_wizard_views.xml',
            # Add views for supporting models like dfr.national.id.type if created
        ],
        'installable': True,
        'application': False, # It's a core module, not a standalone app
        'auto_install': False,
    }
    

## 11. Configuration Parameters

The following system parameters (accessible via `ir.config_parameter`) or settings in a dedicated DFR configuration model will be used:

*   **From `dfr_sequences.xml` (implicitly):**
    *   `dfr.farmer.uid.sequence.prefix` (e.g., "FARM-")
    *   `dfr.farmer.uid.sequence.padding` (e.g., 6)
    *   `dfr.household.uid.sequence.prefix` (e.g., "HOU-")
    *   `dfr.household.uid.sequence.padding` (e.g., 6)
*   **For De-duplication Service (managed by `dfr_deduplication_service.get_deduplication_config()`):**
    *   `dfr.deduplication.realtime.enabled`: (Boolean) Enable/disable real-time duplicate checks on farmer form. Default: `True`. (REQ-FHR-012)
    *   `dfr.deduplication.realtime_exact_fields`: (Comma-separated string) Fields for exact match in real-time check (e.g., `national_id_number`).
    *   `dfr.deduplication.realtime_combo_fields`: (Comma-separated string of field tuples) Field combinations for exact match (e.g., `name,date_of_birth,administrative_area_id`).
    *   `dfr.deduplication.fuzzy.name.threshold`: (Integer, 0-100) Similarity threshold for fuzzy matching on farmer names. Default: `85`. (REQ-FHR-014)
    *   `dfr.deduplication.fuzzy.address.threshold`: (Integer, 0-100) Similarity threshold for fuzzy matching on address components (if applicable). Default: `70`.
    *   `dfr.deduplication.merge_strategy`: (Selection: 'newest_wins', 'oldest_wins', 'master_wins_on_conflict') Default strategy for merging conflicting fields. Default: `'newest_wins'`. (REQ-FHR-015)
*   **For Consent Management (managed by `dfr_consent_service`):**
    *   `dfr.consent.default_version_text`: (Char) Default text or version identifier for consent if not explicitly provided. (REQ-FHR-018)
*   **Feature Toggles:**
    *   `dfr.kyc.advanced_workflow.enabled`: (Boolean) To enable a more complex KYC workflow if designed beyond the basic manual one. Default: `False`. (REQ-FHR-006)
    *   `dfr.farmer.automated_status_transitions.enabled`: (Boolean) Enable/disable automated status transitions defined in `dfr_automated_actions.xml`. Default: `True`. (REQ-FHR-011)

## 12. Dependencies

*   **`base`**: Standard Odoo base module.
*   **`mail`**: For `mail.thread` (chatter, audit) and `mail.activity.mixin`.
*   **`dfr_common_core`** (External DFR Module): Expected to provide:
    *   Base models with common fields (e.g., audit fields, custom `active` field if needed).
    *   Shared utility functions.
    *   Definitions for common selection list models like `dfr.administrative.area`, `dfr.education.level`, `dfr.relationship.type`, `dfr.land.tenure.type`, `dfr.crop.livestock.type`, `dfr.national.id.type`, `dfr.consent.purpose` (or these might be defined within `dfr_farmer_registry` if very specific to it). This SDS assumes some of these common lookups might come from `dfr_common_core`.
*   **`dfr_rbac_config`** (External DFR Module - if groups are centrally managed): Provides the Odoo security groups (`res.groups`) referenced in `ir.model.access.csv`.
*   **`dfr_audit_log`** (External DFR Module - if custom/enhanced logging beyond `mail.thread` is used): May provide services or models for more detailed audit logging.

## 13. Non-Functional Aspects Addressed

*   **Data Integrity:** Enforced through model constraints, UID generation, de-duplication logic, and status workflows.
*   **Security:** Managed via Odoo's RBAC (`ir.model.access.csv`, record rules implicitly defined by `company_id` and user group hierarchy). Sensitive actions logged.
*   **Auditability:** Achieved through `mail.thread` mixin on key models and specific logging in services for critical actions like merging or consent changes.
*   **Maintainability:** Adherence to Odoo modular design, Python PEP 8, and clear separation of concerns between models, services, and views.
*   **Configurability:** Farmer statuses, KYC process steps, de-duplication rules (thresholds, fields), and consent management parameters are designed to be configurable or extensible.
*   **Performance:** Indexing on key fields (`uid`, `national_id_number`) will be crucial. De-duplication service logic, especially fuzzy matching, needs to be optimized for performance on large datasets (e.g., by pre-filtering candidates before intensive comparison).