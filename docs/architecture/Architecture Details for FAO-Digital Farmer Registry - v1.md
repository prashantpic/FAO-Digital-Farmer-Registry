# Architecture Design Specification

# 1. Style
ModularMonolith


---

# 2. Patterns

## 2.1. Odoo Module System
The system is built as a set of Odoo addons (modules). Odoo's framework inherently supports a modular architecture where functionalities are encapsulated in independent but interoperable modules. This aligns with the 'Modular Monolith' style.

### 2.1.3. Benefits

- Encapsulation of features within distinct modules (e.g., farmer registry, dynamic forms).
- Reusability of modules across different parts of the DFR system.
- Easier maintenance and updates of specific functionalities.
- Leverages Odoo's existing module management and extension capabilities.

### 2.1.4. Applicability

- **Scenarios:**
  
  - Developing extensions for the Odoo platform.
  - Systems requiring clear separation of functional concerns within a unified codebase.
  

## 2.2. Model-View-Controller (MVC) / Model-View-Template (MVT)
Odoo's web framework (including Web Client and Website module) follows an MVC/MVT-like pattern. Models define data and business logic, Views (XML, QWeb, OWL) define the presentation, and Controllers handle requests and orchestrate interactions.

### 2.2.3. Benefits

- Separation of concerns between data, presentation, and control logic.
- Improved maintainability and testability of UI components.
- Standardized way of building user interfaces within Odoo.

### 2.2.4. Applicability

- **Scenarios:**
  
  - Developing web interfaces using the Odoo framework (Admin Portal, Farmer Self-Service Portal).
  

## 2.3. Offline-First Synchronization
The mobile enumerator application operates primarily offline, storing data locally and synchronizing with the Odoo backend when connectivity is available. This involves bi-directional sync and conflict resolution.

### 2.3.3. Benefits

- Ensures enumerator productivity in areas with poor or no internet connectivity.
- Reduces data loss by persisting data locally.
- Improves mobile app responsiveness by operating on local data.

### 2.3.4. Applicability

- **Scenarios:**
  
  - Mobile applications used for field data collection in environments with unreliable network access.
  

## 2.4. RESTful API
A secure RESTful API layer is developed as a custom Odoo module to facilitate communication between the Odoo backend and the mobile application, as well as external systems.

### 2.4.3. Benefits

- Standardized, stateless communication protocol.
- Platform-agnostic integration for mobile and external systems.
- Leverages HTTP methods for CRUD operations.

### 2.4.4. Applicability

- **Scenarios:**
  
  - Exposing backend functionalities to client applications (mobile, web) or third-party services.
  - Enabling system integrations.
  

## 2.5. Role-Based Access Control (RBAC)
Access to system functionalities and data is controlled based on user roles defined within Odoo's security framework (groups, access rights, record rules).

### 2.5.3. Benefits

- Enforces principle of least privilege.
- Simplifies permission management.
- Enhances security by restricting access based on responsibilities.

### 2.5.4. Applicability

- **Scenarios:**
  
  - Systems with multiple user types requiring different levels of access to data and features.
  

## 2.6. Dynamic Form Engine
A dedicated Odoo module allows administrators to design custom data collection forms dynamically without coding, including various field types, validation, and conditional logic.

### 2.6.3. Benefits

- Flexibility to adapt data collection needs without new development cycles.
- Empowers non-technical users to create and manage forms.
- Supports diverse data collection scenarios.

### 2.6.4. Applicability

- **Scenarios:**
  
  - Systems requiring adaptable data collection tools for surveys, applications, or supplementary data gathering.
  



---

# 3. Layers

## 3.1. DFR Odoo Presentation Layer
Handles user interaction for the Admin Portal and Farmer Self-Service Portal within the Odoo framework. It renders UIs based on DFR-specific module definitions.

### 3.1.4. Technologystack
Odoo Web Client (JavaScript, XML, OWL), Odoo Website Module (QWeb, HTML, CSS, JavaScript)

### 3.1.5. Language
XML, JavaScript, Python (for Controllers)

### 3.1.6. Type
Presentation

### 3.1.7. Responsibilities

- Rendering user interfaces for DFR Admin Portal and Farmer Self-Service Portal.
- Handling user input and actions from web interfaces.
- Displaying data fetched from application services and models.
- Implementing client-side validation and interactivity.

### 3.1.8. Components

- DFR Admin Portal Views (XML, OWL, JS for Odoo Backend)
- Farmer Self-Service Portal Pages & Templates (QWeb, JS for Odoo Website)
- Odoo Controllers (Python) for serving web pages and handling form submissions from portals.

### 3.1.9. Dependencies

- **Layer Id:** dfr_odoo_application_services  
**Type:** Required  

## 3.2. DFR Odoo Application Services Layer
Encapsulates the core business logic, workflows, and use cases for the DFR platform. Implemented as services within DFR-specific Odoo modules.

### 3.2.4. Technologystack
Odoo Framework, Python

### 3.2.5. Language
Python

### 3.2.6. Type
ApplicationServices

### 3.2.7. Responsibilities

- Orchestrating farmer and household registration processes (REQ-FHR-*).
- Managing dynamic form creation, versioning, and submission processing (REQ-3-*).
- Implementing de-duplication logic (REQ-FHR-012 to REQ-FHR-015).
- Executing notification workflows (REQ-NS-*).
- Coordinating data import/export operations (REQ-DM-*).
- Providing services for analytics and reporting data aggregation (REQ-7-*).

### 3.2.8. Components

- dfr_farmer_registry module services
- dfr_dynamic_forms module services
- dfr_notifications module services
- dfr_data_management module services
- Odoo Automated Actions and Server Actions for workflows.

### 3.2.9. Dependencies

- **Layer Id:** dfr_odoo_domain_models  
**Type:** Required  
- **Layer Id:** dfr_integration  
**Type:** Optional  
- **Layer Id:** dfr_security  
**Type:** Required  

## 3.3. DFR Odoo Domain Models Layer
Defines the DFR data structures, entities (Farmer, Household, Plot, DynamicForm, etc.), their relationships, attributes, model-level validation, and core business rules directly associated with these entities. Leverages Odoo's ORM.

### 3.3.4. Technologystack
Odoo ORM, Python

### 3.3.5. Language
Python

### 3.3.6. Type
BusinessLogic

### 3.3.7. Responsibilities

- Defining DFR-specific data models (Farmer, Household, Plot, FormSubmission, etc.) (REQ-FHR-016).
- Enforcing data integrity through model constraints and validation rules.
- Implementing business logic tied to specific entities (e.g., UID generation REQ-FHR-002, status transitions REQ-FHR-011).
- Managing relationships between entities using Odoo ORM fields.

### 3.3.8. Components

- Python classes inheriting `odoo.models.Model` for all DFR entities.
- Field definitions, `@api.constrains`, `@api.onchange` methods.

### 3.3.9. Dependencies

- **Layer Id:** dfr_odoo_data_access  
**Type:** Required  

## 3.4. DFR Odoo Data Access Layer
Manages persistence and retrieval of DFR data using Odoo's Object-Relational Mapper (ORM) interacting with the PostgreSQL database.

### 3.4.4. Technologystack
Odoo ORM, PostgreSQL

### 3.4.5. Language
Python (ORM interactions), SQL (underlying)

### 3.4.6. Type
DataAccess

### 3.4.7. Responsibilities

- Executing CRUD (Create, Read, Update, Delete) operations on DFR entities via Odoo ORM.
- Translating Odoo domain queries into SQL queries for PostgreSQL.
- Managing database transactions and connections (handled by Odoo framework).
- Ensuring data persistence in PostgreSQL.

### 3.4.8. Components

- Odoo ORM API (e.g., `self.env['model'].create()`, `.search()`, `.write()`, `.unlink()`).
- PostgreSQL Database Management System.

## 3.5. DFR API Gateway Layer (Odoo Module)
Provides secure RESTful API endpoints for the mobile enumerator application and external system integrations. Built as a custom Odoo module.

### 3.5.4. Technologystack
Odoo Controllers (HTTP routes), Python, JSON, OpenAPI v3.x, OAuth2/JWT

### 3.5.5. Language
Python

### 3.5.6. Type
APIGateway

### 3.5.7. Responsibilities

- Exposing secure endpoints for mobile app data synchronization (farmer data, form definitions, submissions) (REQ-PCA-007, REQ-API-005).
- Providing endpoints for farmer lookup and data retrieval for authorized external systems (REQ-API-004).
- Handling API request/response serialization (JSON).
- Enforcing API authentication (OAuth2/JWT) and authorization based on DFR roles (REQ-SADG-002, REQ-5-012).

### 3.5.8. Components

- Odoo Controllers with `@http.route` decorators defining API endpoints.
- Authentication and authorization handlers for API requests.
- Data serialization/deserialization logic.

### 3.5.9. Interfaces

### 3.5.9.1. Mobile Sync API
#### 3.5.9.1.2. Type
REST/JSON

#### 3.5.9.1.3. Operations

- SyncFarmerData
- SyncFormDefinitions
- SubmitFormData

#### 3.5.9.1.4. Visibility
Public

### 3.5.9.2. External System API
#### 3.5.9.2.2. Type
REST/JSON

#### 3.5.9.2.3. Operations

- LookupFarmer
- RetrieveFarmerData

#### 3.5.9.2.4. Visibility
Public


### 3.5.10. Dependencies

- **Layer Id:** dfr_odoo_application_services  
**Type:** Required  
- **Layer Id:** dfr_security  
**Type:** Required  

## 3.6. DFR Integration Layer
Manages communication and data exchange with third-party external systems.

### 3.6.4. Technologystack
Python, Requests library, specific SDKs for external services (e.g., SMS gateways, National ID APIs).

### 3.6.5. Language
Python

### 3.6.6. Type
Integration

### 3.6.7. Responsibilities

- Integrating with National ID validation systems (REQ-FHR-006, REQ-API-007).
- Connecting to SMS and email gateway services for notifications (REQ-NS-003, REQ-API-008).
- Interfacing with weather and advisory service APIs (REQ-API-007).
- Handling data transformation and protocol adaptation for external services.

### 3.6.8. Components

- Connectors/Adapters for SMS gateways (e.g., Twilio, Vonage).
- Connectors for National ID validation APIs.
- Client modules for other third-party services.

### 3.6.9. Dependencies

- **Layer Id:** dfr_odoo_application_services  
**Type:** Required  

## 3.7. DFR Security Layer
Implements and enforces security policies across the DFR platform, leveraging Odoo's security framework and custom security measures.

### 3.7.4. Technologystack
Odoo Security Framework (`ir.model.access.csv`, `ir.rule`, `res.groups`), Python, OAuth2/JWT libraries, HTTPS/TLS.

### 3.7.5. Language
Python, XML (for Odoo security definitions)

### 3.7.6. Type
Security

### 3.7.7. Responsibilities

- Implementing Role-Based Access Control (RBAC) for all data entities and functionalities (REQ-5-*, REQ-SADG-001).
- Managing user authentication and session security for web portals.
- Enforcing API security (OAuth2/JWT authentication and authorization) (REQ-SADG-002).
- Configuring and recommending MFA for administrative users (REQ-5-008).
- Ensuring data transmission encryption (HTTPS/TLS 1.2+) (REQ-PCA-014).
- Managing secure storage of credentials and API keys (REQ-SADG-012).

### 3.7.8. Components

- Odoo security group definitions (`res.groups`).
- Odoo access control lists (`ir.model.access.csv`).
- Odoo record rules (`ir.rule`) for data scoping.
- Custom authentication providers for OAuth2/JWT if needed.
- Configuration of password policies.

## 3.8. DFR Infrastructure Layer
Underlying platform components, hosting environment, and operational tools for the DFR system.

### 3.8.4. Technologystack
Docker, PostgreSQL, Nginx (reverse proxy), Linux OS, CI/CD tools (Jenkins, GitLab CI, GitHub Actions), Backup utilities (`pg_dump`), Monitoring tools.

### 3.8.5. Language
Shell scripts, YAML (for Docker/CI/CD configs)

### 3.8.6. Type
Infrastructure

### 3.8.7. Responsibilities

- Providing containerized deployment environment for Odoo and PostgreSQL (REQ-PCA-015, REQ-DIO-006).
- Managing database backups and recovery procedures (REQ-DIO-007).
- Ensuring HTTPS termination via reverse proxy (REQ-DIO-005).
- Automating build, test, and deployment via CI/CD pipelines (REQ-DIO-011).
- Monitoring system health and performance (REQ-DIO-009).
- Supporting diverse hosting environments (on-premise, cloud) (REQ-PCA-012).

### 3.8.8. Components

- Dockerfiles and Docker Compose files.
- Nginx configuration.
- PostgreSQL server instance.
- CI/CD pipeline scripts.
- Backup and restore scripts.
- Monitoring agent configurations.

## 3.9. DFR Cross-Cutting Concerns
Addresses shared functionalities like logging, configuration, internationalization, and error handling across the DFR Odoo modules.

### 3.9.4. Technologystack
Odoo Framework (logging, i18n, config), Python.

### 3.9.5. Language
Python, XML (for Odoo config/views)

### 3.9.6. Type
CrossCutting

### 3.9.7. Responsibilities

- Providing consistent logging throughout the DFR modules (REQ-SADG-005).
- Managing system configuration parameters (e.g., via `ir.config_parameter`) (REQ-SYSADM-*).
- Supporting multilingual capabilities through Odoo's i18n (`.po` files) (REQ-LMS-*).
- Standardizing error handling and reporting.
- Maintaining audit trails (leveraging Odoo's `mail.thread` and custom logging) (REQ-FHR-010).

### 3.9.8. Components

- Odoo logging service.
- Odoo `ir.config_parameter` model for settings.
- Odoo translation mechanisms.
- Custom utility modules for shared functions.

## 3.10. Mobile Presentation (UI) Layer
User interface for the Android enumerator mobile application.

### 3.10.4. Technologystack
Native Android (Kotlin/Java with XML layouts, Jetpack Compose) or Cross-platform (Flutter with Dart and Widgets).

### 3.10.5. Language
Kotlin/Java or Dart

### 3.10.6. Type
Presentation

### 3.10.7. Responsibilities

- Rendering screens for farmer registration, dynamic forms, search, data lists (REQ-4-002).
- Capturing user input via forms and device sensors (GPS, camera for QR).
- Displaying data from local storage and providing intuitive navigation.
- Adhering to Android Material Design guidelines or platform-specific UX best practices.

### 3.10.8. Components

- Activities/Fragments or Flutter Widgets for each screen.
- UI layouts (XML or Dart code).
- Navigation components (Jetpack Navigation or Flutter Navigator).
- Custom UI elements for form rendering.

### 3.10.9. Dependencies

- **Layer Id:** mobile_application_logic  
**Type:** Required  

## 3.11. Mobile Application & Business Logic Layer
Handles application-specific logic, workflows, state management, and business rules on the mobile device.

### 3.11.4. Technologystack
Native Android (Kotlin/Java) or Cross-platform (Flutter with Dart). Architectural patterns like MVVM, MVI, or BLoC/Provider.

### 3.11.5. Language
Kotlin/Java or Dart

### 3.11.6. Type
BusinessLogic

### 3.11.7. Responsibilities

- Implementing client-side validation for form inputs (REQ-3-002 on mobile).
- Managing UI state and data flow between UI and data layers.
- Orchestrating offline data capture and modification workflows (REQ-4-003).
- Coordinating data synchronization processes with the backend.
- Handling logic for local de-duplication checks (optional, REQ-4-016).

### 3.11.8. Components

- ViewModels (Android Jetpack) or BLoCs/ChangeNotifiers (Flutter).
- Use Cases/Interactors encapsulating specific business operations.
- Validation rule implementations.
- State management solutions.

### 3.11.9. Dependencies

- **Layer Id:** mobile_data  
**Type:** Required  
- **Layer Id:** mobile_cross_cutting_services  
**Type:** Optional  

## 3.12. Mobile Data Layer
Manages local data storage (SQLite encrypted), data access objects, and the synchronization mechanism with the Odoo backend.

### 3.12.4. Technologystack
SQLite with SQLCipher (AES-256), Native Android (Room Persistence Library, Content Providers) or Cross-platform (sqflite with SQLCipher, Moor/Drift). REST client libraries (Retrofit, Dio).

### 3.12.5. Language
Kotlin/Java or Dart

### 3.12.6. Type
DataAccess

### 3.12.7. Responsibilities

- Storing and retrieving farmer data, form definitions, and submissions locally (REQ-4-003).
- Encrypting all sensitive data stored locally (REQ-4-004).
- Implementing bi-directional synchronization with the Odoo backend API (REQ-4-006).
- Handling conflict resolution during synchronization (REQ-4-007).
- Providing an abstraction over local data sources (Repository pattern).

### 3.12.8. Components

- SQLite database schema and DAOs (Data Access Objects).
- Repository classes for abstracting data operations.
- Synchronization engine/service.
- API client for communicating with DFR Odoo backend.
- Encryption/decryption utilities for local data.

## 3.13. Mobile Cross-Cutting Services Layer
Provides common utilities and services for the mobile application, such as location services, QR scanning, logging, and secure key management.

### 3.13.4. Technologystack
Native Android APIs (LocationManager, CameraX/ZXing) or Flutter Plugins (geolocator, qr_code_scanner, logger, flutter_secure_storage).

### 3.13.5. Language
Kotlin/Java or Dart

### 3.13.6. Type
CrossCutting

### 3.13.7. Responsibilities

- Capturing GPS coordinates for plots and homesteads (REQ-4-009).
- Scanning QR codes for farmer identification (REQ-4-008).
- Managing local application logs for troubleshooting (REQ-4-011).
- Securely managing encryption keys using Android Keystore or equivalent (REQ-4-004).
- Handling app updates and version compatibility checks (REQ-4-013).

### 3.13.8. Components

- GPS Location Service wrapper.
- QR Code Scanner utility.
- Logging utility.
- Secure Storage wrapper (for encryption keys).
- App Update checker service.



---

# 4. Quality Attributes

## 4.1. Scalability
System's ability to handle increasing data volumes and user load over time.

### 4.1.3. Tactics

- Configurable Odoo worker processes.
- Support for horizontal scaling of Odoo application servers (load balancing).
- PostgreSQL optimization techniques (indexing, query optimization, connection pooling).
- Efficient data structures and algorithms in custom modules.

### 4.1.4. Requirements

- REQ-PCA-004
- REQ-DIO-013

## 4.2. Security
Protection of data and system resources against unauthorized access and threats.

### 4.2.3. Tactics

- HTTPS/TLS 1.2+ for all client-server communication.
- OWASP Top 10 and MASVS adherence.
- Role-Based Access Control (RBAC) using Odoo security.
- OAuth2/JWT for API authentication.
- AES-256 encryption for mobile local data (SQLCipher).
- Secure credential management and regular patching.
- Maintaining a Software Bill of Materials (SBOM).

### 4.2.4. Requirements

- REQ-PCA-014
- REQ-SADG-*
- REQ-FHR-008
- REQ-5-*

## 4.3. Maintainability
Ease with which the system can be modified, corrected, and enhanced.

### 4.3.3. Tactics

- Modular design using Odoo addons.
- Adherence to coding standards (PEP 8 for Python, Odoo guidelines).
- Comprehensive inline and module-level documentation.
- Separation of configuration from code.
- Use of version control (Git) and semantic versioning.

### 4.3.4. Requirements

- REQ-PCA-016
- REQ-CM-*

## 4.4. Performance
System's responsiveness and efficiency under load.

### 4.4.3. Tactics

- Optimized database queries and indexing.
- Efficient data synchronization algorithms for mobile.
- Caching strategies where appropriate (e.g., for frequently accessed configurations or static data).
- Asynchronous processing for long-running tasks.
- Load testing and performance profiling.

### 4.4.4. Requirements

- REQ-4-014
- REQ-7-008
- REQ-API-009
- REQ-FSSP-011

## 4.5. Reliability & Availability
System's ability to operate without failure and be accessible when needed.

### 4.5.3. Tactics

- Automated daily backups of PostgreSQL databases and critical files.
- Documented data restoration procedures and DR plan (RTO/RPO targets).
- Resilient network communication for mobile sync (resumable, idempotent).
- Use of Docker for consistent deployments.
- System monitoring and alerting.

### 4.5.4. Requirements

- REQ-SADG-011
- REQ-DIO-007
- REQ-DIO-010
- REQ-4-006

## 4.6. Offline Capability
Mobile application's ability to function without an active internet connection.

### 4.6.3. Tactics

- Offline-first architecture for the mobile app.
- Local SQLite database for storing data offline.
- Bi-directional synchronization mechanism with conflict resolution.

### 4.6.4. Requirements

- REQ-PCA-006
- REQ-4-003
- REQ-4-006
- REQ-4-007

## 4.7. Interoperability & Extensibility
System's ability to interact with other systems and be extended with new functionalities.

### 4.7.3. Tactics

- Secure RESTful API layer (OpenAPI v3.x) for integrations.
- Modular Odoo addon architecture allowing new modules for extensions.
- Configurable integration points for third-party services.
- Clear separation between core platform and country-specific modules/configurations.

### 4.7.4. Requirements

- REQ-PCA-003
- REQ-PCA-007
- REQ-API-*

## 4.8. Usability & Accessibility
Ease of use for end-users and accessibility for people with disabilities.

### 4.8.3. Tactics

- Intuitive UI/UX design for web and mobile interfaces.
- Mobile-responsive design for portals.
- Adherence to WCAG 2.1 Level AA for Farmer Self-Service Portal.
- Multilingual support.
- Clear icons, simple language, and logical workflows for enumerators.

### 4.8.4. Requirements

- REQ-4-002
- REQ-FSSP-001
- REQ-FSSP-013
- REQ-LMS-*



---

