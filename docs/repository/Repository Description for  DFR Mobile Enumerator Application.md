# Repository Specification

# 1. Name
DFR Mobile Enumerator Application


---

# 2. Description
Android application for enumerators to register farmers, collect data offline and online, manage plot information, and synchronize data with the DFR backend. Implements offline-first functionality with local encrypted storage.


---

# 3. Type
MobileFrontend


---

# 4. Namespace
com.fao.dfr.mobile


---

# 5. Output Path
dfr_mobile_app


---

# 6. Framework
Flutter/Dart (preferred) or Native Android (Kotlin/Java)


---

# 7. Language
Dart (or Kotlin/Java)


---

# 8. Technology
SQLite, SQLCipher, REST Client (Dio/Retrofit), GPS, QR Scanner


---

# 9. Thirdparty Libraries

- sqflite
- sqlcipher_flutter_libs
- dio
- flutter_bloc
- geolocator
- mobile_scanner
- flutter_secure_storage


---

# 10. Dependencies

- DFR_MOD_API_GATEWAY


---

# 11. Layer Ids

- mobile_presentation
- mobile_application_logic
- mobile_data
- mobile_cross_cutting_services


---

# 12. Requirements

- **Requirement Id:** REQ-PCA-006  
- **Requirement Id:** REQ-4-001  
- **Requirement Id:** REQ-4-002  
- **Requirement Id:** REQ-4-003  
- **Requirement Id:** REQ-4-004  
- **Requirement Id:** REQ-4-006  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
LayeredArchitecture


---

# 16. Id
DFR_MOBILE_APP


---

# 17. Architecture_Map

- mobile_presentation
- mobile_application_logic
- mobile_data
- mobile_cross_cutting_services


---

# 18. Components_Map

- dfr-mobile-app-presentation-014
- dfr-mobile-app-business-logic-015
- dfr-mobile-app-data-sync-016
- dfr-mobile-app-local-data-store-017
- dfr-mobile-app-platform-services-018


---

# 19. Requirements_Map

- REQ-PCA-006
- REQ-4-001
- REQ-4-002
- REQ-4-003
- REQ-4-004
- REQ-4-006


---

# 20. Endpoints

## 20.1. Mobile Farmer Registration Function
Functional endpoint representing the user flow for registering a new farmer or editing an existing one on the mobile app. Involves data capture, local validation, and queuing for sync.

### 20.1.4. Type
MOBILE_FUNCTIONAL_ENDPOINT

### 20.1.5. Method
None

### 20.1.6. Url Pattern
None

### 20.1.7. Request Schema
Farmer profile data (name, DOB, contact, plot details, GPS etc.) entered via UI forms.

### 20.1.8. Response Schema
UI confirmation of local save, visual feedback.

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Mobile UI State Objects

### 20.1.12. Communication Protocol
Internal App Logic

### 20.1.13. Layer Ids

- mobile_presentation
- mobile_application_logic
- mobile_data

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-4-002  
- **Requirement Id:** REQ-4-003  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- mobile_presentation
- mobile_application_logic
- mobile_data

### 20.1.19. Components_Map

- dfr-mobile-app-presentation-014
- dfr-mobile-app-business-logic-015
- dfr-mobile-app-local-data-store-017

### 20.1.20. Requirements_Map

- REQ-4-002
- REQ-4-003

## 20.2. Mobile Dynamic Form Submission Function
Functional endpoint for rendering and submitting dynamic forms on the mobile app. Involves fetching form definitions, capturing responses, and queuing for sync.

### 20.2.4. Type
MOBILE_FUNCTIONAL_ENDPOINT

### 20.2.5. Method
None

### 20.2.6. Url Pattern
None

### 20.2.7. Request Schema
User responses to dynamic form fields.

### 20.2.8. Response Schema
UI confirmation of local save, visual feedback.

### 20.2.9. Authentication Required
True

### 20.2.10. Authorization Required
True

### 20.2.11. Data Formats

- Mobile UI State Objects

### 20.2.12. Communication Protocol
Internal App Logic

### 20.2.13. Layer Ids

- mobile_presentation
- mobile_application_logic
- mobile_data

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-4-002  
- **Requirement Id:** REQ-3-006  
- **Requirement Id:** REQ-3-008  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- mobile_presentation
- mobile_application_logic
- mobile_data

### 20.2.19. Components_Map

- dfr-mobile-app-presentation-014
- dfr-mobile-app-business-logic-015
- dfr-mobile-app-local-data-store-017

### 20.2.20. Requirements_Map

- REQ-4-002
- REQ-3-006
- REQ-3-008

## 20.3. Mobile Data Synchronization Service
Internal mobile app service responsible for bi-directional data synchronization with the DFR backend API, including conflict resolution and queue management.

### 20.3.4. Type
MOBILE_LOCAL_SERVICE

### 20.3.5. Method
None

### 20.3.6. Url Pattern
None

### 20.3.7. Request Schema
Locally queued data changes (farmer, forms).

### 20.3.8. Response Schema
Sync status, server updates.

### 20.3.9. Authentication Required
True

### 20.3.10. Authorization Required
False

### 20.3.11. Data Formats

- JSON

### 20.3.12. Communication Protocol
HTTPS (to backend API)

### 20.3.13. Layer Ids

- mobile_data
- mobile_application_logic

### 20.3.14. Dependencies

- DFR_MOD_API_GATEWAY

### 20.3.15. Requirements

- **Requirement Id:** REQ-4-006  
- **Requirement Id:** REQ-4-007  

### 20.3.16. Version
1.0

### 20.3.17. Is Public
False

### 20.3.18. Architecture_Map

- mobile_data
- mobile_application_logic

### 20.3.19. Components_Map

- dfr-mobile-app-data-sync-016

### 20.3.20. Requirements_Map

- REQ-4-006
- REQ-4-007

## 20.4. Mobile Local Data Storage Service
Internal mobile app service for managing the local encrypted SQLite database (CRUD operations, schema management).

### 20.4.4. Type
MOBILE_LOCAL_SERVICE

### 20.4.5. Method
None

### 20.4.6. Url Pattern
None

### 20.4.7. Request Schema
Data entities (farmer, form definitions, submissions).

### 20.4.8. Response Schema
Operation status, retrieved data.

### 20.4.9. Authentication Required
False

### 20.4.10. Authorization Required
False

### 20.4.11. Data Formats

- SQLite records
- Application Models

### 20.4.12. Communication Protocol
Internal Method Calls

### 20.4.13. Layer Ids

- mobile_data

### 20.4.14. Dependencies


### 20.4.15. Requirements

- **Requirement Id:** REQ-4-003  
- **Requirement Id:** REQ-4-004  

### 20.4.16. Version
1.0

### 20.4.17. Is Public
False

### 20.4.18. Architecture_Map

- mobile_data

### 20.4.19. Components_Map

- dfr-mobile-app-local-data-store-017

### 20.4.20. Requirements_Map

- REQ-4-003
- REQ-4-004

## 20.5. Mobile GPS Capture Function
Functional endpoint for capturing GPS coordinates for plots/homesteads.

### 20.5.4. Type
MOBILE_FUNCTIONAL_ENDPOINT

### 20.5.5. Method
None

### 20.5.6. Url Pattern
None

### 20.5.7. Request Schema
User interaction to trigger GPS capture.

### 20.5.8. Response Schema
Captured GPS coordinates (lat, long).

### 20.5.9. Authentication Required
True

### 20.5.10. Authorization Required
False

### 20.5.11. Data Formats

- Device Location Object

### 20.5.12. Communication Protocol
Internal App Logic/Platform API Call

### 20.5.13. Layer Ids

- mobile_presentation
- mobile_cross_cutting_services

### 20.5.14. Dependencies


### 20.5.15. Requirements

- **Requirement Id:** REQ-4-009  

### 20.5.16. Version
1.0

### 20.5.17. Is Public
False

### 20.5.18. Architecture_Map

- mobile_presentation
- mobile_cross_cutting_services

### 20.5.19. Components_Map

- dfr-mobile-app-platform-services-018

### 20.5.20. Requirements_Map

- REQ-4-009

## 20.6. Mobile QR Code Scanning Function
Functional endpoint for scanning QR codes for farmer identification.

### 20.6.4. Type
MOBILE_FUNCTIONAL_ENDPOINT

### 20.6.5. Method
None

### 20.6.6. Url Pattern
None

### 20.6.7. Request Schema
User interaction to trigger QR scanner.

### 20.6.8. Response Schema
Decoded QR code data (e.g., farmer UID).

### 20.6.9. Authentication Required
True

### 20.6.10. Authorization Required
False

### 20.6.11. Data Formats

- String

### 20.6.12. Communication Protocol
Internal App Logic/Platform API Call

### 20.6.13. Layer Ids

- mobile_presentation
- mobile_cross_cutting_services

### 20.6.14. Dependencies


### 20.6.15. Requirements

- **Requirement Id:** REQ-4-008  

### 20.6.16. Version
1.0

### 20.6.17. Is Public
False

### 20.6.18. Architecture_Map

- mobile_presentation
- mobile_cross_cutting_services

### 20.6.19. Components_Map

- dfr-mobile-app-platform-services-018

### 20.6.20. Requirements_Map

- REQ-4-008



---

