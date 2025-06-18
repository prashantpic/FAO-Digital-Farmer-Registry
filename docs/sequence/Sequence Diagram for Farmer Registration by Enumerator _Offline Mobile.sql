sequenceDiagram
    actor "Enumerator" as actorenumerator
    participant "DFR Mobile App" as dfrmobileappcomposite
    participant "API Service Module (Odoo)" as dfrmodulerestapi008
    participant "Farmer Registry Module (Odoo)" as dfrmodulefarmerregistry002
    participant "PostgreSQL Database" as dfrinfrapostgresdbcontainer020

    note over actorenumerator, dfrinfrapostgresdbcontainer020: This diagram assumes the DFR Mobile App is initially offline for data capture and later gains network connectivity for synchronization.

    actorenumerator-dfrmobileappcomposite: 1. Inputs Farmer Data (Offline Mode)
    activate dfrmobileappcomposite

    dfrmobileappcomposite-dfrmobileappcomposite: 2. Validate Input Data Locally
    dfrmobileappcomposite--dfrmobileappcomposite: Validation Result (Success/Errors)

    note right of dfrmobileappcomposite: Data stored with 'Pending Sync' status. REQ-4-003, REQ-4-004.
    dfrmobileappcomposite-dfrmobileappcomposite: 3. [Validation Success] Store Farmer Data in Local Encrypted DB (SQLite/SQLCipher)
    dfrmobileappcomposite--dfrmobileappcomposite: Local Store Confirmation

    dfrmobileappcomposite--actorenumerator: 4. Display Confirmation (Data Saved Locally)
    deactivate dfrmobileappcomposite

    note over actorenumerator, dfrmobileappcomposite: REQ-4-006
    actorenumerator-dfrmobileappcomposite: 5. Initiates Synchronization (App Online)
    activate dfrmobileappcomposite

    dfrmobileappcomposite-dfrmobileappcomposite: 6. Prepare Queued Farmer Data Batch for Sync
    dfrmobileappcomposite--dfrmobileappcomposite: Queued Data Batch

    note right of dfrmobileappcomposite: REQ-API-005
    dfrmobileappcomposite-dfrmodulerestapi008: 7. POST /api/v1/dfr/sync/registrations (Farmer Data Batch)
    activate dfrmodulerestapi008

    dfrmodulerestapi008-dfrmodulerestapi008: 8. Validate API Request (Auth, Schema)
    dfrmodulerestapi008--dfrmodulerestapi008: Validation Result

    dfrmodulerestapi008-dfrmodulefarmerregistry002: 9. ProcessFarmerRegistrationBatch(Farmer Data Batch)
    activate dfrmodulefarmerregistry002

    loop 10. For each farmer record in batch:
        note right of dfrmodulefarmerregistry002: REQ-FHR-013. Involves querying PostgreSQL.
        dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.1. Perform De-duplication Checks
        activate dfrmodulefarmerregistry002
        dfrmodulefarmerregistry002-dfrinfrapostgresdbcontainer020: 10.1.1. Query for potential duplicates (National ID, Name+DOB+Village, etc.)
        activate dfrinfrapostgresdbcontainer020
        dfrinfrapostgresdbcontainer020--dfrmodulefarmerregistry002: Potential Duplicates Data
        deactivate dfrinfrapostgresdbcontainer020
        dfrmodulefarmerregistry002--dfrmodulefarmerregistry002: De-duplication Result
        deactivate dfrmodulefarmerregistry002

        alt 10.2. [De-duplication Result is Unique or Configured to Proceed]
            note right of dfrmodulefarmerregistry002: REQ-FHR-002
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.2.1. Generate Farmer UID
            dfrmodulefarmerregistry002--dfrmodulefarmerregistry002: Generated Farmer UID

            note right of dfrmodulefarmerregistry002: REQ-FHR-001
            dfrmodulefarmerregistry002-dfrinfrapostgresdbcontainer020: 10.2.2. INSERT Farmer Record (UID, details, status='Pending Verification')
            activate dfrinfrapostgresdbcontainer020
            dfrinfrapostgresdbcontainer020--dfrmodulefarmerregistry002: DB Write Confirmation
            deactivate dfrinfrapostgresdbcontainer020

            note right of dfrmodulefarmerregistry002: REQ-FHR-010, REQ-SADG-005. Using Odoo mail.thread or custom log.
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.2.3. Log Audit Trail (Successful Registration)

            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.2.4. Prepare record result: {LocalID, Status: 'Success', ServerUID, FarmerUID}

        else 10.3. [De-duplication Result is Potential Duplicate for Review]
            note right of dfrmodulefarmerregistry002: REQ-FHR-015
            dfrmodulefarmerregistry002-dfrinfrapostgresdbcontainer020: 10.3.1. UPDATE Farmer Record Status to 'Potential Duplicate'
            activate dfrinfrapostgresdbcontainer020
            dfrinfrapostgresdbcontainer020--dfrmodulefarmerregistry002: DB Update Confirmation
            deactivate dfrinfrapostgresdbcontainer020

            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.3.2. Log Audit Trail (Flagged Potential Duplicate)

            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.3.3. Prepare record result: {LocalID, Status: 'ConflictDuplicate', ServerUID}

        else 10.4. [De-duplication Result is Error or Hard Duplicate]
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.4.1. Log Audit Trail (Registration Failed)

            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 10.4.2. Prepare record result: {LocalID, Status: 'Error', Message: 'Reason'}

        end
    end

    dfrmodulefarmerregistry002--dfrmodulerestapi008: 11. Return Batch Processing Result (List of {LocalID, Status, ServerUID?, FarmerUID?, Error?})
    deactivate dfrmodulefarmerregistry002

    dfrmodulerestapi008--dfrmobileappcomposite: 12. Return Sync Batch Response (Processed Records Status)
    deactivate dfrmodulerestapi008

    note right of dfrmobileappcomposite: REQ-4-006. Updates SQLite records status (Synced, Conflict, Error) and stores Server Farmer UID.
    dfrmobileappcomposite-dfrmobileappcomposite: 13. Update Local Sync Status & Data (UIDs, errors)
    dfrmobileappcomposite--dfrmobileappcomposite: Local DB Update Confirmation

    dfrmobileappcomposite--actorenumerator: 14. Display Sync Completion Status (Success/Partial/Errors)
    deactivate dfrmobileappcomposite

    note over actorenumerator, dfrinfrapostgresdbcontainer020: Error handling for API request validation (step 8) or deeper Farmer Registry errors not fully expanded, but would result in error response propagation.
