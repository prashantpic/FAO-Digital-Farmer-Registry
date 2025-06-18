# DFR Documentation Standards

## 1. Introduction
This document outlines the standards and guidelines for creating and maintaining all documentation related to the Digital Farmer Registry (DFR) project. Consistent and high-quality documentation is crucial for developers, administrators, users, and other stakeholders.
These standards apply to both technical documentation (code comments, API docs, architectural diagrams) and user-facing materials (manuals, guides).
*Req IDs: A.3.5*

## 2. General Principles
*   **Clarity:** Documentation should be clear, concise, and easy to understand by its target audience. Avoid jargon where possible, or define it in a [glossary](../glossary.md).
*   **Accuracy:** Documentation must accurately reflect the current state of the system or code. Outdated documentation is misleading.
*   **Completeness:** Provide sufficient detail for the audience to achieve their goals (e.g., understand a feature, use an API, perform a task).
*   **Accessibility:** Ensure documentation is accessible, considering aspects like readability, structure, and use of alternative text for images.
*   **Discoverability:** Documentation should be well-organized and easy to navigate and search.
*   **Consistency:** Use consistent terminology, formatting, and style across all documentation.

## 3. Code Commenting Standards

### 3.1 Python (Odoo Backend)
*   Adhere to **PEP 8** for general Python code style.
*   Use **PEP 257** for docstrings.
*   **Module-Level Docstrings:** Every `.py` file should start with a docstring explaining its purpose and content.
    ```python
    # -*- coding: utf-8 -*-
    """
    This module implements the core farmer registration functionalities for DFR.
    It includes models for Farmer, Household, and related entities.
    """
    ```
*   **Class Docstrings:** All classes should have a docstring describing their purpose.
    ```python
    class DfrFarmer(models.Model):
        """
        Represents a registered farmer in the DFR system.
        Stores personal information, contact details, and links to households and farms.
        """
        _name = 'dfr.farmer'
        _description = 'Digital Farmer Registry - Farmer'
        # ...
    ```
*   **Method/Function Docstrings:**
    *   All public methods/functions and non-trivial private ones should have docstrings.
    *   Describe what the function does, its arguments (if any), and what it returns (if any).
    *   For Odoo model methods, explain their purpose in the context of the business logic.
    ```python
    def calculate_farmer_age(self):
        """
        Calculates the age of the farmer based on their date of birth.

        :return: Farmer's age in years, or None if date_of_birth is not set.
        :rtype: int or None
        """
        # ...
    ```
*   **Inline Comments:** Use inline comments (`#`) to explain complex or non-obvious parts of the code. Avoid over-commenting simple code.
    ```python
    # Calculate subsidy based on farmer category and land size
    subsidy_amount = self._compute_subsidy(farmer.category_id, farm.land_size)
    ```

### 3.2 XML (Odoo Views, Data Files)
*   Use XML comments (`<!-- ... -->`) to explain complex view structures, non-obvious domain logic in views, or the purpose of specific data records.
    ```xml
    <!-- Inherit the base partner form to add DFR specific fields -->
    <record id="view_partner_form_dfr_inherit" model="ir.ui.view">
        <field name="name">res.partner.form.dfr.inherit</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <!-- Add DFR UID field in the main sheet -->
            <xpath expr="//field[@name='vat']" position="after">
                <field name="dfr_uid"/>
            </xpath>
        </field>
    </record>
    ```

### 3.3 Mobile Application (Kotlin/Java or Dart)
*   **Kotlin/Java:** Use KDoc/JSDoc style comments for classes, methods, and complex code blocks.
    ```kotlin
    /**
     * Synchronizes local farmer data with the remote DFR server.
     * Fetches pending changes and sends them to the API.
     *
     * @param onComplete Callback function invoked upon completion.
     * @param onError Callback function invoked if an error occurs.
     */
    fun syncFarmerData(onComplete: () -> Unit, onError: (Exception) -> Unit) {
        // ...
    }
    ```
*   **Dart (Flutter):** Use Dartdoc style comments (`///` for single line, `/** ... */` for multi-line).
    ```dart
    /// Represents a Farmer entity in the mobile application.
    class Farmer {
      /// The unique identifier for the farmer.
      final String id;
      String name;

      /// Creates a new Farmer instance.
      ///
      /// [id] must not be null.
      Farmer({required this.id, required this.name});
    }
    ```

### 3.4 JavaScript (Odoo Frontend - OWL)
*   Use JSDoc style comments for components, methods, and complex logic.
    ```javascript
    /**
     * @module {owl.Component} dfr.FarmerSearchComponent
     * @description Component for searching farmers in the DFR system.
     */
    class FarmerSearchComponent extends Component {
        // ...
        /**
         * Handles the search button click event.
         * Fetches farmers based on the current query.
         * @async
         */
        async _onSearchClick() {
            // ...
        }
    }
    ```

## 4. README.md Structure
*   Each Odoo module (`addon`) should have a `README.md` or `README.rst` file in its root directory.
*   **Key Sections for Module READMEs:**
    1.  **Module Name and Overview:** Brief description of the module's purpose.
    2.  **Functionality:** Key features provided by the module.
    3.  **Dependencies:** List any other Odoo modules or external libraries it depends on.
    4.  **Configuration (if any):** Steps required to configure the module.
    5.  **Usage (if applicable):** How to use the module's features.
    6.  **Known Issues/Limitations (if any).**
    7.  **Authors/Contributors.**
*   The main project repository `README.md` (as specified in SDS 3.1) provides an overview of the entire documentation portal.

## 5. API Documentation Standards
*   DFR APIs will be documented using the **OpenAPI 3.x specification**.
*   **Source of Truth:** API documentation should be generated from annotations in the Odoo controller code where possible, or maintained in a separate OpenAPI YAML/JSON file that is kept in sync with the implementation.
*   `[Placeholder: Decision on tool/method for generating/maintaining OpenAPI spec - e.g., Odoo built-in tools, connexion, drf-spectacular if Django REST framework were used (not applicable here directly), or manual YAML with linters like Spectral].`
*   **Content for each API Endpoint:**
    *   Path and HTTP method.
    *   Summary and detailed description of the endpoint's purpose.
    *   Request parameters (path, query, header, cookie) with descriptions, data types, and whether they are required.
    *   Request body schema (if applicable) with field descriptions, data types, and examples.
    *   Response schemas for all possible HTTP status codes (success and error), including field descriptions, data types, and examples.
    *   Authentication and authorization requirements.
    *   Rate limiting information (if applicable).
*   The API documentation should be accessible via the [API Developer Guide](../developer-guides/api-developer-guide.md).

## 6. Developer Guide and User Manual Generation
*   **Tool:** MkDocs with the Material for MkDocs theme is the primary tool.
*   **Source Format:** Markdown.
*   **Structure:** Follow the directory and file structure defined in the SDS Section 3.
*   **Content:** Address the "Key Content" points specified for each document in the SDS.

## 7. Documentation Versioning
*   Documentation will be versioned in conjunction with major DFR software releases.
*   The `mike` MkDocs plugin (or a similar tool) will be used to manage and serve multiple versions of the documentation portal.
*   Each software release tag in Git (e.g., `v1.0.0`) will correspond to a version of the documentation.

## 8. Style Guide (Written Documentation)
*   **Language:** English (UK or US - be consistent). Default: `en` (as per `mkdocs.yml`).
    *   `[Placeholder: Decide on specific English variant if strict consistency is required, e.g., en-US or en-GB]`
*   **Tone:** Professional, clear, and direct. Tailor the tone to the target audience (e.g., more technical for developer guides, simpler for end-user manuals).
*   **Formatting:**
    *   Use Markdown effectively for headings, lists, bold/italics, code blocks, tables, links, and admonitions (e.g., `!!! note`, `!!! warning`).
    *   Keep paragraphs relatively short.
    *   Use screenshots and diagrams where they aid understanding (ensure they have alt text).
*   **Terminology:** Use consistent terminology as defined in the [Project Glossary](../glossary.md).
*   **Acronyms:** Define acronyms on first use in a document (e.g., "Digital Farmer Registry (DFR)").
*   **File Naming:** Use lowercase, hyphenated names for Markdown files (e.g., `user-management.md`).
*   **Images:**
    *   Store in `docs/assets/images/`.
    *   Use descriptive filenames.
    *   Provide meaningful alt text for all images for accessibility.
    *   Optimize image sizes for web.
*   **Diagrams:**
    *   Use Mermaid.js for diagrams embedded in Markdown where possible.
    *   For complex diagrams, use static images (PNG, SVG) stored in `docs/assets/images/` and provide alt text.

## 9. Review Process
*   All significant documentation changes (new documents, major updates) should be reviewed before publication.
*   Reviews should check for accuracy, clarity, completeness, and adherence to these standards.
*   For documentation within the code repository (e.g., READMEs, ADRs), the review can be part of the code Pull/Merge Request process.

## 10. Updates and Maintenance
*   Documentation should be treated as a living part of the project.
*   Assign responsibility for keeping specific sections of the documentation up-to-date.
*   Schedule periodic reviews of key documentation (e.g., annually or per major release) to ensure it remains accurate and relevant.

By adhering to these standards, we can create a comprehensive, high-quality documentation suite that effectively supports the DFR project.