# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . Farmer Self-Registration via Portal and Admin Review
  A prospective farmer uses the public Farmer Self-Service Portal to submit their pre-registration details. The system creates a draft record, notifies administrators, who then review and approve/reject the registration.

  #### .4. Purpose
  To allow farmers to initiate their registration process online, reducing enumerator workload and improving accessibility.

  #### .5. Type
  UserJourney

  #### .6. Participant Repository Ids
  
  - dfr-farmer-portal-011
  - dfr-infra-reverse-proxy-021
  - dfr-infra-odoo-app-container-019
  - dfr-module-farmer-registry-002
  - dfr-module-notifications-engine-007
  - dfr-module-admin-settings-005
  - dfr-module-rbac-config-004
  - dfr-module-security-audit-log-013
  
  #### .7. Key Interactions
  
  - Farmer accesses portal and submits pre-registration form.
  - Portal module submits data to Farmer Registry module.
  - Farmer Registry module creates a draft farmer record, performs initial validation.
  - Notifications module alerts admin/supervisor of new submission.
  - Admin/Supervisor logs in, reviews submission via Admin Settings/Registry UI.
  - Admin/Supervisor approves/rejects, status updated in Farmer Registry.
  - Audit log records actions.
  
  #### .8. Related Feature Ids
  
  - REQ-FSSP-001
  - REQ-FSSP-003
  - REQ-FSSP-004
  - REQ-FSSP-005
  - REQ-FSSP-007
  - REQ-FHR-009
  - REQ-FHR-011
  - REQ-NS-001
  
  #### .9. Domain
  Farmer Registration

  #### .10. Metadata
  
  - **Complexity:** High
  - **Priority:** High
  - **Frequency:** Frequent
  


---

# 2. Sequence Diagram Details

- **Success:** True
- **Cache_Created:** True
- **Status:** refreshed
- **Cache_Id:** 90hcwvpdchcrbsw4mxozv4ns2g2li1nap4o2lzhm
- **Cache_Name:** cachedContents/90hcwvpdchcrbsw4mxozv4ns2g2li1nap4o2lzhm
- **Cache_Display_Name:** repositories
- **Cache_Status_Verified:** True
- **Model:** models/gemini-2.5-pro-preview-03-25
- **Workflow_Id:** I9v2neJ0O4zJsz8J
- **Execution_Id:** 8302
- **Project_Id:** 15
- **Record_Id:** 20
- **Cache_Type:** repositories


---

