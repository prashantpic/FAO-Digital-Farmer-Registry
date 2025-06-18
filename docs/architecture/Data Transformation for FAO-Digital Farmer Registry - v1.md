# Specification

# 1. Database Design

- **Entities:**
  
  ### .1. Farmer
  Core entity representing registered farmers

  #### .1.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
**Is Unique:** True  
  - **Name:** uid  
**Type:** VARCHAR  
**Is Required:** True  
**Is Unique:** True  
**Size:** 20  
  - **Name:** fullName  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** dateOfBirth  
**Type:** DATE  
**Is Required:** False  
  - **Name:** sex  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 10  
  - **Name:** roleInHousehold  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** educationLevel  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** contactPhone  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  - **Name:** contactEmail  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 100  
  - **Name:** nationalIdType  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** nationalIdNumber  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** consentStatus  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
**Default Value:** Pending  
  - **Name:** consentDate  
**Type:** TIMESTAMP  
**Is Required:** False  
  - **Name:** consentVersion  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 10  
  - **Name:** status  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 30  
**Default Value:** Pending Verification  
  - **Name:** createdAt  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  - **Name:** updatedAt  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  - **Name:** deletedAt  
**Type:** TIMESTAMP  
**Is Required:** False  
  
  #### .1.4. Primary Keys
  
  - id
  
  #### .1.5. Unique Constraints
  
  - **Name:** uq_farmer_uid  
**Columns:**
    
    - uid
    
  
  #### .1.6. Indexes
  
  - **Name:** idx_farmer_uid  
**Columns:**
    
    - uid
    
**Type:** BTree  
  - **Name:** idx_farmer_national_id_number  
**Columns:**
    
    - nationalIdNumber
    
**Type:** BTree  
  - **Name:** idx_farmer_contact_phone  
**Columns:**
    
    - contactPhone
    
**Type:** BTree  
  - **Name:** idx_farmer_status  
**Columns:**
    
    - status
    
**Type:** BTree  
  - **Name:** idx_farmer_fullname_dob  
**Columns:**
    
    - fullName
    - dateOfBirth
    
**Type:** BTree  
  - **Name:** idx_farmer_consent_status  
**Columns:**
    
    - consentStatus
    
**Type:** BTree  
  - **Name:** idx_farmer_created_at  
**Columns:**
    
    - createdAt
    
**Type:** BTree  
  
  ### .2. Household
  Represents a farmer household unit

  #### .2.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
**Is Unique:** True  
  - **Name:** uid  
**Type:** VARCHAR  
**Is Required:** True  
**Is Unique:** True  
**Size:** 20  
  - **Name:** createdAt  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  - **Name:** updatedAt  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  
  #### .2.4. Primary Keys
  
  - id
  
  #### .2.5. Unique Constraints
  
  - **Name:** uq_household_uid  
**Columns:**
    
    - uid
    
  
  #### .2.6. Indexes
  
  - **Name:** idx_household_uid  
**Columns:**
    
    - uid
    
**Type:** BTree  
  
  ### .3. HouseholdMember
  Members belonging to a household

  #### .3.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** householdId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** farmerId  
**Type:** UUID  
**Is Required:** False  
**Is Foreign Key:** True  
  - **Name:** relationshipToHead  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 50  
  - **Name:** roleInHousehold  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** educationLevel  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  
  #### .3.4. Primary Keys
  
  - id
  
  #### .3.5. Unique Constraints
  
  
  #### .3.6. Indexes
  
  
  ### .4. Farm
  Agricultural farm associated with farmer/household

  #### .4.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** farmerId  
**Type:** UUID  
**Is Required:** False  
**Is Foreign Key:** True  
  - **Name:** householdId  
**Type:** UUID  
**Is Required:** False  
**Is Foreign Key:** True  
  - **Name:** name  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 100  
  
  #### .4.4. Primary Keys
  
  - id
  
  #### .4.5. Unique Constraints
  
  
  #### .4.6. Indexes
  
  
  ### .5. Plot
  Individual land plots within a farm

  #### .5.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** farmId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** size  
**Type:** DECIMAL  
**Is Required:** True  
**Precision:** 10  
**Scale:** 2  
  - **Name:** landTenureType  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 50  
  - **Name:** primaryCrop  
**Type:** VARCHAR  
**Is Required:** False  
**Size:** 50  
  - **Name:** latitude  
**Type:** DECIMAL  
**Is Required:** True  
**Precision:** 9  
**Scale:** 6  
  - **Name:** longitude  
**Type:** DECIMAL  
**Is Required:** True  
**Precision:** 9  
**Scale:** 6  
  - **Name:** ownershipDetails  
**Type:** TEXT  
**Is Required:** False  
  
  #### .5.4. Primary Keys
  
  - id
  
  #### .5.5. Unique Constraints
  
  
  #### .5.6. Indexes
  
  - **Name:** idx_plot_location_spatial  
**Columns:**
    
    - latitude
    - longitude
    
**Type:** GiST  
  
  ### .6. AdministrativeArea
  Hierarchical geographical areas (region/district/village)

  #### .6.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** name  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** type  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  - **Name:** parentId  
**Type:** UUID  
**Is Required:** False  
**Is Foreign Key:** True  
  
  #### .6.4. Primary Keys
  
  - id
  
  #### .6.5. Unique Constraints
  
  
  #### .6.6. Indexes
  
  - **Name:** idx_admin_area_name_type  
**Columns:**
    
    - name
    - type
    
**Type:** BTree  
  - **Name:** idx_admin_area_parent_id  
**Columns:**
    
    - parentId
    
**Type:** BTree  
  
  ### .7. DynamicForm
  Template for customizable data collection forms

  #### .7.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** name  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** version  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 10  
  - **Name:** status  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
**Default Value:** Draft  
  - **Name:** isPortalAccessible  
**Type:** BOOLEAN  
**Is Required:** True  
**Default Value:** false  
  - **Name:** createdAt  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  
  #### .7.4. Primary Keys
  
  - id
  
  #### .7.5. Unique Constraints
  
  - **Name:** uq_dynamicform_name_version  
**Columns:**
    
    - name
    - version
    
  
  #### .7.6. Indexes
  
  - **Name:** idx_dynamicform_status  
**Columns:**
    
    - status
    
**Type:** BTree  
  
  ### .8. FormField
  Fields within a dynamic form

  #### .8.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** formId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** fieldType  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  - **Name:** label  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** isRequired  
**Type:** BOOLEAN  
**Is Required:** True  
**Default Value:** false  
  - **Name:** validationRules  
**Type:** JSON  
**Is Required:** False  
  - **Name:** conditionalLogic  
**Type:** JSON  
**Is Required:** False  
  - **Name:** order  
**Type:** INT  
**Is Required:** True  
  
  #### .8.4. Primary Keys
  
  - id
  
  #### .8.5. Unique Constraints
  
  
  #### .8.6. Indexes
  
  - **Name:** idx_formfield_form_order  
**Columns:**
    
    - formId
    - order
    
**Type:** BTree  
  
  ### .9. FormSubmission
  Instance of a submitted dynamic form

  #### .9.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** formId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** farmerId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** submissionDate  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  - **Name:** status  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
**Default Value:** Submitted  
  
  #### .9.4. Primary Keys
  
  - id
  
  #### .9.5. Unique Constraints
  
  
  #### .9.6. Indexes
  
  - **Name:** idx_formsubmission_farmer_form  
**Columns:**
    
    - farmerId
    - formId
    
**Type:** BTree  
  - **Name:** idx_formsubmission_submission_date  
**Columns:**
    
    - submissionDate
    
**Type:** BTree  
  - **Name:** idx_formsubmission_status  
**Columns:**
    
    - status
    
**Type:** BTree  
  
  ### .10. FormResponse
  Responses for individual form fields

  #### .10.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** submissionId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** fieldId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** value  
**Type:** TEXT  
**Is Required:** True  
  
  #### .10.4. Primary Keys
  
  - id
  
  #### .10.5. Unique Constraints
  
  
  #### .10.6. Indexes
  
  - **Name:** idx_formresponse_submission_field  
**Columns:**
    
    - submissionId
    - fieldId
    
**Type:** BTree  
  - **Name:** idx_formresponse_value_gin  
**Columns:**
    
    - value
    
**Type:** GIN  
  
  ### .11. User
  System users with access permissions

  #### .11.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** username  
**Type:** VARCHAR  
**Is Required:** True  
**Is Unique:** True  
**Size:** 50  
  - **Name:** passwordHash  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** role  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 30  
  - **Name:** assignedAreaId  
**Type:** UUID  
**Is Required:** False  
**Is Foreign Key:** True  
  - **Name:** lastLogin  
**Type:** TIMESTAMP  
**Is Required:** False  
  - **Name:** isActive  
**Type:** BOOLEAN  
**Is Required:** True  
**Default Value:** true  
  
  #### .11.4. Primary Keys
  
  - id
  
  #### .11.5. Unique Constraints
  
  - **Name:** uq_user_username  
**Columns:**
    
    - username
    
  
  #### .11.6. Indexes
  
  - **Name:** idx_user_role  
**Columns:**
    
    - role
    
**Type:** BTree  
  
  ### .12. Notification
  System-generated notifications

  #### .12.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** recipient  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** channel  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 10  
  - **Name:** content  
**Type:** TEXT  
**Is Required:** True  
  - **Name:** status  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
**Default Value:** Pending  
  - **Name:** sentAt  
**Type:** TIMESTAMP  
**Is Required:** False  
  - **Name:** triggerEvent  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 50  
  
  #### .12.4. Primary Keys
  
  - id
  
  #### .12.5. Unique Constraints
  
  
  #### .12.6. Indexes
  
  
  ### .13. AuditLog
  System activity and change history

  #### .13.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** entityName  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 50  
  - **Name:** entityId  
**Type:** UUID  
**Is Required:** True  
  - **Name:** action  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  - **Name:** userId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** oldValue  
**Type:** JSON  
**Is Required:** False  
  - **Name:** newValue  
**Type:** JSON  
**Is Required:** False  
  - **Name:** timestamp  
**Type:** TIMESTAMP  
**Is Required:** True  
**Default Value:** CURRENT_TIMESTAMP  
  
  #### .13.4. Primary Keys
  
  - id
  
  #### .13.5. Unique Constraints
  
  
  #### .13.6. Indexes
  
  - **Name:** idx_auditlog_entity_id_ts  
**Columns:**
    
    - entityName
    - entityId
    - timestamp
    
**Type:** BTree  
  - **Name:** idx_auditlog_user_ts  
**Columns:**
    
    - userId
    - timestamp
    
**Type:** BTree  
  
  ### .14. MobileDevice
  Enumerator mobile devices for offline sync

  #### .14.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** userId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** deviceId  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 100  
  - **Name:** lastSync  
**Type:** TIMESTAMP  
**Is Required:** False  
  - **Name:** appVersion  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  
  #### .14.4. Primary Keys
  
  - id
  
  #### .14.5. Unique Constraints
  
  
  #### .14.6. Indexes
  
  - **Name:** idx_mobiledevice_deviceid  
**Columns:**
    
    - deviceId
    
**Type:** BTree  
  
  ### .15. SyncSession
  Mobile-to-server synchronization records

  #### .15.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** deviceId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** startTime  
**Type:** TIMESTAMP  
**Is Required:** True  
  - **Name:** endTime  
**Type:** TIMESTAMP  
**Is Required:** False  
  - **Name:** recordsSynced  
**Type:** INT  
**Is Required:** True  
  - **Name:** conflictCount  
**Type:** INT  
**Is Required:** True  
**Default Value:** 0  
  - **Name:** status  
**Type:** VARCHAR  
**Is Required:** True  
**Size:** 20  
  
  #### .15.4. Primary Keys
  
  - id
  
  #### .15.5. Unique Constraints
  
  
  #### .15.6. Indexes
  
  - **Name:** idx_syncsession_status_starttime  
**Columns:**
    
    - status
    - startTime
    
**Type:** BTree  
  
  ### .16. Tag
  Categorization for dynamic forms

  #### .16.3. Attributes
  
  - **Name:** id  
**Type:** UUID  
**Is Required:** True  
**Is Primary Key:** True  
  - **Name:** name  
**Type:** VARCHAR  
**Is Required:** True  
**Is Unique:** True  
**Size:** 50  
  
  #### .16.4. Primary Keys
  
  - id
  
  #### .16.5. Unique Constraints
  
  - **Name:** uq_tag_name  
**Columns:**
    
    - name
    
  
  #### .16.6. Indexes
  
  
  ### .17. FormTag
  Relationship between forms and tags

  #### .17.3. Attributes
  
  - **Name:** formId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  - **Name:** tagId  
**Type:** UUID  
**Is Required:** True  
**Is Foreign Key:** True  
  
  #### .17.4. Primary Keys
  
  - formId
  - tagId
  
  #### .17.5. Unique Constraints
  
  
  #### .17.6. Indexes
  
  - **Name:** idx_formtag_tag_form  
**Columns:**
    
    - tagId
    - formId
    
**Type:** BTree  
  
  
- **Relations:**
  
  ### .1. FarmerHouseholdMember
  #### .1.3. Source Entity
  Farmer

  #### .1.4. Target Entity
  HouseholdMember

  #### .1.5. Type
  OneToOne

  #### .1.6. Source Multiplicity
  One

  #### .1.7. Target Multiplicity
  ZeroOrOne

  #### .1.8. Cascade Delete
  False

  #### .1.9. Is Identifying
  False

  #### .1.10. On Delete
  SetNull

  #### .1.11. On Update
  NoAction

  ### .2. HouseholdMembers
  #### .2.3. Source Entity
  Household

  #### .2.4. Target Entity
  HouseholdMember

  #### .2.5. Type
  OneToMany

  #### .2.6. Source Multiplicity
  One

  #### .2.7. Target Multiplicity
  Many

  #### .2.8. Cascade Delete
  True

  #### .2.9. Is Identifying
  True

  #### .2.10. On Delete
  Cascade

  #### .2.11. On Update
  NoAction

  ### .3. FarmerFarms
  #### .3.3. Source Entity
  Farmer

  #### .3.4. Target Entity
  Farm

  #### .3.5. Type
  OneToMany

  #### .3.6. Source Multiplicity
  One

  #### .3.7. Target Multiplicity
  Many

  #### .3.8. Cascade Delete
  False

  #### .3.9. Is Identifying
  False

  #### .3.10. On Delete
  SetNull

  #### .3.11. On Update
  NoAction

  ### .4. HouseholdFarms
  #### .4.3. Source Entity
  Household

  #### .4.4. Target Entity
  Farm

  #### .4.5. Type
  OneToMany

  #### .4.6. Source Multiplicity
  One

  #### .4.7. Target Multiplicity
  Many

  #### .4.8. Cascade Delete
  False

  #### .4.9. Is Identifying
  False

  #### .4.10. On Delete
  SetNull

  #### .4.11. On Update
  NoAction

  ### .5. FarmPlots
  #### .5.3. Source Entity
  Farm

  #### .5.4. Target Entity
  Plot

  #### .5.5. Type
  OneToMany

  #### .5.6. Source Multiplicity
  One

  #### .5.7. Target Multiplicity
  Many

  #### .5.8. Cascade Delete
  True

  #### .5.9. Is Identifying
  True

  #### .5.10. On Delete
  Cascade

  #### .5.11. On Update
  NoAction

  ### .6. AdminAreaHierarchy
  #### .6.3. Source Entity
  AdministrativeArea

  #### .6.4. Target Entity
  AdministrativeArea

  #### .6.5. Type
  OneToMany

  #### .6.6. Source Multiplicity
  One

  #### .6.7. Target Multiplicity
  Many

  #### .6.8. Cascade Delete
  False

  #### .6.9. Is Identifying
  False

  #### .6.10. On Delete
  Restrict

  #### .6.11. On Update
  NoAction

  ### .7. FormFields
  #### .7.3. Source Entity
  DynamicForm

  #### .7.4. Target Entity
  FormField

  #### .7.5. Type
  OneToMany

  #### .7.6. Source Multiplicity
  One

  #### .7.7. Target Multiplicity
  Many

  #### .7.8. Cascade Delete
  True

  #### .7.9. Is Identifying
  True

  #### .7.10. On Delete
  Cascade

  #### .7.11. On Update
  NoAction

  ### .8. FormSubmissions
  #### .8.3. Source Entity
  DynamicForm

  #### .8.4. Target Entity
  FormSubmission

  #### .8.5. Type
  OneToMany

  #### .8.6. Source Multiplicity
  One

  #### .8.7. Target Multiplicity
  Many

  #### .8.8. Cascade Delete
  False

  #### .8.9. Is Identifying
  False

  #### .8.10. On Delete
  Restrict

  #### .8.11. On Update
  NoAction

  ### .9. SubmissionResponses
  #### .9.3. Source Entity
  FormSubmission

  #### .9.4. Target Entity
  FormResponse

  #### .9.5. Type
  OneToMany

  #### .9.6. Source Multiplicity
  One

  #### .9.7. Target Multiplicity
  Many

  #### .9.8. Cascade Delete
  True

  #### .9.9. Is Identifying
  True

  #### .9.10. On Delete
  Cascade

  #### .9.11. On Update
  NoAction

  ### .10. ResponseField
  #### .10.3. Source Entity
  FormField

  #### .10.4. Target Entity
  FormResponse

  #### .10.5. Type
  OneToMany

  #### .10.6. Source Multiplicity
  One

  #### .10.7. Target Multiplicity
  Many

  #### .10.8. Cascade Delete
  False

  #### .10.9. Is Identifying
  False

  #### .10.10. On Delete
  Restrict

  #### .10.11. On Update
  NoAction

  ### .11. FarmerSubmissions
  #### .11.3. Source Entity
  Farmer

  #### .11.4. Target Entity
  FormSubmission

  #### .11.5. Type
  OneToMany

  #### .11.6. Source Multiplicity
  One

  #### .11.7. Target Multiplicity
  Many

  #### .11.8. Cascade Delete
  False

  #### .11.9. Is Identifying
  False

  #### .11.10. On Delete
  Restrict

  #### .11.11. On Update
  NoAction

  ### .12. AreaUsers
  #### .12.3. Source Entity
  AdministrativeArea

  #### .12.4. Target Entity
  User

  #### .12.5. Type
  OneToMany

  #### .12.6. Source Multiplicity
  One

  #### .12.7. Target Multiplicity
  Many

  #### .12.8. Cascade Delete
  False

  #### .12.9. Is Identifying
  False

  #### .12.10. On Delete
  SetNull

  #### .12.11. On Update
  NoAction

  ### .13. UserDevices
  #### .13.3. Source Entity
  User

  #### .13.4. Target Entity
  MobileDevice

  #### .13.5. Type
  OneToMany

  #### .13.6. Source Multiplicity
  One

  #### .13.7. Target Multiplicity
  Many

  #### .13.8. Cascade Delete
  True

  #### .13.9. Is Identifying
  True

  #### .13.10. On Delete
  Cascade

  #### .13.11. On Update
  NoAction

  ### .14. DeviceSessions
  #### .14.3. Source Entity
  MobileDevice

  #### .14.4. Target Entity
  SyncSession

  #### .14.5. Type
  OneToMany

  #### .14.6. Source Multiplicity
  One

  #### .14.7. Target Multiplicity
  Many

  #### .14.8. Cascade Delete
  True

  #### .14.9. Is Identifying
  True

  #### .14.10. On Delete
  Cascade

  #### .14.11. On Update
  NoAction

  ### .15. FormTags
  #### .15.3. Source Entity
  DynamicForm

  #### .15.4. Target Entity
  Tag

  #### .15.5. Type
  ManyToMany

  #### .15.6. Source Multiplicity
  Many

  #### .15.7. Target Multiplicity
  Many

  #### .15.8. Cascade Delete
  False

  #### .15.9. Is Identifying
  False

  #### .15.10. Join Table
  
  - **Name:** FormTag
  - **Columns:**
    
    - **Name:** formId  
**Type:** UUID  
**References:** DynamicForm.id  
    - **Name:** tagId  
**Type:** UUID  
**References:** Tag.id  
    
  
  #### .15.11. On Delete
  Cascade

  #### .15.12. On Update
  NoAction

  ### .16. UserAuditLogs
  #### .16.3. Source Entity
  User

  #### .16.4. Target Entity
  AuditLog

  #### .16.5. Type
  OneToMany

  #### .16.6. Source Multiplicity
  One

  #### .16.7. Target Multiplicity
  Many

  #### .16.8. Cascade Delete
  False

  #### .16.9. Is Identifying
  False

  #### .16.10. On Delete
  Restrict

  #### .16.11. On Update
  NoAction

  ### .17. farmer_sex_relationship
  #### .17.3. Source Entity
  Farmer

  #### .17.4. Target Entity
  SexLookup

  #### .17.5. Type
  OneToMany

  #### .17.6. Source Multiplicity
  *

  #### .17.7. Target Multiplicity
  1

  #### .17.8. Cascade Delete
  False

  #### .17.9. Is Identifying
  False

  #### .17.10. On Delete
  Restrict

  #### .17.11. On Update
  Cascade

  ### .18. farmer_status_relationship
  #### .18.3. Source Entity
  Farmer

  #### .18.4. Target Entity
  FarmerStatusLookup

  #### .18.5. Type
  OneToMany

  #### .18.6. Source Multiplicity
  *

  #### .18.7. Target Multiplicity
  1

  #### .18.8. Cascade Delete
  False

  #### .18.9. Is Identifying
  False

  #### .18.10. On Delete
  Restrict

  #### .18.11. On Update
  Cascade

  ### .19. plot_land_tenure_type_relationship
  #### .19.3. Source Entity
  Plot

  #### .19.4. Target Entity
  LandTenureTypeLookup

  #### .19.5. Type
  OneToMany

  #### .19.6. Source Multiplicity
  *

  #### .19.7. Target Multiplicity
  1

  #### .19.8. Cascade Delete
  False

  #### .19.9. Is Identifying
  False

  #### .19.10. On Delete
  Restrict

  #### .19.11. On Update
  Cascade

  ### .20. dynamic_form_status_relationship
  #### .20.3. Source Entity
  DynamicForm

  #### .20.4. Target Entity
  FormStatusLookup

  #### .20.5. Type
  OneToMany

  #### .20.6. Source Multiplicity
  *

  #### .20.7. Target Multiplicity
  1

  #### .20.8. Cascade Delete
  False

  #### .20.9. Is Identifying
  False

  #### .20.10. On Delete
  Restrict

  #### .20.11. On Update
  Cascade

  ### .21. user_role_relationship
  #### .21.3. Source Entity
  User

  #### .21.4. Target Entity
  RoleLookup

  #### .21.5. Type
  OneToMany

  #### .21.6. Source Multiplicity
  *

  #### .21.7. Target Multiplicity
  1

  #### .21.8. Cascade Delete
  False

  #### .21.9. Is Identifying
  False

  #### .21.10. On Delete
  Restrict

  #### .21.11. On Update
  Cascade

  


---

# 2. Architecture Design

- **Style:** ModularMonolith
- **Patterns:**
  
  ### .1. Odoo Module System
  The system is built as a set of Odoo addons (modules). Odoo's framework inherently supports a modular architecture where functionalities are encapsulated in independent but interoperable modules. This aligns with the 'Modular Monolith' style.

  #### .1.3. Benefits
  
  - Encapsulation of features within distinct modules (e.g., farmer registry, dynamic forms).
  - Reusability of modules across different parts of the DFR system.
  - Easier maintenance and updates of specific functionalities.
  - Leverages Odoo's existing module management and extension capabilities.
  
  #### .1.4. Applicability
  
  - **Scenarios:**
    
    - Developing extensions for the Odoo platform.
    - Systems requiring clear separation of functional concerns within a unified codebase.
    
  
  ### .2. Model-View-Controller (MVC) / Model-View-Template (MVT)
  Odoo's web framework (including Web Client and Website module) follows an MVC/MVT-like pattern. Models define data and business logic, Views (XML, QWeb, OWL) define the presentation, and Controllers handle requests and orchestrate interactions.

  #### .2.3. Benefits
  
  - Separation of concerns between data, presentation, and control logic.
  - Improved maintainability and testability of UI components.
  - Standardized way of building user interfaces within Odoo.
  
  #### .2.4. Applicability
  
  - **Scenarios:**
    
    - Developing web interfaces using the Odoo framework (Admin Portal, Farmer Self-Service Portal).
    
  
  ### .3. Offline-First Synchronization
  The mobile enumerator application operates primarily offline, storing data locally and synchronizing with the Odoo backend when connectivity is available. This involves bi-directional sync and conflict resolution.

  #### .3.3. Benefits
  
  - Ensures enumerator productivity in areas with poor or no internet connectivity.
  - Reduces data loss by persisting data locally.
  - Improves mobile app responsiveness by operating on local data.
  
  #### .3.4. Applicability
  
  - **Scenarios:**
    
    - Mobile applications used for field data collection in environments with unreliable network access.
    
  
  ### .4. RESTful API
  A secure RESTful API layer is developed as a custom Odoo module to facilitate communication between the Odoo backend and the mobile application, as well as external systems.

  #### .4.3. Benefits
  
  - Standardized, stateless communication protocol.
  - Platform-agnostic integration for mobile and external systems.
  - Leverages HTTP methods for CRUD operations.
  
  #### .4.4. Applicability
  
  - **Scenarios:**
    
    - Exposing backend functionalities to client applications (mobile, web) or third-party services.
    - Enabling system integrations.
    
  
  ### .5. Role-Based Access Control (RBAC)
  Access to system functionalities and data is controlled based on user roles defined within Odoo's security framework (groups, access rights, record rules).

  #### .5.3. Benefits
  
  - Enforces principle of least privilege.
  - Simplifies permission management.
  - Enhances security by restricting access based on responsibilities.
  
  #### .5.4. Applicability
  
  - **Scenarios:**
    
    - Systems with multiple user types requiring different levels of access to data and features.
    
  
  ### .6. Dynamic Form Engine
  A dedicated Odoo module allows administrators to design custom data collection forms dynamically without coding, including various field types, validation, and conditional logic.

  #### .6.3. Benefits
  
  - Flexibility to adapt data collection needs without new development cycles.
  - Empowers non-technical users to create and manage forms.
  - Supports diverse data collection scenarios.
  
  #### .6.4. Applicability
  
  - **Scenarios:**
    
    - Systems requiring adaptable data collection tools for surveys, applications, or supplementary data gathering.
    
  
  
- **Layers:**
  
  ### .1. DFR Odoo Presentation Layer
  Handles user interaction for the Admin Portal and Farmer Self-Service Portal within the Odoo framework. It renders UIs based on DFR-specific module definitions.

  #### .1.4. Technologystack
  Odoo Web Client (JavaScript, XML, OWL), Odoo Website Module (QWeb, HTML, CSS, JavaScript)

  #### .1.5. Language
  XML, JavaScript, Python (for Controllers)

  #### .1.6. Type
  Presentation

  #### .1.7. Responsibilities
  
  - Rendering user interfaces for DFR Admin Portal and Farmer Self-Service Portal.
  - Handling user input and actions from web interfaces.
  - Displaying data fetched from application services and models.
  - Implementing client-side validation and interactivity.
  
  #### .1.8. Components
  
  - DFR Admin Portal Views (XML, OWL, JS for Odoo Backend)
  - Farmer Self-Service Portal Pages & Templates (QWeb, JS for Odoo Website)
  - Odoo Controllers (Python) for serving web pages and handling form submissions from portals.
  
  #### .1.9. Dependencies
  
  - **Layer Id:** dfr_odoo_application_services  
**Type:** Required  
  
  ### .2. DFR Odoo Application Services Layer
  Encapsulates the core business logic, workflows, and use cases for the DFR platform. Implemented as services within DFR-specific Odoo modules.

  #### .2.4. Technologystack
  Odoo Framework, Python

  #### .2.5. Language
  Python

  #### .2.6. Type
  ApplicationServices

  #### .2.7. Responsibilities
  
  - Orchestrating farmer and household registration processes (REQ-FHR-*).
  - Managing dynamic form creation, versioning, and submission processing (REQ-3-*).
  - Implementing de-duplication logic (REQ-FHR-012 to REQ-FHR-015).
  - Executing notification workflows (REQ-NS-*).
  - Coordinating data import/export operations (REQ-DM-*).
  - Providing services for analytics and reporting data aggregation (REQ-7-*).
  
  #### .2.8. Components
  
  - dfr_farmer_registry module services
  - dfr_dynamic_forms module services
  - dfr_notifications module services
  - dfr_data_management module services
  - Odoo Automated Actions and Server Actions for workflows.
  
  #### .2.9. Dependencies
  
  - **Layer Id:** dfr_odoo_domain_models  
**Type:** Required  
  - **Layer Id:** dfr_integration  
**Type:** Optional  
  - **Layer Id:** dfr_security  
**Type:** Required  
  
  ### .3. DFR Odoo Domain Models Layer
  Defines the DFR data structures, entities (Farmer, Household, Plot, DynamicForm, etc.), their relationships, attributes, model-level validation, and core business rules directly associated with these entities. Leverages Odoo's ORM.

  #### .3.4. Technologystack
  Odoo ORM, Python

  #### .3.5. Language
  Python

  #### .3.6. Type
  BusinessLogic

  #### .3.7. Responsibilities
  
  - Defining DFR-specific data models (Farmer, Household, Plot, FormSubmission, etc.) (REQ-FHR-016).
  - Enforcing data integrity through model constraints and validation rules.
  - Implementing business logic tied to specific entities (e.g., UID generation REQ-FHR-002, status transitions REQ-FHR-011).
  - Managing relationships between entities using Odoo ORM fields.
  
  #### .3.8. Components
  
  - Python classes inheriting `odoo.models.Model` for all DFR entities.
  - Field definitions, `@api.constrains`, `@api.onchange` methods.
  
  #### .3.9. Dependencies
  
  - **Layer Id:** dfr_odoo_data_access  
**Type:** Required  
  
  ### .4. DFR Odoo Data Access Layer
  Manages persistence and retrieval of DFR data using Odoo's Object-Relational Mapper (ORM) interacting with the PostgreSQL database.

  #### .4.4. Technologystack
  Odoo ORM, PostgreSQL

  #### .4.5. Language
  Python (ORM interactions), SQL (underlying)

  #### .4.6. Type
  DataAccess

  #### .4.7. Responsibilities
  
  - Executing CRUD (Create, Read, Update, Delete) operations on DFR entities via Odoo ORM.
  - Translating Odoo domain queries into SQL queries for PostgreSQL.
  - Managing database transactions and connections (handled by Odoo framework).
  - Ensuring data persistence in PostgreSQL.
  
  #### .4.8. Components
  
  - Odoo ORM API (e.g., `self.env['model'].create()`, `.search()`, `.write()`, `.unlink()`).
  - PostgreSQL Database Management System.
  
  ### .5. DFR API Gateway Layer (Odoo Module)
  Provides secure RESTful API endpoints for the mobile enumerator application and external system integrations. Built as a custom Odoo module.

  #### .5.4. Technologystack
  Odoo Controllers (HTTP routes), Python, JSON, OpenAPI v3.x, OAuth2/JWT

  #### .5.5. Language
  Python

  #### .5.6. Type
  APIGateway

  #### .5.7. Responsibilities
  
  - Exposing secure endpoints for mobile app data synchronization (farmer data, form definitions, submissions) (REQ-PCA-007, REQ-API-005).
  - Providing endpoints for farmer lookup and data retrieval for authorized external systems (REQ-API-004).
  - Handling API request/response serialization (JSON).
  - Enforcing API authentication (OAuth2/JWT) and authorization based on DFR roles (REQ-SADG-002, REQ-5-012).
  
  #### .5.8. Components
  
  - Odoo Controllers with `@http.route` decorators defining API endpoints.
  - Authentication and authorization handlers for API requests.
  - Data serialization/deserialization logic.
  
  #### .5.9. Interfaces
  
  - **Name:** Mobile Sync API  
**Type:** REST/JSON  
**Operations:**
    
    - SyncFarmerData
    - SyncFormDefinitions
    - SubmitFormData
    
**Visibility:** Public  
  - **Name:** External System API  
**Type:** REST/JSON  
**Operations:**
    
    - LookupFarmer
    - RetrieveFarmerData
    
**Visibility:** Public  
  
  #### .5.10. Dependencies
  
  - **Layer Id:** dfr_odoo_application_services  
**Type:** Required  
  - **Layer Id:** dfr_security  
**Type:** Required  
  
  ### .6. DFR Integration Layer
  Manages communication and data exchange with third-party external systems.

  #### .6.4. Technologystack
  Python, Requests library, specific SDKs for external services (e.g., SMS gateways, National ID APIs).

  #### .6.5. Language
  Python

  #### .6.6. Type
  Integration

  #### .6.7. Responsibilities
  
  - Integrating with National ID validation systems (REQ-FHR-006, REQ-API-007).
  - Connecting to SMS and email gateway services for notifications (REQ-NS-003, REQ-API-008).
  - Interfacing with weather and advisory service APIs (REQ-API-007).
  - Handling data transformation and protocol adaptation for external services.
  
  #### .6.8. Components
  
  - Connectors/Adapters for SMS gateways (e.g., Twilio, Vonage).
  - Connectors for National ID validation APIs.
  - Client modules for other third-party services.
  
  #### .6.9. Dependencies
  
  - **Layer Id:** dfr_odoo_application_services  
**Type:** Required  
  
  ### .7. DFR Security Layer
  Implements and enforces security policies across the DFR platform, leveraging Odoo's security framework and custom security measures.

  #### .7.4. Technologystack
  Odoo Security Framework (`ir.model.access.csv`, `ir.rule`, `res.groups`), Python, OAuth2/JWT libraries, HTTPS/TLS.

  #### .7.5. Language
  Python, XML (for Odoo security definitions)

  #### .7.6. Type
  Security

  #### .7.7. Responsibilities
  
  - Implementing Role-Based Access Control (RBAC) for all data entities and functionalities (REQ-5-*, REQ-SADG-001).
  - Managing user authentication and session security for web portals.
  - Enforcing API security (OAuth2/JWT authentication and authorization) (REQ-SADG-002).
  - Configuring and recommending MFA for administrative users (REQ-5-008).
  - Ensuring data transmission encryption (HTTPS/TLS 1.2+) (REQ-PCA-014).
  - Managing secure storage of credentials and API keys (REQ-SADG-012).
  
  #### .7.8. Components
  
  - Odoo security group definitions (`res.groups`).
  - Odoo access control lists (`ir.model.access.csv`).
  - Odoo record rules (`ir.rule`) for data scoping.
  - Custom authentication providers for OAuth2/JWT if needed.
  - Configuration of password policies.
  
  ### .8. DFR Infrastructure Layer
  Underlying platform components, hosting environment, and operational tools for the DFR system.

  #### .8.4. Technologystack
  Docker, PostgreSQL, Nginx (reverse proxy), Linux OS, CI/CD tools (Jenkins, GitLab CI, GitHub Actions), Backup utilities (`pg_dump`), Monitoring tools.

  #### .8.5. Language
  Shell scripts, YAML (for Docker/CI/CD configs)

  #### .8.6. Type
  Infrastructure

  #### .8.7. Responsibilities
  
  - Providing containerized deployment environment for Odoo and PostgreSQL (REQ-PCA-015, REQ-DIO-006).
  - Managing database backups and recovery procedures (REQ-DIO-007).
  - Ensuring HTTPS termination via reverse proxy (REQ-DIO-005).
  - Automating build, test, and deployment via CI/CD pipelines (REQ-DIO-011).
  - Monitoring system health and performance (REQ-DIO-009).
  - Supporting diverse hosting environments (on-premise, cloud) (REQ-PCA-012).
  
  #### .8.8. Components
  
  - Dockerfiles and Docker Compose files.
  - Nginx configuration.
  - PostgreSQL server instance.
  - CI/CD pipeline scripts.
  - Backup and restore scripts.
  - Monitoring agent configurations.
  
  ### .9. DFR Cross-Cutting Concerns
  Addresses shared functionalities like logging, configuration, internationalization, and error handling across the DFR Odoo modules.

  #### .9.4. Technologystack
  Odoo Framework (logging, i18n, config), Python.

  #### .9.5. Language
  Python, XML (for Odoo config/views)

  #### .9.6. Type
  CrossCutting

  #### .9.7. Responsibilities
  
  - Providing consistent logging throughout the DFR modules (REQ-SADG-005).
  - Managing system configuration parameters (e.g., via `ir.config_parameter`) (REQ-SYSADM-*).
  - Supporting multilingual capabilities through Odoo's i18n (`.po` files) (REQ-LMS-*).
  - Standardizing error handling and reporting.
  - Maintaining audit trails (leveraging Odoo's `mail.thread` and custom logging) (REQ-FHR-010).
  
  #### .9.8. Components
  
  - Odoo logging service.
  - Odoo `ir.config_parameter` model for settings.
  - Odoo translation mechanisms.
  - Custom utility modules for shared functions.
  
  ### .10. Mobile Presentation (UI) Layer
  User interface for the Android enumerator mobile application.

  #### .10.4. Technologystack
  Native Android (Kotlin/Java with XML layouts, Jetpack Compose) or Cross-platform (Flutter with Dart and Widgets).

  #### .10.5. Language
  Kotlin/Java or Dart

  #### .10.6. Type
  Presentation

  #### .10.7. Responsibilities
  
  - Rendering screens for farmer registration, dynamic forms, search, data lists (REQ-4-002).
  - Capturing user input via forms and device sensors (GPS, camera for QR).
  - Displaying data from local storage and providing intuitive navigation.
  - Adhering to Android Material Design guidelines or platform-specific UX best practices.
  
  #### .10.8. Components
  
  - Activities/Fragments or Flutter Widgets for each screen.
  - UI layouts (XML or Dart code).
  - Navigation components (Jetpack Navigation or Flutter Navigator).
  - Custom UI elements for form rendering.
  
  #### .10.9. Dependencies
  
  - **Layer Id:** mobile_application_logic  
**Type:** Required  
  
  ### .11. Mobile Application & Business Logic Layer
  Handles application-specific logic, workflows, state management, and business rules on the mobile device.

  #### .11.4. Technologystack
  Native Android (Kotlin/Java) or Cross-platform (Flutter with Dart). Architectural patterns like MVVM, MVI, or BLoC/Provider.

  #### .11.5. Language
  Kotlin/Java or Dart

  #### .11.6. Type
  BusinessLogic

  #### .11.7. Responsibilities
  
  - Implementing client-side validation for form inputs (REQ-3-002 on mobile).
  - Managing UI state and data flow between UI and data layers.
  - Orchestrating offline data capture and modification workflows (REQ-4-003).
  - Coordinating data synchronization processes with the backend.
  - Handling logic for local de-duplication checks (optional, REQ-4-016).
  
  #### .11.8. Components
  
  - ViewModels (Android Jetpack) or BLoCs/ChangeNotifiers (Flutter).
  - Use Cases/Interactors encapsulating specific business operations.
  - Validation rule implementations.
  - State management solutions.
  
  #### .11.9. Dependencies
  
  - **Layer Id:** mobile_data  
**Type:** Required  
  - **Layer Id:** mobile_cross_cutting_services  
**Type:** Optional  
  
  ### .12. Mobile Data Layer
  Manages local data storage (SQLite encrypted), data access objects, and the synchronization mechanism with the Odoo backend.

  #### .12.4. Technologystack
  SQLite with SQLCipher (AES-256), Native Android (Room Persistence Library, Content Providers) or Cross-platform (sqflite with SQLCipher, Moor/Drift). REST client libraries (Retrofit, Dio).

  #### .12.5. Language
  Kotlin/Java or Dart

  #### .12.6. Type
  DataAccess

  #### .12.7. Responsibilities
  
  - Storing and retrieving farmer data, form definitions, and submissions locally (REQ-4-003).
  - Encrypting all sensitive data stored locally (REQ-4-004).
  - Implementing bi-directional synchronization with the Odoo backend API (REQ-4-006).
  - Handling conflict resolution during synchronization (REQ-4-007).
  - Providing an abstraction over local data sources (Repository pattern).
  
  #### .12.8. Components
  
  - SQLite database schema and DAOs (Data Access Objects).
  - Repository classes for abstracting data operations.
  - Synchronization engine/service.
  - API client for communicating with DFR Odoo backend.
  - Encryption/decryption utilities for local data.
  
  ### .13. Mobile Cross-Cutting Services Layer
  Provides common utilities and services for the mobile application, such as location services, QR scanning, logging, and secure key management.

  #### .13.4. Technologystack
  Native Android APIs (LocationManager, CameraX/ZXing) or Flutter Plugins (geolocator, qr_code_scanner, logger, flutter_secure_storage).

  #### .13.5. Language
  Kotlin/Java or Dart

  #### .13.6. Type
  CrossCutting

  #### .13.7. Responsibilities
  
  - Capturing GPS coordinates for plots and homesteads (REQ-4-009).
  - Scanning QR codes for farmer identification (REQ-4-008).
  - Managing local application logs for troubleshooting (REQ-4-011).
  - Securely managing encryption keys using Android Keystore or equivalent (REQ-4-004).
  - Handling app updates and version compatibility checks (REQ-4-013).
  
  #### .13.8. Components
  
  - GPS Location Service wrapper.
  - QR Code Scanner utility.
  - Logging utility.
  - Secure Storage wrapper (for encryption keys).
  - App Update checker service.
  
  
- **Quality Attributes:**
  
  ### .1. Scalability
  System's ability to handle increasing data volumes and user load over time.

  #### .1.3. Tactics
  
  - Configurable Odoo worker processes.
  - Support for horizontal scaling of Odoo application servers (load balancing).
  - PostgreSQL optimization techniques (indexing, query optimization, connection pooling).
  - Efficient data structures and algorithms in custom modules.
  
  #### .1.4. Requirements
  
  - REQ-PCA-004
  - REQ-DIO-013
  
  ### .2. Security
  Protection of data and system resources against unauthorized access and threats.

  #### .2.3. Tactics
  
  - HTTPS/TLS 1.2+ for all client-server communication.
  - OWASP Top 10 and MASVS adherence.
  - Role-Based Access Control (RBAC) using Odoo security.
  - OAuth2/JWT for API authentication.
  - AES-256 encryption for mobile local data (SQLCipher).
  - Secure credential management and regular patching.
  - Maintaining a Software Bill of Materials (SBOM).
  
  #### .2.4. Requirements
  
  - REQ-PCA-014
  - REQ-SADG-*
  - REQ-FHR-008
  - REQ-5-*
  
  ### .3. Maintainability
  Ease with which the system can be modified, corrected, and enhanced.

  #### .3.3. Tactics
  
  - Modular design using Odoo addons.
  - Adherence to coding standards (PEP 8 for Python, Odoo guidelines).
  - Comprehensive inline and module-level documentation.
  - Separation of configuration from code.
  - Use of version control (Git) and semantic versioning.
  
  #### .3.4. Requirements
  
  - REQ-PCA-016
  - REQ-CM-*
  
  ### .4. Performance
  System's responsiveness and efficiency under load.

  #### .4.3. Tactics
  
  - Optimized database queries and indexing.
  - Efficient data synchronization algorithms for mobile.
  - Caching strategies where appropriate (e.g., for frequently accessed configurations or static data).
  - Asynchronous processing for long-running tasks.
  - Load testing and performance profiling.
  
  #### .4.4. Requirements
  
  - REQ-4-014
  - REQ-7-008
  - REQ-API-009
  - REQ-FSSP-011
  
  ### .5. Reliability & Availability
  System's ability to operate without failure and be accessible when needed.

  #### .5.3. Tactics
  
  - Automated daily backups of PostgreSQL databases and critical files.
  - Documented data restoration procedures and DR plan (RTO/RPO targets).
  - Resilient network communication for mobile sync (resumable, idempotent).
  - Use of Docker for consistent deployments.
  - System monitoring and alerting.
  
  #### .5.4. Requirements
  
  - REQ-SADG-011
  - REQ-DIO-007
  - REQ-DIO-010
  - REQ-4-006
  
  ### .6. Offline Capability
  Mobile application's ability to function without an active internet connection.

  #### .6.3. Tactics
  
  - Offline-first architecture for the mobile app.
  - Local SQLite database for storing data offline.
  - Bi-directional synchronization mechanism with conflict resolution.
  
  #### .6.4. Requirements
  
  - REQ-PCA-006
  - REQ-4-003
  - REQ-4-006
  - REQ-4-007
  
  ### .7. Interoperability & Extensibility
  System's ability to interact with other systems and be extended with new functionalities.

  #### .7.3. Tactics
  
  - Secure RESTful API layer (OpenAPI v3.x) for integrations.
  - Modular Odoo addon architecture allowing new modules for extensions.
  - Configurable integration points for third-party services.
  - Clear separation between core platform and country-specific modules/configurations.
  
  #### .7.4. Requirements
  
  - REQ-PCA-003
  - REQ-PCA-007
  - REQ-API-*
  
  ### .8. Usability & Accessibility
  Ease of use for end-users and accessibility for people with disabilities.

  #### .8.3. Tactics
  
  - Intuitive UI/UX design for web and mobile interfaces.
  - Mobile-responsive design for portals.
  - Adherence to WCAG 2.1 Level AA for Farmer Self-Service Portal.
  - Multilingual support.
  - Clear icons, simple language, and logical workflows for enumerators.
  
  #### .8.4. Requirements
  
  - REQ-4-002
  - REQ-FSSP-001
  - REQ-FSSP-013
  - REQ-LMS-*
  
  


---

# 3. Event Driven Architecture Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-17
  - **Architecture Type:** Modular Monolith (Odoo-centric)
  - **Technology Stack:**
    
    - Odoo 18.0 Community
    - Python
    - PostgreSQL
    - REST APIs (Odoo Controllers)
    - Docker
    - Android (Native Kotlin/Java or Flutter/Dart)
    
  - **Bounded Contexts:**
    
    - FarmerRegistry
    - DynamicForms
    - MobileSync
    - Notifications
    - UserManagement
    - SystemAdministration
    - Reporting
    - DataManagement
    
  
- **Project Specific Events:**
  
  - **Event Id:** EVT-FR-001  
**Event Name:** FarmerRegisteredEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered upon successful creation and initial validation of a new farmer record in the DFR system.  
**Trigger Condition:** A new farmer record is successfully created and passes initial validation (e.g., status moves from 'draft' to 'pending verification' or 'active'). REQ-FHR-001, REQ-FHR-011.  
**Source Context:** FarmerRegistry (DFR Odoo Application Services)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    
**Payload:**
    
    - **Schema:**
      
      - **Farmer_Id:** UUID
      - **Farmer_Uid:** string
      - **Full_Name:** string
      - **Contact_Phone:** string
      - **Contact_Email:** string (optional)
      - **Registration_Timestamp:** ISO8601_datetime
      - **Status:** string
      
    - **Required Fields:**
      
      - farmer_id
      - farmer_uid
      - full_name
      - registration_timestamp
      - status
      
    - **Optional Fields:**
      
      - contact_phone
      - contact_email
      
    
**Frequency:** medium  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_registry_farmer
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** farmer.registered
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_notification_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** handleFarmerRegisteredNotification  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateRegistrationKPIs  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FHR-001
    - REQ-NS-001
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Mail Queue Retry (for notifications)
    - **Dead Letter Queue:** Odoo Log (for workflow failures)
    - **Timeout Ms:** 30000
    
  - **Event Id:** EVT-FR-002  
**Event Name:** FarmerSelfRegistrationSubmittedEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered when a farmer submits a pre-registration form via the Farmer Self-Service Portal.  
**Trigger Condition:** Successful submission of the portal pre-registration form (REQ-FSSP-004).  
**Source Context:** FarmerSelfServicePortal (DFR Odoo Presentation Layer)  
**Target Contexts:**
    
    - FarmerRegistry
    - Notifications
    - UserManagement
    
**Payload:**
    
    - **Schema:**
      
      - **Submission_Id:** UUID
      - **Full_Name:** string
      - **Village:** string
      - **Primary_Crop_Type:** string
      - **Contact_Phone:** string
      - **National_Id_Type:** string (optional)
      - **National_Id_Number:** string (optional)
      - **Submission_Timestamp:** ISO8601_datetime
      
    - **Required Fields:**
      
      - submission_id
      - full_name
      - contact_phone
      - submission_timestamp
      
    - **Optional Fields:**
      
      - village
      - primary_crop_type
      - national_id_type
      - national_id_number
      
    
**Frequency:** medium  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_self_registration
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** farmer.self_registration.submitted
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_self_reg_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Farmer Registry Service  
**Handler:** createDraftFarmerFromSelfReg  
**Processing Type:** sync  
    - **Service:** DFR Notification Service  
**Handler:** notifyAdminOfSelfReg  
**Processing Type:** async  
    - **Service:** DFR User Management Service  
**Handler:** assignSelfRegForReview  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FSSP-004
    - REQ-NS-001
    - REQ-FSSP-005
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Server Action Retry (if applicable for routing)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-FR-003  
**Event Name:** FarmerRecordUpdatedEvent  
**Event Type:** domain  
**Category:** FarmerManagement  
**Description:** Triggered when key fields of a farmer's record are updated, including status changes.  
**Trigger Condition:** Write operation on `dfr_farmer_registry_farmer` model affecting audited fields (REQ-FHR-010) or status (REQ-FHR-011).  
**Source Context:** FarmerRegistry (DFR Odoo Application Services)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    - AuditLog
    
**Payload:**
    
    - **Schema:**
      
      - **Farmer_Id:** UUID
      - **Updated_Fields:**
        
        - **Field_Name:**
          
          - **Old_Value:** any
          - **New_Value:** any
          
        
      - **Previous_Status:** string (optional)
      - **New_Status:** string (optional)
      - **Updated_By_User_Id:** UUID
      - **Update_Timestamp:** ISO8601_datetime
      
    - **Required Fields:**
      
      - farmer_id
      - updated_fields
      - updated_by_user_id
      - update_timestamp
      
    - **Optional Fields:**
      
      - previous_status
      - new_status
      
    
**Frequency:** high  
**Business Criticality:** normal  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_farmer_registry_farmer
    - **Operation:** update
    
**Routing:**
    
    - **Routing Key:** farmer.record.updated
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_audit_notification_queue
    
**Consumers:**
    
    - **Service:** DFR AuditLog Service  
**Handler:** logFarmerUpdate  
**Processing Type:** sync  
    - **Service:** DFR Notification Service  
**Handler:** handleFarmerUpdateNotifications  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateFarmerKPIs  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-FHR-010
    - REQ-FHR-011
    - REQ-SADG-005
    
**Error Handling:**
    
    - **Retry Strategy:** None (handled by Odoo transaction)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 10000
    
  - **Event Id:** EVT-DF-001  
**Event Name:** DynamicFormSubmittedEvent  
**Event Type:** domain  
**Category:** DynamicFormData  
**Description:** Triggered when an enumerator or farmer submits a dynamic form.  
**Trigger Condition:** Successful submission of a dynamic form via mobile app or portal (REQ-3-008).  
**Source Context:** DynamicFormEngine (DFR Odoo Application Services / Mobile Data Layer)  
**Target Contexts:**
    
    - Notifications
    - Reporting
    - ProgramManagement (hypothetical future)
    
**Payload:**
    
    - **Schema:**
      
      - **Submission_Id:** UUID
      - **Form_Id:** UUID
      - **Form_Version:** string
      - **Farmer_Id:** UUID
      - **Submitted_By_User_Id:** UUID
      - **Submission_Timestamp:** ISO8601_datetime
      - **Responses:**
        
        - **Field_Id_1:** value_1
        - **Field_Id_2:** value_2
        
      
    - **Required Fields:**
      
      - submission_id
      - form_id
      - farmer_id
      - submitted_by_user_id
      - submission_timestamp
      - responses
      
    - **Optional Fields:**
      
      - form_version
      
    
**Frequency:** high  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** PostgreSQL
    - **Table:** dfr_form_submission
    - **Operation:** create
    
**Routing:**
    
    - **Routing Key:** dynamic_form.submitted
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_form_submission_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** notifyOnFormSubmission  
**Processing Type:** async  
    - **Service:** DFR Reporting Service  
**Handler:** updateFormSubmissionAnalytics  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-3-008
    - REQ-NS-001
    
**Error Handling:**
    
    - **Retry Strategy:** None (handled by Odoo transaction or API error response)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 30000
    
  - **Event Id:** EVT-MS-001  
**Event Name:** MobileSyncBatchProcessedEvent  
**Event Type:** integration  
**Category:** MobileSynchronization  
**Description:** Triggered after a batch of data from a mobile device has been received and processed by the server.  
**Trigger Condition:** Successful completion of a server-side mobile data sync operation (REQ-4-006).  
**Source Context:** DFR API Gateway Layer  
**Target Contexts:**
    
    - FarmerRegistry
    - DynamicForms
    - AuditLog
    
**Payload:**
    
    - **Schema:**
      
      - **Sync_Session_Id:** UUID
      - **Device_Id:** string
      - **User_Id:** UUID
      - **Processed_Timestamp:** ISO8601_datetime
      - **Created_Records_Count:** integer
      - **Updated_Records_Count:** integer
      - **Conflicted_Records_Count:** integer
      - **Status:** success|partial_failure
      
    - **Required Fields:**
      
      - sync_session_id
      - device_id
      - user_id
      - processed_timestamp
      - status
      
    - **Optional Fields:**
      
      - created_records_count
      - updated_records_count
      - conflicted_records_count
      
    
**Frequency:** high  
**Business Criticality:** critical  
**Data Source:**
    
    - **Database:** N/A (API triggered)
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** mobile_sync.batch.processed
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_post_sync_processing_queue
    
**Consumers:**
    
    - **Service:** DFR Farmer Registry Service  
**Handler:** triggerPostSyncDeDuplication  
**Processing Type:** async  
    - **Service:** DFR AuditLog Service  
**Handler:** logSyncActivity  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-4-006
    - REQ-API-005
    - REQ-FHR-013
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Server Action Retry (for post-processing failures)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 120000
    
  - **Event Id:** EVT-NS-001  
**Event Name:** NotificationDispatchRequestedEvent  
**Event Type:** system  
**Category:** Notifications  
**Description:** An internal event indicating a notification needs to be composed and dispatched.  
**Trigger Condition:** Business logic determines a notification is required (e.g., after FarmerRegisteredEvent).  
**Source Context:** Various DFR Application Services  
**Target Contexts:**
    
    - NotificationSystem
    
**Payload:**
    
    - **Schema:**
      
      - **Notification_Type_Code:** string
      - **Recipient_Farmer_Id:** UUID (optional)
      - **Recipient_User_Id:** UUID (optional)
      - **Recipient_Email:** string (optional)
      - **Recipient_Phone:** string (optional)
      - **Language_Code:** string
      - **Context_Data:**
        
        - **Key:** value
        
      
    - **Required Fields:**
      
      - notification_type_code
      - language_code
      - context_data
      
    - **Optional Fields:**
      
      - recipient_farmer_id
      - recipient_user_id
      - recipient_email
      - recipient_phone
      
    
**Frequency:** high  
**Business Criticality:** normal  
**Data Source:**
    
    - **Database:** N/A
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** notification.dispatch.request
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_notification_dispatch_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Module  
**Handler:** processAndSendNotification  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-NS-001
    - REQ-NS-002
    - REQ-NS-005
    
**Error Handling:**
    
    - **Retry Strategy:** Odoo Mail Queue Retry / SMS Gateway Retry (external)
    - **Dead Letter Queue:** Odoo `mail.mail` log / Custom Notification Log
    - **Timeout Ms:** 60000
    
  - **Event Id:** EVT-DM-001  
**Event Name:** BulkImportCompletedEvent  
**Event Type:** system  
**Category:** DataManagement  
**Description:** Triggered upon completion (success or failure) of a bulk data import job.  
**Trigger Condition:** A bulk import process finishes (REQ-DM-001, REQ-DM-002).  
**Source Context:** DataManagement (DFR Odoo Application Services)  
**Target Contexts:**
    
    - SystemAdministration
    - Notifications
    
**Payload:**
    
    - **Schema:**
      
      - **Import_Job_Id:** UUID
      - **Start_Time:** ISO8601_datetime
      - **End_Time:** ISO8601_datetime
      - **Status:** success|failed|partial_success
      - **Total_Records_Processed:** integer
      - **Successful_Records_Count:** integer
      - **Failed_Records_Count:** integer
      - **Error_Log_Path:** string (optional)
      
    - **Required Fields:**
      
      - import_job_id
      - start_time
      - end_time
      - status
      - total_records_processed
      
    - **Optional Fields:**
      
      - successful_records_count
      - failed_records_count
      - error_log_path
      
    
**Frequency:** low  
**Business Criticality:** important  
**Data Source:**
    
    - **Database:** N/A (Process completion)
    - **Table:** N/A
    - **Operation:** N/A
    
**Routing:**
    
    - **Routing Key:** data_import.job.completed
    - **Exchange:** dfr_events_internal
    - **Queue:** dfr_admin_notification_queue
    
**Consumers:**
    
    - **Service:** DFR Notification Service  
**Handler:** notifyAdminOfImportCompletion  
**Processing Type:** async  
    
**Dependencies:**
    
    - REQ-DM-001
    - REQ-DM-002
    
**Error Handling:**
    
    - **Retry Strategy:** None (eventual consistency for notification)
    - **Dead Letter Queue:** Odoo Log
    - **Timeout Ms:** 10000
    
  
- **Event Types And Schema Design:**
  
  - **Essential Event Types:**
    
    - **Event Name:** FarmerRegisteredEvent  
**Category:** domain  
**Description:** Signifies a new farmer is officially in the registry.  
**Priority:** high  
    - **Event Name:** FarmerSelfRegistrationSubmittedEvent  
**Category:** domain  
**Description:** Indicates a potential new farmer initiated registration.  
**Priority:** high  
    - **Event Name:** FarmerRecordUpdatedEvent  
**Category:** domain  
**Description:** Captures changes to farmer data, including status.  
**Priority:** medium  
    - **Event Name:** DynamicFormSubmittedEvent  
**Category:** domain  
**Description:** Marks submission of supplementary data for a farmer.  
**Priority:** high  
    - **Event Name:** MobileSyncBatchProcessedEvent  
**Category:** integration  
**Description:** Server-side confirmation of mobile data processing.  
**Priority:** critical  
    - **Event Name:** NotificationDispatchRequestedEvent  
**Category:** system  
**Description:** Internal request to trigger a notification.  
**Priority:** medium  
    - **Event Name:** BulkImportCompletedEvent  
**Category:** system  
**Description:** Signals completion of a data import job.  
**Priority:** medium  
    
  - **Schema Design:**
    
    - **Format:** JSON
    - **Reasoning:** JSON is lightweight, human-readable, widely supported across web and mobile platforms, and explicitly mentioned for DFR APIs (REQ-API-002). Odoo's Python environment handles JSON easily.
    - **Consistency Approach:** Standard event envelope (event_id, timestamp, event_name, version, source_service, payload) for all events. Payload structure specific to event_name.
    
  - **Schema Evolution:**
    
    - **Backward Compatibility:** True
    - **Forward Compatibility:** False
    - **Strategy:** Additive changes to payload for backward compatibility. Introduce new event versions (e.g., `FarmerRegisteredEvent.v2`) for breaking changes. API endpoint versioning for events from/to external systems/mobile.
    
  - **Event Structure:**
    
    - **Standard Fields:**
      
      - event_id (UUID)
      - event_timestamp (ISO8601)
      - event_name (string)
      - event_version (string, e.g., '1.0')
      - source_service (string)
      - country_code (string, if applicable)
      - correlation_id (UUID, optional)
      
    - **Metadata Requirements:**
      
      - user_id_actor (UUID, if applicable)
      - device_id_source (string, for mobile events)
      
    
  
- **Event Routing And Processing:**
  
  - **Routing Mechanisms:**
    
    - **Type:** Odoo Automated Actions / Server Actions  
**Description:** Native Odoo mechanism to trigger Python code or predefined actions based on model CRUD events (create, write, unlink) or time-based conditions (cron).  
**Use Case:** Internal workflow automation, triggering notifications based on data changes (e.g., FarmerRegisteredEvent, FarmerStatusChangedEvent), scheduling batch tasks.  
    - **Type:** Odoo Python Method Calls  
**Description:** Direct synchronous or asynchronous (e.g., using Odoo's job queue if extended, or simple threading for non-critical tasks) calls to methods within Odoo services/modules.  
**Use Case:** Handling API requests (e.g., from mobile sync), processing events that require complex logic not suitable for simple automated actions.  
    - **Type:** Odoo `bus.bus`  
**Description:** Odoo's built-in long-polling mechanism for near real-time communication from server to specific web client sessions.  
**Use Case:** UI updates in Admin Portal based on server-side events (e.g., notification count in menu). This is primarily for UI reactivity, not robust event processing pipelines.  
    
  - **Processing Patterns:**
    
    - **Pattern:** Sequential (within Odoo Transaction)  
**Applicable Scenarios:**
    
    - Most internal DFR operations initiated by user actions or model changes, such as creating a farmer record and immediately logging an audit entry.
    
**Implementation:** Standard Odoo ORM operations and business logic methods executed within a single database transaction.  
    - **Pattern:** Asynchronous (Odoo Mail Queue / Scheduled Actions)  
**Applicable Scenarios:**
    
    - Dispatching notifications (SMS, Email) to avoid blocking primary operations.
    - Running batch de-duplication processes.
    - Generating periodic reports.
    
**Implementation:** Odoo's `mail.mail` queue for email dispatch (inherent retry). Odoo `ir.cron` for scheduled server actions (e.g., batch processing, report generation).  
    
  - **Filtering And Subscription:**
    
    - **Filtering Mechanism:** Odoo Automated Actions allow filtering based on Odoo domain expressions on model fields. Python logic within handlers for finer-grained filtering.
    - **Subscription Model:** Implicit subscription via Odoo Automated Action configuration (model and trigger conditions) or explicit calls in Python code.
    - **Routing Keys:**
      
      - N/A for Odoo internal message bus - model names and method calls act as implicit routing. For external notifications, recipient identifiers (phone, email) are used.
      
    
  - **Handler Isolation:**
    
    - **Required:** True
    - **Approach:** Odoo modules encapsulate specific functionalities. Server Actions run as separate Python methods. Odoo manages process/thread isolation for concurrent users/requests.
    - **Reasoning:** Ensures stability and separation of concerns as per Odoo's modular design.
    
  - **Delivery Guarantees:**
    
    - **Level:** at-least-once
    - **Justification:** For critical operations like farmer registration or data sync, an 'at-least-once' semantic is preferred, with idempotency in handlers to manage duplicates if retries occur. Odoo transactions provide atomicity for internal operations. External notifications (SMS/email) are typically at-least-once from the DFR system's perspective (gateway handles actual delivery).
    - **Implementation:** Idempotent design for API endpoints and critical Odoo server actions. Odoo's mail queue logs attempts. Mobile sync includes conflict resolution (REQ-4-007).
    
  
- **Event Storage And Replay:**
  
  - **Persistence Requirements:**
    
    - **Required:** True
    - **Duration:** As per audit and data retention policies (REQ-SADG-009, REQ-SYSADM-008).
    - **Reasoning:** Essential for auditing (REQ-SADG-005), change history tracking (REQ-SADG-006), and compliance.
    
  - **Event Sourcing:**
    
    - **Necessary:** False
    - **Justification:** The system relies on Odoo models storing current state. Audit logs and `mail.message` (chatter) provide historical context but are not used for state reconstruction via event replay. The current architecture does not mandate full event sourcing.
    - **Scope:**
      
      
    
  - **Technology Options:**
    
    - **Technology:** PostgreSQL (via Odoo ORM - Custom AuditLog Model)  
**Suitability:** high  
**Reasoning:** Primary database; already in use. Odoo ORM provides easy interaction. Suitable for structured audit data (REQ-SADG-005).  
    - **Technology:** Odoo `mail.message` (Chatter)  
**Suitability:** high  
**Reasoning:** Built-in Odoo feature for record-level history and communication. Good for user-visible change tracking (REQ-FHR-010).  
    
  - **Replay Capabilities:**
    
    - **Required:** False
    - **Scenarios:**
      
      - Replaying events for state reconstruction is not a core requirement. Audit logs are for review/investigation, not system state replay.
      
    - **Implementation:** N/A
    
  - **Retention Policy:**
    
    - **Strategy:** Configurable retention periods for audit logs and data entities as per REQ-SADG-009 and REQ-SYSADM-008.
    - **Duration:** To be defined by national policies.
    - **Archiving Approach:** Database archiving/partitioning for older audit logs if performance becomes an issue. Logical 'archived' status for data entities.
    
  
- **Dead Letter Queue And Error Handling:**
  
  - **Dead Letter Strategy:**
    
    - **Approach:** Logging and Administrative Review. For external notifications, Odoo's `mail.mail` queue has error states. For internal automated/server action failures, errors are logged in Odoo's system logs.
    - **Queue Configuration:** N/A (no dedicated event DLQ). Failures are typically logged in Odoo's standard logging mechanisms or specific tables like `mail.mail` for emails.
    - **Processing Logic:** National Administrators or support teams review Odoo logs or failed message queues to identify issues and trigger manual correction or retry if appropriate.
    
  - **Retry Policies:**
    
    - **Error Type:** Notification Gateway Temporary Failure (Email)  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Delay Configuration:** Odoo mail queue default (configurable)  
    - **Error Type:** Notification Gateway Temporary Failure (SMS)  
**Max Retries:** 2  
**Backoff Strategy:** fixed  
**Delay Configuration:** Configurable per gateway integration, if supported by the gateway connector.  
    - **Error Type:** Internal Odoo Automated Action Failure (transient)  
**Max Retries:** 0  
**Backoff Strategy:** none  
**Delay Configuration:** Error logged, manual intervention required if critical.  
    
  - **Poison Message Handling:**
    
    - **Detection Mechanism:** Repeated failures in Odoo logs for specific automated/server actions, or persistent error state in `mail.mail` queue.
    - **Handling Strategy:** Log the error with details, prevent further automatic retries for that specific item after a threshold, alert administrators.
    - **Alerting Required:** True
    
  - **Error Notification:**
    
    - **Channels:**
      
      - Odoo System Logs
      - Email (to administrators for critical system errors via monitoring tools)
      
    - **Severity:** critical|warning
    - **Recipients:**
      
      - National Administrators
      - Super Administrators
      - IT Support Team
      
    
  - **Recovery Procedures:**
    
    - **Scenario:** Failed automated action due to transient data issue  
**Procedure:** Admin identifies error in log, corrects underlying data, manually re-triggers action if necessary.  
**Automation Level:** semi-automated  
    - **Scenario:** Failed notification dispatch (SMS/Email)  
**Procedure:** Admin reviews Odoo mail queue or SMS gateway logs, identifies reason, corrects contact info or gateway config, retries sending.  
**Automation Level:** manual  
    
  
- **Event Versioning Strategy:**
  
  - **Schema Evolution Approach:**
    
    - **Strategy:** For internal Odoo events (processed by Automated/Server Actions), schema changes are managed via Odoo module updates and migrations. For API-based events (e.g., mobile sync), use API endpoint versioning (e.g., /v1/, /v2/) or a version field within the JSON payload (e.g., `"payload_version": "1.1"`).
    - **Versioning Scheme:** Semantic Versioning (X.Y.Z) for API endpoints. Simple incremental versions (e.g., 1.0, 1.1, 2.0) for event payloads if versioned explicitly.
    - **Migration Strategy:** Backend API to support last N-1 versions of mobile app payloads for a defined period to allow graceful client upgrades. Data migration scripts for Odoo model changes.
    
  - **Compatibility Requirements:**
    
    - **Backward Compatible:** True
    - **Forward Compatible:** False
    - **Reasoning:** API consumers (especially mobile app) should continue to function if new optional fields are added to event payloads (backward compatibility). Breaking changes require a new event/API version. Server should not be expected to process event versions it doesn't know.
    
  - **Version Identification:**
    
    - **Mechanism:** For API-driven events: Primarily through API endpoint version (e.g., `/api/dfr/v1/sync`). Optionally, a `payload_version` field within the JSON payload if finer-grained control per event type is needed.
    - **Location:** header (e.g. `Accept: application/vnd.dfr.v1+json`) or payload
    - **Format:** string (e.g., "v1.0", "1.0.0")
    
  - **Consumer Upgrade Strategy:**
    
    - **Approach:** Mobile app update prompts and enforced updates for critical changes (REQ-DIO-012, REQ-4-013). Backend API supports N-1 versions of mobile app for a period.
    - **Rollout Strategy:** Phased rollout for mobile app updates if possible, coordinated with backend API version support.
    - **Rollback Procedure:** Rollback mobile app to previous stable version if major issues. Backend API rollback to previous version if feasible (depends on DB schema changes).
    
  - **Schema Registry:**
    
    - **Required:** False
    - **Technology:** N/A. OpenAPI Specification serves as the schema definition for external APIs. Internal Odoo event structures are defined by Python code and Odoo models.
    - **Governance:** API schema changes managed via version control of OpenAPI spec and Odoo module code.
    
  
- **Event Monitoring And Observability:**
  
  - **Monitoring Capabilities:**
    
    - **Capability:** Odoo Application Logs  
**Justification:** Standard Odoo logging for errors, warnings, and debug information from custom modules and core.  
**Implementation:** Odoo built-in logging framework, configurable log levels.  
    - **Capability:** Custom AuditLog Table  
**Justification:** To meet REQ-SADG-005 for tracking significant user and system actions.  
**Implementation:** Custom Odoo model and Python logic to populate it upon specific events.  
    - **Capability:** Odoo `mail.message` (Chatter) and `mail.mail` queue  
**Justification:** Tracking record-specific changes and communication, and status of outgoing emails.  
**Implementation:** Leverage built-in Odoo features.  
    - **Capability:** External System Monitoring Tools (Prometheus/Grafana)  
**Justification:** For infrastructure, PostgreSQL, and Odoo application performance metrics (REQ-DIO-009).  
**Implementation:** Integration with standard monitoring stacks.  
    
  - **Tracing And Correlation:**
    
    - **Tracing Required:** True
    - **Correlation Strategy:** Use a unique `correlation_id` (e.g., UUID) generated at the start of a business transaction (e.g., API request from mobile, portal submission) and propagate it through related internal events and logs.
    - **Trace Id Propagation:** Pass `correlation_id` in event payloads and log messages. For API calls, can be passed as HTTP header.
    
  - **Performance Metrics:**
    
    - **Metric:** Event Processing Time (for specific automated actions)  
**Threshold:** To be defined (e.g., < 500ms for high-frequency actions)  
**Alerting:** True  
    - **Metric:** Notification Queue Length (Odoo mail.mail)  
**Threshold:** To be defined (e.g., >100 pending for 10 mins)  
**Alerting:** True  
    - **Metric:** API Endpoint Response Time (for event-receiving endpoints)  
**Threshold:** <500ms (REQ-API-009)  
**Alerting:** True  
    - **Metric:** Error Rate for Event Handlers  
**Threshold:** >5% over 5 mins  
**Alerting:** True  
    
  - **Event Flow Visualization:**
    
    - **Required:** False
    - **Tooling:** N/A (Not an essential requirement to build a dedicated event flow visualization tool. Odoo's technical menu provides some insight into automated actions and server actions configuration. Monitoring tools for metrics.)
    - **Scope:** N/A
    
  - **Alerting Requirements:**
    
    - **Condition:** Critical event handler failure (e.g., FarmerRegistrationEvent handler fails repeatedly)  
**Severity:** critical  
**Response Time:** Immediate  
**Escalation Path:**
    
    - On-call Admin
    - Development Team Lead
    
    - **Condition:** Notification queue exceeding threshold  
**Severity:** warning  
**Response Time:** Within 1 hour  
**Escalation Path:**
    
    - System Administrator
    
    - **Condition:** High error rate for API event endpoints  
**Severity:** critical  
**Response Time:** Immediate  
**Escalation Path:**
    
    - On-call Admin
    - API Development Team
    
    
  
- **Implementation Priority:**
  
  - **Component:** Core Domain Event Handling (FarmerRegistered, FarmerUpdated, DynamicFormSubmitted) via Odoo Automated Actions  
**Priority:** high  
**Dependencies:**
    
    - FarmerRegistry Module
    - DynamicForms Module
    
**Estimated Effort:** Included in module development  
  - **Component:** NotificationDispatchRequestedEvent processing and Notification System integration  
**Priority:** high  
**Dependencies:**
    
    - Notification Module
    - Core Domain Event Handlers
    
**Estimated Effort:** Medium  
  - **Component:** MobileSyncBatchProcessedEvent handling (post-sync tasks)  
**Priority:** high  
**Dependencies:**
    
    - API Gateway Layer
    - FarmerRegistry Module (De-duplication)
    
**Estimated Effort:** Medium  
  - **Component:** Audit Logging for key events  
**Priority:** high  
**Dependencies:**
    
    - Core Domain Event Handlers
    - AuditLog Module
    
**Estimated Effort:** Medium  
  - **Component:** Error Handling and Logging for Event Handlers  
**Priority:** high  
**Dependencies:**
    
    - All event handlers
    
**Estimated Effort:** Integrated into handler development  
  
- **Risk Assessment:**
  
  - **Risk:** Over-reliance on synchronous processing within Odoo leading to performance bottlenecks as event volume grows.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Carefully design automated actions for efficiency. Offload truly asynchronous tasks to Odoo cron jobs or Odoo's mail queue. Monitor performance closely (REQ-DIO-009, REQ-DIO-013).  
  - **Risk:** Lack of robust distributed transaction management if trying to coordinate actions across hypothetical future external microservices (currently not in scope, but a future consideration).  
**Impact:** low  
**Probability:** low  
**Mitigation:** Current monolith avoids this. Future integrations would need careful design (e.g., Sagas, idempotent consumers) if they involve distributed state changes.  
  - **Risk:** Difficulty in debugging complex event chains within Odoo's internal mechanisms if not properly logged with correlation IDs.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Implement and enforce use of correlation IDs for complex flows, especially those initiated by APIs. Enhance logging where Odoo's default is insufficient.  
  - **Risk:** Schema evolution for internal events tied to Odoo module updates can be complex if not managed carefully with data migrations.  
**Impact:** medium  
**Probability:** low  
**Mitigation:** Follow Odoo's best practices for module upgrades and data migrations. Thorough testing of upgrades in staging environment.  
  
- **Recommendations:**
  
  - **Category:** Event Schema  
**Recommendation:** Strictly enforce a common event envelope for all defined `projectSpecificEvents` to ensure consistency in logging and potential future processing.  
**Justification:** Improves maintainability and interoperability.  
**Priority:** high  
  - **Category:** Processing Strategy  
**Recommendation:** Leverage Odoo's `Automated Actions` and `Server Actions` for most internal domain event handling. Use custom Python methods for complex logic or API-triggered event processing. Prioritize synchronous processing within transactions for data consistency, using asynchronous mechanisms (mail queue, cron) only for non-blocking tasks like notifications or batch jobs.  
**Justification:** Aligns with Odoo's architecture, minimizes external dependencies, and ensures transactional integrity for core operations.  
**Priority:** high  
  - **Category:** Error Handling  
**Recommendation:** Enhance Odoo's standard logging for failed automated/server actions with more contextual information and ensure these are captured by system monitoring for alerting.  
**Justification:** Improves troubleshooting and reduces mean time to recovery for internal processing failures.  
**Priority:** medium  
  - **Category:** Observability  
**Recommendation:** Ensure `correlation_id` is logged with every significant step of an event-triggered workflow, particularly for those initiated via API (e.g., mobile sync).  
**Justification:** Facilitates easier debugging and tracing of multi-step processes.  
**Priority:** medium  
  - **Category:** Future Scalability  
**Recommendation:** While not immediately essential, for long-term scalability of specific high-volume asynchronous tasks (if they emerge), consider evaluating Odoo's job queue (if available/extended in Odoo 18 CE or via OCA module) or a lightweight external queue for true decoupling, but only if performance monitoring indicates a clear bottleneck with current Odoo mechanisms.  
**Justification:** Proactive consideration for future growth beyond initial scope, but defer implementation until justified by actual needs.  
**Priority:** low  
  


---

