# Repository Specification

# 1. Name
DFR Analytics and Reporting Module


---

# 2. Description
Provides dashboards with real-time KPIs, map-based visualizations, data filtering, and exportable reports (CSV, XLSX, PDF) for farmer and dynamic form data. Configured and accessed via Admin Portal.


---

# 3. Type
DataAnalytics


---

# 4. Namespace
odoo.addons.dfr_analytics


---

# 5. Output Path
dfr_addons/dfr_analytics


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML, JavaScript, OWL


---

# 8. Technology
Odoo ORM, Odoo Dashboard Module, Odoo Reporting Engine (QWeb), Leaflet.js (optional)


---

# 9. Thirdparty Libraries

- OCA web_map (evaluate)
- OCA web_google_maps (evaluate)


---

# 10. Dependencies

- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS
- DFR_MOD_RBAC_CONFIG


---

# 11. Layer Ids

- dfr_odoo_presentation
- dfr_odoo_application_services


---

# 12. Requirements

- **Requirement Id:** REQ-7-001  
- **Requirement Id:** REQ-7-002  
- **Requirement Id:** REQ-7-004  
- **Requirement Id:** REQ-7-006  


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
DFR_MOD_ANALYTICS_REPORTING


---

# 17. Architecture_Map

- dfr_odoo_presentation
- dfr_odoo_application_services


---

# 18. Components_Map

- dfr-module-analytics-dashboards-006


---

# 19. Requirements_Map

- REQ-7-001
- REQ-7-002
- REQ-7-004
- REQ-7-006


---

# 20. Endpoints

## 20.1. Analytics Dashboard Admin View/Action
Odoo Admin Portal UI displaying key performance indicators (KPIs), charts, and summaries.

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web#action=dfr_dashboard_action (example)

### 20.1.7. Request Schema
User navigation to dashboard.

### 20.1.8. Response Schema
Rendered dashboard with visualizations.

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Odoo Views (XML/OWL)
- JSON (for chart data)

### 20.1.12. Communication Protocol
HTTP/Odoo RPC

### 20.1.13. Layer Ids

- dfr_odoo_presentation

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-7-001  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-analytics-dashboards-006

### 20.1.20. Requirements_Map

- REQ-7-001

## 20.2. Map Visualization Admin View/Action
Odoo Admin Portal UI for map-based visualizations of farmer and plot locations.

### 20.2.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.2.5. Method
None

### 20.2.6. Url Pattern
/web (specific Odoo map view action)

### 20.2.7. Request Schema
User interaction with map controls.

### 20.2.8. Response Schema
Rendered map with plotted data.

### 20.2.9. Authentication Required
True

### 20.2.10. Authorization Required
True

### 20.2.11. Data Formats

- Odoo Views (XML/OWL)
- GeoJSON

### 20.2.12. Communication Protocol
HTTP/Odoo RPC

### 20.2.13. Layer Ids

- dfr_odoo_presentation

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-7-002  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_odoo_presentation

### 20.2.19. Components_Map

- dfr-module-analytics-dashboards-006

### 20.2.20. Requirements_Map

- REQ-7-002

## 20.3. Report Export Admin Action
Odoo Admin Portal functionality for filtering data and exporting reports in CSV, XLSX, or PDF formats.

### 20.3.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.3.5. Method
None

### 20.3.6. Url Pattern
/web (Odoo export controllers or report actions)

### 20.3.7. Request Schema
Filters, selected format.

### 20.3.8. Response Schema
File download (CSV, XLSX, PDF).

### 20.3.9. Authentication Required
True

### 20.3.10. Authorization Required
True

### 20.3.11. Data Formats

- CSV
- XLSX
- PDF

### 20.3.12. Communication Protocol
HTTP

### 20.3.13. Layer Ids

- dfr_odoo_presentation
- dfr_odoo_application_services

### 20.3.14. Dependencies


### 20.3.15. Requirements

- **Requirement Id:** REQ-7-004  
- **Requirement Id:** REQ-7-006  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- dfr_odoo_presentation
- dfr_odoo_application_services

### 20.3.19. Components_Map

- dfr-module-analytics-dashboards-006

### 20.3.20. Requirements_Map

- REQ-7-004
- REQ-7-006



---

