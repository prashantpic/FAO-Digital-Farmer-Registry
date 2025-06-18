sequenceDiagram
    actor "Odoo Admin Portal (Odoo Presentation Layer)" as adminportal
    participant "Data Management Toolkit Module (Odoo)" as datamgmttoolkit
    participant "Farmer Registry Module (Odoo)" as farmerregistrymodule
    participant "PostgreSQL Database" as postgresqldb

    activate adminportal
    adminportal-adminportal: 1. Administrator initiates Bulk Import action and selects CSV/XLSX file for upload
    note over adminportal: Administrator interacts with the system via the Odoo Admin Portal.

    adminportal-datamgmttoolkit: 2. POST /import/upload (filecontent)
    activate datamgmttoolkit
    note left of datamgmttoolkit: Error handling for file parsing or initial setup issues would occur before step 5.1 and result in an immediate error response to the Admin Portal.
    datamgmttoolkit-datamgmttoolkit: 2.1. Parse File Content & Extract Headers
    datamgmttoolkit--adminportal: HTTP 200 OK (parsedheaders, dfrschemafields)
    deactivate datamgmttoolkit

    adminportal-adminportal: 3. Display Column Mapping Interface to Administrator
    adminportal-adminportal: 4. Administrator submits column mappings

    adminportal-datamgmttoolkit: 5. POST /import/start (filereference, columnmappings)
    activate datamgmttoolkit

    loop 5.1 Iterate through rows/batches in the uploaded file
        note right of datamgmttoolkit: The loop (5.1) processes each row (or batch of rows) from the uploaded file individually.
        datamgmttoolkit-datamgmttoolkit: 5.1.1. Validate Row Data (against schema & basic rules)
        datamgmttoolkit-farmerregistrymodule: 5.1.2. validateBusinessRules(mappedrowdata)
        activate farmerregistrymodule
        farmerregistrymodule--datamgmttoolkit: businessValidationResult(isValid, errors)
        deactivate farmerregistrymodule

        alt 5.1.3. If row is valid (schema & business rules)
            datamgmttoolkit-farmerregistrymodule: 5.1.3.1. createOrUpdateFarmerRecord(validrowdata)
            activate farmerregistrymodule
            farmerregistrymodule-postgresqldb: 5.1.3.1.1. EXECUTE SQL INSERT/UPDATE (farmerdata)
            activate postgresqldb
            postgresqldb--farmerregistrymodule: SQLSTATUSOK / SQLERROR
            deactivate postgresqldb
            farmerregistrymodule--datamgmttoolkit: recordImportStatus(success/failure, recordid/errordetails)
            deactivate farmerregistrymodule
            datamgmttoolkit-datamgmttoolkit: 5.1.3.2. Log successful import for row
        else 5.1.4. Else (row is invalid)
            datamgmttoolkit-datamgmttoolkit: 5.1.4.1. Log validation error for row
        end
    end

    datamgmttoolkit-datamgmttoolkit: 5.2. Compile Final Import Report (successes, failures, errors)
    datamgmttoolkit--adminportal: HTTP 200 OK (importreportsummary, reportdetailslink)
    deactivate datamgmttoolkit

    adminportal-adminportal: 6. Display Import Report to Administrator
    deactivate admin_portal