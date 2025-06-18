# Specification

# 1. Files

- **Path:** dfr_addons/dfr_security_config/__init__.py  
**Description:** Python package initializer for the dfr_security_config Odoo module. This file is necessary for Odoo to recognize the directory as a module.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Initializer  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Packaging
    
**Requirement Ids:**
    
    - REQ-5-001
    - REQ-5-004
    - REQ-SADG-001
    
**Purpose:** Marks the directory as an Odoo module package, enabling its discovery and loading by the Odoo framework.  
**Logic Description:** Typically empty for modules that primarily consist of data files like this one. If Python models were part of this module, they would be imported here (e.g., `from . import models`).  
**Documentation:**
    
    - **Summary:** Initializes the dfr_security_config Odoo Python module.
    
**Namespace:** odoo.addons.dfr_security_config  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_security_config/__manifest__.py  
**Description:** Odoo module manifest file for DFR RBAC Configuration. Defines module metadata, dependencies (e.g., dfr_common_core, and other DFR modules whose models are being secured), and data files for security configurations.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Declaration
    
**Requirement Ids:**
    
    - REQ-5-001
    - REQ-5-004
    - REQ-SADG-001
    
**Purpose:** Describes the dfr_security_config module to Odoo, including its name, version, category, author, dependencies, and the data files to be loaded.  
**Logic Description:** Python dictionary containing module metadata: 'name': 'DFR RBAC Configuration', 'version': '18.0.1.0.0', 'category': 'Security', 'author': 'FAO DFR Project Team', 'license': 'MIT or Apache 2.0 (as per REQ-CM-001)', 'depends': ['base', 'dfr_common_core', 'dfr_farmer_registry', 'dfr_dynamic_forms' (List all DFR modules whose models this module configures access for to ensure correct loading order)]. 'data': ['security/dfr_security_groups.xml', 'security/ir.model.access.csv', 'security/dfr_record_rules.xml'], 'installable': True, 'application': False.  
**Documentation:**
    
    - **Summary:** Manifest file for the DFR RBAC Configuration Odoo module.
    
**Namespace:** odoo.addons.dfr_security_config  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_security_config/security/__init__.py  
**Description:** Python package initializer for the 'security' sub-directory within the dfr_security_config module.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Initializer  
**Relative Path:** security/__init__.py  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Packaging
    
**Requirement Ids:**
    
    
**Purpose:** Marks the 'security' directory as a Python package. While not strictly necessary for XML/CSV data files, it's a common convention.  
**Logic Description:** Typically empty.  
**Documentation:**
    
    - **Summary:** Initializes the security sub-package for dfr_security_config module.
    
**Namespace:** odoo.addons.dfr_security_config.security  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_security_config/security/dfr_security_groups.xml  
**Description:** Odoo XML data file defining DFR-specific user security groups (roles) like Super Administrator, National Administrator, Supervisor, Enumerator, Farmer Portal User, Support Team, IT Team, and Policy Maker/Analyst. Implements REQ-5-001.  
**Template:** Odoo XML Data Template  
**Dependancy Level:** 1  
**Name:** dfr_security_groups  
**Type:** ConfigurationData  
**Relative Path:** security/dfr_security_groups.xml  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - RBAC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Role Definition
    - Security Group Hierarchy (via implied_ids if needed)
    
**Requirement Ids:**
    
    - REQ-5-001
    - REQ-SADG-001
    
**Purpose:** Establishes the distinct user roles within the DFR system, forming the foundation for permission assignments.  
**Logic Description:** Contains `<record model="res.groups">` definitions for each DFR role. Each record specifies 'name' (human-readable role name), 'category_id' (e.g., a DFR-specific category like 'module_category_dfr'), and potentially 'implied_ids' for role inheritance. Roles to define include group_dfr_super_admin, group_dfr_national_admin, group_dfr_supervisor, group_dfr_enumerator, group_dfr_farmer_portal_user, group_dfr_support_team, group_dfr_it_team, group_dfr_policy_analyst. IDs should be unique (e.g., `group_dfr_national_admin`). A DFR specific `ir.module.category` should be defined first, e.g., `module_category_dfr` with name 'DFR'.  
**Documentation:**
    
    - **Summary:** Defines Odoo security groups corresponding to DFR user roles.
    
**Namespace:** odoo.addons.dfr_security_config.security  
**Metadata:**
    
    - **Category:** SecurityConfiguration
    
- **Path:** dfr_addons/dfr_security_config/security/ir.model.access.csv  
**Description:** Defines model-level access control list (ACL) permissions (Create, Read, Update, Delete) for all DFR-specific Odoo models, assigning these permissions to the DFR security groups defined in dfr_security_groups.xml. Implements REQ-5-004 and parts of REQ-SADG-001.  
**Template:** Odoo CSV Data Template  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** ConfigurationData  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - RBAC
    - ACL
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    - CRUD Permissions Definition
    
**Requirement Ids:**
    
    - REQ-5-004
    - REQ-SADG-001
    
**Purpose:** Specifies which user roles can perform CRUD operations on various DFR data entities, enforcing the principle of least privilege.  
**Logic Description:** Standard Odoo CSV format: id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink. 
Rows define access rights for models like `dfr_farmer_registry.farmer`, `dfr_farmer_registry.household`, `dfr_farmer_registry.plot`, `dfr_dynamic_forms.form_template`, `dfr_dynamic_forms.form_submission`, etc. (using actual model names from dependent DFR modules). 
Permissions are granted to groups like `dfr_security_config.group_dfr_national_admin`, `dfr_security_config.group_dfr_enumerator`. 
Example: `access_dfr_farmer_enumerator,dfr.farmer.enumerator.access,model_dfr_farmer_registry_farmer,dfr_security_config.group_dfr_enumerator,1,1,1,0` (gives RWC, no D to enumerators for farmer model). Define comprehensive ACLs for all DFR models and roles.  
**Documentation:**
    
    - **Summary:** Provides CSV data for Odoo's ir.model.access model, defining ACLs for DFR entities.
    
**Namespace:** odoo.addons.dfr_security_config.security  
**Metadata:**
    
    - **Category:** SecurityConfiguration
    
- **Path:** dfr_addons/dfr_security_config/security/dfr_record_rules.xml  
**Description:** Odoo XML data file defining record-level security rules (ir.rule) for DFR models. These rules implement fine-grained data access controls, such as scoping data visibility by geographic area or other criteria for roles like Enumerator or Supervisor, contributing to hierarchical access control as per REQ-SADG-001.  
**Template:** Odoo XML Data Template  
**Dependancy Level:** 1  
**Name:** dfr_record_rules  
**Type:** ConfigurationData  
**Relative Path:** security/dfr_record_rules.xml  
**Repository Id:** DFR_MOD_RBAC_CONFIG  
**Pattern Ids:**
    
    - RBAC
    - RecordLevelSecurity
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Scoping Rules
    - Row-Level Security Enforcement
    - Hierarchical Access Control Implementation
    
**Requirement Ids:**
    
    - REQ-SADG-001
    
**Purpose:** Restricts access to specific records within DFR models based on defined Odoo domain expressions, ensuring users only see data relevant to their operational scope.  
**Logic Description:** Contains `<record model="ir.rule">` definitions. Each rule specifies 'name', 'model_id' (referencing the target DFR model, e.g., `model_dfr_farmer_registry_farmer`), 'domain_force' (an Odoo domain string defining the restriction, e.g., `"[('administrative_area_id', 'child_of', user.company_id.administrative_area_id.id)]"` if users are associated with a company linked to an admin area, or `"[('create_uid', '=', user.id)]"` for 'user can only see their own records'), and 'groups' (a Many2many field linking to `res.groups` records, e.g., `[(4, ref('dfr_security_config.group_dfr_enumerator'))]`). Define rules for National Admin (sees all in their country instance, potentially `[('company_id', '=', user.company_id.id)]`), Supervisor (sees data within their supervised areas/teams), and Enumerator (sees data for their assigned area/farmers). `perm_read`, `perm_write`, `perm_create`, `perm_unlink` booleans (1/0) control rule applicability for operations.  
**Documentation:**
    
    - **Summary:** Defines Odoo record rules for fine-grained, row-level access control on DFR data models.
    
**Namespace:** odoo.addons.dfr_security_config.security  
**Metadata:**
    
    - **Category:** SecurityConfiguration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

