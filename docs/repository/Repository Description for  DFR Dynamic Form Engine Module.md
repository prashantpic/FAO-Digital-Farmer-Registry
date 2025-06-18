# Repository Specification

# 1. Name
DFR Dynamic Form Engine Module


---

# 2. Description
Enables administrators to design, manage, and version custom data collection forms. Handles form submissions from various clients (mobile, portal, admin) and links them to farmer profiles. Supports various field types, validation, and conditional logic.


---

# 3. Type
ApplicationService


---

# 4. Namespace
odoo.addons.dfr_dynamic_forms


---

# 5. Output Path
dfr_addons/dfr_dynamic_forms


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML, JavaScript, OWL


---

# 8. Technology
Odoo ORM, Odoo Web Client UI Components


---

# 9. Thirdparty Libraries

- OCA Survey (evaluate components)
- OCA FormIO (evaluate components)


---

# 10. Dependencies

- DFR_MOD_CORE_COMMON
- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_RBAC_CONFIG


---

# 11. Layer Ids

- dfr_odoo_domain_models
- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-3-001  
- **Requirement Id:** REQ-3-002  
- **Requirement Id:** REQ-3-003  
- **Requirement Id:** REQ-3-004  
- **Requirement Id:** REQ-3-008  
- **Requirement Id:** REQ-3-012  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
ModularMonolith


---

# 16. Id
DFR_MOD_DYNAMIC_FORMS


---

# 17. Architecture_Map

- dfr_odoo_domain_models
- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-dynamic-forms-003


---

# 19. Requirements_Map

- REQ-3-001
- REQ-3-002
- REQ-3-003
- REQ-3-004
- REQ-3-008
- REQ-3-012


---

# 20. Endpoints

## 20.1. Dynamic Form Builder Admin View/Action
Odoo Admin Portal UI for designing dynamic forms, defining fields, validation rules, and conditional logic.

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web#model=dfr.form&view_type=form (example)

### 20.1.7. Request Schema
User interaction with form builder UI

### 20.1.8. Response Schema
Saved form definition, rendered form builder UI

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Odoo Views (XML/OWL)
- JSON (for form schema)

### 20.1.12. Communication Protocol
HTTP/Odoo RPC

### 20.1.13. Layer Ids

- dfr_odoo_presentation

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-3-001  
- **Requirement Id:** REQ-3-012  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-dynamic-forms-003

### 20.1.20. Requirements_Map

- REQ-3-001
- REQ-3-012

## 20.2. Dynamic Form Submissions Admin View/Action
Odoo Admin Portal UI for viewing, managing, and exporting dynamic form submissions.

### 20.2.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
/web#model=dfr.form.submission&view_type=list (example)

### 20.2.7. Request Schema
User interaction with Odoo list/form views

### 20.2.8. Response Schema
Rendered list of submissions, submission details

### 20.2.9. Authentication Required
True

### 20.2.10. Authorization Required
True

### 20.2.11. Data Formats

- Odoo Views (XML/OWL)

### 20.2.12. Communication Protocol
HTTP/Odoo RPC

### 20.2.13. Layer Ids

- dfr_odoo_presentation

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-3-010  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-dynamic-forms-003

### 20.2.20. Requirements_Map

- REQ-3-010

## 20.3. Form Definition Service Interface
Internal Python service for managing dynamic form definitions (create, version, publish, retrieve for rendering).

### 20.3.4. Type
ODOO_MODULE_SERVICE_INTERFACE

### 20.3.5. Method
None

### 20.3.6. Url Pattern
None

### 20.3.7. Request Schema
Form definition data, form ID

### 20.3.8. Response Schema
Form definition object (JSON/Python dict), status

### 20.3.9. Authentication Required
False

### 20.3.10. Authorization Required
False

### 20.3.11. Data Formats

- Python Objects
- JSON

### 20.3.12. Communication Protocol
Python Method Call

### 20.3.13. Layer Ids

- dfr_odoo_application_services

### 20.3.14. Dependencies


### 20.3.15. Requirements

- **Requirement Id:** REQ-3-001  
- **Requirement Id:** REQ-3-003  
- **Requirement Id:** REQ-3-006  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- dfr_odoo_application_services

### 20.3.19. Components_Map

- dfr-module-dynamic-forms-003

### 20.3.20. Requirements_Map

- REQ-3-001
- REQ-3-003
- REQ-3-006

## 20.4. Form Submission Service Interface
Internal Python service for processing and storing dynamic form submissions received from various channels.

### 20.4.4. Type
ODOO_MODULE_SERVICE_INTERFACE

### 20.4.5. Method
None

### 20.4.6. Url Pattern
None

### 20.4.7. Request Schema
Submitted form data (responses, farmer UID, form ID)

### 20.4.8. Response Schema
Submission confirmation, submission ID

### 20.4.9. Authentication Required
False

### 20.4.10. Authorization Required
False

### 20.4.11. Data Formats

- Python Objects
- JSON

### 20.4.12. Communication Protocol
Python Method Call

### 20.4.13. Layer Ids

- dfr_odoo_application_services

### 20.4.14. Dependencies


### 20.4.15. Requirements

- **Requirement Id:** REQ-3-007  
- **Requirement Id:** REQ-3-008  

### 20.4.16. Version
1.0

### 20.4.17. Is Public
False

### 20.4.18. Architecture_Map

- dfr_odoo_application_services

### 20.4.19. Components_Map

- dfr-module-dynamic-forms-003

### 20.4.20. Requirements_Map

- REQ-3-007
- REQ-3-008



---

