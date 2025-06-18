sequenceDiagram
    actor "User (Enumerator/Admin)" as actoruser
    participant "DFR UI (Farmer/Admin Portal)" as dfruifarmerregistry
    participant "Farmer Registry Module" as dfrmodulefarmerregistry002
    participant "External Connectors Module" as dfrmoduleexternalconnectors009
    participant "National ID Validation Service" as extnidservice

    actoruser-dfruifarmerregistry: 1. Enters/Submits National ID details (e.g., NID, Name, DOB)
    activate dfruifarmerregistry

    dfruifarmerregistry-dfrmodulefarmerregistry002: 2. processFarmerDataWithNID(farmerRecord, nidDetails)
    activate dfrmodulefarmerregistry002

    note over dfrmodulefarmerregistry002: REQ-FHR-006: National ID input and optional KYC logic (API-based if available).
    dfrmodulefarmerregistry002-dfrmoduleexternalconnectors009: 3. requestNIDValidation(farmerInfo, nidDetails)
    activate dfrmoduleexternalconnectors009

    loop [Loop: Max Retries (e.g., 3 attempts for transient errors)]
        note over dfrmoduleexternalconnectors009: REQ-API-007, REQ-API-011: External Connectors module handles integration with NID validation systems, including protocol transformation and data mapping.
        note right of dfrmoduleexternalconnectors009: Circuit Breaker pattern implemented here to prevent cascading failures if NID service is unresponsive. Retry logic handles transient errors.
        
        alt [Opt: If Circuit Breaker is CLOSED or HALFOPEN]
            note over extnidservice: Idempotency for NID validation calls should be considered. If the NID service itself is not idempotent, the connector should avoid resubmitting if a previous call's outcome is unknown but might have succeeded.
            dfrmoduleexternalconnectors009-extnidservice: 4.1.1. POST /validateNID (nidDetails, apiKey)
            activate extnidservice
            extnidservice--dfrmoduleexternalconnectors009: 4.1.1. HTTP Response (e.g., 200 OK with JSON body, 4xx, 5xx)
            deactivate extnidservice

            alt [Alt: Response Analysis]
                alt [Opt: Successful Validation (e.g., HTTP 200)]
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.1.1. Parse response: {status: 'VALID'/'INVALID'/'NOTFOUND', details: {...}}
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.1.2. Break loop (success)
                else [Opt: Retryable Error (e.g., HTTP 503, Timeout)]
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.2.1. Increment retry counter. Implement backoff delay.
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.2.2. Continue loop (if retries left)
                else [Opt: Non-Retryable Error (e.g., HTTP 400, 401, 403) or Retries Exhausted]
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.3.1. Log error. Set NIDValidationResult to error/unavailable. Update Circuit Breaker state.
                    dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.1.2.3.2. Break loop (failure)
                end
            end
        else [Opt: If Circuit Breaker is OPEN]
            dfrmoduleexternalconnectors009-dfrmoduleexternalconnectors009: 4.2.1. Set NIDValidationResult to 'Service Unavailable (Circuit Breaker Open)'. Break loop.
        end
    end

    dfrmoduleexternalconnectors009--dfrmodulefarmerregistry002: 5. NIDValidationResult: Return NIDValidationResult (parsedResponse or errorStatus)
    deactivate dfrmoduleexternalconnectors009

    alt [Alt: Process NID Validation Result]
        alt [Opt: NID is VALID]
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 6.1.1. updateFarmerRecord(status='NID Validated', validationDetails)
        else [Opt: NID is INVALID or NOTFOUND]
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 6.2.1. updateFarmerRecord(status='NID Invalid/Not Found', flagForReview=true)
        else [Opt: Validation Service ERROR/UNAVAILABLE]
            dfrmodulefarmerregistry002-dfrmodulefarmerregistry002: 6.3.1. updateFarmerRecord(status='NID Validation Pending - Service Error', flagForReview=true)
        end
    end

    dfrmodulefarmerregistry002--dfruifarmerregistry: 7. processingOutcome: Return processingOutcome (e.g., farmer record updated, validation status)
    deactivate dfrmodulefarmerregistry002

    dfruifarmerregistry--actoruser: 8. Display validation status and updated farmer information
    deactivate dfruifarmer_registry