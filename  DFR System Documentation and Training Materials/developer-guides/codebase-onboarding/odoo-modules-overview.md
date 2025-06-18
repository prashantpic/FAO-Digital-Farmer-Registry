# DFR Odoo Modules Overview

## 1. Introduction
Welcome to the Digital Farmer Registry (DFR) Odoo backend! This guide is intended for developers who are new to the DFR Odoo codebase. It provides an overview of the custom Odoo module structure, the purpose of key modules, important Odoo concepts as applied in DFR, and pointers for setting up your development environment.

**Target Audience:** Software Developers, Odoo Developers.
*Req IDs: D.1.4, E.1.4*

Familiarity with Odoo development principles is highly recommended. If you are new to Odoo, please refer to the official [Odoo Developer Documentation](https://www.odoo.com/documentation/master/developer.html) first.

## 2. DFR Odoo Addon Structure
The DFR backend is built as a collection of custom Odoo addons (modules). These addons reside in a dedicated `custom_addons` directory within the Odoo project structure.

Typical Odoo module structure:
```
custom_addons/
  ├── dfr_core/                  # Core functionalities, base models for DFR
  │   ├── __init__.py
  │   ├── __manifest__.py
  │   ├── models/
  │   │   ├── farmer.py
  │   │   └── household.py
  │   ├── views/
  │   │   ├── farmer_views.xml
  │   │   └── dfr_menus.xml
  │   ├── controllers/
  │   │   └── main.py
  │   ├── data/
  │   │   └── initial_data.xml
  │   ├── security/
  │   │   ├── ir.model.access.csv
  │   │   └── dfr_security_groups.xml
  │   └── static/
  │       └── ...
  ├── dfr_dynamic_forms/         # Module for dynamic form builder and submissions
  │   ├── ... (similar structure)
  ├── dfr_api/                   # Module for REST API endpoints
  │   ├── ... (similar structure)
  ├── dfr_gis/                   # GIS related functionalities, plot mapping
  │   ├── ... (similar structure)
  ├── dfr_country_xx_config/     # Example: Country-specific configurations for country XX
  │   ├── ... (similar structure)
  └── ... (other DFR specific modules)
```

## 3. Purpose of Key Custom DFR Modules

*   **`dfr_core` (or similar name like `dfr_base_registry`):**
    *   **Purpose:** Contains the foundational models for the DFR system, such as `dfr.farmer`, `dfr.household`, `dfr.farm`, `dfr.plot`, `dfr.administrative.area`.
    *   **Key Content:** Model definitions (Python), views (XML), base security groups, core menu items, and fundamental business logic related to these entities.
*   **`dfr_dynamic_forms`:**
    *   **Purpose:** Implements the dynamic form builder functionality and handles form submissions.
    *   **Key Content:** Models for `dfr.form.template`, `dfr.form.field`, `dfr.form.submission`, `dfr.form.response`. Views for designing forms and viewing submissions. Logic for form rendering and data validation.
*   **`dfr_api`:**
    *   **Purpose:** Exposes RESTful API endpoints for the DFR mobile application and potentially other external systems.
    *   **Key Content:** Odoo controllers defining API routes (e.g., `/api/v1/farmers`, `/api/v1/sync`). Authentication mechanisms (e.g., OAuth2, token-based). Data serialization/deserialization logic.
*   **`dfr_gis` (or integrated within `dfr_core`):**
    *   **Purpose:** Handles GIS-specific functionalities, such as storing and processing plot boundaries (polygons), calculating areas, and potentially integrating with map views.
    *   **Key Content:** May include models for GIS layers, helper functions for geometric operations. Fields for storing GeoJSON or WKT data.
*   **`dfr_notifications`:**
    *   **Purpose:** Manages system notifications (email, SMS if configured).
    *   **Key Content:** Models for notification templates, triggers, and logs. Integration with Odoo's mail and SMS gateways.
*   **`dfr_reports`:**
    *   **Purpose:** Contains custom reports and dashboards specific to DFR requirements.
    *   **Key Content:** QWeb report templates (XML/HTML), Python logic for report data preparation.
*   **`dfr_country_xx_config` (e.g., `dfr_vu_config` for Vanuatu):**
    *   **Purpose:** Holds configurations specific to a particular country deployment. This helps in keeping the core modules generic.
    *   **Key Content:** Initial data for administrative hierarchies, country-specific form templates, default user roles/groups, translations, specific report layouts if needed.
    *   Depends on core DFR modules.

`[Placeholder: Add more DFR modules as they are defined and their specific purposes.]`

## 4. Key Odoo Concepts in DFR
*   **Models:** Python classes inheriting from `models.Model` define the data structure (database tables). See [Core Entities Schema](../../architecture/data-model/core-entities-schema.md).
*   **Views:** XML definitions control how data is presented to users (forms, lists/trees, kanban, search views, graphs).
*   **Controllers:** Python classes inheriting from `http.Controller` define web routes and API endpoints.
*   **Wizards:** Transient models (`models.TransientModel`) used for interactive dialogs and multi-step operations.
*   **Server Actions & Automated Actions:** Configure automated processes based on triggers or conditions.
*   **Security:**
    *   **Groups (`res.groups`):** Define user roles (e.g., Enumerator, Administrator, Supervisor).
    *   **Access Control Lists (ACLs - `ir.model.access.csv`):** Control read, write, create, delete permissions per model per group.
    *   **Record Rules (`ir.rule`):** Implement row-level security based on defined domains/filters.
*   **ORM (Object-Relational Mapper):** Odoo's ORM provides powerful methods for database interaction (e.g., `search()`, `browse()`, `create()`, `write()`, `unlink()`).
*   **Inheritance:** Odoo's inheritance mechanisms (`_inherit`, `_inherits`) are extensively used to extend existing models and views (both Odoo base modules and DFR core modules).
*   **QWeb Templates:** XML-based templating engine used for generating dynamic web pages and reports.

## 5. Development Environment Setup
Refer to the [Setup Development Environment](./setup-development-environment.md) guide for detailed step-by-step instructions. Key components include:
*   Python (version compatible with Odoo 18.0, e.g., 3.10+).
*   PostgreSQL server.
*   Odoo 18.0 source code.
*   Cloned DFR custom addons repository.
*   Appropriate IDE (e.g., PyCharm, VS Code) with Python and Odoo development plugins/extensions.
*   Odoo configuration file (`odoo.conf`) pointing to your custom addons path.

## 6. Coding Standards and Best Practices
*   Follow [DFR Coding Standards](../../standards/coding-standards.md), which includes PEP 8 for Python and Odoo-specific guidelines.
*   Write clear, maintainable, and well-commented code. See [DFR Documentation Standards](../../standards/documentation-standards.md).
*   Develop unit tests for your business logic. `[Placeholder: Link to testing strategy and how to write tests for DFR modules]`.
*   Use Odoo's internationalization features for all user-facing strings.
*   Optimize database queries and be mindful of performance implications.
*   Adhere to the [Codebase Governance Framework](../../codebase-governance/framework.md) for branching, versioning, and contributions.

## 7. Debugging Odoo
*   **Odoo Shell:** `odoo-bin shell -c /path/to/odoo.conf -d <database_name>` for interactive debugging.
*   **Logging:** Use Python's `logging` module. Odoo logs extensively; configure log levels in `odoo.conf`.
    ```python
    import logging
    _logger = logging.getLogger(__name__)
    _logger.info("This is an info message.")
    _logger.debug("This is a debug message for farmer ID: %s", farmer_id)
    ```
*   **Python Debugger (PDB / IDE Debugger):** Set breakpoints in your Python code.
    ```python
    import pdb; pdb.set_trace()
    ```
    Or use your IDE's debugging capabilities.
*   **Browser Developer Tools:** For frontend issues (JavaScript errors, network requests, OWL component inspection).
*   **Odoo Developer Mode:** Activate from the Odoo UI (Settings -> Activate the developer mode) to access technical features, view metadata, and debug views.

## 8. Key Files and Directories in a Module
*   `__manifest__.py`: Module descriptor (name, version, dependencies, data files, etc.).
*   `__init__.py`: Imports subdirectories (e.g., `models`, `controllers`).
*   `models/`: Contains Python files defining Odoo models.
*   `views/`: Contains XML files defining views, menus, and actions.
*   `controllers/`: Contains Python files defining web controllers (for website pages or API endpoints).
*   `security/`:
    *   `ir.model.access.csv`: Defines model access rights for security groups.
    *   XML files defining security groups and record rules.
*   `data/`: Contains XML files for loading initial/demo data.
*   `static/`: For static assets (CSS, JS, images) used by the module's frontend components.
    *   `static/src/scss/`, `static/src/js/`, `static/src/xml/` (for OWL templates).
*   `tests/`: For unit and integration tests.

This overview should provide a good starting point for understanding the DFR Odoo codebase. Refer to specific module READMEs and the guides linked throughout this document for more detailed information.