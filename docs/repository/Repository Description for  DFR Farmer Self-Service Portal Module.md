# Repository Specification

# 1. Name
DFR Farmer Self-Service Portal Module


---

# 2. Description
Extends Odoo Website module to provide a public-facing, mobile-responsive portal for farmer pre-registration, informational content, and access to selected dynamic forms. Ensures WCAG 2.1 AA compliance.


---

# 3. Type
WebFrontend


---

# 4. Namespace
odoo.addons.dfr_farmer_portal


---

# 5. Output Path
dfr_addons/dfr_farmer_portal


---

# 6. Framework
Odoo 18.0 Community (Website Module)


---

# 7. Language
Python, XML, QWeb, JavaScript, CSS, HTML


---

# 8. Technology
Odoo Website, Bootstrap


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS
- DFR_MOD_LOCALIZATION


---

# 11. Layer Ids

- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-FSSP-001  
- **Requirement Id:** REQ-FSSP-003  
- **Requirement Id:** REQ-FSSP-004  
- **Requirement Id:** REQ-FSSP-009  
- **Requirement Id:** REQ-FSSP-013  


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
DFR_MOD_FARMER_PORTAL


---

# 17. Architecture_Map

- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-farmer-portal-011


---

# 19. Requirements_Map

- REQ-FSSP-001
- REQ-FSSP-003
- REQ-FSSP-004
- REQ-FSSP-009
- REQ-FSSP-013


---

# 20. Endpoints

## 20.1. Farmer Pre-registration Form Page
Public web page with a form for farmers to submit pre-registration data.

### 20.1.4. Type
ODOO_WEBSITE_CONTROLLER

### 20.1.5. Method
GET, POST

### 20.1.6. Url Pattern
/farmer/register

### 20.1.7. Request Schema
GET: None. POST: Farmer pre-registration form fields (name, village, contact, National ID etc.)

### 20.1.8. Response Schema
GET: HTML page with form. POST: Confirmation page or error messages.

### 20.1.9. Authentication Required
False

### 20.1.10. Authorization Required
False

### 20.1.11. Data Formats

- HTML
- application/x-www-form-urlencoded

### 20.1.12. Communication Protocol
HTTPS

### 20.1.13. Layer Ids

- dfr_odoo_presentation

### 20.1.14. Dependencies

- DFR_MOD_FARMER_REGISTRY

### 20.1.15. Requirements

- **Requirement Id:** REQ-FSSP-003  
- **Requirement Id:** REQ-FSSP-004  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
True

### 20.1.18. Architecture_Map

- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-farmer-portal-011

### 20.1.20. Requirements_Map

- REQ-FSSP-003
- REQ-FSSP-004

## 20.2. DFR Information Page
Public web page displaying information about the Digital Farmer Registry.

### 20.2.4. Type
ODOO_WEBSITE_CONTROLLER

### 20.2.5. Method
GET

### 20.2.6. Url Pattern
/dfr/info

### 20.2.7. Request Schema
None

### 20.2.8. Response Schema
HTML page with informational content.

### 20.2.9. Authentication Required
False

### 20.2.10. Authorization Required
False

### 20.2.11. Data Formats

- HTML

### 20.2.12. Communication Protocol
HTTPS

### 20.2.13. Layer Ids

- dfr_odoo_presentation

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-FSSP-002  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
True

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-farmer-portal-011

### 20.2.20. Requirements_Map

- REQ-FSSP-002

## 20.3. Public Dynamic Form Page
Public web page for rendering and submitting specific dynamic forms made available to farmers.

### 20.3.4. Type
ODOO_WEBSITE_CONTROLLER

### 20.3.5. Method
GET, POST

### 20.3.6. Url Pattern
/portal/forms/{form_id}

### 20.3.7. Request Schema
GET: Path parameter {form_id}. POST: Submitted dynamic form data.

### 20.3.8. Response Schema
GET: HTML page rendering the dynamic form. POST: Confirmation or error message.

### 20.3.9. Authentication Required
False

### 20.3.10. Authorization Required
False

### 20.3.11. Data Formats

- HTML
- application/x-www-form-urlencoded

### 20.3.12. Communication Protocol
HTTPS

### 20.3.13. Layer Ids

- dfr_odoo_presentation

### 20.3.14. Dependencies

- DFR_MOD_DYNAMIC_FORMS

### 20.3.15. Requirements

- **Requirement Id:** REQ-FSSP-009  
- **Requirement Id:** REQ-3-009  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
True

### 20.3.18. Architecture_Map

- dfr_odoo_presentation

### 20.3.19. Components_Map

- dfr-module-farmer-portal-011

### 20.3.20. Requirements_Map

- REQ-FSSP-009
- REQ-3-009



---

