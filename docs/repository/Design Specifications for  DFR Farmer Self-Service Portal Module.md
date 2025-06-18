# Software Design Specification: DFR Farmer Self-Service Portal Module (DFR_MOD_FARMER_PORTAL)

## 1. Introduction

### 1.1. Purpose
This document outlines the software design specification for the Digital Farmer Registry (DFR) Farmer Self-Service Portal Module (`DFR_MOD_FARMER_PORTAL`). This module is an Odoo 18.0 Community addon that extends the Odoo Website module. Its primary purpose is to provide a public-facing, mobile-responsive web portal enabling:
*   Farmer pre-registration.
*   Display of informational content about the DFR.
*   Access for farmers to view and submit specific dynamic forms configured for public use.
*   Adherence to Web Content Accessibility Guidelines (WCAG 2.1 Level AA).

This SDS will guide the development of the module, detailing its components, interactions, and technical specifications.

### 1.2. Scope
The scope of this module includes:
*   Development of Odoo controllers to handle HTTP requests for portal pages.
*   Creation of QWeb templates for rendering portal pages, including pre-registration forms, dynamic forms, and informational content.
*   Implementation of client-side JavaScript for form validation, dynamic interactions, and accessibility enhancements.
*   Styling of the portal using CSS, ensuring mobile responsiveness and adherence to WCAG 2.1 AA.
*   Integration with `DFR_MOD_FARMER_REGISTRY` for farmer data submission and `DFR_MOD_DYNAMIC_FORMS` for rendering and processing dynamic forms.
*   Support for country-specific branding and localization through integration with `DFR_MOD_LOCALIZATION`.

The module will *not* handle:
*   Core farmer data storage and business logic (handled by `DFR_MOD_FARMER_REGISTRY`).
*   Dynamic form definition and core processing logic (handled by `DFR_MOD_DYNAMIC_FORMS`).
*   User authentication for already registered farmers to access personalized dashboards (this might be a future extension or separate module). For this module, "public" dynamic forms are primarily for additional data collection linked to an existing farmer, where identification might occur within the form or through a yet-to-be-defined secure context if the farmer is already in a portal session.

### 1.3. Glossary
*   **DFR**: Digital Farmer Registry
*   **SDS**: Software Design Specification
*   **QWeb**: Odoo's primary templating engine
*   **WCAG**: Web Content Accessibility Guidelines
*   **CSRF**: Cross-Site Request Forgery
*   **ARIA**: Accessible Rich Internet Applications
*   **KYC**: Know Your Customer
*   **UID**: Unique Identifier

## 2. System Overview
The `DFR_MOD_FARMER_PORTAL` module is a presentation layer component within the larger DFR system. It acts as the primary public web interface for farmers. It leverages Odoo's Website module capabilities and interacts with backend DFR modules (`DFR_MOD_FARMER_REGISTRY`, `DFR_MOD_DYNAMIC_FORMS`, `DFR_MOD_LOCALIZATION`) to deliver its functionalities.

Key interactions:
*   **Farmers (Public Users)**: Access informational content, submit pre-registration forms, and fill out designated public dynamic forms.
*   **DFR_MOD_FARMER_REGISTRY**: Receives pre-registration data to create or update farmer records in a pending state. Provides data for farmer identification if needed for dynamic forms.
*   **DFR_MOD_DYNAMIC_FORMS**: Provides definitions for dynamic forms to be rendered on the portal and processes submissions of these forms.
*   **DFR_MOD_LOCALIZATION**: Provides country-specific branding information and manages language translations for portal content.

## 3. Design Considerations

### 3.1. Architectural Style
The module adheres to the overall **Modular Monolith** architecture of the DFR system, implemented as an Odoo addon. Internally, it follows an **MVC/MVT (Model-View-Template)** pattern, characteristic of Odoo's web development.

### 3.2. Key Technologies
*   **Backend**: Python 3.11.9 (Odoo 18.0 Controllers)
*   **Frontend Templating**: QWeb (Odoo 18.0)
*   **Frontend Structure/Styling**: HTML5, CSS3, Bootstrap 5.3.x (as provided by Odoo Website)
*   **Frontend Behavior**: JavaScript ES6+ (Odoo's JavaScript framework and/or plain JS)
*   **Odoo Framework**: Odoo 18.0 Community Edition, specifically the `website` module.

### 3.3. Design Patterns
*   **Controller Pattern**: For handling HTTP requests and responses.
*   **Template View Pattern (QWeb)**: For separating presentation logic from application logic.
*   **Responsive Design**: Using Bootstrap grid and CSS media queries for adapting to various screen sizes.

### 3.4. External Dependencies
*   `website`: Base Odoo module for website functionality.
*   `dfr_farmer_registry`: For pre-registration data submission and farmer identification.
*   `dfr_dynamic_forms`: For rendering and submitting dynamic forms.
*   `dfr_localization`: For country-specific branding and language management.

### 3.5. Accessibility (WCAG 2.1 AA)
Accessibility is a core requirement (REQ-FSSP-013). Design and implementation will actively incorporate WCAG 2.1 Level AA guidelines. This includes:
*   Semantic HTML.
*   Keyboard navigability.
*   Sufficient color contrast.
*   Proper use of ARIA attributes.
*   Text alternatives for non-text content (e.g., alt text for logos).
*   Responsive design accommodating zoom and various screen sizes.
*   Clear form labels and error handling.

## 4. Module Structure and Component Specifications
The module will be structured as a standard Odoo addon within the `dfr_addons/dfr_farmer_portal` directory.

### 4.1. `__init__.py`
*   **Purpose**: Initializes the Python package for the Odoo module.
*   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import controllers
    
*   **Requirement Mapping**: Module Initialization

### 4.2. `__manifest__.py`
*   **Purpose**: Defines module metadata, dependencies, data files, and assets.
*   **Logic**:
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'DFR Farmer Self-Service Portal',
        'version': '18.0.1.0.0',
        'summary': 'Public portal for farmer pre-registration and dynamic form access.',
        'author': 'FAO DFR Project Team', # Or specific implementer
        'website': 'https://www.fao.org', # Project specific website
        'license': 'MIT', # Or Apache-2.0, as per REQ-CM-001
        'category': 'Website/Portal',
        'depends': [
            'website',
            'dfr_farmer_registry', # For submitting pre-registrations
            'dfr_dynamic_forms',   # For rendering and submitting dynamic forms
            # 'dfr_localization',  # Implicitly used for branding/language config
        ],
        'data': [
            'views/assets.xml',
            'views/portal_layout.xml',
            'views/portal_preregistration_templates.xml',
            'views/portal_dynamic_form_templates.xml',
            'views/portal_info_page_template.xml', # For DFR_PORTAL_INFO_PAGE
            'views/snippets/country_branding_snippet.xml',
            # Security rules if any portal-specific groups/rules are needed
        ],
        'assets': {
            'web.assets_frontend': [
                'dfr_farmer_portal/static/src/css/portal_main.css',
                'dfr_farmer_portal/static/src/css/portal_accessibility.css',
                'dfr_farmer_portal/static/src/js/portal_preregistration.js',
                'dfr_farmer_portal/static/src/js/portal_dynamic_form.js',
                'dfr_farmer_portal/static/src/js/portal_accessibility.js',
            ],
        },
        'installable': True,
        'application': False, # It's an addon extending website
        'auto_install': False,
    }
    
*   **Requirement Mapping**: REQ-FSSP-001

### 4.3. `controllers/`

#### 4.3.1. `controllers/__init__.py`
*   **Purpose**: Initializes the Python controllers package.
*   **Logic**:
    python
    # -*- coding: utf-8 -*-
    from . import portal
    

#### 4.3.2. `controllers/portal.py`
*   **Purpose**: Handles HTTP requests for portal pages, processes form submissions.
*   **Class**: `FarmerPortalController(odoo.http.Controller)`
*   **Requirement Mapping**: REQ-FSSP-003, REQ-FSSP-004, REQ-FSSP-009, REQ-FSSP-002 (for info page)

*   **Method**: `dfr_information_page(self, **kw)`
    *   **Decorator**: `@http.route('/dfr/info', type='http', auth='public', website=True, methods=['GET'])`
    *   **Parameters**: `**kw` (keyword arguments from request).
    *   **Returns**: `odoo.http.Response` (rendered HTML page).
    *   **Logic**:
        1.  Retrieve localized informational content about the DFR. This content could be:
            *   Managed as Odoo website pages snippets (editable by admin).
            *   Fetched from `ir.config_parameter` if simple text.
            *   Pulled from dedicated model in `dfr_localization` or `dfr_common`.
        2.  Prepare rendering values dictionary.
        3.  Render the `dfr_farmer_portal.portal_info_page_template` QWeb template, passing the content and other necessary values (e.g., website object).
    *   **Endpoint ID**: `DFR_PORTAL_INFO_PAGE`

*   **Method**: `farmer_preregistration_form(self, **kw)`
    *   **Decorator**: `@http.route('/farmer/register', type='http', auth='public', website=True, methods=['GET'])`
    *   **Parameters**: `**kw` (keyword arguments, e.g., for re-displaying form with errors).
    *   **Returns**: `odoo.http.Response` (rendered HTML page).
    *   **Logic**:
        1.  Prepare `render_values` dictionary.
        2.  Add any pre-filled data or error messages from `kw` if re-rendering after a failed POST.
        3.  Fetch necessary data for form options (e.g., list of National ID types if dynamic, village list if from a selection). This might involve calls to `request.env['some.model'].search_read(...)`.
        4.  Render the `dfr_farmer_portal.portal_preregistration_form_template` QWeb template with `render_values`.
    *   **Endpoint ID**: `DFR_PORTAL_PRE_REGISTRATION_FORM_PAGE` (GET part)

*   **Method**: `farmer_preregistration_submit(self, **post)`
    *   **Decorator**: `@http.route('/farmer/register', type='http', auth='public', website=True, methods=['POST'], csrf=True)`
    *   **Parameters**: `**post` (dictionary of submitted form data).
    *   **Returns**: `odoo.http.Response` (redirect or re-rendered form).
    *   **Logic**:
        1.  **Server-Side Validation**:
            *   Retrieve form data: `full_name = post.get('full_name')`, etc.
            *   Validate required fields: `full_name`, `village`, `primary_crop_type`, `contact_number`.
            *   Validate formats (e.g., contact number).
            *   If validation errors:
                *   Store error messages and submitted values.
                *   Call `self.farmer_preregistration_form(**errors_and_values)` to re-render the form with errors.
        2.  **Data Preparation**: Prepare a dictionary of values for creating the farmer record.
        3.  **Service Call to `dfr_farmer_registry`**:
            *   `farmer_registry_service = request.env['dfr.farmer.registry.service']` (assuming a service model exists in `dfr_farmer_registry`).
            *   `result = farmer_registry_service.create_farmer_from_portal(values_dict)`
            *   The `create_farmer_from_portal` method in `dfr_farmer_registry` should:
                *   Set initial status to 'draft' or 'pending verification'.
                *   Perform de-duplication checks.
                *   Handle any specific logic for portal-originated registrations.
                *   Return a dictionary like `{'success': True/False, 'farmer_id': id or None, 'message': 'some message'}`.
        4.  **Handle Response**:
            *   If `result['success']` is True:
                *   Redirect to `dfr_farmer_portal.portal_preregistration_confirmation_template` (or a URL rendering it).
                *   Optionally pass a success message or farmer UID via query params or session.
            *   Else (e.g., backend validation error, de-duplication issue):
                *   Pass `result['message']` and submitted values to `self.farmer_preregistration_form()` to re-render with errors.
    *   **Endpoint ID**: `DFR_PORTAL_PRE_REGISTRATION_FORM_PAGE` (POST part)

*   **Method**: `portal_dynamic_form_render(self, form_id, **kw)`
    *   **Decorator**: `@http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['GET'])`
        *   `form_id`: Odoo `dfr.dynamic.form` record, automatically fetched by Odoo.
    *   **Parameters**: `form_id` (model instance), `**kw`.
    *   **Returns**: `odoo.http.Response`.
    *   **Logic**:
        1.  Check if `form_id` is valid and configured for public portal access (e.g., `form_id.is_public_portal_accessible`). If not, return 404 or an access denied page.
        2.  Fetch form structure (fields, labels, types, validation, conditional logic) from `form_id` or via a service in `dfr_dynamic_forms`. Ensure labels and options are localized.
            *   `form_definition = request.env['dfr.dynamic.form.service'].get_form_render_definition(form_id, lang=request.lang)`
        3.  Prepare `render_values = {'form_record': form_id, 'form_definition': form_definition}`. Add any error messages or pre-filled data from `kw` if re-rendering.
        4.  Render `dfr_farmer_portal.portal_dynamic_form_display_template` with `render_values`.
    *   **Endpoint ID**: `DFR_PORTAL_DYNAMIC_FORM_PAGE` (GET part)

*   **Method**: `portal_dynamic_form_submit(self, form_id, **post)`
    *   **Decorator**: `@http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['POST'], csrf=True)`
    *   **Parameters**: `form_id` (model instance), `**post` (submitted form data).
    *   **Returns**: `odoo.http.Response`.
    *   **Logic**:
        1.  Check `form_id.is_public_portal_accessible`. If not, deny.
        2.  **Farmer Identification**:
            *   Determine how the submitting farmer is identified. If the form is truly public and unauthenticated for this step, the form itself must collect farmer identifying information (e.g., Farmer UID or National ID). This submitted identifier needs to be validated against `dfr_farmer_registry`.
            *   `farmer_identifier = post.get('farmer_identifier_field_name')`
            *   `farmer_record = request.env['dfr.farmer'].sudo().search([('uid', '=', farmer_identifier)], limit=1)` (Or similar lookup logic from `dfr_farmer_registry`).
            *   If farmer not found or ambiguous, re-render form with error.
        3.  **Server-Side Validation**:
            *   Validate `**post` data against the `form_id`'s field definitions (types, required, regex, etc.) using services from `dfr_dynamic_forms`.
            *   If validation errors: Re-render the form using `self.portal_dynamic_form_render(form_id, **errors_and_post_values)`.
        4.  **Service Call to `dfr_dynamic_forms`**:
            *   `dynamic_form_service = request.env['dfr.dynamic.form.service']`
            *   `submission_data = {key: value for key, value in post.items() if key not in ['csrf_token', 'farmer_identifier_field_name']}`
            *   `result = dynamic_form_service.process_portal_submission(form_id, farmer_record.id, submission_data)`
            *   The `process_portal_submission` method in `dfr_dynamic_forms` should:
                *   Create `form.submission` and `form.response` records.
                *   If `form_id` is configured to update core DFR data (REQ-FSSP-010), it must call relevant services in `dfr_farmer_registry` to apply these updates, ensuring core validation and de-duplication logic is triggered.
        5.  **Handle Response**:
            *   If `result['success']`: Redirect to `dfr_farmer_portal.portal_dynamic_form_confirmation_template`.
            *   Else: Re-render form with `result['message']`.
    *   **Endpoint ID**: `DFR_PORTAL_DYNAMIC_FORM_PAGE` (POST part)

### 4.4. `views/`

#### 4.4.1. `views/assets.xml`
*   **Purpose**: Registers static assets (CSS, JS).
*   **Content**:
    xml
    <odoo>
        <data>
            <template id="assets_frontend" inherit_id="web.assets_frontend" name="DFR Portal Assets">
                <xpath expr="." position="inside">
                    <link rel="stylesheet" type="text/css" href="/dfr_farmer_portal/static/src/css/portal_main.css"/>
                    <link rel="stylesheet" type="text/css" href="/dfr_farmer_portal/static/src/css/portal_accessibility.css"/>
                    <script type="text/javascript" src="/dfr_farmer_portal/static/src/js/portal_preregistration.js"></script>
                    <script type="text/javascript" src="/dfr_farmer_portal/static/src/js/portal_dynamic_form.js"></script>
                    <script type="text/javascript" src="/dfr_farmer_portal/static/src/js/portal_accessibility.js"></script>
                </xpath>
            </template>
        </data>
    </odoo>
    
*   **Requirement Mapping**: REQ-FSSP-001, REQ-FSSP-013

#### 4.4.2. `views/portal_layout.xml`
*   **Purpose**: Defines the common layout for portal pages.
*   **Requirement Mapping**: REQ-FSSP-001, REQ-FSSP-013
*   **Key QWeb Template**: `dfr_farmer_portal.portal_layout`
    xml
    <odoo>
        <template id="portal_layout" inherit_id="website.layout" name="DFR Portal Layout">
            <xpath expr="//header//nav" position="before">
                <!-- Country specific logo placeholder -->
                <div class="container">
                    <div class="row">
                        <div class="col-12 text-center my-3">
                             <t t-call="dfr_farmer_portal.s_country_logo_placeholder"/>
                        </div>
                    </div>
                </div>
            </xpath>
            <xpath expr="//main" position="attributes">
                <attribute name="role">main</attribute> <!-- WCAG: main landmark -->
            </xpath>
            <xpath expr="//div[@id='wrapwrap']//main" position="replace">
                <main role="main" class="dfr-portal-main-content">
                    <t t-call="website.navbar_alternate"/> <!-- Or your custom nav if needed -->
                    <div id="wrap" class="oe_structure oe_empty">
                        <t t-call-block="main_content_placeholder"/>
                    </div>
                </main>
            </xpath>
            <xpath expr="//footer" position="attributes">
                <attribute name="role">contentinfo</attribute> <!-- WCAG: footer landmark -->
            </xpath>
             <xpath expr="//footer//div[hasclass('container')]" position="inside">
                <!-- Additional footer content specific to DFR portal if needed -->
                <div class="row mt-2">
                    <div class="col-12 text-center">
                        <p class="text-muted">Powered by DFR Platform</p>
                    </div>
                </div>
            </xpath>
        </template>

        <!-- Placeholder for main content for child templates -->
        <template id="main_content_placeholder" name="Main Content Placeholder">
            <!-- This block will be replaced by content from specific page templates -->
        </template>
    </odoo>
    

#### 4.4.3. `views/portal_preregistration_templates.xml`
*   **Purpose**: QWeb templates for farmer pre-registration form and confirmation.
*   **Requirement Mapping**: REQ-FSSP-001, REQ-FSSP-003, REQ-FSSP-013
*   **Key QWeb Templates**:
    *   `dfr_farmer_portal.portal_preregistration_form_template`
        *   Inherits `dfr_farmer_portal.portal_layout`.
        *   Replaces `main_content_placeholder`.
        *   Contains `<form>` with fields: Full Name, Village, Primary Crop Type, Contact Number, National ID Type, National ID Number.
        *   Each form field group will use Bootstrap classes for layout and include:
            *   `<label for="field_id">Label Text <span class="text-danger" t-if="is_required">*</span></label>`
            *   `<input type="..." class="form-control" id="field_id" name="field_name" t-att-required="is_required or None" t-att-aria-required="is_required and 'true' or None" />`
            *   Error message display logic: `<div t-if="errors.get('field_name')" class="alert alert-danger" role="alert" t-esc="errors['field_name']"/>`
            *   ARIA attributes for accessibility: `aria-describedby` for help/error text.
        *   CSRF token.
    *   `dfr_farmer_portal.portal_preregistration_confirmation_template`
        *   Inherits `dfr_farmer_portal.portal_layout`.
        *   Replaces `main_content_placeholder`.
        *   Displays a thank you message and information about next steps.

#### 4.4.4. `views/portal_dynamic_form_templates.xml`
*   **Purpose**: QWeb templates for rendering and submitting public dynamic forms.
*   **Requirement Mapping**: REQ-FSSP-001, REQ-FSSP-009, REQ-FSSP-013
*   **Key QWeb Templates**:
    *   `dfr_farmer_portal.portal_dynamic_form_display_template`
        *   Inherits `dfr_farmer_portal.portal_layout`.
        *   Replaces `main_content_placeholder`.
        *   Displays `form_record.name` as title.
        *   Contains `<form>` posting to the dynamic form URL.
        *   CSRF token.
        *   Iterates `form_definition.fields` (passed from controller):
            *   Dynamically renders HTML input elements based on `field.type` (text, number, date, select, etc.).
            *   Includes `field.label`, required indicators, help text, error placeholders.
            *   Uses ARIA attributes for accessibility.
            *   Passes `form_definition` as JSON to client-side JS for dynamic interactions if needed.
    *   `dfr_farmer_portal.portal_dynamic_form_confirmation_template`
        *   Inherits `dfr_farmer_portal.portal_layout`.
        *   Replaces `main_content_placeholder`.
        *   Displays a submission success message.

#### 4.4.5. `views/portal_info_page_template.xml`
*   **Purpose**: QWeb template for the DFR informational page.
*   **Requirement Mapping**: REQ-FSSP-002
*   **Key QWeb Template**: `dfr_farmer_portal.portal_info_page_template`
    *   Inherits `dfr_farmer_portal.portal_layout`.
    *   Replaces `main_content_placeholder`.
    *   Content:
        *   Section for "About DFR"
        *   Section for "Benefits for Farmers"
        *   Section for "How to Register (Overview)"
    *   Content should be translatable, possibly using Odoo website snippets or editable areas.
    *   Structure with appropriate headings (h1, h2, h3) for WCAG.

#### 4.4.6. `views/snippets/country_branding_snippet.xml`
*   **Purpose**: Reusable QWeb snippet for country branding elements.
*   **Requirement Mapping**: REQ-FSSP-001
*   **Key QWeb Template**: `dfr_farmer_portal.s_country_logo_placeholder`
    xml
    <odoo>
        <template id="s_country_logo_placeholder" name="Country Logo Placeholder">
            <!-- Logic to fetch and display country-specific logo -->
            <!-- Example: Using current website's company logo -->
            <t t-if="website and website.company_id and website.company_id.logo">
                <img t-att-src="image_data_uri(website.company_id.logo)"
                     class="img-fluid dfr-country-logo"
                     t-att-alt="'Logo of %s' % website.company_id.name"/>
            </t>
            <!-- Fallback or alternative logic if logo is managed differently,
                 e.g., via ir.config_parameter or a model in dfr_localization -->
            <t t-else="">
                 <!-- Default placeholder text or image if no logo is configured -->
                 <span>[Country Logo]</span>
            </t>
        </template>
    </odoo>
    

### 4.5. `static/`

#### 4.5.1. `static/src/js/portal_preregistration.js`
*   **Purpose**: Client-side enhancements for the pre-registration form.
*   **Requirement Mapping**: REQ-FSSP-003, REQ-FSSP-013
*   **Key Functions/Logic**:
    *   `initPreRegistrationFormValidation()`:
        *   Target specific form inputs by ID or class.
        *   Implement client-side validation rules (e.g., regex for phone, patterns for National ID, non-empty for required fields).
        *   Display/hide custom error messages.
        *   Update ARIA attributes (`aria-invalid`, `aria-describedby`).
        *   Prevent form submission if client-side errors exist (can be overridden by user, server-side is definitive).
    *   `handleNationalIdVisibility()`:
        *   Event listener on "National ID Type" select field.
        *   Show/hide "National ID Number" field based on selection.
        *   Ensure accessibility (e.g., `aria-expanded` if content collapses).

#### 4.5.2. `static/src/js/portal_dynamic_form.js`
*   **Purpose**: Client-side logic for dynamic forms.
*   **Requirement Mapping**: REQ-FSSP-009, REQ-FSSP-013
*   **Key Functions/Logic**:
    *   `initDynamicFormInteractions(formElement, formDefinitionJsonString)`:
        *   `formElement`: The HTML form DOM element.
        *   `formDefinitionJsonString`: JSON string containing field definitions, validation rules, conditional logic passed from QWeb.
        *   Parse `formDefinitionJsonString`.
        *   Iterate through fields to apply conditional logic (show/hide fields based on other field values).
        *   Attach event listeners to trigger fields for conditional logic.
    *   `applyClientSideValidations(formElement, formDefinition)`:
        *   Iterate through fields to apply client-side validation rules defined in `formDefinition`.
        *   Display/hide error messages.
        *   Update ARIA attributes.

#### 4.5.3. `static/src/js/portal_accessibility.js`
*   **Purpose**: Dedicated JS for WCAG 2.1 AA compliance enhancements.
*   **Requirement Mapping**: REQ-FSSP-013
*   **Key Functions/Logic**:
    *   `enhanceKeyboardNavigation()`:
        *   Ensure all interactive elements are focusable and operable via keyboard.
        *   Manage focus when dynamic content appears/disappears (e.g., conditional form fields, error messages).
        *   Implement "skip to main content" link if header/nav is extensive.
    *   `manageAriaLiveRegions(message, politeness = 'polite')`:
        *   Function to update content of an ARIA live region (e.g., for announcing form submission status or dynamic error messages to screen readers).
    *   Could also include utilities for checking contrast or other specific WCAG success criteria if needed dynamically.

#### 4.5.4. `static/src/css/portal_main.css`
*   **Purpose**: Main styling for the portal.
*   **Requirement Mapping**: REQ-FSSP-001, REQ-FSSP-013
*   **Content**:
    *   Global styles: typography, base colors, link styles.
    *   Layout styles: header, footer, main content area adjustments.
    *   Form styling: consistent appearance for labels, inputs, selects, buttons, error messages.
    *   Responsive design: Media queries for small (mobile), medium (tablet), and large (desktop) screens.
    *   Country branding: Base styles that can be overridden by country-specific CSS (e.g., using CSS custom properties for theming).

#### 4.5.5. `static/src/css/portal_accessibility.css`
*   **Purpose**: CSS styles specifically for WCAG 2.1 AA compliance.
*   **Requirement Mapping**: REQ-FSSP-013
*   **Content**:
    *   Visible focus indicators for all interactive elements: `a:focus, button:focus, input:focus, select:focus, [tabindex="0"]:focus { outline: 3px solid blue !important; outline-offset: 1px; }` (adjust color/style for high contrast and aesthetics).
    *   Styles for `:focus-visible` pseudo-class for better focus indication management.
    *   Minimum text size and line height considerations.
    *   Ensure sufficient contrast for non-text elements where applicable.
    *   Styling for ARIA roles/states if not handled by default browser styles or JS (e.g., `[aria-invalid="true"]`).

#### 4.5.6. `static/description/icon.png`
*   **Purpose**: Module icon.
*   **Content**: A 128x128 PNG image visually representing the Farmer Self-Service Portal.

### 4.6. `i18n/`

#### 4.6.1. `i18n/dfr_farmer_portal.pot`
*   **Purpose**: Master translation template file.
*   **Content**: Auto-generated by Odoo. Contains all translatable strings from Python code (controllers) and XML/QWeb views.
*   **Requirement Mapping**: REQ-FSSP-001 (implicitly, as part of Odoo module structure for localization)
*   **Note**: Developers must ensure all user-facing strings are correctly marked for translation (e.g., `_("Text")` in Python, appropriate `t-translation` or `t-esc` usage in QWeb).

## 5. Data Models
This module primarily acts as a presentation layer and does not define its own core data models for farmer data or dynamic forms. It relies on models provided by:
*   **`dfr_farmer_registry`**: For `dfr.farmer`, `dfr.household`, etc.
*   **`dfr_dynamic_forms`**: For `dfr.dynamic.form`, `dfr.form.field`, `dfr.form.submission`, `dfr.form.response`.

Any data persisted by this portal (e.g., pre-registration submissions, dynamic form submissions) will be stored within the models of these dependency modules.

## 6. Interfaces

### 6.1. Internal Interfaces (with other DFR Odoo Modules)
*   **To `DFR_MOD_FARMER_REGISTRY`**:
    *   The `FarmerPortalController` will call Python methods/services (e.g., `request.env['dfr.farmer.registry.service'].create_farmer_from_portal(...)`) to submit pre-registration data.
    *   Expected data: Dictionary of validated farmer KYC fields.
    *   Expected response: Success/failure status, optional farmer ID, error messages.
*   **To `DFR_MOD_DYNAMIC_FORMS`**:
    *   The `FarmerPortalController` will call Python methods/services (e.g., `request.env['dfr.dynamic.form.service'].get_form_render_definition(...)` and `request.env['dfr.dynamic.form.service'].process_portal_submission(...)`) to:
        *   Fetch definitions of public dynamic forms for rendering.
        *   Submit data collected through public dynamic forms.
    *   Expected data (fetch): Form ID, current language.
    *   Expected response (fetch): Parsed form definition (fields, labels, rules).
    *   Expected data (submit): Form ID, farmer identifier, dictionary of submitted field values.
    *   Expected response (submit): Success/failure status, error messages.
*   **From `DFR_MOD_LOCALIZATION` (or `dfr_common`)**:
    *   The portal layout and snippets may fetch country-specific branding configurations (e.g., logo URL, theme colors) via Odoo system parameters (`ir.config_parameter`) or methods on a configuration model.

### 6.2. External Interfaces (Public Web Endpoints)
Defined by the controller methods with `@http.route`:
*   `/dfr/info` (GET): DFR Information Page.
*   `/farmer/register` (GET, POST): Farmer Pre-registration Form.
*   `/portal/forms/<model("dfr.dynamic.form"):form_id>` (GET, POST): Public Dynamic Form page.

## 7. Localization
*   All user-facing strings in QWeb templates and Python controllers will be translatable using Odoo's standard i18n mechanisms (`_()` in Python, `t-esc`, `t-raw`, `t-out` with translation context in QWeb).
*   The `dfr_farmer_portal.pot` file will be generated.
*   Actual `.po` translation files for specific languages will be managed by the `DFR_MOD_LOCALIZATION` module or central translation efforts.
*   The portal will use Odoo's website language switcher to allow users to select their preferred language from the list of languages activated for the country instance.
*   Content of informational pages and dynamic forms (labels, instructions, options) must be translatable.

## 8. Accessibility (WCAG 2.1 AA Compliance - REQ-FSSP-013)
Compliance will be achieved through:
*   **Semantic HTML**: Using appropriate HTML5 tags (`<main>`, `<nav>`, `<header>`, `<footer>`, etc.).
*   **Keyboard Navigation**: Ensuring all interactive elements are focusable and operable using a keyboard. Implementing logical tab order.
*   **Focus Management**: Clear visual focus indicators (CSS) and JS-managed focus for dynamic elements.
*   **ARIA Attributes**: Using ARIA roles, states, and properties where necessary to enhance understanding for assistive technologies (e.g., `aria-required`, `aria-invalid`, `aria-describedby`, `role="alert"`).
*   **Form Accessibility**: Associating labels with form controls, grouping related fields with `fieldset` and `legend`, providing clear error identification and instructions.
*   **Color Contrast**: Ensuring text and important UI elements meet contrast ratios (primarily via CSS in `portal_accessibility.css` and `portal_main.css`).
*   **Responsive Design**: Ensuring content reflows and is usable when zoomed or on different screen sizes.
*   **Text Alternatives**: Providing `alt` text for images (e.g., country logo).
*   **Dedicated CSS and JS**: `portal_accessibility.css` and `portal_accessibility.js` will contain specific styles and scripts to address WCAG criteria that cannot be met by standard Odoo/Bootstrap components alone.

## 9. Security Considerations
*   **CSRF Protection**: Enabled for all POST requests handled by Odoo website controllers (`csrf=True`).
*   **Input Validation**:
    *   Client-side (JavaScript) for immediate user feedback.
    *   Server-side (Python controllers) as the authoritative source of validation. Validate data types, formats, lengths, and against business rules.
*   **Output Encoding**: Rely on Odoo's QWeb templating engine for automatic HTML escaping of dynamic content (`t-esc`).
*   **Data Handling**: Data submitted through public forms is passed to backend service layers (`dfr_farmer_registry`, `dfr_dynamic_forms`) which are responsible for their own internal security and permission checks before persisting data. Submitted pre-registration data should create records in a 'pending' or 'draft' state requiring further administrative review.
*   **Error Handling**: User-friendly error messages will be displayed on the portal. Detailed technical errors and stack traces will *not* be shown publicly but logged on the server.
*   **HTTPS**: Assumed to be enforced at the reverse proxy level (e.g., Nginx) for all portal traffic (as per REQ-DIO-005).

## 10. Deployment Considerations
*   **Assets**: CSS and JavaScript files will be registered in `views/assets.xml` and bundled by Odoo's asset management system for frontend delivery.
*   **Dependencies**: Ensure `dfr_farmer_registry` and `dfr_dynamic_forms` (and implicitly `dfr_localization` or `dfr_common` for branding/language config) are installed in the Odoo instance.
*   **Country-Specific Branding**: The mechanism for applying country-specific logos and potentially themes (CSS overrides) needs to be robust, likely configured through `dfr_localization` or system parameters that this portal module can read. The `country_branding_snippet.xml` provides a placeholder for this.
*   **Configuration**:
    *   Public accessibility of specific dynamic forms needs to be configurable within the `dfr_dynamic_forms` module (e.g., a boolean field `is_public_portal_accessible` on the `dfr.dynamic.form` model).
    *   Informational content needs to be manageable, potentially via Odoo website's page editor or snippets.