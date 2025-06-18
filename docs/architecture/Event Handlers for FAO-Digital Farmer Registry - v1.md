# Specification

# 1. Event Driven Architecture Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-17
  - **Architecture Type:** Modular Monolith (Odoo-centric)
  - **Technology Stack:**
    
    - Odoo 18.0 Community
    - Python
    - PostgreSQL
    - REST APIs (Odoo Controllers)
    - Docker
    - Android (Native Kotlin/Java or Flutter/Dart)
    
  - **Bounded Contexts:**
    
    - FarmerRegistry
    - DynamicForms
    - MobileSync
    - Notifications
    - UserManagement
    - SystemAdministration
    - Reporting
    - DataManagement
    
  
- **Project Specific Events:**
  
  - **Event Id:** EVT-FR-001  
**Event Name:** FarmerRegisteredEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered upon successful creation and initial validation of a new farmer record in the DFR system.  
**Trigger Condition:** A new farmer record is successfully created and passes initial validation (e.g., status moves from 'draft' to 'pending verification' or 'active'). REQ-FHR-001, REQ-FHR-011.  
**Source Context:** FarmerRegistry (DFR Odoo Application Services)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    
**Payload:**
    
    - **Schema:**
      
      - **Farmer_Id:** UUID
      - **Farmer_Uid:** string
      - **Full_Name:** string
      - **Contact_Phone:** string
      - **Contact_Email:** string (optional)
      - **Registration_Timestamp:** ISO8601_datetime
      - **Status:** string
      
    - **Required Fields:**
      
      - farmer_id
      - farmer_uid
      - full_name
      - registration_timestamp
      - status
      
    - **Optional Fields:**
      
      - contact_phone
      - contact_email
      
    
**Frequency:** medium  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_registry_farmer
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** farmer.registered
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_notification_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** handleFarmerRegisteredNotification  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateRegistrationKPIs  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FHR-001
    - REQ-NS-001
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Mail Queue Retry (for notifications)
    - **Dead Letter Queue:** Odoo Log (for workflow failures)
    - **Timeout Ms:** 30000
    
  - **Event Id:** EVT-FR-002  
**Event Name:** FarmerSelfRegistrationSubmittedEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered when a farmer submits a pre-registration form via the Farmer Self-Service Portal.  
**Trigger Condition:** Successful submission of the portal pre-registration form (REQ-FSSP-004).  
**Source Context:** FarmerSelfServicePortal (DFR Odoo Presentation Layer)  
**Target Contexts:**
    
    - FarmerRegistry
    - Notifications
    - UserManagement
    
**Payload:**
    
    - **Schema:**
      
      - **Submission_Id:** UUID
      - **Full_Name:** string
      - **Village:** string
      - **Primary_Crop_Type:** string
      - **Contact_Phone:** string
      - **National_Id_Type:** string (optional)
      - **National_Id_Number:** string (optional)
      - **Submission_Timestamp:** ISO8601_datetime
      
    - **Required Fields:**
      
      - submission_id
      - full_name
      - contact_phone
      - submission_timestamp
      
    - **Optional Fields:**
      
      - village
      - primary_crop_type
      - national_id_type
      - national_id_number
      
    
**Frequency:** medium  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_self_registration
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** farmer.self_registration.submitted
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_self_reg_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Farmer Registry Service  
**Handler:** createDraftFarmerFromSelfReg  
**Processing Type:** sync  
    - **Service:** DFR Notification Service  
**Handler:** notifyAdminOfSelfReg  
**Processing Type:** async  
    - **Service:** DFR User Management Service  
**Handler:** assignSelfRegForReview  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FSSP-004
    - REQ-NS-001
    - REQ-FSSP-005
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Server Action Retry (if applicable for routing)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-FR-003  
**Event Name:** FarmerRecordUpdatedEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered when key fields of a farmer's record are updated, including status changes.  
**Trigger Condition:** Write operation on `dfr_farmer_registry_farmer` model affecting audited fields (REQ-FHR-010) or status (REQ-FHR-011).  
**Source Context:** FarmerRegistry (DFR Odoo Application Services)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    - AuditLog
    
**Payload:**
    
    - **Schema:**
      
      - **Farmer_Id:** UUID
      - **Updated_Fields:**
        
        - **Field_Name:**
          
          - **Old_Value:** any
          - **New_Value:** any
          
        
      - **Previous_Status:** string (optional)
      - **New_Status:** string (optional)
      - **Updated_By_User_Id:** UUID
      - **Update_Timestamp:** ISO8601_datetime
      
    - **Required Fields:**
      
      - farmer_id
      - updated_fields
      - updated_by_user_id
      - update_timestamp
      
    - **Optional Fields:**
      
      - previous_status
      - new_status
      
    
**Frequency:** high  
**Business Criticality:** normal  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_registry_farmer
    - **Operation:** update
    
**Routing:**
    
    - **Routing Key:** farmer.record.updated
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_audit_notification_queue
    
**Consumers:**
    
    - **Service:** DFR AuditLog Service  
**Handler:** logFarmerUpdate  
**Processing Type:** sync  
    - **Service:** DFR Notification Service  
**Handler:** handleFarmerUpdateNotifications  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateFarmerKPIs  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FHR-010
    - REQ-FHR-011
    - REQ-SADG-005
    
**Error Handling:**
    
    - **Retry Strategy:** None (handled by Odoo transaction)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 10000
    
  - **Event Id:** EVT-DF-001  
**Event Name:** DynamicFormSubmittedEvent  
**Event Type:** domain  
**Category:** DynamicFormData  
**Description:** Triggered when an enumerator or farmer submits a dynamic form.  
**Trigger Condition:** Successful submission of a dynamic form via mobile app or portal (REQ-3-008).  
**Source Context:** DynamicFormEngine (DFR Odoo Application Services / Mobile Data Layer)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    - ProgramManagement (hypothetical future)
    
**Payload:**
    
    - **Schema:**
      
      - **Submission_Id:** UUID
      - **Form_Id:** UUID
      - **Form_Version:** string
      - **Farmer_Id:** UUID
      - **Submitted_By_User_Id:** UUID
      - **Submission_Timestamp:** ISO8601_datetime
      - **Responses:**
        
        - **Field_Id_1:** value_1
        - **Field_Id_2:** value_2
        
      
    - **Required Fields:**
      
      - submission_id
      - form_id
      - farmer_id
      - submitted_by_user_id
      - submission_timestamp
      - responses
      
    - **Optional Fields:**
      
      - form_version
      
    
**Frequency:** high  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_form_submission
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** dynamic_form.submitted
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_form_submission_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** notifyOnFormSubmission  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateFormSubmissionAnalytics  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-3-008
    - REQ-NS-001
    
**Error Handling:**
    
    - **Retry Strategy:** None (handled by Odoo transaction or API error response)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 30000
    
  - **Event Id:** EVT-MS-001  
**Event Name:** MobileSyncBatchProcessedEvent  
**Event Type:** integration  
**Category:** MobileSynchronization  
**Description:** Triggered after a batch of data from a mobile device has been received and processed by the server.  
**Trigger Condition:** Successful completion of a server-side mobile data sync operation (REQ-4-006).  
**Source Context:** DFR API Gateway Layer  
**Target Contexts:**
    
    - FarmerRegistry
    - DynamicForms
    - AuditLog
    
**Payload:**
    
    - **Schema:**
      
      - **Sync_Session_Id:** UUID
      - **Device_Id:** string
      - **User_Id:** UUID
      - **Processed_Timestamp:** ISO8601_datetime
      - **Created_Records_Count:** integer
      - **Updated_Records_Count:** integer
      - **Conflicted_Records_Count:** integer
      - **Status:** success|partial_failure
      
    - **Required Fields:**
      
      - sync_session_id
      - device_id
      - user_id
      - processed_timestamp
      - status
      
    - **Optional Fields:**
      
      - created_records_count
      - updated_records_count
      - conflicted_records_count
      
    
**Frequency:** high  
**Business Criticality:** critical  
**Data Source:**
    
    - **Database:** N/A (API triggered)
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** mobile_sync.batch.processed
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_post_sync_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Farmer Registry Service  
**Handler:** triggerPostSyncDeDuplication  
**Processing Type:** async  
    - **Service:** DFR AuditLog Service  
**Handler:** logSyncActivity  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-4-006
    - REQ-API-005
    - REQ-FHR-013
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Server Action Retry (for post-processing failures)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 120000
    
  - **Event Id:** EVT-NS-001  
**Event Name:** NotificationDispatchRequestedEvent  
**Event Type:** system  
**Category:** Notifications  
**Description:** An internal event indicating a notification needs to be composed and dispatched.  
**Trigger Condition:** Business logic determines a notification is required (e.g., after FarmerRegisteredEvent).  
**Source Context:** Various DFR Application Services  
**Target Contexts:**
    
    - NotificationSystem
    
**Payload:**
    
    - **Schema:**
      
      - **Notification_Type_Code:** string
      - **Recipient_Farmer_Id:** UUID (optional)
      - **Recipient_User_Id:** UUID (optional)
      - **Recipient_Email:** string (optional)
      - **Recipient_Phone:** string (optional)
      - **Language_Code:** string
      - **Context_Data:**
        
        - **Key:** value
        
      
    - **Required Fields:**
      
      - notification_type_code
      - language_code
      - context_data
      
    - **Optional Fields:**
      
      - recipient_farmer_id
      - recipient_user_id
      - recipient_email
      - recipient_phone
      
    
**Frequency:** high  
**Business Criticality:** normal  
**Data Source:**
    
    - **Database:** N/A
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** notification.dispatch.request
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_notification_dispatch_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Module  
**Handler:** processAndSendNotification  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-NS-001
    - REQ-NS-002
    - REQ-NS-005
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Mail Queue Retry / SMS Gateway Retry (external)
    - **Dead Letter Queue:** Odoo `mail.mail` log / Custom Notification Log
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-DM-001  
**Event Name:** BulkImportCompletedEvent  
**Event Type:** system  
**Category:** DataManagement  
**Description:** Triggered upon completion (success or failure) of a bulk data import job.  
**Trigger Condition:** A bulk import process finishes (REQ-DM-001, REQ-DM-002).  
**Source Context:** DataManagement (DFR Odoo Application Services)  
**Target Contexts:**
    
    - SystemAdministration
    - Notifications
    
**Payload:**
    
    - **Schema:**
      
      - **Import_Job_Id:** UUID
      - **Start_Time:** ISO8601_datetime
      - **End_Time:** ISO8601_datetime
      - **Status:** success|failed|partial_success
      - **Total_Records_Processed:** integer
      - **Successful_Records_Count:** integer
      - **Failed_Records_Count:** integer
      - **Error_Log_Path:** string (optional)
      
    - **Required Fields:**
      
      - import_job_id
      - start_time
      - end_time
      - status
      - total_records_processed
      
    - **Optional Fields:**
      
      - successful_records_count
      - failed_records_count
      - error_log_path
      
    
**Frequency:** low  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** N/A (Process completion)
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** data_import.job.completed
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_admin_notification_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** notifyAdminOfImportCompletion  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-DM-001
    - REQ-DM-002
    
**Error Handling:**
    
    - **Retry Strategy:** None (eventual consistency for notification)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 10000
    
  
- **Event Types And Schema Design:**
  
  - **Essential Event Types:**
    
    - **Event Name:** FarmerRegisteredEvent  
**Category:** domain  
**Description:** Signifies a new farmer is officially in the registry.  
**Priority:** high  
    - **Event Name:** FarmerSelfRegistrationSubmittedEvent  
**Category:** domain  
**Description:** Indicates a potential new farmer initiated registration.  
**Priority:** high  
    - **Event Name:** FarmerRecordUpdatedEvent  
**Category:** domain  
**Description:** Captures changes to farmer data, including status.  
**Priority:** medium  
    - **Event Name:** DynamicFormSubmittedEvent  
**Category:** domain  
**Description:** Marks submission of supplementary data for a farmer.  
**Priority:** high  
    - **Event Name:** MobileSyncBatchProcessedEvent  
**Category:** integration  
**Description:** Server-side confirmation of mobile data processing.  
**Priority:** critical  
    - **Event Name:** NotificationDispatchRequestedEvent  
**Category:** system  
**Description:** Internal request to trigger a notification.  
**Priority:** medium  
    - **Event Name:** BulkImportCompletedEvent  
**Category:** system  
**Description:** Signals completion of a data import job.  
**Priority:** medium  
    
  - **Schema Design:**
    
    - **Format:** JSON
    - **Reasoning:** JSON is lightweight, human-readable, widely supported across web and mobile platforms, and explicitly mentioned for DFR APIs (REQ-API-002). Odoo's Python environment handles JSON easily.
    - **Consistency Approach:** Standard event envelope (event_id, timestamp, event_name, version, source_service, payload) for all events. Payload structure specific to event_name.
    
  - **Schema Evolution:**
    
    - **Backward Compatibility:** True
    - **Forward Compatibility:** False
    - **Strategy:** Additive changes to payload for backward compatibility. Introduce new event versions (e.g., `FarmerRegisteredEvent.v2`) for breaking changes. API endpoint versioning for events from/to external systems/mobile.
    
  - **Event Structure:**
    
    - **Standard Fields:**
      
      - event_id (UUID)
      - event_timestamp (ISO8601)
      - event_name (string)
      - event_version (string, e.g., '1.0')
      - source_service (string)
      - country_code (string, if applicable)
      - correlation_id (UUID, optional)
      
    - **Metadata Requirements:**
      
      - user_id_actor (UUID, if applicable)
      - device_id_source (string, for mobile events)
      
    
  
- **Event Routing And Processing:**
  
  - **Routing Mechanisms:**
    
    - **Type:** Odoo Automated Actions / Server Actions  
**Description:** Native Odoo mechanism to trigger Python code or predefined actions based on model CRUD events (create, write, unlink) or time-based conditions (cron).  
**Use Case:** Internal workflow automation, triggering notifications based on data changes (e.g., FarmerRegisteredEvent, FarmerStatusChangedEvent), scheduling batch tasks.  
    - **Type:** Odoo Python Method Calls  
**Description:** Direct synchronous or asynchronous (e.g., using Odoo's job queue if extended, or simple threading for non-critical tasks) calls to methods within Odoo services/modules.  
**Use Case:** Handling API requests (e.g., from mobile sync), processing events that require complex logic not suitable for simple automated actions.  
    - **Type:** Odoo `bus.bus`  
**Description:** Odoo's built-in long-polling mechanism for near real-time communication from server to specific web client sessions.  
**Use Case:** UI updates in Admin Portal based on server-side events (e.g., notification count in menu). This is primarily for UI reactivity, not robust event processing pipelines.  
    
  - **Processing Patterns:**
    
    - **Pattern:** Sequential (within Odoo Transaction)  
**Applicable Scenarios:**
    
    - Most internal DFR operations initiated by user actions or model changes, such as creating a farmer record and immediately logging an audit entry.
    
**Implementation:** Standard Odoo ORM operations and business logic methods executed within a single database transaction.  
    - **Pattern:** Asynchronous (Odoo Mail Queue / Scheduled Actions)  
**Applicable Scenarios:**
    
    - Dispatching notifications (SMS, Email) to avoid blocking primary operations.
    - Running batch de-duplication processes.
    - Generating periodic reports.
    
**Implementation:** Odoo's `mail.mail` queue for email dispatch (inherent retry). Odoo `ir.cron` for scheduled server actions (e.g., batch processing, report generation).  
    
  - **Filtering And Subscription:**
    
    - **Filtering Mechanism:** Odoo Automated Actions allow filtering based on Odoo domain expressions on model fields. Python logic within handlers for finer-grained filtering.
    - **Subscription Model:** Implicit subscription via Odoo Automated Action configuration (model and trigger conditions) or explicit calls in Python code.
    - **Routing Keys:**
      
      - N/A for Odoo internal message bus - model names and method calls act as implicit routing. For external notifications, recipient identifiers (phone, email) are used.
      
    
  - **Handler Isolation:**
    
    - **Required:** True
    - **Approach:** Odoo modules encapsulate specific functionalities. Server Actions run as separate Python methods. Odoo manages process/thread isolation for concurrent users/requests.
    - **Reasoning:** Ensures stability and separation of concerns as per Odoo's modular design.
    
  - **Delivery Guarantees:**
    
    - **Level:** at-least-once
    - **Justification:** For critical operations like farmer registration or data sync, an 'at-least-once' semantic is preferred, with idempotency in handlers to manage duplicates if retries occur. Odoo transactions provide atomicity for internal operations. External notifications (SMS/email) are typically at-least-once from the DFR system's perspective (gateway handles actual delivery).
    - **Implementation:** Idempotent design for API endpoints and critical Odoo server actions. Odoo's mail queue logs attempts. Mobile sync includes conflict resolution (REQ-4-007).
    
  
- **Event Storage And Replay:**
  
  - **Persistence Requirements:**
    
    - **Required:** True
    - **Duration:** As per audit and data retention policies (REQ-SADG-009, REQ-SYSADM-008).
    - **Reasoning:** Essential for auditing (REQ-SADG-005), change history tracking (REQ-SADG-006), and compliance.
    
  - **Event Sourcing:**
    
    - **Necessary:** False
    - **Justification:** The system relies on Odoo models storing current state. Audit logs and `mail.message` (chatter) provide historical context but are not used for state reconstruction via event replay. The current architecture does not mandate full event sourcing.
    - **Scope:**
      
      
    
  - **Technology Options:**
    
    - **Technology:** PostgreSQL (via Odoo ORM - Custom AuditLog Model)  
**Suitability:** high  
**Reasoning:** Primary database; already in use. Odoo ORM provides easy interaction. Suitable for structured audit data (REQ-SADG-005).  
    - **Technology:** Odoo `mail.message` (Chatter)  
**Suitability:** high  
**Reasoning:** Built-in Odoo feature for record-level history and communication. Good for user-visible change tracking (REQ-FHR-010).  
    
  - **Replay Capabilities:**
    
    - **Required:** False
    - **Scenarios:**
      
      - Replaying events for state reconstruction is not a core requirement. Audit logs are for review/investigation, not system state replay.
      
    - **Implementation:** N/A
    
  - **Retention Policy:**
    
    - **Strategy:** Configurable retention periods for audit logs and data entities as per REQ-SADG-009 and REQ-SYSADM-008.
    - **Duration:** To be defined by national policies.
    - **Archiving Approach:** Database archiving/partitioning for older audit logs if performance becomes an issue. Logical 'archived' status for data entities.
    
  
- **Dead Letter Queue And Error Handling:**
  
  - **Dead Letter Strategy:**
    
    - **Approach:** Logging and Administrative Review. For external notifications, Odoo's `mail.mail` queue has error states. For internal automated/server action failures, errors are logged in Odoo's system logs.
    - **Queue Configuration:** N/A (no dedicated event DLQ). Failures are typically logged in Odoo's standard logging mechanisms or specific tables like `mail.mail` for emails.
    - **Processing Logic:** National Administrators or support teams review Odoo logs or failed message queues to identify issues and trigger manual correction or retry if appropriate.
    
  - **Retry Policies:**
    
    - **Error Type:** Notification Gateway Temporary Failure (Email)  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Delay Configuration:** Odoo mail queue default (configurable)  
    - **Error Type:** Notification Gateway Temporary Failure (SMS)  
**Max Retries:** 2  
**Backoff Strategy:** fixed  
**Delay Configuration:** Configurable per gateway integration, if supported by the gateway connector.  
    - **Error Type:** Internal Odoo Automated Action Failure (transient)  
**Max Retries:** 0  
**Backoff Strategy:** none  
**Delay Configuration:** Error logged, manual intervention required if critical.  
    
  - **Poison Message Handling:**
    
    - **Detection Mechanism:** Repeated failures in Odoo logs for specific automated/server actions, or persistent error state in `mail.mail` queue.
    - **Handling Strategy:** Log the error with details, prevent further automatic retries for that specific item after a threshold, alert administrators.
    - **Alerting Required:** True
    
  - **Error Notification:**
    
    - **Channels:**
      
      - Odoo System Logs
      - Email (to administrators for critical system errors via monitoring tools)
      
    - **Severity:** critical|warning
    - **Recipients:**
      
      - National Administrators
      - Super Administrators
      - IT Support Team
      
    
  - **Recovery Procedures:**
    
    - **Scenario:** Failed automated action due to transient data issue  
**Procedure:** Admin identifies error in log, corrects underlying data, manually re-triggers action if necessary.  
**Automation Level:** semi-automated  
    - **Scenario:** Failed notification dispatch (SMS/Email)  
**Procedure:** Admin reviews Odoo mail queue or SMS gateway logs, identifies reason, corrects contact info or gateway config, retries sending.  
**Automation Level:** manual  
    
  
- **Event Versioning Strategy:**
  
  - **Schema Evolution Approach:**
    
    - **Strategy:** For internal Odoo events (processed by Automated/Server Actions), schema changes are managed via Odoo module updates and migrations. For API-based events (e.g., mobile sync), use API endpoint versioning (e.g., /v1/, /v2/) or a version field within the JSON payload (e.g., `"payload_version": "1.1"`).
    - **Versioning Scheme:** Semantic Versioning (X.Y.Z) for API endpoints. Simple incremental versions (e.g., 1.0, 1.1, 2.0) for event payloads if versioned explicitly.
    - **Migration Strategy:** Backend API to support last N-1 versions of mobile app payloads for a defined period to allow graceful client upgrades. Data migration scripts for Odoo model changes.
    
  - **Compatibility Requirements:**
    
    - **Backward Compatible:** True
    - **Forward Compatible:** False
    - **Reasoning:** API consumers (especially mobile app) should continue to function if new optional fields are added to event payloads (backward compatibility). Breaking changes require a new event/API version. Server should not be expected to process event versions it doesn't know.
    
  - **Version Identification:**
    
    - **Mechanism:** For API-driven events: Primarily through API endpoint version (e.g., `/api/dfr/v1/sync`). Optionally, a `payload_version` field within the JSON payload if finer-grained control per event type is needed.
    - **Location:** header (e.g. `Accept: application/vnd.dfr.v1+json`) or payload
    - **Format:** string (e.g., "v1.0", "1.0.0")
    
  - **Consumer Upgrade Strategy:**
    
    - **Approach:** Mobile app update prompts and enforced updates for critical changes (REQ-DIO-012, REQ-4-013). Backend API supports N-1 versions of mobile app for a period.
    - **Rollout Strategy:** Phased rollout for mobile app updates if possible, coordinated with backend API version support.
    - **Rollback Procedure:** Rollback mobile app to previous stable version if major issues. Backend API rollback to previous version if feasible (depends on DB schema changes).
    
  - **Schema Registry:**
    
    - **Required:** False
    - **Technology:** N/A. OpenAPI Specification serves as the schema definition for external APIs. Internal Odoo event structures are defined by Python code and Odoo models.
    - **Governance:** API schema changes managed via version control of OpenAPI spec and Odoo module code.
    
  
- **Event Monitoring And Observability:**
  
  - **Monitoring Capabilities:**
    
    - **Capability:** Odoo Application Logs  
**Justification:** Standard Odoo logging for errors, warnings, and debug information from custom modules and core.  
**Implementation:** Odoo built-in logging framework, configurable log levels.  
    - **Capability:** Custom AuditLog Table  
**Justification:** To meet REQ-SADG-005 for tracking significant user and system actions.  
**Implementation:** Custom Odoo model and Python logic to populate it upon specific events.  
    - **Capability:** Odoo `mail.message` (Chatter) and `mail.mail` queue  
**Justification:** Tracking record-specific changes and communication, and status of outgoing emails.  
**Implementation:** Leverage built-in Odoo features.  
    - **Capability:** External System Monitoring Tools (Prometheus/Grafana)  
**Justification:** For infrastructure, PostgreSQL, and Odoo application performance metrics (REQ-DIO-009).  
**Implementation:** Integration with standard monitoring stacks.  
    
  - **Tracing And Correlation:**
    
    - **Tracing Required:** True
    - **Correlation Strategy:** Use a unique `correlation_id` (e.g., UUID) generated at the start of a business transaction (e.g., API request from mobile, portal submission) and propagate it through related internal events and logs.
    - **Trace Id Propagation:** Pass `correlation_id` in event payloads and log messages. For API calls, can be passed as HTTP header.
    
  - **Performance Metrics:**
    
    - **Metric:** Event Processing Time (for specific automated actions)  
**Threshold:** To be defined (e.g., < 500ms for high-frequency actions)  
**Alerting:** True  
    - **Metric:** Notification Queue Length (Odoo mail.mail)  
**Threshold:** To be defined (e.g., >100 pending for 10 mins)  
**Alerting:** True  
    - **Metric:** API Endpoint Response Time (for event-receiving endpoints)  
**Threshold:** <500ms (REQ-API-009)  
**Alerting:** True  
    - **Metric:** Error Rate for Event Handlers  
**Threshold:** >5% over 5 mins  
**Alerting:** True  
    
  - **Event Flow Visualization:**
    
    - **Required:** False
    - **Tooling:** N/A (Not an essential requirement to build a dedicated event flow visualization tool. Odoo's technical menu provides some insight into automated actions and server actions configuration. Monitoring tools for metrics.)
    - **Scope:** N/A
    
  - **Alerting Requirements:**
    
    - **Condition:** Critical event handler failure (e.g., FarmerRegistrationEvent handler fails repeatedly)  
**Severity:** critical  
**Response Time:** Immediate  
**Escalation Path:**
    
    - On-call Admin
    - Development Team Lead
    
    - **Condition:** Notification queue exceeding threshold  
**Severity:** warning  
**Response Time:** Within 1 hour  
**Escalation Path:**
    
    - System Administrator
    
    - **Condition:** High error rate for API event endpoints  
**Severity:** critical  
**Response Time:** Immediate  
**Escalation Path:**
    
    - On-call Admin
    - API Development Team
    
    
  
- **Implementation Priority:**
  
  - **Component:** Core Domain Event Handling (FarmerRegistered, FarmerUpdated, DynamicFormSubmitted) via Odoo Automated Actions  
**Priority:** high  
**Dependencies:**
    
    - FarmerRegistry Module
    - DynamicForms Module
    
**Estimated Effort:** Included in module development  
  - **Component:** NotificationDispatchRequestedEvent processing and Notification System integration  
**Priority:** high  
**Dependencies:**
    
    - Notification Module
    - Core Domain Event Handlers
    
**Estimated Effort:** Medium  
  - **Component:** MobileSyncBatchProcessedEvent handling (post-sync tasks)  
**Priority:** high  
**Dependencies:**
    
    - API Gateway Layer
    - FarmerRegistry Module (De-duplication)
    
**Estimated Effort:** Medium  
  - **Component:** Audit Logging for key events  
**Priority:** high  
**Dependencies:**
    
    - Core Domain Event Handlers
    - AuditLog Module
    
**Estimated Effort:** Medium  
  - **Component:** Error Handling and Logging for Event Handlers  
**Priority:** high  
**Dependencies:**
    
    - All event handlers
    
**Estimated Effort:** Integrated into handler development  
  
- **Risk Assessment:**
  
  - **Risk:** Over-reliance on synchronous processing within Odoo leading to performance bottlenecks as event volume grows.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Carefully design automated actions for efficiency. Offload truly asynchronous tasks to Odoo cron jobs or Odoo's mail queue. Monitor performance closely (REQ-DIO-009, REQ-DIO-013).  
  - **Risk:** Lack of robust distributed transaction management if trying to coordinate actions across hypothetical future external microservices (currently not in scope, but a future consideration).  
**Impact:** low  
**Probability:** low  
**Mitigation:** Current monolith avoids this. Future integrations would need careful design (e.g., Sagas, idempotent consumers) if they involve distributed state changes.  
  - **Risk:** Difficulty in debugging complex event chains within Odoo's internal mechanisms if not properly logged with correlation IDs.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Implement and enforce use of correlation IDs for complex flows, especially those initiated by APIs. Enhance logging where Odoo's default is insufficient.  
  - **Risk:** Schema evolution for internal events tied to Odoo module updates can be complex if not managed carefully with data migrations.  
**Impact:** medium  
**Probability:** low  
**Mitigation:** Follow Odoo's best practices for module upgrades and data migrations. Thorough testing of upgrades in staging environment.  
  
- **Recommendations:**
  
  - **Category:** Event Schema  
**Recommendation:** Strictly enforce a common event envelope for all defined `projectSpecificEvents` to ensure consistency in logging and potential future processing.  
**Justification:** Improves maintainability and interoperability.  
**Priority:** high  
  - **Category:** Processing Strategy  
**Recommendation:** Leverage Odoo's `Automated Actions` and `Server Actions` for most internal domain event handling. Use custom Python methods for complex logic or API-triggered event processing. Prioritize synchronous processing within transactions for data consistency, using asynchronous mechanisms (mail queue, cron) only for non-blocking tasks like notifications or batch jobs.  
**Justification:** Aligns with Odoo's architecture, minimizes external dependencies, and ensures transactional integrity for core operations.  
**Priority:** high  
  - **Category:** Error Handling  
**Recommendation:** Enhance Odoo's standard logging for failed automated/server actions with more contextual information and ensure these are captured by system monitoring for alerting.  
**Justification:** Improves troubleshooting and reduces mean time to recovery for internal processing failures.  
**Priority:** medium  
  - **Category:** Observability  
**Recommendation:** Ensure `correlation_id` is logged with every significant step of an event-triggered workflow, particularly for those initiated via API (e.g., mobile sync).  
**Justification:** Facilitates easier debugging and tracing of multi-step processes.  
**Priority:** medium  
  - **Category:** Future Scalability  
**Recommendation:** While not immediately essential, for long-term scalability of specific high-volume asynchronous tasks (if they emerge), consider evaluating Odoo's job queue (if available/extended in Odoo 18 CE or via OCA module) or a lightweight external queue for true decoupling, but only if performance monitoring indicates a clear bottleneck with current Odoo mechanisms.  
**Justification:** Proactive consideration for future growth beyond initial scope, but defer implementation until justified by actual needs.  
**Priority:** low  
  


---

