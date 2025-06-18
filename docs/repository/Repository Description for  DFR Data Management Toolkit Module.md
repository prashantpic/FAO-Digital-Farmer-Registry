# Repository Specification

# 1. Name
DFR Data Management Toolkit Module


---

# 2. Description
Provides tools within the Odoo Admin Portal for bulk import of legacy farmer data (CSV/XLSX), bulk data validation, field mapping, and exportable reports/extracts. Supports data migration activities.


---

# 3. Type
ETL


---

# 4. Namespace
odoo.addons.dfr_data_tools


---

# 5. Output Path
dfr_addons/dfr_data_tools


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML


---

# 8. Technology
Odoo ORM, Odoo Import/Export Framework


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS
- DFR_MOD_CORE_COMMON


---

# 11. Layer Ids

- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-DM-001  
- **Requirement Id:** REQ-DM-002  
- **Requirement Id:** REQ-DM-007  
- **Requirement Id:** REQ-TSE-001  


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
DFR_MOD_DATA_MGMT_TOOLKIT


---

# 17. Architecture_Map

- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-data-management-tools-010


---

# 19. Requirements_Map

- REQ-DM-001
- REQ-DM-002
- REQ-DM-007
- REQ-TSE-001


---

# 20. Endpoints

## 20.1. Bulk Data Import Admin Wizard
Odoo Admin Portal wizard for uploading CSV/XLSX files, mapping fields, performing bulk validation, and importing legacy farmer data.

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web (specific Odoo wizard action)

### 20.1.7. Request Schema
Uploaded file (CSV/XLSX), field mapping configuration.

### 20.1.8. Response Schema
Import status, error logs, confirmation.

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Odoo Views (XML/OWL)
- CSV
- XLSX

### 20.1.12. Communication Protocol
HTTP/Odoo RPC

### 20.1.13. Layer Ids

- dfr_odoo_presentation
- dfr_odoo_application_services

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-DM-001  
- **Requirement Id:** REQ-DM-002  
- **Requirement Id:** REQ-DM-003  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_odoo_presentation
- dfr_odoo_application_services

### 20.1.19. Components_Map

- dfr-module-data-management-tools-010

### 20.1.20. Requirements_Map

- REQ-DM-001
- REQ-DM-002
- REQ-DM-003

## 20.2. Data Export Admin Action
Odoo Admin Portal functionality for exporting reports and raw data extracts in standard formats (CSV, XLSX).

### 20.2.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
/web/export/... (Odoo standard export controller)

### 20.2.7. Request Schema
Selected data model, fields, filters, format.

### 20.2.8. Response Schema
File download (CSV, XLSX).

### 20.2.9. Authentication Required
True

### 20.2.10. Authorization Required
True

### 20.2.11. Data Formats

- CSV
- XLSX

### 20.2.12. Communication Protocol
HTTP

### 20.2.13. Layer Ids

- dfr_odoo_presentation

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-DM-004  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-data-management-tools-010

### 20.2.20. Requirements_Map

- REQ-DM-004



---

