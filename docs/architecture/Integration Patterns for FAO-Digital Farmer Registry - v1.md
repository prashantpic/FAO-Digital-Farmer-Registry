# Architecture Design Specification

# 1. Patterns

## 1.1. Request-Reply
### 1.1.2. Type
RequestReply

### 1.1.3. Implementation
Synchronous HTTP/REST calls. Odoo backend uses Python controllers (potentially with OCA `base_rest`) for its API endpoints. Mobile client (Flutter/Native) uses HTTP client libraries (e.g., `dio`, Retrofit). External integrations from Odoo use Python's `requests` library or specific service SDKs. Farmer Self-Service Portal uses standard HTML form submissions processed by Odoo controllers.

### 1.1.4. Applicability
Essential for real-time interactions: mobile app fetching/submitting data (farmer profiles, dynamic forms as per REQ-PCA-007, REQ-API-005), Farmer Self-Service Portal submissions (REQ-FSSP-004), Odoo backend integrating with external services like National ID validation (REQ-FHR-006, REQ-API-007), SMS/Email gateways (REQ-NS-004, REQ-API-008), and external systems consuming DFR APIs (REQ-API-004, REQ-API-006).

## 1.2. API Gateway
### 1.2.2. Type
APIGateway

### 1.2.3. Implementation
A custom Odoo module with HTTP controllers exposing consolidated and secured RESTful API endpoints, as per `dfr_api_gateway` layer. Utilizes Odoo's routing and security mechanisms (OAuth2/JWT as per REQ-PCA-007).

### 1.2.4. Applicability
Centralizing and securing API access for the mobile enumerator application and authorized external systems. Manages request routing, authentication, authorization (REQ-SADG-002), and provides a unified interface to backend services as outlined in REQ-API-001.

## 1.3. Backend for Frontend (BFF)
### 1.3.2. Type
BackendForFrontend

### 1.3.3. Implementation
Specific REST API endpoints within the DFR API Gateway, designed and optimized for the mobile enumerator application's unique requirements, particularly for data synchronization (REQ-API-005).

### 1.3.4. Applicability
Providing a tailored and optimized API interface specifically for the mobile client, simplifying data exchange for offline synchronization, form definition retrieval, and submission processing, thereby enhancing mobile app performance and reducing complexity on the client-side.

## 1.4. Data Synchronization (Offline Sync)
### 1.4.2. Type
DataSynchronization

### 1.4.3. Implementation
Bi-directional synchronization mechanism between the mobile application (local SQLite encrypted with SQLCipher) and the Odoo backend (PostgreSQL) via REST APIs. Involves client-side data queuing, batching, and a defined conflict resolution strategy (REQ-4-007).

### 1.4.4. Applicability
Enabling the core offline-first capability of the mobile enumerator application (REQ-PCA-006, REQ-4-003, REQ-4-006), allowing enumerators to work in areas with unreliable or no internet connectivity and synchronize data when online.

## 1.5. File Transfer
### 1.5.2. Type
FileTransfer

### 1.5.3. Implementation
Utilizing Odoo's standard import/export functionality for CSV and XLSX file formats for bulk data operations (REQ-DM-001, REQ-DM-004). PDF reports generated using Odoo's QWeb reporting engine (REQ-7-004).

### 1.5.4. Applicability
Essential for bulk data import (e.g., data migration from legacy systems), data export for external analysis or reporting, and providing formatted PDF reports from the system.

## 1.6. Idempotent Receiver
### 1.6.2. Type
IdempotentReceiver

### 1.6.3. Implementation
Logic embedded within the Odoo API endpoints, particularly those handling mobile data synchronization and submissions from external systems. This involves checking for duplicate requests (e.g., using unique transaction IDs or checksums of data) to prevent reprocessing.

### 1.6.4. Applicability
Crucial for ensuring data integrity and preventing unintended side effects from retried mobile sync operations (as per REQ-4-006 for resilient, idempotent sync) or submissions from external systems, especially over unreliable networks.

## 1.7. Retry Pattern
### 1.7.2. Type
Retry

### 1.7.3. Implementation
Client-side logic within the mobile application (for sync operations) and within the DFR Integration Layer (when calling external services like SMS/Email gateways or National ID APIs). Implements retries with appropriate backoff strategies (e.g., exponential backoff).

### 1.7.4. Applicability
Improving the resilience and reliability of communications between the mobile app and the backend (REQ-4-006), and between the DFR backend and external third-party services, by automatically re-attempting failed operations due to transient network issues or temporary service unavailability.

## 1.8. Circuit Breaker
### 1.8.2. Type
CircuitBreaker

### 1.8.3. Implementation
Protective wrapper logic around calls from the DFR Integration Layer to external third-party services (e.g., National ID validation, SMS/Email gateways). Monitors call success/failure rates and temporarily halts further calls if a service appears unavailable, preventing system degradation.

### 1.8.4. Applicability
Enhancing system stability and responsiveness by preventing the DFR platform from being bogged down by repeated, failing calls to unreliable or temporarily unavailable external dependencies (as required for robust integrations REQ-API-007, REQ-FHR-006, REQ-NS-004).

## 1.9. Client-Side Queueing
### 1.9.2. Type
ClientSideQueueing

### 1.9.3. Implementation
The mobile enumerator application stores data (new registrations, form submissions, edits) locally in its encrypted SQLite database when operating offline. This data acts as a queue for later transmission to the Odoo backend during synchronization.

### 1.9.4. Applicability
Fundamental to the offline-first functionality (REQ-4-003) of the mobile application. Ensures data captured by enumerators is not lost due to lack of internet connectivity and can be synced when a connection is re-established.



---

