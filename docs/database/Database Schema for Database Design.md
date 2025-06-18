# Specification

# 1. Entities

## 1.1. Farmer
Core entity representing registered farmers

### 1.1.3. Attributes

### 1.1.3.1. id
#### 1.1.3.1.2. Type
UUID

#### 1.1.3.1.3. Is Required
True

#### 1.1.3.1.4. Is Primary Key
True

#### 1.1.3.1.5. Is Unique
True

### 1.1.3.2. uid
#### 1.1.3.2.2. Type
VARCHAR

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Is Unique
True

#### 1.1.3.2.5. Size
20

### 1.1.3.3. fullName
#### 1.1.3.3.2. Type
VARCHAR

#### 1.1.3.3.3. Is Required
True

#### 1.1.3.3.4. Size
100

### 1.1.3.4. dateOfBirth
#### 1.1.3.4.2. Type
DATE

#### 1.1.3.4.3. Is Required
False

### 1.1.3.5. sex
#### 1.1.3.5.2. Type
VARCHAR

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
10

### 1.1.3.6. roleInHousehold
#### 1.1.3.6.2. Type
VARCHAR

#### 1.1.3.6.3. Is Required
False

#### 1.1.3.6.4. Size
50

### 1.1.3.7. educationLevel
#### 1.1.3.7.2. Type
VARCHAR

#### 1.1.3.7.3. Is Required
False

#### 1.1.3.7.4. Size
50

### 1.1.3.8. contactPhone
#### 1.1.3.8.2. Type
VARCHAR

#### 1.1.3.8.3. Is Required
True

#### 1.1.3.8.4. Size
20

### 1.1.3.9. contactEmail
#### 1.1.3.9.2. Type
VARCHAR

#### 1.1.3.9.3. Is Required
False

#### 1.1.3.9.4. Size
100

### 1.1.3.10. nationalIdType
#### 1.1.3.10.2. Type
VARCHAR

#### 1.1.3.10.3. Is Required
False

#### 1.1.3.10.4. Size
50

### 1.1.3.11. nationalIdNumber
#### 1.1.3.11.2. Type
VARCHAR

#### 1.1.3.11.3. Is Required
False

#### 1.1.3.11.4. Size
50

### 1.1.3.12. consentStatus
#### 1.1.3.12.2. Type
VARCHAR

#### 1.1.3.12.3. Is Required
True

#### 1.1.3.12.4. Size
20

#### 1.1.3.12.5. Default Value
Pending

### 1.1.3.13. consentDate
#### 1.1.3.13.2. Type
TIMESTAMP

#### 1.1.3.13.3. Is Required
False

### 1.1.3.14. consentVersion
#### 1.1.3.14.2. Type
VARCHAR

#### 1.1.3.14.3. Is Required
False

#### 1.1.3.14.4. Size
10

### 1.1.3.15. status
#### 1.1.3.15.2. Type
VARCHAR

#### 1.1.3.15.3. Is Required
True

#### 1.1.3.15.4. Size
30

#### 1.1.3.15.5. Default Value
Pending Verification

### 1.1.3.16. createdAt
#### 1.1.3.16.2. Type
TIMESTAMP

#### 1.1.3.16.3. Is Required
True

#### 1.1.3.16.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.17. updatedAt
#### 1.1.3.17.2. Type
TIMESTAMP

#### 1.1.3.17.3. Is Required
True

#### 1.1.3.17.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.18. deletedAt
#### 1.1.3.18.2. Type
TIMESTAMP

#### 1.1.3.18.3. Is Required
False


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints

### 1.1.5.1. uq_farmer_uid
#### 1.1.5.1.2. Columns

- uid


### 1.1.6. Indexes

### 1.1.6.1. idx_farmer_uid
#### 1.1.6.1.2. Columns

- uid

#### 1.1.6.1.3. Type
BTree

### 1.1.6.2. idx_farmer_national_id_number
#### 1.1.6.2.2. Columns

- nationalIdNumber

#### 1.1.6.2.3. Type
BTree

### 1.1.6.3. idx_farmer_contact_phone
#### 1.1.6.3.2. Columns

- contactPhone

#### 1.1.6.3.3. Type
BTree

### 1.1.6.4. idx_farmer_status
#### 1.1.6.4.2. Columns

- status

#### 1.1.6.4.3. Type
BTree

### 1.1.6.5. idx_farmer_fullname_dob
#### 1.1.6.5.2. Columns

- fullName
- dateOfBirth

#### 1.1.6.5.3. Type
BTree

### 1.1.6.6. idx_farmer_consent_status
#### 1.1.6.6.2. Columns

- consentStatus

#### 1.1.6.6.3. Type
BTree

### 1.1.6.7. idx_farmer_created_at
#### 1.1.6.7.2. Columns

- createdAt

#### 1.1.6.7.3. Type
BTree


## 1.2. Household
Represents a farmer household unit

### 1.2.3. Attributes

### 1.2.3.1. id
#### 1.2.3.1.2. Type
UUID

#### 1.2.3.1.3. Is Required
True

#### 1.2.3.1.4. Is Primary Key
True

#### 1.2.3.1.5. Is Unique
True

### 1.2.3.2. uid
#### 1.2.3.2.2. Type
VARCHAR

#### 1.2.3.2.3. Is Required
True

#### 1.2.3.2.4. Is Unique
True

#### 1.2.3.2.5. Size
20

### 1.2.3.3. createdAt
#### 1.2.3.3.2. Type
TIMESTAMP

#### 1.2.3.3.3. Is Required
True

#### 1.2.3.3.4. Default Value
CURRENT_TIMESTAMP

### 1.2.3.4. updatedAt
#### 1.2.3.4.2. Type
TIMESTAMP

#### 1.2.3.4.3. Is Required
True

#### 1.2.3.4.4. Default Value
CURRENT_TIMESTAMP


### 1.2.4. Primary Keys

- id

### 1.2.5. Unique Constraints

### 1.2.5.1. uq_household_uid
#### 1.2.5.1.2. Columns

- uid


### 1.2.6. Indexes

### 1.2.6.1. idx_household_uid
#### 1.2.6.1.2. Columns

- uid

#### 1.2.6.1.3. Type
BTree


## 1.3. HouseholdMember
Members belonging to a household

### 1.3.3. Attributes

### 1.3.3.1. id
#### 1.3.3.1.2. Type
UUID

#### 1.3.3.1.3. Is Required
True

#### 1.3.3.1.4. Is Primary Key
True

### 1.3.3.2. householdId
#### 1.3.3.2.2. Type
UUID

#### 1.3.3.2.3. Is Required
True

#### 1.3.3.2.4. Is Foreign Key
True

### 1.3.3.3. farmerId
#### 1.3.3.3.2. Type
UUID

#### 1.3.3.3.3. Is Required
False

#### 1.3.3.3.4. Is Foreign Key
True

### 1.3.3.4. relationshipToHead
#### 1.3.3.4.2. Type
VARCHAR

#### 1.3.3.4.3. Is Required
True

#### 1.3.3.4.4. Size
50

### 1.3.3.5. roleInHousehold
#### 1.3.3.5.2. Type
VARCHAR

#### 1.3.3.5.3. Is Required
False

#### 1.3.3.5.4. Size
50

### 1.3.3.6. educationLevel
#### 1.3.3.6.2. Type
VARCHAR

#### 1.3.3.6.3. Is Required
False

#### 1.3.3.6.4. Size
50


### 1.3.4. Primary Keys

- id

### 1.3.5. Unique Constraints


### 1.3.6. Indexes


## 1.4. Farm
Agricultural farm associated with farmer/household

### 1.4.3. Attributes

### 1.4.3.1. id
#### 1.4.3.1.2. Type
UUID

#### 1.4.3.1.3. Is Required
True

#### 1.4.3.1.4. Is Primary Key
True

### 1.4.3.2. farmerId
#### 1.4.3.2.2. Type
UUID

#### 1.4.3.2.3. Is Required
False

#### 1.4.3.2.4. Is Foreign Key
True

### 1.4.3.3. householdId
#### 1.4.3.3.2. Type
UUID

#### 1.4.3.3.3. Is Required
False

#### 1.4.3.3.4. Is Foreign Key
True

### 1.4.3.4. name
#### 1.4.3.4.2. Type
VARCHAR

#### 1.4.3.4.3. Is Required
False

#### 1.4.3.4.4. Size
100


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints


### 1.4.6. Indexes


## 1.5. Plot
Individual land plots within a farm

### 1.5.3. Attributes

### 1.5.3.1. id
#### 1.5.3.1.2. Type
UUID

#### 1.5.3.1.3. Is Required
True

#### 1.5.3.1.4. Is Primary Key
True

### 1.5.3.2. farmId
#### 1.5.3.2.2. Type
UUID

#### 1.5.3.2.3. Is Required
True

#### 1.5.3.2.4. Is Foreign Key
True

### 1.5.3.3. size
#### 1.5.3.3.2. Type
DECIMAL

#### 1.5.3.3.3. Is Required
True

#### 1.5.3.3.4. Precision
10

#### 1.5.3.3.5. Scale
2

### 1.5.3.4. landTenureType
#### 1.5.3.4.2. Type
VARCHAR

#### 1.5.3.4.3. Is Required
True

#### 1.5.3.4.4. Size
50

### 1.5.3.5. primaryCrop
#### 1.5.3.5.2. Type
VARCHAR

#### 1.5.3.5.3. Is Required
False

#### 1.5.3.5.4. Size
50

### 1.5.3.6. latitude
#### 1.5.3.6.2. Type
DECIMAL

#### 1.5.3.6.3. Is Required
True

#### 1.5.3.6.4. Precision
9

#### 1.5.3.6.5. Scale
6

### 1.5.3.7. longitude
#### 1.5.3.7.2. Type
DECIMAL

#### 1.5.3.7.3. Is Required
True

#### 1.5.3.7.4. Precision
9

#### 1.5.3.7.5. Scale
6

### 1.5.3.8. ownershipDetails
#### 1.5.3.8.2. Type
TEXT

#### 1.5.3.8.3. Is Required
False


### 1.5.4. Primary Keys

- id

### 1.5.5. Unique Constraints


### 1.5.6. Indexes

### 1.5.6.1. idx_plot_location_spatial
#### 1.5.6.1.2. Columns

- latitude
- longitude

#### 1.5.6.1.3. Type
GiST


## 1.6. AdministrativeArea
Hierarchical geographical areas (region/district/village)

### 1.6.3. Attributes

### 1.6.3.1. id
#### 1.6.3.1.2. Type
UUID

#### 1.6.3.1.3. Is Required
True

#### 1.6.3.1.4. Is Primary Key
True

### 1.6.3.2. name
#### 1.6.3.2.2. Type
VARCHAR

#### 1.6.3.2.3. Is Required
True

#### 1.6.3.2.4. Size
100

### 1.6.3.3. type
#### 1.6.3.3.2. Type
VARCHAR

#### 1.6.3.3.3. Is Required
True

#### 1.6.3.3.4. Size
20

### 1.6.3.4. parentId
#### 1.6.3.4.2. Type
UUID

#### 1.6.3.4.3. Is Required
False

#### 1.6.3.4.4. Is Foreign Key
True


### 1.6.4. Primary Keys

- id

### 1.6.5. Unique Constraints


### 1.6.6. Indexes

### 1.6.6.1. idx_admin_area_name_type
#### 1.6.6.1.2. Columns

- name
- type

#### 1.6.6.1.3. Type
BTree

### 1.6.6.2. idx_admin_area_parent_id
#### 1.6.6.2.2. Columns

- parentId

#### 1.6.6.2.3. Type
BTree


## 1.7. DynamicForm
Template for customizable data collection forms

### 1.7.3. Attributes

### 1.7.3.1. id
#### 1.7.3.1.2. Type
UUID

#### 1.7.3.1.3. Is Required
True

#### 1.7.3.1.4. Is Primary Key
True

### 1.7.3.2. name
#### 1.7.3.2.2. Type
VARCHAR

#### 1.7.3.2.3. Is Required
True

#### 1.7.3.2.4. Size
100

### 1.7.3.3. version
#### 1.7.3.3.2. Type
VARCHAR

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Size
10

### 1.7.3.4. status
#### 1.7.3.4.2. Type
VARCHAR

#### 1.7.3.4.3. Is Required
True

#### 1.7.3.4.4. Size
20

#### 1.7.3.4.5. Default Value
Draft

### 1.7.3.5. isPortalAccessible
#### 1.7.3.5.2. Type
BOOLEAN

#### 1.7.3.5.3. Is Required
True

#### 1.7.3.5.4. Default Value
false

### 1.7.3.6. createdAt
#### 1.7.3.6.2. Type
TIMESTAMP

#### 1.7.3.6.3. Is Required
True

#### 1.7.3.6.4. Default Value
CURRENT_TIMESTAMP


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints

### 1.7.5.1. uq_dynamicform_name_version
#### 1.7.5.1.2. Columns

- name
- version


### 1.7.6. Indexes

### 1.7.6.1. idx_dynamicform_status
#### 1.7.6.1.2. Columns

- status

#### 1.7.6.1.3. Type
BTree


## 1.8. FormField
Fields within a dynamic form

### 1.8.3. Attributes

### 1.8.3.1. id
#### 1.8.3.1.2. Type
UUID

#### 1.8.3.1.3. Is Required
True

#### 1.8.3.1.4. Is Primary Key
True

### 1.8.3.2. formId
#### 1.8.3.2.2. Type
UUID

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

### 1.8.3.3. fieldType
#### 1.8.3.3.2. Type
VARCHAR

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Size
20

### 1.8.3.4. label
#### 1.8.3.4.2. Type
VARCHAR

#### 1.8.3.4.3. Is Required
True

#### 1.8.3.4.4. Size
100

### 1.8.3.5. isRequired
#### 1.8.3.5.2. Type
BOOLEAN

#### 1.8.3.5.3. Is Required
True

#### 1.8.3.5.4. Default Value
false

### 1.8.3.6. validationRules
#### 1.8.3.6.2. Type
JSON

#### 1.8.3.6.3. Is Required
False

### 1.8.3.7. conditionalLogic
#### 1.8.3.7.2. Type
JSON

#### 1.8.3.7.3. Is Required
False

### 1.8.3.8. order
#### 1.8.3.8.2. Type
INT

#### 1.8.3.8.3. Is Required
True


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints


### 1.8.6. Indexes

### 1.8.6.1. idx_formfield_form_order
#### 1.8.6.1.2. Columns

- formId
- order

#### 1.8.6.1.3. Type
BTree


## 1.9. FormSubmission
Instance of a submitted dynamic form

### 1.9.3. Attributes

### 1.9.3.1. id
#### 1.9.3.1.2. Type
UUID

#### 1.9.3.1.3. Is Required
True

#### 1.9.3.1.4. Is Primary Key
True

### 1.9.3.2. formId
#### 1.9.3.2.2. Type
UUID

#### 1.9.3.2.3. Is Required
True

#### 1.9.3.2.4. Is Foreign Key
True

### 1.9.3.3. farmerId
#### 1.9.3.3.2. Type
UUID

#### 1.9.3.3.3. Is Required
True

#### 1.9.3.3.4. Is Foreign Key
True

### 1.9.3.4. submissionDate
#### 1.9.3.4.2. Type
TIMESTAMP

#### 1.9.3.4.3. Is Required
True

#### 1.9.3.4.4. Default Value
CURRENT_TIMESTAMP

### 1.9.3.5. status
#### 1.9.3.5.2. Type
VARCHAR

#### 1.9.3.5.3. Is Required
True

#### 1.9.3.5.4. Size
20

#### 1.9.3.5.5. Default Value
Submitted


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints


### 1.9.6. Indexes

### 1.9.6.1. idx_formsubmission_farmer_form
#### 1.9.6.1.2. Columns

- farmerId
- formId

#### 1.9.6.1.3. Type
BTree

### 1.9.6.2. idx_formsubmission_submission_date
#### 1.9.6.2.2. Columns

- submissionDate

#### 1.9.6.2.3. Type
BTree

### 1.9.6.3. idx_formsubmission_status
#### 1.9.6.3.2. Columns

- status

#### 1.9.6.3.3. Type
BTree


## 1.10. FormResponse
Responses for individual form fields

### 1.10.3. Attributes

### 1.10.3.1. id
#### 1.10.3.1.2. Type
UUID

#### 1.10.3.1.3. Is Required
True

#### 1.10.3.1.4. Is Primary Key
True

### 1.10.3.2. submissionId
#### 1.10.3.2.2. Type
UUID

#### 1.10.3.2.3. Is Required
True

#### 1.10.3.2.4. Is Foreign Key
True

### 1.10.3.3. fieldId
#### 1.10.3.3.2. Type
UUID

#### 1.10.3.3.3. Is Required
True

#### 1.10.3.3.4. Is Foreign Key
True

### 1.10.3.4. value
#### 1.10.3.4.2. Type
TEXT

#### 1.10.3.4.3. Is Required
True


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints


### 1.10.6. Indexes

### 1.10.6.1. idx_formresponse_submission_field
#### 1.10.6.1.2. Columns

- submissionId
- fieldId

#### 1.10.6.1.3. Type
BTree

### 1.10.6.2. idx_formresponse_value_gin
#### 1.10.6.2.2. Columns

- value

#### 1.10.6.2.3. Type
GIN


## 1.11. User
System users with access permissions

### 1.11.3. Attributes

### 1.11.3.1. id
#### 1.11.3.1.2. Type
UUID

#### 1.11.3.1.3. Is Required
True

#### 1.11.3.1.4. Is Primary Key
True

### 1.11.3.2. username
#### 1.11.3.2.2. Type
VARCHAR

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Is Unique
True

#### 1.11.3.2.5. Size
50

### 1.11.3.3. passwordHash
#### 1.11.3.3.2. Type
VARCHAR

#### 1.11.3.3.3. Is Required
True

#### 1.11.3.3.4. Size
100

### 1.11.3.4. role
#### 1.11.3.4.2. Type
VARCHAR

#### 1.11.3.4.3. Is Required
True

#### 1.11.3.4.4. Size
30

### 1.11.3.5. assignedAreaId
#### 1.11.3.5.2. Type
UUID

#### 1.11.3.5.3. Is Required
False

#### 1.11.3.5.4. Is Foreign Key
True

### 1.11.3.6. lastLogin
#### 1.11.3.6.2. Type
TIMESTAMP

#### 1.11.3.6.3. Is Required
False

### 1.11.3.7. isActive
#### 1.11.3.7.2. Type
BOOLEAN

#### 1.11.3.7.3. Is Required
True

#### 1.11.3.7.4. Default Value
true


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints

### 1.11.5.1. uq_user_username
#### 1.11.5.1.2. Columns

- username


### 1.11.6. Indexes

### 1.11.6.1. idx_user_role
#### 1.11.6.1.2. Columns

- role

#### 1.11.6.1.3. Type
BTree


## 1.12. Notification
System-generated notifications

### 1.12.3. Attributes

### 1.12.3.1. id
#### 1.12.3.1.2. Type
UUID

#### 1.12.3.1.3. Is Required
True

#### 1.12.3.1.4. Is Primary Key
True

### 1.12.3.2. recipient
#### 1.12.3.2.2. Type
VARCHAR

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Size
100

### 1.12.3.3. channel
#### 1.12.3.3.2. Type
VARCHAR

#### 1.12.3.3.3. Is Required
True

#### 1.12.3.3.4. Size
10

### 1.12.3.4. content
#### 1.12.3.4.2. Type
TEXT

#### 1.12.3.4.3. Is Required
True

### 1.12.3.5. status
#### 1.12.3.5.2. Type
VARCHAR

#### 1.12.3.5.3. Is Required
True

#### 1.12.3.5.4. Size
20

#### 1.12.3.5.5. Default Value
Pending

### 1.12.3.6. sentAt
#### 1.12.3.6.2. Type
TIMESTAMP

#### 1.12.3.6.3. Is Required
False

### 1.12.3.7. triggerEvent
#### 1.12.3.7.2. Type
VARCHAR

#### 1.12.3.7.3. Is Required
True

#### 1.12.3.7.4. Size
50


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes


## 1.13. AuditLog
System activity and change history

### 1.13.3. Attributes

### 1.13.3.1. id
#### 1.13.3.1.2. Type
UUID

#### 1.13.3.1.3. Is Required
True

#### 1.13.3.1.4. Is Primary Key
True

### 1.13.3.2. entityName
#### 1.13.3.2.2. Type
VARCHAR

#### 1.13.3.2.3. Is Required
True

#### 1.13.3.2.4. Size
50

### 1.13.3.3. entityId
#### 1.13.3.3.2. Type
UUID

#### 1.13.3.3.3. Is Required
True

### 1.13.3.4. action
#### 1.13.3.4.2. Type
VARCHAR

#### 1.13.3.4.3. Is Required
True

#### 1.13.3.4.4. Size
20

### 1.13.3.5. userId
#### 1.13.3.5.2. Type
UUID

#### 1.13.3.5.3. Is Required
True

#### 1.13.3.5.4. Is Foreign Key
True

### 1.13.3.6. oldValue
#### 1.13.3.6.2. Type
JSON

#### 1.13.3.6.3. Is Required
False

### 1.13.3.7. newValue
#### 1.13.3.7.2. Type
JSON

#### 1.13.3.7.3. Is Required
False

### 1.13.3.8. timestamp
#### 1.13.3.8.2. Type
TIMESTAMP

#### 1.13.3.8.3. Is Required
True

#### 1.13.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.13.4. Primary Keys

- id

### 1.13.5. Unique Constraints


### 1.13.6. Indexes

### 1.13.6.1. idx_auditlog_entity_id_ts
#### 1.13.6.1.2. Columns

- entityName
- entityId
- timestamp

#### 1.13.6.1.3. Type
BTree

### 1.13.6.2. idx_auditlog_user_ts
#### 1.13.6.2.2. Columns

- userId
- timestamp

#### 1.13.6.2.3. Type
BTree


## 1.14. MobileDevice
Enumerator mobile devices for offline sync

### 1.14.3. Attributes

### 1.14.3.1. id
#### 1.14.3.1.2. Type
UUID

#### 1.14.3.1.3. Is Required
True

#### 1.14.3.1.4. Is Primary Key
True

### 1.14.3.2. userId
#### 1.14.3.2.2. Type
UUID

#### 1.14.3.2.3. Is Required
True

#### 1.14.3.2.4. Is Foreign Key
True

### 1.14.3.3. deviceId
#### 1.14.3.3.2. Type
VARCHAR

#### 1.14.3.3.3. Is Required
True

#### 1.14.3.3.4. Size
100

### 1.14.3.4. lastSync
#### 1.14.3.4.2. Type
TIMESTAMP

#### 1.14.3.4.3. Is Required
False

### 1.14.3.5. appVersion
#### 1.14.3.5.2. Type
VARCHAR

#### 1.14.3.5.3. Is Required
True

#### 1.14.3.5.4. Size
20


### 1.14.4. Primary Keys

- id

### 1.14.5. Unique Constraints


### 1.14.6. Indexes

### 1.14.6.1. idx_mobiledevice_deviceid
#### 1.14.6.1.2. Columns

- deviceId

#### 1.14.6.1.3. Type
BTree


## 1.15. SyncSession
Mobile-to-server synchronization records

### 1.15.3. Attributes

### 1.15.3.1. id
#### 1.15.3.1.2. Type
UUID

#### 1.15.3.1.3. Is Required
True

#### 1.15.3.1.4. Is Primary Key
True

### 1.15.3.2. deviceId
#### 1.15.3.2.2. Type
UUID

#### 1.15.3.2.3. Is Required
True

#### 1.15.3.2.4. Is Foreign Key
True

### 1.15.3.3. startTime
#### 1.15.3.3.2. Type
TIMESTAMP

#### 1.15.3.3.3. Is Required
True

### 1.15.3.4. endTime
#### 1.15.3.4.2. Type
TIMESTAMP

#### 1.15.3.4.3. Is Required
False

### 1.15.3.5. recordsSynced
#### 1.15.3.5.2. Type
INT

#### 1.15.3.5.3. Is Required
True

### 1.15.3.6. conflictCount
#### 1.15.3.6.2. Type
INT

#### 1.15.3.6.3. Is Required
True

#### 1.15.3.6.4. Default Value
0

### 1.15.3.7. status
#### 1.15.3.7.2. Type
VARCHAR

#### 1.15.3.7.3. Is Required
True

#### 1.15.3.7.4. Size
20


### 1.15.4. Primary Keys

- id

### 1.15.5. Unique Constraints


### 1.15.6. Indexes

### 1.15.6.1. idx_syncsession_status_starttime
#### 1.15.6.1.2. Columns

- status
- startTime

#### 1.15.6.1.3. Type
BTree


## 1.16. Tag
Categorization for dynamic forms

### 1.16.3. Attributes

### 1.16.3.1. id
#### 1.16.3.1.2. Type
UUID

#### 1.16.3.1.3. Is Required
True

#### 1.16.3.1.4. Is Primary Key
True

### 1.16.3.2. name
#### 1.16.3.2.2. Type
VARCHAR

#### 1.16.3.2.3. Is Required
True

#### 1.16.3.2.4. Is Unique
True

#### 1.16.3.2.5. Size
50


### 1.16.4. Primary Keys

- id

### 1.16.5. Unique Constraints

### 1.16.5.1. uq_tag_name
#### 1.16.5.1.2. Columns

- name


### 1.16.6. Indexes


## 1.17. FormTag
Relationship between forms and tags

### 1.17.3. Attributes

### 1.17.3.1. formId
#### 1.17.3.1.2. Type
UUID

#### 1.17.3.1.3. Is Required
True

#### 1.17.3.1.4. Is Foreign Key
True

### 1.17.3.2. tagId
#### 1.17.3.2.2. Type
UUID

#### 1.17.3.2.3. Is Required
True

#### 1.17.3.2.4. Is Foreign Key
True


### 1.17.4. Primary Keys

- formId
- tagId

### 1.17.5. Unique Constraints


### 1.17.6. Indexes

### 1.17.6.1. idx_formtag_tag_form
#### 1.17.6.1.2. Columns

- tagId
- formId

#### 1.17.6.1.3. Type
BTree




---

# 2. Relations

## 2.1. FarmerHouseholdMember
### 2.1.3. Source Entity
Farmer

### 2.1.4. Target Entity
HouseholdMember

### 2.1.5. Type
OneToOne

### 2.1.6. Source Multiplicity
One

### 2.1.7. Target Multiplicity
ZeroOrOne

### 2.1.8. Cascade Delete
False

### 2.1.9. Is Identifying
False

### 2.1.10. On Delete
SetNull

### 2.1.11. On Update
NoAction

## 2.2. HouseholdMembers
### 2.2.3. Source Entity
Household

### 2.2.4. Target Entity
HouseholdMember

### 2.2.5. Type
OneToMany

### 2.2.6. Source Multiplicity
One

### 2.2.7. Target Multiplicity
Many

### 2.2.8. Cascade Delete
True

### 2.2.9. Is Identifying
True

### 2.2.10. On Delete
Cascade

### 2.2.11. On Update
NoAction

## 2.3. FarmerFarms
### 2.3.3. Source Entity
Farmer

### 2.3.4. Target Entity
Farm

### 2.3.5. Type
OneToMany

### 2.3.6. Source Multiplicity
One

### 2.3.7. Target Multiplicity
Many

### 2.3.8. Cascade Delete
False

### 2.3.9. Is Identifying
False

### 2.3.10. On Delete
SetNull

### 2.3.11. On Update
NoAction

## 2.4. HouseholdFarms
### 2.4.3. Source Entity
Household

### 2.4.4. Target Entity
Farm

### 2.4.5. Type
OneToMany

### 2.4.6. Source Multiplicity
One

### 2.4.7. Target Multiplicity
Many

### 2.4.8. Cascade Delete
False

### 2.4.9. Is Identifying
False

### 2.4.10. On Delete
SetNull

### 2.4.11. On Update
NoAction

## 2.5. FarmPlots
### 2.5.3. Source Entity
Farm

### 2.5.4. Target Entity
Plot

### 2.5.5. Type
OneToMany

### 2.5.6. Source Multiplicity
One

### 2.5.7. Target Multiplicity
Many

### 2.5.8. Cascade Delete
True

### 2.5.9. Is Identifying
True

### 2.5.10. On Delete
Cascade

### 2.5.11. On Update
NoAction

## 2.6. AdminAreaHierarchy
### 2.6.3. Source Entity
AdministrativeArea

### 2.6.4. Target Entity
AdministrativeArea

### 2.6.5. Type
OneToMany

### 2.6.6. Source Multiplicity
One

### 2.6.7. Target Multiplicity
Many

### 2.6.8. Cascade Delete
False

### 2.6.9. Is Identifying
False

### 2.6.10. On Delete
Restrict

### 2.6.11. On Update
NoAction

## 2.7. FormFields
### 2.7.3. Source Entity
DynamicForm

### 2.7.4. Target Entity
FormField

### 2.7.5. Type
OneToMany

### 2.7.6. Source Multiplicity
One

### 2.7.7. Target Multiplicity
Many

### 2.7.8. Cascade Delete
True

### 2.7.9. Is Identifying
True

### 2.7.10. On Delete
Cascade

### 2.7.11. On Update
NoAction

## 2.8. FormSubmissions
### 2.8.3. Source Entity
DynamicForm

### 2.8.4. Target Entity
FormSubmission

### 2.8.5. Type
OneToMany

### 2.8.6. Source Multiplicity
One

### 2.8.7. Target Multiplicity
Many

### 2.8.8. Cascade Delete
False

### 2.8.9. Is Identifying
False

### 2.8.10. On Delete
Restrict

### 2.8.11. On Update
NoAction

## 2.9. SubmissionResponses
### 2.9.3. Source Entity
FormSubmission

### 2.9.4. Target Entity
FormResponse

### 2.9.5. Type
OneToMany

### 2.9.6. Source Multiplicity
One

### 2.9.7. Target Multiplicity
Many

### 2.9.8. Cascade Delete
True

### 2.9.9. Is Identifying
True

### 2.9.10. On Delete
Cascade

### 2.9.11. On Update
NoAction

## 2.10. ResponseField
### 2.10.3. Source Entity
FormField

### 2.10.4. Target Entity
FormResponse

### 2.10.5. Type
OneToMany

### 2.10.6. Source Multiplicity
One

### 2.10.7. Target Multiplicity
Many

### 2.10.8. Cascade Delete
False

### 2.10.9. Is Identifying
False

### 2.10.10. On Delete
Restrict

### 2.10.11. On Update
NoAction

## 2.11. FarmerSubmissions
### 2.11.3. Source Entity
Farmer

### 2.11.4. Target Entity
FormSubmission

### 2.11.5. Type
OneToMany

### 2.11.6. Source Multiplicity
One

### 2.11.7. Target Multiplicity
Many

### 2.11.8. Cascade Delete
False

### 2.11.9. Is Identifying
False

### 2.11.10. On Delete
Restrict

### 2.11.11. On Update
NoAction

## 2.12. AreaUsers
### 2.12.3. Source Entity
AdministrativeArea

### 2.12.4. Target Entity
User

### 2.12.5. Type
OneToMany

### 2.12.6. Source Multiplicity
One

### 2.12.7. Target Multiplicity
Many

### 2.12.8. Cascade Delete
False

### 2.12.9. Is Identifying
False

### 2.12.10. On Delete
SetNull

### 2.12.11. On Update
NoAction

## 2.13. UserDevices
### 2.13.3. Source Entity
User

### 2.13.4. Target Entity
MobileDevice

### 2.13.5. Type
OneToMany

### 2.13.6. Source Multiplicity
One

### 2.13.7. Target Multiplicity
Many

### 2.13.8. Cascade Delete
True

### 2.13.9. Is Identifying
True

### 2.13.10. On Delete
Cascade

### 2.13.11. On Update
NoAction

## 2.14. DeviceSessions
### 2.14.3. Source Entity
MobileDevice

### 2.14.4. Target Entity
SyncSession

### 2.14.5. Type
OneToMany

### 2.14.6. Source Multiplicity
One

### 2.14.7. Target Multiplicity
Many

### 2.14.8. Cascade Delete
True

### 2.14.9. Is Identifying
True

### 2.14.10. On Delete
Cascade

### 2.14.11. On Update
NoAction

## 2.15. FormTags
### 2.15.3. Source Entity
DynamicForm

### 2.15.4. Target Entity
Tag

### 2.15.5. Type
ManyToMany

### 2.15.6. Source Multiplicity
Many

### 2.15.7. Target Multiplicity
Many

### 2.15.8. Cascade Delete
False

### 2.15.9. Is Identifying
False

### 2.15.10. Join Table
### 2.15.10. FormTag
#### 2.15.10.2. Columns

- **Name:** formId  
**Type:** UUID  
**References:** DynamicForm.id  
- **Name:** tagId  
**Type:** UUID  
**References:** Tag.id  

### 2.15.11. On Delete
Cascade

### 2.15.12. On Update
NoAction

## 2.16. UserAuditLogs
### 2.16.3. Source Entity
User

### 2.16.4. Target Entity
AuditLog

### 2.16.5. Type
OneToMany

### 2.16.6. Source Multiplicity
One

### 2.16.7. Target Multiplicity
Many

### 2.16.8. Cascade Delete
False

### 2.16.9. Is Identifying
False

### 2.16.10. On Delete
Restrict

### 2.16.11. On Update
NoAction

## 2.17. farmer_sex_relationship
### 2.17.3. Source Entity
Farmer

### 2.17.4. Target Entity
SexLookup

### 2.17.5. Type
OneToMany

### 2.17.6. Source Multiplicity
*

### 2.17.7. Target Multiplicity
1

### 2.17.8. Cascade Delete
False

### 2.17.9. Is Identifying
False

### 2.17.10. On Delete
Restrict

### 2.17.11. On Update
Cascade

## 2.18. farmer_status_relationship
### 2.18.3. Source Entity
Farmer

### 2.18.4. Target Entity
FarmerStatusLookup

### 2.18.5. Type
OneToMany

### 2.18.6. Source Multiplicity
*

### 2.18.7. Target Multiplicity
1

### 2.18.8. Cascade Delete
False

### 2.18.9. Is Identifying
False

### 2.18.10. On Delete
Restrict

### 2.18.11. On Update
Cascade

## 2.19. plot_land_tenure_type_relationship
### 2.19.3. Source Entity
Plot

### 2.19.4. Target Entity
LandTenureTypeLookup

### 2.19.5. Type
OneToMany

### 2.19.6. Source Multiplicity
*

### 2.19.7. Target Multiplicity
1

### 2.19.8. Cascade Delete
False

### 2.19.9. Is Identifying
False

### 2.19.10. On Delete
Restrict

### 2.19.11. On Update
Cascade

## 2.20. dynamic_form_status_relationship
### 2.20.3. Source Entity
DynamicForm

### 2.20.4. Target Entity
FormStatusLookup

### 2.20.5. Type
OneToMany

### 2.20.6. Source Multiplicity
*

### 2.20.7. Target Multiplicity
1

### 2.20.8. Cascade Delete
False

### 2.20.9. Is Identifying
False

### 2.20.10. On Delete
Restrict

### 2.20.11. On Update
Cascade

## 2.21. user_role_relationship
### 2.21.3. Source Entity
User

### 2.21.4. Target Entity
RoleLookup

### 2.21.5. Type
OneToMany

### 2.21.6. Source Multiplicity
*

### 2.21.7. Target Multiplicity
1

### 2.21.8. Cascade Delete
False

### 2.21.9. Is Identifying
False

### 2.21.10. On Delete
Restrict

### 2.21.11. On Update
Cascade



---

