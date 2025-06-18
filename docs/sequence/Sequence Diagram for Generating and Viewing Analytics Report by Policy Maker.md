sequenceDiagram
    actor "Policy Maker/Analyst" as actorpolicymaker
    participant "Odoo Admin Portal" as odooadminportal
    participant "Odoo Authentication Service" as odooauthservice
    participant "Analytics and Reporting Module" as analyticsreportingmodule
    participant "Farmer Registry Module" as farmerregistrymodule
    participant "Dynamic Form Engine Module" as dynamicformenginemodule
    participant "PostgreSQL Database" as postgresqldatabase

    note over actorpolicymaker: Policy Maker must have appropriate roles/permissions (REQ-7-007) to access analytics.

    actorpolicymaker-odooadminportal: 1. Enters credentials and requests login
    activate odooadminportal
    odooadminportal-odooauthservice: 1.1. POST /web/session/authenticate (credentials)
    activate odooauthservice
    odooauthservice-postgresqldatabase: 1.1.1. SELECT user FROM resusers WHERE login=... AND password=...
    activate postgresqldatabase
    postgresqldatabase--odooauthservice: User record / No record
    deactivate postgresqldatabase
    odooauthservice--odooadminportal: HTTP 200 OK (sessionid, userdetails, roles) / HTTP 401 Unauthorized
    deactivate odooauthservice
    odooadminportal--actorpolicymaker: 1.2. Displays Admin Dashboard / Login Error Message
    deactivate odooadminportal

    actorpolicymaker-odooadminportal: 2. Navigates to Analytics/Reporting Section
    activate odooadminportal
    odooadminportal-analyticsreportingmodule: 2.1. GET /web#action=dfranalytics.actionreportdashboard
    activate analyticsreportingmodule
    analyticsreportingmodule--odooadminportal: Analytics Dashboard View (list of reports, filters)
    deactivate analyticsreportingmodule
    odooadminportal--actorpolicymaker: 2.2. Displays Analytics Dashboard
    deactivate odooadminportal

    actorpolicymaker-odooadminportal: 3. Selects report/dashboard and applies filters (e.g., geography, time period)
    activate odooadminportal
    odooadminportal-analyticsreportingmodule: 3.1. call: generatereport(reportid, filtercriteria)
    activate analyticsreportingmodule
    note right of analyticsreportingmodule: Filter criteria (REQ-7-004, REQ-7-006) can include geography, dynamic form type, time period, farmer status, etc.
    analyticsreportingmodule-farmerregistrymodule: 3.1.1. call: getfarmerdata(filtercriteria)
    activate farmerregistrymodule
    farmerregistrymodule-postgresqldatabase: 3.1.1.1. SELECT ... FROM dfrfarmer ... WHERE ... (filtered)
    activate postgresqldatabase
    postgresqldatabase--farmerregistrymodule: Raw Farmer Records
    deactivate postgresqldatabase
    farmerregistrymodule--analyticsreportingmodule: farmerdatalist
    deactivate farmerregistrymodule
    analyticsreportingmodule-dynamicformenginemodule: 3.1.2. call: getdynamicformdata(filtercriteria)
    activate dynamicformenginemodule
    dynamicformenginemodule-postgresqldatabase: 3.1.2.1. SELECT ... FROM dfrformsubmission ... WHERE ... (filtered)
    activate postgresqldatabase
    postgresqldatabase--dynamicformenginemodule: Raw Form Submission Records
    deactivate postgresqldatabase
    dynamicformenginemodule--analyticsreportingmodule: dynamicformsubmissiondatalist
    deactivate dynamicformenginemodule
    analyticsreportingmodule-analyticsreportingmodule: 3.1.3. processandaggregatedata(farmerdata, formdata)
    note right of analyticsreportingmodule: Data aggregation and processing (REQ-7-001, REQ-7-002) happens here to generate KPIs, charts, tables.
    analyticsreportingmodule-analyticsreportingmodule: 3.1.4. formatreportoutput(aggregated_data)
    note right of analyticsreportingmodule: Report formatting can be for screen display or exportable formats like PDF (via QWeb - REQ-7-004).
    analyticsreportingmodule--odooadminportal: Report Data / Dashboard View Content / Error
    deactivate analyticsreportingmodule
    odooadminportal--actorpolicymaker: 3.2. Displays Generated Report/Dashboard (KPIs, charts, tables) / Error Message
    deactivate odooadminportal