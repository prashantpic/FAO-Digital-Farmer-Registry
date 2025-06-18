# Specification

# 1. Files

- **Path:** dfr_addons/dfr_farmer_portal/__init__.py  
**Description:** Odoo module initializer. Imports subdirectories like controllers and models (if any).  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the Python package for the Odoo module, making controllers and models available.  
**Logic Description:** Contains import statements for sub-modules/packages, e.g., 'from . import controllers'.  
**Documentation:**
    
    - **Summary:** Standard Odoo module __init__.py file.
    
**Namespace:** odoo.addons.dfr_farmer_portal  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_portal/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, data files, and assets.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - OdooModuleSystem
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Asset Bundling
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    
**Purpose:** Describes the DFR Farmer Self-Service Portal module to the Odoo system.  
**Logic Description:** Contains a Python dictionary with keys like 'name', 'version', 'summary', 'author', 'website', 'license', 'category', 'depends' (e.g., ['website', 'dfr_farmer_registry', 'dfr_dynamic_forms']), 'data' (listing XML view files), 'assets' (listing JS/CSS bundles), 'installable': True, 'application': False, 'auto_install': False.  
**Documentation:**
    
    - **Summary:** Defines metadata for the DFR Farmer Portal Odoo module.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** dfr_addons/dfr_farmer_portal/controllers/__init__.py  
**Description:** Initializer for the controllers package.  
**Template:** Odoo Python Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** controllers/__init__.py  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes controller classes available within the 'controllers' package.  
**Logic Description:** Imports specific controller files, e.g., 'from . import portal'.  
**Documentation:**
    
    - **Summary:** Initializes the Python controllers package for the DFR Farmer Portal module.
    
**Namespace:** odoo.addons.dfr_farmer_portal.controllers  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** dfr_addons/dfr_farmer_portal/controllers/portal.py  
**Description:** Main controller for the Farmer Self-Service Portal. Handles routes for pre-registration and dynamic form display/submission.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 1  
**Name:** portal  
**Type:** Controller  
**Relative Path:** controllers/portal.py  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - Model-View-Controller
    
**Members:**
    
    
**Methods:**
    
    - **Name:** farmer_preregistration_form  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public|@http.route('/farmer/register', type='http', auth='public', website=True, methods=['GET'])  
    - **Name:** farmer_preregistration_submit  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public|@http.route('/farmer/register', type='http', auth='public', website=True, methods=['POST'], csrf=True)  
    - **Name:** portal_dynamic_form_render  
**Parameters:**
    
    - self
    - form_id
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public|@http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['GET'])  
    - **Name:** portal_dynamic_form_submit  
**Parameters:**
    
    - self
    - form_id
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public|@http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['POST'], csrf=True)  
    
**Implemented Features:**
    
    - Farmer Pre-registration Form Display
    - Farmer Pre-registration Submission
    - Public Dynamic Form Display
    - Public Dynamic Form Submission
    
**Requirement Ids:**
    
    - REQ-FSSP-003
    - REQ-FSSP-004
    - REQ-FSSP-009
    
**Purpose:** Handles HTTP requests for portal pages, processes form submissions, and interacts with backend DFR services.  
**Logic Description:** farmer_preregistration_form: Renders the QWeb template for the pre-registration form. farmer_preregistration_submit: Validates submitted data. Calls services from DFR_MOD_FARMER_REGISTRY to create a farmer record with 'draft' or 'pending verification' status. Redirects to a confirmation page or shows errors. portal_dynamic_form_render: Fetches the specified dynamic form definition (using services from DFR_MOD_DYNAMIC_FORMS). Renders the QWeb template for displaying the dynamic form. portal_dynamic_form_submit: Validates submitted dynamic form data. Calls services from DFR_MOD_DYNAMIC_FORMS to process the submission and link it to the farmer. Redirects or shows errors. Ensures CSRF protection on POST routes.  
**Documentation:**
    
    - **Summary:** Defines HTTP endpoints and request handling logic for the Farmer Self-Service Portal.
    
**Namespace:** odoo.addons.dfr_farmer_portal.controllers.portal  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** dfr_addons/dfr_farmer_portal/views/assets.xml  
**Description:** XML file to register static assets (CSS, JS) for the Farmer Self-Service Portal.  
**Template:** Odoo XML View Template  
**Dependancy Level:** 0  
**Name:** assets  
**Type:** View  
**Relative Path:** views/assets.xml  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Management
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    - REQ-FSSP-013
    
**Purpose:** Declares CSS and JavaScript files to be loaded for the portal frontend.  
**Logic Description:** Uses Odoo's asset bundle mechanism. Defines a new asset bundle or inherits 'web.assets_frontend' to add custom CSS (portal_main.css, portal_accessibility.css) and JS (portal_preregistration.js, portal_dynamic_form.js, portal_accessibility.js) files.  
**Documentation:**
    
    - **Summary:** Manages the inclusion of static resources for the DFR Farmer Portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** View
    
- **Path:** dfr_addons/dfr_farmer_portal/views/portal_layout.xml  
**Description:** QWeb template for the common layout of the Farmer Self-Service Portal (header, footer, main content area). Implements country-specific branding placeholders and mobile responsiveness.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 1  
**Name:** portal_layout  
**Type:** View  
**Relative Path:** views/portal_layout.xml  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - Model-View-Template
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Portal Layout
    - Country Branding Placeholder
    - Mobile Responsive Design
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    - REQ-FSSP-013
    
**Purpose:** Provides a consistent look and feel for all portal pages, incorporating branding and responsiveness.  
**Logic Description:** Defines a main QWeb template inheriting from 'website.layout'. Includes sections for header (with country logo snippet), navigation, main content block (t-call='main_content_placeholder'), and footer. Uses Bootstrap classes for responsiveness. Ensures semantic HTML structure for WCAG compliance.  
**Documentation:**
    
    - **Summary:** Defines the main layout structure for the DFR Farmer Portal pages.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** View
    
- **Path:** dfr_addons/dfr_farmer_portal/views/portal_preregistration_templates.xml  
**Description:** QWeb templates for the farmer pre-registration form and confirmation page.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_preregistration_templates  
**Type:** View  
**Relative Path:** views/portal_preregistration_templates.xml  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - Model-View-Template
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Pre-registration Form UI
    - Submission Confirmation UI
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    - REQ-FSSP-003
    - REQ-FSSP-013
    
**Purpose:** Defines the user interface for farmers to pre-register and see submission status.  
**Logic Description:** Contains a QWeb template for the '/farmer/register' page, inheriting 'dfr_farmer_portal.portal_layout'. Defines form fields for full name, village, primary crop type, contact number, National ID (type and number) with appropriate input types and labels. Includes client-side validation hints. Implements ARIA attributes for accessibility. Another template for the registration confirmation/thank you page.  
**Documentation:**
    
    - **Summary:** Provides the QWeb templates for farmer pre-registration journey.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** View
    
- **Path:** dfr_addons/dfr_farmer_portal/views/portal_dynamic_form_templates.xml  
**Description:** QWeb templates for rendering and submitting publicly accessible dynamic forms.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_dynamic_form_templates  
**Type:** View  
**Relative Path:** views/portal_dynamic_form_templates.xml  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    - Model-View-Template
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dynamic Form Rendering on Portal
    - Dynamic Form Submission UI
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    - REQ-FSSP-009
    - REQ-FSSP-013
    
**Purpose:** Defines the user interface for farmers to view and submit additional information via dynamic forms.  
**Logic Description:** Contains a QWeb template for the '/portal/forms/{form_id}' page, inheriting 'dfr_farmer_portal.portal_layout'. Iterates through form fields passed from the controller and renders appropriate input elements based on field type. Handles display of labels, instructions, and validation messages. Implements ARIA attributes. Includes a template for submission confirmation.  
**Documentation:**
    
    - **Summary:** Provides QWeb templates for displaying and submitting dynamic forms on the portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** View
    
- **Path:** dfr_addons/dfr_farmer_portal/views/snippets/country_branding_snippet.xml  
**Description:** QWeb snippet for reusable country branding elements, like logos.  
**Template:** Odoo QWeb Snippet Template  
**Dependancy Level:** 1  
**Name:** country_branding_snippet  
**Type:** View  
**Relative Path:** views/snippets/country_branding_snippet.xml  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Country Branding Element
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    
**Purpose:** Encapsulates country-specific branding elements for easy inclusion in layouts.  
**Logic Description:** Defines a QWeb template (e.g., 'dfr_farmer_portal.s_country_logo') that displays a country logo. The logo source could be configurable or dynamically determined based on the current website context or a system parameter.  
**Documentation:**
    
    - **Summary:** Provides a reusable QWeb snippet for country-specific branding.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** View
    
- **Path:** dfr_addons/dfr_farmer_portal/static/src/js/portal_preregistration.js  
**Description:** JavaScript for client-side enhancements of the farmer pre-registration form, including validation and dynamic interactions.  
**Template:** Odoo JavaScript Template  
**Dependancy Level:** 0  
**Name:** portal_preregistration  
**Type:** JavaScript  
**Relative Path:** static/src/js/portal_preregistration.js  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initPreRegistrationFormValidation  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** handleNationalIdVisibility  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Client-side Pre-registration Form Validation
    - Pre-registration Form Dynamic Behavior
    
**Requirement Ids:**
    
    - REQ-FSSP-003
    - REQ-FSSP-013
    
**Purpose:** Enhances the usability and accessibility of the farmer pre-registration form.  
**Logic Description:** Uses Odoo's JavaScript framework or plain JavaScript. Implements client-side validation for fields like contact number format, National ID format (if applicable), required fields. May include logic to conditionally show/hide National ID fields based on selection. Ensures ARIA attributes are updated dynamically if needed for accessibility.  
**Documentation:**
    
    - **Summary:** Provides client-side logic for the farmer pre-registration form.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/static/src/js/portal_dynamic_form.js  
**Description:** JavaScript for client-side interactions and validation for dynamic forms rendered on the portal.  
**Template:** Odoo JavaScript Template  
**Dependancy Level:** 0  
**Name:** portal_dynamic_form  
**Type:** JavaScript  
**Relative Path:** static/src/js/portal_dynamic_form.js  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initDynamicFormInteractions  
**Parameters:**
    
    - formId
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** applyClientSideValidations  
**Parameters:**
    
    - formRules
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Dynamic Form Client-side Validation
    - Dynamic Form Client-side Conditional Logic
    
**Requirement Ids:**
    
    - REQ-FSSP-009
    - REQ-FSSP-013
    
**Purpose:** Handles client-side aspects of dynamic forms, such as conditional field display and basic validation.  
**Logic Description:** Interprets form field metadata (validation rules, conditional logic) passed from the server. Implements client-side validation for various field types. Handles showing/hiding fields based on conditional logic. Ensures WCAG compliance for dynamic elements.  
**Documentation:**
    
    - **Summary:** Provides client-side logic for dynamic forms on the portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/static/src/js/portal_accessibility.js  
**Description:** JavaScript dedicated to enhancing WCAG 2.1 AA compliance across the portal.  
**Template:** Odoo JavaScript Template  
**Dependancy Level:** 0  
**Name:** portal_accessibility  
**Type:** JavaScript  
**Relative Path:** static/src/js/portal_accessibility.js  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** enhanceKeyboardNavigation  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** manageAriaLiveRegions  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Accessibility Enhancements
    
**Requirement Ids:**
    
    - REQ-FSSP-013
    
**Purpose:** Provides specific JavaScript-based solutions to meet WCAG 2.1 AA guidelines where HTML/CSS alone are insufficient.  
**Logic Description:** May include functions to improve keyboard navigation focus management, manage ARIA live regions for dynamic updates, ensure proper handling of custom widgets, or provide alternative interactions for complex elements. This file is for specific JS-driven accessibility fixes.  
**Documentation:**
    
    - **Summary:** Contains JavaScript code specifically for improving portal accessibility.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/static/src/css/portal_main.css  
**Description:** Main CSS file for styling the Farmer Self-Service Portal. Includes styles for layout, responsiveness, and country-specific branding overrides.  
**Template:** CSS Stylesheet  
**Dependancy Level:** 0  
**Name:** portal_main  
**Type:** CSS  
**Relative Path:** static/src/css/portal_main.css  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Portal Styling
    - Mobile Responsiveness
    - Country Branding CSS
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    - REQ-FSSP-013
    
**Purpose:** Defines the visual appearance of the portal, ensuring it's responsive and brand-aligned.  
**Logic Description:** Contains CSS rules for overall portal layout, typography, form styling, buttons, header, footer. Uses media queries for responsiveness across desktop, tablet, and mobile devices. Includes classes for country-specific themes or branding elements (e.g., logo sizing, color overrides). Basic accessibility considerations like minimum font sizes and sufficient spacing.  
**Documentation:**
    
    - **Summary:** Provides core styling for the DFR Farmer Portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/static/src/css/portal_accessibility.css  
**Description:** CSS file dedicated to styles specifically required for WCAG 2.1 AA compliance.  
**Template:** CSS Stylesheet  
**Dependancy Level:** 0  
**Name:** portal_accessibility  
**Type:** CSS  
**Relative Path:** static/src/css/portal_accessibility.css  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Accessibility Styling
    
**Requirement Ids:**
    
    - REQ-FSSP-013
    
**Purpose:** Ensures the portal meets visual accessibility guidelines.  
**Logic Description:** Contains CSS rules for focus indicators (visible focus outlines), high contrast modes (if implemented as an option), ensuring text spacing, and other visual aspects of WCAG compliance. Styles for ARIA roles and states where necessary.  
**Documentation:**
    
    - **Summary:** Provides CSS styles to enhance portal accessibility as per WCAG guidelines.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/static/description/icon.png  
**Description:** Icon for the DFR Farmer Portal module, displayed in the Odoo apps list.  
**Template:** Image Resource  
**Dependancy Level:** 0  
**Name:** icon  
**Type:** Image  
**Relative Path:** static/description/icon.png  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Icon
    
**Requirement Ids:**
    
    
**Purpose:** Provides a visual identifier for the module in the Odoo interface.  
**Logic Description:** A PNG image, typically 128x128 pixels.  
**Documentation:**
    
    - **Summary:** Module icon for DFR Farmer Portal.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** StaticResource
    
- **Path:** dfr_addons/dfr_farmer_portal/i18n/dfr_farmer_portal.pot  
**Description:** Master translation template file (.pot) for all translatable strings in the DFR Farmer Portal module.  
**Template:** Odoo POT File  
**Dependancy Level:** 0  
**Name:** dfr_farmer_portal  
**Type:** Localization  
**Relative Path:** i18n/dfr_farmer_portal.pot  
**Repository Id:** DFR_MOD_FARMER_PORTAL  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Base
    
**Requirement Ids:**
    
    - REQ-FSSP-001
    
**Purpose:** Contains all user-facing strings extracted from Python code and XML views, ready for translation.  
**Logic Description:** Generated by Odoo's i18n tools. Lists all msgid/msgstr pairs. This file will be used to create language-specific .po files.  
**Documentation:**
    
    - **Summary:** Base translation template for the DFR Farmer Portal module.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Localization
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

