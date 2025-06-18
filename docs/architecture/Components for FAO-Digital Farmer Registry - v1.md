# Architecture Design Specification

# 1. Components

- **Components:**
  
  ### .1. DFR Common Core Module
  Provides shared utilities, base models/mixins, core configurations, and implements foundational architectural principles (e.g., DPI). Serves as a base for other DFR-specific Odoo modules.

  #### .1.4. Type
  Odoo Addon

  #### .1.5. Dependencies
  
  
  #### .1.6. Properties
  
  - **Technical_Name:** dfr_common
  - **Version:** 1.0.0
  
  #### .1.7. Interfaces
  
  - **Name:** Base DFR Models/Mixins  
**Type:** Python Classes  
  - **Name:** Shared Utility Functions  
**Type:** Python API  
  
  #### .1.8. Technology
  Odoo 18, Python

  #### .1.9. Resources
  
  
  #### .1.10. Configuration
  
  - **Central_Config_Parameters:** via ir.config_parameter
  
  #### .1.11. Responsible Features
  
  - REQ-PCA-002
  - REQ-PCA-003
  - REQ-PCA-008
  - REQ-PCA-011
  - REQ-PCA-016
  
  #### .1.12. Security
  
  - **Remarks:** Establishes base security practices for other modules.
  
  ### .2. Farmer Registry Module
  Manages core farmer, household, farm, and plot data, including UIDs, KYC, consent management, status workflows, and de-duplication logic.

  #### .2.4. Type
  Odoo Addon

  #### .2.5. Dependencies
  
  - dfr-common-module
  - odoo-security-config
  - audit-logging-module
  
  #### .2.6. Properties
  
  - **Technical_Name:** dfr_farmer_registry
  - **Version:** 1.0.0
  
  #### .2.7. Interfaces
  
  - **Name:** Farmer Model (dfr.farmer)  
**Type:** Odoo Model  
  - **Name:** Household Model (dfr.household)  
**Type:** Odoo Model  
  - **Name:** Plot Model (dfr.plot)  
**Type:** Odoo Model  
  - **Name:** De-duplication Service  
**Type:** Python API  
  
  #### .2.8. Technology
  Odoo 18, Python, PostgreSQL

  #### .2.9. Resources
  
  
  #### .2.10. Configuration
  
  - **Deduplication_Rules:** Configurable via Odoo UI
  - **Farmer_Statuses:** Configurable selection field & workflows
  
  #### .2.11. Responsible Features
  
  - Farmer & Household Registration Management
  - REQ-FHR-001
  - REQ-FHR-002
  - REQ-FHR-006
  - REQ-FHR-012
  - REQ-FHR-015
  - REQ-FHR-018
  
  #### .2.12. Security
  
  - **Remarks:** Implements RBAC for farmer data, consent field protections.
  
  ### .3. Dynamic Form Engine Module
  Allows administrators to design, manage, and version custom data collection forms with various field types, validation rules, and conditional logic. Manages form submissions.

  #### .3.4. Type
  Odoo Addon

  #### .3.5. Dependencies
  
  - dfr-common-module
  - farmer-registry-module
  - odoo-security-config
  
  #### .3.6. Properties
  
  - **Technical_Name:** dfr_dynamic_forms
  - **Version:** 1.0.0
  
  #### .3.7. Interfaces
  
  - **Name:** Dynamic Form Model (dfr.form)  
**Type:** Odoo Model  
  - **Name:** Form Field Model (dfr.form.field)  
**Type:** Odoo Model  
  - **Name:** Form Submission Model (dfr.form.submission)  
**Type:** Odoo Model  
  - **Name:** Form Builder UI  
**Type:** Odoo Admin View  
  
  #### .3.8. Technology
  Odoo 18, Python, JavaScript/OWL (for builder UI)

  #### .3.9. Resources
  
  
  #### .3.10. Configuration
  
  - **Field_Types_Supported:** Text, Number, Date, Selection, GPS, Image
  - **Validation_Rules_Engine:** Odoo constraints & custom logic
  
  #### .3.11. Responsible Features
  
  - Dynamic Form Engine & Management
  - REQ-3-001
  - REQ-3-002
  - REQ-3-003
  - REQ-3-004
  - REQ-3-008
  
  #### .3.12. Security
  
  - **Remarks:** RBAC for form design, publication, and submission access.
  
  ### .4. Analytics and Reporting Module
  Provides dashboards, KPIs, map-based visualizations, data filtering, and export functionalities for farmer and dynamic form data.

  #### .4.4. Type
  Odoo Addon

  #### .4.5. Dependencies
  
  - farmer-registry-module
  - dynamic-form-engine-module
  - odoo-security-config
  
  #### .4.6. Properties
  
  - **Technical_Name:** dfr_analytics
  - **Version:** 1.0.0
  
  #### .4.7. Interfaces
  
  - **Name:** DFR Dashboard  
**Type:** Odoo Dashboard View  
  - **Name:** Custom QWeb Reports  
**Type:** Odoo Reports  
  - **Name:** Data Export API (CSV, XLSX)  
**Type:** Odoo Standard Export  
  
  #### .4.8. Technology
  Odoo 18, Python, XML (views), QWeb (reports)

  #### .4.9. Resources
  
  
  #### .4.10. Configuration
  
  - **Kpi_Definitions:** Configurable
  - **Report_Filters:** Standard Odoo search views
  
  #### .4.11. Responsible Features
  
  - Analytics & Reporting
  - REQ-7-001
  - REQ-7-002
  - REQ-7-004
  - REQ-7-006
  
  #### .4.12. Security
  
  - **Remarks:** RBAC for accessing reports and data scope.
  
  ### .5. Notification System Module
  Manages and sends automated notifications (SMS, email, push) based on system events, using configurable templates and integrating with third-party gateways.

  #### .5.4. Type
  Odoo Addon

  #### .5.5. Dependencies
  
  - dfr-common-module
  - farmer-registry-module
  - dynamic-form-engine-module
  - external-integration-connectors-module
  
  #### .5.6. Properties
  
  - **Technical_Name:** dfr_notifications
  - **Version:** 1.0.0
  
  #### .5.7. Interfaces
  
  - **Name:** Notification Template Model  
**Type:** Odoo Model  
  - **Name:** Notification Sending Service  
**Type:** Python API  
  - **Name:** Gateway Configuration UI  
**Type:** Odoo Admin View  
  
  #### .5.8. Technology
  Odoo 18, Python

  #### .5.9. Resources
  
  
  #### .5.10. Configuration
  
  - **Supported_Channels:** SMS, Email, Mobile Push (via FCM integration)
  - **Template_Language:** QWeb/Jinja
  
  #### .5.11. Responsible Features
  
  - Notification System
  - REQ-NS-001
  - REQ-NS-003
  - REQ-NS-005
  - REQ-SYSADM-004
  
  #### .5.12. Security
  
  - **Remarks:** Secure storage of gateway credentials.
  
  ### .6. API Service Module
  Provides a secure RESTful API layer for mobile application data synchronization and external system integrations, compliant with OpenAPI v3.x and using OAuth2/JWT authentication.

  #### .6.4. Type
  Odoo Addon

  #### .6.5. Dependencies
  
  - farmer-registry-module
  - dynamic-form-engine-module
  - odoo-security-config
  
  #### .6.6. Properties
  
  - **Technical_Name:** dfr_api_services
  - **Version:** 1.0.0
  
  #### .6.7. Interfaces
  
  - **Name:** Mobile Sync API (/api/mobile/sync)  
**Type:** REST/JSON (OpenAPI v3.x)  
  - **Name:** Farmer Data API (/api/farmer)  
**Type:** REST/JSON (OpenAPI v3.x)  
  - **Name:** Dynamic Form API (/api/form)  
**Type:** REST/JSON (OpenAPI v3.x)  
  
  #### .6.8. Technology
  Odoo 18, Python, OAuth2/JWT libraries

  #### .6.9. Resources
  
  
  #### .6.10. Configuration
  
  - **Authentication_Method:** OAuth2/JWT
  - **Api_Versioning_Strategy:** URL path based
  
  #### .6.11. Responsible Features
  
  - API & External Integrations
  - REQ-PCA-007
  - REQ-API-001
  - REQ-API-002
  - REQ-API-005
  
  #### .6.12. Security
  
  - **Remarks:** Enforces HTTPS, OAuth2/JWT authentication, RBAC on API endpoints.
  
  ### .7. External Integration Connectors Module
  Contains connectors and adapters for specific third-party systems like National ID validation, weather services, and potentially complex payment gateways if not covered by basic notification gateways.

  #### .7.4. Type
  Odoo Addon

  #### .7.5. Dependencies
  
  - api-service-module
  - dfr-common-module
  
  #### .7.6. Properties
  
  - **Technical_Name:** dfr_integrations
  - **Version:** 1.0.0
  
  #### .7.7. Interfaces
  
  - **Name:** National ID Validation Service Client  
**Type:** Python API  
  - **Name:** Weather Service Client  
**Type:** Python API  
  
  #### .7.8. Technology
  Python, Requests library, Specific SDKs

  #### .7.9. Resources
  
  
  #### .7.10. Configuration
  
  - **External_Api_Keys:** Securely configurable per country instance
  
  #### .7.11. Responsible Features
  
  - REQ-API-007
  - REQ-API-011
  - REQ-FHR-006 (for NID integration part)
  
  #### .7.12. Security
  
  - **Remarks:** Secure handling of external API credentials and data exchange.
  
  ### .8. Data Management Toolkit Module
  Provides tools for bulk data import/export (CSV, XLSX) and supports data migration activities, enhancing Odoo's standard capabilities with custom wizards or scripts if needed.

  #### .8.4. Type
  Odoo Addon

  #### .8.5. Dependencies
  
  - farmer-registry-module
  - dynamic-form-engine-module
  - dfr-common-module
  
  #### .8.6. Properties
  
  - **Technical_Name:** dfr_data_tools
  - **Version:** 1.0.0
  
  #### .8.7. Interfaces
  
  - **Name:** Bulk Import Wizard  
**Type:** Odoo Admin View  
  - **Name:** Data Export Functionality  
**Type:** Odoo Standard/Custom Export  
  
  #### .8.8. Technology
  Odoo 18, Python

  #### .8.9. Resources
  
  
  #### .8.10. Configuration
  
  - **Supported_Formats:** CSV, XLSX
  - **Validation_Reporting:** Detailed error logs
  
  #### .8.11. Responsible Features
  
  - Data Management (Import, Export, Migration)
  - REQ-DM-001
  - REQ-DM-002
  - REQ-DM-007
  
  #### .8.12. Security
  
  - **Remarks:** RBAC controls access to import/export functions.
  
  ### .9. Farmer Self-Service Portal Module
  Extends Odoo Website module to provide a public-facing portal for farmer pre-registration, informational content, and access to specific dynamic forms.

  #### .9.4. Type
  Odoo Addon

  #### .9.5. Dependencies
  
  - farmer-registry-module
  - dynamic-form-engine-module
  - odoo-localization-engine
  
  #### .9.6. Properties
  
  - **Technical_Name:** dfr_farmer_portal
  - **Version:** 1.0.0
  
  #### .9.7. Interfaces
  
  - **Name:** Pre-registration Form Page  
**Type:** Public Web Page  
  - **Name:** Informational Content Pages  
**Type:** Public Web Page  
  - **Name:** Farmer-Accessible Dynamic Forms  
**Type:** Public Web Page  
  
  #### .9.8. Technology
  Odoo 18 Website Module (QWeb, JavaScript, CSS)

  #### .9.9. Resources
  
  
  #### .9.10. Configuration
  
  - **Portal_Access_Toggle:** Configurable by National Admin
  - **Branding:** Country-specific
  
  #### .9.11. Responsible Features
  
  - Farmer Self-Service Portal
  - REQ-FSSP-001
  - REQ-FSSP-003
  - REQ-FSSP-009
  
  #### .9.12. Security
  
  - **Remarks:** Public access for pre-registration, authenticated access for registered farmers (future).
  
  ### .10. Audit Logging Enhancements Module
  Enhances Odoo's native auditing capabilities (`mail.thread`) if more detailed or specific audit trails are required for critical DFR operations.

  #### .10.4. Type
  Odoo Addon

  #### .10.5. Dependencies
  
  - dfr-common-module
  
  #### .10.6. Properties
  
  - **Technical_Name:** dfr_audit_log_enhancements
  - **Version:** 1.0.0
  
  #### .10.7. Interfaces
  
  - **Name:** Custom Audit Log Model (if needed)  
**Type:** Odoo Model  
  - **Name:** Audit Log Viewing Interface  
**Type:** Odoo Admin View  
  
  #### .10.8. Technology
  Odoo 18, Python

  #### .10.9. Resources
  
  
  #### .10.10. Configuration
  
  - **Audited_Actions_Config:** Defines what gets logged beyond Odoo defaults
  
  #### .10.11. Responsible Features
  
  - Security, Auditing & Data Governance
  - REQ-FHR-010
  - REQ-SADG-005
  - REQ-SADG-006
  
  #### .10.12. Security
  
  - **Remarks:** Secure storage and restricted access to audit logs.
  
  ### .11. Odoo Security Framework Configuration
  Configuration of Odoo's native Role-Based Access Control (RBAC) mechanisms, including user groups, access control lists (ACLs), and record rules. This is not a single module but a collection of security configurations within all DFR modules and Odoo core settings.

  #### .11.4. Type
  Framework Configuration

  #### .11.5. Dependencies
  
  
  #### .11.6. Properties
  
  
  #### .11.7. Interfaces
  
  - **Name:** User Roles (res.groups)  
**Type:** Odoo Data  
  - **Name:** Model Access Rights (ir.model.access)  
**Type:** Odoo Data  
  - **Name:** Record Rules (ir.rule)  
**Type:** Odoo Data  
  
  #### .11.8. Technology
  Odoo 18 (XML, CSV definitions)

  #### .11.9. Resources
  
  
  #### .11.10. Configuration
  
  - **Password_Policies:** Configurable in Odoo settings
  - **Mfa_Recommendation:** Strongly recommended for admins
  
  #### .11.11. Responsible Features
  
  - User Management & Access Control (RBAC)
  - REQ-PCA-018
  - REQ-5-001
  - REQ-5-004
  - REQ-5-011
  - REQ-SADG-001
  
  #### .11.12. Security
  
  - **Remarks:** Core of the system's security posture.
  
  ### .12. Odoo Localization Engine
  Leverages Odoo's built-in internationalization (i18n) and localization (l10n) capabilities, including `.po` file management for translating UI elements, dynamic form content, and notification templates.

  #### .12.4. Type
  Framework Feature

  #### .12.5. Dependencies
  
  
  #### .12.6. Properties
  
  
  #### .12.7. Interfaces
  
  - **Name:** Translation Files (.po)  
**Type:** Data Files  
  - **Name:** Language Management UI  
**Type:** Odoo Admin View  
  
  #### .12.8. Technology
  Odoo 18 i18n

  #### .12.9. Resources
  
  
  #### .12.10. Configuration
  
  - **Active_Languages:** Configurable per country instance
  - **Date_Time_Number_Formats:** Localized based on user/country settings
  
  #### .12.11. Responsible Features
  
  - Localization & Multilingual Support
  - REQ-PCA-018
  - REQ-LMS-001
  - REQ-LMS-002
  - REQ-LMS-004
  
  #### .12.12. Security
  
  
  ### .13. Mobile Presentation Layer (UI)
  Handles user interface rendering, user input, and navigation for the Android enumerator application.

  #### .13.4. Type
  Mobile Layer

  #### .13.5. Dependencies
  
  - mobile-app-logic-layer
  
  #### .13.6. Properties
  
  - **Ui_Paradigm:** Native (Activities/Fragments/Compose) or Cross-platform (Flutter Widgets)
  
  #### .13.7. Interfaces
  
  - **Name:** Farmer Registration Screens  
**Type:** Mobile UI View  
  - **Name:** Dynamic Form Rendering View  
**Type:** Mobile UI View  
  - **Name:** GPS Capture Interface  
**Type:** Mobile UI View  
  
  #### .13.8. Technology
  Android (Kotlin/Java or Flutter/Dart)

  #### .13.9. Resources
  
  
  #### .13.10. Configuration
  
  
  #### .13.11. Responsible Features
  
  - Mobile Application (Enumerator Focused)
  - REQ-4-002
  - REQ-4-010
  
  #### .13.12. Security
  
  
  ### .14. Mobile Application Logic Layer
  Manages UI state, client-side validation, business logic execution, and workflow orchestration on the mobile device.

  #### .14.4. Type
  Mobile Layer

  #### .14.5. Dependencies
  
  - mobile-presentation-layer
  - mobile-data-layer
  - mobile-cross-cutting-layer
  
  #### .14.6. Properties
  
  - **Architecture_Pattern:** MVVM, MVI, BLoC/Provider
  
  #### .14.7. Interfaces
  
  - **Name:** ViewModels/BLoCs/Controllers  
**Type:** Internal API  
  - **Name:** Use Cases/Interactors  
**Type:** Internal API  
  
  #### .14.8. Technology
  Android (Kotlin/Java or Flutter/Dart)

  #### .14.9. Resources
  
  
  #### .14.10. Configuration
  
  
  #### .14.11. Responsible Features
  
  - Mobile Application (Enumerator Focused)
  - REQ-4-003 (offline logic)
  - REQ-4-016 (local de-dupe)
  
  #### .14.12. Security
  
  
  ### .15. Mobile Data Layer
  Manages local data storage (encrypted SQLite), data access objects (DAOs), API communication with the Odoo backend, and the bi-directional synchronization engine including conflict resolution.

  #### .15.4. Type
  Mobile Layer

  #### .15.5. Dependencies
  
  - api-service-module
  
  #### .15.6. Properties
  
  - **Local_Database:** SQLite with SQLCipher (AES-256)
  - **Api_Client:** Retrofit/OkHttp or Dio
  
  #### .15.7. Interfaces
  
  - **Name:** Repository Pattern Implementation  
**Type:** Internal API  
  - **Name:** Synchronization Service  
**Type:** Internal API  
  - **Name:** Local DAOs  
**Type:** Internal API  
  
  #### .15.8. Technology
  Android (Kotlin/Java or Flutter/Dart), SQLite, SQLCipher

  #### .15.9. Resources
  
  
  #### .15.10. Configuration
  
  - **Sync_Frequency:** User-triggered or periodic (configurable)
  - **Conflict_Resolution_Strategy:** Timestamp-based or server-wins (defined)
  
  #### .15.11. Responsible Features
  
  - Mobile Application (Enumerator Focused)
  - REQ-PCA-006
  - REQ-4-003
  - REQ-4-004
  - REQ-4-006
  - REQ-4-007
  
  #### .15.12. Security
  
  - **Remarks:** AES-256 encryption for local data, secure key management.
  
  ### .16. Mobile Cross-Cutting Services Layer
  Provides common utilities for the mobile app, such as GPS location services, QR code scanning, local logging, secure encryption key management, and app update checks.

  #### .16.4. Type
  Mobile Layer

  #### .16.5. Dependencies
  
  
  #### .16.6. Properties
  
  
  #### .16.7. Interfaces
  
  - **Name:** Location Service  
**Type:** Internal API  
  - **Name:** QR Scanner Service  
**Type:** Internal API  
  - **Name:** Secure Storage Service  
**Type:** Internal API  
  - **Name:** Logging Service  
**Type:** Internal API  
  
  #### .16.8. Technology
  Android APIs (LocationManager, CameraX) or Flutter Plugins (geolocator, qr_code_scanner, flutter_secure_storage)

  #### .16.9. Resources
  
  
  #### .16.10. Configuration
  
  
  #### .16.11. Responsible Features
  
  - Mobile Application (Enumerator Focused)
  - REQ-4-008
  - REQ-4-009
  - REQ-4-011
  - REQ-4-013
  
  #### .16.12. Security
  
  - **Remarks:** Secure key management using Android Keystore or equivalent.
  
  ### .17. Deployment and Operations Services
  Encompasses the infrastructure, tools, and processes for deploying, managing, monitoring, and maintaining the DFR system. Includes CI/CD pipelines, containerization, backup/restore, and monitoring.

  #### .17.4. Type
  Infrastructure Services

  #### .17.5. Dependencies
  
  
  #### .17.6. Properties
  
  - **Ci_Cd_Tools:** Jenkins, GitLab CI, or GitHub Actions
  - **Containerization:** Docker
  - **Monitoring_Tools:** Prometheus/Grafana, Zabbix, or Cloud Provider tools
  
  #### .17.7. Interfaces
  
  - **Name:** Deployment Scripts/Pipelines  
**Type:** DevOps Processes  
  - **Name:** Monitoring Dashboard  
**Type:** Operational UI  
  - **Name:** Backup & Restore Procedures  
**Type:** Operational Guides  
  
  #### .17.8. Technology
  Docker, Linux, Nginx, PostgreSQL, CI/CD tooling

  #### .17.9. Resources
  
  
  #### .17.10. Configuration
  
  - **Deployment_Environments:** Development, Staging, Production per country
  - **Backup_Strategy:** Daily pg_dump/WAL archiving, offsite storage
  - **Rto_Rpo_Targets:** Defined per country DR plan
  
  #### .17.11. Responsible Features
  
  - Deployment, Infrastructure & Operations Management
  - REQ-PCA-012
  - REQ-PCA-015
  - REQ-DIO-002
  - REQ-DIO-006
  - REQ-DIO-007
  - REQ-DIO-009
  - REQ-DIO-011
  
  #### .17.12. Security
  
  - **Remarks:** HTTPS enforcement, secure credential management for infrastructure.
  
  
- **Configuration:**
  
  - **Platform Version:** Odoo 18.0 Community Edition
  - **Database System:** PostgreSQL
  - **Backend Language:** Python
  - **Mobile Platform:** Android (Native Kotlin/Java or Cross-platform Flutter/Dart)
  - **Api Standard:** RESTful JSON, OpenAPI v3.x
  - **Authentication Standard:** OAuth2/JWT
  - **Version Control:** Git (GitHub/GitLab)
  - **Semantic Versioning:** 2.0.0
  - **Default License:** MIT or Apache 2.0
  


---

# 2. Component_Relations

- **Architecture:**
  
  - **Components:**
    
    - **Id:** dfr-module-core-001  
**Name:** DFR Core Utilities  
**Description:** Provides core shared utilities, base models (if any), abstract classes, common configurations, and helps enforce platform architecture principles. Manages shared codebase governance aspects.  
**Type:** OdooModule  
**Dependencies:**
    
    - Odoo Framework (base, mail)
    
**Properties:**
    
    - **Layer:** DFR Cross-Cutting Concerns / DFR Odoo Domain Models (base parts)
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Services
    - Shared Python utilities
    
**Technology:** Odoo 18 CE, Python  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    - **Storage:** Part of Odoo filestore/DB
    
**Configuration:**
    
    - **Platform_Version_Enforcement:** Odoo 18.0 CE
    - **Base_License_Policy:** MIT or Apache 2.0 (as per REQ-CM-001)
    
**Health Check:**
    
    - **Path:** N/A (Part of Odoo Framework Health)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-001
    - REQ-PCA-002
    - REQ-PCA-003
    - REQ-PCA-008
    - REQ-PCA-009
    - REQ-PCA-011
    - REQ-PCA-016
    - REQ-PCA-017
    - REQ-CM-004
    - REQ-CM-013
    - REQ-CM-006
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-module-farmer-registry-002  
**Name:** DFR Farmer Registry Engine  
**Description:** Manages farmer, household, farm, and plot data models, unique identifiers, CRUD operations, status lifecycle, de-duplication logic, consent management, and KYC workflow hooks. Implements the core farmer data schema.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - Odoo Framework (ORM, mail)
    
**Properties:**
    
    - **Layer:** DFR Odoo Domain Models / DFR Odoo Application Services
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Models (ORM API)
    - Odoo Services for business logic
    - Odoo Views for Admin Portal
    
**Technology:** Odoo 18 CE, Python, XML  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    - **Storage:** PostgreSQL (Farmer, Household, Plot tables etc.)
    
**Configuration:**
    
    - **Uid_Sequence_Prefix:** Configurable per country
    - **Deduplication_Fields:** Configurable (National ID, Name+DOB+Village)
    - **Farmer_Statuses:** Configurable selection list
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-FHR-001
    - REQ-FHR-002
    - REQ-FHR-003
    - REQ-FHR-004
    - REQ-FHR-005
    - REQ-FHR-006
    - REQ-FHR-007
    - REQ-FHR-010
    - REQ-FHR-011
    - REQ-FHR-012
    - REQ-FHR-013
    - REQ-FHR-014
    - REQ-FHR-015
    - REQ-FHR-016
    - REQ-FHR-018
    - REQ-PCA-018
    - REQ-FHR-017
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - National Administrator
      - Supervisor
      - Enumerator
      
    
    - **Id:** dfr-module-dynamic-forms-003  
**Name:** DFR Dynamic Form Engine  
**Description:** Enables administrators to design custom data collection forms (fields, validation, conditional logic, versioning, tags), manages form submissions, and links submissions to farmers. Supports rendering forms in web and mobile.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - dfr-module-farmer-registry-002
    - Odoo Framework (ORM, Web Client)
    
**Properties:**
    
    - **Layer:** DFR Odoo Domain Models / DFR Odoo Application Services / DFR Odoo Presentation Layer
    - **Version:** 1.0.0
    - **Oca_Evaluation:** Survey, FormIO components (REQ-3-012)
    
**Interfaces:**
    
    - Odoo Models (Form Definition, Submission)
    - Odoo Services for form logic
    - Odoo Views for Form Builder UI
    
**Technology:** Odoo 18 CE, Python, XML, JavaScript/OWL  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    - **Storage:** PostgreSQL (Form definition & submission tables)
    
**Configuration:**
    
    - **Supported_Field_Types:** Text, Number, Date, Selection, GPS, Image
    - **Form_Versioning_Scheme:** Major.Minor
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-3-001
    - REQ-3-002
    - REQ-3-003
    - REQ-3-004
    - REQ-3-005
    - REQ-3-006
    - REQ-3-007
    - REQ-3-008
    - REQ-3-009
    - REQ-3-010
    - REQ-3-011
    - REQ-3-012
    - REQ-3-013
    - REQ-3-014
    - REQ-SYSADM-005
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - National Administrator (design)
      - Enumerator/Farmer (submission)
      
    
    - **Id:** dfr-module-rbac-config-004  
**Name:** DFR RBAC Configuration  
**Description:** Defines DFR-specific user roles as Odoo groups, configures access control lists (ir.model.access.csv) and record rules (ir.rule) for all DFR modules to enforce granular permissions and data scoping.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - Odoo Framework (res.groups, ir.model.access, ir.rule)
    
**Properties:**
    
    - **Layer:** DFR Security Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Security Group definitions
    - Odoo Access Control List files
    - Odoo Record Rule definitions
    
**Technology:** Odoo 18 CE, XML, Python (for complex record rules if any)  
**Resources:**
    
    - **Cpu:** N/A (Configuration data)
    - **Memory:** N/A (Configuration data)
    
**Configuration:**
    
    - **Defined_Roles:** Super Administrator, National Administrator, Supervisor, Enumerator, Farmer, Support Team, IT Team, Policy Maker/Analyst
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-5-001
    - REQ-5-002
    - REQ-5-003
    - REQ-5-004
    - REQ-5-005
    - REQ-5-006
    - REQ-5-007
    - REQ-5-009
    - REQ-5-010
    - REQ-5-011
    - REQ-5-013
    - REQ-5-014
    - REQ-SADG-001
    - REQ-FHR-008
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-module-admin-settings-005  
**Name:** DFR Admin Settings Panel  
**Description:** Provides centralized Odoo admin views for country-specific configurations, system-wide parameters not covered by other DFR modules, de-duplication rule settings, and audit log access.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - dfr-module-farmer-registry-002
    - dfr-module-dynamic-forms-003
    - dfr-module-notifications-engine-007
    - Odoo Framework (ir.config_parameter)
    
**Properties:**
    
    - **Layer:** DFR Odoo Presentation Layer / DFR Odoo Application Services
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Admin Views (Settings Panels)
    
**Technology:** Odoo 18 CE, Python, XML  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Country_Specific_Params_Model:** res.config.settings extension or custom model
    - **Audit_Log_View_Filters:** Configurable date range, user, action
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-SYSADM-001
    - REQ-SYSADM-002
    - REQ-SYSADM-003
    - REQ-SYSADM-007
    - REQ-SYSADM-008
    - REQ-SYSADM-010
    - REQ-SYSADM-013
    - REQ-SYSADM-014
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - Super Administrator
      - National Administrator
      
    
    - **Id:** dfr-module-analytics-dashboards-006  
**Name:** DFR Analytics & Dashboards  
**Description:** Provides custom dashboards with KPIs, map-based visualizations for farmer/plot locations, custom QWeb reports for formatted output, and enhances data export capabilities for analytics.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-farmer-registry-002
    - dfr-module-dynamic-forms-003
    - Odoo Framework (Dashboard, Reporting, ORM, web_map OCA potentially)
    
**Properties:**
    
    - **Layer:** DFR Odoo Presentation Layer / DFR Odoo Application Services
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Dashboard Views
    - Odoo Report Actions (QWeb)
    - Odoo Map Views
    
**Technology:** Odoo 18 CE, Python, XML, JavaScript/OWL, QWeb  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Default_Kpis:** Total Farmers, Gender Disaggregation, Age Distribution
    - **Map_Provider_Integration:** Leaflet.js / OpenStreetMap (default), Google Maps (configurable if OCA module used)
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-003
    - REQ-7-004
    - REQ-7-005
    - REQ-7-006
    - REQ-7-007
    - REQ-7-008
    - REQ-SYSADM-011
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - National Administrator
      - Policy Maker/Analyst
      - Supervisor
      
    
    - **Id:** dfr-module-notifications-engine-007  
**Name:** DFR Notifications Engine  
**Description:** Manages automated notifications (SMS, email, mobile push). Includes logic for triggering notifications, managing multilingual templates, and UI for configuring third-party gateway credentials.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - dfr-module-external-connectors-009
    - Odoo Framework (ORM, mail, Automated Actions)
    
**Properties:**
    
    - **Layer:** DFR Odoo Application Services / DFR Integration Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Services for triggering notifications
    - Odoo Views for template and gateway configuration
    
**Technology:** Odoo 18 CE, Python, XML, QWeb (for email templates)  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Supported_Channels:** SMS, Email, Mobile Push (via FCM)
    - **Template_Placeholders_Guide:** Documented variables (farmer name, ID, etc.)
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-NS-001
    - REQ-NS-002
    - REQ-NS-003
    - REQ-NS-004
    - REQ-NS-005
    - REQ-NS-006
    - REQ-NS-007
    - REQ-NS-008
    - REQ-NS-009
    - REQ-NS-010
    - REQ-SYSADM-004
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - National Administrator (config)
      
    
    - **Id:** dfr-module-rest-api-008  
**Name:** DFR REST API Services  
**Description:** Provides secure RESTful API endpoints for mobile application data synchronization and external system integrations. Handles authentication (OAuth2/JWT) and complies with OpenAPI v3.x.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-farmer-registry-002
    - dfr-module-dynamic-forms-003
    - dfr-module-rbac-config-004
    - Odoo Framework (HTTP Controllers, OCA base_rest potentially)
    
**Properties:**
    
    - **Layer:** DFR API Gateway Layer (Odoo Module)
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - RESTful JSON API (OpenAPI v3.x documented)
    
**Technology:** Odoo 18 CE, Python, JSON  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Auth_Method:** OAuth2 / JWT
    - **Api_Version_Prefix:** /api/v1/dfr
    - **Rate_Limiting:** Configurable (e.g., Nginx level)
    
**Health Check:**
    
    - **Path:** /api/v1/dfr/health
    - **Interval:** 60
    - **Timeout:** 5
    
**Responsible Features:**
    
    - REQ-PCA-007
    - REQ-API-001
    - REQ-API-002
    - REQ-API-003
    - REQ-API-004
    - REQ-API-005
    - REQ-API-006
    - REQ-API-009
    - REQ-API-010
    - REQ-SADG-002
    - REQ-5-012
    - REQ-CM-007
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - Mobile App User
      - External System Integrator Role
      
    
    - **Id:** dfr-module-external-connectors-009  
**Name:** DFR External System Connectors  
**Description:** Contains client-side logic and adapters for connecting to various third-party systems like National ID validation services, SMS/Email gateways, and weather/advisory APIs.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - Odoo Framework
    
**Properties:**
    
    - **Layer:** DFR Integration Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Python Services for specific external system interactions
    
**Technology:** Odoo 18 CE, Python, Requests library, Specific SDKs  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **National_Id_Api_Url:** Configurable per country
    - **Sms_Gateway_Credentials:** Securely stored per country
    
**Health Check:**
    
    - **Path:** N/A (Health depends on external services)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-API-007
    - REQ-API-008
    - REQ-API-011
    - REQ-FHR-006
    - REQ-NS-004
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-module-data-management-tools-010  
**Name:** DFR Data Management Tools  
**Description:** Provides enhanced tools for bulk data import/export (CSV, XLSX) if Odoo's standard capabilities are insufficient, including complex data mapping, validation logic for migration, and reporting on import/export processes.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-farmer-registry-002
    - Odoo Framework (Import/Export tools, ORM)
    
**Properties:**
    
    - **Layer:** DFR Odoo Application Services / DFR Odoo Presentation Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Admin Views/Wizards for data operations
    - Odoo Services for custom import/export logic
    
**Technology:** Odoo 18 CE, Python, XML  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Import_Batch_Size:** Configurable
    - **Migration_Validation_Rules_Engine:** Custom Python logic or enhanced model constraints
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-DM-001
    - REQ-DM-002
    - REQ-DM-003
    - REQ-DM-004
    - REQ-DM-005
    - REQ-DM-006
    - REQ-DM-007
    - REQ-DM-008
    - REQ-DM-009
    - REQ-DM-010
    - REQ-DM-011
    - REQ-DM-012
    - REQ-SYSADM-012
    - REQ-TSE-001
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - National Administrator
      - IT Team (migration)
      
    
    - **Id:** dfr-module-farmer-portal-011  
**Name:** DFR Farmer Self-Service Portal  
**Description:** Extends Odoo's Website module to provide a public-facing portal for farmers. Includes pre-registration forms, informational content, display of selected dynamic forms, and country-specific branding. Ensures mobile responsiveness and accessibility (WCAG).  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-farmer-registry-002
    - dfr-module-dynamic-forms-003
    - Odoo Framework (website module)
    
**Properties:**
    
    - **Layer:** DFR Odoo Presentation Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Public Web Pages (HTML, QWeb)
    - Odoo Controllers for form submissions
    
**Technology:** Odoo 18 CE, Python, XML, QWeb, JavaScript, CSS  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    
**Configuration:**
    
    - **Portal_Enable_Toggle:** Per country instance
    - **Pre_Registration_Fields:** Configurable subset of farmer model
    - **Wcag_Compliance_Level:** 2.1 AA (target)
    
**Health Check:**
    
    - **Path:** N/A (Part of Odoo Website Health)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-005
    - REQ-FSSP-001
    - REQ-FSSP-002
    - REQ-FSSP-003
    - REQ-FSSP-004
    - REQ-FSSP-005
    - REQ-FSSP-006
    - REQ-FSSP-007
    - REQ-FSSP-008
    - REQ-FSSP-009
    - REQ-FSSP-010
    - REQ-FSSP-011
    - REQ-FSSP-012
    - REQ-FSSP-013
    - REQ-FHR-009
    - REQ-3-009
    - REQ-SYSADM-009
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    - **Allowed Roles:**
      
      - Public User (pre-registration)
      - Authenticated Farmer (view own data/specific forms)
      
    
    - **Id:** dfr-module-localization-pack-012  
**Name:** DFR Localization Pack  
**Description:** Manages DFR-specific localization assets, including .po files for all custom modules. Facilitates language switching and ensures correct display of localized content, date/time formats, and RTL scripts if required.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - All other DFR modules
    - Odoo Framework (i18n)
    
**Properties:**
    
    - **Layer:** DFR Cross-Cutting Concerns
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Odoo Translation mechanisms (.po files)
    
**Technology:** Odoo 18 CE, .po files  
**Resources:**
    
    - **Cpu:** N/A (Language assets)
    - **Memory:** N/A (Language assets)
    
**Configuration:**
    
    - **Supported_Languages:** Configurable per country instance
    - **Default_Language_Setting:** Per country instance
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-018
    - REQ-LMS-001
    - REQ-LMS-002
    - REQ-LMS-004
    - REQ-LMS-005
    - REQ-LMS-006
    - REQ-LMS-007
    - REQ-LMS-008
    - REQ-LMS-009
    - REQ-LMS-010
    - REQ-LMS-011
    - REQ-SYSADM-006
    - REQ-CM-008
    - REQ-TSE-004
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-module-security-audit-log-013  
**Name:** DFR Security & Audit Logging Extensions  
**Description:** Enhances Odoo's audit capabilities for DFR-specific needs. Implements detailed logging for critical events, manages consent tracking, enforces strong password policies, supports MFA recommendations, and handles data retention/archiving policies. Includes OWASP Top 10 mitigation adherence and SBOM management.  
**Type:** OdooModule  
**Dependencies:**
    
    - dfr-module-core-001
    - dfr-module-farmer-registry-002
    - Odoo Framework (mail.thread, Logging)
    
**Properties:**
    
    - **Layer:** DFR Security Layer / DFR Cross-Cutting Concerns
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Custom Logging services
    - Odoo Model extensions for chatter/tracking
    
**Technology:** Odoo 18 CE, Python  
**Resources:**
    
    - **Cpu:** Shared with Odoo App Server
    - **Memory:** Shared with Odoo App Server
    - **Storage:** PostgreSQL (audit log tables, mail messages)
    
**Configuration:**
    
    - **Password_Policy_Params:** Length, complexity, expiry (via Odoo settings)
    - **Data_Retention_Periods:** Configurable per entity type
    - **Pii_Encryption_Fields:** Configurable if pgcrypto used
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-SADG-003
    - REQ-SADG-005
    - REQ-SADG-006
    - REQ-SADG-007
    - REQ-SADG-008
    - REQ-SADG-009
    - REQ-SADG-010
    - REQ-SADG-012
    - REQ-PCA-014
    - REQ-CM-010
    - REQ-DIO-023
    - REQ-5-008
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - Super Administrator
      - National Administrator (audit view)
      
    
    - **Id:** dfr-mobile-app-presentation-014  
**Name:** Mobile App Presentation Layer  
**Description:** Handles the user interface and user experience for the Android enumerator mobile application. Renders screens for farmer registration, dynamic forms, search, data lists, and captures user input. Adheres to Material Design guidelines.  
**Type:** MobileComponent  
**Dependencies:**
    
    - dfr-mobile-app-business-logic-015
    
**Properties:**
    
    - **Layer:** Mobile Presentation (UI) Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - User Interface Screens and Navigation Flows
    
**Technology:** Android Native (Kotlin/Java + XML/Jetpack Compose) or Cross-platform (Flutter/Dart + Widgets)  
**Resources:**
    
    - **Cpu:** Device Dependant
    - **Memory:** Device Dependant
    - **Storage:** Device Dependant (UI assets)
    
**Configuration:**
    
    - **Theme_Support:** Light/Dark mode based on OS settings
    - **Accessibility_Features:** Font scaling, talkback support (platform provided)
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-4-002
    - REQ-4-009
    - REQ-4-010
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-mobile-app-business-logic-015  
**Name:** Mobile App Business Logic Layer  
**Description:** Manages application-specific logic, workflows, UI state, and business rules on the mobile device. Implements client-side validation, orchestrates offline data capture, and coordinates synchronization processes.  
**Type:** MobileComponent  
**Dependencies:**
    
    - dfr-mobile-app-data-sync-016
    - dfr-mobile-app-platform-services-018
    
**Properties:**
    
    - **Layer:** Mobile Application & Business Logic Layer
    - **Version:** 1.0.0
    - **Architecture_Pattern:** MVVM, MVI, or BLoC/Provider
    
**Interfaces:**
    
    - ViewModels / BLoCs / Controllers for UI interaction
    
**Technology:** Android Native (Kotlin/Java) or Cross-platform (Flutter/Dart)  
**Resources:**
    
    - **Cpu:** Device Dependant
    - **Memory:** Device Dependant
    
**Configuration:**
    
    - **Local_Deduplication_Rules:** Configurable (e.g., National ID on device)
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-4-003
    - REQ-4-008
    - REQ-4-012
    - REQ-4-016
    - REQ-4-014
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-mobile-app-data-sync-016  
**Name:** Mobile App Data Synchronization Service  
**Description:** Implements bi-directional data synchronization between the mobile app's local storage and the Odoo backend via REST APIs. Handles conflict resolution and ensures resilient network communication.  
**Type:** MobileComponent  
**Dependencies:**
    
    - dfr-mobile-app-local-data-store-017
    - dfr-module-rest-api-008 (Backend API)
    
**Properties:**
    
    - **Layer:** Mobile Data Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Service API for initiating sync, checking status
    
**Technology:** Android Native (Kotlin/Java with Retrofit/OkHttp) or Cross-platform (Flutter/Dart with Dio/http)  
**Resources:**
    
    - **Cpu:** Device Dependant (intensive during sync)
    - **Memory:** Device Dependant (intensive during sync)
    - **Network:** Required for operation
    
**Configuration:**
    
    - **Sync_Conflict_Resolution_Strategy:** Timestamp-based Last-Write-Wins or Server-Wins (configurable/defined)
    - **Sync_Chunk_Size:** Configurable for large datasets
    
**Health Check:**
    
    - **Path:** N/A (Reports sync status to UI/logs)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-006
    - REQ-4-006
    - REQ-4-007
    - REQ-4-014
    - REQ-4-015
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-mobile-app-local-data-store-017  
**Name:** Mobile App Local Data Store  
**Description:** Manages local data storage using an encrypted SQLite database. Stores farmer data, dynamic form definitions, and submissions offline. Provides Data Access Objects (DAOs) for data manipulation.  
**Type:** MobileComponent  
**Dependencies:**
    
    
**Properties:**
    
    - **Layer:** Mobile Data Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - DAOs for CRUD operations on local entities
    
**Technology:** SQLite with SQLCipher (AES-256 encryption), Room Persistence Library (Android) or sqflite/Moor/Drift (Flutter)  
**Resources:**
    
    - **Storage:** Device Dependant (up to 5000 farmer profiles target - REQ-4-005)
    
**Configuration:**
    
    - **Encryption_Key_Management:** Android Keystore System / flutter_secure_storage
    
**Health Check:**
    
    - **Path:** N/A (DB integrity checks on startup)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-4-003
    - REQ-4-004
    - REQ-4-005
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-mobile-app-platform-services-018  
**Name:** Mobile App Platform Services Wrapper  
**Description:** Provides abstracted access to native device capabilities like GPS, QR code scanning, camera, local logging, secure key management for encryption keys, and app update checks.  
**Type:** MobileComponent  
**Dependencies:**
    
    
**Properties:**
    
    - **Layer:** Mobile Cross-Cutting Services Layer
    - **Version:** 1.0.0
    
**Interfaces:**
    
    - Service APIs for GPS, QR Scanner, Logging, Secure Storage, App Update
    
**Technology:** Android Native APIs (LocationManager, CameraX/ZXing) or Flutter Plugins (geolocator, qr_code_scanner, logger, flutter_secure_storage)  
**Resources:**
    
    - **Sensors:** GPS, Camera
    
**Configuration:**
    
    - **Gps_Accuracy_Threshold:** Configurable (e.g., <10 meters)
    - **Log_Level:** Configurable (Debug, Info, Error)
    
**Health Check:**
    
    - **Path:** N/A
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-4-001
    - REQ-4-009
    - REQ-4-008
    - REQ-4-011
    - REQ-4-013
    - REQ-PCA-019
    - REQ-4-017
    - REQ-4-018
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-infra-odoo-app-container-019  
**Name:** Odoo Application Server Container  
**Description:** Docker container running the Odoo 18 CE application server with all DFR custom modules installed and configured. Handles web requests, executes business logic, and interacts with the database.  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    - dfr-infra-postgres-db-container-020
    - dfr-infra-reverse-proxy-021
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer
    - **Version:** Odoo 18.0 + DFR Modules vX.Y.Z
    
**Interfaces:**
    
    - HTTP/HTTPS (via reverse proxy)
    - Odoo RPC (internal)
    
**Technology:** Docker, Odoo 18 CE, Python 3.x  
**Resources:**
    
    - **Cpu:** Configurable (e.g., 2+ cores)
    - **Memory:** Configurable (e.g., 4GB+ RAM)
    - **Storage:** For Odoo filestore (attachments)
    
**Configuration:**
    
    - **Odoo_Conf_File:** Mounted or templated
    - **Workers:** Configurable number of Odoo worker processes
    - **Db_Host:** Link to PostgreSQL container
    
**Health Check:**
    
    - **Path:** Odoo's default health or custom endpoint
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-PCA-015
    - REQ-DIO-001
    - REQ-DIO-006
    - REQ-DIO-013
    - REQ-DIO-021
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-infra-postgres-db-container-020  
**Name:** PostgreSQL Database Container  
**Description:** Docker container running the PostgreSQL database management system, storing all DFR data for a specific country instance. Ensures data persistence and isolation.  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer
    - **Version:** PostgreSQL 15+ (aligned with Odoo 18 compatibility)
    
**Interfaces:**
    
    - SQL (via PostgreSQL protocol)
    
**Technology:** Docker, PostgreSQL  
**Resources:**
    
    - **Cpu:** Configurable (e.g., 2+ cores)
    - **Memory:** Configurable (e.g., 4GB+ RAM)
    - **Storage:** For database files, WALs (size depends on data volume)
    
**Configuration:**
    
    - **Postgresql_Conf_File:** Mounted or templated
    - **Pg_Hba_Conf_File:** To allow Odoo app server connection
    - **Max_Connections:** Configurable
    
**Health Check:**
    
    - **Path:** N/A (DB connection check from app server)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-001
    - REQ-PCA-010
    - REQ-PCA-015
    - REQ-DIO-001
    - REQ-DIO-006
    - REQ-DIO-013
    - REQ-DIO-021
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-infra-reverse-proxy-021  
**Name:** Web Reverse Proxy Server  
**Description:** Handles incoming HTTPS traffic, performs SSL/TLS termination, load balances requests to Odoo worker processes (if applicable), and can serve static content or implement rate limiting.  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    - dfr-infra-odoo-app-container-019
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer
    - **Version:** Nginx (latest stable) or Apache (latest stable)
    
**Interfaces:**
    
    - HTTPS (port 443)
    
**Technology:** Nginx or Apache  
**Resources:**
    
    - **Cpu:** Configurable (e.g., 1+ core)
    - **Memory:** Configurable (e.g., 1GB+ RAM)
    
**Configuration:**
    
    - **Ssl_Certificate_Path:** Path to SSL certs
    - **Load_Balancing_Strategy:** Round-robin, least connections
    - **Timeout_Settings:** Proxy timeouts
    
**Health Check:**
    
    - **Path:** N/A (Monitors backend Odoo server health)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-DIO-005
    - REQ-PCA-014
    
**Security:**
    
    - **Requires Authentication:** False
    - **Requires Authorization:** False
    
    - **Id:** dfr-ops-ci-cd-pipeline-022  
**Name:** CI/CD Pipeline System  
**Description:** Automates the building, testing (unit, integration), and deployment of the DFR core platform (Odoo modules and mobile app) to various environments (Dev, Staging, Prod).  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    - Git Version Control System
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer / DevOps
    - **Version:** Jenkins, GitLab CI, or GitHub Actions (as chosen)
    
**Interfaces:**
    
    - Web UI for pipeline management
    - API for programmatic triggers
    
**Technology:** Jenkins/GitLab CI/GitHub Actions, Docker, Shell scripts, Python scripts  
**Resources:**
    
    - **Cpu:** Depends on CI/CD server load
    - **Memory:** Depends on CI/CD server load
    - **Storage:** For build artifacts, logs
    
**Configuration:**
    
    - **Pipeline_Definition_Files:** Jenkinsfile, .gitlab-ci.yml, or GitHub Actions workflow YAMLs
    - **Environment_Specific_Deploy_Configs:** Managed per environment branch/tag
    
**Health Check:**
    
    - **Path:** N/A (Pipeline success/failure status)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - REQ-DIO-017
    - REQ-CM-002
    - REQ-CM-014
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-ops-backup-restore-023  
**Name:** Data Backup & Restore Utility  
**Description:** Automated system for daily backups of PostgreSQL databases and critical system files (Odoo custom modules, configurations, filestore). Includes documented procedures for data restoration to meet RTO/RPO targets.  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    - dfr-infra-postgres-db-container-020
    - dfr-infra-odoo-app-container-019
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer / Operations
    - **Version:** Custom scripts utilizing pg_dump/pg_basebackup, rsync
    
**Interfaces:**
    
    - Command-line interface for manual execution/monitoring
    - Scheduled cron jobs
    
**Technology:** Shell scripts, Python scripts, pg_dump/pg_basebackup, rsync, cron  
**Resources:**
    
    - **Storage:** For backup files (local and offsite/cloud)
    
**Configuration:**
    
    - **Backup_Schedule:** Daily
    - **Retention_Policy:** Daily for 7 days, weekly for 4 weeks, etc. (REQ-DIO-008)
    - **Backup_Destination:** Local path, S3 bucket, etc.
    
**Health Check:**
    
    - **Path:** N/A (Backup success/failure logs)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-PCA-012
    - REQ-SADG-011
    - REQ-DIO-007
    - REQ-DIO-008
    - REQ-DIO-010
    - REQ-DIO-015
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-ops-monitoring-alerting-024  
**Name:** System Monitoring & Alerting Dashboard  
**Description:** Tracks key performance indicators (KPIs) for Odoo application, PostgreSQL database, and server infrastructure. Provides configurable alert thresholds and notification channels for administrators.  
**Type:** InfrastructureComponent  
**Dependencies:**
    
    - dfr-infra-odoo-app-container-019
    - dfr-infra-postgres-db-container-020
    - dfr-infra-reverse-proxy-021
    
**Properties:**
    
    - **Layer:** DFR Infrastructure Layer / Operations
    - **Version:** Prometheus/Grafana, Zabbix, or Cloud Provider Tools (as chosen)
    
**Interfaces:**
    
    - Web UI Dashboard
    - Alerting notification channels (Email, SMS via gateway)
    
**Technology:** Prometheus, Grafana, Zabbix, CloudWatch, Azure Monitor, etc.  
**Resources:**
    
    - **Cpu:** Depends on monitoring server load
    - **Memory:** Depends on monitoring server load
    - **Storage:** For metrics data
    
**Configuration:**
    
    - **Monitored_Metrics_List:** CPU, RAM, Disk I/O, Network, DB connections, Odoo worker status, HTTP error rates
    - **Alert_Thresholds_Config:** Definable for critical/warning events
    
**Health Check:**
    
    - **Path:** Monitoring system's own health endpoint
    - **Interval:** 300
    - **Timeout:** 30
    
**Responsible Features:**
    
    - REQ-PCA-012
    - REQ-DIO-009
    - REQ-CM-011
    - REQ-TSE-008
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    
    - **Id:** dfr-docs-platform-025  
**Name:** DFR Documentation Platform  
**Description:** A centralized, searchable documentation wiki or portal hosting user manuals, guides, FAQs, training materials, and technical documentation. Provides version control for content and accessibility to authorized users.  
**Type:** SoftwareComponent  
**Dependencies:**
    
    
**Properties:**
    
    - **Layer:** N/A (Supporting Asset)
    - **Version:** Chosen Wiki/Portal software (e.g., Confluence, ReadtheDocs, MkDocs, Docusaurus) or Static Site Generator
    
**Interfaces:**
    
    - Web UI for browsing and searching documentation
    
**Technology:** Wiki Software, Static Site Generator, or Hosted Service  
**Resources:**
    
    - **Cpu:** Depends on platform choice
    - **Memory:** Depends on platform choice
    - **Storage:** For documentation content
    
**Configuration:**
    
    - **Search_Engine_Integration:** Enabled
    - **Access_Control_Rules:** Public, Authenticated Users (role-based if platform supports)
    
**Health Check:**
    
    - **Path:** Platform's own health endpoint or availability check
    - **Interval:** 300
    - **Timeout:** 30
    
**Responsible Features:**
    
    - REQ-CM-008
    - REQ-CM-009
    - REQ-CM-015
    - REQ-TSE-001
    - REQ-TSE-002
    - REQ-TSE-003
    - REQ-TSE-004
    - REQ-TSE-005
    - REQ-TSE-006
    - REQ-TSE-007
    - REQ-TSE-009
    - REQ-TSE-010
    - REQ-TSE-011
    - REQ-TSE-012
    - REQ-TSE-013
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** True
    - **Allowed Roles:**
      
      - All DFR Users (role-specific content access)
      
    
    
  - **Configuration:**
    
    - **Platform_Name:** Digital Farmer Registry (DFR)
    - **Core_Technology_Backend:** Odoo 18.0 Community Edition
    - **Core_Technology_Database:** PostgreSQL (version compatible with Odoo 18)
    - **Core_Technology_Mobile:** Android (Native Kotlin/Java or Cross-platform Flutter/Dart)
    - **Default_Code_License:** MIT or Apache 2.0
    - **Version_Control_System:** Git (GitHub/GitLab)
    - **Semantic_Versioning_Standard:** Semantic Versioning 2.0.0
    - **Ci_Cd_Tool_Preference:** Jenkins, GitLab CI, or GitHub Actions
    - **Security_Standard_Web:** OWASP Top 10
    - **Security_Standard_Mobile:** OWASP MASVS
    - **Api_Documentation_Standard:** OpenAPI Specification v3.x
    - **Deployment_Environments:**
      
      - Development
      - Staging
      - Production
      
    - **Containerization_Technology:** Docker
    - **Data_Transmission_Encryption:** HTTPS/TLS 1.2+
    - **Backup_Frequency:** Daily
    - **Supported_Hosting_Environments:**
      
      - Government Data Centers (Linux)
      - Approved Cloud Providers (AWS, Azure, GCP)
      - Hybrid
      
    
  


---

