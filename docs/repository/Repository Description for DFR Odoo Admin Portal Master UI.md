# Repository Specification

# 1. Name
DFR Odoo Admin Portal Master UI


---

# 2. Description
This repository acts as a Master UI coordinator for the Digital Farmer Registry (DFR) Odoo Admin Portal. It integrates and orchestrates various DFR backend Odoo modules that contribute UI elements (views, menus, actions) to the Odoo Web Client, ensuring a cohesive and unified administrative user experience. Its primary responsibility is to serve as a meta-module or a top-level addon that declares dependencies on all functional DFR backend modules, thereby pulling them into a single, deployable administrative interface. This repository ensures that all administrative functionalities, such as farmer management, dynamic form building, user and role configuration, system settings, analytics dashboards, notification management, data import/export tools, and audit log viewing, are presented consistently within the Odoo backend. It facilitates the overall look and feel, navigation structure, and unified access to tools for National Administrators, Supervisors, and Super Administrators. It does not introduce new core business logic itself but focuses on the aggregation and presentation of UIs from underlying modules, aligning with REQ-PCA-005 for web interfaces. It also plays a role in managing shared UI context or state if necessary across different admin sections provided by disparate modules. This master UI ensures that all Odoo modules like dfr_farmer_registry, dfr_dynamic_forms, dfr_admin_settings, dfr_analytics, etc., are correctly loaded and their respective UIs are accessible from the main Odoo application menu in a structured manner. It simplifies deployment by ensuring all necessary UI-contributing backend modules are included.


---

# 3. Type
WebFrontend


---

# 4. Namespace
odoo.addons.dfr_admin_portal_master


---

# 5. Output Path
dfr_addons/dfr_admin_portal_master


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML


---

# 8. Technology
Odoo Web Client (JavaScript, XML, OWL), Odoo Framework


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_CORE_COMMON
- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS
- DFR_MOD_RBAC_CONFIG
- DFR_MOD_ADMIN_SETTINGS
- DFR_MOD_ANALYTICS_DASHBOARDS
- DFR_MOD_NOTIFICATIONS_ENGINE
- DFR_MOD_REST_API_CONFIG_UI
- DFR_MOD_EXTERNAL_CONNECTORS_CONFIG_UI
- DFR_MOD_DATA_MANAGEMENT_TOOLS
- DFR_MOD_LOCALIZATION_PACK_ADMIN_UI
- DFR_MOD_SECURITY_AUDIT_LOG_UI
- DFR_BUSINESS_PROCESS_ORCHESTRATOR_UI


---

# 11. Layer Ids

- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-PCA-005  
- **Requirement Id:** REQ-5-001  
- **Requirement Id:** REQ-SYSADM-001  
- **Requirement Id:** REQ-UIX-001  


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
REPO-01-MUI


---

# 17. Architecture_Map

- dfr_odoo_presentation


---

# 18. Components_Map

- DFR Admin Portal Views (XML, OWL, JS for Odoo Backend)


---

# 19. Requirements_Map

- REQ-PCA-005
- REQ-5-001
- REQ-SYSADM-001
- REQ-UIX-001


---

