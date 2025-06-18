# DFR System Documentation and Training Materials - Software Design Specification

## 1. Introduction

### 1.1 Purpose
This document outlines the Software Design Specification (SDS) for the DFR System Documentation and Training Materials repository. This repository serves as the central knowledge base for the Digital Farmer Registry (DFR) project, encompassing all technical documentation, user-facing guides, training resources, and governance frameworks. The specifications herein will guide the creation and organization of these materials.

### 1.2 Scope
The scope of this SDS is limited to the `DFR_SYSTEM_DOCS_TRAINING` repository. It covers the structure, content, and configuration of the documentation portal and all associated materials. This includes architectural blueprints, design specifications, API documentation, user manuals, training scripts, and knowledge transfer kits.

### 1.3 Overview of the Documentation Portal
The DFR Documentation Portal will be a static website generated using MkDocs. It will provide a structured, navigable, and searchable interface for all project documentation and training resources. The primary language for source documents is English, with provisions for multilingual outputs based on translated source files or post-generation translation processes.

## 2. General Design and Configuration

### 2.1 Documentation Tool
*   **Tool:** MkDocs 1.6.0
*   **Source Language:** Markdown (primarily CommonMark with GFM extensions where supported by MkDocs and plugins)
*   **Build Environment:** Python 3.11.9 (for MkDocs and plugins)

### 2.2 `mkdocs.yml` Configuration Details
The `mkdocs.yml` file is the primary configuration for the MkDocs static site generator.

yaml
# mkdocs.yml
site_name: 'Digital Farmer Registry (DFR) Documentation Portal'
site_url: 'https://example.com/dfr-docs/' # Placeholder, to be updated with actual URL
site_author: 'DFR Project Team'
site_description: 'Comprehensive documentation and training materials for the Digital Farmer Registry (DFR) project.'

repo_name: 'DFR_SYSTEM_DOCS_TRAINING' # Or actual Git repository name
repo_url: 'https://github.com/example/dfr-docs-repo' # Placeholder, to be updated

copyright: 'Copyright © DFR Project Team'

theme:
  name: 'material'
  language: 'en' # Default language
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.footer
    - search.suggest
    - search.highlight
    - content.code.annotate
    - content.tooltips
  palette:
    # Palette toggle for light/dark mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: 'blue'
      accent: 'indigo'
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: 'blue'
      accent: 'indigo'
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: 'Roboto'
    code: 'Roboto Mono'
  logo: 'assets/images/dfr_logo.png' # Placeholder for DFR logo
  favicon: 'assets/images/dfr_favicon.ico' # Placeholder for DFR favicon

plugins:
  - search: # Enables client-side search
      lang: # Add languages here as translations become available for search index
        - en
  - awesome-pages: # For cleaner navigation management in mkdocs.yml or separate .pages files
      collapse_single_pages: true
  - mermaid2: # For rendering Mermaid diagrams
      # arguments: {'theme': 'forest'} # Example theme
  - print-site: # For generating a printable version of the site or sections
      add_to_navigation: true
  # - i18n: # If mkdocs-static-i18n plugin is used for multilingual content
  #     docs_structure: suffix # e.g., page.md, page.fr.md
  #     languages:
  #       - locale: en
  #         default: true
  #         name: English
  #       - locale: fr_CK
  #         name: French (Cook Islands) # Example, update as per project needs
  #       # Add other supported languages from project config: sm_WS, to_TO, en_SB, bi_VU

extra_css:
  - 'assets/stylesheets/extra.css' # For custom styling

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - admonition
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - footnotes
  - toc:
      permalink: true # Adds a permalink to headings

# Navigation - this will be a detailed representation of the docs/ directory structure
# The 'awesome-pages' plugin can simplify this by inferring from directory structure or using .pages files.
# Example structure if not using awesome-pages for full control:
nav:
  - 'Home': 'index.md'
  - 'Overview': 'README.md'
  - 'Glossary': 'glossary.md'
  - 'Architecture':
    - 'Overview': 'architecture/overview.md'
    - 'Architectural Decision Records':
      - 'ADR-001: Odoo Version Choice': 'architecture/adr/ADR-001-Choice-of-Odoo-Version.md'
      # ... other ADRs
    - 'Data Model':
      - 'Core Entities Schema': 'architecture/data-model/core-entities-schema.md'
      # ... other data model docs
    - 'Deployment Strategy':
      - 'Hosting & Deployment Strategy': 'architecture/deployment-strategy/hosting-deployment-strategy.md'
      # ... other deployment docs
  - 'Codebase Governance':
    - 'Framework': 'codebase-governance/framework.md'
  - 'Standards':
    - 'Documentation Standards': 'standards/documentation-standards.md'
  - 'Licensing':
    - 'Open Source Declaration': 'licensing/open-source-declaration.md'
  - 'User Manuals':
    - 'Administrator Manual':
      - 'Introduction': 'user-manuals/administrator-manual/index.md'
      - 'User Management': 'user-manuals/administrator-manual/01-user-management.md'
      - 'Dynamic Form Builder': 'user-manuals/administrator-manual/02-dynamic-form-builder.md'
      # ... other admin manual sections
    - 'Enumerator Manual':
      - 'Mobile App Overview': 'user-manuals/enumerator-manual/mobile-app-overview.md'
      - 'Farmer Registration (Mobile)': 'user-manuals/enumerator-manual/01-farmer-registration-mobile.md'
      # ... other enumerator manual sections
    - 'Support Team Manual':
      - 'Introduction': 'user-manuals/support-team-manual/index.md'
      # ... other support manual sections
  - 'Developer Guides':
    - 'Codebase Onboarding':
      - 'Odoo Modules Overview': 'developer-guides/codebase-onboarding/odoo-modules-overview.md'
      - 'Mobile App Architecture': 'developer-guides/codebase-onboarding/mobile-app-architecture.md'
      # ... other onboarding sections
    - 'API Developer Guide': 'developer-guides/api-developer-guide.md' # Link to OpenAPI/Swagger or embedded content
    - 'CI/CD Pipeline': 'developer-guides/ci-cd-pipeline.md'
  - 'Training Materials':
    - 'Quick Start Guides':
      - 'Admin Quick Start': 'training-materials/quick-start-guides/admin-quick-start.md'
      # ... other quick start guides
    - 'Video Scripts & Assets':
      - 'Administrator Videos':
        - 'User Management Script': 'training-materials/scripts-assets-for-videos/admin-videos/01-user-management-script.md'
        # ... other admin video scripts
      - 'Enumerator Videos':
        # ... enumerator video scripts
    - 'Helpdesk SOPs': 'training-materials/helpdesk-sop/index.md'
    - 'Change Management Toolkit': 'training-materials/change-management-toolkit/index.md'
  - 'Knowledge Transfer Kit':
    - 'Overview': 'knowledge-transfer-kit/index.md'
    - 'Exit Checklist': 'knowledge-transfer-kit/exit-checklist.md'
    - 'Final Reports':
      - 'Data Migration Report (Template)': 'knowledge-transfer-kit/final-reports/data-migration-report-template.md'
    - 'Credential & Config Matrix (Template)': 'knowledge-transfer-kit/credential-config-matrix-template.md'

extra:
  social: # Example, adjust as needed
    - icon: fontawesome/brands/github
      link: 'https://github.com/example' # Placeholder
  version:
    provider: mike # If using mike for versioning documentation
    default: latest

# Required for mkdocs-static-i18n if used
# languages:
#   en: English
#   fr_CK: Français (Îles Cook)
#   sm_WS: Gagana Samoa
#   to_TO: Lea faka-Tonga
#   en_SB: English (Solomon Islands) # Assuming English is primary for SI, adjust if Pidgin or other
#   bi_VU: Bislama

# Default values from repository configuration
# DocTool: MkDocs
# DefaultLanguage: en
# SupportedLanguages: [en, fr_CK, sm_WS, to_TO, en_SB, bi_VU]
# RepositoryVersion: 1.0.0
# ProjectName: Digital Farmer Registry (DFR) Documentation
# OutputFormats: [HTML, PDF (via plugin if available)]


### 2.3 Language Support
*   **Primary Language:** English (en).
*   **Supported Languages:** As defined in the project configuration (`en`, `fr_CK`, `sm_WS`, `to_TO`, `en_SB`, `bi_VU`).
*   **Translation Management:** Source files will be primarily in English. Translated versions of Markdown files will be maintained (e.g., using a suffix convention like `page.fr_CK.md` if `mkdocs-static-i18n` plugin is used, or separate directory structures per language). The MkDocs configuration will be adjusted to build sites for each supported language or provide a language switcher. Theme-level string translations will rely on the Material for MkDocs theme's i18n capabilities.

### 2.4 Documentation Versioning
*   Documentation will be versioned in conjunction with major software releases of the DFR platform.
*   The `mike` MkDocs plugin is recommended for managing and deploying multiple versions of the documentation.
*   Each version will be a snapshot of the `docs/` directory at the time of the software release.

## 3. Documentation Portal Structure and Content

The documentation portal will be organized into logical sections corresponding to the directories defined in the `file_structure_json`.

### 3.1. Root Level (`docs/`)

*   **`index.md` (Homepage)**
    *   **Purpose:** Main landing page for the documentation portal.
    *   **Key Content:** Welcome message, brief introduction to DFR, purpose of the portal, highlights of key sections, quick links to important guides (e.g., Administrator Manual, Enumerator Mobile App Guide).
    *   **Target Audience:** All DFR stakeholders.
    *   **Req IDs:** C.1.4
*   **`README.md` (Repository Overview)**
    *   **Purpose:** To provide an initial guide and overview for anyone accessing the documentation *repository* (distinct from the portal homepage).
    *   **Key Content:** Overview of this documentation repository, structure of the `docs/` directory, instructions for building the documentation locally (if applicable), contribution guidelines (if any), link to the hosted portal.
    *   **Target Audience:** Developers, documentation contributors, technical stakeholders.
    *   **Req IDs:** C.1.4
*   **`glossary.md`**
    *   **Purpose:** To ensure consistent understanding and use of terminology.
    *   **Key Content:** Alphabetically sorted list of key terms, acronyms (DFR, API, KYC, GPS, RTO, RPO, SOP, etc.), and domain-specific language with clear definitions in the DFR context.
    *   **Target Audience:** All DFR stakeholders.
    *   **Req IDs:** C.1.1

### 3.2. Architecture Documentation (`docs/architecture/`)
This section details the DFR system's architecture.
*Req IDs: E.1.4, A.3.3, A.3.4*

*   **`overview.md`**
    *   **Purpose:** Foundational understanding of DFR system architecture.
    *   **Key Content:** Introduction, architectural style (Modular Monolith with Odoo), key components (Odoo Backend, Mobile App, API Layer, Farmer Portal), high-level interaction diagrams (e.g., C4 model Context/Container diagrams), technology stack summary, architectural principles (scalability, security, maintainability).
    *   **Target Audience:** Technical stakeholders, developers, administrators.
*   **`adr/` (Architectural Decision Records)**
    *   **Purpose:** Document significant architectural decisions, their rationale, and consequences.
    *   **Key Content:** Individual Markdown files for each ADR, following a standard template (Title, Status, Context, Decision, Consequences, Alternatives).
        *   Example: `ADR-001-Choice-of-Odoo-Version.md`: Rationale for Odoo 18.0 Community, benefits, challenges.
    *   **Target Audience:** Technical stakeholders, developers.
*   **`data-model/`**
    *   **Purpose:** Comprehensive reference for the DFR data model.
    *   **Key Content:**
        *   `core-entities-schema.md`: Detailed schema for core Odoo models (Farmer, Household, Plot, etc.) - model name, purpose, fields (name, type, constraints, description), relationships, key business rules. May include embedded or linked ERDs.
        *   `dynamic-forms-schema.md`: Schema for dynamic form definitions and submissions.
        *   `audit-log-schema.md`: Schema for audit log entries.
    *   **Target Audience:** Developers, data administrators, technical analysts.
*   **`deployment-strategy/`**
    *   **Purpose:** Guide infrastructure setup and deployment.
    *   **Key Content:**
        *   `hosting-deployment-strategy.md`: Supported hosting environments, hardware/OS specs for on-premise, cloud service recommendations, Docker strategy, three-tier environment overview, backup strategy (frequency, retention, tools), DR approach (RTO/RPO guidelines), CI/CD overview.
        *   `country-specific-deployment-plan-template.md`: A template for creating deployment plans for each country, to be filled during WP-B.
    *   **Target Audience:** IT teams, administrators, technical project managers.

### 3.3. Codebase Governance (`docs/codebase-governance/`)
*Req IDs: A.3.2*

*   **`framework.md`**
    *   **Purpose:** Establish rules for managing the shared DFR codebase.
    *   **Key Content:** Core codebase architecture (shared vs. country-specific modules/configs), branching strategy (e.g., GitFlow), versioning policy (Semantic Versioning 2.0.0), maintenance plan, contribution model (issue tracker, PR process), update/deployment policy for country instances, guidelines for country-specific extensions.
    *   **Target Audience:** Developers, technical leads, project managers.

### 3.4. Standards (`docs/standards/`)
*Req IDs: A.3.5*

*   **`documentation-standards.md`**
    *   **Purpose:** Ensure consistency and quality in all project documentation.
    *   **Key Content:** Code commenting standards (inline, function/class docstrings for Python, Java/Kotlin, Dart, JS; XML comments for Odoo views), README.md structure, API documentation standards (OpenAPI 3.x), developer guide generation tools (Sphinx, MkDocs), documentation versioning, style guide (tone, language, formatting).
    *   **Target Audience:** All project contributors (developers, technical writers).
*   **`coding-standards.md`**
    *   **Purpose:** Define coding conventions for DFR development.
    *   **Key Content:** PEP 8 for Python, Odoo development guidelines, Android (Kotlin/Java) best practices, Flutter/Dart best practices, JavaScript coding standards (if applicable), frontend framework (OWL) conventions. Naming conventions, error handling patterns, security coding practices.

### 3.5. Licensing (`docs/licensing/`)
*Req IDs: A.3.6*

*   **`open-source-declaration.md`**
    *   **Purpose:** Provide transparency on software licensing and ensure compliance.
    *   **Key Content:** Statement of DFR's primary license (MIT or Apache 2.0). Table of all third-party open-source components (name, version, license, link). Confirmation of license compatibility review. This document will be tightly linked with the Software Bill of Materials (SBOM).
    *   **Target Audience:** Legal teams, FAO, national counterparts, developers.

### 3.6. User Manuals (`docs/user-manuals/`)
Modular, role-based, and multilingual user guides.
*Req IDs: B.3.B1.13, C.1.1*

*   **`administrator-manual/`**
    *   **Target Audience:** National Administrators, Super Administrators.
    *   **`index.md`**: Overview and Table of Contents.
    *   **Sections (examples):**
        *   `01-introduction.md`: Role overview, dashboard navigation.
        *   `02-user-management.md`: Creating users, assigning roles, password policies, MFA setup.
        *   `03-dynamic-form-builder.md`: Designing forms, field types, validation, conditional logic, versioning.
        *   `04-business-rules-config.md`: Workflow configuration, de-duplication rules, status management.
        *   `05-notification-system.md`: Template management, trigger configuration, gateway setup.
        *   `06-analytics-reporting.md`: Accessing dashboards, generating reports, custom views, data export.
        *   `07-data-management.md`: Bulk import/export, data migration validation.
        *   `08-localization-settings.md`: Managing language packs, country-specific settings.
        *   `09-system-monitoring-logs.md`: Viewing audit logs, basic system health.
        *   `10-portal-management.md`: Enabling/disabling Farmer Self-Service Portal.
*   **`enumerator-manual/`**
    *   **Target Audience:** Enumerators.
    *   **`index.md`**: Overview and Table of Contents.
    *   **`mobile-app-overview.md`**: Installation, login, navigation, offline mode, sync process, language selection.
    *   **Sections (examples):**
        *   `01-farmer-search.md`: Searching existing farmers (UID, name, QR).
        *   `02-farmer-registration-mobile.md`: Step-by-step new farmer registration.
        *   `03-household-management.md`: Adding/editing household members.
        *   `04-farm-plot-management.md`: Adding/editing farms and plots, GPS capture.
        *   `05-dynamic-forms-mobile.md`: Accessing and completing dynamic forms.
        *   `06-data-synchronization.md`: How and when to sync, troubleshooting common sync issues.
        *   `07-troubleshooting-mobile.md`: Common mobile app issues and solutions.
*   **`support-team-manual/`**
    *   **Target Audience:** National and Central Support Teams.
    *   **`index.md`**: Overview and Table of Contents.
    *   **Sections (examples):**
        *   `01-ticketing-sop.md`: Ticket logging, prioritization, SLAs.
        *   `02-common-issues-web.md`: Troubleshooting Odoo admin portal issues.
        *   `03-common-issues-mobile.md`: Advanced mobile app troubleshooting.
        *   `04-data-quality-checks.md`: Procedures for basic data quality verification.
        *   `05-escalation-procedures.md`: Escalation matrix and process.
        *   `06-user-account-support.md`: Assisting with account lockouts, MFA issues.
*   **`farmer-portal-guide/`** (if distinct from informational content on the portal itself)
    *   **Target Audience:** Farmers.
    *   **`index.md`**: How to use the self-service portal, pre-registration steps, accessing information.

### 3.7. Developer Guides (`docs/developer-guides/`)
Technical documentation for developers.
*Req IDs: D.1.4, E.1.4*

*   **`codebase-onboarding/`**
    *   **Purpose:** Help new developers understand the DFR codebase.
    *   **`odoo-modules-overview.md`**: DFR Odoo addon structure, purpose of custom modules, key models, development environment setup, coding standards specific to DFR Odoo, debugging.
    *   `mobile-app-architecture.md`: Mobile app (Android native or Flutter) architecture, project structure, key components, state management, data layer, development environment setup, coding standards.
    *   `setup-development-environment.md`: Step-by-step guide for setting up local dev environments for both Odoo backend and Mobile app.
*   **`api-developer-guide.md`**
    *   **Purpose:** Guide for integrating external systems with DFR APIs.
    *   **Key Content:** Introduction to DFR APIs, authentication mechanisms (OAuth2/JWT details), link to live OpenAPI/Swagger documentation (or embedded content), common request/response examples, error codes, rate limiting, best practices for API clients.
*   **`ci-cd-pipeline.md`**
    *   **Purpose:** Explain the automated build, test, and deployment process.
    *   **Key Content:** Overview of CI/CD workflow, tools used (Jenkins, GitLab CI, GitHub Actions), pipeline script configurations (e.g., Jenkinsfile), automated testing procedures, deployment steps to staging/production, troubleshooting pipeline issues.
*   **`testing-strategy.md`**
    *   **Purpose:** Outline the approach to testing the DFR system.
    *   **Key Content:** Levels of testing (unit, integration, system, UAT), tools used, test environment setup, how to write and run tests for Odoo modules and mobile app.

### 3.8. Training Materials (`docs/training-materials/`)
Source files for training sessions and resources.
*Req IDs: C.1.1*

*   **`quick-start-guides/`**
    *   **Purpose:** Printable, concise guides for common tasks by role.
    *   **Files (examples):** `admin-quick-start.md`, `enumerator-mobile-quick-start.md`.
*   **`scripts-assets-for-videos/`**
    *   **Purpose:** Source scripts and asset lists for screencast training videos.
    *   **Structure:** Subdirectories per role (e.g., `admin-videos/`, `enumerator-videos/`).
    *   **Files (examples):** `admin-videos/01-user-management-script.md`, `enumerator-videos/01-farmer-registration-script.md`. Each script includes scene descriptions, narration, and on-screen actions.
*   **`helpdesk-sop/`**
    *   **`index.md`**: Helpdesk SOPs, troubleshooting handbook, escalation matrix (can link to sections in Support Team Manual).
*   **`change-management-toolkit/`**
    *   **`index.md`**: Communication templates (SMS, email, posters), adoption monitoring tips, local support guidance.
*   **`tot-program/`**
    *   **`trainer-guide.md`**: Guide for national trainers, sample agendas, presentation scripts, practice exercises.
    *   **`participant-workbook.md`**: Workbook for ToT participants.

### 3.9. Knowledge Transfer Kit (`docs/knowledge-transfer-kit/`)
Documents for the final handover.
*Req IDs: D.1.6, E.1.4*

*   **`index.md`**: Overview of the KT kit contents.
*   **`exit-checklist.md`**: Comprehensive checklist for asset and knowledge handover.
*   **`final-reports/`**
    *   `data-migration-report-template.md`: Template for country-specific data migration final reports.
    *   `lessons-learned-template.md`: Template for documenting lessons learned.
*   **`credential-config-matrix-template.md`**: Template for national teams to manage credentials and configurations.
*   **`handover-certificate-template.md`**: Template for the Ownership Transfer Certificate.

### 3.10. Assets (`docs/assets/`)
Shared assets for the documentation.

*   **`images/`**
    *   **Purpose:** Store diagrams, screenshots, logos used across the documentation.
    *   **Files (examples):** `dfr_architecture_overview.png`, `dfr_logo.png`, `dfr_favicon.ico`, screenshots of UI elements.
*   **`stylesheets/`**
    *   **`extra.css`**: Custom CSS to override or enhance the MkDocs theme.
*   **`downloads/`**
    *   **Purpose:** Store printable versions of guides, templates, or other downloadable resources.
*   **`videos/`** (If not hosted externally)
    *   **Purpose:** Store final MP4 training videos. Links preferred if videos are hosted on a streaming platform.

## 4. Content Generation and Maintenance

### 4.1 Source Format
All documentation will be primarily written in Markdown. reStructuredText might be used if Sphinx is chosen for certain advanced documentation features, but Markdown is preferred for general use with MkDocs.

### 4.2 Tools
*   **Primary Tool:** MkDocs with Material for MkDocs theme and selected plugins.
*   **Diagrams:** Mermaid.js (rendered via `mkdocs-mermaid2` plugin or natively by theme) for flowcharts, sequence diagrams, ERDs where appropriate. Static images for complex diagrams.
*   **Version Control:** Git, hosted on a platform like GitHub or GitLab.

### 4.3 Contribution Workflow
(To be detailed further in the Codebase Governance Framework)
1.  Issues for new documentation or updates are tracked in an issue tracker.
2.  Contributors create feature branches for their changes.
3.  Changes are written in Markdown and committed.
4.  Pull/Merge Requests are created for review.
5.  Reviewers check for accuracy, clarity, and adherence to standards.
6.  Approved changes are merged into the main development branch.
7.  The documentation portal is rebuilt and deployed.

### 4.4 Update Strategy
*   Documentation will be updated iteratively alongside software development.
*   Major documentation updates will align with software releases (Semantic Versioning).
*   A designated documentation owner or team will be responsible for ensuring accuracy and completeness.
*   Regular reviews of documentation will be scheduled.

## 5. Deployment and Hosting

### 5.1 Generation
The documentation portal will be a static HTML website generated by MkDocs using the `mkdocs build` command.

### 5.2 Hosting Options
*   GitHub Pages (if the repository is on GitHub).
*   GitLab Pages (if the repository is on GitLab).
*   Dedicated web server (e.g., Nginx serving the static files).
*   Cloud storage with static website hosting (e.g., AWS S3, Azure Blob Storage).
The chosen hosting solution must be accessible to all target users and support HTTPS.

## 6. Requirements Traceability
The documentation structure and content outlined above directly address the requirements mapped to this repository, including:
*   **A.3 (Overall Technical Documentation):** Covered by sections on Architecture, Developer Guides, Standards, Licensing, and KT Kit.
*   **A.3.5 (Documentation Standards Guide):** Directly addressed by `standards/documentation-standards.md`.
*   **B.3.B1.13 (Admin manuals, user guides, SOPs):** Covered by the `user-manuals/` section.
*   **C.1.1 (Modular, multilingual training materials by role):** Addressed by `training-materials/` and the overall multilingual approach.
*   **C.1.4 (Hosted documentation wiki/portal):** This entire SDS defines the plan for such a portal.
*   **D.1.4 (Updated Codebase Onboarding Guide and API Developer Documentation):** Covered by `developer-guides/`.
*   **D.1.6 (Final Knowledge Transfer Kit):** Addressed by `knowledge-transfer-kit/`.
*   **E.1.4 (Final comprehensive technical documentation set):** This SDS plans for the creation of this set.

Individual Markdown files will also internally reference specific SRS requirement IDs they address where applicable.

## 7. Output Formats and Accessibility

*   **Primary Output:** HTML (web portal).
*   **Secondary Output:** PDF (using `mkdocs-print-site-plugin` or similar for printable versions of key manuals or sections).
*   **Accessibility:** The chosen MkDocs theme (Material for MkDocs) has good accessibility support. Efforts will be made to ensure content (e.g., use of alt text for images, proper heading structures) also adheres to WCAG 2.1 Level AA guidelines where feasible. Videos will be scripted, and providing subtitles/transcripts will be a goal for enhanced accessibility. Materials will be designed to be accessible offline and in low-bandwidth formats as per REQ-TSE-012 (e.g., downloadable PDFs, compressed videos).