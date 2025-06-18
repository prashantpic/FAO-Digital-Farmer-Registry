# Repository Specification

# 1. Name
DFR RBAC Configuration Module


---

# 2. Description
Defines DFR-specific user roles (Odoo groups), access control lists (ACLs - ir.model.access.csv), and record rules (ir.rule) for all DFR modules. This module primarily contains configuration data rather than executable code with traditional endpoints.


---

# 3. Type
RBACService


---

# 4. Namespace
odoo.addons.dfr_security_config


---

# 5. Output Path
dfr_addons/dfr_security_config


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
XML, CSV


---

# 8. Technology
Odoo Security Framework


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_CORE_COMMON


---

# 11. Layer Ids

- dfr_security


---

# 12. Requirements

- **Requirement Id:** REQ-5-001  
- **Requirement Id:** REQ-5-004  
- **Requirement Id:** REQ-SADG-001  


---

# 13. Generate Tests
False


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
ModularMonolith


---

# 16. Id
DFR_MOD_RBAC_CONFIG


---

# 17. Architecture_Map

- dfr_security


---

# 18. Components_Map

- dfr-module-rbac-config-004


---

# 19. Requirements_Map

- REQ-5-001
- REQ-5-004
- REQ-SADG-001


---

# 20. Endpoints

## 20.1. Access Control Rules Definition
Defines Odoo access rights (read, write, create, delete) for DFR models per user group (role). These are declarative configurations.

### 20.1.4. Type
ODOO_SECURITY_DEFINITION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
None

### 20.1.7. Request Schema
ir.model.access.csv file format

### 20.1.8. Response Schema
Applied security permissions within Odoo

### 20.1.9. Authentication Required
False

### 20.1.10. Authorization Required
False

### 20.1.11. Data Formats

- CSV

### 20.1.12. Communication Protocol
Odoo Module Loading

### 20.1.13. Layer Ids

- dfr_security

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-5-002  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_security

### 20.1.19. Components_Map

- dfr-module-rbac-config-004

### 20.1.20. Requirements_Map

- REQ-5-002

## 20.2. Record Rules Definition
Defines Odoo record rules for fine-grained, row-level data access control based on Odoo domain expressions.

### 20.2.4. Type
ODOO_SECURITY_DEFINITION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
None

### 20.2.7. Request Schema
ir.rule model data (XML definitions)

### 20.2.8. Response Schema
Applied data filtering within Odoo

### 20.2.9. Authentication Required
False

### 20.2.10. Authorization Required
False

### 20.2.11. Data Formats

- XML

### 20.2.12. Communication Protocol
Odoo Module Loading

### 20.2.13. Layer Ids

- dfr_security

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-5-003  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_security

### 20.2.19. Components_Map

- dfr-module-rbac-config-004

### 20.2.20. Requirements_Map

- REQ-5-003

## 20.3. User Groups (Roles) Definition
Defines Odoo user groups corresponding to DFR roles (e.g., National Administrator, Enumerator, Supervisor).

### 20.3.4. Type
ODOO_SECURITY_DEFINITION

### 20.3.5. Method
None

### 20.3.6. Url Pattern
None

### 20.3.7. Request Schema
res.groups model data (XML definitions)

### 20.3.8. Response Schema
Defined user roles within Odoo

### 20.3.9. Authentication Required
False

### 20.3.10. Authorization Required
False

### 20.3.11. Data Formats

- XML

### 20.3.12. Communication Protocol
Odoo Module Loading

### 20.3.13. Layer Ids

- dfr_security

### 20.3.14. Dependencies


### 20.3.15. Requirements

- **Requirement Id:** REQ-5-001  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- dfr_security

### 20.3.19. Components_Map

- dfr-module-rbac-config-004

### 20.3.20. Requirements_Map

- REQ-5-001



---

