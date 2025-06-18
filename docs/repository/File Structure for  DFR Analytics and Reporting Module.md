# Specification

# 1. Files

- **Path:** dfr_addons/dfr_analytics/__init__.py  
**Description:** Initializes the Python package for the DFR Analytics and Reporting Odoo module, importing submodules like models, wizards, controllers, and reports.  
**Template:** Odoo Python Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** __init__.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python modules within 'dfr_analytics' available for import.  
**Logic Description:** Contains import statements for controllers, models, wizards, and report sub-packages.  
**Documentation:**
    
    - **Summary:** Root __init__.py for the dfr_analytics Odoo module.
    
**Namespace:** odoo.addons.dfr_analytics  
**Metadata:**
    
    - **Category:** Module Definition
    
- **Path:** dfr_addons/dfr_analytics/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, and data files to be loaded (views, security, reports, assets).  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Loading
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Declares the dfr_analytics module to Odoo, specifying its properties, dependencies, and the XML/CSV/data files it uses.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'depends', 'data', 'assets'. Dependencies will include 'web', 'board', 'dfr_farmer_registry', 'dfr_dynamic_forms', 'dfr_rbac_config'. Data files will list XML views, security rules, report definitions, etc.  
**Documentation:**
    
    - **Summary:** Manifest file for the DFR Analytics and Reporting module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Module Definition
    
- **Path:** dfr_addons/dfr_analytics/models/__init__.py  
**Description:** Initializes the Python package for Odoo models within the dfr_analytics module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** models/__init__.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all model files defined within the 'models' directory.  
**Logic Description:** Contains import statements for each Python model file (e.g., 'from . import analytics_service').  
**Documentation:**
    
    - **Summary:** __init__.py for the models directory of dfr_analytics.
    
**Namespace:** odoo.addons.dfr_analytics.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/models/analytics_service.py  
**Description:** Python model (potentially a TransientModel or regular Model if data needs to be stored/cached) providing services to fetch and compute data for dashboards and reports. This acts as a backend service layer for analytics.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** analytics_service  
**Type:** Model  
**Relative Path:** models/analytics_service.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** get_farmer_registration_kpis  
**Parameters:**
    
    - filters=None
    
**Return Type:** dict  
**Attributes:** public|api.model  
**Purpose:** Fetches data for farmer registration KPIs: total registrations, gender disaggregation, age distribution, registration trends.  
    - **Name:** get_landholding_summary_kpis  
**Parameters:**
    
    - filters=None
    
**Return Type:** dict  
**Attributes:** public|api.model  
**Purpose:** Fetches data for landholding summary KPIs.  
    - **Name:** get_dynamic_form_submission_kpis  
**Parameters:**
    
    - form_id=None
    - filters=None
    
**Return Type:** dict  
**Attributes:** public|api.model  
**Purpose:** Fetches data for KPIs related to dynamic form submissions.  
    - **Name:** get_farmer_plot_geo_data  
**Parameters:**
    
    - filters=None
    
**Return Type:** list  
**Attributes:** public|api.model  
**Purpose:** Fetches farmer and plot geographical data for map visualizations.  
    - **Name:** prepare_export_data  
**Parameters:**
    
    - entity_type
    - filters=None
    - fields_to_export=None
    
**Return Type:** list[dict]  
**Attributes:** public|api.model  
**Purpose:** Prepares data for CSV/XLSX export based on entity type and filters.  
    
**Implemented Features:**
    
    - KPI Data Calculation
    - Geo Data Retrieval
    - Dynamic Form Analytics Data
    - Report Data Preparation
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-006
    
**Purpose:** Centralizes backend logic for fetching and processing data required for analytical dashboards, map views, and potentially report exports. Interacts with core DFR models.  
**Logic Description:** Contains Python methods using Odoo ORM to query dfr_farmer_registry and dfr_dynamic_forms models. Aggregates data to compute KPIs (total farmers, by gender, by age group, land size summaries, registration trends over time, dynamic form submission counts, response distributions). Formats geo-data (latitude, longitude) for consumption by map components.  
**Documentation:**
    
    - **Summary:** Service model for DFR analytics data processing.
    
**Namespace:** odoo.addons.dfr_analytics.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/security/ir.model.access.csv  
**Description:** CSV file defining model-level access rights (read, write, create, unlink) for any custom models introduced by the dfr_analytics module (e.g., wizard models).  
**Template:** Odoo CSV Data  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** Security  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Role-Based Access Control (RBAC)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Ensures appropriate user roles can access models specific to the analytics module, like wizards or report configuration models.  
**Logic Description:** Standard Odoo CSV format: id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink. Defines access for groups like 'base.group_user' or custom analytics groups to any new models.  
**Documentation:**
    
    - **Summary:** Access control list for dfr_analytics module models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** dfr_addons/dfr_analytics/wizards/__init__.py  
**Description:** Initializes the Python package for Odoo wizard models within the dfr_analytics module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** wizards/__init__.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all wizard model files defined within the 'wizards' directory.  
**Logic Description:** Contains import statements for each Python wizard file (e.g., 'from . import report_export_wizard').  
**Documentation:**
    
    - **Summary:** __init__.py for the wizards directory of dfr_analytics.
    
**Namespace:** odoo.addons.dfr_analytics.wizards  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/wizards/report_export_wizard.py  
**Description:** Odoo TransientModel for handling user interaction for custom report exports. Allows users to specify filters and select export formats (CSV, XLSX).  
**Template:** Odoo Python Wizard  
**Dependancy Level:** 2  
**Name:** report_export_wizard  
**Type:** Wizard Model  
**Relative Path:** wizards/report_export_wizard.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected  
    - **Name:** report_type  
**Type:** fields.Selection  
**Attributes:** public  
**Purpose:** Selection field for report type (e.g., 'farmer_data', 'dynamic_form_data').  
    - **Name:** dynamic_form_id  
**Type:** fields.Many2one  
**Attributes:** public  
**Purpose:** Link to dfr_dynamic_forms.dynamic_form if report_type is 'dynamic_form_data'.  
    - **Name:** date_from  
**Type:** fields.Date  
**Attributes:** public  
**Purpose:** Start date for filtering.  
    - **Name:** date_to  
**Type:** fields.Date  
**Attributes:** public  
**Purpose:** End date for filtering.  
    - **Name:** export_format  
**Type:** fields.Selection  
**Attributes:** public  
**Purpose:** Selection for export format ('csv', 'xlsx').  
    
**Methods:**
    
    - **Name:** action_export_report  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
**Purpose:** Generates the report file (CSV/XLSX) based on wizard parameters and returns an Odoo action to download it.  
    
**Implemented Features:**
    
    - Custom Report Export Logic
    - User-defined Filters for Export
    
**Requirement Ids:**
    
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Provides a user interface for generating custom CSV/XLSX exports of farmer and dynamic form data with filtering options.  
**Logic Description:** Defines fields for user input (filters, format). The 'action_export_report' method queries data using 'analytics_service.py' methods or directly, formats it into CSV or XLSX (e.g., using 'io' and 'csv'/'openpyxl' libraries), and returns a download action. Handles data for both core farmer registry and dynamic forms.  
**Documentation:**
    
    - **Summary:** Wizard for custom data exports from the DFR analytics module.
    
**Namespace:** odoo.addons.dfr_analytics.wizards  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/report/__init__.py  
**Description:** Initializes the Python package for Odoo report-related Python files (e.g., custom report parsers/models).  
**Template:** Odoo Python Init  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** report/__init__.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Report Logic Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports Python files related to report generation logic if any.  
**Logic Description:** Contains import statements for report model files, if any (e.g., 'from . import farmer_data_export_reports').  
**Documentation:**
    
    - **Summary:** __init__.py for the report directory of dfr_analytics.
    
**Namespace:** odoo.addons.dfr_analytics.report  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/report/farmer_data_export_reports.py  
**Description:** Python logic for PDF reports related to farmer data, inheriting from 'report.abstract_report_xlsx' for XLSX or defining QWeb data preparation methods.  
**Template:** Odoo Report Python  
**Dependancy Level:** 2  
**Name:** farmer_data_export_reports  
**Type:** Report Model  
**Relative Path:** report/farmer_data_export_reports.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
**Purpose:** Odoo model name for the report, e.g., 'report.dfr_analytics.report_farmer_statistics_pdf'.  
    
**Methods:**
    
    - **Name:** _get_report_values  
**Parameters:**
    
    - docids
    - data=None
    
**Return Type:** dict  
**Attributes:** public|api.model  
**Purpose:** Prepares data to be passed to the QWeb template for PDF farmer reports. Called by Odoo reporting engine.  
    
**Implemented Features:**
    
    - PDF Report Data Preparation (Farmer Data)
    
**Requirement Ids:**
    
    - REQ-7-004
    
**Purpose:** Provides backend data and logic for generating structured PDF reports on farmer data. This is mainly for custom QWeb PDF reports.  
**Logic Description:** Inherits from `odoo.addons.report_xlsx.report.report_xlsx.ReportXlsx` if direct XLSX generation is complex and not handled by wizard, or `odoo.models.AbstractModel` for QWeb PDF. The `_get_report_values` method fetches and processes data for PDF reports based on `docids` or `data` from a wizard/action context.  
**Documentation:**
    
    - **Summary:** Python backend for farmer data PDF reports.
    
**Namespace:** odoo.addons.dfr_analytics.report  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/report/dynamic_form_data_export_reports.py  
**Description:** Python logic for PDF reports related to dynamic form data, similar to farmer_data_export_reports.py but for dynamic forms.  
**Template:** Odoo Report Python  
**Dependancy Level:** 2  
**Name:** dynamic_form_data_export_reports  
**Type:** Report Model  
**Relative Path:** report/dynamic_form_data_export_reports.py  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected  
**Purpose:** Odoo model name for the report, e.g., 'report.dfr_analytics.report_dynamic_form_summary_pdf'.  
    
**Methods:**
    
    - **Name:** _get_report_values  
**Parameters:**
    
    - docids
    - data=None
    
**Return Type:** dict  
**Attributes:** public|api.model  
**Purpose:** Prepares data to be passed to the QWeb template for PDF dynamic form reports. Called by Odoo reporting engine.  
    
**Implemented Features:**
    
    - PDF Report Data Preparation (Dynamic Form Data)
    
**Requirement Ids:**
    
    - REQ-7-006
    
**Purpose:** Provides backend data and logic for generating structured PDF reports on dynamic form submission data. This is mainly for custom QWeb PDF reports.  
**Logic Description:** Similar to farmer_data_export_reports.py. Fetches dynamic form submission data based on criteria, processes it, and returns it for QWeb PDF rendering.  
**Documentation:**
    
    - **Summary:** Python backend for dynamic form data PDF reports.
    
**Namespace:** odoo.addons.dfr_analytics.report  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** dfr_addons/dfr_analytics/static/src/js/dashboard_manager.js  
**Description:** Main OWL component for the DFR Analytics Dashboard. Orchestrates the layout and rendering of various KPI widgets and charts.  
**Template:** Odoo OWL Component  
**Dependancy Level:** 3  
**Name:** DashboardManager  
**Type:** OWL Component  
**Relative Path:** static/src/js/dashboard_manager.js  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** kpiData  
**Type:** Object  
**Attributes:** public|state  
**Purpose:** Holds data for KPIs.  
    - **Name:** chartData  
**Type:** Object  
**Attributes:** public|state  
**Purpose:** Holds data for charts.  
    
**Methods:**
    
    - **Name:** onWillStart  
**Parameters:**
    
    
**Return Type:** Promise  
**Attributes:** public  
**Purpose:** Fetches initial dashboard data from backend using RPC to 'analytics_service.py'.  
    - **Name:** updateDashboardData  
**Parameters:**
    
    - filters
    
**Return Type:** Promise  
**Attributes:** public  
**Purpose:** Refreshes dashboard data based on applied filters.  
    
**Implemented Features:**
    
    - Dashboard Layout
    - KPI Display
    - Chart Display
    - Dynamic Form Data Visualization on Dashboard
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-006
    
**Purpose:** Renders the main analytics dashboard interface in Odoo, displaying various visualizations.  
**Logic Description:** OWL component that defines the structure of the dashboard. Uses sub-components like 'KpiWidget' and 'ChartWidget'. Fetches data via RPC calls to 'analytics_service.py' methods. Handles user interactions for filtering or drilling down if implemented.  
**Documentation:**
    
    - **Summary:** Core OWL component for the analytics dashboard.
    
**Namespace:** dfr_analytics.DashboardManager  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/js/kpi_widget.js  
**Description:** Reusable OWL component for displaying a single Key Performance Indicator (KPI) on the dashboard.  
**Template:** Odoo OWL Component  
**Dependancy Level:** 3  
**Name:** KpiWidget  
**Type:** OWL Component  
**Relative Path:** static/src/js/kpi_widget.js  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** title  
**Type:** String  
**Attributes:** public|props  
**Purpose:** Title of the KPI.  
    - **Name:** value  
**Type:** String | Number  
**Attributes:** public|props  
**Purpose:** Value of the KPI.  
    - **Name:** icon  
**Type:** String  
**Attributes:** public|props  
**Purpose:** Optional icon for the KPI.  
    
**Methods:**
    
    
**Implemented Features:**
    
    - KPI Value Display
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-006
    
**Purpose:** A simple component to display a named KPI value, often with an icon and title.  
**Logic Description:** Takes properties like title, value, and icon, and renders them in a consistent style. Used by 'DashboardManager'.  
**Documentation:**
    
    - **Summary:** OWL component for displaying individual KPIs.
    
**Namespace:** dfr_analytics.KpiWidget  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/js/chart_widget.js  
**Description:** Reusable OWL component for displaying charts (e.g., bar, line, pie) on the dashboard. May integrate a charting library if Odoo's native capabilities are insufficient.  
**Template:** Odoo OWL Component  
**Dependancy Level:** 3  
**Name:** ChartWidget  
**Type:** OWL Component  
**Relative Path:** static/src/js/chart_widget.js  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** chartType  
**Type:** String  
**Attributes:** public|props  
**Purpose:** Type of chart (bar, line, etc.).  
    - **Name:** chartData  
**Type:** Object  
**Attributes:** public|props  
**Purpose:** Data to be rendered in the chart.  
    - **Name:** chartOptions  
**Type:** Object  
**Attributes:** public|props  
**Purpose:** Configuration options for the chart.  
    
**Methods:**
    
    - **Name:** onMounted  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
**Purpose:** Initializes and renders the chart using the provided data and options.  
    
**Implemented Features:**
    
    - Chart Visualization
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-006
    
**Purpose:** Visualizes data sets using various chart types within the dashboard.  
**Logic Description:** Takes chart type, data, and options as props. Uses Odoo's built-in charting or a third-party library (e.g., Chart.js, if bundled or available) to render the chart in a canvas or SVG element within its template. Used by 'DashboardManager'.  
**Documentation:**
    
    - **Summary:** OWL component for displaying charts.
    
**Namespace:** dfr_analytics.ChartWidget  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/js/map_view_component.js  
**Description:** OWL component for displaying map-based visualizations. May use Leaflet.js or integrate with OCA map modules.  
**Template:** Odoo OWL Component  
**Dependancy Level:** 3  
**Name:** MapViewComponent  
**Type:** OWL Component  
**Relative Path:** static/src/js/map_view_component.js  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    - **Name:** geoData  
**Type:** Object  
**Attributes:** public|state  
**Purpose:** GeoJSON data for map features.  
    
**Methods:**
    
    - **Name:** onWillStart  
**Parameters:**
    
    
**Return Type:** Promise  
**Attributes:** public  
**Purpose:** Fetches initial map data from backend using RPC to 'analytics_service.py'.  
    - **Name:** onMounted  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
**Purpose:** Initializes the map (e.g., Leaflet) and plots the geoData.  
    
**Implemented Features:**
    
    - Map-based Data Visualization
    
**Requirement Ids:**
    
    - REQ-7-002
    
**Purpose:** Displays farmer and plot locations on an interactive map within an Odoo view.  
**Logic Description:** Fetches GeoJSON data via RPC. Initializes a map library (e.g., Leaflet.js, which might be in static/lib/) within its template. Adds markers or polygons based on the fetched geoData. Supports basic map interactions like zoom and pan.  
**Documentation:**
    
    - **Summary:** OWL component for map visualizations.
    
**Namespace:** dfr_analytics.MapViewComponent  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/xml/dashboard_templates.xml  
**Description:** QWeb/OWL templates for the analytics dashboard and its sub-components (KPI widgets, charts).  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** dashboard_templates  
**Type:** OWL Template  
**Relative Path:** static/src/xml/dashboard_templates.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dashboard UI Structure
    - KPI Widget UI
    - Chart Widget UI
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-006
    
**Purpose:** Defines the HTML structure and presentation logic for OWL components used in the dashboard.  
**Logic Description:** Contains <t-name> templates for DashboardManager, KpiWidget, ChartWidget, defining their visual layout using QWeb directives and standard HTML.  
**Documentation:**
    
    - **Summary:** OWL templates for dashboard components.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/xml/map_view_templates.xml  
**Description:** QWeb/OWL templates for the map visualization component.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** map_view_templates  
**Type:** OWL Template  
**Relative Path:** static/src/xml/map_view_templates.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Map View UI Structure
    
**Requirement Ids:**
    
    - REQ-7-002
    
**Purpose:** Defines the HTML structure for the MapViewComponent, including the container where the map will be rendered.  
**Logic Description:** Contains a <t-name> template for MapViewComponent, typically including a div element that will serve as the map container.  
**Documentation:**
    
    - **Summary:** OWL template for the map view component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/static/src/scss/analytics_styles.scss  
**Description:** SCSS/CSS styles for custom styling of dashboard elements, charts, and map views.  
**Template:** Odoo SCSS  
**Dependancy Level:** 3  
**Name:** analytics_styles  
**Type:** Styling  
**Relative Path:** static/src/scss/analytics_styles.scss  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom UI Styling
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-006
    
**Purpose:** Provides custom visual appearance for analytics components beyond Odoo's default styling.  
**Logic Description:** Contains SCSS rules targeting elements within the dashboard, KPI widgets, charts, and map components to achieve desired look and feel.  
**Documentation:**
    
    - **Summary:** Custom styles for the DFR analytics module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/views/assets.xml  
**Description:** XML file to register static assets (JS, CSS, OWL templates) with Odoo's asset management system, making them available to the web client.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** assets  
**Type:** Odoo View XML  
**Relative Path:** views/assets.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Static Asset Registration
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-002
    - REQ-7-006
    
**Purpose:** Ensures that custom JavaScript, CSS, and OWL templates are loaded by the Odoo web client.  
**Logic Description:** Uses <odoo><data> and <template id='assets_backend' inherit_id='web.assets_backend'> to link JS files, SCSS files, and XML template files for OWL components.  
**Documentation:**
    
    - **Summary:** Asset registration for dfr_analytics module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** dfr_addons/dfr_analytics/views/analytics_dashboard_views.xml  
**Description:** XML file defining Odoo views for the analytics dashboard, including the main dashboard action and menu item. This view will embed OWL components.  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** analytics_dashboard_views  
**Type:** Odoo View XML  
**Relative Path:** views/analytics_dashboard_views.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dashboard View Definition
    - Dashboard Menu Access
    
**Requirement Ids:**
    
    - REQ-7-001
    - REQ-7-006
    
**Purpose:** Creates the user-accessible dashboard within the Odoo Admin Portal.  
**Logic Description:** Defines an <record id='dfr_analytics_dashboard_action' model='ir.actions.client'> with tag 'dfr_analytics.DashboardManager'. Defines a <menuitem> linking to this action. The view structure might involve Odoo's `board` view type or a custom client action rendering the OWL dashboard.  
**Documentation:**
    
    - **Summary:** Odoo views for the DFR analytics dashboard.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/views/map_visualization_views.xml  
**Description:** XML file defining Odoo views for map visualizations, including actions and menu items. Embeds the map OWL component.  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** map_visualization_views  
**Type:** Odoo View XML  
**Relative Path:** views/map_visualization_views.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Map View Definition
    - Map View Menu Access
    
**Requirement Ids:**
    
    - REQ-7-002
    
**Purpose:** Provides user access to map-based visualizations of farmer/plot data within Odoo.  
**Logic Description:** Defines an <record id='dfr_map_view_action' model='ir.actions.client'> with tag 'dfr_analytics.MapViewComponent'. Defines a <menuitem> for accessing this map view. The view could also be an Odoo `map` view type if using OCA `web_map` directly, or a client action for a custom OWL component.  
**Documentation:**
    
    - **Summary:** Odoo views for map visualizations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/views/report_actions_views.xml  
**Description:** XML file defining Odoo menu items and actions for accessing report export functionalities (triggering wizards or direct report actions).  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** report_actions_views  
**Type:** Odoo View XML  
**Relative Path:** views/report_actions_views.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Report Export Menu Access
    
**Requirement Ids:**
    
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Provides users with menu entries to initiate data exports for farmer and dynamic form data.  
**Logic Description:** Defines <menuitem> entries under a 'Reporting' or 'Analytics' parent menu. These menu items will trigger `ir.actions.act_window` (for wizards like `report_export_wizard`) or `ir.actions.report` (for direct PDF/QWeb reports).  
**Documentation:**
    
    - **Summary:** Odoo views for report export actions and menus.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/wizards/report_export_wizard_views.xml  
**Description:** XML views defining the form for the Report Export Wizard, allowing users to specify filters and select export format.  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** report_export_wizard_views  
**Type:** Odoo View XML  
**Relative Path:** wizards/report_export_wizard_views.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Report Export Wizard UI
    
**Requirement Ids:**
    
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Defines the user interface for the report export wizard.  
**Logic Description:** Contains an <record id='view_report_export_wizard_form' model='ir.ui.view'> defining the form layout with fields for report_type, dynamic_form_id, date_from, date_to, export_format, and buttons to trigger 'action_export_report'.  
**Documentation:**
    
    - **Summary:** Odoo XML views for the report export wizard.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** dfr_addons/dfr_analytics/report/report_templates.xml  
**Description:** XML file containing QWeb templates for generating PDF reports and defining `ir.actions.report` records.  
**Template:** Odoo XML View  
**Dependancy Level:** 4  
**Name:** report_templates  
**Type:** Odoo Report XML  
**Relative Path:** report/report_templates.xml  
**Repository Id:** DFR_MOD_ANALYTICS_REPORTING  
**Pattern Ids:**
    
    - Odoo Module System
    - Model-View-Controller (MVC) / Model-View-Template (MVT)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PDF Report Templates
    - Report Action Definitions
    
**Requirement Ids:**
    
    - REQ-7-004
    - REQ-7-006
    
**Purpose:** Defines the visual layout of PDF reports and registers these reports with Odoo's reporting engine.  
**Logic Description:** Contains <template id='...'> definitions using QWeb syntax for PDF report layouts (e.g., farmer statistics, dynamic form summaries). Also defines <record model='ir.actions.report'> entries linking report names to models (like 'report.dfr_analytics.report_farmer_statistics_pdf') and QWeb templates.  
**Documentation:**
    
    - **Summary:** QWeb templates and report actions for dfr_analytics module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableAdvancedMapLayers
  - enableDynamicFormSpecificDashboardsByDefault
  
- **Database Configs:**
  
  


---

