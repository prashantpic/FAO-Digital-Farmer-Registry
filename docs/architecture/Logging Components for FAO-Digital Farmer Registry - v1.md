# Specification

# 1. Logging And Observability Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-17
  - **Technology Stack:**
    
    - Odoo 18.0 Community
    - Python
    - PostgreSQL
    - Docker
    - Nginx
    - Android (Flutter/Dart or Native Kotlin/Java)
    - REST APIs
    
  - **Monitoring Requirements:**
    
    - REQ-DIO-009 (System Monitoring)
    - REQ-SADG-005 (Audit Logs)
    - REQ-API-009 (API Performance)
    - REQ-4-011 (Mobile App Logs - local & optional server sync)
    - REQ-CM-011 (Quarterly Health/Patch Reports)
    
  - **System Architecture:** Modular Monolith (Odoo-centric) with mobile client and external APIs. Dockerized deployment with separate Odoo, PostgreSQL, and Nginx containers per country instance.
  - **Environment:** production
  
- **Log Level And Category Strategy:**
  
  - **Default Log Level:** INFO
  - **Environment Specific Levels:**
    
    - **Environment:** production  
**Log Level:** INFO  
**Justification:** Balance detail with performance for live systems. REQ-DIO-009 implies monitoring critical events.  
    - **Environment:** staging  
**Log Level:** DEBUG  
**Justification:** Enable detailed logging for UAT, pre-production testing, and data migration validation. REQ-DIO-004.  
    - **Environment:** development  
**Log Level:** DEBUG  
**Justification:** Maximum verbosity for development and troubleshooting.  
    
  - **Component Categories:**
    
    - **Component:** DFR_Odoo_Modules  
**Category:** Application  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Core application logic, business rule execution. REQ-SADG-005.  
    - **Component:** DFR_API_Services  
**Category:** API  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** API request/response logging for traceability and error diagnosis. REQ-API-009.  
    - **Component:** DFR_Mobile_Sync_Handler  
**Category:** Integration  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Server-side handling of mobile sync operations. REQ-4-006, REQ-4-011.  
    - **Component:** Nginx  
**Category:** Infrastructure  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Access logs for traffic analysis and error logs for proxy issues. REQ-DIO-005.  
    - **Component:** PostgreSQL  
**Category:** Database  
**Log Level:** WARNING  
**Verbose Logging:** False  
**Justification:** Database errors, slow queries (if configured). Odoo drives most queries.  
    - **Component:** DFR_Audit_Log  
**Category:** Security  
**Log Level:** INFO  
**Verbose Logging:** True  
**Justification:** Dedicated audit trail for critical actions. REQ-SADG-005.  
    - **Component:** DFR_Notification_Gateway_Interaction  
**Category:** Integration  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Logs related to sending SMS/Email via external gateways. REQ-NS-004.  
    
  - **Sampling Strategies:**
    
    
  - **Logging Approach:**
    
    - **Structured:** True
    - **Format:** JSON
    - **Standard Fields:**
      
      - timestamp
      - level
      - logger_name
      - message
      - correlation_id
      - user_id
      - country_instance_id
      - source_component
      - client_ip_anonymized
      
    - **Custom Fields:**
      
      - farmer_uid
      - form_id
      - sync_session_id
      - api_endpoint
      - operation_name
      - error_code
      
    
  
- **Log Aggregation Architecture:**
  
  - **Collection Mechanism:**
    
    - **Type:** agent
    - **Technology:** Promtail
    - **Configuration:**
      
      - **Scrape_Configs:**
        
        - **Job_Name:** odoo_app  
**Static_Configs:**
    
    - **Targets:**
    
    - localhost:9182
    
**Labels:**
    
    - **App:** dfr-odoo
    - **__Path__:** /var/log/odoo/*.log
    
    
        - **Job_Name:** nginx  
**Static_Configs:**
    
    - **Targets:**
    
    - localhost:9182
    
**Labels:**
    
    - **App:** dfr-nginx
    - **__Path__:** /var/log/nginx/*.log
    
    
        - **Job_Name:** postgresql  
**Static_Configs:**
    
    - **Targets:**
    
    - localhost:9182
    
**Labels:**
    
    - **App:** dfr-postgresql
    - **__Path__:** /var/log/postgresql/*.csv
    
    
        
      - **Positions_File:** /tmp/positions.yaml
      - **Target_Config:**
        
        - **Sync_Period:** 10s
        
      
    - **Justification:** Integrates well with Prometheus/Grafana (REQ-DIO-009). Lightweight agent for collecting logs from files/stdout.
    
  - **Strategy:**
    
    - **Approach:** centralized
    - **Reasoning:** Centralized per country instance for unified analysis, troubleshooting, and auditing. REQ-PCA-010, REQ-DIO-001.
    - **Local Retention:** 24 hours
    
  - **Shipping Methods:**
    
    - **Protocol:** HTTP  
**Destination:** Loki (per country instance)  
**Reliability:** at-least-once  
**Compression:** True  
    
  - **Buffering And Batching:**
    
    - **Buffer Size:** 1MB
    - **Batch Size:** 1000
    - **Flush Interval:** 5s
    - **Backpressure Handling:** Retry with backoff
    
  - **Transformation And Enrichment:**
    
    - **Transformation:** Add 'country_instance_id' label  
**Purpose:** Segregate logs per country  
**Stage:** collection (Promtail agent)  
    - **Transformation:** Parse JSON log lines  
**Purpose:** Enable field extraction and search  
**Stage:** collection (Promtail pipeline_stages) or ingestion (Loki)  
    
  - **High Availability:**
    
    - **Required:** False
    - **Redundancy:** N/A
    - **Failover Strategy:** N/A (Loki HA is complex and likely out of scope for 'essential')
    
  
- **Retention Policy Design:**
  
  - **Retention Periods:**
    
    - **Log Type:** DFR_Audit_Log  
**Retention Period:** 1 year active, 7 years archive  
**Justification:** Compliance and long-term audit. REQ-SADG-005, REQ-SADG-009.  
**Compliance Requirement:** Country-specific data protection laws (placeholder)  
    - **Log Type:** DFR_Application_Logs (Odoo, API, MobileSyncHandler)  
**Retention Period:** 90 days active, 1 year archive  
**Justification:** Operational troubleshooting and short-term analysis.  
**Compliance Requirement:** N/A  
    - **Log Type:** Infrastructure_Logs (Nginx, PostgreSQL errors)  
**Retention Period:** 30 days active, 90 days archive  
**Justification:** System stability troubleshooting.  
**Compliance Requirement:** N/A  
    - **Log Type:** Security_Event_Logs  
**Retention Period:** 1 year active, 3 years archive  
**Justification:** Security incident investigation. REQ-SADG-007.  
**Compliance Requirement:** Country-specific cybersecurity regulations (placeholder)  
    
  - **Compliance Requirements:**
    
    - **Regulation:** Country-Specific Data Protection Laws (To be defined per country - Placeholder)  
**Applicable Log Types:**
    
    - DFR_Audit_Log
    - DFR_Application_Logs
    
**Minimum Retention:** To be defined  
**Special Handling:** PII masking/access controls. REQ-SADG-008.  
    
  - **Volume Impact Analysis:**
    
    - **Estimated Daily Volume:** To be determined per country instance based on user activity.
    - **Storage Cost Projection:** Dependent on chosen storage for Loki (e.g., S3, local disk) and retention periods.
    - **Compression Ratio:** Estimated 5:1 to 10:1 with Loki's default compression.
    
  - **Storage Tiering:**
    
    - **Hot Storage:**
      
      - **Duration:** 90 days (for App/Audit logs)
      - **Accessibility:** immediate
      - **Cost:** medium (Loki default)
      
    - **Warm Storage:**
      
      - **Duration:** Up to 1 year (for App/Audit logs)
      - **Accessibility:** seconds-minutes
      - **Cost:** low (e.g., S3 Standard-IA for Loki chunks)
      
    - **Cold Storage:**
      
      - **Duration:** >1 year (for Audit logs)
      - **Accessibility:** hours (e.g., S3 Glacier for Loki archive)
      - **Cost:** very_low
      
    
  - **Compression Strategy:**
    
    - **Algorithm:** gzip (Loki default)
    - **Compression Level:** default
    - **Expected Ratio:** 5:1
    
  - **Anonymization Requirements:**
    
    - **Data Type:** PII (NationalID, Phone, Email in non-audit logs)  
**Method:** Masking (e.g., nationalId: "****1234")  
**Timeline:** At Ingestion or Query Time (if supported)  
**Compliance:** REQ-SADG-008, REQ-SADG-009  
    
  
- **Search Capability Requirements:**
  
  - **Essential Capabilities:**
    
    - **Capability:** Filter by timestamp range  
**Performance Requirement:** <5s for typical queries  
**Justification:** Basic troubleshooting and log review. REQ-SYSADM-007.  
    - **Capability:** Filter by log level (INFO, WARN, ERROR)  
**Performance Requirement:** <5s  
**Justification:** Error diagnosis.  
    - **Capability:** Filter by logger_name/source_component  
**Performance Requirement:** <5s  
**Justification:** Isolating issues to specific modules/services.  
    - **Capability:** Filter by correlation_id  
**Performance Requirement:** <2s  
**Justification:** Tracing request flows.  
    - **Capability:** Filter by user_id  
**Performance Requirement:** <5s  
**Justification:** Auditing user activity.  
    - **Capability:** Filter by country_instance_id  
**Performance Requirement:** <2s  
**Justification:** Segregating logs for multi-tenant (country) admin.  
    - **Capability:** Full-text search on 'message' field  
**Performance Requirement:** <10s  
**Justification:** Keyword-based troubleshooting.  
    
  - **Performance Characteristics:**
    
    - **Search Latency:** <5-10s for common queries
    - **Concurrent Users:** 5
    - **Query Complexity:** simple to medium (Loki LogQL)
    - **Indexing Strategy:** Loki labels (timestamp, level, logger_name, correlation_id, user_id, country_instance_id, source_component, app)
    
  - **Indexed Fields:**
    
    - **Field:** timestamp  
**Index Type:** Loki internal (implicit)  
**Search Pattern:** Time range  
**Frequency:** high  
    - **Field:** level  
**Index Type:** Loki label  
**Search Pattern:** Exact match  
**Frequency:** high  
    - **Field:** logger_name  
**Index Type:** Loki label  
**Search Pattern:** Exact match / Regex  
**Frequency:** high  
    - **Field:** correlation_id  
**Index Type:** Loki label  
**Search Pattern:** Exact match  
**Frequency:** medium  
    - **Field:** user_id  
**Index Type:** Loki label  
**Search Pattern:** Exact match  
**Frequency:** medium  
    - **Field:** country_instance_id  
**Index Type:** Loki label  
**Search Pattern:** Exact match  
**Frequency:** high  
    - **Field:** error_code  
**Index Type:** Loki label (if extracted)  
**Search Pattern:** Exact match  
**Frequency:** low  
    
  - **Full Text Search:**
    
    - **Required:** True
    - **Fields:**
      
      - message
      - stack_trace
      
    - **Search Engine:** Loki (LogQL with regex/string matching)
    - **Relevance Scoring:** False
    
  - **Correlation And Tracing:**
    
    - **Correlation Ids:**
      
      - correlation_id (generated per request/transaction)
      
    - **Trace Id Propagation:** Manual via log context and event payloads
    - **Span Correlation:** False
    - **Cross Service Tracing:** False
    
  - **Dashboard Requirements:**
    
    - **Dashboard:** Log Overview Dashboard (Grafana)  
**Purpose:** High-level view of log volumes, error rates by component/country.  
**Refresh Interval:** 1m  
**Audience:** Admins, Support Teams  
    - **Dashboard:** API Error Log Dashboard (Grafana)  
**Purpose:** Focus on API endpoint errors, response codes, latencies from logs.  
**Refresh Interval:** 1m  
**Audience:** Admins, Developers  
    
  
- **Storage Solution Selection:**
  
  - **Selected Technology:**
    
    - **Primary:** Grafana Loki
    - **Reasoning:** Cost-effective, optimized for labels not full-text indexing (reducing storage), integrates natively with Prometheus/Grafana stack (REQ-DIO-009). Simple to operate for essential logging.
    - **Alternatives:**
      
      - ELK Stack (Elasticsearch, Logstash, Kibana) - More powerful but complex/resource-intensive for 'essential' scope.
      
    
  - **Scalability Requirements:**
    
    - **Expected Growth Rate:** 100% data volume in 5 years per country (REQ-DIO-013). Loki scales horizontally.
    - **Peak Load Handling:** Sized per country instance based on projected user activity and log generation.
    - **Horizontal Scaling:** True
    
  - **Cost Performance Analysis:**
    
    - **Solution:** Loki  
**Cost Per Gb:** Low (depends on underlying storage like S3)  
**Query Performance:** Good for label-based queries, moderate for full-text regex  
**Operational Complexity:** medium  
    
  - **Backup And Recovery:**
    
    - **Backup Frequency:** Daily (for Loki index/data if on persistent volumes, or rely on object storage versioning/replication if S3-backed)
    - **Recovery Time Objective:** 4 hours
    - **Recovery Point Objective:** 24 hours
    - **Testing Frequency:** Annually
    
  - **Geo Distribution:**
    
    - **Required:** False
    - **Regions:**
      
      
    - **Replication Strategy:** N/A (Each country instance is independent. REQ-PCA-010)
    
  - **Data Sovereignty:**
    
    - **Region:** Per Country Instance (CKI, Samoa, Tonga, Solomon Islands, Vanuatu)  
**Requirements:**
    
    - Logs must reside within country-approved infrastructure or cloud region if specified. REQ-DIO-002.
    
**Compliance Framework:** Country-specific data privacy laws  
    
  
- **Access Control And Compliance:**
  
  - **Access Control Requirements:**
    
    - **Role:** Super Administrator  
**Permissions:**
    
    - read_all_logs
    - manage_log_config
    
**Log Types:**
    
    - *
    
**Justification:** Platform-wide oversight. REQ-5-001.  
    - **Role:** National Administrator  
**Permissions:**
    
    - read_country_instance_logs
    - export_country_audit_logs
    
**Log Types:**
    
    - DFR_Audit_Log
    - DFR_Application_Logs
    - Infrastructure_Logs (for their instance)
    
**Justification:** Country-level admin and audit. REQ-5-001, REQ-SYSADM-007.  
    - **Role:** Support Team (National/Central)  
**Permissions:**
    
    - read_relevant_app_system_logs
    
**Log Types:**
    
    - DFR_Application_Logs (PII Masked)
    - Infrastructure_Logs (errors)
    
**Justification:** Troubleshooting user issues. REQ-5-014.  
    - **Role:** IT Team (National/FAO)  
**Permissions:**
    
    - read_infrastructure_logs
    - read_system_logs
    
**Log Types:**
    
    - Infrastructure_Logs
    - DFR_Application_Logs (errors)
    
**Justification:** System maintenance and deployment. REQ-5-014.  
    
  - **Sensitive Data Handling:**
    
    - **Data Type:** National ID  
**Handling Strategy:** mask  
**Fields:**
    
    - nationalIdNumber in general application logs
    
**Compliance Requirement:** REQ-SADG-008, REQ-SADG-009  
    - **Data Type:** Contact Phone  
**Handling Strategy:** mask  
**Fields:**
    
    - contactPhone in general application logs
    
**Compliance Requirement:** REQ-SADG-008, REQ-SADG-009  
    - **Data Type:** Full Email Address  
**Handling Strategy:** mask  
**Fields:**
    
    - contactEmail in general application logs (e.g., show domain only or u***@domain.com)
    
**Compliance Requirement:** REQ-SADG-008, REQ-SADG-009  
    - **Data Type:** Passwords  
**Handling Strategy:** exclude  
**Fields:**
    
    - Any password field - never log passwords
    
**Compliance Requirement:** Security best practice. REQ-SADG-003.  
    
  - **Encryption Requirements:**
    
    - **In Transit:**
      
      - **Required:** True
      - **Protocol:** HTTPS/TLS 1.2+
      - **Certificate Management:** Standard SSL certificates per instance. REQ-DIO-005.
      
    - **At Rest:**
      
      - **Required:** True
      - **Algorithm:** AES-256 (for Loki storage via underlying disk/object storage encryption)
      - **Key Management:** Provider-managed (e.g., AWS KMS, Azure Key Vault) or OS-level disk encryption.
      
    
  - **Audit Trail:**
    
    - **Log Access:** True
    - **Retention Period:** 1 year (for log access audit, separate from DFR audit log itself)
    - **Audit Log Location:** Centralized log management system (Loki)
    - **Compliance Reporting:** True
    
  - **Regulatory Compliance:**
    
    - **Regulation:** Country-Specific Data Protection Act (Placeholder)  
**Applicable Components:**
    
    - DFR_Odoo_Modules
    - PostgreSQL
    - Loki
    
**Specific Requirements:**
    
    - Data minimization in logs
    - Secure storage
    - Access control
    - Retention according to national law. REQ-SADG-008.
    
**Evidence Collection:** Audit logs, access control configurations, retention policy documents.  
    
  - **Data Protection Measures:**
    
    - **Measure:** PII Masking in general logs  
**Implementation:** Log processing rules (Promtail pipeline or Loki ingest) or application-level formatting.  
**Monitoring Required:** True  
    - **Measure:** Role-Based Access Control for Logs  
**Implementation:** Loki/Grafana user permissions mapped to DFR roles.  
**Monitoring Required:** True  
    
  
- **Project Specific Logging Config:**
  
  - **Logging Config:**
    
    - **Level:** INFO
    - **Retention:** See retentionPolicyDesign
    - **Aggregation:** Centralized per country via Promtail to Loki
    - **Storage:** Loki
    - **Configuration:**
      
      - **Odoo_Log_Format:** json
      - **Odoo_Log_Handler:** stdout_json_handler
      
    
  - **Component Configurations:**
    
    - **Component:** dfr_* (Odoo Modules)  
**Log Level:** INFO (Production), DEBUG (Staging/Dev)  
**Output Format:** JSON  
**Destinations:**
    
    - stdout (for Docker to capture)
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** N/A
    
**Custom Fields:**
    
    - correlation_id
    - user_id
    - country_instance_id
    - farmer_uid
    - form_id
    
    - **Component:** nginx  
**Log Level:** INFO (access_log), WARN (error_log)  
**Output Format:** standard_nginx_format (access), standard_nginx_error_format  
**Destinations:**
    
    - /var/log/nginx/access.log
    - /var/log/nginx/error.log
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** N/A
    
**Custom Fields:**
    
    - correlation_id (via custom header if propagated by Odoo)
    
    - **Component:** postgresql  
**Log Level:** WARNING  
**Output Format:** csvlog (or standard text format)  
**Destinations:**
    
    - stderr or /var/log/postgresql/postgresql.log
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** N/A
    
**Custom Fields:**
    
    
    - **Component:** MobileAppBackendAPI (Server-Side Handlers in Odoo)  
**Log Level:** INFO (DEBUG for specific error conditions with payload snippets - PII masked)  
**Output Format:** JSON  
**Destinations:**
    
    - stdout (Odoo logger)
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** N/A
    
**Custom Fields:**
    
    - correlation_id
    - user_id
    - device_id_anonymized
    - sync_session_id
    - api_endpoint
    
    
  - **Metrics:**
    
    - **Custom Metrics:**
      
      - **Log_Error_Rate_Per_Component:** Count of ERROR/CRITICAL logs per component over time.
      - **Audit_Log_Volume:** Volume of DFR_Audit_Log entries per day.
      - **Api_Error_Log_Count:** Count of 5xx errors in API logs.
      
    
  - **Alert Rules:**
    
    - **Name:** HighOdooErrorRate  
**Condition:** rate(odoo_logs{level=~"ERROR|CRITICAL"}[5m]) > 5  
**Severity:** Critical  
**Actions:**
    
    - **Type:** email  
**Target:** national_admins_group;it_support_group  
**Configuration:**
    
    - **Subject:** High Odoo Error Rate Detected in [CountryInstance]
    
    
**Suppression Rules:**
    
    - During scheduled maintenance window
    
**Escalation Path:**
    
    - IT Support -> Super Admin if unresolved in 1hr
    
    - **Name:** PostgreSQLCriticalError  
**Condition:** postgresql_logs{level="PANIC|FATAL"} > 0  
**Severity:** Critical  
**Actions:**
    
    - **Type:** email  
**Target:** db_admins_group;it_support_group  
**Configuration:**
    
    - **Subject:** PostgreSQL Critical Error in [CountryInstance]
    
    
**Suppression Rules:**
    
    
**Escalation Path:**
    
    
    - **Name:** AuditActionFailure  
**Condition:** dfr_audit_logs{event_status="failure"} > 0  
**Severity:** High  
**Actions:**
    
    - **Type:** email  
**Target:** national_admins_group  
**Configuration:**
    
    - **Subject:** Failed Audit Action Recorded in [CountryInstance]
    
    
**Suppression Rules:**
    
    
**Escalation Path:**
    
    
    
  
- **Implementation Priority:**
  
  - **Component:** Odoo Modules (dfr_*) Structured JSON Logging to stdout  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Promtail Agent Configuration for Odoo, Nginx, PostgreSQL  
**Priority:** high  
**Dependencies:**
    
    - Loki instance setup
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Loki Centralized Log Storage Setup (per country)  
**Priority:** high  
**Dependencies:**
    
    - Infrastructure provisioning
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Standard Grafana Dashboards for Logs  
**Priority:** medium  
**Dependencies:**
    
    - Loki setup
    - Promtail shipping logs
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** DFR_Audit_Log Specific Logging and Indexing  
**Priority:** high  
**Dependencies:**
    
    - Odoo Modules Logging
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Log-based Alerting Configuration (Basic)  
**Priority:** medium  
**Dependencies:**
    
    - Loki setup
    - Grafana/Alertmanager
    
**Estimated Effort:** Low  
**Risk Level:** low  
  - **Component:** PII Masking Strategy Implementation for general logs  
**Priority:** high  
**Dependencies:**
    
    - Structured Logging
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Excessive log volume impacting Loki performance or storage costs.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Implement appropriate log levels per environment. Monitor log volumes. Adjust retention policies. Optimize Loki label cardinality.  
**Contingency Plan:** Scale Loki storage/instances. Archive logs more aggressively.  
  - **Risk:** PII leakage in logs despite masking efforts.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Thorough testing of masking rules. Regular review of log content for PII. Strict access controls on logs. REQ-SADG-008.  
**Contingency Plan:** Purge affected logs if permissible. Incident response plan.  
  - **Risk:** Inconsistent structured logging format across DFR modules.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Provide clear logging guidelines and helper functions for developers. Code reviews.  
**Contingency Plan:** Post-processing/parsing rules in Promtail/Loki if necessary (adds complexity).  
  - **Risk:** Log search performance degradation over time with increasing data.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Optimize Loki label usage. Ensure appropriate indexing strategy. Scale Loki query frontend if needed.  
**Contingency Plan:** Archive older logs more frequently. Re-evaluate indexing strategy.  
  - **Risk:** Configuration drift for Promtail/Loki across 5 country instances.  
**Impact:** low  
**Probability:** medium  
**Mitigation:** Use configuration management tools (e.g., Ansible, Terraform) for deploying and managing logging infrastructure. Version control configurations.  
**Contingency Plan:** Manual audit and reconfiguration.  
  
- **Recommendations:**
  
  - **Category:** Logging Implementation  
**Recommendation:** Adopt structured JSON logging for all custom Odoo modules from the outset, writing to stdout for Docker compatibility.  
**Justification:** Essential for effective parsing, searching, and analysis in a centralized system like Loki. REQ-SADG-005.  
**Priority:** high  
**Implementation Notes:** Create a shared logging utility within `dfr_common` to ensure consistent format and inclusion of standard fields like correlation_id, user_id, country_instance_id.  
  - **Category:** Log Aggregation  
**Recommendation:** Use Promtail for log collection and Loki for storage and querying, per country instance.  
**Justification:** Aligns with existing monitoring stack (Prometheus/Grafana - REQ-DIO-009) and provides a cost-effective, scalable solution for essential logging.  
**Priority:** high  
**Implementation Notes:** Configure Promtail to add a `country_instance_id` label to all log streams for proper segregation in Loki.  
  - **Category:** Audit Logging  
**Recommendation:** Implement custom audit logging for DFR-specific critical actions (beyond Odoo's mail.thread) into a dedicated, structured log stream or by tagging mail.thread messages appropriately for specific audit searches.  
**Justification:** REQ-SADG-005 requires comprehensive audit logs. Relying solely on mail.thread might not capture all system-level auditable events or provide easy querying for specific audit reports.  
**Priority:** high  
**Implementation Notes:** Ensure audit logs capture 'who, what, when, where' and outcome for key operations.  
  - **Category:** PII Handling  
**Recommendation:** Implement PII masking at the application logging level for general logs. For dedicated DFR_Audit_Logs, if PII must be stored unmasked, ensure extremely strict, role-based access control is applied in Loki/Grafana.  
**Justification:** Compliance with data privacy (REQ-SADG-008, REQ-SADG-009). Masking in general logs reduces risk, while audit logs need to be accurate but protected.  
**Priority:** high  
**Implementation Notes:** Define a clear list of PII fields and their masking rules. Review audit log access permissions meticulously.  
  - **Category:** Mobile App Logs (Server-Side)  
**Recommendation:** Ensure robust server-side logging for all API interactions with the mobile app, including sync session details, data validation errors from mobile, and conflict resolution events.  
**Justification:** Essential for troubleshooting mobile sync issues (REQ-4-006, REQ-4-011), which are critical for offline-first functionality.  
**Priority:** high  
**Implementation Notes:** Include `device_id` (anonymized if necessary for general logs, full for specific error tracing), `user_id`, and `sync_session_id` in these logs.  
  


---

