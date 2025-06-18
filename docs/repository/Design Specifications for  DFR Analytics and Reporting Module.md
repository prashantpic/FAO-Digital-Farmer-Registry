markdown
# Software Design Specification: DFR Analytics and Reporting Module

## 1. Introduction

This document outlines the software design for the DFR Analytics and Reporting Module (`dfr_analytics`). This Odoo 18.0 Community module is responsible for providing dashboards with real-time Key Performance Indicators (KPIs), map-based visualizations, data filtering capabilities, and exportable reports (CSV, XLSX, PDF) for farmer and dynamic form data. It is configured and accessed via the DFR Admin Portal.

**Project:** FAO-Digital Farmer Registry (DFR)
**Module ID:** DFR_MOD_ANALYTICS_REPORTING
**Namespace:** `odoo.addons.dfr_analytics`
**Output Path:** `dfr_addons/dfr_analytics`

## 2. Goals and Scope

The primary goal of this module is to provide authorized users with tools to analyze and visualize DFR data, enabling informed decision-making and operational oversight.

**In Scope:**
*   Displaying KPIs for farmer registrations, gender disaggregation, age distribution, landholding summaries, and registration trends. (REQ-7-001)
*   Providing map-based visualizations for farmer and plot locations. (REQ-7-002)
*   Allowing users to export reports and data extracts in CSV, XLSX, and PDF formats. (REQ-7-004)
*   Providing built-in dashboarding and exportable reporting for data collected through dynamic forms. (REQ-7-006)
*   Integration with `dfr_farmer_registry` and `dfr_dynamic_forms` modules for data sourcing.
*   Adherence to RBAC rules defined in `dfr_rbac_config`.

**Out of Scope:**
*   Definition of user roles and core permissions (handled by `dfr_rbac_config`).
*   Data capture for farmer registration or dynamic forms (handled by respective modules).
*   Advanced, highly customizable BI tool integration (beyond Odoo's native capabilities and specified export formats).

## 3. Architecture

The `dfr_analytics` module follows the **Modular Monolith** architecture style inherent to Odoo. It leverages Odoo's **Model-View-Controller (MVC) / Model-View-Template (MVT)** pattern for its web components.

**Key Architectural Layers (within this module's context):**
*   **Presentation Layer (`dfr_odoo_presentation`):**
    *   Odoo Admin Portal views (XML, OWL, JS) for dashboards and map visualizations.
    *   Wizard views (XML) for report export configuration.
    *   QWeb templates for PDF reports.
*   **Application Services Layer (`dfr_odoo_application_services`):**
    *   Python services (within Odoo models) to fetch, compute, and prepare data for presentation.
    *   Logic for handling report generation and export requests.

**Dependencies:**
*   `web` (Odoo core web module)
*   `board` (Odoo core dashboard module)
*   `dfr_farmer_registry` (for accessing farmer, household, plot data)
*   `dfr_dynamic_forms` (for accessing dynamic form definitions and submission data)
*   `dfr_rbac_config` (for ensuring access controls are respected)
*   (Optional, for evaluation) `web_map` or `web_google_maps` (OCA modules for map views)

## 4. Technology Stack

*   **Framework:** Odoo 18.0 Community
*   **Programming Languages:** Python 3.11.9, XML 1.0, JavaScript ES6+, OWL (Odoo Web Library)
*   **Core Technologies:** Odoo ORM, Odoo Dashboard Module, Odoo Reporting Engine (QWeb)
*   **Optional Third-party Libraries (to be evaluated):**
    *   `OCA/web_map`: For generic map views.
    *   `OCA/web_google_maps`: For Google Maps integration (if preferred and API keys are manageable).
    *   `Leaflet.js`: If more custom client-side map interactions are needed beyond OCA module capabilities.
*   **Data Formats for Export:** CSV, XLSX, PDF
*   **Data Format for Map GeoData:** GeoJSON

## 5. Detailed Design

### 5.1. Module Initialization and Manifest

#### 5.1.1. `__init__.py`
*   **Purpose:** Initializes the Python package for the module.
*   **Logic:**
    python
    # dfr_addons/dfr_analytics/__init__.py
    from . import models
    from . import wizards
    from . import report
    # Any other top-level Python submodules
    
*   **Requirements:** Module Initialization

#### 5.1.2. `__manifest__.py`
*   **Purpose:** Declares the module to Odoo.
*   **Logic:**
    python
    # dfr_addons/dfr_analytics/__manifest__.py
    {
        'name': 'DFR Analytics and Reporting',
        'version': '18.0.1.0.0',
        'summary': 'Provides dashboards, KPIs, map visualizations, and exportable reports for the DFR system.',
        'author': 'FAO DFR Project Team',
        'website': 'https://www.fao.org', # Replace with actual project website
        'category': 'DigitalFarmerRegistry/Reporting',
        'license': 'MIT', # Or Apache 2.0 as per final decision
        'depends': [
            'web',
            'board', # Odoo dashboard module
            'dfr_common', # Assuming a common core module
            'dfr_farmer_registry',
            'dfr_dynamic_forms',
            'dfr_rbac_config',
            # Add 'web_map' or 'web_google_maps' if decided to use
        ],
        'data': [
            'security/ir.model.access.csv',
            'views/assets.xml',
            'views/analytics_dashboard_views.xml',
            'views/map_visualization_views.xml',
            'views/report_actions_views.xml',
            'wizards/report_export_wizard_views.xml',
            'report/report_templates.xml',
            # Add menu entries XML files if separate
        ],
        'assets': {
            'web.assets_backend': [
                'dfr_analytics/static/src/scss/analytics_styles.scss',
                'dfr_analytics/static/src/js/dashboard_manager.js',
                'dfr_analytics/static/src/js/kpi_widget.js',
                'dfr_analytics/static/src/js/chart_widget.js',
                'dfr_analytics/static/src/js/map_view_component.js',
                'dfr_analytics/static/src/xml/dashboard_templates.xml',
                'dfr_analytics/static/src/xml/map_view_templates.xml',
                # Add Leaflet.js lib if used directly and not via OCA
                # 'dfr_analytics/static/lib/leaflet/leaflet.js',
                # 'dfr_analytics/static/lib/leaflet/leaflet.css',
            ],
        },
        'installable': True,
        'application': False, # This is an addon, not a standalone application
        'auto_install': False,
    }
    
*   **Requirements:** REQ-7-001, REQ-7-002, REQ-7-004, REQ-7-006, Module Definition, Dependency Management, Data File Loading

### 5.2. Models (`models/`)

#### 5.2.1. `models/__init__.py`
*   **Purpose:** Initializes Python models.
*   **Logic:**
    python
    # dfr_addons/dfr_analytics/models/__init__.py
    from . import analytics_service
    
*   **Requirements:** Model Package Initialization

#### 5.2.2. `models/analytics_service.py`
*   **Purpose:** Backend service layer for fetching and computing analytics data.
*   **Class:** `AnalyticsService` (inherits `models.TransientModel` or `models.AbstractModel` as it's primarily a service, not storing persistent data itself)
    *   `_name = 'dfr.analytics.service'`
    *   `_description = 'DFR Analytics Data Service'`
*   **Methods:**
    *   `get_farmer_registration_kpis(self, filters=None)`:
        *   **Purpose:** Fetches data for farmer registration KPIs.
        *   **Parameters:**
            *   `filters (dict, optional)`: Dictionary of filters to apply (e.g., date range, geographic area).
        *   **Returns:** `dict` containing:
            *   `total_registrations (int)`
            *   `gender_disaggregation (dict)`: e.g., `{'male': 100, 'female': 120, 'other': 5}`
            *   `age_distribution (dict)`: e.g., `{'<18': 10, '18-35': 80, ...}`
            *   `registration_trends (list)`: e.g., `[{'period': '2023-01', 'count': 50}, ...]`
        *   **Logic:**
            1.  Construct Odoo domain based on `filters`.
            2.  Query `dfr.farmer` model using `search_count()` for total.
            3.  Query `dfr.farmer` using `read_group()` for gender and age disaggregation. Age calculation might require Python logic if DOB is stored.
            4.  Query `dfr.farmer` grouping by creation date (e.g., month/year) for trends.
        *   **Requirements:** REQ-7-001

    *   `get_landholding_summary_kpis(self, filters=None)`:
        *   **Purpose:** Fetches data for landholding summary KPIs.
        *   **Parameters:**
            *   `filters (dict, optional)`: Filters.
        *   **Returns:** `dict` containing:
            *   `total_plots (int)`
            *   `total_land_area (float)`
            *   `average_plot_size (float)`
            *   `land_distribution_by_size (dict)`: e.g., `{'<1ha': 50, '1-5ha': 30, ...}`
        *   **Logic:**
            1.  Construct Odoo domain based on `filters` applied to `dfr.farmer` and linked `dfr.plot`.
            2.  Query `dfr.plot` for total count and sum of `plot_size`.
            3.  Calculate average.
            4.  Use `read_group()` or custom grouping on `plot_size` for distribution.
        *   **Requirements:** REQ-7-001

    *   `get_dynamic_form_submission_kpis(self, form_id=None, filters=None)`:
        *   **Purpose:** Fetches data for dynamic form submission KPIs.
        *   **Parameters:**
            *   `form_id (int, optional)`: ID of the `dfr.dynamic.form` to analyze. If None, may provide overview for all.
            *   `filters (dict, optional)`: Filters.
        *   **Returns:** `dict` containing:
            *   `total_submissions (int)`
            *   `submissions_per_form (dict)`: If `form_id` is None, `{'form_name1': count, ...}`
            *   `response_distribution (dict)`: For select/multi-select fields of a specific form, `{'field_label1': {'option1': count, ...}}` (requires more complex logic to inspect form fields and aggregate `dfr.form.response`).
        *   **Logic:**
            1.  Construct domain for `dfr.form.submission` based on `form_id` and `filters`.
            2.  Query for total submissions.
            3.  If `form_id` is given, iterate through its `dfr.form.field` definitions. For selection fields, query `dfr.form.response` to aggregate counts per option.
        *   **Requirements:** REQ-7-006

    *   `get_farmer_plot_geo_data(self, filters=None)`:
        *   **Purpose:** Fetches farmer homestead and plot geographical data.
        *   **Parameters:**
            *   `filters (dict, optional)`: Filters to apply to farmers/plots.
        *   **Returns:** `list` of `dict` in GeoJSON-like structure:
            *   e.g., `[{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [lng, lat]}, 'properties': {'farmer_uid': '...', 'name': '...'}}, ...]`
            *   e.g., `[{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[lng, lat], ...]]}, 'properties': {'plot_uid': '...', 'farmer_name': '...'}}, ...]`
        *   **Logic:**
            1.  Construct domain for `dfr.farmer` and `dfr.plot` based on `filters`.
            2.  Query `dfr.farmer` for homestead GPS coordinates (if stored on farmer model).
            3.  Query `dfr.plot` for plot GPS coordinates (point or polygon).
            4.  Format data into a list of GeoJSON-like features.
        *   **Requirements:** REQ-7-002

    *   `prepare_export_data(self, entity_type, filters=None, fields_to_export=None)`:
        *   **Purpose:** Prepares data for CSV/XLSX export.
        *   **Parameters:**
            *   `entity_type (str)`: e.g., 'farmer', 'plot', 'dynamic_form_X'.
            *   `filters (dict, optional)`: Filters.
            *   `fields_to_export (list, optional)`: List of field names to export.
        *   **Returns:** `list` of `dict`, where each dict is a row.
        *   **Logic:**
            1.  Determine the target Odoo model based on `entity_type`.
            2.  If `entity_type` is for a dynamic form, identify the specific form and its fields.
            3.  Construct domain based on `filters`.
            4.  Fetch records using `search_read()` with specified `fields_to_export`.
            5.  For dynamic forms, this will involve fetching `dfr.form.submission` and then joining/pivoting `dfr.form.response` data to create a flat structure with form field labels as column headers.
        *   **Requirements:** REQ-7-004, REQ-7-006

### 5.3. Security (`security/`)

#### 5.3.1. `security/ir.model.access.csv`
*   **Purpose:** Define model-level access rights.
*   **Logic:**
    csv
    id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
    access_dfr_analytics_service,dfr.analytics.service access,model_dfr_analytics_service,base.group_user,1,0,0,0
    access_dfr_report_export_wizard,dfr.report.export.wizard access,model_dfr_report_export_wizard,base.group_user,1,1,1,1 
    # Add entries for any other custom models if created (e.g., report specific models)
    # Access to dfr.farmer, dfr.plot, dfr.form.submission etc. is managed by their respective modules.
    # This module primarily reads data, so perm_read=1 for base.group_user on service models is often sufficient.
    # Specific admin roles (e.g., National Admin, Policy Maker) might need explicit read access granted via dfr_rbac_config or here if those groups are defined globally.
    
*   **Requirements:** REQ-7-001, REQ-7-002, REQ-7-004, REQ-7-006, Model Access Control

### 5.4. Wizards (`wizards/`)

#### 5.4.1. `wizards/__init__.py`
*   **Purpose:** Initializes Python wizards.
*   **Logic:**
    python
    # dfr_addons/dfr_analytics/wizards/__init__.py
    from . import report_export_wizard
    
*   **Requirements:** Wizard Package Initialization

#### 5.4.2. `wizards/report_export_wizard.py`
*   **Purpose:** Model for the report export wizard UI.
*   **Class:** `ReportExportWizard` (inherits `models.TransientModel`)
    *   `_name = 'dfr.report.export.wizard'`
    *   `_description = 'DFR Report Export Wizard'`
    *   **Fields:**
        *   `report_type (fields.Selection)`: Selection of what to export (e.g., `[('farmer_core_data', 'Farmer Core Data'), ('farmer_plot_data', 'Farmer Plot Data'), ('dynamic_form_data', 'Dynamic Form Data')]`).
        *   `dynamic_form_id (fields.Many2one)`: `'dfr.dynamic.form'`, string="Dynamic Form", help="Select if exporting dynamic form data." Conditionally visible.
        *   `date_from (fields.Date)`: "Date From"
        *   `date_to (fields.Date)`: "Date To"
        *   `geographic_area_ids (fields.Many2many)`: `'dfr.administrative.area'`, string="Geographic Areas" (assuming `dfr.administrative.area` model exists in `dfr_farmer_registry` or `dfr_common`).
        *   `farmer_status_ids (fields.Many2many)`: `'dfr.farmer.status'`, string="Farmer Statuses" (assuming `dfr.farmer.status` model or selection field exists).
        *   `export_format (fields.Selection)`: `[('csv', 'CSV'), ('xlsx', 'Excel XLSX')]`, default='csv', required=True.
        *   `data_file (fields.Binary)`: "Exported File", readonly=True.
        *   `file_name (fields.Char)`: "File Name", readonly=True.
*   **Methods:**
    *   `action_export_report(self)`:
        *   **Purpose:** Generates and provides the report file for download.
        *   **Logic:**
            1.  `self.ensure_one()`
            2.  Construct `filters` dictionary from wizard fields (`date_from`, `date_to`, `geographic_area_ids`, `farmer_status_ids`).
            3.  Call appropriate method on `self.env['dfr.analytics.service']` (e.g., `prepare_export_data`) with `self.report_type`, `filters`, and `self.dynamic_form_id.id` if applicable.
            4.  Receive list of dictionaries (data rows).
            5.  If `self.export_format == 'csv'`:
                *   Use `io.StringIO` and `csv.writer` to generate CSV data.
                *   Encode to `base64`.
                *   Set `self.data_file` and `self.file_name` (e.g., `f"{self.report_type}_export.csv"`).
            6.  If `self.export_format == 'xlsx'`:
                *   Use `openpyxl` (add to manifest dependencies if not already available system-wide or via another module).
                *   Create workbook, worksheet, write headers and data.
                *   Save to `io.BytesIO`.
                *   Encode to `base64`.
                *   Set `self.data_file` and `self.file_name` (e.g., `f"{self.report_type}_export.xlsx"`).
            7.  Return an action to re-open the wizard in the same view (form view), so the download link for `data_file` becomes active.
                python
                # Example return structure
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'view_mode': 'form',
                    'res_id': self.id,
                    'views': [(False, 'form')],
                    'target': 'new',
                }
                
        *   **Requirements:** REQ-7-004, REQ-7-006, Custom Report Export Logic

### 5.5. Reports (`report/`)

#### 5.5.1. `report/__init__.py`
*   **Purpose:** Initializes Python report logic.
*   **Logic:**
    python
    # dfr_addons/dfr_analytics/report/__init__.py
    from . import farmer_data_export_reports
    from . import dynamic_form_data_export_reports
    
*   **Requirements:** Report Logic Package Initialization

#### 5.5.2. `report/farmer_data_export_reports.py`
*   **Purpose:** Backend logic for PDF reports on farmer data.
*   **Class:** `FarmerStatisticsPdfReport` (inherits `models.AbstractModel`)
    *   `_name = 'report.dfr_analytics.report_farmer_statistics_pdf'` (matches `report_name` in XML)
    *   `_description = 'Farmer Statistics PDF Report'`
*   **Methods:**
    *   `_get_report_values(self, docids, data=None)`:
        *   **Purpose:** Prepares data for the QWeb PDF template.
        *   **Parameters:**
            *   `docids (list)`: List of IDs of records to report on (typically `dfr.farmer` IDs if called directly on records, or empty if called from a wizard).
            *   `data (dict, optional)`: Data passed from a wizard or action context (contains filters).
        *   **Returns:** `dict` to be passed to QWeb template (e.g., `{'doc_ids': docids, 'doc_model': 'dfr.farmer', 'docs': farmers, 'report_data': kpi_data}`).
        *   **Logic:**
            1.  Extract filters from `data` if provided.
            2.  Fetch farmer records based on `docids` or filtered criteria using `self.env['dfr.analytics.service']`.
            3.  Fetch relevant KPI data using `self.env['dfr.analytics.service']`.
            4.  Structure data for the QWeb template.
        *   **Requirements:** REQ-7-004, PDF Report Data Preparation (Farmer Data)

#### 5.5.3. `report/dynamic_form_data_export_reports.py`
*   **Purpose:** Backend logic for PDF reports on dynamic form data.
*   **Class:** `DynamicFormSummaryPdfReport` (inherits `models.AbstractModel`)
    *   `_name = 'report.dfr_analytics.report_dynamic_form_summary_pdf'`
    *   `_description = 'Dynamic Form Submission Summary PDF Report'`
*   **Methods:**
    *   `_get_report_values(self, docids, data=None)`:
        *   **Purpose:** Prepares data for QWeb PDF.
        *   **Parameters:**
            *   `docids (list)`: Typically `dfr.form.submission` IDs or `dfr.dynamic.form` ID.
            *   `data (dict, optional)`: Filters, form ID.
        *   **Returns:** `dict` for QWeb.
        *   **Logic:**
            1.  Extract `form_id` and filters from `data`.
            2.  Fetch dynamic form submissions and aggregated response data using `self.env['dfr.analytics.service']`.
            3.  Structure data for QWeb template.
        *   **Requirements:** REQ-7-006, PDF Report Data Preparation (Dynamic Form Data)

### 5.6. Static Assets (`static/`)

#### 5.6.1. `static/src/js/dashboard_manager.js`
*   **Purpose:** Main OWL component for the DFR Analytics Dashboard.
*   **Class:** `DashboardManager` (extends `Component`, uses `useState`, `onWillStart`, `onMounted`)
    *   **State (`kpiData`, `chartData`):** Initialized as empty objects/arrays.
    *   `onWillStart()`:
        *   Makes RPC call to `dfr.analytics.service` methods (e.g., `get_farmer_registration_kpis`, `get_landholding_summary_kpis`) to fetch initial data.
        *   Updates component state with fetched data.
    *   `updateDashboardData(filters)`:
        *   Method to be called when filters change.
        *   Makes RPC calls with new filters.
        *   Updates state.
    *   **Template:** `dfr_analytics.DashboardManager` (defined in `dashboard_templates.xml`)
        *   Renders various `KpiWidget` and `ChartWidget` components, passing relevant data from its state.
        *   May include filter components (date pickers, dropdowns for geographic areas).
*   **Requirements:** REQ-7-001, REQ-7-006, Dashboard Layout, KPI Display, Chart Display

#### 5.6.2. `static/src/js/kpi_widget.js`
*   **Purpose:** Reusable OWL component for displaying a single KPI.
*   **Class:** `KpiWidget` (extends `Component`)
    *   **Props:** `title (String)`, `value (String | Number)`, `icon (String, optional)`, `trend (String, optional: "up", "down", "neutral")`, `percentage_change (String, optional)`.
    *   **Template:** `dfr_analytics.KpiWidget`
*   **Requirements:** REQ-7-001, REQ-7-006, KPI Value Display

#### 5.6.3. `static/src/js/chart_widget.js`
*   **Purpose:** Reusable OWL component for displaying charts.
*   **Class:** `ChartWidget` (extends `Component`, uses `onMounted`, `useRef`)
    *   **Props:** `chartType (String)`, `chartData (Object)`, `chartOptions (Object, optional)`.
    *   `canvasRef = useRef("canvas")`
    *   `onMounted()`:
        *   Initializes a chart using a library like Chart.js (if bundled/available) on the `canvasRef.el`.
        *   Uses `this.props.chartType`, `this.props.chartData`, `this.props.chartOptions`.
    *   `onWillUpdateProps(nextProps)`:
        *   If chart library instance exists, update it with `nextProps`.
    *   `onWillUnmount()`:
        *   Destroy chart instance to prevent memory leaks.
    *   **Template:** `dfr_analytics.ChartWidget` (contains a `<canvas>`)
*   **Requirements:** REQ-7-001, REQ-7-006, Chart Visualization

#### 5.6.4. `static/src/js/map_view_component.js`
*   **Purpose:** OWL component for map-based visualizations.
*   **Class:** `MapViewComponent` (extends `Component`, uses `useState`, `onWillStart`, `onMounted`, `useRef`)
    *   **State (`geoData`):** Initialized as `null` or empty.
    *   `mapRef = useRef("mapContainer")`
    *   `mapInstance = null`
    *   `onWillStart()`:
        *   Makes RPC call to `dfr.analytics.service` method `get_farmer_plot_geo_data` to fetch initial GeoJSON data.
        *   Updates `this.state.geoData`.
    *   `onMounted()`:
        *   Load Leaflet.js library if not already loaded globally or via assets.
        *   Initialize Leaflet map on `this.mapRef.el`.
        *   Set initial view (center, zoom).
        *   Add tile layer (e.g., OpenStreetMap).
        *   If `this.state.geoData` is available, create `L.geoJSON` layer and add to map.
    *   `updateMapFeatures(newGeoData)`:
        *   Clears existing features from `mapInstance`.
        *   Adds new features from `newGeoData`.
    *   **Template:** `dfr_analytics.MapViewComponent`
*   **Requirements:** REQ-7-002, Map-based Data Visualization
*   **Note:** If using OCA `web_map` or `web_google_maps`, this component might not be custom OWL but rather configuring Odoo's map view type in XML. If a fully custom Leaflet integration is chosen, ensure Leaflet library files are included in `static/lib/` and registered in `assets.xml`.

#### 5.6.5. `static/src/xml/dashboard_templates.xml`
*   **Purpose:** QWeb/OWL templates for dashboard components.
*   **Content:**
    *   `dfr_analytics.DashboardManager`: Main layout, sections for different KPIs/charts, filter area.
    *   `dfr_analytics.KpiWidget`: Structure to display title, value, icon, trend.
    *   `dfr_analytics.ChartWidget`: A `<div>` containing a `<canvas>` element for chart rendering.
*   **Requirements:** REQ-7-001, REQ-7-006, Dashboard UI Structure

#### 5.6.6. `static/src/xml/map_view_templates.xml`
*   **Purpose:** QWeb/OWL template for the map component.
*   **Content:**
    *   `dfr_analytics.MapViewComponent`: A `<div>` with a specific ID (e.g., `id="dfr-map-container"`) to serve as the Leaflet map container. This div should have appropriate styling for height/width.
*   **Requirements:** REQ-7-002, Map View UI Structure

#### 5.6.7. `static/src/scss/analytics_styles.scss`
*   **Purpose:** Custom SCSS/CSS styles.
*   **Content:** Styles for:
    *   Dashboard layout (spacing, borders).
    *   KPI widget appearance (colors, font sizes).
    *   Chart container styling.
    *   Map container styling (height, width, borders).
    *   Leaflet pop-up styling if customized.
*   **Requirements:** REQ-7-001, REQ-7-002, REQ-7-006, Custom UI Styling

### 5.7. Views (`views/`)

#### 5.7.1. `views/assets.xml`
*   **Purpose:** Register static assets.
*   **Logic:**
    xml
    <odoo>
        <data>
            <template id="assets_backend_dfr_analytics" name="DFR Analytics Assets" inherit_id="web.assets_backend">
                <xpath expr="." position="inside">
                    <link rel="stylesheet" type="text/scss" href="/dfr_analytics/static/src/scss/analytics_styles.scss"/>
                    <!-- Uncomment if Leaflet is bundled directly -->
                    <!-- <link rel="stylesheet" type="text/css" href="/dfr_analytics/static/lib/leaflet/leaflet.css"/> -->
                    <!-- <script type="text/javascript" src="/dfr_analytics/static/lib/leaflet/leaflet.js"></script> -->
                    
                    <script type="text/javascript" src="/dfr_analytics/static/src/js/kpi_widget.js"></script>
                    <script type="text/javascript" src="/dfr_analytics/static/src/js/chart_widget.js"></script>
                    <script type="text/javascript" src="/dfr_analytics/static/src/js/map_view_component.js"></script>
                    <script type="text/javascript" src="/dfr_analytics/static/src/js/dashboard_manager.js"></script>
                </xpath>
            </template>
        </data>
    </odoo>
    
*   **Requirements:** REQ-7-001, REQ-7-002, REQ-7-006, Static Asset Registration

#### 5.7.2. `views/analytics_dashboard_views.xml`
*   **Purpose:** Define Odoo views for the analytics dashboard.
*   **Logic:**
    xml
    <odoo>
        <data>
            <!-- Client Action for the Dashboard -->
            <record id="dfr_analytics_dashboard_action" model="ir.actions.client">
                <field name="name">DFR Analytics Dashboard</field>
                <field name="tag">dfr_analytics.DashboardManager</field>
                <!-- Add context or params if needed by DashboardManager OWL component -->
            </record>

            <!-- Main Menu Item -->
            <menuitem id="menu_dfr_analytics_root"
                      name="DFR Analytics"
                      sequence="150" 
                      web_icon="dfr_analytics,static/description/icon.png"/> 
                      <!-- Ensure icon.png exists -->

            <menuitem id="menu_dfr_analytics_dashboard"
                      name="Dashboard"
                      parent="menu_dfr_analytics_root"
                      action="dfr_analytics_dashboard_action"
                      sequence="10"/>
        </data>
    </odoo>
    
*   **Requirements:** REQ-7-001, REQ-7-006, Dashboard View Definition, Dashboard Menu Access

#### 5.7.3. `views/map_visualization_views.xml`
*   **Purpose:** Define Odoo views for map visualizations.
*   **Logic:**
    xml
    <odoo>
        <data>
            <!-- Client Action for Map View -->
            <record id="dfr_map_visualization_action" model="ir.actions.client">
                <field name="name">Farmer &amp; Plot Map</field>
                <field name="tag">dfr_analytics.MapViewComponent</field>
                 <!-- If using OCA web_map, this would be different:
                <field name="res_model">dfr.plot</field>  Or dfr.farmer
                <field name="view_mode">map,tree,form</field> 
                <field name="view_id" ref="view_dfr_plot_map"/> This map view needs to be defined
                -->
            </record>

            <menuitem id="menu_dfr_map_visualization"
                      name="Map View"
                      parent="menu_dfr_analytics_root"
                      action="dfr_map_visualization_action"
                      sequence="20"/>
            
            <!-- Example of an Odoo Map View if using OCA web_map for Plots -->
            <!-- This would require dfr.plot to have latitude and longitude fields recognized by web_map -->
            <!-- <record id="view_dfr_plot_map" model="ir.ui.view">
                <field name="name">dfr.plot.map</field>
                <field name="model">dfr.plot</field> 
                <field name="arch" type="xml">
                    <map_view 
                        latitude="gps_latitude_field_name" 
                        longitude="gps_longitude_field_name"
                        color="farmer_id" 
                        library="leaflet" <!-- or 'google' if web_google_maps -->
                    <!-- Add more map view options as needed -->
                    <!-- >
                        <field name="name"/>
                        <field name="farmer_id"/>
                    </map_view> 
                </field>
            </record> -->

        </data>
    </odoo>
    
*   **Requirements:** REQ-7-002, Map View Definition, Map View Menu Access

#### 5.7.4. `views/report_actions_views.xml`
*   **Purpose:** Define menu items for report export functionalities.
*   **Logic:**
    xml
    <odoo>
        <data>
            <!-- Sub-menu for Reports -->
            <menuitem id="menu_dfr_analytics_reports_sub"
                      name="Reports &amp; Exports"
                      parent="menu_dfr_analytics_root"
                      sequence="30"/>

            <!-- Action to open Report Export Wizard -->
            <record id="action_dfr_report_export_wizard" model="ir.actions.act_window">
                <field name="name">Export DFR Data</field>
                <field name="res_model">dfr.report.export.wizard</field>
                <field name="view_mode">form</field>
                <field name="target">new</field>
            </record>

            <menuitem id="menu_dfr_report_export_wizard_item"
                      name="Custom Data Export (CSV/XLSX)"
                      parent="menu_dfr_analytics_reports_sub"
                      action="action_dfr_report_export_wizard"
                      sequence="10"/>

            <!-- Example for a direct PDF report -->
            <record id="action_report_farmer_statistics" model="ir.actions.report">
                <field name="name">Farmer Statistics (PDF)</field>
                <field name="model">dfr.farmer</field> <!-- Or a wizard if it needs parameters -->
                <field name="report_type">qweb-pdf</field>
                <field name="report_name">dfr_analytics.report_farmer_statistics_pdf</field>
                <field name="report_file">dfr_analytics.report_farmer_statistics_pdf</field>
                <field name="binding_model_id" eval="False"/> <!-- Not bound to model actions by default -->
            </record>

             <menuitem id="menu_dfr_report_farmer_statistics_pdf"
                      name="Farmer Statistics (PDF)"
                      parent="menu_dfr_analytics_reports_sub"
                      action="action_report_farmer_statistics"
                      sequence="20"/>
            
            <!-- Add similar for dynamic form PDF reports -->

        </data>
    </odoo>
    
*   **Requirements:** REQ-7-004, REQ-7-006, Report Export Menu Access

#### 5.7.5. `wizards/report_export_wizard_views.xml`
*   **Purpose:** XML view for the Report Export Wizard.
*   **Logic:**
    xml
    <odoo>
        <data>
            <record id="view_dfr_report_export_wizard_form" model="ir.ui.view">
                <field name="name">dfr.report.export.wizard.form</field>
                <field name="model">dfr.report.export.wizard</field>
                <field name="arch" type="xml">
                    <form string="Export DFR Data">
                        <group>
                            <group>
                                <field name="report_type"/>
                                <field name="dynamic_form_id" 
                                       attrs="{'invisible': [('report_type', '!=', 'dynamic_form_data')], 
                                                'required': [('report_type', '=', 'dynamic_form_data')]}"/>
                                <field name="export_format"/>
                            </group>
                            <group string="Filters">
                                <field name="date_from"/>
                                <field name="date_to"/>
                                <field name="geographic_area_ids" widget="many2many_tags"/>
                                <field name="farmer_status_ids" widget="many2many_tags"/>
                            </group>
                        </group>
                        <group attrs="{'invisible': [('data_file', '=', False)]}">
                             <field name="data_file" readonly="1" filename="file_name"/>
                             <field name="file_name" invisible="1"/>
                        </group>
                        <footer>
                            <button name="action_export_report" string="Generate Export" type="object" class="btn-primary"/>
                            <button string="Cancel" class="btn-secondary" special="cancel"/>
                        </footer>
                    </form>
                </field>
            </record>
        </data>
    </odoo>
    
*   **Requirements:** REQ-7-004, REQ-7-006, Report Export Wizard UI

#### 5.7.6. `report/report_templates.xml`
*   **Purpose:** QWeb templates for PDF reports.
*   **Logic:**
    xml
    <odoo>
        <data>
            <!-- Farmer Statistics PDF Report Template -->
            <template id="report_farmer_statistics_pdf_document">
                <t t-call="web.html_container">
                    <t t-foreach="docs" t-as="doc"> <!-- if iterating specific farmer records -->
                        <t t-call="web.external_layout">
                            <div class="page">
                                <h2>Farmer Statistics Report</h2>
                                <p>Report Date: <span t-esc="context_timestamp(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M')"/></p>
                                
                                <!-- Example KPI Display -->
                                <div class="row">
                                    <div class="col-6">Total Registered Farmers: <span t-esc="report_data.get('total_registrations')"/></div>
                                </div>
                                <!-- Gender Disaggregation Table -->
                                <h3>Gender Disaggregation</h3>
                                <table class="table table-sm">
                                    <thead><tr><th>Gender</th><th>Count</th></tr></thead>
                                    <tbody>
                                        <t t-foreach="report_data.get('gender_disaggregation', {})" t-as="gender_count">
                                            <tr>
                                                <td t-esc="gender_count_key"/>
                                                <td t-esc="gender_count_value"/>
                                            </tr>
                                        </t>
                                    </tbody>
                                </table>
                                <!-- Add more sections for age, landholding, trends -->
                            </div>
                        </t>
                    </t>
                </t>
            </template>

            <template id="report_farmer_statistics_pdf">
                 <t t-call="web.basic_layout">
                    <t t-foreach="docs if docs else [0]" t-as="o"> <!-- Handle if docs is empty for general report -->
                        <t t-call="dfr_analytics.report_farmer_statistics_pdf_document" t-lang="o.partner_id.lang if o and o.partner_id else user.lang"/>
                    </t>
                 </t>
            </template>

            <!-- Dynamic Form Summary PDF Report Template -->
            <template id="report_dynamic_form_summary_pdf_document">
                 <t t-call="web.html_container">
                    <t t-foreach="docs" t-as="form_submission_doc"> <!-- if iterating submissions, or just one doc for summary -->
                        <t t-call="web.external_layout">
                             <div class="page">
                                <h2>Dynamic Form: <span t-esc="report_data.get('form_name')"/> - Summary Report</h2>
                                <p>Total Submissions: <span t-esc="report_data.get('total_submissions')"/></p>
                                <!-- Display response distributions, etc. -->
                                <t t-foreach="report_data.get('response_distribution', {})" t-as="field_summary">
                                    <h3><t t-esc="field_summary_key"/></h3>
                                    <table class="table table-sm">
                                        <thead><tr><th>Option</th><th>Count</th></tr></thead>
                                        <tbody>
                                             <t t-foreach="field_summary_value" t-as="option_data">
                                                <tr>
                                                    <td t-esc="option_data_key"/>
                                                    <td t-esc="option_data_value"/>
                                                </tr>
                                            </t>
                                        </tbody>
                                    </table>
                                </t>
                            </div>
                        </t>
                    </t>
                </t>
            </template>
            
            <template id="report_dynamic_form_summary_pdf">
                 <t t-call="web.basic_layout">
                    <t t-foreach="docs if docs else [0]" t-as="o">
                        <t t-call="dfr_analytics.report_dynamic_form_summary_pdf_document" t-lang="user.lang"/>
                    </t>
                 </t>
            </template>

            <!-- Report Actions for PDF reports are defined in views/report_actions_views.xml -->
            <!-- Make sure report_name in ir.actions.report matches the template id -->

        </data>
    </odoo>
    
*   **Requirements:** REQ-7-004, REQ-7-006, PDF Report Templates, Report Action Definitions

## 6. Data Model (Relevant to this module)

This module primarily reads from and aggregates data from other DFR modules (`dfr_farmer_registry`, `dfr_dynamic_forms`). It introduces transient models for wizards.

*   **`dfr.analytics.service` (TransientModel/AbstractModel):** Defined in 5.2.2. Does not store persistent data.
*   **`dfr.report.export.wizard` (TransientModel):** Defined in 5.4.2. Stores temporary user input for report generation.

## 7. User Interface Design Highlights

*   **Analytics Dashboard:**
    *   Clean, intuitive layout using Odoo's dashboard capabilities, enhanced with OWL components.
    *   Prominent display of KPIs (REQ-7-001).
    *   Interactive charts for trends and distributions (REQ-7-001, REQ-7-006).
    *   Filters (date, geography, etc.) to refine dashboard data.
*   **Map Visualization View:**
    *   Interactive map (Leaflet or OCA component based).
    *   Markers for farmer/plot locations, potentially with pop-ups showing basic info on click (REQ-7-002).
    *   Ability to filter data displayed on the map.
*   **Report Export Wizard:**
    *   Simple form for selecting report type, export format, and applying filters (REQ-7-004, REQ-7-006).
    *   Clear download link for the generated file.
*   **PDF Reports:**
    *   Professionally formatted using QWeb, including headers, footers, and clear data presentation.

## 8. Error Handling

*   **Backend Services (`analytics_service.py`):**
    *   Gracefully handle cases where data is not found (e.g., return empty lists/dicts or appropriate messages).
    *   Log any unexpected ORM or calculation errors.
    *   Raise user-friendly `UserError` for invalid input parameters if methods are called incorrectly.
*   **OWL Components (JavaScript):**
    *   Display user-friendly error messages if RPC calls to the backend fail.
    *   Handle missing or malformed data gracefully (e.g., display "N/A" or a placeholder).
    *   Validate user input in filter components.
*   **Report Export Wizard:**
    *   Validate user input (e.g., date ranges).
    *   Provide clear error messages if report generation fails.
    *   Handle potential errors during file generation (CSV, XLSX).
*   **QWeb PDF Reports:**
    *   Templates should handle missing data gracefully to avoid rendering errors.

## 9. Security Considerations

*   All views, actions, and server methods within this module must respect Odoo's standard access control mechanisms. Access to dashboards, specific KPIs, map views, and export functionalities will be controlled by user roles defined in the `dfr_rbac_config` module.
*   The `analytics_service.py` methods will perform data fetching respecting the current user's access rights (Odoo ORM handles this implicitly if `sudo()` is not misused).
*   No sensitive data should be hardcoded in client-side JavaScript.
*   Data exported must be based on the user's permissions.

## 10. Performance Considerations

*   **KPI Calculation:**
    *   Optimize ORM queries in `analytics_service.py` using `read_group`, appropriate domains, and minimizing fetched fields.
    *   Consider caching aggregated results for frequently accessed, non-volatile KPIs if performance becomes an issue (though Odoo's ORM caching might suffice).
*   **Dashboard Loading:**
    *   Load initial dashboard data efficiently.
    *   Implement filters that trigger targeted data refresh rather than full reloads.
*   **Map Visualization:**
    *   For large datasets, implement server-side clustering or bounding box queries to fetch only visible map data if using a custom Leaflet solution. OCA `web_map` might have its own optimizations.
    *   Lazy load map tiles.
*   **Data Export:**
    *   For large exports, consider asynchronous processing or batching if synchronous generation leads to timeouts. Odoo's default export is generally optimized for reasonable datasets.
*   **Database Indexing:** Ensure fields used in common filters and groupings (e.g., creation dates, status fields, geographic identifiers, farmer ID in plot/submission tables) within `dfr_farmer_registry` and `dfr_dynamic_forms` are appropriately indexed. This is primarily the responsibility of those modules but impacts this analytics module.

## 11. Scalability

*   The design relies on Odoo's inherent scalability for handling concurrent users accessing dashboards and reports.
*   Efficient backend queries in `analytics_service.py` are crucial for maintaining performance as data volume grows.
*   The use of Odoo's dashboard module and client actions allows for standard Odoo scaling practices (e.g., multiple workers).

## 12. Internationalization and Localization

*   All user-facing strings in XML views, OWL templates, and Python code (e.g., wizard field labels, messages) must be translatable using Odoo's standard `_()` method or `t-translation` attributes.
*   Report templates (QWeb) must support translation.
*   The module itself does not introduce new languages but will respect the languages configured in Odoo and provide translatable strings.

## 13. Testing Strategy

*   **Unit Tests (Python):**
    *   Test methods in `analytics_service.py` with mock data to verify KPI calculations and data preparation logic.
    *   Test `report_export_wizard.py` methods for correct filter processing and data generation for CSV/XLSX.
    *   Test report model methods (`_get_report_values`) for correct data fetching for PDF reports.
*   **Integration Tests (Python/Odoo):**
    *   Test interactions between `analytics_service.py` and actual `dfr_farmer_registry`, `dfr_dynamic_forms` models using a test database.
    *   Verify report generation (CSV, XLSX, PDF) through Odoo's reporting engine and wizard actions.
*   **UI Tests (JavaScript/OWL):**
    *   Test OWL components (`DashboardManager`, `KpiWidget`, `ChartWidget`, `MapViewComponent`) for correct rendering, data display, and basic interactivity using Odoo's JavaScript test framework (QUnit).
    *   Verify RPC calls from OWL components fetch and display data correctly.
*   **Manual Testing:**
    *   Verify dashboard layout and functionality across different browsers.
    *   Test map interactions (zoom, pan, markers).
    *   Test report export functionality (filters, formats, content correctness).
    *   Validate access control for different user roles.

## 14. Deployment Considerations

*   This module will be deployed as part of the standard Odoo addon deployment process.
*   Dependencies listed in `__manifest__.py` must be installed.
*   If OCA map modules are used, they need to be available in the addons path.
*   If Leaflet.js is bundled directly, ensure `static/lib` contents are correctly deployed and accessible.
*   Initial setup might involve configuring default dashboard layouts or views for specific user roles if needed.

## 15. Future Enhancements (Considerations)

*   More advanced charting options or integration with dedicated BI visualization libraries if Odoo's native capabilities are limiting.
*   User-configurable dashboard widgets.
*   Support for saving and sharing custom filter sets for dashboards and reports.
*   Performance optimizations for extremely large datasets (e.g., materialized views for KPIs, advanced caching).
*   Integration with external BI platforms via API if required.
