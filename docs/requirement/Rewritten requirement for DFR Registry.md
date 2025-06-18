**Software Requirements Specification: Digital Farmer Registry (DFR)**

**Version:** 1.0
**Date:** October 26, 2023

**1. Introduction**

    **1.1. Purpose**
        This document specifies the requirements for the Digital Farmer Registry (DFR) system. The DFR will serve as a foundational dataset to streamline service delivery, improve beneficiary targeting, enable data-driven decision-making, and enhance accountability across agriculture-related programs in the Cook Islands, Samoa, Solomon Islands, Tonga, and Vanuatu. It aims to provide a single source of truth for farmer data, enabling integration with various e-services, aligning with Digital Public Infrastructure (DPI) principles.

    **1.2. Scope**
        The scope of this project includes the architecture, design, development, deployment, data migration, training, cutover, capacity building, and support of a unified, modular, and reusable DFR platform. This core platform will be replicated, configured, and deployed across five Project Targeted Pacific Island Countries: Cook Islands (CKI), Samoa, Tonga, Solomon Islands, and Vanuatu. Each instance will have localized settings, administrative roles, language packs, and hosting environments, while being based on a shared core codebase. The system will include web and mobile interfaces, a dynamic form engine, integration APIs, and robust data management capabilities. The technology stack is ODOO 18.0 community edition addon. [Specifying the exact Odoo version (18.0) is critical for development and dependency management.] The backend will primarily use Python with the Odoo framework, and PostgreSQL as the database. [Explicitly stating core Odoo technologies provides immediate clarity.]

    **1.3. Definitions, Acronyms, and Abbreviations**
        *   API: Application Programming Interface
        *   AES: Advanced Encryption Standard [Added for clarity as AES-256 is referenced later]
        *   CKI: Cook Islands
        *   CI/CD: Continuous Integration/Continuous Deployment
        *   CRUD: Create, Read, Update, Delete
        *   CSV: Comma-Separated Values
        *   DAST: Dynamic Application Security Testing
        *   DFR: Digital Farmer Registry
        *   DPI: Digital Public Infrastructure
        *   DR: Disaster Recovery
        *   ETL: Extract, Transform, Load (for data migration)
        *   FAO: Food and Agriculture Organization of the United Nations
        *   GPS: Global Positioning System
        *   JSON: JavaScript Object Notation
        *   JWT: JSON Web Token
        *   KPI: Key Performance Indicator
        *   KYC: Know Your Customer
        *   LMS: Learning Management System
        *   MDM: Mobile Device Management
        *   MFA: Multi-Factor Authentication [Added as it's a security best practice likely to be implemented]
        *   ORM: Object-Relational Mapping
        *   OWASP: Open Web Application Security Project
        *   PII: Personally Identifiable Information
        *   PITR: Point-In-Time Recovery
        *   PWA: Progressive Web Application
        *   QR Code: Quick Response Code
        *   RBAC: Role-Based Access Control
        *   REST: Representational State Transfer
        *   RPO: Recovery Point Objective
        *   RTO: Recovery Time Objective
        *   SAST: Static Application Security Testing
        *   SBOM: Software Bill of Materials [Added as it's referenced in security requirements]
        *   SDK: Software Development Kit
        *   SLA: Service Level Agreement
        *   SMS: Short Message Service
        *   SOP: Standard Operating Procedure
        *   SPOF: Single Point of Failure
        *   SRS: Software Requirements Specification
        *   SSL: Secure Sockets Layer (often used interchangeably with TLS)
        *   TLS: Transport Layer Security [Added as it's the modern standard replacing SSL]
        *   ToT: Training-of-Trainers
        *   UI: User Interface
        *   UID: Unique Identifier
        *   UAT: User Acceptance Testing
        *   UX: User Experience
        *   WCAG: Web Content Accessibility Guidelines
        *   WP: Work Package
        *   XLSX: XML Spreadsheet (Office Open XML Workbook)
        *   XML-RPC: Extensible Markup Language Remote Procedure Call

    **1.4. References**
        *   User Requirements Document (provided by user)
        *   Gap Analysis Document (provided by user)
        *   MIT License
        *   Apache 2.0 License
        *   OpenAPI Specification (Version 3.x recommended) [Specifying version ensures modern practices]
        *   Swagger (Tools for implementing OpenAPI Specification)
        *   WCAG Guidelines (Version 2.1 or higher, Level AA)
        *   OAuth2 Authorization Framework (RFC 6749)
        *   JWT Standard (RFC 7519)
        *   AES-256 Encryption Standard (FIPS 197)
        *   Odoo 18.0 Community Edition Documentation [Essential reference for the core technology]
        *   PostgreSQL Documentation [Essential for database management and optimization]
        *   PEP 8 -- Style Guide for Python Code [Essential for Python development consistency]
        *   OWASP Top 10 Web Application Security Risks
        *   OWASP Mobile Application Security Verification Standard (MASVS)
        *   [Placeholder for specific Data Privacy Regulations for CKI, Samoa, Solomon Islands, Tonga, Vanuatu once identified]
        *   [Placeholder for specific National IT and Data Governance Policies for CKI, Samoa, Solomon Islands, Tonga, Vanuatu once identified]

    **1.5. Overview**
        This SRS is organized into sections covering the overall description of the DFR, specific functional and non-functional requirements, interface requirements, data requirements, and transition requirements. The requirements are derived from the user-provided documents, with gaps identified in the "Gap Analysis" document addressed and integrated herein. The document details the work packages: Platform Architecture & Governance Foundation (WP-A), Platform Design, Development & Deployment (WP-B), Capacity Building, Training & Change Management (WP-C), Post-Deployment Support, Maintenance & Handover (WP-D), and Codebase Ownership Transfer & Exit Readiness (WP-E).

**2. Overall Description**

    **2.1. Product Perspective**
        The DFR will be an ODOO 18.0 community addon-based system, leveraging its Python backend and PostgreSQL database. It is a new, self-contained product designed as a unified, modular, and reusable digital platform. It will be deployed as five independent but centrally maintained instances for CKI, Samoa, Tonga, Solomon Islands, and Vanuatu. The system is intended to be a core component of the agricultural digital ecosystem in these countries, aligning with DPI principles. It may replace or integrate with existing farmer data systems, as detailed in the transition requirements.

    **2.2. Product Functions (Summary)**
        The DFR platform will provide the following key functionalities:
        *   Establishment of a shared, modular platform architecture and governance using Odoo's inherent modularity.
        *   Core farmer and household registration and management using custom Odoo models.
        *   Dynamic data collection through a configurable form builder, developed as an Odoo module.
        *   Offline-first mobile data collection for enumerators (Android application).
        *   Role-based access control and administration tools leveraging Odoo's security framework.
        *   Dashboards, analytics, and reporting using Odoo's reporting engine and views.
        *   Notification system (SMS, email, push) integrated with Odoo's communication tools.
        *   Secure RESTful APIs for integration, built as a custom Odoo module.
        *   Data import/export capabilities using Odoo's standard tools, potentially extended, including comprehensive data migration from legacy systems.
        *   A public-facing farmer self-service portal using Odoo's Website/Portal module.
        *   Comprehensive localization and multilingual support via Odoo's translation mechanisms.
        *   Robust data security, audit logging, and change history leveraging Odoo features and custom extensions.
        *   Capacity building and training programs.
        *   Long-term support, maintenance, and knowledge transfer.
        *   Full codebase ownership transfer to participating countries.

    **2.3. User Characteristics**
        The primary users of the DFR system include:
        *   **Farmers:** For self-registration (via portal) and receiving information.
        *   **Enumerators:** For registering farmers, collecting data offline and online using mobile devices.
        *   **Supervisors:** For overseeing enumerator activities, data validation, and management.
        *   **National Administrators:** For managing users, configuring country-specific settings (including business rules for workflows, de-duplication, and notifications), designing dynamic forms, managing notifications, accessing analytics, overseeing data migration validation, and overall system administration at the country level within the Odoo backend.
        *   **Super Administrators (FAO/Central):** For platform-level oversight, core Odoo codebase maintenance, and managing super admin functions.
        *   **Support Teams (National & Central):** For providing technical assistance and troubleshooting.
        *   **IT Teams (National & FAO):** For system maintenance, deployment, Odoo updates, data migration execution, and future development.
        *   **Policy Makers/Analysts:** For accessing aggregated data and analytics for decision-making.

    **2.4. Constraints**
        *   The system must be developed as an ODOO 18.0 community addon. [Reiterating specific version for clarity]
        *   The development timeframe is 14 weeks from project kick-off for Work Packages A and B, contingent upon the timely provision of critical dependencies as outlined in section 2.5, particularly data volume estimates and finalized core data schema.
        *   The solution must be a unified, modular, and reusable digital platform, not five separate systems, leveraging a shared Odoo codebase with country-specific configurations and modules.
        *   The codebase must be open-source under MIT or Apache 2.0 license.
        *   The system must adhere to DPI principles (openness, reusability, inclusion, sovereign ownership).
        *   Training delivery will be remote-first.
        *   Post-deployment support will be for 24 months under an SLA.
        *   Specific data privacy regulations applicable in each of the five countries (to be identified and documented as per section 1.4) must be adhered to, with system features designed to support compliance.
        *   The system must support deployment in diverse environments: government data centers, government-approved cloud services (e.g., AWS, Azure, GCP, or local equivalents), or hybrid architectures. [Adding examples of cloud services for clarity]
        *   The mobile application must target Android devices. [Clarifying the mobile OS constraint]
        *   All business rules, including workflows, validation logic, and decision points, must be configurable within the Odoo system by authorized National Administrators where feasible, or clearly documented if hard-coded.

    **2.5. Assumptions and Dependencies**
        *   FAO and national counterparts will provide:
            *   Final common data schema for the core registry, including a preliminary list of core common data fields (e.g., Farmer Unique ID, Full Name, Date of Birth, Sex, National ID (type & number), Contact Number, Village, Administrative Unit Levels, Household ID, Household Head, Number of Household Members, Plot ID, Plot Size, Plot Location Coordinates (type: GPS point/polygon), Land Ownership Type) as a top priority. The process for finalizing the complete common data schema, including data types and validation rules for each field, is a critical path item. [Adding detail on schema finalization importance]
            *   Estimates for current and projected (5-10 years) data volumes (farmers, households, plots, dynamic form submissions) per country. The provision of these estimates by [Specify Deadline, e.g., end of Week 2 of project kick-off] is a critical path item for the completion of Work Package A. Delays or significant inaccuracies in these estimates may impact the 14-week timeline for Work Packages A and B or necessitate adjustments to the system's long-term scalability design (e.g., database indexing strategies, hardware provisioning), potentially requiring future rework. If estimates are significantly delayed, baseline assumptions (e.g., 1 million farmers per large country, 100,000 per small country, average 2 plots per farmer, 10 dynamic form submissions per farmer over 5 years) will be used, with the understanding that re-scoping or re-phasing may be required if actuals differ significantly. [Adding example baseline assumptions if estimates are delayed is crucial for planning]
            *   Localization inputs (language files in .po format for Odoo, and equivalent for mobile app; form field translations).
            *   Credentials for third-party API testing (e.g., SMS gateways, National ID validation sandbox environments where integration is expected).
            *   Specific external system details and API documentation (OpenAPI specs preferred) for planned integrations.
            *   Identification and documentation of key data protection and privacy laws for each target country, including consent management requirements, data subject rights procedures, and data breach notification protocols.
            *   Nomination of ToT participants and facilitation of their access to training sessions.
            *   Approval of patch releases for deployment to staging and production environments.
            *   Availability of detailed information on any existing farmer registration systems (digital, paper-based, or spreadsheet-based) in each country, including data schemas, data volume, quality assessments, and access methods, for planning data migration.
            *   Clear definition of roles and responsibilities for data migration activities (extraction, cleansing, validation, sign-off) between FAO, national counterparts, and the contractor.
            *   Defined business rules for farmer/household status transitions, de-duplication logic, and notification triggers, or commitment to define these during the design phase.
            *   Relevant national IT and data governance policies that the DFR system must comply with.
        *   Core farmer registration must be completed before applying dynamic forms.
        *   Internet connectivity may be limited or intermittent in some areas, necessitating robust offline capabilities for the mobile app.
        *   Participating countries have agreed on core common data points, with allowances for country-specific variations managed through Odoo configurations or separate, additive modules.

**3. Specific Requirements**

    **3.1. Work Package A: Platform Architecture & Governance Foundation**

        **A.1. Objective:** To establish the overarching architectural blueprint and governance principles for the DFR platform, enabling sustainable, scalable, and interoperable deployments across Project Targeted Pacific Island Countries. This work package lays the technical and institutional foundation for all subsequent work by defining a shared, modular, and open-source architecture based on Odoo 18.0 Community Edition, ensuring reusability, localization, and sovereign ownership in alignment with DPI standards.

        **A.2. Scope of Work**

            **A.2.1. System Architecture Blueprint**
                *   Develop a shared, modular platform architecture based on ODOO 18.0 community addon, utilizing:
                    *   Odoo's inherent modular monolith pattern. [Odoo is primarily a modular monolith; microservices would be a significant deviation and likely out of scope/budget for an Odoo addon project].
                    *   Clear separation of core functionality (shared Odoo modules in the core codebase) and country-level configuration/extensions (country-specific Odoo modules or configurations).
                    *   Design for scalability to accommodate future services (e.g., subsidy targeting, e-advisory) and increasing data volumes, leveraging PostgreSQL optimization techniques and Odoo worker configuration.
                *   The architecture must support:
                    *   Web interfaces (Admin Portal using Odoo Web Client - JavaScript/XML/OWL, Farmer Self-Service Portal using Odoo Website/Portal module).
                    *   A native Android mobile enumerator application (developed in Kotlin or Java) or a cross-platform mobile application (e.g., Flutter with Dart, preferred for performance and UI consistency over this type of data collection app). [Specifying Kotlin/Java for native Android or recommending Flutter for cross-platform provides clearer direction].
                    *   Offline-first mobile operations with robust bi-directional synchronization (e.g., using a queue-based system with background services) and conflict resolution strategies (e.g., last-write-wins, or flagging for manual review in Odoo backend).
                    *   A secure RESTful API layer built as a custom Odoo module (potentially leveraging OCA modules like `base_rest` and `base_rest_auth_api_key` or `auth_oauth` for OAuth2/JWT authentication). [Suggesting specific OCA modules can accelerate development and ensure standardization].
                    *   Multi-language UI (Odoo .po files, Android string resources) and dynamic forms.
                    *   Granular role-based access control (RBAC) using Odoo's `ir.model.access.csv` and security groups.
                    *   Comprehensive audit logging using Odoo's existing mechanisms (`mail.thread` for chatter/history) extended for specific auditable events.

            **A.2.2. Codebase Governance & Reusability**
                *   Define a structure for a shared core Odoo codebase:
                    *   Maintained centrally (e.g., by FAO or a designated central team) with a clear governance model for its evolution. This model will define:
                        *   The process for participating countries to contribute proposals or request changes (e.g., feature requests, bug reports via an issue tracker like JIRA, Trello, or GitHub Issues) to the central core codebase. [Specifying issue tracking tools helps operationalize this].
                        *   A policy outlining how updates and new versions of the central core are reviewed (e.g., peer review, QA testing), approved, and applied to country instances, ensuring stability and compatibility.
                        *   The extent to which a country can implement specific modifications. Country-specific needs will primarily be met through configurations and custom/additive Odoo modules that do not alter the core modules themselves. This approach ensures countries can benefit from central maintenance, support, and shared platform advancements.
                        *   If a country chooses to fork and extensively modify core modules beyond the agreed governance, they acknowledge responsibility for independently managing those modifications, including merging future updates from the central core or diverging, which may impact their ability to leverage shared platform benefits and central support for those modified components.
                    *   The core codebase will be source-controlled using Git (e.g., GitHub or GitLab, with a preference for a platform that supports robust CI/CD and issue tracking). [Adding preference rationale].
                    *   Tagged and versioned (Semantic Versioning 2.0.0) with a clear release history and changelog. [Specifying SemVer for clarity].
                *   Country-level forks, clones, or deployment configurations must support:
                    *   Independent deployment and operation of their Odoo instance.
                    *   Localized content (language packs as .po files, form translations) and specific configurations (Odoo `ir.config_parameter` or custom models for settings).
                    *   Complete isolation of data (separate PostgreSQL databases per country instance) and administrative controls per country instance.
                *   The entire codebase to be licensed under MIT or Apache 2.0.

            **A.2.3. DPI Compliance & Interoperability Readiness**
                *   Ensure the architecture and design adhere to DPI principles (openness, reusability, inclusion, data sovereignty).
                *   Ensure readiness for integration with external systems through the defined RESTful API layer. This includes potential integrations with:
                    *   National ID validation systems.
                    *   Weather and advisory service APIs.
                    *   Distribution, subsidy, or payment platforms.
                    *   For each planned integration, specific external system details, API documentation (endpoints, authentication methods like OAuth2/API Keys, request/response schemas, rate limits) will be identified in collaboration with FAO and national counterparts.

            **A.2.4. Hosting & Deployment Governance**
                *   Define hosting options suitable for each country's context and preferences:
                    *   Government-managed data center (requiring clear hardware/OS specifications).
                    *   Government-approved cloud service provider (e.g., AWS, Azure, GCP, or local providers; specifying services like EC2/VMs for Odoo, RDS/Managed PostgreSQL for database, S3/Blob storage for backups). [Adding specific cloud service examples].
                    *   Hybrid architecture (e.g., edge devices/offline capabilities with cloud synchronization).
                *   Specify:
                    *   Access control layers, including separation of duties for admin/super admin roles (leveraging Odoo roles and potentially infrastructure-level access controls).
                    *   Comprehensive backup (e.g., daily PostgreSQL dumps using `pg_dump` or continuous archiving with `pg_basebackup` and WAL archiving), rollback, and system monitoring protocols (e.g., using Prometheus, Grafana, Zabbix, or cloud provider tools).
                    *   A detailed Disaster Recovery (DR) plan, including explicit Recovery Time Objective (RTO) and Recovery Point Objective (RPO) targets for each country's DFR instance. This plan should include procedures for restoring PostgreSQL databases and Odoo application servers. [Adding detail on PostgreSQL DR].
                    *   A clear model for localization (Odoo .po files) and deployment configuration (environment variables, Odoo configuration files) for each country instance.
                    *   Strategy for mobile app distribution, prioritizing Mobile Device Management (MDM) or a private app store (e.g., Google Play Private Channel) to ensure robust management of updates, especially with data schema changes for offline-first devices. If manual APK distribution is deemed unavoidable for specific contexts, the following safeguards must be implemented:
                        *   The system must include mechanisms for prompting or enforcing app updates on enumerator devices if a version mismatch with schema implications is detected (e.g., app checks version against server API on sync).
                        *   The backend system (Odoo API) should have the capability to refuse synchronization attempts from critically outdated app versions that could lead to data integrity issues.
                        *   Clear communication protocols and procedures must be established for update rollouts, particularly when schema changes are involved.
                        *   The mobile application should incorporate a pre-synchronization check to detect critical schema incompatibilities with the server and prevent data entry or guide the user to update, minimizing data loss or corruption risks.
                        *   A defined support window for older app versions following a schema update will be established, after which outdated versions may lose sync capability.
                    This strategy includes management of updates with data schema changes for offline-first devices.

            **A.2.5. Compliance & Documentation Principles**
                *   Define standards for:
                    *   Code commenting (inline using Python docstrings, XML comments) and documentation (module-level READMEs in Markdown format).
                    *   API documentation using OpenAPI Specification v3.x / Swagger, ideally auto-generated from the RESTful API layer code or annotations. [Specifying OpenAPI version].
                    *   DevOps workflow, including CI/CD pipeline logic (e.g., using Jenkins, GitLab CI, GitHub Actions) for automated testing (unit, integration) and deployment to staging/production environments. [Adding examples of CI/CD tools].
                    *   Semantic versioning (Major.Minor.Patch) for all releases of the core platform and mobile app.
                    *   Validation procedures for new releases and patches (e.g., UAT by national teams on staging environment).
                    *   Licensing and IP governance documentation.

        **A.3. Deliverables (for WP-A)**
            *   A3.1. Technical Architecture Blueprint for the core Odoo platform (including key modules, data models, and interaction diagrams) and country-level extension/configuration strategy.
            *   A3.2. Codebase governance framework (structure, branching strategy e.g., GitFlow, maintenance plan, contribution model via issue tracker and pull requests).
            *   A3.3. DPI compliance checklist and architectural alignment matrix.
            *   A3.4. Hosting and deployment strategy guide, including DR plan with RTO/RPO targets, PostgreSQL backup/restore procedures, and mobile app distribution strategy.
            *   A3.5. Documentation standards guide (code comments, developer guides using tools like Sphinx for Python/Odoo, API documentation standards, versioning policy).
            *   A3.6. Licensing & Open-Source Use Declaration (confirming MIT / Apache 2.0 and listing any third-party open-source libraries used and their licenses).

        **A.4. Acceptance Criteria (for WP-A)**
            *   Architecture design, including Odoo module structure and mobile app interaction, reviewed and approved by FAO.
            *   DPI-aligned structure and principles are demonstrably established in the architecture.
            *   Deployment options per country are feasible, documented, reflect country preferences, and include specific considerations for Odoo and PostgreSQL hosting.
            *   An open-source repository (e.g., GitHub/GitLab) is initialized with the basic Odoo module structure and CI/CD pipeline configuration.
            *   WCAG 2.1 AA compliance considerations and security best practices (OWASP Top 10 for web, mobile specific OWASP guidelines) are validated in the architectural design.

    **3.2. Work Package B: Platform Design, Development & Deployment**

        **B.1. Objective:** To design, develop, and deliver a robust, secure, and scalable DFR platform, built on the shared Odoo 18.0 Community Edition core codebase. The platform must support standardized farmer registration, country-specific dynamic data collection, web and offline mobile interfaces, a dynamic form engine, integration APIs, and localization features, fully aligned with DPI principles. This includes managing the transition from any existing systems through effective data migration and deployment strategies.

        **B.2. Scope of Work**

            **B.2.1. Core Functional Engines (Odoo Modules)**

                **1. Farmer Registry Engine (Fixed Core Odoo Module)**
                    *   A standardized, production-ready Odoo module (e.g., `dfr_farmer_registry`) to register and manage farmers and their households using the common data model (Odoo models defined in Python) agreed across all participating countries.
                    *   Key features:
                        *   Generation of unique farmer and household IDs (UIDs) using Odoo sequences or UUIDs, ensuring uniqueness across the system. [Specifying UID generation methods].
                        *   Farmer profiles: full name, date of birth, sex, role in household, education level, contact information (phone, email if available) - all as fields in Odoo models.
                        *   Household member profiles: relationship to head, sex, age, role, education - managed via Odoo one2many/many2many relations.
                        *   Farm and plot details: size, land tenure/type, primary crop/livestock, location (administrative tagging, GPS coordinates as float fields or using PostGIS types if advanced spatial queries are needed), ownership details. [Mentioning PostGIS for advanced geo-capabilities].
                        *   National ID input (type and number) and optional KYC logic (manual verification workflow within Odoo or API-based if available).
                        *   Geo-location capture (GPS coordinates for plots/homestead) and administrative area tagging (e.g., region, district, village - potentially using hierarchical Odoo models for administrative units).
                        *   Role-based view and edit permissions for farmer data using Odoo's access rights (`ir.model.access.csv` and record rules).
                        *   Integration points with the Farmer Self-Service Portal for pre-registrations (e.g., creating draft farmer records in Odoo).
                        *   Comprehensive audit trail for all profile edits, status changes, and verification steps using Odoo's `mail.thread` (chatter) and custom logging if needed.
                        *   Definition of farmer/household statuses (e.g., 'Pending Verification', 'Active', 'Inactive', 'Deceased', 'Duplicate', 'Archived' - using an Odoo selection field) and workflows (Odoo automated actions or server actions) for status changes, specifying impact on system behavior (e.g., eligibility, analytics). Specific business rules defining the triggers, conditions, and automated/manual actions for transitioning between these statuses (e.g., criteria for moving from 'Pending Verification' to 'Active', or flagging as 'Duplicate') will be documented and configured in Odoo.
                        *   A de-duplication strategy including:
                            *   De-duplication checks performed in real-time during online data entry (e.g., via Admin Portal, connected Farmer Self-Service Portal) based on key identifiers (e.g., National ID, or combination of full name, DOB, village) using Odoo model constraints or custom onchange methods.
                            *   For data captured offline via the mobile app, de-duplication checks against the central registry will be performed upon synchronization. The mobile app may perform local de-duplication checks against its own offline dataset (SQLite database) to prevent obvious duplicates on the device, but comprehensive de-duplication occurs post-sync.
                            *   Configurable fuzzy matching logic (e.g., using Python libraries like FuzzyWuzzy or Levenshtein distance, integrated into Odoo) to identify potential duplicates. The specific parameters for fuzzy matching logic and the definitive rules for data retention/merging during the de-duplication workflow in Odoo will be configurable and finalized in consultation with national administrators.
                            *   An enhanced administrative workflow in Odoo for reviewing, comparing, and merging potential duplicate records, including those flagged post-synchronization from offline devices. This workflow will have clear rules for data retention from merged records.

                **2. Dynamic Data Configuration Engine (Custom Form Builder Odoo Module)**
                    *   A user-friendly tool within Odoo (e.g., a new Odoo module `dfr_dynamic_forms`), designed to be as 'no-code/low-code' as feasible within the Odoo 18.0 Community Edition addon framework, enabling authorized country-level administrators to design, publish, and manage custom data collection forms linked to existing farmer profiles. While aiming for intuitive graphical interfaces for form creation (similar to Odoo Studio but potentially simpler or more focused) and standard field types, the implementation of complex input validation rules (e.g., regex patterns via Odoo model constraints or Python code) and conditional logic (show/hide fields based on other field values using Odoo's `attrs` attribute in views or custom JavaScript) may involve a 'low-code' approach. This could include administrators using a simplified interface to select from predefined validation rules and construct conditional logic via a guided rule builder that translates to Odoo domain syntax or view attributes, rather than requiring them to write raw Odoo domains or Python code. Achieving a purely graphical 'no-code' experience for the most advanced conditional logic and regex patterns is acknowledged as a significant custom development effort; the solution will prioritize usability for common scenarios while providing robust capabilities. Exploration of suitable OCA (Odoo Community Association) modules (e.g., `survey` for form rendering, or parts of `formio` if adaptable) that might provide a foundation will be considered, understanding they may also have limitations or require customization. [Adding specific Odoo technical approaches and acknowledging complexity].
                    *   Features:
                        *   Intuitive interface in Odoo for creating forms with various field types (text, number, date, dropdown/selection, multi-select/many2many_tags, GPS, image/binary, etc.).
                        *   Support for input validation rules (required, min/max length, numeric range, regex patterns - implemented via Odoo model constraints or custom Python/JS) and conditional logic (show/hide fields based on other field values - using Odoo view `attrs` or custom JS).
                        *   Form versioning (e.g., by creating new form definitions and linking submissions to a specific version) to manage changes over time and preserve data integrity for submissions made on older versions.
                        *   Ability to tag forms (e.g., \"Cyclone Damage Assessment 2025\", \"Subsidy Application\" - using Odoo `mail.activity.type` or a custom tagging model).
                        *   Country-specific metadata and language support for form fields and instructions (using Odoo's translatable fields).
                        *   Form definitions (e.g., as JSON schema or structured Odoo models) to be synced to and rendered on the mobile enumerator app for offline data collection.
                        *   All dynamic form submissions must be linked to a `farmer_uid` (a many2one field to the farmer record) from the core registry.
                        *   Support for designing forms where selected fields can be made available for public farmers' entry via the Farmer Self-Service Portal. Such dynamic forms available on the portal should primarily be for collecting *additional* information linked to an existing (even if provisionally registered) farmer profile. If a dynamic form on the portal is used to capture or update fields that are part of the core farmer/household/plot data model, a strict backend process (e.g., Odoo server action or automated action) must ensure this data is routed through the Core Farmer Registry Engine's validation, de-duplication, and processing logic, maintaining data integrity and consistency with the core registry, rather than storing it merely as separate dynamic form submission data.
                        *   Built-in dashboard and exportable reporting (CSV, XLSX via Odoo's standard export or custom reports) for data collected through each dynamic form.
                    *   A governance process for the creation, modification, and publication of dynamic forms will be established at the national level. This includes defining roles and responsibilities for form design, approval of validation rules and conditional logic, and version management.
                    *   Note: Dynamic forms are designed to extend, not replace, the core farmer registry data model. Data from dynamic forms will be stored in separate Odoo models linked to the farmer record.

            **B.2.2. Rest of System Components & Features**

                **1. Mobile Enumerator App (Android)**
                    *   A native Android application (Kotlin/Java, min SDK e.g., API 26 - Android 8.0) or a high-performance cross-platform application (e.g., Flutter with Dart). [Specifying min SDK level is important for device compatibility].
                    *   Responsive and user-friendly interface, optimized for field data collection on smartphones and tablets.
                    *   Offline-first functionality:
                        *   Ability to create new farmer registrations, edit existing profiles, and complete dynamic forms entirely offline, storing data in a local SQLite database.
                        *   Encrypted local storage (AES-256) for all data stored on the device using SQLCipher or similar. Encryption keys managed securely (e.g., Android Keystore System).
                        *   Maximum offline data footprint per device to be optimized for performance (e.g., up to 1000-5000 farmer profiles and associated active form definitions), subject to device capabilities and efficient data structures. [Providing a range for offline data].
                    *   Bi-directional synchronization mechanism with the Odoo backend via custom REST APIs:
                        *   Syncs farmer profiles (core and dynamic form data) and dynamic form definitions.
                        *   Robust conflict resolution strategy (e.g., timestamp-based, last-write-wins, or flagging conflicts for manual resolution in Odoo). A clear strategy must be defined and implemented.
                    *   Farmer search functionality using QR code scan (linked to farmer UID) or manual UID/name entry within the local offline dataset and via API for online search.
                    *   GPS-based plot location marking (point and/or polygon capture - using device GPS capabilities, potentially with a mapping library like Mapbox SDK or Google Maps SDK if complex interactions are needed). [Mentioning mapping SDKs if advanced features are needed].
                    *   Multilingual UI toggle, supporting configured languages (using Android string resources or equivalent for cross-platform).
                    *   Detailed logs of activities and synchronization status reports, viewable within the app and optionally syncable to the server for troubleshooting.
                    *   Functionality to review, validate, enrich, and approve self-registered farmers submitted via the public Farmer Self-Service Portal, if assigned to the enumerator.

                **2. Role-Based Access Control (RBAC) & Admin Tools (Odoo)**
                    *   Hierarchical access levels: Super Admin (platform-wide), National Admin (country-wide), Supervisor, Enumerator - implemented using Odoo's security groups and `ir.rule` for record-level access.
                    *   Configurable permissions within Odoo for CRUD operations on all data entities, data access scope (e.g., by geographic area using record rules), form publication rights, and system settings.
                    *   Admin dashboard in Odoo to:
                        *   Manage users (create, activate/deactivate, assign roles/groups, reset passwords - using Odoo's standard user management).
                        *   View system logs (Odoo server logs, custom audit logs) and audit trails.
                        *   Interface for approving, rejecting, or assigning portal-based self-registrations to enumerators/supervisors for validation. This includes:
                            *   Automated or manual assignment rules for submissions (e.g., based on geographic area indicated by the farmer, using Odoo server actions or custom logic).
                            *   System notifications (Odoo internal messages, email) to assigned personnel.
                            *   Clear steps for review, field verification (if required), data enrichment, and approval/rejection within an Odoo workflow.
                            *   Status tracking for all self-registrations, visible to administrators. An indicative SLA for initial review (e.g., within 3-5 business days) will be targeted.

                **3. Dashboards & Analytics (Odoo)**
                    *   Real-time Key Performance Indicators (KPIs) on the admin dashboard (Odoo dashboard module): total farmer registrations, gender disaggregation, age distribution, landholding summaries, registration trends.
                    *   Map-based visualizations for farmer and plot locations (e.g., using Odoo's map views with OCA `web_map` or `web_google_maps` module, or integrating a library like Leaflet.js for custom visualizations). [Suggesting specific Odoo map modules or libraries].
                    *   Ability to filter data and export reports (CSV, XLSX, PDF via Odoo's standard export and reporting engine, potentially QWeb for PDF) by geography, dynamic form, time period, farmer status, or other relevant criteria.
                    *   Country-specific analytics views, configurable by National Admins (e.g., saved filters, custom Odoo views).

                **4. Notifications System (Odoo Module)**
                    *   Trigger-based alerts for various system events (e.g., successful farmer registration, self-registration submission, eligibility confirmation for a program linked via dynamic form) using Odoo's automated actions or custom server actions. Business rules for triggering notifications (e.g., events, recipients, content based on farmer status or form submission data) will be configurable by National Administrators using Odoo's automated actions and template system.
                    *   Supported channels: SMS, email (using Odoo's built-in mail system), and potentially push notifications to the mobile app (e.g., via Firebase Cloud Messaging - FCM, requiring setup and integration). [Specifying FCM for push notifications].
                    *   Integration-ready with third-party SMS/email gateway services (e.g., Twilio, Vonage, SendGrid, or local providers via configurable REST/SMPP connectors). Credentials to be provided per country and stored securely (e.g., Odoo `ir.config_parameter` or environment variables).
                    *   Templates for notifications (Odoo email templates, custom models for SMS templates) managed via the Odoo admin console, with support for localization and dynamic placeholders (QWeb/Jinja syntax).

                **5. Integration APIs (Odoo Module/Custom Layer)**
                    *   Secure RESTful APIs, compliant with OpenAPI/Swagger standards (v3.x) for documentation. Built as a custom Odoo module, potentially using OCA `base_rest` as a foundation. [Reiterating OCA `base_rest`].
                    *   Authentication using OAuth2 (e.g., using Odoo's `auth_oauth` module or a custom implementation) / JWT.
                    *   Key endpoints to include:
                        *   Farmer lookup (search by UID, National ID, other criteria).
                        *   Farmer data retrieval (core profile, specific dynamic form data - subject to permissions).
                        *   Endpoints for receiving data from external systems (e.g., weather alerts, ID validation responses).
                        *   Endpoints for handshake with other systems as required.
                        *   Mobile app synchronization endpoints (for sending/receiving farmer data, dynamic forms, etc.).
                    *   The API layer will be developed as a custom Odoo module or utilize a robust OCA module (e.g., `base_rest`), ensuring it meets RESTful conventions and proper error handling.

                **6. Data Migration and Import/Export Toolkits (Odoo)**
                    *   Admin interface within Odoo for bulk import of legacy farmer data from CSV/XLSX formats (using Odoo's standard import interface, possibly extended with custom wizards for complex mapping or validation).
                    *   Bulk data validation during import, with detailed error logs and reporting (Odoo's import provides some feedback; can be enhanced).
                    *   Support for mapping fields from import files to the DFR data schema, including basic data transformation capabilities (potentially through pre-processing scripts or custom import logic if Odoo's default is insufficient).
                    *   Exportable reports and raw data extracts in standard formats (CSV, XLSX - using Odoo's standard export features).
                    *   Detailed data migration plan to be developed for each country, covering:
                        *   Source data identification and analysis (from legacy systems/files).
                        *   Data extraction procedures from identified legacy sources.
                        *   Data cleansing and transformation rules and processes (e.g., standardization of values, handling missing data, format conversions).
                        *   Mapping of legacy data fields to DFR Odoo schema.
                        *   Data loading procedures (ETL) into the DFR staging environment.
                        *   Comprehensive data validation and reconciliation strategy post-migration (e.g., record counts, spot checks, field-level validation against source, user acceptance testing of migrated data).
                        *   Error handling and resolution process for migration discrepancies.
                        *   Sign-off procedure for migrated data by national counterparts.
                    *   Support for incremental data migration if a phased rollout or parallel run is adopted.

                **7. Farmer Self-Service Portal (Public Web Interface - Odoo Portal/Website)**
                    *   A country-branded, mobile-responsive public website, built using Odoo's website/portal capabilities.
                    *   Displays localized information about the Digital Farmer Registry, its benefits, and how to register.
                    *   A simple and accessible form for farmer pre-registration, capturing key KYC fields (e.g., name, village, primary crop type, contact number, National ID if applicable). Data submitted through this pre-registration form directly populates the Core Farmer Registry Engine (e.g., creates a 'draft' or 'pending verification' farmer record), initiating the standard registration workflow.
                    *   Submissions are securely stored in Odoo and routed (e.g., using Odoo activities or assignments) to assigned enumerators or National Admins/Supervisors for review, validation, data enrichment, and final approval.
                    *   Supports multilingual interface based on country configuration (using Odoo's website language switcher).
                    *   An audit trail is maintained for each self-registration submission and its processing steps (e.g., via Odoo chatter on the farmer record).
                    *   Admin controls within Odoo for enabling/disabling public portal access per country.

                **8. Localization Toolkit (Odoo)**
                    *   Multi-language support across all user interfaces (web admin, mobile app, self-service portal) and dynamic form content using Odoo's standard translation system (`.po` files).
                    *   Mechanism for managing language packs (translations) for UI elements and form field labels/instructions (Odoo's 'Load a Translation' feature).
                    *   Support for Right-to-Left (RTL) scripts if required by any participating country (Odoo has some RTL support; needs verification for specific languages).
                    *   Admin interface in Odoo for uploading and managing translated content.

                **9. Hosting & Deployment (as per WP-A.2.4)**
                    *   System deployed to country-approved infrastructure (government data center, approved cloud, or hybrid).
                    *   Establishment of at least three-tier architecture environments: Development (local or shared dev server), Staging (UAT, pre-prod, data migration testing), and Production for each country instance. [Standard environment setup].
                    *   HTTPS/SSL (TLS 1.2+ enforced) enabled for all web traffic, using reverse proxies like Nginx or Apache. [Specifying TLS version and reverse proxy].
                    *   Automated backup procedures (e.g., cron jobs for `pg_dump`, WAL archiving) and system monitoring readiness (integration with tools like Prometheus/Grafana).
                    *   Deployment via Docker containers or equivalent packaging for consistency and ease of management. Odoo and PostgreSQL should run in separate containers. [Adding detail on container setup]. Consider Docker Compose for simpler setups and Kubernetes for complex, scalable deployments. [Suggesting orchestration tools].
                    *   Admin console or configuration files (Odoo config file, environment variables) to manage hosting-related settings.
                    *   A detailed deployment plan for each country instance, outlining:
                        *   Implementation approach (e.g., Pilot phase with a subset of users/data, followed by a Phased Rollout by region/enumerator group, or a Big Bang approach if deemed appropriate and low risk for a specific country context). The choice of approach will be determined in consultation with FAO and national counterparts for each country.
                        *   Pre-deployment checklist.
                        *   User communication plan for deployment.

                **10. Data Security, Audit Logs & Change History (Odoo)**
                    *   Robust data security measures implemented throughout the Odoo application (access rights, record rules, password policies) and infrastructure (firewalls, secure configurations).
                    *   Comprehensive audit logs capturing user actions: logins (successful/failed), data creation, updates, deletions (tracked via Odoo's `mail.thread` and custom logging for critical actions), dynamic form submissions, verification actions, and mobile sync events. Log data should be stored securely and be tamper-evident if possible.
                    *   Change history tracking (versioning) for all critical data records, particularly within the Farmer Registry Engine (e.g., changes to farmer profile, plot details) using Odoo's `mail.thread` capabilities or custom versioning if more detail is needed.
                    *   Ability for authorized administrators to export audit logs and change history for compliance, system monitoring, or investigation purposes.
                    *   Restricted visibility of logs to authorized admin roles only (configured via Odoo access rights).
                    *   Data privacy compliance: The system must be designed to comply with identified data protection and privacy laws of each target country (as per section 1.4 and 2.5), including features for managing farmer consent for data collection and use (e.g., specific consent fields in Odoo, audit of consent changes). The system must incorporate mechanisms to manage farmer consent in accordance with the specific legal requirements of each target country, including obtaining, recording, and managing consent for data collection, processing, storage, and potential sharing. This includes versioning of consent given and allowing for withdrawal of consent where legally mandated.
                    *   Data retention policies: Clear data retention policies for farmer profiles, household data, plot information, dynamic form submissions, and audit logs will be configurable (e.g., via system parameters or scheduled actions in Odoo), based on guidance from FAO and national counterparts. An archiving strategy for older data (e.g., moving to a separate archive database or cold storage, with mechanisms for retrieval if needed) will be implemented to ensure long-term system performance and manage storage costs. The process for defining, approving, and implementing these country-specific data retention and archiving policies will be established in collaboration with FAO and national legal/IT focal points.

        **B.3. Deliverables (for WP-B)**
            *   B1.1. Fully developed Core Farmer Registry Engine (Odoo module, e.g., `dfr_farmer_registry`).
            *   B1.2. Fully functional Dynamic Form Engine (Custom Form Builder Odoo module, e.g., `dfr_dynamic_forms`).
            *   B1.3. Offline-enabled Android Enumerator App (Native or Cross-platform, APK/AAB file and source code).
            *   B1.4. Web Admin Portal (Odoo backend) with RBAC, dashboard, and form controls.
            *   B1.5. Role-based analytics and reporting suite within Odoo (standard reports, custom QWeb reports if needed).
            *   B1.6. Notification System (Odoo module) configured for SMS/Email alerts to farmers.
            *   B1.7. Integration-ready RESTful APIs with OpenAPI/Swagger documentation (JSON/YAML file and live documentation endpoint).
            *   B1.8. Data Migration and Import/export toolkit within Odoo, metadata mapping guides, and country-specific data migration plans and validation reports.
            *   B1.9. Farmer Self-Service Portal (Odoo website/portal) with country branding and public-facing registration workflow.
            *   B1.10. Localization toolkit and initial language packs (.po files based on provided translations).
            *   B1.11. DevOps-ready deployment package (e.g., Docker images, Docker Compose files, CI/CD pipeline scripts/configuration for Jenkins/GitLab CI/GitHub Actions) and country-specific deployment plans.
            *   B1.12. Operational sandbox/testing environment populated with mock data (realistic, anonymized if based on real data) for each country, including migrated data samples where applicable.
            *   B1.13. Admin manuals, user guides, SOPs for system use, including notification templates and data migration procedures.
            *   B1.14. Implemented Data Security features, Audit Logs & Change History functionality.

        **B.4. Delivery Preconditions & Clarifications (for WP-B)**
            *   FAO and national counterparts will provide:
                *   Final common data schema for the core registry (including field names, types, constraints).
                *   Localization inputs (language files as .po, form field translations).
                *   Credentials for third-party API testing (e.g., SMS gateway sandbox accounts).
                *   Details of specific systems for any immediate integrations (API endpoints, authentication details, sample requests/responses).
                *   Source data for migration (if applicable) in agreed formats, and participation in data validation and sign-off.
                *   Finalized business rules for critical workflows, or active participation in their definition during design.
            *   Core farmer registration data model (Odoo models) must be finalized before extensive development of the registry engine.
            *   Every dynamic form submission must link to a unique `farmer_uid` (many2one relation in Odoo).
            *   The dynamic form engine must support form versioning to preserve historical data schemas.

        **B.5. Acceptance Criteria (for WP-B)**
            *   Fully functional system deployed and live in a staging environment for all five countries, demonstrating core functionalities as per this SRS.
            *   All modules (Farmer Registry, Dynamic Forms, Mobile App, Admin Portal, APIs, etc.) are tested (unit, integration, user acceptance), integrated, and validated against requirements.
            *   Successful completion of data migration UAT for each country instance with legacy data, meeting agreed data quality and completeness thresholds.
            *   Admins and enumerators (test users) are able to operate the system independently in the sandbox environment following provided user guides.
            *   Offline mobile app functionality, including data sync (bi-directional) and conflict resolution, is demonstrated and validated with various network conditions (offline, intermittent, stable).
            *   Key performance indicators (KPIs) for system responsiveness are met in the staging environment under simulated load. Examples:
                *   Mobile app sync completion time for 500 records < 2 minutes on a simulated 3G connection (e.g., 384 kbps down / 128 kbps up).
                *   Web portal page load times < 3 seconds for 95% of requests for standard views.
                *   API response times < 500 ms for 95% of calls under a concurrent load of 10 test users per country instance. (Targets to be finalized with FAO and benchmarked).
            *   Security measures, including RBAC, audit logs, data encryption (mobile local storage, data in transit via TLS), and protection against OWASP Top 10 web vulnerabilities, are implemented and verified (e.g., through vulnerability scans, penetration testing if in scope).

    **3.3. Work Package C: Capacity Building, Training & Change Management**

        **C.1. Objective:** To equip national administrators, enumerators, and support personnel across targeted countries with the knowledge, tools, and confidence to independently operate, manage, and sustain the DFR system, including processes related to data migration validation and system cutover.

        **C.2. Scope of Work**

            **C.2.1. Key Activities**
                **1. Training Resource Development**
                    *   Develop modular, role-based training materials aligned with user categories:
                        *   Administrators: Odoo user management, dynamic form builder usage, business rule configuration (workflows, de-duplication, notifications), notification system configuration, analytics and reporting (Odoo standard and custom), data import/export, data migration validation procedures, system monitoring basics (Odoo logs, basic server health checks), cutover participation roles.
                        *   Enumerators: Mobile app usage (online/offline modes), farmer registration process, completing dynamic forms, data synchronization procedures and troubleshooting, QR code scanning, GPS capture, common mobile app issues.
                        *   Support teams: Common troubleshooting procedures (Odoo and mobile app), sync issue diagnosis, access control management, escalation paths, basic data quality checks, data migration issue reporting.
                    *   Develop a package of self-paced learning resources, including:
                        *   Step-by-step illustrated user manuals (PDF and web-accessible versions, e.g., HTML generated from Markdown/Sphinx).
                        *   Screencast training videos (e.g., MP4 format, 720p resolution) for each core task on both Web (Odoo) and Android platforms.
                        *   A centralized, searchable documentation wiki/portal (e.g., hosted on a simple platform like MkDocs, ReadtheDocs, or integrated if Odoo has such capability, or a shared document repository like SharePoint/Google Drive) covering: FAQs, guides, glossary, visual walkthroughs, versioned updates, configuration guides, and admin tools overview. [Suggesting specific tools for documentation portal].
                        *   Printable quick-reference guides and cheat sheets.
                    *   All materials to be developed in English and translated into local languages (using provided translations) as agreed with FAO and national counterparts.

                **2. Remote Training Delivery**
                    *   Conduct a remote-only Train-the-Trainer (ToT) program for designated personnel in each country.
                    *   Training delivered under FAO guidance and support via preferred virtual platforms (e.g., Zoom, Microsoft Teams, Google Meet) with features for screen sharing, recording, and Q&A. [Adding examples of virtual platforms].
                    *   All ToT sessions to be recorded (e.g., in MP4 format) and shared with countries for future reuse and for those unable to attend live.
                    *   Coordinate with national focal points to ensure participant access and engagement.
                    *   Incorporate interactive Q&A sessions and feedback mechanisms (e.g., polls, online forms).
                    *   Support national trainers with sample training agendas, presentation scripts (e.g., PowerPoint, Google Slides), practice exercises using the sandbox platform (including data migration validation exercises), troubleshooting kits, and escalation protocols.

                **3. Helpdesk SOPs & Change Management Support**
                    *   Develop Helpdesk Standard Operating Procedures (SOPs) for Tier-1 support at the national level, including ticket logging and prioritization guidelines.
                    *   Document common troubleshooting flows (e.g., mobile app sync failure, login issues, dynamic form errors, data correction procedures within Odoo, data migration queries).
                    *   Provide a digital adoption & change management guide, including:
                        *   Communication templates (e.g., SMS, email, posters) for engaging enumerators and farmers about the DFR, including system transition and go-live announcements.
                        *   Tips for monitoring system adoption rates (e.g., active users in Odoo, mobile app sync frequency) and data quality (e.g., completeness, consistency checks).
                        *   Guidance on establishing local support mechanisms.

        **C.3. Deliverables (for WP-C)**
            *   C1.1. Modular, multilingual training materials by role (admin, enumerator, support) in editable formats (e.g., Word, PowerPoint) and distributable formats (PDF, HTML), including data migration and cutover specific content.
            *   C1.2. Illustrated user manuals and quick-start guides (PDF + web-optimized versions).
            *   C1.3. Screencast-style training videos hosted on an accessible platform (e.g., YouTube private channel, Vimeo, shared drive, or LMS if available by FAO).
            *   C1.4. Hosted documentation wiki/portal with search, navigation, and update tracking capabilities, or source files for such a portal.
            *   C1.5. At least three (3) distinct virtual ToT sessions (e.g., Admin Training, Enumerator Training, Support Training) delivered and recorded for each of the five countries.
            *   C1.6. Helpdesk SOPs, escalation matrix, and troubleshooting handbook.
            *   C1.7. Change management toolkit for each country (communication templates, adoption tracking tips, support guidance).

        **C.4. Delivery Preconditions & Clarifications (for WP-C)**
            *   Contractor is not required to deliver in-person training.
            *   FAO and national focal points will:
                *   Nominate ToT participants with appropriate technical aptitude and training capacity.
                *   Facilitate participant access to virtual sessions (stable internet, necessary devices).
                *   Review and approve localized language versions of training materials.
                *   Participate in defining roles for cutover and data migration validation.
            *   Contractor must ensure:
                *   Training videos and materials are accessible offline (e.g., downloadable) and in low-bandwidth formats where possible (e.g., compressed videos, optimized PDFs).
                *   The training sandbox environment accurately mirrors the production system, including dynamic forms, user roles, and sufficient dummy data (and sample migrated data) for realistic training exercises.

        **C.5. Acceptance Criteria (for WP-C)**
            *   Training materials are delivered in English and localized languages as agreed, reviewed, and approved by FAO/national counterparts.
            *   All training videos cover core system workflows, are clear, concise, and usable for independent learning.
            *   The documentation wiki/portal is live, searchable, and updated through the deployment phase with relevant content.
            *   Virtual ToT sessions completed for all five countries, with participation logs and session recordings shared with FAO.
            *   Sandbox environment access is successfully used by trainees during ToT sessions, with positive feedback on its utility.
            *   At least 85% of ToT participants confirm (via standardized feedback forms post-training) their readiness and confidence to train other users in their respective countries, including understanding their roles in data migration validation and system cutover.
            *   Helpdesk SOPs are reviewed and accepted by FAO and national focal teams.
            *   Change management and adoption guidance provided, with country-specific recommendations acknowledged by national counterparts.

    **3.4. Work Package D: Post-Deployment Support, Maintenance & Handover**

        **D.1. Objective:** To provide 24-month SLA-based support and maintenance services for the DFR platform, ensuring continuous improvements, patching (Odoo core and custom modules), and complete knowledge transfer post-deployment to enable long-term sustainability. This includes a defined hypercare period immediately following go-live for each country instance.

        **D.2. Scope of Work**

            **D.2.1. Support & Maintenance Services**
                *   Incident support (bug fixing) for issues encountered in live production environments (Odoo web and mobile app) via a defined ticketing system (e.g., JIRA Service Desk, Zendesk, or email-based helpdesk). [Specifying ticketing system examples]. This includes an initial hypercare support period (e.g., 2-4 weeks post go-live per country) with heightened monitoring and faster response times for critical issues.
                *   Patch management for the shared core Odoo codebase (custom modules) and guidance on applying Odoo S.A. security updates for the community edition, including security updates and bug fixes. Patches will be tested on staging before production deployment.
                *   System performance monitoring (Odoo application performance, PostgreSQL database health, server resource utilization) and proactive issue detection in collaboration with national IT teams, using tools like Prometheus, Grafana, or Odoo's own monitoring capabilities.
                *   Quarterly system health reviews and patch release reports provided to FAO.
                *   Implementation of minor enhancements and UI/UX improvements based on prioritized requests from FAO or country teams (within a predefined effort cap per quarter, e.g., 5-10 developer-days, to be agreed). [Quantifying minor enhancement cap].
                *   Mobile app updates to ensure compatibility with new Android OS versions (within reasonable limits, e.g., latest 3 major versions) and security patches.
                *   Support for dynamic form logic corrections (if issues arise from core engine bugs not configurable by admins), user permission adjustments, or minor workflow issues not configurable by National Admins.
                *   A detailed list of key metrics for system health and performance monitoring (Odoo application: response times, error rates; PostgreSQL database: query performance, connection counts, disk space; server infrastructure: CPU, memory, network I/O; mobile sync processes: success/failure rates, sync times) will be defined. Alert thresholds for critical and warning events and the corresponding notification channels (e.g., email, SMS to designated admin groups) will be established and monitored.

            **D.2.2. Documentation, Code Standards & Knowledge Transfer (Ongoing)**
                *   Deliver and maintain the complete source code in a version-controlled repository (e.g., GitHub/GitLab), structured as:
                    *   Modular, well-commented Odoo modules (Python, XML, JS) and mobile app codebase (Kotlin/Java or Dart).
                    *   Clearly separated frontend (Odoo web client, mobile app UI), backend (Odoo Python modules), mobile, and configuration layers.
                    *   Open-source license (MIT or Apache 2.0) with no usage restrictions.
                *   Provide and update a Codebase Onboarding Guide, including:
                    *   Explanation of Odoo module structure, key custom models, and mobile app project structure.
                    *   Configuration instructions (e.g., Odoo config file, environment variables, API keys, language pack management).
                    *   Detailed deployment walkthrough (Docker/Kubernetes or equivalent, including Nginx/reverse proxy setup).
                    *   Scripts for staging and production deployment (e.g., shell scripts, Ansible playbooks if used).
                *   Ensure consistent function-level code commenting (Python docstrings, JSDoc, KDoc/JavaDoc) and use of README files per Odoo module/mobile app component.
                *   Provide and update an API developer guide for external system integration, based on the OpenAPI/Swagger documentation.
                *   Maintain a detailed Change Log (CHANGELOG.md) with semantic versioning and release notes for all platform updates and patches.

            **D.2.3. Knowledge Transfer & Exit Readiness (Culminating at end of support period)**
                *   Conduct a series of remote walkthrough sessions with FAO and designated national IT teams to explain:
                    *   Odoo core code structure, custom module logic (Python, XML, JS), and extension points.
                    *   Mobile app architecture (native Android or Flutter/React Native) and codebase.
                    *   Dynamic form builder configuration and advanced usage (e.g., complex validations, conditional logic if implemented via code).
                    *   Dashboard and reporting setup and customization within Odoo (QWeb report development, custom views).
                    *   Data backup (PostgreSQL `pg_dump`, WAL archiving), restoration (PITR), and migration practices (including scripts and lessons learned from initial migration).
                    *   System monitoring (key metrics, tools used) and basic troubleshooting (Odoo logs, PostgreSQL performance).
                *   Deliver a Final Knowledge Transfer Kit at the end of the support period, including:
                    *   Final system architecture diagram (including infrastructure components).
                    *   Final data schema documentation (Odoo models with fields, types, relations - potentially generated using tools or custom scripts).
                    *   Admin credential matrix (template, to be populated by countries for their internal records).
                    *   Handover certificates from each country (confirming receipt of code, docs, and KT).

        **D.3. Deliverables (for WP-D)**
            *   D1.1. 24-month support and issue resolution services, evidenced by ticket logs from the helpdesk system and resolution tracking, including hypercare period reports.
            *   D1.2. Quarterly system health, performance, and enhancement reports.
            *   D1.3. Fully version-controlled code repository (Odoo modules, mobile app) with comprehensive comments, README files, and confirmed open-source license.
            *   D1.4. Updated Codebase Onboarding Guide and API Developer Documentation.
            *   D1.5. Remote knowledge transfer walkthrough sessions with FAO/country IT teams (recordings and documentation shared).
            *   D1.6. Final Knowledge Transfer Kit with handover documentation and exit checklist.
            *   D1.7. Clean and consistently maintained Change Log (CHANGELOG.md) and semantic version history of all releases and patches.

        **D.4. Delivery Preconditions & Clarifications (for WP-D)**
            *   Contractor must be available for email/ticket-based support during agreed business hours, adhering to defined SLAs.
            *   FAO and national teams will:
                *   Report incidents via an agreed channel (e.g., helpdesk portal, dedicated email) with sufficient detail for diagnosis.
                *   Approve patch releases for deployment to staging and subsequently production environments in a timely manner.
            *   Contractor shall not impose additional licensing, access, or tooling restrictions on the use, deployment, or customization of the delivered system beyond the chosen open-source license terms.

        **D.5. Support SLAs (Service Level Agreements)**
            | Issue Severity             | Response Time   | Resolution Time Target |\n            |----------------------------|-----------------|------------------------|\n            | Critical (System down, major data loss/corruption risk, core functionality unusable for all users) | 1 business hour | 4 business hours       |\n            | High (Major function failure, no workaround, significant impact on many users) | 2 business hours | 8 business hours       |\n            | Medium (Minor function failure, workaround available; performance degradation impacting some users) | 4 business hours | 2 business days        |\n            | Low (Cosmetic issues, usability tweaks, content updates, queries, non-critical errors) | 1 business day  | 5 business days        |\n            *(Business hours for SLA response times must be clearly defined, e.g., Monday-Friday, 9 AM - 5 PM in a specific primary support timezone, or a model that provides reasonable overlap across the Pacific Island Countries. This definition must account for providing equitable service coverage across all five participating Pacific Island Countries (Cook Islands, Samoa, Solomon Islands, Tonga, and Vanuatu) and their respective time zones, particularly for Critical and High severity issues. This may be achieved through strategies such as: defining extended support hours for critical issues (e.g., on-call for P1), implementing a tiered support model where national teams provide initial response within their local business hours with clear escalation paths, or by explicitly stating the operational support timezone and acknowledging its implications for response times in other zones. The chosen approach will be agreed upon with FAO. Hypercare period SLAs for Critical/High issues may be more stringent and will be defined in the country-specific cutover plan.)* [Enhanced SLA business hours definition for clarity across time zones and added note on hypercare].

        **D.6. Acceptance Criteria (for WP-D)**
            *   SLAs are consistently met throughout the 24-month support period, as evidenced by support logs and quarterly reports.
            *   All documentation (Codebase Onboarding Guide, API Guide, KT Kit) is delivered, complete, and up-to-date at the point of final handover.
            *   National IT teams demonstrate capability to operate and perform basic maintenance (e.g., Odoo updates, PostgreSQL backups, user management) independently by the end of the support period (assessed via feedback, KT session outcomes, and ability to resolve minor issues).
            *   Final knowledge transfer walkthroughs are conducted, recordings shared, and all KT documents accepted by FAO.
            *   Handover packages and certificates are signed off by FAO or respective national counterparts at the conclusion of the support period.

    **3.5. Work Package E: Codebase Ownership Transfer & Exit Readiness**

        **E.1. Objective:** To ensure that each participating country gains full operational ownership and control over its deployed DFR system instance, including its specific configured version of the codebase (Odoo modules, mobile app), deployment artifacts, essential credentials (for systems managed by contractor during setup, to be securely transferred), and comprehensive documentation. This transfer supports national digital sovereignty and aims to eliminate long-term dependency, within the framework of the shared codebase governance model (as defined in A.2.2) designed for ongoing sustainability and reusability.

        **E.2. Scope of Work**
            The contractor shall carry out a structured, documented, and country-specific ownership transfer process. This largely overlaps with and is the culmination of activities in WP-D, specifically focusing on the final handover.

            **E.2.1. Ownership Transfer Elements**
                For each country, the contractor shall ensure final delivery and confirmation of receipt for:
                **1. Codebase Transfer**
                    *   Access to the shared core Odoo codebase and a clear definition (e.g., specific Git version tag or branch) that is precisely aligned to the country's finally deployed version. This includes:
                        *   All country-specific configuration files (e.g., Odoo config, environment variable templates) and settings.
                        *   Country-specific language packs (.po files).
                        *   Any custom/additive Odoo modules developed for that country instance in line with the codebase governance model.
                        *   Confirmed access (e.g., as owner or admin, as appropriate per the governance model) to their specific instance configurations and relevant parts of the version-controlled repository (e.g., GitHub/GitLab, including transfer of repository ownership or granting admin rights to national IT teams).

                **2. Deployment Assets**
                    *   Final versions of Docker containers (images and Dockerfiles), CI/CD scripts (e.g., Jenkinsfile, .gitlab-ci.yml), and environment configuration templates used for their instance.
                    *   Handover of any cloud credentials (e.g., IAM user credentials, service account keys) if the infrastructure was initially set up and managed by the contractor on a national cloud account (to be securely transferred to national IT, with guidance on changing passwords/keys post-transfer).
                    *   Documentation for accessing admin panels (Odoo, hosting provider, monitoring tools) and managing security keys (SSL/TLS certificates, API keys, database credentials - with clear instructions on rotation/updates).

                **3. Documentation & Admin Toolkits**
                    *   Final, country-specific (if variations exist beyond configuration) architecture diagram, schema documentation (Odoo models, PostgreSQL schema), and system overview.
                    *   Final deployment and rollback guides, including steps for Odoo and PostgreSQL.
                    *   System update procedures (for custom modules and Odoo core) and test protocols.
                    *   Final data migration reports and lessons learned documentation.

                **4. Credential & Configuration Matrix (Template and Guidance)**
                    *   A template for a National Admin user account matrix (for countries to maintain who has what role in Odoo).
                    *   Documentation of any integration keys or sandbox access credentials that were centrally managed by the contractor during development/support, with instructions for national teams to generate/manage their own production keys.
                    *   Guidance on managing notification template controls and API tokens within Odoo.

                **5. Walkthrough & Sign-off**
                    *   A final live remote session with FAO and national IT focal points to confirm handover of all assets and address final questions.
                    *   This session will serve as a final check against the Knowledge Transfer Kit and the deliverables listed in this section.
                    *   A signed Country Ownership Transfer Certificate by the designated national authority and FAO.

        **E.3. Deliverables (for WP-E - primarily confirmations and finalizations from WP-D)**
            *   E1.1. Confirmed country-specific version of the codebase (Git tag/branch) accessible in a version-controlled repository by each country.
            *   E1.2. Country Codebase Repositories: Confirmation of access (admin/owner rights) to all relevant configuration files, language packs, and deployment packages (Dockerfiles, CI/CD scripts).
            *   E1.3. Documented procedure for managing access credentials to production and admin environments (primary responsibility shifts to country IT, including secure storage and rotation policies).
            *   E1.4. Final comprehensive technical documentation set (architecture, schema, deployment guide, CI/CD instructions, API docs, Odoo module documentation, data migration reports).
            *   E1.5. Credential & access control matrix template and guidance provided to each national instance.
            *   E1.6. Shared recording of the final system handover walkthrough with FAO and national IT teams.
            *   E1.7. Signed Ownership Transfer Certificate for each participating country.

        **E.4. Acceptance Criteria (for WP-E)**
            *   Handover certificates are signed by authorized representatives from all five countries and FAO, confirming receipt and acceptance of all deliverables outlined in WP-E.2.1.
            *   National IT teams confirm they have the necessary access, code, documentation, and knowledge (as per KT sessions) to independently manage, maintain (including applying Odoo updates), and deploy their DFR instance.

    **3.6. Transition Requirements** (New Section)

        **3.6.1. Overall Transition Strategy**
            *   The DFR system will be implemented on a country-by-country basis.
            *   For each country, the implementation approach (e.g., Pilot phase with a subset of users/data, followed by a Phased Rollout by region/enumerator group, or a Big Bang approach) will be determined in consultation with FAO and national counterparts, documented in the country-specific deployment plan (B.2.2.9).
            *   A detailed transition plan will be developed for each country, encompassing data migration, training, cutover, and legacy system considerations.

        **3.6.2. Data Migration Strategy** (Consolidates and expands on B.2.2.6)
            *   A comprehensive data migration strategy will be executed for each country instance requiring migration from existing systems (digital or paper-based).
            *   This strategy includes:
                *   Identification and profiling of source data systems/formats.
                *   Secure extraction of data from legacy systems.
                *   Data cleansing, transformation, and mapping to the DFR Odoo schema, with business rules for transformation clearly documented and approved.
                *   Loading of transformed data into the DFR staging environment for validation.
                *   Rigorous validation of migrated data by national counterparts, including record counts, field-level checks, and business rule compliance, supported by reconciliation reports.
                *   Iterative error correction and re-validation cycles.
                *   Formal sign-off on migrated data quality and completeness before production cutover.
                *   Procedures for handling data entered into legacy systems during the transition period (if parallel run occurs).

        **3.6.3. Training for Transition**
            *   Training materials and sessions (WP-C) will include specific modules on:
                *   National administrators' roles in overseeing and validating data migration.
                *   User roles and responsibilities during the cutover period.
                *   Using the new DFR system in the context of replacing legacy processes.

        **3.6.4. System Cutover and Go-Live Strategy**
            *   Development of a detailed cutover plan for each country's DFR instance go-live, including:
                *   Go/No-Go criteria for proceeding with the production cutover (e.g., successful UAT completion, data migration validation sign-off, critical bug resolution, user training completion, infrastructure readiness).
                *   A detailed timeline and sequence of cutover activities (e.g., final data migration sync, legacy system freeze (if applicable), system configuration lockdown, switching DNS, enabling access to DFR).
                *   Communication plan for all stakeholders (users, IT, management) before, during, and after cutover.
                *   Defined rollback/contingency plan in case of cutover failure, specifying triggers for rollback, procedures to revert to the previous state or a stable interim state, and responsibilities.
                *   Post-go-live hypercare support period definition (e.g., first 2-4 weeks with intensified support and dedicated resources as per D.2.1).
                *   Success criteria for go-live (e.g., system stability, successful first transactions/registrations, key user confirmation of operational readiness, performance metrics met).

        **3.6.5. Legacy System Integration and Decommissioning (If Applicable)**
            *   If DFR needs to integrate with legacy systems during a transition period (parallel run):
                *   APIs or data exchange mechanisms will be defined for data synchronization.
                *   The direction and frequency of synchronization will be specified.
            *   For each country, if the DFR replaces existing systems, a strategy for the eventual decommissioning of these legacy systems will be outlined in consultation with national counterparts. This includes:
                *   Criteria for initiating decommissioning (e.g., successful DFR operation for a defined period, full data migration and validation, user adoption targets met).
                *   Data archival procedures for legacy data not migrated to DFR but required for historical/legal reasons, ensuring compliance with national data retention policies.
                *   Secure shutdown and disposal/repurposing of legacy system hardware/software.
                *   Formal communication to any remaining users of the legacy system regarding its decommissioning.

        **3.6.6. Business Rule Transition**
            *   Existing business rules from legacy systems or manual processes will be identified, documented, and reviewed for applicability in the new DFR system.
            *   National administrators will be trained on how to configure and manage these business rules (e.g., farmer statuses, de-duplication parameters, notification triggers, dynamic form validation) within the Odoo platform.
            *   Any business rules that cannot be configured and require code changes will be clearly documented and implemented as part of WP-B, with approval from national counterparts.

**4. Non-Functional Requirements**

    **4.1. Performance Requirements**
        *   **Response Times:**
            *   Web Admin Portal (Odoo): Standard page loads (most list/form views) < 3 seconds; data-intensive operations (e.g., complex searches on >100k records, report generation for 1000s of records) < 10-15 seconds. [Adjusted for potentially larger datasets].
            *   Farmer Self-Service Portal: Page loads < 3 seconds.
            *   Mobile Enumerator App: UI responsiveness < 1 second for typical interactions (form navigation, data input).
            *   API Response Times: < 500 ms for 95% of calls under expected peak load (to be defined per country, e.g., 10-50 requests/second for key APIs).
        *   **Synchronization:**
            *   Mobile app sync (bi-directional) for a batch of 500 farmer records (new or updated) with associated data (e.g., 2 plots, 1 dynamic form submission per farmer) should complete within 2 minutes over a stable 3G connection (e.g., 384 kbps down / 128 kbps up). [Adding detail to record complexity].
        *   **Concurrent Users:** The system (per country instance) must support at least:
            *   50 concurrent *active* enumerators using the mobile app (actively syncing or interacting online). [Clarified 'active'].
            *   10 concurrent *active* administrative users on the Odoo web portal.
            *   100 concurrent users on the Farmer Self-Service Portal during peak registration drives (e.g., browsing, submitting forms).
            *(These are initial targets and should be refined based on country-specific expected load and confirmed via load testing.)*
        *   **Data Import:** Bulk import of 10,000 farmer records (CSV/XLSX) using Odoo's import tool during data migration or ongoing operations should complete within an acceptable timeframe (e.g., < 30 minutes), with progress indication and clear error reporting. [Refined import time].

    **4.2. Scalability Requirements**
        *   The architecture must be scalable to handle a 100% increase in the number of farmers, households, plots, and dynamic form submissions over a 5-year period without significant performance degradation or requiring major re-architecture. This involves:
            *   Odoo application server scalability (horizontal scaling via multiple Odoo workers/processes, potentially load balanced).
            *   PostgreSQL database scalability (efficient indexing, query optimization, connection pooling e.g., PgBouncer, potential for read replicas if supported by the Odoo setup and application logic). [Adding specific database scalability techniques].
        *   The system should allow for horizontal scaling of application servers and potentially database read replicas if Odoo architecture and hosting permit.
        *   Estimates for current and future data volumes per country will be provided by FAO/national counterparts to guide database sizing, indexing strategies (e.g., on frequently queried fields, foreign keys), and Odoo configuration (e.g., worker limits).

    **4.3. Security Requirements**
        *   All data transmission between client (browser, mobile app) and server must be encrypted using HTTPS/TLS (TLS 1.2 or higher enforced). [Enforced TLS version].
        *   Data at rest on the mobile enumerator app must be encrypted using AES-256 encryption (e.g., SQLCipher for SQLite). Encryption keys must be managed securely using platform-provided mechanisms (e.g., Android Keystore System).
        *   Authentication: Strong password policies (configurable in Odoo, e.g., length, complexity, expiry), OAuth2/JWT for APIs. Multi-Factor Authentication (MFA/2FA) should be available and recommended for all administrative Odoo users. [Added MFA recommendation].
        *   Authorization: Granular RBAC must be enforced across all system components (Odoo access rights, record rules, API endpoint protection).
        *   Protection against common web vulnerabilities (OWASP Top 10) must be implemented and verified (e.g., SQL injection (mitigated by Odoo ORM), XSS, CSRF). Regular security scanning (SAST/DAST tools like SonarQube, OWASP ZAP), manual security code reviews for critical security-sensitive modules, and penetration testing (if in scope) should be part of the quality assurance process. [Added SAST/DAST tools and manual reviews].
        *   Regular security patching of Odoo (custom modules and core), underlying OS (e.g., Linux distributions), PostgreSQL, Nginx, and all dependencies.
        *   Comprehensive audit trails for all sensitive operations and data changes, stored securely.
        *   Compliance with identified data protection and privacy laws for each target country (as per section 1.4, 2.5), including mechanisms for farmer consent management and data subject rights (e.g., access, rectification, erasure where applicable, data breach notification considerations).
        *   Session Management: Secure session handling for web applications, including appropriate timeouts and cookie security flags (HttpOnly, Secure, SameSite). [Added session management specifics].
        *   Input Validation: Strict input validation on all user-supplied data on both client-side (as a preliminary check) and server-side (as the authoritative check) to prevent injection attacks and ensure data integrity. [Explicitly stated input validation].
        *   Dependency Management: Regularly scan and update third-party libraries and dependencies (Odoo modules, Python packages, mobile app libraries) to patch known vulnerabilities. A Software Bill of Materials (SBOM) should be maintained and provided.

    **4.4. Usability Requirements**
        *   Interfaces (web and mobile) must be intuitive, user-friendly, and require minimal training for basic operations. Design should follow established UX principles for clarity and efficiency.
        *   The mobile app must be optimized for ease of use in field conditions, potentially with varying literacy levels of enumerators (e.g., clear icons, simple language, logical flow).
        *   Web interfaces (Odoo admin, Farmer Self-Service Portal) should adhere to WCAG 2.1 Level AA accessibility guidelines where feasible within the Odoo framework.
        *   Clear error messaging (user-friendly, non-technical) and guidance for users to correct errors or proceed.
        *   Consistent navigation, terminology, and visual design across the platform (Odoo and mobile app where appropriate).

    **4.5. Reliability Requirements**
        *   The system should aim for 99.5% uptime for each country instance (excluding scheduled maintenance windows, which should be communicated in advance).
        *   Robust error handling (e.g., try-catch blocks, graceful degradation) and data validation (Odoo constraints, API validation) to prevent data corruption.
        *   Offline mobile app must function reliably without data loss when network connectivity is unavailable. Local data integrity must be maintained.
        *   Synchronization mechanism must be resilient to network interruptions (e.g., resumable, idempotent operations) and ensure data consistency between mobile and server, with clear conflict resolution.
        *   Backup and recovery procedures must be in place and regularly tested to meet defined RTO/RPO targets.
        *   The system design should aim to avoid single points of failure (SPOFs) in critical components, where feasible within the Odoo architecture and hosting environment.

    **4.6. Maintainability Requirements**
        *   The codebase must be modular (Odoo modules, distinct mobile app components), well-documented (inline comments, Python docstrings, JSDoc, module READMEs), and adhere to defined coding standards (e.g., PEP 8 for Python, Odoo development guidelines, Android/Flutter best practices).
        *   Configuration (e.g., country-specific settings, API keys, business rule parameters) should be separated from code (e.g., Odoo config files, environment variables, `ir.config_parameter`, dedicated Odoo models for settings) to allow for easier country-specific adaptations and deployments.
        *   CI/CD pipelines should facilitate automated testing (unit tests, integration tests) and deployment, reducing manual intervention and errors.
        *   Clear version control practices (Git with semantic versioning, feature branching e.g., GitFlow, regular merging) must be followed.

    **4.7. Portability Requirements**
        *   The core Odoo platform should be deployable on various infrastructures (on-premise servers running Linux, cloud VMs) as per country requirements, facilitated by Docker or equivalent containerization. [Specifying Linux as common OS for Odoo].
        *   The Android mobile app must be compatible with a wide range of common Android devices (smartphones and tablets, targeting Android 8.0 Oreo / API level 26 and above). [Reiterating Android version].

    **4.8. Localization Requirements**
        *   All user-facing text in web and mobile interfaces, including dynamic form elements, must be localizable using standard Odoo translation mechanisms (.po files) and Android string resources (or equivalent for cross-platform mobile).
        *   Support for multiple languages per country instance, configurable by administrators (Odoo language settings).
        *   Support for RTL (Right-to-Left) scripts if required by any participating country (Odoo's web client has some RTL support; mobile app needs specific RTL handling if using native components or Flutter widgets that support it).
        *   Date, time, and number formats should be adaptable to local conventions (Odoo generally handles this based on language settings; mobile app may need specific formatting libraries).

    **4.9. Data Management Requirements**
        *   **Data Privacy & Compliance:** The system must be designed to comply with identified data protection and privacy laws for each target country (as per section 1.4, 2.5). This includes features for managing farmer consent for data collection, processing, and sharing (e.g., specific fields, audit trails for consent changes, clear privacy notices, versioning of consent, withdrawal of consent). The system must support data subject rights as mandated by specific country regulations, including mechanisms for farmers to request access to their data, request corrections, and, where applicable, request data erasure or restriction of processing. Workflows within Odoo will be designed to facilitate these requests.
        *   **Data Retention & Archiving:** Configurable data retention policies for all major data entities (farmer profiles, household data, plot information, dynamic form submissions, audit logs) will be implemented based on legal, operational, and country-specific requirements. An archiving strategy for historical data (e.g., moving inactive records to separate tables/database or cold storage, with defined retrieval processes) will be developed to ensure long-term system performance and manage storage costs, while maintaining accessibility for reporting if needed. The process for defining and approving these policies will be agreed with FAO and national counterparts. [Adding detail on archiving methods].
        *   **De-duplication:** A robust de-duplication strategy as outlined in B.2.1.1, including both real-time checks and batch processing capabilities within Odoo, with configurable parameters for matching logic and merge rules.
        *   **Data Integrity:** Mechanisms to ensure data accuracy and consistency, including input validation (Odoo model constraints, API validation), referential integrity (enforced by PostgreSQL foreign keys via Odoo ORM), and controlled vocabularies (Odoo selection fields, many2one relations to master data models) where appropriate.
        *   **Data Ownership:** Each participating country will retain full ownership of all data collected and managed within its respective DFR instance. The DFR platform architecture will ensure strict data segregation between country instances.

**5. Interface Requirements**

    **5.1. User Interfaces**
        *   **Web Admin Portal (Odoo Backend):** For administrators, supervisors. Must be responsive for desktop and tablet use, leveraging Odoo's standard web client (XML views, JavaScript/OWL framework).
        *   **Mobile Enumerator App (Android):** Native (Kotlin/Java) or cross-platform (Flutter/Dart recommended) application for enumerators. Optimized for smartphones and tablets (various screen sizes and orientations) used in field conditions. Adherence to platform-specific UI/UX guidelines (e.g., Android Material Design) to ensure a familiar and intuitive experience for enumerators.
        *   **Farmer Self-Service Portal (Odoo Website/Portal):** Public-facing web interface for farmers, built using Odoo's Website module. Must be mobile-responsive and accessible (WCAG 2.1 AA).

    **5.2. API Interfaces**
        *   **DFR Core APIs:** Secure RESTful APIs for system integrations (as detailed in B.2.2.5).
            *   Protocol: HTTPS (TLS 1.2+)
            *   Data Format: JSON
            *   Authentication: OAuth2/JWT
            *   Documentation: OpenAPI Specification v3.x (e.g., Swagger UI endpoint).
        *   **Third-Party Integrations:** The system must be capable of consuming APIs from external systems (e.g., ID validation, weather services - typically REST/JSON or SOAP/XML) and exposing data via its own APIs. Specific protocols and formats will depend on the external systems identified. Adapters or connectors might be needed within Odoo for non-REST/JSON services.

**6. Data Requirements**

    **6.1. Data Model**
        *   **Core Farmer Registry:** Based on the common data schema to be finalized with FAO and national counterparts. Key entities include Farmer, Household, HouseholdMember, Farm, Plot - implemented as Odoo models (Python classes inheriting `models.Model`). Relationships (one2many, many2one, many2many) will be defined using Odoo ORM fields. [Adding Odoo specific implementation details].
        *   **Dynamic Forms:** Form definitions (structure, fields, validation, logic - likely stored as JSON in an Odoo text field or structured Odoo models) and submitted form data linked to Farmer UIDs (stored in separate Odoo models dynamically created or linked to a generic submission model).
        *   **User and Role Data:** For RBAC, using Odoo's `res.users`, `res.groups`, `ir.model.access`, and `ir.rule` models.
        *   **Audit Logs and Change History:** Detailed records of system activities and data modifications, leveraging Odoo's `mail.thread` (chatter) for record changes and custom logging models for specific events (e.g., login attempts, sync events).
        *   **Geospatial Data:** Plot location coordinates (latitude, longitude) stored as float fields. If advanced geospatial queries (e.g., proximity, area calculations within database) are required, PostgreSQL with PostGIS extension should be considered, and Odoo fields adapted accordingly. [Reiterating PostGIS for geospatial data].

    **6.2. Data Migration** (Refer to section 3.6.2 for detailed strategy)
        *   The system must provide tools (as per B.2.2.6 - Odoo's standard import/export, potentially extended with custom Python scripts/Odoo modules for complex transformations or large volumes) for migrating legacy farmer data from various sources (CSV/XLSX, databases).
        *   This includes data validation (pre-migration profiling, Odoo model constraints during load, post-migration reconciliation), error reporting (Odoo's import feedback, custom logs for script-based migrations), and field mapping capabilities.

    **6.3. Data Backup and Recovery**
        *   Automated daily backups of each country's PostgreSQL database (using `pg_dump` or `pg_basebackup` with WAL archiving for Point-In-Time Recovery - PITR) and critical system files (Odoo custom modules, configuration files, filestore if used extensively). [Adding specific PostgreSQL backup tools and PITR].
        *   Defined procedures for data restoration to meet RTO/RPO targets, including full and partial restore scenarios. Restoration procedures must be documented and tested regularly as part of DR drills.
        *   Backup retention policy to be defined (e.g., daily for 7 days, weekly for 4 weeks, monthly for 6 months, annual for 1 year), stored securely (e.g., offsite or in a separate cloud storage region). [Adding example retention policy and secure storage].

    **6.4. Data Confidentiality and Integrity**
        *   PII must be handled with strict confidentiality, accessible only to authorized users based on their roles and permissions (enforced by Odoo RBAC). Consider encryption at rest for highly sensitive PII fields in the database (e.g., using PostgreSQL `pgcrypto`) if mandated by specific country regulations or data privacy impact assessments, beyond standard Odoo access controls. [Adding `pgcrypto` as an option for field-level encryption].
        *   Measures to ensure data integrity throughout its lifecycle (capture, storage, processing, transmission) including input validation, referential integrity (PostgreSQL foreign keys), Odoo model constraints, and audit trails.