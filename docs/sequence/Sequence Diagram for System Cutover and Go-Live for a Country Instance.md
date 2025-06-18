sequenceDiagram
    actor "FAO Project Team" as faoprojectteam
    actor "National IT Team" as nationalitteam
    actor "Contractor Team" as contractorteam
    participant "Legacy System (if any)" as legacysystem
    participant "Staging DFR DB" as stagingdb
    participant "Data Management Tools" as datamanagementtools
    participant "Production DFR Odoo App" as productionodooapp
    participant "Production DFR DB" as productiondb
    participant "Backup System" as backupsystem
    participant "DNS Management System" as dnsmanagementsystem
    actor "DFR End Users" as dfrendusers

    faoprojectteam-nationalitteam: 1. Review Pre-Cutover Checklist & Go/No-Go Criteria
    activate nationalitteam
    note over faoprojectteam: Go/No-Go decision based on REQ-DIO-004 criteria: successful UAT, data migration validation sign-off, infrastructure readiness, critical bug resolution, user training completion.
    nationalitteam--faoprojectteam: Go/No-Go Decision (Assume 'Go')
    deactivate nationalitteam

    faoprojectteam-contractorteam: 2. Instruct: Proceed with Cutover Plan
    activate contractorteam
    contractorteam--faoprojectteam: Acknowledgement

    opt Legacy System Freeze
        contractorteam-nationalitteam: 3.1 Request: Freeze Data Entry in Legacy System (if applicable)
        activate nationalitteam
        nationalitteam-legacysystem: 3.1.1 Command: Freeze Data Entry
        activate legacysystem
        legacysystem--nationalitteam: Status: Data Entry Frozen
        deactivate legacysystem
        nationalitteam--contractorteam: Confirmation: Legacy Data Entry Frozen
        deactivate nationalitteam
    end

    contractorteam-datamanagementtools: 4. Initiate: Final Data Migration Sync (Legacy/Staging - Prod DB)
    activate datamanagementtools
    datamanagementtools-stagingdb: 4.1 Extract Delta Data / Final Full Data
    activate stagingdb
    stagingdb--datamanagementtools: Delta/Full Data
    deactivate stagingdb
    datamanagementtools-productiondb: 4.2 Load/Apply Data to Production DB
    activate productiondb
    productiondb--datamanagementtools: Load Status (Success/Failure)
    deactivate productiondb
    datamanagementtools--contractorteam: Final Sync Status
    deactivate datamanagementtools

    contractorteam-nationalitteam: 5. Report: Final Data Migration Sync Status & Request Validation
    activate nationalitteam
    note right of contractorteam: Rollback plan (as per 3.6.4) would be triggered if critical steps (e.g., Final Sync, Health Checks, Backup) fail and cannot be immediately remediated.
    nationalitteam--contractorteam: Validation Sign-off (Assume Success)
    deactivate nationalitteam

    contractorteam-productionodooapp: 6. Configure: Apply Final Production Configurations
    activate productionodooapp
    productionodooapp--contractorteam: Status: Configurations Applied
    deactivate productionodooapp

    contractorteam-productionodooapp: 7. Command: Lock System Configuration
    activate productionodooapp
    productionodooapp--contractorteam: Status: Configuration Locked
    deactivate productionodooapp

    contractorteam-productionodooapp: 8. Execute: Final System Health Checks & Smoke Tests (App)
    activate productionodooapp
    productionodooapp--contractorteam: App Health & Smoke Test Results
    deactivate productionodooapp

    contractorteam-productiondb: 9. Execute: Final System Health Checks (DB)
    activate productiondb
    productiondb--contractorteam: DB Health Results
    deactivate productiondb

    contractorteam-faoprojectteam: 10. Report: Final Health Check Status
    contractorteam-nationalitteam: 10.1 Report: Final Health Check Status

    contractorteam-backupsystem: 11. Initiate: Full Backup of Production Database
    activate backupsystem
    backupsystem-productiondb: 11.1 Perform DB Backup Operation
    activate productiondb
    productiondb--backupsystem: DB Backup Data/Status
    deactivate productiondb
    backupsystem--contractorteam: Backup Status (Assume Success)
    deactivate backupsystem

    contractorteam-nationalitteam: 12. Report: Production Backup Status & Request DNS Update
    activate nationalitteam
    nationalitteam--contractorteam: Confirmation: DNS Update Initiated
    nationalitteam-dnsmanagementsystem: 13. Update DNS Record (Point to Production DFR Instance)
    activate dnsmanagementsystem
    dnsmanagementsystem--nationalitteam: DNS Update Confirmation
    deactivate dnsmanagementsystem
    note right of nationalitteam: DNS propagation time needs to be considered before full user access and widespread announcement.
    nationalitteam-contractorteam: 14. Inform: DNS Update Completed (Allow for propagation)
    deactivate nationalitteam

    contractorteam-productionodooapp: 15. Command: Enable User Access (Enumerators, Administrators)
    activate productionodooapp
    productionodooapp--contractorteam: Status: User Access Enabled
    deactivate productionodooapp

    faoprojectteam-nationalitteam: 16. Coordinate: Announce System Go-Live to End Users
    activate nationalitteam
    nationalitteam-dfrendusers: 16.1 Inform: DFR System is Live!
    nationalitteam--faoprojectteam: Announcement Sent Confirmation
    deactivate nationalitteam

    contractorteam-faoprojectteam: 17. Inform: Post-Go-Live Hypercare Support Period Begins
    deactivate contractorteam
