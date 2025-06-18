# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . Consent Withdrawal Process
  A farmer requests to withdraw their consent for data processing. An administrator processes this request, updates the farmer's consent status in the DFR, and ensures data processing reflects this change as per legal mandates.

  #### .4. Purpose
  To comply with data privacy regulations regarding the right to withdraw consent.

  #### .5. Type
  ComplianceFlow

  #### .6. Participant Repository Ids
  
  - Farmer
  - dfr-module-admin-settings-005
  - dfr-infra-odoo-app-container-019
  - dfr-module-farmer-registry-002
  - dfr-module-security-audit-log-013
  
  #### .7. Key Interactions
  
  - Farmer submits a consent withdrawal request.
  - Administrator receives and logs the request, verifies farmer's identity.
  - Administrator accesses DFR Admin Portal, locates farmer's record.
  - Administrator updates farmer's consent status to 'Withdrawn' or equivalent.
  - System business rules ensure that data processing for this farmer is restricted/stopped according to the withdrawal (e.g., exclusion from certain reports, no further comms).
  - The consent withdrawal and its processing are logged in the audit trail.
  - Confirmation may be sent to the farmer.
  
  #### .8. Related Feature Ids
  
  - REQ-SADG-008
  - REQ-SADG-009
  - REQ-FHR-018
  
  #### .9. Domain
  Data Privacy & Compliance

  #### .10. Metadata
  
  - **Complexity:** Medium
  - **Priority:** High
  - **Frequency:** Rare/AsNeeded
  


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

