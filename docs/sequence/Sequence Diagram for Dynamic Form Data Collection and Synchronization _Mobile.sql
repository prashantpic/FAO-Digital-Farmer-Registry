sequenceDiagram
    actor "Enumerator" as EnumeratorActor
    participant "Mobile UI" as DFRMobileAppPresentationLayer
    participant "Mobile Logic" as DFRMobileAppApplicationLogicLayer
    participant "Mobile Local DB" as DFRMobileAppDataLayer
    participant "API Service" as APIServiceModuleOdoo
    participant "Dynamic Form Engine" as DynamicFormEngineModuleOdoo
    participant "Farmer Registry" as FarmerRegistryModuleOdoo
    participant "PostgreSQL DB" as PostgreSQLDatabase

    note over DFRMobileAppApplicationLogicLayer: Phase 1: Data entry on Mobile App. This can happen offline.

    EnumeratorActor-DFRMobileAppPresentationLayer: 1. Selects Farmer & Dynamic Form
    activate DFRMobileAppPresentationLayer

    DFRMobileAppPresentationLayer-DFRMobileAppApplicationLogicLayer: 2. requestFormDefinitionAndFarmer(farmerId, formId)
    activate DFRMobileAppApplicationLogicLayer
    DFRMobileAppApplicationLogicLayer-DFRMobileAppDataLayer: 2.1. getFormDefinition(formId)
    activate DFRMobileAppDataLayer
    DFRMobileAppDataLayer--DFRMobileAppApplicationLogicLayer: 2.2. formDefinition
    deactivate DFRMobileAppDataLayer
    DFRMobileAppApplicationLogicLayer-DFRMobileAppDataLayer: 2.3. getFarmerContext(farmerId)
    activate DFRMobileAppDataLayer
    DFRMobileAppDataLayer--DFRMobileAppApplicationLogicLayer: 2.4. farmerContext
    deactivate DFRMobileAppDataLayer
    DFRMobileAppApplicationLogicLayer--DFRMobileAppPresentationLayer: 3. displayableFormDefinition, farmerContext
    deactivate DFRMobileAppApplicationLogicLayer

    DFRMobileAppPresentationLayer-DFRMobileAppPresentationLayer: 4. Render Dynamic Form

    EnumeratorActor-DFRMobileAppPresentationLayer: 5. Enters data into form

    DFRMobileAppPresentationLayer-DFRMobileAppPresentationLayer: 6. Perform client-side validation (REQ-3-002 Mobile)
    alt Validation Fails
        DFRMobileAppPresentationLayer--EnumeratorActor: 6.1.1. Display validation errors
    end

    EnumeratorActor-DFRMobileAppPresentationLayer: 7. Submits Form

    DFRMobileAppPresentationLayer-DFRMobileAppApplicationLogicLayer: 8. processFormSubmission(formData)
    activate DFRMobileAppApplicationLogicLayer
    DFRMobileAppApplicationLogicLayer-DFRMobileAppDataLayer: 8.1. saveSubmissionLocally(submissionData) (REQ-4-003)
    activate DFRMobileAppDataLayer
    DFRMobileAppDataLayer--DFRMobileAppApplicationLogicLayer: 8.2. localSaveConfirmation
    deactivate DFRMobileAppDataLayer
    DFRMobileAppApplicationLogicLayer--DFRMobileAppPresentationLayer: 9. localSubmissionStatus
    deactivate DFRMobileAppApplicationLogicLayer

    DFRMobileAppPresentationLayer--EnumeratorActor: 10. Display 'Submission Saved Locally' confirmation
    deactivate DFRMobileAppPresentationLayer

    note over DFRMobileAppApplicationLogicLayer: Phase 2: Synchronization with Odoo Backend. Triggered by enumerator or automatically if online.
    opt Initiate Sync (User-triggered or Auto-sync if Online)
        activate DFRMobileAppApplicationLogicLayer
        DFRMobileAppApplicationLogicLayer-DFRMobileAppDataLayer: 11.1. getPendingSubmissions()
        activate DFRMobileAppDataLayer
        DFRMobileAppDataLayer--DFRMobileAppApplicationLogicLayer: 11.2. pendingSubmissionsList
        deactivate DFRMobileAppDataLayer

        DFRMobileAppApplicationLogicLayer-APIServiceModuleOdoo: 11.3. POST /api/dfr/v1/dynamic-form/submit (submissions) (REQ-API-005)
        activate APIServiceModuleOdoo
        APIServiceModuleOdoo-APIServiceModuleOdoo: 11.3.1. Authenticate & Authorize Request (OAuth2/JWT)
        alt Auth Fails
            APIServiceModuleOdoo--DFRMobileAppApplicationLogicLayer: 11.3.2.1. Return 401/403 Error
        end

        APIServiceModuleOdoo-DynamicFormEngineModuleOdoo: 11.3.3. processDynamicFormSubmission(submissionData)
        activate DynamicFormEngineModuleOdoo
        DynamicFormEngineModuleOdoo-DynamicFormEngineModuleOdoo: 11.3.3.1. Validate submission (REQ-3-002 Server)
        alt Validation Fails (Server)
            DynamicFormEngineModuleOdoo--APIServiceModuleOdoo: 11.3.3.2.1. Return validationError
        end

        DynamicFormEngineModuleOdoo-FarmerRegistryModuleOdoo: 11.3.3.3. getFarmerDetails(farmerUid) (REQ-3-008)
        activate FarmerRegistryModuleOdoo
        FarmerRegistryModuleOdoo-PostgreSQLDatabase: 11.3.3.3.1. SELECT FROM farmertable
        activate PostgreSQLDatabase
        PostgreSQLDatabase--FarmerRegistryModuleOdoo: 11.3.3.3.2. farmerRecord
        deactivate PostgreSQLDatabase
        FarmerRegistryModuleOdoo--DynamicFormEngineModuleOdoo: 11.3.3.4. farmerDetails
        deactivate FarmerRegistryModuleOdoo
        alt Farmer Not Found
            DynamicFormEngineModuleOdoo--APIServiceModuleOdoo: 11.3.3.5.1. Return farmerNotFoundError
        end

        DynamicFormEngineModuleOdoo-PostgreSQLDatabase: 11.3.3.6. INSERT INTO formsubmissiontable (submissionData) (REQ-3-008)
        activate PostgreSQLDatabase
        PostgreSQLDatabase--DynamicFormEngineModuleOdoo: 11.3.3.7. dbConfirmation
        deactivate PostgreSQLDatabase
        DynamicFormEngineModuleOdoo--APIServiceModuleOdoo: 11.3.4. processingResult (success/errors)
        deactivate DynamicFormEngineModuleOdoo

        note right of APIServiceModuleOdoo: REQ-4-007 (Conflict Resolution) logic is part of the sync response processing but not detailed here. This diagram assumes direct success/failure of submission.
        APIServiceModuleOdoo--DFRMobileAppApplicationLogicLayer: 11.4. syncResponse (status per submission)
        deactivate APIServiceModuleOdoo

        DFRMobileAppApplicationLogicLayer-DFRMobileAppDataLayer: 11.5. updateLocalSubmissionStatus(syncResponse) (REQ-4-006)
        activate DFRMobileAppDataLayer
        DFRMobileAppDataLayer--DFRMobileAppApplicationLogicLayer: 11.6. localUpdateConfirmation
        deactivate DFRMobileAppDataLayer

        DFRMobileAppApplicationLogicLayer-DFRMobileAppPresentationLayer: 11.7. notifyUISyncComplete(status)
        activate DFRMobileAppPresentationLayer
        deactivate DFRMobileAppApplicationLogicLayer
    end

    DFRMobileAppPresentationLayer--EnumeratorActor: 12. Display Sync Status
    deactivate DFRMobileAppPresentationLayer