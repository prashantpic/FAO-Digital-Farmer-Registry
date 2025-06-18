# Repository Specification

# 1. Name
DFR Farmer Registry Module


---

# 2. Description
Manages core farmer, household, farm, and plot data. Implements CRUD operations, UID generation, status workflows, KYC processes, consent management, and de-duplication logic. Data is exposed via the API Gateway and Odoo Admin Portal.


---

# 3. Type
DomainService


---

# 4. Namespace
odoo.addons.dfr_farmer_registry


---

# 5. Output Path
dfr_addons/dfr_farmer_registry


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML


---

# 8. Technology
Odoo ORM, PostgreSQL


---

# 9. Thirdparty Libraries

- FuzzyWuzzy (for de-duplication)


---

# 10. Dependencies

- DFR_MOD_CORE_COMMON
- DFR_MOD_RBAC_CONFIG
- DFR_MOD_AUDIT_LOG


---

# 11. Layer Ids

- dfr_odoo_domain_models
- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-FHR-001  
- **Requirement Id:** REQ-FHR-002  
- **Requirement Id:** REQ-FHR-006  
- **Requirement Id:** REQ-FHR-011  
- **Requirement Id:** REQ-FHR-012  
- **Requirement Id:** REQ-FHR-015  
- **Requirement Id:** REQ-FHR-018  


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
DFR_MOD_FARMER_REGISTRY


---

# 17. Architecture_Map

- dfr_odoo_domain_models
- dfr_odoo_application_services
- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-farmer-registry-002


---

# 19. Requirements_Map

- REQ-FHR-001
- REQ-FHR-002
- REQ-FHR-006
- REQ-FHR-011
- REQ-FHR-012
- REQ-FHR-015
- REQ-FHR-018


---

# 20. Endpoints

## 20.1. Farmer Admin View/Action
Odoo Admin Portal view for managing farmer profiles (CRUD operations).

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web#model=dfr.farmer&view_type=list (example)

### 20.1.7. Request Schema
User interaction with Odoo form/list views

### 20.1.8. Response Schema
Rendered Odoo views, data persistence

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Odoo Views (XML/OWL)

### 20.1.12. Communication Protocol
HTTP/Odoo RPC

### 20.1.13. Layer Ids

- dfr_odoo_presentation

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-FHR-001  
- **Requirement Id:** REQ-FHR-008  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-farmer-registry-002

### 20.1.20. Requirements_Map

- REQ-FHR-001
- REQ-FHR-008

## 20.2. Household Admin View/Action
Odoo Admin Portal view for managing household profiles and members.

### 20.2.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
/web#model=dfr.household&view_type=list (example)

### 20.2.7. Request Schema
User interaction with Odoo form/list views

### 20.2.8. Response Schema
Rendered Odoo views, data persistence

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

- **Requirement Id:** REQ-FHR-001  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-farmer-registry-002

### 20.2.20. Requirements_Map

- REQ-FHR-001

## 20.3. Plot Admin View/Action
Odoo Admin Portal view for managing farm plot details, including geolocation.

### 20.3.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.3.5. Method
None

### 20.3.6. Url Pattern
/web#model=dfr.plot&view_type=list (example)

### 20.3.7. Request Schema
User interaction with Odoo form/list views

### 20.3.8. Response Schema
Rendered Odoo views, data persistence

### 20.3.9. Authentication Required
True

### 20.3.10. Authorization Required
True

### 20.3.11. Data Formats

- Odoo Views (XML/OWL)

### 20.3.12. Communication Protocol
HTTP/Odoo RPC

### 20.3.13. Layer Ids

- dfr_odoo_presentation

### 20.3.14. Dependencies


### 20.3.15. Requirements

- **Requirement Id:** REQ-FHR-005  
- **Requirement Id:** REQ-FHR-007  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- dfr_odoo_presentation

### 20.3.19. Components_Map

- dfr-module-farmer-registry-002

### 20.3.20. Requirements_Map

- REQ-FHR-005
- REQ-FHR-007

## 20.4. De-duplication Service Interface
Internal Python service for identifying and managing potential duplicate farmer records based on configurable rules and fuzzy matching.

### 20.4.4. Type
ODOO_MODULE_SERVICE_INTERFACE

### 20.4.5. Method
None

### 20.4.6. Url Pattern
None

### 20.4.7. Request Schema
Farmer data for comparison

### 20.4.8. Response Schema
List of potential duplicates or merged record

### 20.4.9. Authentication Required
False

### 20.4.10. Authorization Required
False

### 20.4.11. Data Formats

- Python Objects

### 20.4.12. Communication Protocol
Python Method Call

### 20.4.13. Layer Ids

- dfr_odoo_application_services

### 20.4.14. Dependencies


### 20.4.15. Requirements

- **Requirement Id:** REQ-FHR-012  
- **Requirement Id:** REQ-FHR-013  
- **Requirement Id:** REQ-FHR-014  
- **Requirement Id:** REQ-FHR-015  

### 20.4.16. Version
1.0

### 20.4.17. Is Public
False

### 20.4.18. Architecture_Map

- dfr_odoo_application_services

### 20.4.19. Components_Map

- dfr-module-farmer-registry-002

### 20.4.20. Requirements_Map

- REQ-FHR-012
- REQ-FHR-013
- REQ-FHR-014
- REQ-FHR-015

## 20.5. Consent Management Service Interface
Internal Python service for managing farmer consent for data collection and use, including recording, versioning, and withdrawal.

### 20.5.4. Type
ODOO_MODULE_SERVICE_INTERFACE

### 20.5.5. Method
None

### 20.5.6. Url Pattern
None

### 20.5.7. Request Schema
Farmer ID, consent status, consent version

### 20.5.8. Response Schema
Confirmation of consent update

### 20.5.9. Authentication Required
False

### 20.5.10. Authorization Required
False

### 20.5.11. Data Formats

- Python Objects

### 20.5.12. Communication Protocol
Python Method Call

### 20.5.13. Layer Ids

- dfr_odoo_application_services

### 20.5.14. Dependencies


### 20.5.15. Requirements

- **Requirement Id:** REQ-FHR-018  
- **Requirement Id:** REQ-SADG-008  

### 20.5.16. Version
1.0

### 20.5.17. Is Public
False

### 20.5.18. Architecture_Map

- dfr_odoo_application_services

### 20.5.19. Components_Map

- dfr-module-farmer-registry-002

### 20.5.20. Requirements_Map

- REQ-FHR-018
- REQ-SADG-008



---

