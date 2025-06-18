# Repository Specification

# 1. Name
DFR Localization Module


---

# 2. Description
Manages DFR-specific localization assets, including .po translation files for all custom DFR modules. Leverages Odoo's built-in internationalization (i18n) capabilities to support multiple languages, date/time formats, and RTL scripts if required. Configuration for active languages is managed via Odoo Admin.


---

# 3. Type
Internationalization


---

# 4. Namespace
odoo.addons.dfr_localization


---

# 5. Output Path
dfr_addons/dfr_localization


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
XML, .po files


---

# 8. Technology
Odoo i18n framework, Gettext (.po files)


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_CORE_COMMON
- All other DFR Odoo modules


---

# 11. Layer Ids

- dfr_cross_cutting
- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-PCA-018  
- **Requirement Id:** REQ-LMS-001  
- **Requirement Id:** REQ-LMS-002  
- **Requirement Id:** REQ-LMS-004  


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
DFR_MOD_LOCALIZATION


---

# 17. Architecture_Map

- dfr_cross_cutting
- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-localization-pack-012


---

# 19. Requirements_Map

- REQ-PCA-018
- REQ-LMS-001
- REQ-LMS-002
- REQ-LMS-004


---

# 20. Endpoints

## 20.1. Translation Files Management
Mechanism for managing language translation files (.po format) for all UI elements, dynamic form content, and notification templates within DFR modules. Handled by Odoo's standard translation import/export tools.

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web#action=base.action_translation_import (example)

### 20.1.7. Request Schema
Uploaded .po files or selection of language to export.

### 20.1.8. Response Schema
Confirmation of import/export, updated translations in the system.

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- .po files

### 20.1.12. Communication Protocol
HTTP/Odoo RPC (for UI), Odoo Module Loading (for initial .po files)

### 20.1.13. Layer Ids

- dfr_cross_cutting
- dfr_odoo_presentation

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-LMS-002  
- **Requirement Id:** REQ-SYSADM-006  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_cross_cutting
- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-localization-pack-012

### 20.1.20. Requirements_Map

- REQ-LMS-002
- REQ-SYSADM-006

## 20.2. Active Language Configuration
Odoo Admin Portal settings for managing installed and active languages for a country instance. This uses Odoo's standard language management features.

### 20.2.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
/web#action=base.action_lang_tree (example)

### 20.2.7. Request Schema
User selection of languages to activate/deactivate.

### 20.2.8. Response Schema
Updated language configuration for the instance.

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

- **Requirement Id:** REQ-LMS-005  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-localization-pack-012

### 20.2.20. Requirements_Map

- REQ-LMS-005



---

