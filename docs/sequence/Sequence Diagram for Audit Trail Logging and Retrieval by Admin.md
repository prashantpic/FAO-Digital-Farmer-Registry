sequenceDiagram
    actor "Client UI / User Actor" as useractor
    participant "DFR Odoo App Server" as dfrinfraodooappcontainer019
    participant "Farmer Registry Module" as dfrmodulefarmerregistry002
    participant "Dynamic Form Module" as dfrmoduledynamicforms003
    participant "Audit Logging Extensions Module" as dfrmodulesecurityauditlog013
    participant "Admin Settings Panel Module" as dfrmoduleadminsettings005

    group Scenario 1: Logging an Auditable Action
        group 1.A: User Updates a Farmer Record
            useractor-dfrinfraodooappcontainer019: 1.1.1. Submit Farmer Record Update (e.g., HTTP POST /web/dataset/callkw)
            activate dfrinfraodooappcontainer019
            dfrinfraodooappcontainer019-dfrmodulefarmerregistry002: 1.1.2. processfarmerupdate(farmerid, datachanges)
            activate dfrmodulefarmerregistry002
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 1.1.2.1. [Internal] Validate and Persist Farmer Data Changes to DB
            dfrmodulefarmerregistry002-dfrmodulesecurityauditlog013: 1.1.2.2. logevent(action='UPDATE', entity='Farmer', entityid, changes, userinfo)
            activate dfrmodulesecurityauditlog013
            note right of dfrmodulesecurityauditlog013: REQ-FHR-010: Audit trail for profile edits.
            note right of dfrmodulesecurityauditlog013: REQ-SADG-005: Log data updates.
            dfrmodulesecurityauditlog013-dfrmodulesecurityauditlog013: 1.1.2.2.1. [Internal] Create and Persist Audit Log Entry (e.g., to mail.thread or custom model)
            dfrmodulesecurityauditlog013--dfrmodulefarmerregistry002: Log Acknowledged
            deactivate dfrmodulesecurityauditlog013
            dfrmodulefarmerregistry002--dfrinfraodooappcontainer019: Update Result
            deactivate dfrmodulefarmerregistry002
            dfrinfraodooappcontainer019--useractor: HTTP 200 OK (Update Success/Failure)
            deactivate dfrinfraodooappcontainer019
        end
        group 1.B: User Submits a Dynamic Form
            useractor-dfrinfraodooappcontainer019: 1.2.1. Submit Dynamic Form Data (e.g., HTTP POST /form/submit)
            activate dfrinfraodooappcontainer019
            dfrinfraodooappcontainer019-dfrmoduledynamicforms003: 1.2.2. processformsubmission(formid, submissiondata)
            activate dfrmoduledynamicforms003
            dfrmoduledynamicforms003-dfrmoduledynamicforms003: 1.2.2.1. [Internal] Validate and Persist Form Submission Data to DB
            dfrmoduledynamicforms003-dfrmodulesecurityauditlog013: 1.2.2.2. logevent(action='CREATE', entity='FormSubmission', entityid, userinfo)
            activate dfrmodulesecurityauditlog013
            note right of dfrmodulesecurityauditlog013: REQ-SADG-005: Log dynamic form submissions.
            dfrmodulesecurityauditlog013--dfrmoduledynamicforms003: Log Acknowledged
            deactivate dfrmodulesecurityauditlog013
            dfrmoduledynamicforms003--dfrinfraodooappcontainer019: Submission Result
            deactivate dfrmoduledynamicforms003
            dfrinfraodooappcontainer019--useractor: HTTP 200 OK (Submission Success/Failure)
            deactivate dfrinfraodooappcontainer019
        end
        group 1.C: User Logs In
            useractor-dfrinfraodooappcontainer019: 1.3.1. Submit Login Credentials (e.g., HTTP POST /web/login)
            activate dfrinfraodooappcontainer019
            dfrinfraodooappcontainer019-dfrinfraodooappcontainer019: 1.3.2. [Odoo Core Auth] Authenticate User
            dfrinfraodooappcontainer019-dfrmodulesecurityauditlog013: 1.3.3. logevent(action='LOGINSUCCESS/FAILURE', userid, ipaddress, timestamp)
            activate dfrmodulesecurityauditlog013
            note right of dfrmodulesecurityauditlog013: REQ-SADG-005: Logins (successful/failed).
            dfrmodulesecurityauditlog013--dfrinfraodooappcontainer019: Log Acknowledged
            deactivate dfrmodulesecurityauditlog013
            dfrinfraodooappcontainer019--useractor: HTTP 200 OK (Login Success/Failure, Session Cookie)
            deactivate dfrinfraodooappcontainer019
        end
    end
    group Scenario 2: Authorized Admin Retrieves Audit Logs
        note left of useractor: Admin User is assumed to be authenticated.
        useractor-dfrinfraodooappcontainer019: 2.1. Navigate to Audit Log View (e.g., GET /web#action=auditlogview)
        activate dfrinfraodooappcontainer019
        dfrinfraodooappcontainer019-dfrmoduleadminsettings005: 2.2. renderauditlogpagerequest()
        activate dfrmoduleadminsettings005
        note right of dfrmoduleadminsettings005: REQ-SYSADM-007: Interface for viewing audit trails.
        dfrmoduleadminsettings005--dfrinfraodooappcontainer019: Audit Log Page UI Definition
        deactivate dfrmoduleadminsettings005
        dfrinfraodooappcontainer019--useractor: HTTP 200 OK (Audit Log Page HTML/JS)
        deactivate dfrinfraodooappcontainer019
        note left of useractor: Filters: date range, user, action type.
        useractor-dfrinfraodooappcontainer019: 2.3. Request Audit Logs with Filters (e.g., HTTP POST /web/dataset/searchread)
        activate dfrinfraodooappcontainer019
        dfrinfraodooappcontainer019-dfrmoduleadminsettings005: 2.4. fetchfilteredauditlogsrequest(filters)
        activate dfrmoduleadminsettings005
        dfrmoduleadminsettings005-dfrmodulesecurityauditlog013: 2.4.1. retrieve_logs(filters)
        activate dfrmodulesecurityauditlog013
        note right of dfrmodulesecurityauditlog013: REQ-SADG-005, REQ-SADG-007: Retrieve audit logs.
        dfrmodulesecurityauditlog013-dfrmodulesecurityauditlog013: 2.4.1.1. [Internal] Query Audit Log DB Table with Filters
        dfrmodulesecurityauditlog013--dfrmoduleadminsettings005: Raw Log Records (List/JSON)
        deactivate dfrmodulesecurityauditlog013
        dfrmoduleadminsettings005-dfrmoduleadminsettings005: 2.4.2. [Internal] Format Log Records for Display
        dfrmoduleadminsettings005--dfrinfraodooappcontainer019: Formatted Log Data for UI
        deactivate dfrmoduleadminsettings005
        dfrinfraodooappcontainer019--useractor: HTTP 200 OK (JSON with Log Entries)
        deactivate dfrinfraodooappcontainer019
    end
    note over useractor,dfrmoduleadminsettings005: This diagram covers two main scenarios: logging an auditable action (data update, form submission, login) and an admin retrieving these logs. Specific DB interactions are represented as internal processing within the Odoo modules to maintain focus on inter-module communication.