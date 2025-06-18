# Specification

# 1. Telemetry And Metrics Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-17
  - **Technology Stack:**
    
    - Odoo 18.0 Community Edition
    - Python
    - PostgreSQL
    - Docker
    - Nginx
    - Android (Native Kotlin/Java or Flutter/Dart)
    - REST APIs (JSON, OpenAPI v3.x)
    - OAuth2/JWT
    
  - **Monitoring Components:**
    
    - Prometheus
    - Grafana
    - Loki (or ELK Stack)
    - Odoo Internal Logging
    - Custom Backup Scripts Reporting
    
  - **Requirements:**
    
    - REQ-DIO-009 (System Monitoring)
    - REQ-PCA-004 (Scalability, PostgreSQL optimization, Odoo worker config)
    - REQ-API-009 (API Response Times)
    - REQ-7-008 (Report Generation Performance)
    - REQ-FSSP-011 (Portal Page Loads)
    - REQ-DIO-022 (Uptime)
    - REQ-SADG-005 (Audit Logging)
    - REQ-SADG-011 (Backup Monitoring)
    - REQ-4-014 (Mobile Sync Performance)
    
  - **Environment:** production
  
- **Standard System Metrics Selection:**
  
  - **Hardware Utilization Metrics:**
    
    - **Name:** system_cpu_usage_percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** CPU utilization for Odoo, PostgreSQL, Nginx hosts/containers.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus node_exporter/cAdvisor
    
**Thresholds:**
    
    - **Warning:** 75
    - **Critical:** 90
    
**Justification:** REQ-DIO-009: Monitor server resource utilization.  
    - **Name:** system_memory_usage_percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** Memory utilization for Odoo, PostgreSQL, Nginx hosts/containers.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus node_exporter/cAdvisor
    
**Thresholds:**
    
    - **Warning:** 80
    - **Critical:** 95
    
**Justification:** REQ-DIO-009: Monitor server resource utilization.  
    - **Name:** system_disk_io_bytes_total  
**Type:** counter  
**Unit:** bytes  
**Description:** Disk I/O operations for PostgreSQL and Odoo filestore.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus node_exporter/cAdvisor
    
**Thresholds:**
    
    - **Warning:** N/A (trend analysis)
    - **Critical:** N/A (trend analysis)
    
**Justification:** REQ-DIO-009: Monitor server resource utilization, identify disk bottlenecks.  
    - **Name:** system_disk_space_usage_percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** Disk space utilization for database, logs, backups.  
**Collection:**
    
    - **Interval:** 300s
    - **Method:** Prometheus node_exporter
    
**Thresholds:**
    
    - **Warning:** 80
    - **Critical:** 90
    
**Justification:** REQ-DIO-009: Monitor server resource utilization, prevent out-of-disk errors.  
    - **Name:** system_network_traffic_bytes_total  
**Type:** counter  
**Unit:** bytes  
**Description:** Network traffic (in/out) for all system components.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus node_exporter/cAdvisor
    
**Thresholds:**
    
    - **Warning:** N/A (trend analysis)
    - **Critical:** N/A (trend analysis)
    
**Justification:** REQ-DIO-009: Monitor server resource utilization, identify network bottlenecks.  
    
  - **Runtime Metrics:**
    
    - **Name:** postgresql_active_connections  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active connections to PostgreSQL database.  
**Technology:** PostgreSQL  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus postgres_exporter
    
**Criticality:** high  
**Justification:** REQ-PCA-004, REQ-DIO-009: Monitor database health and connection pool usage.  
    - **Name:** postgresql_query_latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of PostgreSQL queries.  
**Technology:** PostgreSQL  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus postgres_exporter (from pg_stat_statements)
    
**Criticality:** high  
**Justification:** REQ-PCA-004, REQ-DIO-009: Monitor database performance.  
    - **Name:** odoo_worker_process_count_active  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active Odoo worker processes.  
**Technology:** Odoo  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Odoo Prometheus Exporter or process monitoring
    
**Criticality:** medium  
**Justification:** REQ-PCA-004, REQ-DIO-009: Monitor Odoo application server health and capacity.  
    - **Name:** odoo_worker_cpu_usage_seconds_total  
**Type:** counter  
**Unit:** seconds  
**Description:** CPU time consumed by Odoo worker processes.  
**Technology:** Odoo  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Odoo Prometheus Exporter or process monitoring
    
**Criticality:** medium  
**Justification:** REQ-PCA-004, REQ-DIO-009: Monitor Odoo worker performance.  
    
  - **Request Response Metrics:**
    
    - **Name:** http_requests_total  
**Type:** counter  
**Unit:** count  
**Description:** Total HTTP requests received by Nginx (Admin Portal, Farmer Portal, APIs).  
**Dimensions:**
    
    - method
    - path
    - status_code
    - instance
    
**Percentiles:**
    
    
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Nginx Log Exporter / Prometheus
    
**Justification:** REQ-API-009, REQ-DIO-009: Monitor overall system load and identify error rates.  
    - **Name:** http_request_duration_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of HTTP requests for all services.  
**Dimensions:**
    
    - method
    - path
    - instance
    
**Percentiles:**
    
    - 0.5
    - 0.9
    - 0.95
    - 0.99
    
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Nginx Log Exporter / Odoo Prometheus Exporter
    
**Justification:** REQ-API-009, REQ-7-008, REQ-FSSP-011, REQ-DIO-009: Monitor performance SLAs.  
    
  - **Availability Metrics:**
    
    - **Name:** system_uptime_percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of time the DFR system (Odoo instance, Portals) is available and responsive.  
**Calculation:** (TotalTime - UnscheduledDowntime) / TotalTime * 100, excluding scheduled maintenance.  
**Sla Target:** 99.5  
**Justification:** REQ-DIO-022: Track system availability against target.  
    
  - **Scalability Metrics:**
    
    - **Name:** odoo_concurrent_users_active  
**Type:** gauge  
**Unit:** count  
**Description:** Number of concurrently active users on Odoo Admin Portal and Farmer Self-Service Portal.  
**Capacity Threshold:** Defined per country based on REQ-FSSP-012 and general load expectations.  
**Auto Scaling Trigger:** False  
**Justification:** REQ-DIO-013, REQ-FSSP-012: Monitor user load for capacity planning.  
    
  
- **Application Specific Metrics Design:**
  
  - **Transaction Metrics:**
    
    - **Name:** dfr_farmer_registrations_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of new farmer registrations processed.  
**Business_Context:** Core Farmer Registry growth  
**Dimensions:**
    
    - country_code
    - registration_source (admin_portal|mobile_app|self_service)
    
**Collection:**
    
    - **Interval:** N/A (event-driven)
    - **Method:** Odoo application logic incrementing counter
    
**Aggregation:**
    
    - **Functions:**
      
      - sum
      - rate
      
    - **Window:** 1h, 24h
    
**Justification:** REQ-FHR-001, REQ-7-001: Track core system activity.  
    - **Name:** dfr_dynamic_form_submissions_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of dynamic form submissions processed.  
**Business_Context:** Supplementary data collection volume  
**Dimensions:**
    
    - country_code
    - form_id
    - submission_source (admin_portal|mobile_app|self_service)
    
**Collection:**
    
    - **Interval:** N/A (event-driven)
    - **Method:** Odoo application logic incrementing counter
    
**Aggregation:**
    
    - **Functions:**
      
      - sum
      - rate
      
    - **Window:** 1h, 24h
    
**Justification:** REQ-3-008, REQ-7-006: Track dynamic form usage.  
    - **Name:** dfr_mobile_sync_sessions_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of mobile synchronization sessions completed.  
**Business_Context:** Mobile enumerator activity  
**Dimensions:**
    
    - country_code
    - user_id_mobile
    - status (success|failure|partial)
    
**Collection:**
    
    - **Interval:** N/A (event-driven)
    - **Method:** Odoo API logic incrementing counter
    
**Aggregation:**
    
    - **Functions:**
      
      - sum
      - rate
      
    - **Window:** 1h, 24h
    
**Justification:** REQ-4-006, REQ-4-011: Monitor mobile app synchronization activity and reliability.  
    - **Name:** dfr_mobile_sync_records_processed_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of records (farmer, form submissions) processed during mobile sync.  
**Business_Context:** Mobile data volume  
**Dimensions:**
    
    - country_code
    - record_type (farmer|form_submission)
    - direction (upload|download)
    
**Collection:**
    
    - **Interval:** N/A (event-driven)
    - **Method:** Odoo API logic incrementing counter
    
**Aggregation:**
    
    - **Functions:**
      
      - sum
      
    - **Window:** 1h, 24h
    
**Justification:** REQ-4-014, REQ-4-006: Monitor mobile data volume for performance and capacity planning.  
    
  - **Cache Performance Metrics:**
    
    
  - **External Dependency Metrics:**
    
    - **Name:** dfr_external_api_call_duration_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of calls to external services (SMS, Email, National ID).  
**Dependency:** sms_gateway|email_gateway|national_id_api  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Response Time:** Defined per external service agreement
    - **Availability:** Defined per external service agreement
    
**Justification:** REQ-NS-004, REQ-FHR-006, REQ-API-007: Monitor performance and reliability of critical external integrations.  
    - **Name:** dfr_external_api_call_errors_total  
**Type:** counter  
**Unit:** count  
**Description:** Number of errors when calling external services.  
**Dependency:** sms_gateway|email_gateway|national_id_api  
**Circuit Breaker Integration:** True  
**Justification:** REQ-NS-004, REQ-FHR-006, REQ-API-007: Track reliability of external integrations.  
    
  - **Error Metrics:**
    
    - **Name:** dfr_application_errors_total  
**Type:** counter  
**Unit:** count  
**Description:** Total number of unhandled exceptions in DFR Odoo modules.  
**Error Types:**
    
    - python_exception
    - orm_error
    - workflow_error
    
**Dimensions:**
    
    - country_code
    - module_name
    - error_class
    
**Alert Threshold:** >5 in 5 min  
**Justification:** REQ-SADG-005, REQ-DIO-009: Identify and address application stability issues.  
    - **Name:** dfr_api_endpoint_errors_total  
**Type:** counter  
**Unit:** count  
**Description:** Total errors (4xx, 5xx) returned by DFR API endpoints.  
**Error Types:**
    
    - 400
    - 401
    - 403
    - 404
    - 500
    - 503
    
**Dimensions:**
    
    - country_code
    - api_endpoint
    - http_status_code
    
**Alert Threshold:** >10 in 5 min for 5xx  
**Justification:** REQ-API-001, REQ-DIO-009: Monitor API health and client errors.  
    - **Name:** dfr_data_validation_errors_total  
**Type:** counter  
**Unit:** count  
**Description:** Total data validation errors during farmer registration or dynamic form submission.  
**Error Types:**
    
    - missing_required_field
    - invalid_format
    - duplicate_entry_attempt
    
**Dimensions:**
    
    - country_code
    - data_entity (farmer|dynamic_form)
    - validation_rule_violated
    
**Alert Threshold:** Spike detection  
**Justification:** REQ-FHR-012, REQ-3-002: Monitor data quality issues and de-duplication effectiveness.  
    - **Name:** dfr_mobile_sync_conflicts_total  
**Type:** counter  
**Unit:** count  
**Description:** Number of data conflicts detected during mobile synchronization.  
**Dimensions:**
    
    - country_code
    - user_id_mobile
    - conflict_type
    
**Alert Threshold:** Spike detection  
**Justification:** REQ-4-007: Monitor data consistency issues from offline work.  
    
  - **Throughput And Latency Metrics:**
    
    - **Name:** dfr_api_throughput_requests_per_second  
**Type:** gauge  
**Unit:** rps  
**Description:** Requests per second processed by key DFR API endpoints.  
**Percentiles:**
    
    
**Buckets:**
    
    
**Sla Targets:**
    
    - **P95:** N/A (target overall RPS defined per country)
    - **P99:** N/A
    
**Justification:** REQ-API-009: Monitor API load against capacity.  
    - **Name:** dfr_mobile_sync_duration_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Duration of mobile synchronization sessions.  
**Percentiles:**
    
    - 0.5
    - 0.9
    - 0.95
    
**Buckets:**
    
    - 0.1
    - 0.5
    - 1
    - 5
    - 10
    - 30
    - 60
    - 120
    
**Sla Targets:**
    
    - **P95:** 120 (for 500 records, REQ-4-014)
    - **P99:** N/A
    
**Justification:** REQ-4-014: Monitor mobile sync performance.  
    
  
- **Business Kpi Identification:**
  
  - **Critical Business Metrics:**
    
    - **Name:** kpi_total_registered_farmers  
**Type:** gauge  
**Unit:** count  
**Description:** Total number of unique, active farmers in the registry.  
**Business Owner:** National DFR Admin  
**Calculation:** COUNT(DISTINCT farmer_id) WHERE status = 'Active'  
**Reporting Frequency:** daily  
**Target:** Varies per country projection  
**Justification:** REQ-7-001: Core measure of DFR adoption and scale.  
    - **Name:** kpi_farmer_gender_disaggregation  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of registered farmers by gender.  
**Business Owner:** National DFR Admin / Policy Maker  
**Calculation:** GROUP BY gender, COUNT(*) / total_farmers * 100  
**Reporting Frequency:** daily  
**Target:** Country-specific inclusion targets  
**Justification:** REQ-7-001: Monitor inclusivity and gender balance.  
    - **Name:** kpi_farmer_age_distribution  
**Type:** histogram  
**Unit:** count  
**Description:** Distribution of registered farmers by age groups.  
**Business Owner:** National DFR Admin / Policy Maker  
**Calculation:** COUNT(*) GROUP BY age_bucket (e.g., <25, 25-35, 36-45, etc.)  
**Reporting Frequency:** daily  
**Target:** N/A (observational)  
**Justification:** REQ-7-001: Understand farmer demographics.  
    - **Name:** kpi_landholding_summary_hectares  
**Type:** gauge  
**Unit:** hectares  
**Description:** Total registered landholding area, average per farmer.  
**Business Owner:** National DFR Admin / Policy Maker  
**Calculation:** SUM(plot_size), AVG(plot_size_per_farmer)  
**Reporting Frequency:** daily  
**Target:** N/A (observational)  
**Justification:** REQ-7-001: Understand land use patterns.  
    - **Name:** kpi_dynamic_form_submissions_by_type_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of submissions for each active dynamic form type.  
**Business Owner:** National DFR Admin  
**Calculation:** COUNT(*) GROUP BY form_id  
**Reporting Frequency:** daily  
**Target:** N/A (observational)  
**Justification:** REQ-7-006: Track usage of specific dynamic forms.  
    
  - **User Engagement Metrics:**
    
    - **Name:** kpi_active_enumerators_daily  
**Type:** gauge  
**Unit:** count  
**Description:** Number of unique enumerators syncing data daily.  
**Segmentation:**
    
    - country_code
    - region (if applicable)
    
**Cohort Analysis:** False  
**Justification:** Monitor enumerator activity and system usage (implied by REQ-4-006).  
    - **Name:** kpi_portal_self_registrations_daily  
**Type:** gauge  
**Unit:** count  
**Description:** Number of new self-registrations submitted via the Farmer Portal daily.  
**Segmentation:**
    
    - country_code
    
**Cohort Analysis:** False  
**Justification:** Monitor Farmer Self-Service Portal adoption (REQ-FSSP-004).  
    
  - **Conversion Metrics:**
    
    - **Name:** kpi_self_registration_to_active_conversion_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of portal self-registrations that become fully 'Active' farmers.  
**Funnel Stage:** SelfRegistration -> Verification -> Active  
**Conversion Target:** Country-specific target (e.g., >70%)  
**Justification:** Measure efficiency of self-registration validation process (implied by REQ-FSSP-004, REQ-FHR-011).  
    
  - **Operational Efficiency Kpis:**
    
    - **Name:** kpi_duplicate_record_identification_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of incoming registrations flagged as potential duplicates by the system.  
**Calculation:** (PotentialDuplicatesFlagged / TotalIncomingRegistrations) * 100  
**Benchmark Target:** N/A (observational, indicates data quality/de-dupe effectiveness)  
**Justification:** Measure effectiveness of de-duplication strategy (REQ-FHR-012 to REQ-FHR-015).  
    - **Name:** kpi_mobile_sync_success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of mobile synchronization sessions that complete successfully.  
**Calculation:** (SuccessfulSyncSessions / TotalSyncSessions) * 100  
**Benchmark Target:** >98%  
**Justification:** Measure reliability of mobile data synchronization (REQ-4-006).  
    
  - **Revenue And Cost Metrics:**
    
    
  - **Customer Satisfaction Indicators:**
    
    
  
- **Collection Interval Optimization:**
  
  - **Sampling Frequencies:**
    
    - **Metric Category:** HardwareUtilization  
**Interval:** 60s  
**Justification:** Standard interval for infrastructure monitoring.  
**Resource Impact:** low  
    - **Metric Category:** RequestResponse  
**Interval:** 15s  
**Justification:** Capture rapid changes in request patterns and latency.  
**Resource Impact:** medium  
    - **Metric Category:** PostgreSQLPerformance  
**Interval:** 60s  
**Justification:** Balance detail with resource impact on DB.  
**Resource Impact:** medium  
    - **Metric Category:** ApplicationSpecificCounters  
**Interval:** N/A (event-driven)  
**Justification:** Incremented on actual occurrence.  
**Resource Impact:** low  
    - **Metric Category:** BusinessKPIs (derived)  
**Interval:** 1h (for dashboard refresh)  
**Justification:** KPIs aggregated for reporting, less frequent updates acceptable.  
**Resource Impact:** low  
    
  - **High Frequency Metrics:**
    
    - **Name:** http_request_duration_seconds  
**Interval:** 15s  
**Criticality:** high  
**Cost Justification:** Essential for meeting performance SLAs (REQ-API-009, REQ-FSSP-011).  
    - **Name:** dfr_api_endpoint_errors_total  
**Interval:** 15s (for rate calculation)  
**Criticality:** high  
**Cost Justification:** Early detection of API failures is critical.  
    
  - **Cardinality Considerations:**
    
    - **Metric Name:** http_requests_total  
**Estimated Cardinality:** Medium (path, status_code, instance)  
**Dimension Strategy:** Limit path cardinality if too high by grouping common paths.  
**Mitigation Approach:** Use Prometheus relabeling or aggregation rules if necessary.  
    - **Metric Name:** dfr_dynamic_form_submissions_total  
**Estimated Cardinality:** High (country_code, form_id)  
**Dimension Strategy:** Keep form_id as it is crucial. Aggregate at country level first.  
**Mitigation Approach:** Ensure form_id is a manageable set, potentially use form_name_version if IDs are too granular for some views.  
    
  - **Aggregation Periods:**
    
    - **Metric Type:** Counters (for rates)  
**Periods:**
    
    - 1m
    - 5m
    - 1h
    
**Retention Strategy:** Raw data for short term, aggregated for long term.  
    - **Metric Type:** Histograms (for percentiles)  
**Periods:**
    
    - 1m
    - 5m
    - 1h
    
**Retention Strategy:** Raw data for short term, aggregated (e.g., summary quantiles) for long term.  
    - **Metric Type:** BusinessKPIs  
**Periods:**
    
    - 1h
    - 24h
    - 7d
    - 30d
    
**Retention Strategy:** Aggregated data stored long-term.  
    
  - **Collection Methods:**
    
    - **Method:** PrometheusScrape  
**Applicable Metrics:**
    
    - system_cpu_usage_percentage
    - postgresql_active_connections
    - http_requests_total
    
**Implementation:** Prometheus server pulls metrics from exporters (node_exporter, postgres_exporter, Nginx log exporter, Odoo exporter).  
**Performance:** Scalable, industry standard.  
    - **Method:** ApplicationInstrumentation (Odoo)  
**Applicable Metrics:**
    
    - dfr_farmer_registrations_total
    - dfr_application_errors_total
    
**Implementation:** Custom Python code within Odoo modules updates Prometheus client library counters/gauges or writes to structured logs.  
**Performance:** Low overhead if implemented efficiently.  
    
  
- **Aggregation Method Selection:**
  
  - **Statistical Aggregations:**
    
    - **Metric Name:** http_request_duration_seconds  
**Aggregation Functions:**
    
    - avg
    - p50
    - p90
    - p95
    - p99
    - rate (for counts)
    
**Windows:**
    
    - 1m
    - 5m
    - 1h
    
**Justification:** Comprehensive performance analysis.  
    - **Metric Name:** dfr_farmer_registrations_total  
**Aggregation Functions:**
    
    - sum
    - rate
    
**Windows:**
    
    - 1h
    - 24h
    
**Justification:** Track growth and activity trends.  
    
  - **Histogram Requirements:**
    
    - **Metric Name:** http_request_duration_seconds  
**Buckets:**
    
    - 0.005
    - 0.01
    - 0.025
    - 0.05
    - 0.1
    - 0.25
    - 0.5
    - 1
    - 2.5
    - 5
    - 10
    
**Percentiles:**
    
    - 0.5
    - 0.9
    - 0.95
    - 0.99
    
**Accuracy:** High for performance SLAs.  
    - **Metric Name:** dfr_mobile_sync_duration_seconds  
**Buckets:**
    
    - 1
    - 5
    - 10
    - 30
    - 60
    - 120
    - 300
    
**Percentiles:**
    
    - 0.5
    - 0.9
    - 0.95
    
**Accuracy:** High for mobile performance (REQ-4-014).  
    
  - **Percentile Calculations:**
    
    - **Metric Name:** http_request_duration_seconds  
**Percentiles:**
    
    - 0.50
    - 0.90
    - 0.95
    - 0.99
    
**Algorithm:** Prometheus native histogram/summary  
**Accuracy:** High  
    
  - **Metric Types:**
    
    - **Name:** system_cpu_usage_percentage  
**Implementation:** gauge  
**Reasoning:** Represents a current value that can go up or down.  
**Resets Handling:** N/A  
    - **Name:** http_requests_total  
**Implementation:** counter  
**Reasoning:** Monotonically increasing value, used for rate calculations.  
**Resets Handling:** Prometheus `rate()` and `increase()` handle counter resets.  
    - **Name:** http_request_duration_seconds  
**Implementation:** histogram  
**Reasoning:** To observe distribution and calculate percentiles for latency.  
**Resets Handling:** N/A  
    
  - **Dimensional Aggregation:**
    
    - **Metric Name:** http_requests_total  
**Dimensions:**
    
    - status_code
    - path
    - method
    
**Aggregation Strategy:** Sum by desired dimensions for error rates, request rates per endpoint.  
**Cardinality Impact:** Medium, path needs careful management if highly dynamic.  
    
  - **Derived Metrics:**
    
    - **Name:** http_error_rate_percentage  
**Calculation:** sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100  
**Source Metrics:**
    
    - http_requests_total
    
**Update Frequency:** Evaluated by Prometheus query  
    - **Name:** kpi_daily_new_farmers_rate  
**Calculation:** increase(dfr_farmer_registrations_total[24h]) / 24 / 3600  
**Source Metrics:**
    
    - dfr_farmer_registrations_total
    
**Update Frequency:** Evaluated by Prometheus query  
    
  
- **Storage Requirements Planning:**
  
  - **Retention Periods:**
    
    - **Metric Type:** HighResolutionPerformanceMetrics (e.g., 15s http_request_duration)  
**Retention Period:** 7d  
**Justification:** Short-term debugging and fine-grained analysis.  
**Compliance Requirement:** N/A  
    - **Metric Type:** AggregatedPerformanceMetrics (e.g., 1h averages, percentiles)  
**Retention Period:** 90d  
**Justification:** Medium-term trend analysis and capacity planning.  
**Compliance Requirement:** N/A  
    - **Metric Type:** BusinessKPIs  
**Retention Period:** 2y  
**Justification:** Long-term strategic analysis and reporting as per REQ-7-001 timeframe.  
**Compliance Requirement:** N/A  
    - **Metric Type:** AuditLogMetrics (if derived, e.g., login_failures_total)  
**Retention Period:** As per REQ-SADG-009 for audit logs.  
**Justification:** Security and compliance.  
**Compliance Requirement:** Country-specific  
    
  - **Data Resolution:**
    
    - **Time Range:** 0-7 days  
**Resolution:** 15s-60s (raw)  
**Query Performance:** High for recent data  
**Storage Optimization:** None  
    - **Time Range:** 7-90 days  
**Resolution:** 5m-1h (aggregated)  
**Query Performance:** Medium for trends  
**Storage Optimization:** Downsampling  
    - **Time Range:** >90 days  
**Resolution:** 1h-24h (aggregated)  
**Query Performance:** Lower for historical reporting  
**Storage Optimization:** Aggressive downsampling  
    
  - **Downsampling Strategies:**
    
    - **Source Resolution:** 15s  
**Target Resolution:** 5m  
**Aggregation Method:** avg, sum, min, max, p95 for histograms  
**Trigger Condition:** Data older than 7 days  
    - **Source Resolution:** 1m  
**Target Resolution:** 1h  
**Aggregation Method:** avg, sum, min, max, p95 for histograms  
**Trigger Condition:** Data older than 7 days  
    
  - **Storage Performance:**
    
    - **Write Latency:** <100ms for Prometheus TSDB
    - **Query Latency:** <1s for typical Grafana dashboards (REQ-7-008 for system reports implies similar for metrics)
    - **Throughput Requirements:** Medium (dependent on number of metrics and scrape interval)
    - **Scalability Needs:** Vertical scaling of Prometheus initially, consider federated or remote write for very large scale.
    
  - **Query Optimization:**
    
    - **Query Pattern:** Time-series aggregation for dashboards  
**Optimization Strategy:** Use Prometheus recording rules for pre-aggregating common queries.  
**Indexing Requirements:**
    
    - Prometheus TSDB internal indexing
    
    
  - **Cost Optimization:**
    
    - **Strategy:** Aggressive downsampling and retention policies for non-critical metrics.  
**Implementation:** Configure Prometheus retention and recording rules.  
**Expected Savings:** Reduced storage costs.  
**Tradeoffs:** Loss of granularity for older data.  
    
  
- **Project Specific Metrics Config:**
  
  - **Standard Metrics:**
    
    - **Name:** nginx_http_requests_total  
**Type:** counter  
**Unit:** count  
**Collection:**
    
    - **Interval:** 15s
    - **Method:** Prometheus Nginx Log Exporter
    
**Thresholds:**
    
    - **Warning:** N/A
    - **Critical:** N/A
    
**Dimensions:**
    
    - host
    - path
    - method
    - status
    
    - **Name:** postgresql_connections  
**Type:** gauge  
**Unit:** count  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** Prometheus postgres_exporter
    
**Thresholds:**
    
    - **Warning:** 80% of max_connections
    - **Critical:** 95% of max_connections
    
**Dimensions:**
    
    - datname
    - state
    
    - **Name:** odoo_log_errors_total  
**Type:** counter  
**Unit:** count  
**Collection:**
    
    - **Interval:** N/A (from logs)
    - **Method:** Loki/Promtail alert rule or Odoo Prometheus Exporter parsing logs
    
**Thresholds:**
    
    - **Warning:** >5/min
    - **Critical:** >20/min
    
**Dimensions:**
    
    - logger_name
    - country_code
    
    
  - **Custom Metrics:**
    
    - **Name:** dfr_farmer_consent_status_count  
**Description:** Count of farmers by consent status.  
**Calculation:** Odoo model query grouping by consentStatus.  
**Type:** gauge  
**Unit:** count  
**Business Context:** Data Privacy Compliance (REQ-FHR-018)  
**Collection:**
    
    - **Interval:** 5m
    - **Method:** Custom Odoo Prometheus Exporter endpoint
    
**Alerting:**
    
    - **Enabled:** False
    - **Conditions:**
      
      
    
    - **Name:** dfr_deduplication_review_queue_size  
**Description:** Number of farmer records pending de-duplication review.  
**Calculation:** Odoo model query on farmer records with status 'Potential Duplicate'.  
**Type:** gauge  
**Unit:** count  
**Business Context:** Data Quality Management (REQ-FHR-015)  
**Collection:**
    
    - **Interval:** 5m
    - **Method:** Custom Odoo Prometheus Exporter endpoint
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - >100 for 24h
      
    
    - **Name:** dfr_notification_dispatch_failures_total  
**Description:** Total count of failed notification dispatches.  
**Calculation:** Counter incremented by Odoo notification module on gateway error.  
**Type:** counter  
**Unit:** count  
**Business Context:** Communication Reliability (REQ-NS-001)  
**Collection:**
    
    - **Interval:** N/A (event-driven)
    - **Method:** Odoo application instrumentation
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - rate > 5/min for 5 mins
      
    
    
  - **Dashboard Metrics:**
    
    - **Dashboard:** DFR System Overview  
**Metrics:**
    
    - system_cpu_usage_percentage
    - system_memory_usage_percentage
    - http_requests_total (rate)
    - http_request_duration_seconds (p95)
    - system_uptime_percentage
    - kpi_total_registered_farmers
    
**Refresh Interval:** 1m  
**Audience:** Super Administrators, National Administrators, IT Support  
    - **Dashboard:** DFR Farmer Registration KPIs  
**Metrics:**
    
    - kpi_total_registered_farmers
    - kpi_farmer_gender_disaggregation
    - kpi_farmer_age_distribution
    - kpi_daily_new_farmers_rate
    - kpi_portal_self_registrations_daily
    - kpi_self_registration_to_active_conversion_rate
    
**Refresh Interval:** 1h  
**Audience:** National Administrators, Policy Makers  
    - **Dashboard:** DFR Mobile App Operations  
**Metrics:**
    
    - dfr_mobile_sync_sessions_total (rate, success/failure breakdown)
    - dfr_mobile_sync_duration_seconds (p95)
    - dfr_mobile_sync_conflicts_total (rate)
    - kpi_active_enumerators_daily
    
**Refresh Interval:** 5m  
**Audience:** National Administrators, IT Support  
    
  
- **Implementation Priority:**
  
  - **Component:** Basic Hardware & HTTP Monitoring (CPU, Mem, Disk, HTTP req/err/lat)  
**Priority:** high  
**Dependencies:**
    
    - Prometheus
    - Grafana
    - node_exporter
    - Nginx Log Exporter
    
**Estimated Effort:** Low-Medium  
**Risk Level:** low  
  - **Component:** PostgreSQL Database Monitoring  
**Priority:** high  
**Dependencies:**
    
    - Prometheus
    - Grafana
    - postgres_exporter
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Core Application Transaction Metrics (Farmer Reg, Form Sub, Mobile Sync)  
**Priority:** high  
**Dependencies:**
    
    - Odoo Application Instrumentation
    - Odoo Prometheus Exporter
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Business KPIs Dashboard  
**Priority:** medium  
**Dependencies:**
    
    - Core App Transaction Metrics
    - Grafana
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** External Dependency Monitoring  
**Priority:** medium  
**Dependencies:**
    
    - Odoo Application Instrumentation
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Over-collection of high cardinality metrics leading to Prometheus performance issues.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Carefully select dimensions for metrics. Use relabeling/aggregation rules in Prometheus. Regularly review metric cardinality.  
**Contingency Plan:** Drop high cardinality metrics or dimensions. Scale Prometheus resources.  
  - **Risk:** Inaccurate business KPI calculation due to metric misinterpretation or collection errors.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Thoroughly validate KPI calculations against source data. Involve business stakeholders in metric definition and validation.  
**Contingency Plan:** Recalculate KPIs from raw data if possible. Issue corrections.  
  - **Risk:** Monitoring system outage leading to loss of operational visibility.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Monitor the monitoring system itself (e.g., Prometheus `up` metric). Ensure high availability setup for critical monitoring components.  
**Contingency Plan:** Rely on basic Odoo/system logs until monitoring is restored. Prioritize monitoring system recovery.  
  
- **Recommendations:**
  
  - **Category:** Metric Naming  
**Recommendation:** Adopt a consistent naming convention for all metrics (e.g., `dfr_<subsystem>_<metric_name>_<unit>`).  
**Justification:** Improves discoverability, readability, and manageability of metrics.  
**Priority:** high  
**Implementation Notes:** Document the chosen convention and enforce it in code reviews.  
  - **Category:** Dashboarding  
**Recommendation:** Develop role-specific dashboards in Grafana focusing on metrics relevant to each user group (Admin, Support, Policy Maker).  
**Justification:** Provides targeted insights and avoids information overload. Aligns with REQ-7-007 for role-based analytics.  
**Priority:** high  
**Implementation Notes:** Iterate on dashboards based on user feedback.  
  - **Category:** Alerting  
**Recommendation:** Start with conservative alert thresholds and refine them based on operational experience to minimize alert fatigue while ensuring critical issues are caught.  
**Justification:** Balances sensitivity with practicality, ensuring alerts are actionable.  
**Priority:** medium  
**Implementation Notes:** Implement a clear escalation path for alerts. Regularly review alert effectiveness.  
  - **Category:** Odoo Custom Exporter  
**Recommendation:** Develop or leverage a robust Odoo Prometheus exporter module to expose application-specific metrics efficiently, rather than relying solely on log parsing for all app metrics.  
**Justification:** More reliable and performant way to expose internal Odoo application state and counters as metrics.  
**Priority:** medium  
**Implementation Notes:** Ensure the exporter handles Odoo's multi-process architecture correctly.  
  


---

