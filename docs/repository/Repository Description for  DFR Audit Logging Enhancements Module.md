# Repository Specification

# 1. Name
DFR Audit Logging Enhancements Module


---

# 2. Description
Enhances Odoo's native auditing capabilities for DFR-specific needs. Captures comprehensive audit logs for user actions and system events, ensuring traceability and compliance. Provides an interface for authorized administrators to view audit logs.


---

# 3. Type
AuditingService


---

# 4. Namespace
odoo.addons.dfr_audit_log_enhancements


---

# 5. Output Path
dfr_addons/dfr_audit_log_enhancements


---

# 6. Framework
Odoo 18.0 Community


---

# 7. Language
Python, XML


---

# 8. Technology
Odoo ORM, Odoo Logging Framework, Odoo mail.thread


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- DFR_MOD_CORE_COMMON
- DFR_MOD_RBAC_CONFIG


---

# 11. Layer Ids

- dfr_security
- dfr_cross_cutting
- dfr_odoo_presentation


---

# 12. Requirements

- **Requirement Id:** REQ-SADG-005  
- **Requirement Id:** REQ-SADG-006  
- **Requirement Id:** REQ-FHR-010  


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
DFR_MOD_AUDIT_LOG


---

# 17. Architecture_Map

- dfr_security
- dfr_cross_cutting
- dfr_odoo_presentation


---

# 18. Components_Map

- dfr-module-security-audit-log-013


---

# 19. Requirements_Map

- REQ-SADG-005
- REQ-SADG-006
- REQ-FHR-010


---

# 20. Endpoints

## 20.1. Audit Log Viewer Admin Action
Odoo Admin Portal UI for authorized administrators to view and filter audit logs for system activities and data changes.

### 20.1.4. Type
ODOO_ADMIN_VIEW_ACTION

### 20.1.5. Method
None

### 20.1.6. Url Pattern
/web#model=dfr.audit.log&view_type=list (example)

### 20.1.7. Request Schema
User interaction with filter controls (date range, user, action type).

### 20.1.8. Response Schema
Rendered list of audit log entries.

### 20.1.9. Authentication Required
True

### 20.1.10. Authorization Required
True

### 20.1.11. Data Formats

- Odoo Views (XML/OWL)

### 20.1.12. Communication Protocol
HTTP/Odoo RPC

### 20.1.13. Layer Ids

- dfr_odoo_presentation

### 20.1.14. Dependencies


### 20.1.15. Requirements

- **Requirement Id:** REQ-SADG-007  
- **Requirement Id:** REQ-SYSADM-007  

### 20.1.16. Version
1.0

### 20.1.17. Is Public
False

### 20.1.18. Architecture_Map

- dfr_odoo_presentation

### 20.1.19. Components_Map

- dfr-module-security-audit-log-013

### 20.1.20. Requirements_Map

- REQ-SADG-007
- REQ-SYSADM-007

## 20.2. Audit Log Recording Service Interface
Internal Python service used by other DFR modules to record auditable events and data changes into the audit log system.

### 20.2.4. Type
ODOO_MODULE_SERVICE_INTERFACE

### 20.2.5. Method
None

### 20.2.6. Url Pattern
None

### 20.2.7. Request Schema
Audit event details (user, action, entity, old/new values).

### 20.2.8. Response Schema
Confirmation of log entry.

### 20.2.9. Authentication Required
False

### 20.2.10. Authorization Required
False

### 20.2.11. Data Formats

- Python Objects

### 20.2.12. Communication Protocol
Python Method Call

### 20.2.13. Layer Ids

- dfr_cross_cutting
- dfr_security

### 20.2.14. Dependencies


### 20.2.15. Requirements

- **Requirement Id:** REQ-SADG-005  
- **Requirement Id:** REQ-SADG-006  

### 20.2.16. Version
1.0

### 20.2.17. Is Public
False

### 20.2.18. Architecture_Map

- dfr_cross_cutting
- dfr_security

### 20.2.19. Components_Map

- dfr-module-security-audit-log-013

### 20.2.20. Requirements_Map

- REQ-SADG-005
- REQ-SADG-006



---

