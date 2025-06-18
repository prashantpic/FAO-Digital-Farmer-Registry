sequenceDiagram
    actor "Policy Maker (User)" as PolicyMaker
    participant "Web Browser" as Browser
    participant "Odoo App Server (Web/HTTP)" as dfrinfraodooappcontainer019
    participant "Odoo Security (RBAC)" as dfrmodulerbacconfig004
    participant "Analytics Module" as dfrmoduleanalyticsdashboards006
    participant "Farmer Registry Module" as dfrmodulefarmerregistry002
    participant "Dynamic Forms Module" as dfrmoduledynamicforms003
    participant "PostgreSQL Database" as PostgreSQLDB

    PolicyMaker--Browser: 1. Enters DFR Admin Portal URL & Credentials
    Browser--dfrinfraodooappcontainer019: 2. POST /web/login (credentials)
    activate dfrinfraodooappcontainer019
    dfrinfraodooappcontainer019--dfrmodulerbacconfig004: 2.1. Authenticate User(credentials, 'Policy Maker' role context)
    activate dfrmodulerbacconfig004
    dfrmodulerbacconfig004--dfrinfraodooappcontainer019: 2.2. Return Auth Result, Session Info
    deactivate dfrmodulerbacconfig004
    alt Login Succeeded
        dfrinfraodooappcontainer019--dfrinfraodooappcontainer019: 2.3.1. Create User Session
    end
    dfrinfraodooappcontainer019--Browser: 3. Return HTTP 302 Redirect to Dashboard (with session cookie)
    deactivate dfrinfraodooappcontainer019

    PolicyMaker--Browser: 4. Navigates to Analytics Dashboard
    Browser--dfrinfraodooappcontainer019: 5. GET /dfr/analyticsdashboard
    activate dfrinfraodooappcontainer019
    dfrinfraodooappcontainer019--dfrmodulerbacconfig004: 5.1. Authorize Access to Analytics Dashboard ('Policy Maker' role)
    activate dfrmodulerbacconfig004
    dfrmodulerbacconfig004--dfrinfraodooappcontainer019: 5.2. Return Authorization Result
    deactivate dfrmodulerbacconfig004
    alt Authorization Succeeded
        dfrinfraodooappcontainer019--dfrmoduleanalyticsdashboards006: 5.3. Request Dashboard Data (Filters: None)
        activate dfrmoduleanalyticsdashboards006
        dfrmoduleanalyticsdashboards006--dfrmodulefarmerregistry002: 5.3.1. fetchaggregatedfarmerdata(usercontext)
        activate dfrmodulefarmerregistry002
        dfrmodulefarmerregistry002--PostgreSQLDB: 5.3.1.1. SELECT ... FROM farmertable ... (ORM Query respecting RBAC)
        activate PostgreSQLDB
        note over PostgreSQLDB: RBAC is enforced by the Odoo framework (ORM and controllers) based on the logged-in user's context (Policy Maker role). This is implicitly applied to all data fetching operations.
        PostgreSQLDB--dfrmodulefarmerregistry002: 5.3.1.2. Return Farmer Data Rows
        deactivate PostgreSQLDB
        dfrmodulefarmerregistry002--dfrmoduleanalyticsdashboards006: 5.3.2. Return Aggregated Farmer Data
        deactivate dfrmodulefarmerregistry002
        dfrmoduleanalyticsdashboards006--dfrmoduledynamicforms003: 5.3.3. fetchaggregatedformdata(usercontext)
        activate dfrmoduledynamicforms003
        dfrmoduledynamicforms003--PostgreSQLDB: 5.3.3.1. SELECT ... FROM formsubmissiontable ... (ORM Query respecting RBAC)
        activate PostgreSQLDB
        PostgreSQLDB--dfrmoduledynamicforms003: 5.3.3.2. Return Form Data Rows
        deactivate PostgreSQLDB
        dfrmoduledynamicforms003--dfrmoduleanalyticsdashboards006: 5.3.4. Return Aggregated Form Data
        deactivate dfrmoduledynamicforms003
        dfrmoduleanalyticsdashboards006--dfrmoduleanalyticsdashboards006: 5.3.5. Process data, Generate KPIs, Prepare Map Visualization Data (e.g., plot coordinates)
        note right of dfrmoduleanalyticsdashboards006: Map visualizations are prepared server-side by the Analytics Module and rendered client-side by the Browser using data provided (e.g., list of plot coordinates).
        dfrmoduleanalyticsdashboards006--dfrinfraodooappcontainer019: 5.4. Return Processed Dashboard Data
        deactivate dfrmoduleanalyticsdashboards006
    end
    dfrinfraodooappcontainer019--Browser: 6. Return Analytics Dashboard Page HTML/JS
    deactivate dfrinfraodooappcontainer019

    PolicyMaker--Browser: 7. Applies Filters (e.g., geography, time period)
    Browser--dfrinfraodooappcontainer019: 8. GET /dfr/analyticsdashboard?filtergeo=X&filter_time=Y
    activate dfrinfraodooappcontainer019
    dfrinfraodooappcontainer019--dfrmoduleanalyticsdashboards006: 8.1. Request Dashboard Data (Filters: {geo:X, time:Y})
    activate dfrmoduleanalyticsdashboards006
    dfrmoduleanalyticsdashboards006--dfrmodulefarmerregistry002: 8.1.1. fetchaggregatedfarmerdata(filters, usercontext)
    activate dfrmodulefarmerregistry002
    dfrmodulefarmerregistry002--dfrmoduleanalyticsdashboards006: 8.1.2. Return Filtered Aggregated Farmer Data
    deactivate dfrmodulefarmerregistry002
    dfrmoduleanalyticsdashboards006--dfrmoduledynamicforms003: 8.1.3. fetchaggregatedformdata(filters, usercontext)
    activate dfrmoduledynamicforms003
    dfrmoduledynamicforms003--dfrmoduleanalyticsdashboards006: 8.1.4. Return Filtered Aggregated Form Data
    deactivate dfrmoduledynamicforms003
    dfrmoduleanalyticsdashboards006--dfrmoduleanalyticsdashboards006: 8.1.5. Re-process data, Update KPIs & Visualizations
    dfrmoduleanalyticsdashboards006--dfrinfraodooappcontainer019: 8.2. Return Processed Filtered Dashboard Data
    deactivate dfrmoduleanalyticsdashboards006
    dfrinfraodooappcontainer019--Browser: 9. Return Updated Analytics Dashboard Page/Data
    deactivate dfrinfraodooappcontainer019

    PolicyMaker--Browser: 10. Requests Report Export (e.g., CSV)
    Browser--dfrinfraodooappcontainer019: 11. GET /dfr/analytics/export?format=csv&filters=...
    activate dfrinfraodooappcontainer019
    dfrinfraodooappcontainer019--dfrmoduleanalyticsdashboards006: 11.1. Request Export Data (format='csv', filters)
    activate dfrmoduleanalyticsdashboards006
    dfrmoduleanalyticsdashboards006--dfrmodulefarmerregistry002: 11.1.1. fetchexportfarmerdata(filters, usercontext)
    activate dfrmodulefarmerregistry002
    dfrmodulefarmerregistry002--dfrmoduleanalyticsdashboards006: 11.1.2. Return Farmer Data for Export
    deactivate dfrmodulefarmerregistry002
    dfrmoduleanalyticsdashboards006--dfrmoduledynamicforms003: 11.1.3. fetchexportformdata(filters, usercontext)
    activate dfrmoduledynamicforms003
    dfrmoduledynamicforms003--dfrmoduleanalyticsdashboards006: 11.1.4. Return Form Data for Export
    deactivate dfrmoduledynamicforms003
    dfrmoduleanalyticsdashboards006--dfrmoduleanalyticsdashboards006: 11.1.5. Format Data as CSV (or other requested format)
    note right of dfrmoduleanalyticsdashboards006: Report export (CSV, XLSX, PDF) involves fetching potentially large datasets. PDF generation uses Odoo's QWeb engine.
    dfrmoduleanalyticsdashboards006--dfrinfraodooappcontainer019: 11.2. Return Formatted Report Data (CSV)
    deactivate dfrmoduleanalyticsdashboards006
    dfrinfraodooappcontainer019--Browser: 12. Return HTTP Response with Report File (Content-Disposition: attachment)
    deactivate dfrinfraodooappcontainer019

    PolicyMaker--Browser: 13. Logs out
    Browser--dfrinfraodooappcontainer019: 14. GET /web/session/logout
    activate dfrinfraodooappcontainer019
    dfrinfraodooappcontainer019--dfrinfraodooappcontainer019: 14.1. Invalidate User Session
    dfrinfraodooappcontainer019--Browser: 15. Return HTTP 302 Redirect to Login Page
    deactivate dfrinfraodooappcontainer019