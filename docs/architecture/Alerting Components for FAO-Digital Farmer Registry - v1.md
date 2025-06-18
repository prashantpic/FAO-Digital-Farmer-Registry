# Specification

# 1. Alerting And Incident Response Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-17
  - **Technology Stack:**
    
    - Odoo 18.0 Community
    - Python
    - PostgreSQL
    - Docker
    - Nginx
    - Android (Flutter/Native)
    
  - **Metrics Configuration:**
    
    - Prometheus/Grafana based monitoring for infrastructure, PostgreSQL, Odoo application & API performance. Centralized logging via Loki/ELK. Custom metrics for business processes.
    
  - **Monitoring Needs:**
    
    - Ensure high availability, performance, data integrity, and operational health of DFR instances. Proactive detection of issues affecting farmer registration, data synchronization, and portal accessibility.
    
  - **Environment:** production
  
- **Alert Condition And Threshold Design:**
  
  - **Critical Metrics Alerts:**
    
    - **Metric:** API_P95_Latency_ms  
**Condition:** P95 Latency > 500ms over 5 minutes for critical API endpoints  
**Threshold Type:** static  
**Value:** 500  
**Justification:** REQ-API-009: Ensure API responsiveness for mobile app and external integrations.  
**Business Impact:** Degraded mobile app performance, slow external system integrations, potential data sync issues.  
    - **Metric:** PostgreSQL_CPU_Utilization_Percent  
**Condition:** CPU Utilization > 85% sustained for 10 minutes  
**Threshold Type:** static  
**Value:** 85  
**Justification:** REQ-DIO-009, REQ-PCA-004: Prevent database performance degradation or unavailability.  
**Business Impact:** Slow DFR operations, potential data processing failures, system instability.  
    - **Metric:** System_Backup_Failure_Count  
**Condition:** Backup job failure count > 0 for daily backups  
**Threshold Type:** static  
**Value:** 0  
**Justification:** REQ-SADG-011, REQ-DIO-007: Critical for data recoverability and DR.  
**Business Impact:** Risk of data loss in case of system failure, inability to meet RPO.  
    - **Metric:** Host_Disk_Space_Free_Percent  
**Condition:** Free disk space < 15% on critical partitions (OS, DB data, Odoo filestore)  
**Threshold Type:** static  
**Value:** 15  
**Justification:** REQ-DIO-009: Prevent system crashes due to disk exhaustion.  
**Business Impact:** System unavailability, data corruption, inability to log or store new data.  
    
  - **Threshold Strategies:**
    
    - **Strategy:** static  
**Applicable Metrics:**
    
    - API_P95_Latency_ms
    - PostgreSQL_CPU_Utilization_Percent
    - System_Backup_Failure_Count
    - Host_Disk_Space_Free_Percent
    - Odoo_App_Error_Rate_Percent
    
**Implementation:** Fixed values based on performance requirements and operational stability.  
**Advantages:**
    
    - Simple to implement and understand.
    
    - **Strategy:** dynamic  
**Applicable Metrics:**
    
    - Mobile_Sync_Error_Rate_Percent_Baseline_Deviation
    - Notification_Gateway_Error_Rate_Percent_Baseline_Deviation
    
**Implementation:** Thresholds based on rolling averages or standard deviations from historical data, if advanced monitoring tools support it. Otherwise, static with periodic review.  
**Advantages:**
    
    - Adapts to normal fluctuations, reduces false positives for metrics with natural variance.
    
    
  - **Baseline Deviation Alerts:**
    
    
  - **Predictive Alerts:**
    
    
  - **Compound Conditions:**
    
    
  
- **Severity Level Classification:**
  
  - **Severity Definitions:**
    
    - **Level:** Critical  
**Criteria:** System down, core functionality unavailable, imminent data loss/corruption risk, major security breach.  
**Business Impact:** Service outage, significant financial/reputational loss, SLA breach for RTO/RPO.  
**Customer Impact:** All users unable to use critical features.  
**Response Time:** <15 minutes acknowledgement, <4 hours resolution target (as per REQ-TSE-008 for Critical SLA)  
**Escalation Required:** True  
    - **Level:** High  
**Criteria:** Significant performance degradation, partial loss of non-critical functionality, increased risk of data issues, security vulnerability identified.  
**Business Impact:** Degraded service, moderate financial/reputational impact.  
**Customer Impact:** Significant portion of users impacted or key features slow/unreliable.  
**Response Time:** <1 hour acknowledgement, <8 hours resolution target (as per REQ-TSE-008 for High SLA)  
**Escalation Required:** True  
    - **Level:** Medium  
**Criteria:** Minor performance issues, isolated functionality errors, potential future risks building up (e.g., disk space warning).  
**Business Impact:** Minor service inconvenience, low financial/reputational impact.  
**Customer Impact:** Some users experience minor issues, non-critical features affected.  
**Response Time:** <2 hours acknowledgement, <2 business days resolution target (as per REQ-TSE-008 for Medium SLA)  
**Escalation Required:** False  
    - **Level:** Warning  
**Criteria:** Metrics approaching thresholds, potential for future issues if unaddressed, informational.  
**Business Impact:** No immediate impact, but potential for future impact if ignored.  
**Customer Impact:** No immediate customer impact.  
**Response Time:** Acknowledge within 4 business hours.  
**Escalation Required:** False  
    
  - **Business Impact Matrix:**
    
    
  - **Customer Impact Criteria:**
    
    
  - **Sla Violation Severity:**
    
    
  - **System Health Severity:**
    
    
  
- **Notification Channel Strategy:**
  
  - **Channel Configuration:**
    
    - **Channel:** email  
**Purpose:** Primary notification for all severity levels to National Admins and Support Teams.  
**Applicable Severities:**
    
    - Critical
    - High
    - Medium
    - Warning
    
**Time Constraints:** 24/7  
**Configuration:**
    
    - **Smtp_Server:** country_specific_smtp
    - **From_Address:** dfr-alerts@example.com
    
    - **Channel:** odoo_internal_notification  
**Purpose:** Secondary notification for Medium/Warning alerts for logged-in National Admins.  
**Applicable Severities:**
    
    - Medium
    - Warning
    
**Time Constraints:** During Odoo Admin Portal usage  
**Configuration:**
    
    - **Odoo_Activity_Type:** DFR_Alert
    
    - **Channel:** sms  
**Purpose:** Emergency notification for Critical alerts to designated On-Call personnel.  
**Applicable Severities:**
    
    - Critical
    
**Time Constraints:** 24/7  
**Configuration:**
    
    - **Sms_Gateway_Integration_Details:** country_specific_sms_gateway_config
    
    
  - **Routing Rules:**
    
    - **Condition:** Severity == 'Critical'  
**Severity:** Critical  
**Alert Type:** Any  
**Channels:**
    
    - email
    - sms
    
**Priority:** 1  
    - **Condition:** Severity == 'High'  
**Severity:** High  
**Alert Type:** Any  
**Channels:**
    
    - email
    
**Priority:** 2  
    - **Condition:** Severity == 'Medium'  
**Severity:** Medium  
**Alert Type:** Any  
**Channels:**
    
    - email
    - odoo_internal_notification
    
**Priority:** 3  
    - **Condition:** Severity == 'Warning'  
**Severity:** Warning  
**Alert Type:** Any  
**Channels:**
    
    - email
    - odoo_internal_notification
    
**Priority:** 4  
    
  - **Time Based Routing:**
    
    
  - **Ticketing Integration:**
    
    - **System:** Internal Odoo-based Issue Tracker (if developed) or External System (future consideration)  
**Trigger Conditions:**
    
    - Severity == 'Critical'
    - Severity == 'High'
    
**Ticket Priority:** Matches Alert Severity  
**Auto Assignment:** True  
    
  - **Emergency Notifications:**
    
    
  - **Chat Platform Integration:**
    
    
  
- **Alert Correlation Implementation:**
  
  - **Grouping Requirements:**
    
    - **Grouping Criteria:** By Source Component (e.g., specific API endpoint, DB instance) AND Alert Type  
**Time Window:** 5 minutes  
**Max Group Size:** 10  
**Suppression Strategy:** Consolidate similar alerts into a single notification with count.  
    
  - **Parent Child Relationships:**
    
    
  - **Topology Based Correlation:**
    
    
  - **Time Window Correlation:**
    
    
  - **Causal Relationship Detection:**
    
    
  - **Maintenance Window Suppression:**
    
    - **Maintenance Type:** Scheduled System Maintenance (Patching, Upgrades)  
**Suppression Scope:**
    
    - All alerts from affected components/country instance
    
**Automatic Detection:** False  
**Manual Override:** True  
    
  
- **False Positive Mitigation:**
  
  - **Noise Reduction Strategies:**
    
    - **Strategy:** Use 'for X minutes' conditions for rate/utilization alerts  
**Implementation:** Monitoring tool's alert rule configuration.  
**Applicable Alerts:**
    
    - HighAPILatency
    - HighAPIErrorRate
    - PostgreSQL_HighCPU
    
**Effectiveness:** High for reducing noise from transient spikes.  
    
  - **Confirmation Counts:**
    
    - **Alert Type:** RateBasedError  
**Confirmation Threshold:** 3  
**Confirmation Window:** 5 minutes  
**Reset Condition:** Rate below threshold for 10 minutes  
    - **Alert Type:** ResourceUtilization  
**Confirmation Threshold:** 2  
**Confirmation Window:** 10 minutes  
**Reset Condition:** Utilization below threshold for 15 minutes  
    
  - **Dampening And Flapping:**
    
    - **Metric:** NetworkConnectivityToExternalGateway  
**Dampening Period:** 5 minutes  
**Flapping Threshold:** 3  
**Suppression Duration:** 15 minutes  
    
  - **Alert Validation:**
    
    
  - **Smart Filtering:**
    
    
  - **Quorum Based Alerting:**
    
    
  
- **On Call Management Integration:**
  
  - **Escalation Paths:**
    
    - **Severity:** Critical  
**Escalation Levels:**
    
    - **Level:** 1  
**Recipients:**
    
    - PrimaryOnCallAdmin
    - PrimaryOnCallSupport
    
**Escalation Time:** 15 minutes  
**Requires Acknowledgment:** True  
    - **Level:** 2  
**Recipients:**
    
    - SecondaryOnCallAdmin
    - SupportTeamLead
    
**Escalation Time:** 30 minutes (if L1 no ack)  
**Requires Acknowledgment:** True  
    
**Ultimate Escalation:** ManagementNotificationList  
    - **Severity:** High  
**Escalation Levels:**
    
    - **Level:** 1  
**Recipients:**
    
    - PrimaryOnCallSupport
    - NationalAdminGroup
    
**Escalation Time:** 30 minutes  
**Requires Acknowledgment:** True  
    
**Ultimate Escalation:** SupportTeamLead  
    
  - **Escalation Timeframes:**
    
    
  - **On Call Rotation:**
    
    - **Team:** NationalAdmins  
**Rotation Type:** weekly  
**Handoff Time:** Monday 09:00 Local  
**Backup Escalation:** SuperAdminTeam  
    - **Team:** ITSupportTeam  
**Rotation Type:** daily_business_hours_then_oncall  
**Handoff Time:** Daily 09:00 Local & 17:00 Local  
**Backup Escalation:** ITManagement  
    
  - **Acknowledgment Requirements:**
    
    - **Severity:** Critical  
**Acknowledgment Timeout:** 15 minutes  
**Auto Escalation:** True  
**Requires Comment:** False  
    - **Severity:** High  
**Acknowledgment Timeout:** 30 minutes  
**Auto Escalation:** True  
**Requires Comment:** False  
    
  - **Incident Ownership:**
    
    - **Assignment Criteria:** Based on alert type and affected component (e.g., DB issues to DBA, App issues to App Support).  
**Ownership Transfer:** Formal handover in ticketing system or during shift change.  
**Tracking Mechanism:** Ticketing system (REQ-TSE-008).  
    
  - **Follow The Sun Support:**
    
    
  
- **Project Specific Alerts Config:**
  
  - **Alerts:**
    
    - **Name:** HighAPILatency  
**Description:** P95 API response time for critical endpoints exceeds 500ms for 5 minutes.  
**Condition:** avg(api_p95_latency_ms{critical_endpoint='true'}) > 500 for 5m  
**Threshold:** >500ms  
**Severity:** High  
**Channels:**
    
    - email
    
**Correlation:**
    
    - **Group Id:** API_Performance
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - SupportTeamLead
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/api-latency
    - **Troubleshooting Steps:**
      
      - Check Odoo application server logs.
      - Check PostgreSQL performance.
      - Review Nginx logs.
      - Analyze recent deployments.
      
    
    - **Name:** HighAPIErrorRate  
**Description:** API error rate (5xx) for critical endpoints exceeds 5% over 5 minutes.  
**Condition:** sum(rate(api_http_requests_total{status_code=~'5..', critical_endpoint='true'}[5m])) / sum(rate(api_http_requests_total{critical_endpoint='true'}[5m])) > 0.05  
**Threshold:** >5%  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** API_Availability
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - PrimaryOnCallAdmin
      - DevTeamLead
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 3
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/api-errors
    - **Troubleshooting Steps:**
      
      - Check Odoo application server logs for exceptions.
      - Verify backend service health (DB, Odoo workers).
      - Inspect recent code changes.
      
    
    - **Name:** OdooAppErrorRate  
**Description:** Overall Odoo application error rate (logged exceptions) is high.  
**Condition:** rate(odoo_application_exceptions_total[5m]) > 10  
**Threshold:** >10 errors/min  
**Severity:** High  
**Channels:**
    
    - email
    
**Correlation:**
    
    - **Group Id:** Odoo_App_Health
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - SupportTeamLead
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/odoo-app-errors
    - **Troubleshooting Steps:**
      
      - Review Odoo server logs for specific error messages.
      - Check for resource contention (CPU, memory).
      - Analyze recently deployed custom modules.
      
    
    - **Name:** PostgreSQL_HighCPU  
**Description:** PostgreSQL CPU utilization is above 85% for 10 minutes.  
**Condition:** avg_over_time(postgresql_cpu_utilization_percent[10m]) > 85  
**Threshold:** >85%  
**Severity:** High  
**Channels:**
    
    - email
    
**Correlation:**
    
    - **Group Id:** DB_Performance
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      - During_Data_Migration_Window
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - DBA_Team
      - SupportTeamLead
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 10m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/db-high-cpu
    - **Troubleshooting Steps:**
      
      - Identify long-running or inefficient queries using pg_stat_activity.
      - Check for high connection counts.
      - Review recent schema changes or large data operations.
      
    
    - **Name:** PostgreSQL_LowDiskSpaceData  
**Description:** PostgreSQL data partition free disk space is below 15%.  
**Condition:** postgresql_disk_free_percent{partition='/var/lib/postgresql/data'} < 15  
**Threshold:** <15%  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** DB_Availability
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - DBA_Team
      - PrimaryOnCallAdmin
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 1m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/db-low-disk
    - **Troubleshooting Steps:**
      
      - Identify large tables/indexes.
      - Archive or delete old WAL files if applicable and safe.
      - Increase disk capacity.
      
    
    - **Name:** ServerHost_LowDiskSpaceOS  
**Description:** Server OS partition (hosting Odoo logs/filestore) free disk space is below 10%.  
**Condition:** host_disk_free_percent{partition='/opt/odoo' OR partition='/var/log'} < 10  
**Threshold:** <10%  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** Server_Availability
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - PrimaryOnCallAdmin
      - SysAdminTeam
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 1m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/server-low-disk
    - **Troubleshooting Steps:**
      
      - Archive or delete old Odoo logs.
      - Check Odoo filestore size and archive old attachments if policy allows.
      - Increase disk capacity.
      
    
    - **Name:** BackupFailure  
**Description:** Daily system backup job failed.  
**Condition:** system_backup_status{job_type='daily_full'} == 'failed'  
**Threshold:** status == failed  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** Data_Protection
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - PrimaryOnCallAdmin
      - SysAdminTeam
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** N/A
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/backup-failure
    - **Troubleshooting Steps:**
      
      - Check backup script logs for error details.
      - Verify connectivity to backup storage.
      - Ensure sufficient disk space for backup creation.
      - Manually trigger backup job after fixing the issue.
      
    
    - **Name:** MobileSyncAPI_HighErrorRate  
**Description:** Mobile Sync API endpoints are experiencing a high error rate (>5% for 5 mins).  
**Condition:** sum(rate(api_http_requests_total{endpoint_group='mobile_sync', status_code=~'5..|401|403'}[5m])) / sum(rate(api_http_requests_total{endpoint_group='mobile_sync'}[5m])) > 0.05  
**Threshold:** >5%  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** Mobile_Sync_Health
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - PrimaryOnCallAdmin
      - MobileDevTeamLead
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/mobile-sync-errors
    - **Troubleshooting Steps:**
      
      - Check Odoo logs for sync API errors.
      - Verify database connectivity and performance.
      - Investigate for schema mismatches or conflict resolution issues.
      
    
    - **Name:** NotificationGateway_FailureRate  
**Description:** Failure rate for sending notifications via external gateways (SMS/Email) exceeds 10% over 15 minutes.  
**Condition:** avg_over_time(notification_gateway_failure_rate_percent{channel='any'}[15m]) > 10  
**Threshold:** >10%  
**Severity:** High  
**Channels:**
    
    - email
    
**Correlation:**
    
    - **Group Id:** Notification_System_Health
    - **Suppression Rules:**
      
      - If_Specific_Gateway_Maintenance_Announced
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - SupportTeamLead
      - NationalAdminGroup
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** True
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 15m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/notification-gateway-failures
    - **Troubleshooting Steps:**
      
      - Check Odoo logs for gateway API error messages.
      - Verify gateway credentials and account status.
      - Check network connectivity to the gateway provider.
      - Test with an alternate gateway if configured.
      
    
    - **Name:** OdooMailQueue_ExcessiveLength  
**Description:** Odoo mail queue (for emails) has more than 100 pending messages for over 30 minutes.  
**Condition:** odoo_mail_queue_length > 100 for 30m  
**Threshold:** >100 emails  
**Severity:** Medium  
**Channels:**
    
    - email
    - odoo_internal_notification
    
**Correlation:**
    
    - **Group Id:** Notification_System_Health
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** False
    - **Escalation Time:** 
    - **Escalation Path:**
      
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 30m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/odoo-mail-queue
    - **Troubleshooting Steps:**
      
      - Check Odoo scheduler status.
      - Inspect `mail.mail` records for error states.
      - Verify email server configuration and connectivity.
      
    
    - **Name:** SSLCertificate_NearingExpiry  
**Description:** SSL/TLS certificate for a DFR instance web endpoint is nearing expiry (e.g., within 14 days).  
**Condition:** ssl_certificate_days_until_expiry{instance='country_instance_domain'} < 14  
**Threshold:** <14 days  
**Severity:** High  
**Channels:**
    
    - email
    
**Correlation:**
    
    - **Group Id:** Security_Compliance
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** False
    - **Escalation Time:** 
    - **Escalation Path:**
      
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 24h
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** http://internal-wiki/runbook/ssl-cert-renewal
    - **Troubleshooting Steps:**
      
      - Initiate SSL certificate renewal process.
      - Verify new certificate installation on reverse proxy.
      - Confirm certificate chain validity.
      
    
    - **Name:** OdooWorker_Unavailable  
**Description:** Number of available Odoo workers is critically low or zero.  
**Condition:** odoo_active_workers_count < odoo_configured_workers_min_threshold for 5m  
**Threshold:** defined by odoo_configured_workers_min_threshold  
**Severity:** Critical  
**Channels:**
    
    - email
    - sms
    
**Correlation:**
    
    - **Group Id:** Odoo_App_Availability
    - **Suppression Rules:**
      
      - During_Scheduled_Maintenance
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - PrimaryOnCallAdmin
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      - Attempt Odoo service restart if configured
      
    - **Runbook Url:** http://internal-wiki/runbook/odoo-worker-unavailable
    - **Troubleshooting Steps:**
      
      - Check Odoo server logs for worker startup errors.
      - Verify server resources (CPU, Memory).
      - Inspect Odoo configuration for worker settings.
      
    
    
  - **Alert Groups:**
    
    - **Group Id:** API_Performance  
**Name:** API Performance Issues  
**Alerts:**
    
    - HighAPILatency
    
**Suppression Strategy:** Suppress if Odoo_App_Health group is active  
**Escalation Override:**   
    - **Group Id:** DB_Availability  
**Name:** Database Availability Issues  
**Alerts:**
    
    - PostgreSQL_LowDiskSpaceData
    
**Suppression Strategy:**   
**Escalation Override:**   
    
  - **Notification Templates:**
    
    - **Template Id:** DefaultEmailCritical  
**Channel:** email  
**Format:** Subject: CRITICAL DFR Alert: {{AlertName}} for {{CountryInstance}}

Severity: {{Severity}}
Time: {{Timestamp}}
Description: {{Description}}
Condition: {{Condition}}
Metric Value: {{MetricValue}}

Runbook: {{RunbookURL}}

Please investigate immediately.  
**Variables:**
    
    - AlertName
    - CountryInstance
    - Severity
    - Timestamp
    - Description
    - Condition
    - MetricValue
    - RunbookURL
    
    - **Template Id:** DefaultSMSSimple  
**Channel:** sms  
**Format:** CRITICAL DFR Alert: {{AlertName}} on {{CountryInstance}}. Details: {{ShortDescription}}. Investigate.  
**Variables:**
    
    - AlertName
    - CountryInstance
    - ShortDescription
    
    
  
- **Implementation Priority:**
  
  - **Component:** Core Performance & Availability Alerts (API, DB, Host, Backup)  
**Priority:** high  
**Dependencies:**
    
    - MonitoringInfrastructureSetup
    
**Estimated Effort:** 10 days  
**Risk Level:** low  
  - **Component:** Application Specific Alerts (Mobile Sync, Notifications, Odoo Workers)  
**Priority:** high  
**Dependencies:**
    
    - CoreAlertsSetup
    - ApplicationMetricsInstrumentation
    
**Estimated Effort:** 8 days  
**Risk Level:** medium  
  - **Component:** Advanced Alerting Features (Correlation, Escalation Policies)  
**Priority:** medium  
**Dependencies:**
    
    - CoreAlertsSetup
    
**Estimated Effort:** 5 days  
**Risk Level:** low  
  
- **Risk Assessment:**
  
  - **Risk:** Alert Fatigue due to too many low-value alerts or poorly tuned thresholds.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Focus on essential, actionable alerts. Iteratively tune thresholds. Implement effective correlation and suppression.  
**Contingency Plan:** Regular review and refinement of alert configuration based on operational feedback.  
  - **Risk:** Failure of notification delivery channels.  
**Impact:** medium  
**Probability:** low  
**Mitigation:** Use multiple notification channels for critical alerts. Monitor health of notification gateways themselves.  
**Contingency Plan:** Manual check of monitoring dashboards during critical periods. Fallback communication protocols.  
  
- **Recommendations:**
  
  - **Category:** ThresholdTuning  
**Recommendation:** Establish initial static thresholds based on requirements, then iteratively refine them based on observed system behavior in Staging and early Production.  
**Justification:** Ensures alerts are meaningful and reduces false positives over time.  
**Priority:** high  
**Implementation Notes:** Allocate time for threshold review post-deployment of each country instance.  
  - **Category:** RunbookDevelopment  
**Recommendation:** Develop detailed, actionable runbooks for each defined alert, linked directly from alert notifications.  
**Justification:** Speeds up incident response and ensures consistent troubleshooting procedures.  
**Priority:** high  
**Implementation Notes:** Runbooks should be living documents, updated as the system evolves.  
  - **Category:** AlertReviewProcess  
**Recommendation:** Implement a regular (e.g., monthly or quarterly) process to review alert effectiveness, false positive rates, and incident response outcomes to continuously improve the alerting strategy.  
**Justification:** Maintains the relevance and effectiveness of the alerting system as the DFR platform evolves.  
**Priority:** medium  
**Implementation Notes:** Involve National Admins and Support Teams in the review process.  
  


---

