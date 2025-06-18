# Specification

# 1. Files

- **Path:** dfr_addons/dfr_farmer_registry/__init__.py  
**Description:** Initializes the Python package for the DFR Farmer Registry Odoo module, importing submodules like models, services, and wizards.  
**Template:** Python Odoo Module Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Module Initialization  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Import Structure
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Makes Python modules (models, services, wizards) accessible to Odoo.  
**Logic Description:** Contains import statements for sub-directories like 'models', 'services', 'wizards'.  
**Documentation:**
    
    - **Summary:** Standard Odoo module __init__.py file to ensure Python submodules are loaded.
    
**Namespace:** odoo.addons.dfr_farmer_registry  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_registry/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata such as name, version, author, dependencies, and data files to load (XML, CSV).  
**Template:** Python Odoo Module Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Loading
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Provides essential metadata for the Odoo module system to recognize and load the dfr_farmer_registry module.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'depends' (e.g., ['base', 'mail', 'dfr_common_core']), 'data' (listing XML and CSV files), 'installable', 'application'.  
**Documentation:**
    
    - **Summary:** Declares the DFR Farmer Registry module to Odoo, its dependencies, and associated data files.
    
**Namespace:** odoo.addons.dfr_farmer_registry  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_registry/models/__init__.py  
**Description:** Initializes the 'models' Python package, importing all defined Odoo model files within this directory.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Model Initialization  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Ensures all Odoo models defined in the 'models' directory are loaded by the module.  
**Logic Description:** Contains import statements for each model file, e.g., 'from . import dfr_farmer', 'from . import dfr_household'.  
**Documentation:**
    
    - **Summary:** Imports all domain model files for the DFR Farmer Registry module.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_registry/models/dfr_farmer.py  
**Description:** Defines the Odoo model for 'Farmer' entities. Includes fields for farmer profile, UID, National ID, KYC status, consent details, and farmer status. Implements logic for UID generation, real-time de-duplication checks (onchange/constraints), status workflows, and consent management methods.  
**Template:** Python Odoo Model  
**Dependancy Level:** 1  
**Name:** dfr_farmer  
**Type:** Model  
**Relative Path:** models/dfr_farmer.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** uid  
**Type:** fields.Char  
**Attributes:** readonly|required|copy=False|index=True  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required  
    - **Name:** national_id_type_id  
**Type:** fields.Many2one  
**Attributes:**   
    - **Name:** national_id_number  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** kyc_status  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** kyc_verification_date  
**Type:** fields.Date  
**Attributes:**   
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** required|default='pending_verification'  
    - **Name:** consent_status  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** consent_date  
**Type:** fields.Datetime  
**Attributes:**   
    - **Name:** consent_version_agreed  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** consent_purpose_ids  
**Type:** fields.Many2many  
**Attributes:**   
    
**Methods:**
    
    - **Name:** _compute_uid_value  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** api.depends  
    - **Name:** create  
**Parameters:**
    
    - vals_list
    
**Return Type:** res.partner  
**Attributes:** api.model_create_multi  
    - **Name:** action_request_kyc_verification  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** action_mark_kyc_verified  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** action_mark_kyc_rejected  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** action_set_status_active  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** action_set_status_inactive  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** onchange_check_potential_duplicates  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** api.onchange  
    - **Name:** _sql_constraints_check_national_id_unique  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** record_consent_action  
**Parameters:**
    
    - consent_details
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** withdraw_consent_action  
**Parameters:**
    
    - withdrawal_reason
    
**Return Type:** bool  
**Attributes:**   
    
**Implemented Features:**
    
    - Farmer Profile Management
    - UID Generation
    - National ID Capture
    - KYC Status Tracking
    - Consent Management
    - Farmer Status Workflow
    - Real-time De-duplication Hints
    
**Requirement Ids:**
    
    - REQ-FHR-001
    - REQ-FHR-002
    - REQ-FHR-006
    - REQ-FHR-011
    - REQ-FHR-012
    - REQ-FHR-018
    
**Purpose:** Represents and manages individual farmer data within the DFR system.  
**Logic Description:** Inherits from 'mail.thread' for chatter and audit. Defines fields as per common data model. UID generated using Odoo sequence or UUID on creation. KYC status has its own lifecycle. Farmer status workflow uses selection field and model methods, potentially triggered by automated actions. Onchange methods trigger calls to DeDuplicationService for real-time duplicate hints. Consent fields store current consent state; methods allow recording/updating consent via ConsentService.  
**Documentation:**
    
    - **Summary:** Odoo model for dfr.farmer. Stores core farmer information, manages identity, status, consent, and interfaces with de-duplication and KYC processes.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models.dfr_farmer  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_farmer_registry/models/dfr_household.py  
**Description:** Defines the Odoo model for 'Household' entities. Includes fields for household UID and status, and relationships to farmers and household members.  
**Template:** Python Odoo Model  
**Dependancy Level:** 1  
**Name:** dfr_household  
**Type:** Model  
**Relative Path:** models/dfr_household.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** uid  
**Type:** fields.Char  
**Attributes:** readonly|required|copy=False|index=True  
    - **Name:** head_of_household_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farmer'  
    - **Name:** member_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='dfr.household_member', inverse_name='household_id'  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** required|default='active'  
    
**Methods:**
    
    - **Name:** _compute_uid_value  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** api.depends  
    - **Name:** create  
**Parameters:**
    
    - vals_list
    
**Return Type:** res.partner  
**Attributes:** api.model_create_multi  
    - **Name:** action_set_status_active  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** action_set_status_inactive  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Household Profile Management
    - UID Generation
    - Household Status Workflow
    
**Requirement Ids:**
    
    - REQ-FHR-001
    - REQ-FHR-002
    - REQ-FHR-011
    
**Purpose:** Represents and manages household data, linking farmers and household members.  
**Logic Description:** Inherits from 'mail.thread'. Defines fields for household UID and status. UID generated on creation. Manages relationship to household members and head of household (farmer). Status workflow similar to farmer status.  
**Documentation:**
    
    - **Summary:** Odoo model for dfr.household. Stores household information and manages its members and status.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models.dfr_household  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_farmer_registry/models/dfr_household_member.py  
**Description:** Defines the Odoo model for 'HouseholdMember' entities, linking individuals to a household.  
**Template:** Python Odoo Model  
**Dependancy Level:** 1  
**Name:** dfr_household_member  
**Type:** Model  
**Relative Path:** models/dfr_household_member.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** household_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.household', required=True, ondelete='cascade'  
    - **Name:** farmer_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farmer'  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required  
    - **Name:** relationship_to_head  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** age  
**Type:** fields.Integer  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - Household Member Management
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Represents individual members of a household.  
**Logic Description:** Links to `dfr.household` and potentially to `dfr.farmer` if the member is also a registered farmer. Captures member-specific details like relationship to head.  
**Documentation:**
    
    - **Summary:** Odoo model for dfr.household_member. Stores information about individuals belonging to a household.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models.dfr_household_member  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_farmer_registry/models/dfr_farm.py  
**Description:** Defines the Odoo model for 'Farm' entities, associated with a farmer or household.  
**Template:** Python Odoo Model  
**Dependancy Level:** 1  
**Name:** dfr_farm  
**Type:** Model  
**Relative Path:** models/dfr_farm.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required  
    - **Name:** farmer_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farmer'  
    - **Name:** household_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.household'  
    - **Name:** plot_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='dfr.plot', inverse_name='farm_id'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Farm Management
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Represents a farm unit, which can contain multiple plots.  
**Logic Description:** Links to `dfr.farmer` or `dfr.household`. Contains one-to-many relationship to `dfr.plot`.  
**Documentation:**
    
    - **Summary:** Odoo model for dfr.farm. Stores information about a farm entity.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models.dfr_farm  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_farmer_registry/models/dfr_plot.py  
**Description:** Defines the Odoo model for 'Plot' entities, representing individual land plots.  
**Template:** Python Odoo Model  
**Dependancy Level:** 1  
**Name:** dfr_plot  
**Type:** Model  
**Relative Path:** models/dfr_plot.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** farm_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farm', required=True, ondelete='cascade'  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required  
    - **Name:** size  
**Type:** fields.Float  
**Attributes:**   
    - **Name:** gps_latitude  
**Type:** fields.Float  
**Attributes:** digits=(10, 7)  
    - **Name:** gps_longitude  
**Type:** fields.Float  
**Attributes:** digits=(10, 7)  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Plot Management
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Represents an individual agricultural plot with details like size and location.  
**Logic Description:** Links to `dfr.farm`. Stores plot-specific information including GPS coordinates.  
**Documentation:**
    
    - **Summary:** Odoo model for dfr.plot. Stores information about individual farm plots.
    
**Namespace:** odoo.addons.dfr_farmer_registry.models.dfr_plot  
**Metadata:**
    
    - **Category:** dfr_odoo_domain_models
    
- **Path:** dfr_addons/dfr_farmer_registry/services/__init__.py  
**Description:** Initializes the 'services' Python package, importing all defined service files.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Service Initialization  
**Relative Path:** services/__init__.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    
**Requirement Ids:**
    
    - REQ-FHR-012
    - REQ-FHR-015
    - REQ-FHR-018
    
**Purpose:** Ensures all service classes defined in the 'services' directory are accessible.  
**Logic Description:** Contains import statements for each service file, e.g., 'from . import dfr_deduplication_service'.  
**Documentation:**
    
    - **Summary:** Imports all domain service files for the DFR Farmer Registry module.
    
**Namespace:** odoo.addons.dfr_farmer_registry.services  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_registry/services/dfr_deduplication_service.py  
**Description:** Implements the de-duplication logic. Provides methods to find potential duplicates based on configured rules (including fuzzy matching using FuzzyWuzzy) and to process the merging of duplicate farmer records. Called by farmer model onchange/constraints and deduplication review wizard.  
**Template:** Python Odoo Service  
**Dependancy Level:** 2  
**Name:** dfr_deduplication_service  
**Type:** Service  
**Relative Path:** services/dfr_deduplication_service.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** find_potential_duplicates  
**Parameters:**
    
    - farmer_data
    - config_rules
    
**Return Type:** list  
**Attributes:**   
    - **Name:** perform_record_merge  
**Parameters:**
    
    - master_farmer_id
    - duplicate_farmer_ids
    - merge_rules
    
**Return Type:** dfr.farmer  
**Attributes:**   
    - **Name:** get_deduplication_config  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - De-duplication Logic
    - Fuzzy Matching
    - Duplicate Record Merging
    
**Requirement Ids:**
    
    - REQ-FHR-012
    - REQ-FHR-015
    
**Purpose:** Encapsulates business logic for identifying and managing duplicate farmer records.  
**Logic Description:** Uses FuzzyWuzzy for name/address similarity. `find_potential_duplicates` checks against existing records based on National ID or combination of fields, returns a list of matches with scores. `perform_record_merge` takes a master record and duplicates, applies retention rules, archives duplicates, and updates linkages. `get_deduplication_config` fetches rules from system parameters or a dedicated config model.  
**Documentation:**
    
    - **Summary:** Service responsible for farmer de-duplication operations, including finding potential matches and merging confirmed duplicates.
    
**Namespace:** odoo.addons.dfr_farmer_registry.services.dfr_deduplication_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_farmer_registry/services/dfr_consent_service.py  
**Description:** Manages farmer consent. Provides methods for recording, updating, versioning, and withdrawing consent for data collection and use. Called by the farmer model.  
**Template:** Python Odoo Service  
**Dependancy Level:** 2  
**Name:** dfr_consent_service  
**Type:** Service  
**Relative Path:** services/dfr_consent_service.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** record_consent  
**Parameters:**
    
    - farmer_id
    - consent_status
    - consent_date
    - consent_version
    - consent_purposes
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** update_consent_status  
**Parameters:**
    
    - farmer_id
    - new_status
    - reason
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** withdraw_consent  
**Parameters:**
    
    - farmer_id
    - withdrawal_date
    - reason
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** get_farmer_consent_details  
**Parameters:**
    
    - farmer_id
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - Consent Recording
    - Consent Update
    - Consent Withdrawal
    - Consent Versioning
    
**Requirement Ids:**
    
    - REQ-FHR-018
    
**Purpose:** Encapsulates business logic for managing farmer consent according to data privacy regulations.  
**Logic Description:** `record_consent` updates the farmer's consent fields. `update_consent_status` handles changes, potentially logging them. `withdraw_consent` marks consent as withdrawn and logs the action. All actions ensure comprehensive audit trails are created on the farmer record (via `mail.thread` tracking on consent fields).  
**Documentation:**
    
    - **Summary:** Service responsible for all farmer consent management operations.
    
**Namespace:** odoo.addons.dfr_farmer_registry.services.dfr_consent_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_farmer_registry/services/dfr_kyc_service.py  
**Description:** Handles the Know Your Customer (KYC) verification process. Provides methods for managing the manual verification workflow within Odoo.  
**Template:** Python Odoo Service  
**Dependancy Level:** 2  
**Name:** dfr_kyc_service  
**Type:** Service  
**Relative Path:** services/dfr_kyc_service.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiate_kyc_verification  
**Parameters:**
    
    - farmer_id
    - submitted_documents
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** process_kyc_review  
**Parameters:**
    
    - farmer_id
    - reviewer_id
    - review_status
    - review_comments
    
**Return Type:** bool  
**Attributes:**   
    - **Name:** get_farmer_kyc_status  
**Parameters:**
    
    - farmer_id
    
**Return Type:** str  
**Attributes:**   
    
**Implemented Features:**
    
    - KYC Process Management
    - KYC Status Update
    
**Requirement Ids:**
    
    - REQ-FHR-006
    
**Purpose:** Encapsulates business logic for the farmer KYC verification workflow.  
**Logic Description:** `initiate_kyc_verification` updates the farmer's KYC status to 'pending' and stores any document references. `process_kyc_review` updates the status to 'verified' or 'rejected' based on reviewer input and logs the action. This service primarily orchestrates updates on the `dfr.farmer` model's KYC-related fields.  
**Documentation:**
    
    - **Summary:** Service responsible for managing the manual Know Your Customer (KYC) verification process for farmers.
    
**Namespace:** odoo.addons.dfr_farmer_registry.services.dfr_kyc_service  
**Metadata:**
    
    - **Category:** dfr_odoo_application_services
    
- **Path:** dfr_addons/dfr_farmer_registry/wizards/__init__.py  
**Description:** Initializes the 'wizards' Python package, importing all wizard model files.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Wizard Initialization  
**Relative Path:** wizards/__init__.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Discovery
    
**Requirement Ids:**
    
    - REQ-FHR-015
    - REQ-FHR-006
    
**Purpose:** Ensures all Odoo wizard models defined in the 'wizards' directory are loaded.  
**Logic Description:** Contains import statements for each wizard model file, e.g., 'from . import dfr_deduplication_review_wizard'.  
**Documentation:**
    
    - **Summary:** Imports all wizard (transient model) files for the DFR Farmer Registry module.
    
**Namespace:** odoo.addons.dfr_farmer_registry.wizards  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_registry/wizards/dfr_deduplication_review_wizard.py  
**Description:** Defines the Odoo transient model (wizard) for reviewing, comparing, and merging potential duplicate farmer records identified by the De-duplication Service.  
**Template:** Python Odoo Wizard  
**Dependancy Level:** 2  
**Name:** dfr_deduplication_review_wizard  
**Type:** Wizard  
**Relative Path:** wizards/dfr_deduplication_review_wizard.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** master_farmer_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farmer', string='Master Record'  
    - **Name:** duplicate_farmer_ids  
**Type:** fields.Many2many  
**Attributes:** comodel_name='dfr.farmer', string='Potential Duplicates'  
    - **Name:** merge_field_selection_json  
**Type:** fields.Text  
**Attributes:** string='Field Merge Choices'  
    
**Methods:**
    
    - **Name:** action_compare_records  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    - **Name:** action_merge_records  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    - **Name:** action_mark_as_not_duplicate  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - Duplicate Review Interface
    - Record Comparison UI Logic
    - Merge Execution Trigger
    
**Requirement Ids:**
    
    - REQ-FHR-015
    
**Purpose:** Provides a user interface for administrators to manage potential duplicate farmer records.  
**Logic Description:** Wizard displays potential duplicate pairs. Allows admin to select a master record and choose which fields to retain from which record during a merge. `action_merge_records` calls the `DeDuplicationService` to perform the actual merge. `action_mark_as_not_duplicate` updates statuses accordingly.  
**Documentation:**
    
    - **Summary:** Odoo wizard for the administrative workflow of reviewing and merging potential duplicate farmer records.
    
**Namespace:** odoo.addons.dfr_farmer_registry.wizards.dfr_deduplication_review_wizard  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/wizards/dfr_farmer_kyc_wizard.py  
**Description:** Defines an Odoo transient model (wizard) to guide administrators through the manual KYC verification workflow for a farmer.  
**Template:** Python Odoo Wizard  
**Dependancy Level:** 2  
**Name:** dfr_farmer_kyc_wizard  
**Type:** Wizard  
**Relative Path:** wizards/dfr_farmer_kyc_wizard.py  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    - **Name:** farmer_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='dfr.farmer', required=True, readonly=True  
    - **Name:** verification_notes  
**Type:** fields.Text  
**Attributes:**   
    - **Name:** supporting_document_attachment_ids  
**Type:** fields.Many2many  
**Attributes:** comodel_name='ir.attachment'  
    - **Name:** outcome  
**Type:** fields.Selection  
**Attributes:** [('verified', 'Verified'), ('rejected', 'Rejected')]  
**Is Required:** True  
    
**Methods:**
    
    - **Name:** action_process_kyc_review  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - Manual KYC Workflow UI
    
**Requirement Ids:**
    
    - REQ-FHR-006
    
**Purpose:** Provides a step-by-step UI for administrators to review and update a farmer's KYC status.  
**Logic Description:** The wizard is launched from a farmer record. It displays farmer details, allows document review (if attachments are part of KYC), and enables the admin to set the KYC outcome (verified/rejected) with notes. `action_process_kyc_review` calls the `KYCService` or directly updates the farmer model's KYC status fields.  
**Documentation:**
    
    - **Summary:** Odoo wizard to facilitate the manual Know Your Customer (KYC) verification workflow.
    
**Namespace:** odoo.addons.dfr_farmer_registry.wizards.dfr_farmer_kyc_wizard  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/data/dfr_sequences.xml  
**Description:** Defines Odoo sequences for generating unique Farmer UIDs and Household UIDs, if Odoo's ir.sequence is used for this purpose.  
**Template:** XML Odoo Data  
**Dependancy Level:** 1  
**Name:** dfr_sequences  
**Type:** Data  
**Relative Path:** data/dfr_sequences.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - UID Sequence Definition
    
**Requirement Ids:**
    
    - REQ-FHR-002
    
**Purpose:** Configures unique ID generation sequences within Odoo for farmer and household records.  
**Logic Description:** Contains `<record>` tags defining `ir.sequence` entries for `dfr.farmer.uid.sequence` and `dfr.household.uid.sequence`, specifying prefix, padding, and step.  
**Documentation:**
    
    - **Summary:** XML data file for Odoo sequences used in UID generation.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_farmer_registry/data/dfr_farmer_status_data.xml  
**Description:** Defines initial or default farmer status values if these are stored as master data (e.g., in a separate model) or used as keys for selection fields.  
**Template:** XML Odoo Data  
**Dependancy Level:** 1  
**Name:** dfr_farmer_status_data  
**Type:** Data  
**Relative Path:** data/dfr_farmer_status_data.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Farmer Statuses
    
**Requirement Ids:**
    
    - REQ-FHR-011
    
**Purpose:** Provides predefined farmer status options for the system.  
**Logic Description:** This file might not be strictly necessary if statuses are simple selection field keys defined directly in the model. If statuses were more complex (e.g., requiring descriptions, color codes), this would populate a `dfr.farmer.status` model.  
**Documentation:**
    
    - **Summary:** XML data file for initial farmer status configurations.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_farmer_registry/data/dfr_national_id_type_data.xml  
**Description:** Defines initial or default National ID types if these are stored as master data and selectable.  
**Template:** XML Odoo Data  
**Dependancy Level:** 1  
**Name:** dfr_national_id_type_data  
**Type:** Data  
**Relative Path:** data/dfr_national_id_type_data.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default National ID Types
    
**Requirement Ids:**
    
    - REQ-FHR-006
    
**Purpose:** Provides predefined National ID type options for farmer profiles.  
**Logic Description:** Populates a `dfr.national.id.type` model (if created for configurability) with common ID types (e.g., 'Passport', 'Driver License', 'National Card'). If National ID type is a simple selection field, this file isn't needed.  
**Documentation:**
    
    - **Summary:** XML data file for initial National ID type configurations.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_farmer_registry/data/dfr_automated_actions.xml  
**Description:** Defines Odoo server actions or automated actions to implement parts of the farmer/household status workflows, such as notifications on status change or automatic transitions based on conditions.  
**Template:** XML Odoo Data  
**Dependancy Level:** 3  
**Name:** dfr_automated_actions  
**Type:** Data  
**Relative Path:** data/dfr_automated_actions.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Workflow Automation for Statuses
    
**Requirement Ids:**
    
    - REQ-FHR-011
    
**Purpose:** Configures automated behaviors within the farmer and household status lifecycle.  
**Logic Description:** Contains `<record>` tags defining `ir.actions.server` or `base.automation` entries. For example, an action to send an email when a farmer's status changes to 'Active', or to automatically archive a farmer record if inactive for a certain period (though complex period checks might need cron jobs).  
**Documentation:**
    
    - **Summary:** XML data file defining automated server actions for DFR workflows.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_farmer_registry/security/ir.model.access.csv  
**Description:** Defines access control list (ACL) for Odoo models within the DFR Farmer Registry module. Specifies CRUD permissions for various user groups.  
**Template:** CSV Odoo Security  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** Security  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Manages permissions for creating, reading, updating, and deleting records of DFR models.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Defines access rights for models like `dfr.farmer`, `dfr.household` for different user groups (e.g., DFR Enumerator, DFR Supervisor, DFR National Admin).  
**Documentation:**
    
    - **Summary:** Defines model-level access permissions for the DFR Farmer Registry module.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_farmer_registry/views/dfr_farmer_views.xml  
**Description:** Defines Odoo views (form, list, search, kanban) for the 'Farmer' model. Includes layout for farmer profile, National ID, KYC, consent, and status fields.  
**Template:** XML Odoo View  
**Dependancy Level:** 3  
**Name:** dfr_farmer_views  
**Type:** View  
**Relative Path:** views/dfr_farmer_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Farmer UI (List, Form, Search)
    - KYC UI Elements
    - Consent UI Elements
    - Status Display & Actions
    
**Requirement Ids:**
    
    - REQ-FHR-001
    - REQ-FHR-006
    - REQ-FHR-011
    - REQ-FHR-012
    - REQ-FHR-015
    - REQ-FHR-018
    
**Purpose:** Provides the user interface for managing farmer records in the Odoo backend.  
**Logic Description:** Contains XML definitions for list, form, and search views for `dfr.farmer`. Form view includes sections for personal details, National ID, KYC information (with buttons to trigger KYC wizard/actions), consent details (with buttons for consent actions), and farmer status (with buttons for manual status transitions). `attrs` used for conditional visibility based on status or KYC state. Includes action to launch de-duplication review wizard for selected records.  
**Documentation:**
    
    - **Summary:** XML views for the dfr.farmer model, defining its presentation in the Odoo Admin Portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/views/dfr_household_views.xml  
**Description:** Defines Odoo views (form, list, search) for the 'Household' model.  
**Template:** XML Odoo View  
**Dependancy Level:** 3  
**Name:** dfr_household_views  
**Type:** View  
**Relative Path:** views/dfr_household_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Household UI (List, Form, Search)
    
**Requirement Ids:**
    
    - REQ-FHR-001
    - REQ-FHR-011
    
**Purpose:** Provides the user interface for managing household records.  
**Logic Description:** XML definitions for list, form, and search views for `dfr.household`. Form view includes fields for UID, head of household, and a list of household members. Includes display of household status and actions for status changes.  
**Documentation:**
    
    - **Summary:** XML views for the dfr.household model.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/views/dfr_farm_views.xml  
**Description:** Defines Odoo views (form, list, search) for the 'Farm' model.  
**Template:** XML Odoo View  
**Dependancy Level:** 3  
**Name:** dfr_farm_views  
**Type:** View  
**Relative Path:** views/dfr_farm_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Farm UI (List, Form, Search)
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Provides the user interface for managing farm records.  
**Logic Description:** XML definitions for list, form, and search views for `dfr.farm`. Form view includes fields for farm name, associated farmer/household, and a list of plots.  
**Documentation:**
    
    - **Summary:** XML views for the dfr.farm model.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/views/dfr_plot_views.xml  
**Description:** Defines Odoo views (form, list, search) for the 'Plot' model.  
**Template:** XML Odoo View  
**Dependancy Level:** 3  
**Name:** dfr_plot_views  
**Type:** View  
**Relative Path:** views/dfr_plot_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Plot UI (List, Form, Search)
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Provides the user interface for managing plot records.  
**Logic Description:** XML definitions for list, form, and search views for `dfr.plot`. Form view includes fields for plot name, size, GPS coordinates, and associated farm.  
**Documentation:**
    
    - **Summary:** XML views for the dfr.plot model.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/views/dfr_menu_views.xml  
**Description:** Defines Odoo menu items for accessing Farmer, Household, Farm, and Plot views within the DFR Farmer Registry module.  
**Template:** XML Odoo Menu  
**Dependancy Level:** 3  
**Name:** dfr_menu_views  
**Type:** View  
**Relative Path:** views/dfr_menu_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Navigation Menus
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Creates navigation entries in the Odoo UI for DFR Farmer Registry functionalities.  
**Logic Description:** Contains XML definitions for `ir.ui.menu` records, creating a main DFR menu and sub-menus for Farmers, Households, Farms, and Plots, linking to their respective list actions.  
**Documentation:**
    
    - **Summary:** Defines the menu structure for accessing DFR Farmer Registry features in Odoo.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/wizards/dfr_deduplication_review_wizard_views.xml  
**Description:** Defines Odoo views (form) for the De-duplication Review Wizard.  
**Template:** XML Odoo Wizard View  
**Dependancy Level:** 3  
**Name:** dfr_deduplication_review_wizard_views  
**Type:** View  
**Relative Path:** wizards/dfr_deduplication_review_wizard_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - De-duplication Review Wizard UI
    
**Requirement Ids:**
    
    - REQ-FHR-015
    
**Purpose:** Provides the user interface for the de-duplication review and merge process.  
**Logic Description:** XML definition for the form view of `dfr.deduplication.review.wizard`. Displays fields for master record, potential duplicates, and options/fields to select data from during merge. Buttons for 'Compare', 'Merge', 'Mark as Not Duplicate'.  
**Documentation:**
    
    - **Summary:** XML views for the De-duplication Review Wizard.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/wizards/dfr_farmer_kyc_wizard_views.xml  
**Description:** Defines Odoo views (form) for the Farmer KYC Verification Wizard.  
**Template:** XML Odoo Wizard View  
**Dependancy Level:** 3  
**Name:** dfr_farmer_kyc_wizard_views  
**Type:** View  
**Relative Path:** wizards/dfr_farmer_kyc_wizard_views.xml  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    - OdooModuleSystem
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Verification Wizard UI
    
**Requirement Ids:**
    
    - REQ-FHR-006
    
**Purpose:** Provides the user interface for the manual KYC verification workflow.  
**Logic Description:** XML definition for the form view of `dfr.farmer.kyc.wizard`. Displays farmer details, fields for verification notes, document attachments, and outcome selection. Button to process the review.  
**Documentation:**
    
    - **Summary:** XML views for the Farmer KYC Verification Wizard.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** dfr_odoo_presentation
    
- **Path:** dfr_addons/dfr_farmer_registry/static/description/icon.png  
**Description:** Icon for the DFR Farmer Registry Odoo module, displayed in the Odoo Apps list.  
**Template:** Image  
**Dependancy Level:** 0  
**Name:** icon  
**Type:** Static Asset  
**Relative Path:** static/description/icon.png  
**Repository Id:** DFR_MOD_FARMER_REGISTRY  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Icon
    
**Requirement Ids:**
    
    - REQ-FHR-001
    
**Purpose:** Provides a visual identifier for the module in the Odoo backend.  
**Logic Description:** A PNG image file, typically 90x90 pixels or as per Odoo guidelines.  
**Documentation:**
    
    - **Summary:** Module icon for DFR Farmer Registry.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Static
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedKYCWorkflow
  - EnableFuzzyNameMatchingThresholdConfig
  - EnableAutomatedStatusTransitions
  
- **Database Configs:**
  
  - dfr.farmer.uid.sequence.prefix
  - dfr.farmer.uid.sequence.padding
  - dfr.household.uid.sequence.prefix
  - dfr.deduplication.realtime.enabled
  - dfr.deduplication.fuzzy.name.threshold
  - dfr.consent.default_version_text
  


---

