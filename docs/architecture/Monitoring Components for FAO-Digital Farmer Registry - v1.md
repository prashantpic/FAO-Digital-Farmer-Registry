# Specification

# 1. Monitoring Components

## 1.1. DFR Infrastructure & Container Monitoring
Monitors health and resource utilization of physical/virtual hosts and Docker containers running DFR components (Odoo, PostgreSQL, Nginx) as per REQ-DIO-009, B.2.2.9, A.2.4. This ensures operational stability and capacity planning.

### 1.1.3. Type
InfrastructureMonitoring

### 1.1.5. Provider
Prometheus (with node_exporter, cAdvisor) & Grafana

### 1.1.6. Features

- Host CPU, Memory, Disk I/O, Network utilization
- Docker container CPU, Memory, Disk I/O, Network utilization
- Container health status (restarts, uptime, state)
- Alerting on resource exhaustion or container failures

### 1.1.7. Configuration

- **Metrics Data Sources:**
  
  - node_exporter for host metrics
  - cAdvisor for Docker container metrics
  
- **Dashboarding:** Grafana dashboards for resource overview, container health, and alerting configuration via Alertmanager
- **Key Requirements:**
  
  - REQ-DIO-009
  - REQ-PCA-012
  - REQ-DIO-006
  

## 1.2. DFR PostgreSQL Database Monitoring
Monitors PostgreSQL database performance, health, connections, query efficiency, and resource usage critical for DFR operations, supporting REQ-DIO-009, B.2.2.9, A.2.4, and REQ-PCA-004 (PostgreSQL optimization).

### 1.2.3. Type
DatabaseMonitoring

### 1.2.5. Provider
Prometheus (with postgres_exporter) & Grafana

### 1.2.6. Features

- Active connections & connection pool status
- Query latency, throughput, and slow query identification
- Index hit rates, sequential scans, and table/index bloat
- Replication lag and status (if read replicas are used)
- Disk space usage for data, WALs, and temporary files
- Lock contention and deadlocks
- Transaction rates and database size growth

### 1.2.7. Configuration

- **Metrics Data Source:** postgres_exporter (e.g., querying pg_stat_activity, pg_stat_database, pg_locks, pg_stat_user_tables)
- **Dashboarding:** Grafana dashboards for PostgreSQL health, performance tuning, and alerting on critical database events
- **Key Requirements:**
  
  - REQ-DIO-009
  - REQ-PCA-004
  

## 1.3. DFR Odoo Application & API Monitoring
Monitors Odoo application server performance, worker health, web request/error rates, and REST API endpoint responsiveness (Admin Portal, Farmer Portal, Mobile & External APIs), as per REQ-DIO-009, B.2.2.9, A.2.4, REQ-API-009.

### 1.3.3. Type
ApplicationMonitoring

### 1.3.5. Provider
Odoo Internal Logging, Nginx Access/Error Logs, Prometheus (via Odoo Prometheus Exporter or Nginx Log Exporter) & Grafana

### 1.3.6. Features

- Odoo worker process count, status, and resource usage
- HTTP request rates, latency (overall, per endpoint for UI and API)
- HTTP error rates (e.g., 4xx, 5xx) and specific error types
- Python application exceptions and tracebacks (from Odoo logs)
- API endpoint specific metrics (e.g., request volume, latency for `REQ-API-009` targets)
- User session counts (for web portals)

### 1.3.7. Configuration

- **Log Sources For Metrics:**
  
  - Odoo server logs
  - Nginx access/error logs
  
- **Metrics Exporter:** Dedicated Odoo Prometheus exporter (e.g., `odoo-prometheus-exporter`) or Nginx log exporter (e.g., `nginx-log-exporter`)
- **Dashboarding:** Grafana dashboards for Odoo application health, API performance, and error tracking. Alerting on high error rates or slow responses.
- **Key Requirements:**
  
  - REQ-DIO-009
  - REQ-API-009
  - REQ-PCA-004
  - REQ-7-008
  

## 1.4. DFR Centralized Log Management
Centralizes logs from DFR Odoo application, Nginx reverse proxy, PostgreSQL database, and custom audit trails for comprehensive troubleshooting, operational analysis, and security auditing, as per REQ-SADG-005, REQ-FHR-010, REQ-SYSADM-007, REQ-DIO-009.

### 1.4.3. Type
LogAggregation

### 1.4.5. Provider
Grafana Loki & Promtail (or ELK Stack components like Filebeat, Logstash, Elasticsearch, Kibana)

### 1.4.6. Features

- Log collection from Odoo application (Python logging, `mail.thread` for audit), Nginx (access/error), PostgreSQL (database events, errors, slow queries)
- Centralized log storage, indexing, and retention management
- Log search, filtering, and analysis capabilities
- Correlation of logs with metrics (especially if using Loki with Prometheus)
- Access control for log data as per REQ-SADG-005

### 1.4.7. Configuration

- **Log Collection Agents:** Promtail (for Loki) or Filebeat/Fluentd agents on application/database/proxy servers
- **Log Sources:**
  
  - Odoo log files/streams
  - Nginx access/error log files
  - PostgreSQL log files/streams
  - Custom audit log outputs if separate
  
- **Log Storage And Query:** Loki or Elasticsearch backend with Kibana or Grafana for querying
- **Key Requirements:**
  
  - REQ-SADG-005
  - REQ-FHR-010
  - REQ-SYSADM-007
  

## 1.5. DFR Backup & Restore Process Monitoring
Monitors the success, failure, and duration of automated daily backup processes for PostgreSQL databases and critical system files, ensuring data recoverability as required by REQ-SADG-011, REQ-DIO-007.

### 1.5.3. Type
ProcessMonitoring

### 1.5.5. Provider
Custom Backup Scripts reporting status to Prometheus Pushgateway or logs to Centralized Log Management System

### 1.5.6. Features

- Backup job completion status (success/failure)
- Timestamp of last successful backup for each instance/component
- Backup job duration and size
- Alerting on backup failures or jobs exceeding expected duration
- Verification of restore test success/failure logs

### 1.5.7. Configuration

- **Status Source:** Backup script output (e.g., exit codes, structured log messages, metrics pushed to Prometheus Pushgateway)
- **Alerting:** Via Prometheus Alertmanager based on metrics or log-based alerts via Loki/ELK
- **Key Requirements:**
  
  - REQ-SADG-011
  - REQ-DIO-007
  - REQ-DIO-008
  - REQ-DIO-010
  

## 1.6. DFR Notification Gateway Monitoring
Monitors the interaction with third-party SMS, Email, and potentially Push Notification gateways, tracking dispatch success/failure rates and gateway errors, as per REQ-NS-* (Notification System requirements).

### 1.6.3. Type
IntegrationMonitoring

### 1.6.5. Provider
Odoo Application Logs (capturing gateway API responses/errors) & Custom Metrics sent to Prometheus

### 1.6.6. Features

- Notification dispatch success/failure rates per channel (SMS, Email, Push)
- Gateway API error counts and types (e.g., authentication failures, invalid recipient, rate limiting)
- Latency of gateway API responses
- Queue length for outgoing notifications (if applicable)
- Alerting on high failure rates, specific critical gateway errors, or prolonged dispatch delays

### 1.6.7. Configuration

- **Data Source:** Odoo application logs detailing gateway interactions; custom metrics instrumented in notification sending logic (e.g., using Prometheus client libraries).
- **Dashboarding:** Grafana dashboards for visualizing notification gateway health and performance.
- **Key Requirements:**
  
  - REQ-NS-001
  - REQ-NS-003
  - REQ-NS-004
  

## 1.7. DFR Mobile App Sync Health Monitoring (Server-Side)
Monitors the server-side API endpoints dedicated to mobile application synchronization. Tracks sync success/failure rates, data validation errors from mobile client submissions, and conflict occurrences to ensure reliable offline-first operation, as per REQ-4-006, REQ-4-007, REQ-4-011 (server-side aspect).

### 1.7.3. Type
APIMonitoring

### 1.7.5. Provider
Odoo API Endpoint Logs & Metrics (part of Odoo Application Monitoring) & Centralized Log Management

### 1.7.6. Features

- Mobile sync API request rates, latency, and error rates
- Count of successful versus failed synchronization sessions initiated by mobile apps
- Number of data conflicts detected and resolved/flagged on the server-side
- Data validation errors for records received from mobile devices
- Volume of data synced (up/down) per session or time period
- Alerting on high sync failure rates or significant data validation issues from mobile clients

### 1.7.7. Configuration

- **Data Source:** Nginx/Odoo logs for sync API endpoints; specific metrics instrumented in the Odoo backend's synchronization handling logic (e.g., conflict counts, validation errors).
- **Dashboarding:** Grafana dashboard dedicated to mobile synchronization health, tracking key metrics and error patterns.
- **Key Requirements:**
  
  - REQ-4-006
  - REQ-4-007
  - REQ-4-011
  - REQ-API-005
  - REQ-DIO-012
  



---

