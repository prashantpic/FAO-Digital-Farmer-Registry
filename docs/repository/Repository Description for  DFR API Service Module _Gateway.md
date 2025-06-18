# Repository Specification

# 1. Name
DFR API Service Module (Gateway)


---

# 2. Description
Central Odoo module acting as an API Gateway, exposing secure RESTful API endpoints for the mobile enumerator application and authorized external systems. Handles request routing, authentication (OAuth2/JWT), authorization, and data serialization (JSON).


---

# 3. Type
ApiGateway


---

# 4. Namespace
odoo.addons.dfr_api_services


---

# 5. Output Path
dfr_addons/dfr_api_services


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python


---

# 8. Technology
Odoo HTTP Controllers, JSON, OpenAPI v3.x, OAuth2/JWT


---

# 9. Thirdparty Libraries

- PyJWT
- OCA base_rest (evaluate)


---

# 10. Dependencies

- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS
- DFR_MOD_RBAC_CONFIG
- DFR_MOD_SECURITY_AUDIT_LOG


---

# 11. Layer Ids

- dfr_api_gateway


---

# 12. Requirements

- **Requirement Id:** REQ-PCA-007  
- **Requirement Id:** REQ-API-001  
- **Requirement Id:** REQ-API-002  
- **Requirement Id:** REQ-API-003  
- **Requirement Id:** REQ-API-005  
- **Requirement Id:** REQ-SADG-002  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
ModularMonolith


---

# 16. Id
DFR_MOD_API_GATEWAY


---

# 17. Architecture_Map

- dfr_api_gateway


---

# 18. Components_Map

- dfr-module-rest-api-008


---

# 19. Requirements_Map

- REQ-PCA-007
- REQ-API-001
- REQ-API-002
- REQ-API-003
- REQ-API-005
- REQ-SADG-002


---

# 20. Endpoints

## 20.1. API Authentication Token Endpoint
OAuth2/JWT token issuance endpoint for authenticating API clients (mobile app, external systems).

### 20.1.4. Type
REST_API

### 20.1.5. Method
POST

### 20.1.6. Url Pattern
/api/dfr/v1/auth/token

### 20.1.7. Request Schema
Client credentials (grant_type, client_id, client_secret, username, password as per OAuth2 flow)

### 20.1.8. Response Schema
Access token, refresh token, token type, expires_in

### 20.1.9. Authentication Required
False

### 20.1.10. Authorization Required
False

### 20.1.11. Data Formats

- JSON
- application/x-www-form-urlencoded

### 20.1.12. Communication Protocol
HTTPS

### 20.1.13. Layer Ids

- dfr_api_gateway
- dfr_security

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-API-003  
- **Requirement Id:** REQ-SADG-002  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
True

### 20.1.18. Architecture_Map

- dfr_api_gateway
- dfr_security

### 20.1.19. Components_Map

- dfr-module-rest-api-008

### 20.1.20. Requirements_Map

- REQ-API-003
- REQ-SADG-002

## 20.2. Mobile Sync Farmers Data Endpoint
Bi-directional synchronization of farmer, household, and plot data for the mobile app.

### 20.2.4. Type
REST_API

### 20.2.5. Method
POST

### 20.2.6. Url Pattern
/api/dfr/v1/sync/farmers

### 20.2.7. Request Schema
Batch of created/updated farmer records from mobile; request for updated records from server

### 20.2.8. Response Schema
Batch of updated farmer records from server; server acknowledgement of mobile data

### 20.2.9. Authentication Required
True

### 20.2.10. Authorization Required
True

### 20.2.11. Data Formats

- JSON

### 20.2.12. Communication Protocol
HTTPS

### 20.2.13. Layer Ids

- dfr_api_gateway

### 20.2.14. Dependencies

- DFR_MOD_FARMER_REGISTRY

### 20.2.15. Requirements

- **Requirement Id:** REQ-API-005  
- **Requirement Id:** REQ-4-006  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_api_gateway

### 20.2.19. Components_Map

- dfr-module-rest-api-008

### 20.2.20. Requirements_Map

- REQ-API-005
- REQ-4-006

## 20.3. Mobile Sync Form Definitions Endpoint
Synchronization of dynamic form definitions to the mobile app.

### 20.3.4. Type
REST_API

### 20.3.5. Method
GET

### 20.3.6. Url Pattern
/api/dfr/v1/sync/form-definitions

### 20.3.7. Request Schema
Request for updated form definitions (optionally with last sync timestamp)

### 20.3.8. Response Schema
List of active/updated dynamic form definitions (JSON schema or structured Odoo models)

### 20.3.9. Authentication Required
True

### 20.3.10. Authorization Required
True

### 20.3.11. Data Formats

- JSON

### 20.3.12. Communication Protocol
HTTPS

### 20.3.13. Layer Ids

- dfr_api_gateway

### 20.3.14. Dependencies

- DFR_MOD_DYNAMIC_FORMS

### 20.3.15. Requirements

- **Requirement Id:** REQ-API-005  
- **Requirement Id:** REQ-3-006  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- dfr_api_gateway

### 20.3.19. Components_Map

- dfr-module-rest-api-008

### 20.3.20. Requirements_Map

- REQ-API-005
- REQ-3-006

## 20.4. Mobile Sync Form Submissions Endpoint
Receives dynamic form submissions from the mobile app.

### 20.4.4. Type
REST_API

### 20.4.5. Method
POST

### 20.4.6. Url Pattern
/api/dfr/v1/sync/form-submissions

### 20.4.7. Request Schema
Batch of completed dynamic form submissions from mobile

### 20.4.8. Response Schema
Server acknowledgement of submissions

### 20.4.9. Authentication Required
True

### 20.4.10. Authorization Required
True

### 20.4.11. Data Formats

- JSON

### 20.4.12. Communication Protocol
HTTPS

### 20.4.13. Layer Ids

- dfr_api_gateway

### 20.4.14. Dependencies

- DFR_MOD_DYNAMIC_FORMS

### 20.4.15. Requirements

- **Requirement Id:** REQ-API-005  
- **Requirement Id:** REQ-3-008  

### 20.4.16. Version
1.0

### 20.4.17. Is Public
False

### 20.4.18. Architecture_Map

- dfr_api_gateway

### 20.4.19. Components_Map

- dfr-module-rest-api-008

### 20.4.20. Requirements_Map

- REQ-API-005
- REQ-3-008

## 20.5. External Farmer Lookup Endpoint
Allows authorized external systems to lookup farmer data by UID, National ID, or other criteria.

### 20.5.4. Type
REST_API

### 20.5.5. Method
GET

### 20.5.6. Url Pattern
/api/dfr/v1/external/farmers/lookup

### 20.5.7. Request Schema
Query parameters (e.g., uid, national_id, name, village)

### 20.5.8. Response Schema
List of matching farmer profiles (core data, subject to permissions)

### 20.5.9. Authentication Required
True

### 20.5.10. Authorization Required
True

### 20.5.11. Data Formats

- JSON

### 20.5.12. Communication Protocol
HTTPS

### 20.5.13. Layer Ids

- dfr_api_gateway

### 20.5.14. Dependencies

- DFR_MOD_FARMER_REGISTRY

### 20.5.15. Requirements

- **Requirement Id:** REQ-API-004  

### 20.5.16. Version
1.0

### 20.5.17. Is Public
False

### 20.5.18. Architecture_Map

- dfr_api_gateway

### 20.5.19. Components_Map

- dfr-module-rest-api-008

### 20.5.20. Requirements_Map

- REQ-API-004

## 20.6. External Farmer Data Retrieval Endpoint
Allows authorized external systems to retrieve detailed farmer data (core profile, specific dynamic form data) by Farmer ID.

### 20.6.4. Type
REST_API

### 20.6.5. Method
GET

### 20.6.6. Url Pattern
/api/dfr/v1/external/farmers/{farmerId}

### 20.6.7. Request Schema
Path parameter: farmerId. Optional query params for specific data sections.

### 20.6.8. Response Schema
Detailed farmer profile data (subject to permissions).

### 20.6.9. Authentication Required
True

### 20.6.10. Authorization Required
True

### 20.6.11. Data Formats

- JSON

### 20.6.12. Communication Protocol
HTTPS

### 20.6.13. Layer Ids

- dfr_api_gateway

### 20.6.14. Dependencies

- DFR_MOD_FARMER_REGISTRY
- DFR_MOD_DYNAMIC_FORMS

### 20.6.15. Requirements

- **Requirement Id:** REQ-API-004  

### 20.6.16. Version
1.0

### 20.6.17. Is Public
False

### 20.6.18. Architecture_Map

- dfr_api_gateway

### 20.6.19. Components_Map

- dfr-module-rest-api-008

### 20.6.20. Requirements_Map

- REQ-API-004

## 20.7. API Health Check Endpoint
Provides a simple health check endpoint for monitoring API availability.

### 20.7.4. Type
REST_API

### 20.7.5. Method
GET

### 20.7.6. Url Pattern
/api/dfr/v1/health

### 20.7.7. Request Schema
None

### 20.7.8. Response Schema
{ "status": "UP" }

### 20.7.9. Authentication Required
False

### 20.7.10. Authorization Required
False

### 20.7.11. Data Formats

- JSON

### 20.7.12. Communication Protocol
HTTPS

### 20.7.13. Layer Ids

- dfr_api_gateway

### 20.7.14. Dependencies


### 20.7.15. Requirements

- **Requirement Id:** REQ-DIO-009  

### 20.7.16. Version
1.0

### 20.7.17. Is Public
True

### 20.7.18. Architecture_Map

- dfr_api_gateway

### 20.7.19. Components_Map

- dfr-module-rest-api-008

### 20.7.20. Requirements_Map

- REQ-DIO-009



---

