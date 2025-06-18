# Specification

# 1. Files

- **Path:** dfr_common/__init__.py  
**Description:** Initializes the Python package for the dfr_common Odoo module, making submodules like models and utils importable.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - REQ-PCA-002
    
**Purpose:** To declare the directory as a Python package and specify modules to be imported.  
**Logic Description:** This file will contain import statements for the 'models' and 'utils' subdirectories. For example: from . import models; from . import utils.  
**Documentation:**
    
    - **Summary:** Standard Odoo module __init__.py file. Imports sub-packages models and utils.
    
**Namespace:** odoo.addons.dfr_common  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_common/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata such as name, version, author, dependencies, license, and data files to load.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Versioning
    - Licensing Information
    
**Requirement Ids:**
    
    - REQ-PCA-002
    - REQ-PCA-008
    - REQ-CM-001
    
**Purpose:** To provide Odoo with essential information about the dfr_common module for its registration and loading.  
**Logic Description:** This file will be a Python dictionary containing keys like 'name', 'version', 'summary', 'description', 'author', 'website', 'license' (e.g., 'MIT' or 'Apache-2.0'), 'category', 'depends' (e.g., ['base']), 'data', 'installable', 'application', 'auto_install'. The version will follow Semantic Versioning 2.0.0.  
**Documentation:**
    
    - **Summary:** Defines the dfr_common module for Odoo, including its version, license, dependencies, and data files. Key for module installation and management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_common/LICENSE  
**Description:** Contains the full text of the open-source license (MIT or Apache 2.0) under which the DFR Common Core Module is distributed.  
**Template:** License Text File  
**Dependancy Level:** 0  
**Name:** LICENSE  
**Type:** License  
**Relative Path:** LICENSE  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Open Source Licensing
    
**Requirement Ids:**
    
    - REQ-PCA-008
    - REQ-CM-001
    
**Purpose:** To legally define the terms under which the software can be used, modified, and distributed.  
**Logic Description:** This file will contain the verbatim text of either the MIT License or the Apache License 2.0, as decided for the project. No other content.  
**Documentation:**
    
    - **Summary:** Specifies the open-source license governing the use of the dfr_common module. Will contain either MIT or Apache 2.0 license text.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Legal
    
- **Path:** dfr_common/models/__init__.py  
**Description:** Initializes the Python package for the models directory, importing all Odoo model files within it.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Aggregation
    
**Requirement Ids:**
    
    - REQ-PCA-002
    
**Purpose:** To make individual model files (dfr_abstract_model.py, dfr_audit_mixin.py, etc.) accessible when the 'models' package is imported.  
**Logic Description:** This file will contain import statements for each Python file in the 'models' directory. For example: from . import dfr_abstract_model; from . import dfr_audit_mixin; from . import dfr_uid_mixin; from . import dfr_config_settings.  
**Documentation:**
    
    - **Summary:** Imports all Odoo model definitions within the dfr_common.models package.
    
**Namespace:** odoo.addons.dfr_common.models  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_common/models/dfr_abstract_model.py  
**Description:** Defines a base abstract Odoo model for DFR entities. Intended to be inherited by specific DFR entity models in other modules. May include common fields or methods, and inherit from DFRUidMixin and DfrAuditMixin.  
**Template:** Odoo Model Template  
**Dependancy Level:** 3  
**Name:** dfr_abstract_model  
**Type:** Odoo Abstract Model  
**Relative Path:** models/dfr_abstract_model.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - MixinPattern
    - AbstractSuperclass
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** get_dfr_context_info  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Base DFR Model Structure
    - Shared Model Logic
    
**Requirement Ids:**
    
    - REQ-PCA-002
    - REQ-PCA-016
    
**Purpose:** To provide a common, reusable base for all DFR-specific Odoo models, ensuring consistency and reducing code duplication.  
**Logic Description:** This Python file will define an Odoo abstract model (e.g., class DfrAbstractModel(models.AbstractModel)). It will inherit from 'dfr.uid.mixin' and 'dfr.audit.mixin'. It can define common helper methods or fields that should be present in most DFR models. For example, a method to get common DFR context or default values.  
**Documentation:**
    
    - **Summary:** Provides an abstract base model (DfrAbstractModel) for other DFR Odoo models. It incorporates UID and audit functionalities through mixins and can define shared fields or methods.
    
**Namespace:** odoo.addons.dfr_common.models.dfr_abstract_model  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_common/models/dfr_audit_mixin.py  
**Description:** Defines an Odoo model mixin to enhance audit trail capabilities for DFR entities, potentially extending Odoo's 'mail.thread'.  
**Template:** Odoo Model Template  
**Dependancy Level:** 2  
**Name:** dfr_audit_mixin  
**Type:** Odoo Model Mixin  
**Relative Path:** models/dfr_audit_mixin.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - MixinPattern
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** log_dfr_specific_event  
**Parameters:**
    
    - self
    - event_description
    - event_data=None
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Enhanced Audit Logging
    
**Requirement Ids:**
    
    - REQ-PCA-016
    - REQ-FHR-010
    
**Purpose:** To provide a reusable component for adding standardized and enhanced audit logging to DFR models beyond default Odoo capabilities if needed.  
**Logic Description:** This Python file will define an Odoo abstract model mixin (e.g., class DfrAuditMixin(models.AbstractModel)). It will inherit from 'mail.thread' and 'mail.activity.mixin' for chatter and activity integration. It may add custom methods to log specific DFR-related auditable events if Odoo's standard tracking is insufficient for certain requirements.  
**Documentation:**
    
    - **Summary:** A mixin class (DfrAuditMixin) to be inherited by DFR models requiring comprehensive audit trails. Leverages Odoo's mail.thread and can add custom logging methods for specific DFR events.
    
**Namespace:** odoo.addons.dfr_common.models.dfr_audit_mixin  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_common/models/dfr_uid_mixin.py  
**Description:** Defines an Odoo model mixin for generating and managing unique identifiers (UIDs) for DFR entities, using Odoo sequences or UUIDs.  
**Template:** Odoo Model Template  
**Dependancy Level:** 2  
**Name:** dfr_uid_mixin  
**Type:** Odoo Model Mixin  
**Relative Path:** models/dfr_uid_mixin.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - MixinPattern
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected  
    - **Name:** dfr_uid  
**Type:** fields.Char  
**Attributes:** public|readonly|copy=False  
    
**Methods:**
    
    - **Name:** _compute_dfr_uid  
**Parameters:**
    
    - self
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** create  
**Parameters:**
    
    - self
    - vals_list
    
**Return Type:** models.Model  
**Attributes:** public|@api.model_create_multi  
    
**Implemented Features:**
    
    - Unique ID Generation
    
**Requirement Ids:**
    
    - REQ-PCA-016
    - REQ-FHR-002
    
**Purpose:** To provide a reusable and consistent mechanism for generating unique identifiers for key DFR entities.  
**Logic Description:** This Python file will define an Odoo abstract model mixin (e.g., class DfrUidMixin(models.AbstractModel)). It will include a character field for the DFR UID. The 'create' method will be overridden to generate a unique ID (e.g., using Odoo's ir.sequence or Python's uuid module) upon record creation if not already provided. The UID should be indexed and unique per model that inherits it.  
**Documentation:**
    
    - **Summary:** A mixin class (DfrUidMixin) for DFR models to automatically generate a unique DFR UID upon creation. Uses Odoo sequences or UUIDs. Contains a 'dfr_uid' field.
    
**Namespace:** odoo.addons.dfr_common.models.dfr_uid_mixin  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_common/models/dfr_config_settings.py  
**Description:** Extends Odoo's base configuration wizard (res.config.settings) to include DFR-common system settings. Allows administrators to manage these settings via the Odoo UI.  
**Template:** Odoo Model Template  
**Dependancy Level:** 3  
**Name:** dfr_config_settings  
**Type:** Odoo Transient Model  
**Relative Path:** models/dfr_config_settings.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _inherit  
**Type:** str  
**Attributes:** protected  
    - **Name:** dfr_common_setting_example  
**Type:** fields.Char  
**Attributes:** public|config_parameter='dfr_common.setting_example'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - DFR Common Configuration Management
    
**Requirement Ids:**
    
    - REQ-PCA-003
    - REQ-PCA-016
    - REQ-CM-013
    
**Purpose:** To provide a centralized UI for National Administrators to configure DFR common settings, separating configuration from code.  
**Logic Description:** This Python file will define a class that inherits from 'res.config.settings' (TransientModel). It will add fields that represent DFR-common configurable parameters (e.g., a default setting example, a toggle for a common feature). These fields will typically use the 'config_parameter' attribute to store their values in 'ir.config_parameter'.  
**Documentation:**
    
    - **Summary:** Extends Odoo's res.config.settings model to add configuration options specific to the DFR common core. Stores settings in ir.config_parameter.
    
**Namespace:** odoo.addons.dfr_common.models.dfr_config_settings  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_common/utils/__init__.py  
**Description:** Initializes the Python package for the utils directory, making utility modules importable.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** utils/__init__.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Utility Aggregation
    
**Requirement Ids:**
    
    - REQ-PCA-016
    
**Purpose:** To make utility functions and constants defined in dfr_utils.py and constants.py accessible when the 'utils' package is imported.  
**Logic Description:** This file will contain import statements for each Python file in the 'utils' directory. For example: from . import constants; from . import dfr_utils.  
**Documentation:**
    
    - **Summary:** Imports utility modules like constants and dfr_utils within the dfr_common.utils package.
    
**Namespace:** odoo.addons.dfr_common.utils  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** dfr_common/utils/constants.py  
**Description:** Defines shared constants used across the DFR platform. This ensures consistency and avoids magic strings/numbers.  
**Template:** Python Module Template  
**Dependancy Level:** 0  
**Name:** constants  
**Type:** Python Module  
**Relative Path:** utils/constants.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DPI_PRINCIPLE_OPENNESS  
**Type:** str  
**Attributes:** public|final  
    - **Name:** DPI_PRINCIPLE_REUSABILITY  
**Type:** str  
**Attributes:** public|final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Constants Definition
    
**Requirement Ids:**
    
    - REQ-PCA-011
    - REQ-PCA-016
    
**Purpose:** To provide a single source of truth for constants related to DFR common functionalities and principles.  
**Logic Description:** This Python file will contain various constant definitions relevant to the DFR common core. Examples: DEFAULT_COUNTRY_CODE, MAX_RECORDS_PER_PAGE, status codes if shared, DPI principle identifiers. For instance: DPI_PRINCIPLE_OPENNESS = 'openness'.  
**Documentation:**
    
    - **Summary:** Contains DFR-specific shared constants. For example, constants related to DPI principles or default configuration values.
    
**Namespace:** odoo.addons.dfr_common.utils.constants  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** dfr_common/utils/dfr_utils.py  
**Description:** Provides common utility functions and helper methods for use by various DFR Odoo modules.  
**Template:** Python Module Template  
**Dependancy Level:** 1  
**Name:** dfr_utils  
**Type:** Python Module  
**Relative Path:** utils/dfr_utils.py  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** format_dfr_date  
**Parameters:**
    
    - date_obj
    
**Return Type:** str  
**Attributes:** public|static  
    - **Name:** get_dfr_config_param  
**Parameters:**
    
    - env
    - param_name
    - default_value=None
    
**Return Type:** any  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Common Helper Functions
    - Configuration Access Utilities
    
**Requirement Ids:**
    
    - REQ-PCA-016
    - REQ-CM-013
    
**Purpose:** To offer a collection of reusable utility functions that simplify common tasks and promote code reuse across DFR modules.  
**Logic Description:** This Python file will define various static methods or functions. Examples: A function to consistently format dates for DFR display, a helper to retrieve configuration parameters safely (e.g., from ir.config_parameter), validation helpers, or small data transformation utilities if needed by multiple modules. It will implement the DFR_MOD_CORE_COMMON_UTIL_SVC interface.  
**Documentation:**
    
    - **Summary:** A collection of shared utility functions for the DFR platform. Includes helpers for date formatting, configuration parameter retrieval, etc.
    
**Namespace:** odoo.addons.dfr_common.utils.dfr_utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** dfr_common/security/ir.model.access.csv  
**Description:** Defines model access rights (CRUD permissions) for any Odoo models introduced by the dfr_common module, such as configuration models.  
**Template:** Odoo CSV Data Template  
**Dependancy Level:** 4  
**Name:** ir.model.access  
**Type:** Odoo Security Data  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - RoleBasedAccessControl
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-PCA-016
    
**Purpose:** To control which user groups have create, read, write, and delete permissions on the models defined in this common module.  
**Logic Description:** This CSV file will follow Odoo's standard format for ir.model.access.csv. It will list access rules: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. For example, it might grant 'base.group_system' (System Administrators) full access to 'dfr.config.settings' model if such a model were not transient and needed direct CRUD.  
**Documentation:**
    
    - **Summary:** Specifies access control lists (ACLs) for models defined within the dfr_common module. Ensures appropriate permissions for managing common configurations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_common/data/dfr_config_parameters.xml  
**Description:** Odoo XML data file to define default values for DFR-common system parameters stored in 'ir.config_parameter'.  
**Template:** Odoo XML Data Template  
**Dependancy Level:** 1  
**Name:** dfr_config_parameters_data  
**Type:** Odoo Data  
**Relative Path:** data/dfr_config_parameters.xml  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default System Parameters
    
**Requirement Ids:**
    
    - REQ-CM-013
    - REQ-PCA-003
    
**Purpose:** To set up initial, sensible default configurations for the DFR common core module, which can be overridden per deployment if necessary.  
**Logic Description:** This XML file will use Odoo's data loading mechanism. It will contain <record> tags for model 'ir.config_parameter' to set default values for parameters. Example: <record id='dfr_default_setting_example_param' model='ir.config_parameter'><field name='key'>dfr_common.setting_example</field><field name='value'>DefaultValue</field></record>.  
**Documentation:**
    
    - **Summary:** Provides default values for DFR-common system configuration parameters (ir.config_parameter). These can be overridden in specific deployments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_common/views/dfr_config_settings_views.xml  
**Description:** Odoo XML views for the DFR-common configuration settings interface, allowing administrators to manage settings defined in dfr_config_settings.py.  
**Template:** Odoo XML View Template  
**Dependancy Level:** 4  
**Name:** dfr_config_settings_views  
**Type:** Odoo View  
**Relative Path:** views/dfr_config_settings_views.xml  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - ModelViewController
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configuration UI
    
**Requirement Ids:**
    
    - REQ-CM-013
    - REQ-PCA-016
    
**Purpose:** To create the user interface within Odoo's settings area for managing DFR common configurations.  
**Logic Description:** This XML file will define Odoo views (form views, potentially actions and menus) for the 'dfr.config.settings' model. It will use Odoo's view architecture to lay out fields for administrators to interact with. Example: A form view inheriting from 'res.config.settings.view.form' to add a new settings block for DFR common parameters.  
**Documentation:**
    
    - **Summary:** Defines the Odoo views (forms, actions, menus) for managing DFR common configuration settings through the administrator interface.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_common/i18n/dfr_common.pot  
**Description:** Translation template file (.pot) for all translatable strings within the dfr_common module. Used as a base for creating language-specific .po files.  
**Template:** Odoo POT File Template  
**Dependancy Level:** 0  
**Name:** dfr_common  
**Type:** Odoo Translation Template  
**Relative Path:** i18n/dfr_common.pot  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    - Internationalization
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Support Base
    
**Requirement Ids:**
    
    - REQ-PCA-016
    
**Purpose:** To enable multilingual support for any user-facing text defined in the dfr_common module, such as configuration setting labels or descriptions.  
**Logic Description:** This file will be generated by Odoo's translation export mechanism or can be created manually. It lists all strings marked for translation in Python code (e.g., _('My String')) and XML files (e.g., attributes like 'string'). Contains msgid and empty msgstr entries.  
**Documentation:**
    
    - **Summary:** Contains all translatable strings for the dfr_common module. This POT file is used to generate .po files for specific language translations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Localization
    
- **Path:** dfr_common/static/description/icon.png  
**Description:** Standard icon for the dfr_common Odoo module, displayed in the Odoo Apps list.  
**Template:** Odoo Module Icon  
**Dependancy Level:** 0  
**Name:** icon  
**Type:** Image  
**Relative Path:** static/description/icon.png  
**Repository Id:** DFR_MOD_CORE_COMMON  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Identification
    
**Requirement Ids:**
    
    - REQ-PCA-002
    
**Purpose:** To provide a visual identifier for the module within the Odoo interface.  
**Logic Description:** This is a PNG image file, typically 96x96 pixels, representing the module.  
**Documentation:**
    
    - **Summary:** The icon for the dfr_common module, displayed in the Odoo interface.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Asset
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

