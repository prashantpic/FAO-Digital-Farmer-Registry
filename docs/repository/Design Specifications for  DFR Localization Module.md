# Software Design Specification: DFR Localization Module (DFR_MOD_LOCALIZATION)

## 1. Introduction

### 1.1 Purpose
This document outlines the software design for the DFR Localization Module (`dfr_localization`). This module is responsible for managing all DFR-specific localization assets, primarily the GNU Gettext Portable Object (`.po`) translation files. It leverages Odoo's built-in internationalization (i18n) framework to provide multilingual support for all custom Digital Farmer Registry (DFR) Odoo modules. This includes UI elements, dynamic form content, notifications, and other user-facing text.

### 1.2 Scope
The scope of this module includes:
*   Defining the structure for storing translation files (`.po` files) for various languages.
*   Providing a master translation template (`.pot` file) consolidating all translatable strings from all DFR custom modules.
*   Including placeholder `.po` files for target languages (English, French, and languages for the five Pacific Island Countries: Samoan, Tongan, Bislama, Cook Islands Māori, Pijin).
*   Ensuring that this module, when installed, makes these translations available to the Odoo system.
*   Configuring dependencies on all other DFR custom modules to enable comprehensive extraction of translatable strings.

This module does *not* implement custom user interfaces for translation management; it relies on Odoo's standard tools ("Load a Translation", language settings). The actual translation of strings into target languages is an external process; this module provides the framework and files for those translations.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **DFR:** Digital Farmer Registry
*   **i18n:** Internationalization
*   **L10n:** Localization
*   **PO File:** Portable Object file, a standard file format used by GNU Gettext for localization.
*   **POT File:** Portable Object Template file, a master template for PO files, containing all translatable strings.
*   **Odoo:** Open Source ERP system used as the base for DFR.
*   **PIC:** Pacific Island Countries
*   **MIT:** Massachusetts Institute of Technology (License)
*   **Apache 2.0:** Apache License, Version 2.0

## 2. System Overview
The `dfr_localization` module is a crucial component of the DFR platform, acting as a central repository for all translation files related to custom DFR functionality. It integrates seamlessly with Odoo's i18n system. By declaring dependencies on all other DFR-specific Odoo modules (e.g., `dfr_common_core`, `dfr_farmer_registry`, `dfr_dynamic_forms`, `dfr_notifications_module`), it allows Odoo's translation tools to scan these modules and aggregate all translatable strings into a single master `.pot` file managed within `dfr_localization`.

When a specific language (e.g., French, Samoan) is enabled in an Odoo instance, Odoo will look for a corresponding `.po` file (e.g., `fr.po`, `sm.po`) within the `i18n` directory of installed modules, including `dfr_localization`. This module will provide these `.po` files, enabling the DFR user interface and content to be displayed in the selected language.

The module itself has minimal Python code and primarily consists of the `__manifest__.py` file and the `i18n` directory containing the translation files.

## 3. Module Design

### 3.1 `__init__.py`
*   **Path:** `dfr_addons/dfr_localization/__init__.py`
*   **Purpose:** Standard Odoo module Python package initializer.
*   **Logic:** This file will be empty or contain only `pass`.
    python
    # -*- coding: utf-8 -*-
    # Part of Odoo. See LICENSE file for full copyright and licensing details.
    pass
    
*   **Requirements Met:** REQ-LMS-001

### 3.2 `__manifest__.py`
*   **Path:** `dfr_addons/dfr_localization/__manifest__.py`
*   **Purpose:** Declares the module's metadata, dependencies, and configuration for Odoo. This is critical for ensuring Odoo's i18n system correctly processes all translatable strings from the entire DFR custom application suite.
*   **Key Contents:**
    *   `name`: "DFR Localization Pack"
    *   `version`: "18.0.1.0.0" (or current version)
    *   `summary`: "Provides translations for all Digital Farmer Registry (DFR) custom modules."
    *   `description`: """This module centralizes localization assets for the DFR platform, including .po files for multiple languages. It depends on all other DFR modules to ensure comprehensive translation coverage."""
    *   `author`: "FAO & SSS-AI"
    *   `license`: "MIT" (or "Apache-2.0", to be finalized as per REQ-CM-001)
    *   `category`: "Localization"
    *   `depends`:
        *   `'base'`
        *   `'dfr_common_core'` (Example name, actual module names for DFR Common Core)
        *   `'dfr_farmer_registry'` (Example name, actual module names for Farmer Registry Engine)
        *   `'dfr_dynamic_forms'` (Example name, actual module names for Dynamic Form Engine)
        *   `'dfr_notifications_module'` (Example name, actual module names for Notification System)
        *   `'dfr_api_management'` (Example name, actual module names for API Management)
        *   `'dfr_admin_tools'` (Example name, actual module names for Admin Tools)
        *   `'dfr_self_service_portal'` (Example name, actual module names for Farmer Self-Service Portal)
        *   *(Add all other custom DFR Odoo modules here)*
    *   `data`: This key will generally be empty. `.po` files are loaded automatically by Odoo from the `i18n` directory when a language is installed or modules are updated.
    *   `installable`: `True`
    *   `application`: `False`
    *   `auto_install`: `False` (or `True` if it should be installed automatically when its dependencies are installed)

*   **Logic Description:** The `depends` list is paramount. It instructs Odoo that this module is related to others. When Odoo's i18n tools (e.g., for exporting terms to a `.pot` file or loading translations) are run in the context of `dfr_localization`, they will also scan all modules listed in `depends` for translatable strings (strings wrapped in `_()`, strings in XML views, model field labels, etc.).
*   **Requirements Met:** REQ-LMS-001, REQ-LMS-002, REQ-LMS-004, REQ-PCA-018

    python
    # -*- coding: utf-8 -*-
    {
        'name': "DFR Localization Pack",
        'version': '18.0.1.0.0',
        'summary': "Provides translations for all Digital Farmer Registry (DFR) custom modules.",
        'description': """
    This module centralizes localization assets for the DFR platform,
    including .po files for multiple languages. It depends on all other
    DFR modules to ensure comprehensive translation coverage.
        """,
        'author': "FAO & SSS-AI",
        'license': 'MIT', # Or 'Apache-2.0'
        'category': 'Localization',
        'depends': [
            'base',
            # --- DFR Core Modules ---
            'dfr_common_core', # Placeholder - replace with actual DFR module name
            # --- DFR Functional Modules ---
            'dfr_farmer_registry', # Placeholder
            'dfr_dynamic_forms', # Placeholder
            'dfr_notifications_module', # Placeholder
            'dfr_api_management', # Placeholder
            'dfr_admin_tools', # Placeholder
            'dfr_self_service_portal', # Placeholder
            # ... Add ALL other custom DFR Odoo modules here
        ],
        'data': [
            # Typically empty for a pure localization module if .po files are in i18n/
            # and no specific views/data are defined by this module itself.
        ],
        'installable': True,
        'application': False,
        'auto_install': False, # Or True, depending on desired behavior
    }
    

### 3.3 `i18n` Directory Structure and Files
This directory contains all translation assets.

#### 3.3.1 `i18n/dfr_localization.pot`
*   **Path:** `dfr_addons/dfr_localization/i18n/dfr_localization.pot`
*   **Purpose:** Master Portable Object Template (POT) file. It contains all unique translatable strings extracted from the `dfr_localization` module and all its DFR dependencies. This file serves as the basis for creating language-specific `.po` files.
*   **Generation Process:**
    1.  Ensure `dfr_localization` and all its DFR module dependencies are present in the Odoo addons path.
    2.  Use Odoo's command-line interface to export translatable terms for `dfr_localization`. The command typically looks like:
        bash
        odoo-bin --dev=all -c <your_odoo_config_file> -d <your_database_name> -u dfr_localization --i18n-export --language=en_US --output=addons/dfr_localization/i18n/dfr_localization.pot
        
        (Replace placeholders with actual values. The database might need to be initialized with `dfr_localization` and its dependencies installed/updated for accurate term extraction.)
    3.  This process should be repeated whenever new translatable strings are added or existing ones are modified in any of the DFR modules.
*   **Content Structure (Example Snippet):**
    pot
    # Translations template for DFR custom modules.
    # Copyright (C) YEAR FAO & SSS-AI
    # This file is distributed under the same license as the DFR Localization Pack package.
    # FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
    #
    #, fuzzy
    msgid ""
    msgstr ""
    "Project-Id-Version: DFR Localization Pack 18.0.1.0.0\n"
    "Report-Msgid-Bugs-To: \n"
    "POT-Creation-Date: YYYY-MM-DD HH:MM+ZONE\n"
    "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
    "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
    "Language-Team: LANGUAGE <LL@li.org>\n"
    "Language: \n"
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "Plural-Forms: nplurals=2; plural=(n != 1);\n"

    #. module: dfr_farmer_registry
    #: model:ir.model.fields,field_description:dfr_farmer_registry.field_farmer_profile__full_name
    msgid "Full Name"
    msgstr ""

    #. module: dfr_dynamic_forms
    #: model_terms:ir.ui.view,arch_db:dfr_dynamic_forms.view_dynamic_form_form
    msgid "Create New Dynamic Form"
    msgstr ""
    
*   **Requirements Met:** REQ-LMS-001, REQ-LMS-002, REQ-LMS-004, REQ-PCA-018

#### 3.3.2 Language-Specific `.po` Files
For each supported language, a `.po` file will exist in the `i18n` directory (e.g., `en.po`, `fr.po`, `sm.po`, `to.po`, `bi.po`, `cki.po`, `pis.po`).

*   **Purpose:** Provide actual translations for the strings defined in the `.pot` file for a specific language.
*   **Generation/Update Process:**
    1.  Initially, copy `dfr_localization.pot` to `xx.po` (where `xx` is the language code, e.g., `fr`).
    2.  Translate the `msgstr` entries in the `xx.po` file.
    3.  For updates, use Gettext tools (like `msgmerge`) to merge new strings from an updated `.pot` file into existing `.po` files, preserving existing translations.
*   **Content Structure (Example `fr.po` Snippet):**
    po
    # French translations for DFR custom modules.
    # Copyright (C) YEAR FAO & SSS-AI
    # This file is distributed under the same license as the DFR Localization Pack package.
    # Translator Name <translator@example.com>, YEAR.
    #
    msgid ""
    msgstr ""
    "Project-Id-Version: DFR Localization Pack 18.0.1.0.0\n"
    "Report-Msgid-Bugs-To: \n"
    "POT-Creation-Date: YYYY-MM-DD HH:MM+ZONE\n"
    "PO-Revision-Date: YYYY-MM-DD HH:MM+ZONE\n" # Date of last translation update
    "Last-Translator: Translator Name <translator@example.com>\n"
    "Language-Team: French <contact@project.org>\n"
    "Language: fr\n" # ISO 639-1 language code
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "Plural-Forms: nplurals=2; plural=(n > 1);\n" # Language-specific plural forms

    #. module: dfr_farmer_registry
    #: model:ir.model.fields,field_description:dfr_farmer_registry.field_farmer_profile__full_name
    msgid "Full Name"
    msgstr "Nom Complet" # Translated string

    #. module: dfr_dynamic_forms
    #: model_terms:ir.ui.view,arch_db:dfr_dynamic_forms.view_dynamic_form_form
    msgid "Create New Dynamic Form"
    msgstr "Créer un Nouveau Formulaire Dynamique" # Translated string
    
*   **Specific Language Files:**
    *   `i18n/en.po`: English translations. `msgstr` entries will be identical to `msgid`.
    *   `i18n/fr.po`: French translations.
    *   `i18n/sm.po`: Samoan translations.
    *   `i18n/to.po`: Tongan translations.
    *   `i18n/bi.po`: Bislama (Vanuatu) translations.
    *   `i18n/cki.po`: Cook Islands Māori (Rarotongan) translations. *Note: Confirm official ISO 639 code.*
    *   `i18n/pis.po`: Pijin (Solomon Islands) translations. *Note: Confirm official ISO 639 code.*
*   **Headers:** Each `.po` file must have correct headers, especially the `Language:` and `Plural-Forms:` lines, specific to the target language.
*   **Requirements Met:** REQ-LMS-001, REQ-LMS-002, REQ-LMS-004, REQ-PCA-018

## 4. Data Design
This module does not define new Odoo models or database tables. Its "data" consists of the `.po` and `.pot` files, whose structure is governed by the GNU Gettext format.

## 5. Interface Design

### 5.1 Internal Interfaces
This module does not expose new programmatic interfaces. It relies on Odoo's internal i18n mechanisms.

### 5.2 User Interfaces
This module does not create new user interfaces. It enables the localization of existing UIs in other DFR modules and Odoo itself. The management of translations and active languages is done through standard Odoo administrative interfaces:
*   **Translation Import/Export:**
    *   **Odoo Standard View:** Typically accessed via Developer Mode -> Settings -> Translations -> Import / Export Translations.
    *   **Purpose:** Allows administrators to export `.pot` files or specific language `.po` files, and import updated `.po` files to load new translations.
    *   **Relevant Endpoint (Conceptual):** `DFR_MOD_LOC_TRANSLATION_FILES_ENDPOINT` (This is an Odoo system action, not a custom endpoint defined by this module).
*   **Language Configuration:**
    *   **Odoo Standard View:** Typically accessed via Settings -> Translations -> Languages.
    *   **Purpose:** Allows administrators to install new languages (making Odoo load the corresponding `.po` files from modules like `dfr_localization`) and activate/deactivate languages for the instance.
    *   **Relevant Endpoint (Conceptual):** `DFR_MOD_LOC_LANGUAGE_CONFIG_ENDPOINT` (This is an Odoo system action).

## 6. Dependencies
*   **Odoo `base` module:** For the core internationalization framework.
*   **All other custom DFR Odoo modules:** As listed in the `depends` key of `__manifest__.py`. This is essential for `dfr_localization` to act as the central translation provider for the entire DFR application suite. Example dependencies (replace with actual names):
    *   `dfr_common_core`
    *   `dfr_farmer_registry`
    *   `dfr_dynamic_forms`
    *   `dfr_notifications_module`
    *   `dfr_api_management`
    *   `dfr_admin_tools`
    *   `dfr_self_service_portal`

## 7. Requirements Traceability
| Requirement ID | Component(s)                                 | Design Specification Section(s) |
|----------------|----------------------------------------------|---------------------------------|
| REQ-PCA-018    | `i18n/*.po` files, `__manifest__.py`         | 3.2, 3.3.1, 3.3.2               |
| REQ-LMS-001    | `i18n/*.po` files, `__manifest__.py`         | 3.2, 3.3.1, 3.3.2               |
| REQ-LMS-002    | `i18n/*.po` files, `__manifest__.py`         | 3.2, 3.3.1, 3.3.2, 5.2          |
| REQ-LMS-004    | `i18n/*.po` files, `__manifest__.py`         | 3.2, 3.3.1, 3.3.2               |
| REQ-SYSADM-006 | Interaction with Odoo Language Settings View | 5.2 (implicitly enabled by this module) |

## 8. Localization Strategy
1.  **String Extraction:** All translatable strings from DFR modules are marked using Odoo conventions (e.g., `_("My String")` in Python, `t-esc` or `t-out` in QWeb, field strings in models/views).
2.  **POT File Generation:** The `dfr_localization.pot` file is generated/updated using Odoo's i18n export tools, targeting the `dfr_localization` module. Due to its manifest dependencies, this will include terms from all DFR modules.
3.  **PO File Creation/Update:** For each target language, a `.po` file is created from the `.pot` file or updated using tools like `msgmerge`.
4.  **Translation:** Translators fill in the `msgstr` entries in each language-specific `.po` file.
5.  **Integration:** The translated `.po` files are placed in the `dfr_addons/dfr_localization/i18n/` directory.
6.  **Loading Translations:**
    *   Odoo automatically loads translations from `.po` files for installed modules when a language is activated.
    *   Administrators can manually update translations for an active language using Odoo's "Load a Translation" feature, selecting the relevant language and uploading the corresponding `.po` file from this module. This overrides existing translations for that language from this module.

## 9. Deployment Considerations
*   The `dfr_localization` module must be deployed alongside all other custom DFR Odoo modules.
*   Ensure file permissions for the `i18n` directory and its contents are correct.
*   After deployment or updates to `.po` files, Odoo might need a server restart or an administrator might need to manually trigger a "Load a Translation" for the changes to take full effect for all users and parts of the system.
*   The list of languages to be installed and activated by default on each country instance will be part of the instance-specific deployment configuration.

## 10. Non-Functional Requirements
*   **Maintainability:** Translations are maintained in standard `.po` files, separate from code, facilitating updates by translators without needing developer intervention for the translation content itself.
*   **Completeness:** The module aims to provide a structure for complete translation coverage of all DFR custom UI elements. The completeness of actual translations depends on the translation process.
*   **Consistency:** By centralizing translation management through this module and a master `.pot` file, consistency in terminology across the DFR platform can be better managed.

This SDS focuses on the structure and role of the `DFR_MOD_LOCALIZATION` module as a container and enabler for translations, rather than a module with complex executable code. Its correct configuration, especially the `depends` list in `__manifest__.py`, is key to its effectiveness.