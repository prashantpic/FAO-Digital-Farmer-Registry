# Specification

# 1. Files

- **Path:** prometheus/prometheus.yml  
**Description:** Main Prometheus configuration file. Defines global settings, rule file paths, scrape configurations (by including files from scrape_configs directory), and Alertmanager configuration.  
**Template:** YAML Configuration File  
**Dependancy Level:** 1  
**Name:** prometheus  
**Type:** Configuration  
**Relative Path:** prometheus/prometheus.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Prometheus Core Configuration
    - Alerting Integration
    - Service Discovery Setup
    
**Requirement Ids:**
    
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Defines the master configuration for the Prometheus monitoring server, including how it discovers targets, scrapes metrics, evaluates rules, and communicates with Alertmanager.  
**Logic Description:** Specifies 'global' block for default scrape interval/timeout. Lists 'rule_files' to load alert definitions. Includes 'scrape_configs' by referencing YAML files in the 'scrape_configs' directory. Defines 'alerting' block to specify Alertmanager server addresses.  
**Documentation:**
    
    - **Summary:** Central configuration for Prometheus, orchestrating metric collection, rule evaluation, and alert forwarding. References external files for modularity.
    
**Namespace:** dfr.ops.monitoring.prometheus  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/scrape_configs/odoo_exporter_jobs.yml  
**Description:** Prometheus scrape job definitions for Odoo application instances. Configures how Prometheus discovers and scrapes metrics from Odoo exporters (e.g., custom exporters or odoo_prometheus_exporter).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** odoo_exporter_jobs  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/odoo_exporter_jobs.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Application Monitoring
    - Odoo Performance Metrics Collection
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Configures Prometheus to scrape metrics exposed by Odoo instances, enabling monitoring of application performance and health.  
**Logic Description:** Defines one or more 'job_name' entries (e.g., 'dfr_odoo_app'). Specifies 'static_configs' or service discovery mechanism (e.g., 'dns_sd_configs', 'file_sd_configs') to find Odoo exporter endpoints. Sets 'metrics_path' (e.g., /metrics) and target port. Includes relabeling configurations if necessary.  
**Documentation:**
    
    - **Summary:** Defines scrape targets for Odoo application metrics. Allows Prometheus to collect data on Odoo performance, request rates, error counts, etc.
    
**Namespace:** dfr.ops.monitoring.prometheus.scrape_configs  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/scrape_configs/postgres_exporter_jobs.yml  
**Description:** Prometheus scrape job definitions for PostgreSQL database instances. Configures scraping from PostgreSQL exporters (e.g., pg_exporter, postgres_exporter).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** postgres_exporter_jobs  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/postgres_exporter_jobs.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PostgreSQL Database Monitoring
    - Database Performance Metrics Collection
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Configures Prometheus to scrape metrics from PostgreSQL exporters, enabling monitoring of database health, performance, and resource utilization.  
**Logic Description:** Defines job(s) for PostgreSQL exporters. Specifies targets (PostgreSQL exporter instances) via static configs or service discovery. Configures connection parameters for the exporter if needed (though often exporter is configured separately).  
**Documentation:**
    
    - **Summary:** Defines scrape targets for PostgreSQL database metrics. Allows collection of data on query performance, connections, replication status, etc.
    
**Namespace:** dfr.ops.monitoring.prometheus.scrape_configs  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/scrape_configs/nginx_exporter_jobs.yml  
**Description:** Prometheus scrape job definitions for Nginx reverse proxy instances. Configures scraping from Nginx exporters (e.g., nginx-prometheus-exporter or Nginx stub_status module).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** nginx_exporter_jobs  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/nginx_exporter_jobs.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Nginx Reverse Proxy Monitoring
    - Web Traffic Metrics Collection
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Configures Prometheus to scrape metrics from Nginx instances, enabling monitoring of web traffic, request rates, error rates, and connection statuses.  
**Logic Description:** Defines job(s) for Nginx exporters or stub_status endpoints. Specifies targets (Nginx instances/exporter endpoints). Sets appropriate metrics path and port.  
**Documentation:**
    
    - **Summary:** Defines scrape targets for Nginx web server/reverse proxy metrics. Facilitates monitoring of HTTP request patterns and server health.
    
**Namespace:** dfr.ops.monitoring.prometheus.scrape_configs  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/scrape_configs/node_exporter_jobs.yml  
**Description:** Prometheus scrape job definitions for host system metrics using Node Exporter. Configures scraping of OS-level metrics like CPU, memory, disk, and network usage.  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** node_exporter_jobs  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/node_exporter_jobs.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Host System Monitoring
    - Server Resource Utilization Metrics
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Configures Prometheus to scrape metrics from Node Exporter instances running on DFR servers, providing visibility into underlying system resource usage.  
**Logic Description:** Defines job(s) for Node Exporter. Specifies targets (servers running Node Exporter). Sets default Node Exporter port (9100) and metrics path (/metrics).  
**Documentation:**
    
    - **Summary:** Defines scrape targets for host-level system metrics (CPU, memory, disk, network) via Node Exporter.
    
**Namespace:** dfr.ops.monitoring.prometheus.scrape_configs  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/scrape_configs/backup_status_exporter_jobs.yml  
**Description:** Prometheus scrape job definitions for monitoring the status of DFR backup jobs. This might target a custom exporter or a metrics endpoint provided by the backup solution.  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** backup_status_exporter_jobs  
**Type:** Configuration  
**Relative Path:** prometheus/scrape_configs/backup_status_exporter_jobs.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Backup Job Status Monitoring
    
**Requirement Ids:**
    
    - REQ-SADG-011
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Configures Prometheus to scrape metrics related to the success, failure, and duration of DFR backup operations.  
**Logic Description:** Defines a job for the backup status exporter. Specifies the target(s) exposing backup metrics. Configures metrics path and port for the exporter. This helps in tracking backup success rates and identifying failures promptly.  
**Documentation:**
    
    - **Summary:** Defines scrape targets for monitoring DFR backup job statuses. Essential for ensuring data recoverability and operational reliability.
    
**Namespace:** dfr.ops.monitoring.prometheus.scrape_configs  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/general_system_alerts.yml  
**Description:** Prometheus alerting rules for general system health and availability (e.g., instance down, high CPU/memory usage on hosts).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** general_system_alerts  
**Type:** Configuration  
**Relative Path:** prometheus/rules/general_system_alerts.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Health Alerting
    - Host Resource Alerting
    
**Requirement Ids:**
    
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Defines alert conditions for fundamental system metrics to notify administrators of critical infrastructure issues.  
**Logic Description:** Contains 'groups' with 'rules'. Rules define 'alert' names, PromQL 'expr' for conditions (e.g., 'up == 0', 'node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10'), 'for' duration, 'labels' (severity), and 'annotations' (summary, description).  
**Documentation:**
    
    - **Summary:** Alerting rules for overall system health, such as server reachability and high resource utilization.
    
**Namespace:** dfr.ops.monitoring.prometheus.rules  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/odoo_specific_alerts.yml  
**Description:** Prometheus alerting rules specific to Odoo application performance and health (e.g., high error rates, slow response times, low worker availability).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** odoo_specific_alerts  
**Type:** Configuration  
**Relative Path:** prometheus/rules/odoo_specific_alerts.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Application Alerting
    - Odoo Performance Degradation Alerts
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Defines alert conditions based on Odoo-specific metrics to identify application-level issues.  
**Logic Description:** Rules for Odoo metrics: e.g., HTTP error rate ('rate(odoo_http_requests_total{status=~\"5..\"}[5m]) > ...'), average request latency, number of active Odoo workers. Includes alert names, PromQL expressions, duration, labels, and annotations.  
**Documentation:**
    
    - **Summary:** Alerting rules for Odoo application metrics, focusing on performance, error rates, and availability.
    
**Namespace:** dfr.ops.monitoring.prometheus.rules  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/postgres_specific_alerts.yml  
**Description:** Prometheus alerting rules specific to PostgreSQL database health (e.g., high number of slow queries, low disk space for data directory, replication lag).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** postgres_specific_alerts  
**Type:** Configuration  
**Relative Path:** prometheus/rules/postgres_specific_alerts.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PostgreSQL Database Alerting
    - Database Performance Issue Alerts
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Defines alert conditions based on PostgreSQL-specific metrics to identify database-level issues.  
**Logic Description:** Rules for PostgreSQL metrics: e.g., number of active connections nearing max_connections, high replication lag ('pg_replication_lag > ...'), low transaction ID wraparound remaining, slow query counts if available from exporter. Includes standard alert fields.  
**Documentation:**
    
    - **Summary:** Alerting rules for PostgreSQL database metrics, covering performance, resource usage, and replication health.
    
**Namespace:** dfr.ops.monitoring.prometheus.rules  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/nginx_specific_alerts.yml  
**Description:** Prometheus alerting rules specific to Nginx reverse proxy performance (e.g., high 5xx error rates, increased latency from Nginx perspective).  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** nginx_specific_alerts  
**Type:** Configuration  
**Relative Path:** prometheus/rules/nginx_specific_alerts.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Nginx Reverse Proxy Alerting
    - Web Traffic Anomaly Alerts
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Defines alert conditions based on Nginx-specific metrics to identify issues with web traffic handling.  
**Logic Description:** Rules for Nginx metrics: e.g., high HTTP 5xx server error rate ('rate(nginx_http_requests_total{status=~\"5..\"}[5m]) > ...'), increased request processing time, high number of active connections. Includes standard alert fields.  
**Documentation:**
    
    - **Summary:** Alerting rules for Nginx metrics, focusing on error rates, latency, and connection handling.
    
**Namespace:** dfr.ops.monitoring.prometheus.rules  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/backup_failure_alerts.yml  
**Description:** Prometheus alerting rules for DFR backup job failures or significant delays, based on metrics from the backup status exporter.  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** backup_failure_alerts  
**Type:** Configuration  
**Relative Path:** prometheus/rules/backup_failure_alerts.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Backup Failure Alerting
    - Backup Delay Alerting
    
**Requirement Ids:**
    
    - REQ-SADG-011
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Defines alert conditions to notify administrators immediately if DFR backup jobs fail or do not complete within expected timeframes.  
**Logic Description:** Rules for backup metrics: e.g., alert if 'backup_last_success_timestamp_seconds < time() - 25*3600' (backup older than 25 hours), or if 'backup_last_status != 0' (non-zero indicates failure). Includes alert names, PromQL expressions, duration, labels (critical severity), and detailed annotations for resolution guidance.  
**Documentation:**
    
    - **Summary:** Alerting rules specifically for monitoring the success and timeliness of DFR backup operations.
    
**Namespace:** dfr.ops.monitoring.prometheus.rules  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** alertmanager/alertmanager.yml  
**Description:** Main Alertmanager configuration file. Defines alert routing, receivers (e.g., email, Slack, PagerDuty), inhibition rules, and notification templates.  
**Template:** YAML Configuration File  
**Dependancy Level:** 1  
**Name:** alertmanager  
**Type:** Configuration  
**Relative Path:** alertmanager/alertmanager.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alert Routing
    - Notification Channel Configuration
    - Alert Grouping and Inhibition
    
**Requirement Ids:**
    
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Configures how alerts generated by Prometheus are processed, grouped, deduplicated, and delivered to operational teams.  
**Logic Description:** Defines 'global' settings (e.g., SMTP server details). Specifies 'route' block for default and specific alert routing based on labels (e.g., severity, service). Defines 'receivers' with configurations for different notification channels (email_configs, slack_configs, etc.). May include 'inhibit_rules' to suppress alerts. References 'templates' for custom notification formatting.  
**Documentation:**
    
    - **Summary:** Central configuration for Alertmanager, controlling alert lifecycle from reception to notification dispatch.
    
**Namespace:** dfr.ops.monitoring.alertmanager  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** alertmanager/templates/notification_templates.tmpl  
**Description:** Custom Go template file for Alertmanager notifications. Allows customization of the format and content of alerts sent via email, Slack, etc.  
**Template:** Go Template File  
**Dependancy Level:** 0  
**Name:** notification_templates  
**Type:** Configuration  
**Relative Path:** alertmanager/templates/notification_templates.tmpl  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Alert Notification Formatting
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Provides customizable templates for formatting alert notifications, ensuring clarity and relevance for recipients.  
**Logic Description:** Uses Go templating language. Defines named templates (e.g., 'dfr.email.subject', 'dfr.email.html_body', 'dfr.slack.message'). Accesses alert data (labels, annotations, status) via template variables (e.g., .Status, .Labels.severity, .Annotations.summary). Enables rich formatting for different notification channels.  
**Documentation:**
    
    - **Summary:** Custom templates for Alertmanager notifications, allowing tailored message content and appearance for various channels.
    
**Namespace:** dfr.ops.monitoring.alertmanager.templates  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/datasources/prometheus_datasource.yml  
**Description:** Grafana datasource provisioning file. Defines the Prometheus datasource for Grafana, allowing dashboards to query Prometheus metrics.  
**Template:** YAML Configuration File  
**Dependancy Level:** 0  
**Name:** prometheus_datasource  
**Type:** Configuration  
**Relative Path:** grafana/datasources/prometheus_datasource.yml  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Grafana Prometheus Datasource Provisioning
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Automates the configuration of the Prometheus datasource within Grafana, ensuring dashboards can connect to and visualize metrics from Prometheus.  
**Logic Description:** Specifies 'apiVersion' and 'datasources'. Defines a datasource with 'name' (e.g., 'DFR-Prometheus'), 'type' ('prometheus'), 'url' (Prometheus server address, e.g., http://prometheus:9090), 'access' ('server' or 'proxy'), and other relevant settings like 'isDefault'.  
**Documentation:**
    
    - **Summary:** Configuration file for automatically provisioning the Prometheus datasource in Grafana.
    
**Namespace:** dfr.ops.monitoring.grafana.datasources  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/dfr_system_overview.json  
**Description:** Grafana dashboard definition (JSON model) for a DFR system overview. Displays key health indicators and aggregated KPIs from various DFR components.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** dfr_system_overview  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/dfr_system_overview.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DFR System Health Dashboard
    - Aggregated KPI Visualization
    
**Requirement Ids:**
    
    - REQ-DIO-009
    - REQ-CM-011
    - REQ-TSE-008
    - A.2.4
    
**Purpose:** Provides a high-level visual summary of the DFR platform's health, performance, and key operational metrics for administrators and support teams.  
**Logic Description:** Grafana JSON dashboard model. Defines 'title', 'panels' (graphs, stat panels, tables), 'templating' (variables for filtering, e.g., country instance). Panels use PromQL queries against the Prometheus datasource to visualize metrics like overall system uptime, active users, registration rates, error summaries, and backup status.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard providing a holistic overview of the DFR system's status and key performance indicators.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/odoo_application_performance.json  
**Description:** Grafana dashboard definition for detailed Odoo application performance monitoring. Visualizes metrics like request latency, error rates, worker utilization, and database interaction times.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** odoo_application_performance  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/odoo_application_performance.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Performance Dashboard
    - Odoo Error Rate Visualization
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Provides in-depth insights into Odoo application performance, helping identify bottlenecks and diagnose issues.  
**Logic Description:** Grafana JSON dashboard model. Focuses on Odoo-specific metrics. Panels display request throughput, 95th/99th percentile latencies, HTTP status code distributions (2xx, 4xx, 5xx), Odoo worker process status, and potentially metrics related to specific Odoo modules or long-running tasks.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard dedicated to Odoo application performance metrics.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/postgresql_database_health.json  
**Description:** Grafana dashboard definition for PostgreSQL database health and performance. Visualizes metrics such as connection counts, query performance, replication status, cache hit rates, and disk usage.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** postgresql_database_health  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/postgresql_database_health.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PostgreSQL Health Dashboard
    - Database Query Performance Visualization
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Provides a comprehensive view of PostgreSQL database performance and resource utilization.  
**Logic Description:** Grafana JSON dashboard model. Panels visualize active connections, transactions per second, slow query counts, index hit rates, table/index sizes, replication lag, WAL generation rates, and disk space for data directories.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard focusing on PostgreSQL database health and performance.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/nginx_web_traffic.json  
**Description:** Grafana dashboard definition for Nginx reverse proxy monitoring. Visualizes web traffic metrics, request rates, response status codes, and upstream server health.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** nginx_web_traffic  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/nginx_web_traffic.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Nginx Traffic Dashboard
    - HTTP Error Analysis
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Provides insights into web traffic patterns and the health of the Nginx reverse proxy layer.  
**Logic Description:** Grafana JSON dashboard model. Panels display total requests, requests per second, distribution of HTTP status codes, active connections, upstream server response times (if Nginx is load balancing), and data transfer rates.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard for Nginx web traffic analysis and performance monitoring.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/host_node_metrics.json  
**Description:** Grafana dashboard definition for visualizing host system metrics collected by Node Exporter. Displays CPU, memory, disk I/O, network traffic, and load average for DFR servers.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** host_node_metrics  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/host_node_metrics.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Server Resource Monitoring Dashboard
    - Host Health Visualization
    
**Requirement Ids:**
    
    - REQ-DIO-009
    
**Purpose:** Provides a detailed view of server resource utilization, crucial for capacity planning and troubleshooting infrastructure performance issues.  
**Logic Description:** Grafana JSON dashboard model. Utilizes metrics from Node Exporter. Panels show CPU usage (per core, total, system/user/iowait), memory usage (total, free, cached, buffers), disk space usage per mount point, disk I/O operations, network traffic (in/out), and system load average.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard displaying key host-level system metrics from Node Exporter.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** grafana/dashboards/backup_operations_status.json  
**Description:** Grafana dashboard definition for visualizing the status and history of DFR backup operations. Displays metrics like last successful backup time, backup duration, and failure counts.  
**Template:** JSON Configuration File  
**Dependancy Level:** 1  
**Name:** backup_operations_status  
**Type:** Configuration  
**Relative Path:** grafana/dashboards/backup_operations_status.json  
**Repository Id:** DFR_MONITORING_CONFIG  
**Pattern Ids:**
    
    - ConfigurationAsCode
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Backup Status Dashboard
    - Backup History Visualization
    
**Requirement Ids:**
    
    - REQ-SADG-011
    - REQ-DIO-009
    - A.2.4
    
**Purpose:** Provides a clear visual representation of DFR backup job health, enabling quick identification of issues and trends in backup performance.  
**Logic Description:** Grafana JSON dashboard model. Uses metrics from the backup status exporter. Panels display status of the latest backup job (success/failure), timestamp of the last successful backup, duration of recent backup jobs, historical success/failure trends, and potentially backup size trends. Alerts related to backup failures are also important and handled by Alertmanager.  
**Documentation:**
    
    - **Summary:** JSON definition for a Grafana dashboard specifically for monitoring the status and history of DFR backup operations.
    
**Namespace:** dfr.ops.monitoring.grafana.dashboards  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableOdooAppMonitoring
  - EnablePostgresDBMonitoring
  - EnableNginxProxyMonitoring
  - EnableHostSystemMonitoring
  - EnableBackupStatusMonitoring
  - EnableAlertingSystemWide
  - EnableOdooAlerts
  - EnablePostgresAlerts
  - EnableNginxAlerts
  - EnableBackupFailureAlerts
  
- **Database Configs:**
  
  


---

