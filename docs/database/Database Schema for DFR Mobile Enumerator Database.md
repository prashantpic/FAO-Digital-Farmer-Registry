# Specification

# 1. Database Design

## 1.1. Farmer
Local copy of core farmer data needed on the mobile device.

### 1.1.3. Attributes

### 1.1.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.1.3.1.2. Type
TEXT

#### 1.1.3.1.3. Is Required
True

#### 1.1.3.1.4. Is Primary Key
True

### 1.1.3.2. uid
Farmer UID.

#### 1.1.3.2.2. Type
VARCHAR

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Size
20

### 1.1.3.3. fullName
Full name.

#### 1.1.3.3.2. Type
VARCHAR

#### 1.1.3.3.3. Is Required
True

#### 1.1.3.3.4. Size
100

### 1.1.3.4. dateOfBirth
Date of birth (stored as text, e.g., YYYY-MM-DD).

#### 1.1.3.4.2. Type
TEXT

#### 1.1.3.4.3. Is Required
False

### 1.1.3.5. sex
Sex.

#### 1.1.3.5.2. Type
VARCHAR

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
10

### 1.1.3.6. contactPhone
Contact phone number.

#### 1.1.3.6.2. Type
VARCHAR

#### 1.1.3.6.3. Is Required
True

#### 1.1.3.6.4. Size
20

### 1.1.3.7. nationalIdType
National ID Type.

#### 1.1.3.7.2. Type
VARCHAR

#### 1.1.3.7.3. Is Required
False

#### 1.1.3.7.4. Size
50

### 1.1.3.8. nationalIdNumber
National ID Number.

#### 1.1.3.8.2. Type
VARCHAR

#### 1.1.3.8.3. Is Required
False

#### 1.1.3.8.4. Size
50

### 1.1.3.9. status
Farmer status.

#### 1.1.3.9.2. Type
VARCHAR

#### 1.1.3.9.3. Is Required
True

#### 1.1.3.9.4. Size
30

### 1.1.3.10. syncStatus
Synchronization status of the record.

#### 1.1.3.10.2. Type
VARCHAR

#### 1.1.3.10.3. Is Required
True

#### 1.1.3.10.4. Size
20

#### 1.1.3.10.5. Default Value
'Synced'

#### 1.1.3.10.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.1.3.11. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt for this record.

#### 1.1.3.11.2. Type
INTEGER

#### 1.1.3.11.3. Is Required
False

### 1.1.3.12. isDeleted
Flag for soft deletion on the device before syncing delete operation.

#### 1.1.3.12.2. Type
BOOLEAN

#### 1.1.3.12.3. Is Required
True

#### 1.1.3.12.4. Default Value
false

### 1.1.3.13. localDraftData
JSON or other format for locally held changes/drafts not yet marked for sync.

#### 1.1.3.13.2. Type
TEXT

#### 1.1.3.13.3. Is Required
False


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints


### 1.1.6. Indexes

### 1.1.6.1. idx_mobile_farmer_uid
Index on UID for local lookups.

#### 1.1.6.1.2. Columns

- uid

#### 1.1.6.1.3. Type
BTree


## 1.2. Household
Local copy of household data.

### 1.2.3. Attributes

### 1.2.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.2.3.1.2. Type
TEXT

#### 1.2.3.1.3. Is Required
True

#### 1.2.3.1.4. Is Primary Key
True

### 1.2.3.2. uid
Household UID.

#### 1.2.3.2.2. Type
VARCHAR

#### 1.2.3.2.3. Is Required
True

#### 1.2.3.2.4. Size
20

### 1.2.3.3. syncStatus
Synchronization status of the record.

#### 1.2.3.3.2. Type
VARCHAR

#### 1.2.3.3.3. Is Required
True

#### 1.2.3.3.4. Size
20

#### 1.2.3.3.5. Default Value
'Synced'

#### 1.2.3.3.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.2.3.4. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.2.3.4.2. Type
INTEGER

#### 1.2.3.4.3. Is Required
False

### 1.2.3.5. isDeleted
Flag for soft deletion.

#### 1.2.3.5.2. Type
BOOLEAN

#### 1.2.3.5.3. Is Required
True

#### 1.2.3.5.4. Default Value
false


### 1.2.4. Primary Keys

- id

### 1.2.5. Unique Constraints


### 1.2.6. Indexes


## 1.3. HouseholdMember
Local copy of household member data.

### 1.3.3. Attributes

### 1.3.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.3.3.1.2. Type
TEXT

#### 1.3.3.1.3. Is Required
True

#### 1.3.3.1.4. Is Primary Key
True

### 1.3.3.2. householdId
Foreign key linking to the local Household record.

#### 1.3.3.2.2. Type
TEXT

#### 1.3.3.2.3. Is Required
True

#### 1.3.3.2.4. Is Foreign Key
True

#### 1.3.3.2.5. References
Household.id

### 1.3.3.3. farmerId
Foreign key linking to the local Farmer record (if registered).

#### 1.3.3.3.2. Type
TEXT

#### 1.3.3.3.3. Is Required
False

#### 1.3.3.3.4. Is Foreign Key
True

#### 1.3.3.3.5. References
Farmer.id

### 1.3.3.4. relationshipToHead
Relationship to head.

#### 1.3.3.4.2. Type
VARCHAR

#### 1.3.3.4.3. Is Required
True

#### 1.3.3.4.4. Size
50

### 1.3.3.5. syncStatus
Synchronization status of the record.

#### 1.3.3.5.2. Type
VARCHAR

#### 1.3.3.5.3. Is Required
True

#### 1.3.3.5.4. Size
20

#### 1.3.3.5.5. Default Value
'Synced'

#### 1.3.3.5.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.3.3.6. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.3.3.6.2. Type
INTEGER

#### 1.3.3.6.3. Is Required
False

### 1.3.3.7. isDeleted
Flag for soft deletion.

#### 1.3.3.7.2. Type
BOOLEAN

#### 1.3.3.7.3. Is Required
True

#### 1.3.3.7.4. Default Value
false


### 1.3.4. Primary Keys

- id

### 1.3.5. Unique Constraints


### 1.3.6. Indexes


## 1.4. Farm
Local copy of farm data.

### 1.4.3. Attributes

### 1.4.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.4.3.1.2. Type
TEXT

#### 1.4.3.1.3. Is Required
True

#### 1.4.3.1.4. Is Primary Key
True

### 1.4.3.2. farmerId
Foreign key linking to the local Farmer record.

#### 1.4.3.2.2. Type
TEXT

#### 1.4.3.2.3. Is Required
False

#### 1.4.3.2.4. Is Foreign Key
True

#### 1.4.3.2.5. References
Farmer.id

### 1.4.3.3. householdId
Foreign key linking to the local Household record.

#### 1.4.3.3.2. Type
TEXT

#### 1.4.3.3.3. Is Required
False

#### 1.4.3.3.4. Is Foreign Key
True

#### 1.4.3.3.5. References
Household.id

### 1.4.3.4. name
Farm name.

#### 1.4.3.4.2. Type
VARCHAR

#### 1.4.3.4.3. Is Required
False

#### 1.4.3.4.4. Size
100

### 1.4.3.5. syncStatus
Synchronization status of the record.

#### 1.4.3.5.2. Type
VARCHAR

#### 1.4.3.5.3. Is Required
True

#### 1.4.3.5.4. Size
20

#### 1.4.3.5.5. Default Value
'Synced'

#### 1.4.3.5.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.4.3.6. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.4.3.6.2. Type
INTEGER

#### 1.4.3.6.3. Is Required
False

### 1.4.3.7. isDeleted
Flag for soft deletion.

#### 1.4.3.7.2. Type
BOOLEAN

#### 1.4.3.7.3. Is Required
True

#### 1.4.3.7.4. Default Value
false


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints


### 1.4.6. Indexes


## 1.5. Plot
Local copy of plot data, including location captured via device GPS.

### 1.5.3. Attributes

### 1.5.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.5.3.1.2. Type
TEXT

#### 1.5.3.1.3. Is Required
True

#### 1.5.3.1.4. Is Primary Key
True

### 1.5.3.2. farmId
Foreign key linking to the local Farm record.

#### 1.5.3.2.2. Type
TEXT

#### 1.5.3.2.3. Is Required
True

#### 1.5.3.2.4. Is Foreign Key
True

#### 1.5.3.2.5. References
Farm.id

### 1.5.3.3. size
Size of the plot (using REAL for floating point).

#### 1.5.3.3.2. Type
REAL

#### 1.5.3.3.3. Is Required
True

### 1.5.3.4. landTenureType
Land tenure type.

#### 1.5.3.4.2. Type
VARCHAR

#### 1.5.3.4.3. Is Required
True

#### 1.5.3.4.4. Size
50

### 1.5.3.5. primaryCrop
Primary crop.

#### 1.5.3.5.2. Type
VARCHAR

#### 1.5.3.5.3. Is Required
False

#### 1.5.3.5.4. Size
50

### 1.5.3.6. latitude
Latitude (using REAL for floating point, simpler than GEOMETRY for mobile).

#### 1.5.3.6.2. Type
REAL

#### 1.5.3.6.3. Is Required
True

### 1.5.3.7. longitude
Longitude (using REAL for floating point).

#### 1.5.3.7.2. Type
REAL

#### 1.5.3.7.3. Is Required
True

### 1.5.3.8. ownershipDetails
Ownership details.

#### 1.5.3.8.2. Type
TEXT

#### 1.5.3.8.3. Is Required
False

### 1.5.3.9. syncStatus
Synchronization status of the record.

#### 1.5.3.9.2. Type
VARCHAR

#### 1.5.3.9.3. Is Required
True

#### 1.5.3.9.4. Size
20

#### 1.5.3.9.5. Default Value
'Synced'

#### 1.5.3.9.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.5.3.10. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.5.3.10.2. Type
INTEGER

#### 1.5.3.10.3. Is Required
False

### 1.5.3.11. isDeleted
Flag for soft deletion.

#### 1.5.3.11.2. Type
BOOLEAN

#### 1.5.3.11.3. Is Required
True

#### 1.5.3.11.4. Default Value
false


### 1.5.4. Primary Keys

- id

### 1.5.5. Unique Constraints


### 1.5.6. Indexes

### 1.5.6.1. idx_mobile_plot_farm_id
Index on farm ID for retrieving plots belonging to a farm.

#### 1.5.6.1.2. Columns

- farmId

#### 1.5.6.1.3. Type
BTree

### 1.5.6.2. idx_mobile_plot_location
Basic index on location coordinates.

#### 1.5.6.2.2. Columns

- latitude
- longitude

#### 1.5.6.2.3. Type
BTree


## 1.6. AdministrativeArea
Subset of administrative area data needed for lookup/filtering on the device.

### 1.6.3. Attributes

### 1.6.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.6.3.1.2. Type
TEXT

#### 1.6.3.1.3. Is Required
True

#### 1.6.3.1.4. Is Primary Key
True

### 1.6.3.2. name
Name of the administrative area.

#### 1.6.3.2.2. Type
VARCHAR

#### 1.6.3.2.3. Is Required
True

#### 1.6.3.2.4. Size
100

### 1.6.3.3. type
Type of administrative area.

#### 1.6.3.3.2. Type
VARCHAR

#### 1.6.3.3.3. Is Required
True

#### 1.6.3.3.4. Size
20

### 1.6.3.4. parentId
Foreign key linking to the local parent administrative area.

#### 1.6.3.4.2. Type
TEXT

#### 1.6.3.4.3. Is Required
False

#### 1.6.3.4.4. Is Foreign Key
True

#### 1.6.3.4.5. References
AdministrativeArea.id


### 1.6.4. Primary Keys

- id

### 1.6.5. Unique Constraints


### 1.6.6. Indexes

### 1.6.6.1. idx_mobile_admin_area_parent_id
Index on parent ID for hierarchy navigation.

#### 1.6.6.1.2. Columns

- parentId

#### 1.6.6.1.3. Type
BTree


## 1.7. DynamicForm
Local copy of dynamic form templates needed for rendering forms offline.

### 1.7.3. Attributes

### 1.7.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.7.3.1.2. Type
TEXT

#### 1.7.3.1.3. Is Required
True

#### 1.7.3.1.4. Is Primary Key
True

### 1.7.3.2. name
Name of the dynamic form.

#### 1.7.3.2.2. Type
VARCHAR

#### 1.7.3.2.3. Is Required
True

#### 1.7.3.2.4. Size
100

### 1.7.3.3. version
Version identifier.

#### 1.7.3.3.2. Type
VARCHAR

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Size
10

### 1.7.3.4. status
Publication status.

#### 1.7.3.4.2. Type
VARCHAR

#### 1.7.3.4.3. Is Required
True

#### 1.7.3.4.4. Size
20


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints


### 1.7.6. Indexes


## 1.8. FormField
Local copy of form field definitions for dynamic forms.

### 1.8.3. Attributes

### 1.8.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.8.3.1.2. Type
TEXT

#### 1.8.3.1.3. Is Required
True

#### 1.8.3.1.4. Is Primary Key
True

### 1.8.3.2. formId
Foreign key linking to the local DynamicForm template.

#### 1.8.3.2.2. Type
TEXT

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

#### 1.8.3.2.5. References
DynamicForm.id

### 1.8.3.3. fieldType
Type of input field.

#### 1.8.3.3.2. Type
VARCHAR

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Size
20

### 1.8.3.4. label
Field label (localizable).

#### 1.8.3.4.2. Type
TEXT

#### 1.8.3.4.3. Is Required
True

### 1.8.3.5. isRequired
Indicates if required (0 for false, 1 for true).

#### 1.8.3.5.2. Type
INTEGER

#### 1.8.3.5.3. Is Required
True

### 1.8.3.6. validationRules
JSON string of validation rules.

#### 1.8.3.6.2. Type
TEXT

#### 1.8.3.6.3. Is Required
False

### 1.8.3.7. conditionalLogic
JSON string of conditional logic.

#### 1.8.3.7.2. Type
TEXT

#### 1.8.3.7.3. Is Required
False

### 1.8.3.8. order
Order of the field.

#### 1.8.3.8.2. Type
INTEGER

#### 1.8.3.8.3. Is Required
True

### 1.8.3.9. options
JSON string for select/multiselect options if applicable.

#### 1.8.3.9.2. Type
TEXT

#### 1.8.3.9.3. Is Required
False


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints


### 1.8.6. Indexes

### 1.8.6.1. idx_mobile_formfield_form_order
Index for retrieving fields for a form in order.

#### 1.8.6.1.2. Columns

- formId
- order

#### 1.8.6.1.3. Type
BTree


## 1.9. FormSubmission
Local records of completed dynamic forms, pending synchronization.

### 1.9.3. Attributes

### 1.9.3.1. id
Primary key (locally generated UUID or identifier).

#### 1.9.3.1.2. Type
TEXT

#### 1.9.3.1.3. Is Required
True

#### 1.9.3.1.4. Is Primary Key
True

### 1.9.3.2. serverId
Server-side UUID after successful synchronization.

#### 1.9.3.2.2. Type
TEXT

#### 1.9.3.2.3. Is Required
False

### 1.9.3.3. formId
Foreign key linking to the local DynamicForm template.

#### 1.9.3.3.2. Type
TEXT

#### 1.9.3.3.3. Is Required
True

#### 1.9.3.3.4. Is Foreign Key
True

#### 1.9.3.3.5. References
DynamicForm.id

### 1.9.3.4. farmerId
Foreign key linking to the local Farmer record.

#### 1.9.3.4.2. Type
TEXT

#### 1.9.3.4.3. Is Required
True

#### 1.9.3.4.4. Is Foreign Key
True

#### 1.9.3.4.5. References
Farmer.id

### 1.9.3.5. submissionDate
Unix timestamp when the form was submitted on the device.

#### 1.9.3.5.2. Type
INTEGER

#### 1.9.3.5.3. Is Required
True

### 1.9.3.6. status
Processing status on the mobile device.

#### 1.9.3.6.2. Type
VARCHAR

#### 1.9.3.6.3. Is Required
True

#### 1.9.3.6.4. Size
20

#### 1.9.3.6.5. Constraints

- CHECK (status IN ('Draft', 'PendingSync', 'Synced', 'SyncFailed'))

#### 1.9.3.6.6. Default Value
'Draft'

### 1.9.3.7. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.9.3.7.2. Type
INTEGER

#### 1.9.3.7.3. Is Required
False

### 1.9.3.8. errorMessage
Details of any error during sync.

#### 1.9.3.8.2. Type
TEXT

#### 1.9.3.8.3. Is Required
False


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints


### 1.9.6. Indexes

### 1.9.6.1. idx_mobile_formsubmission_farmer_form
Index for retrieving submissions by farmer and form.

#### 1.9.6.1.2. Columns

- farmerId
- formId

#### 1.9.6.1.3. Type
BTree


## 1.10. FormResponse
Local storage for field values within a form submission.

### 1.10.3. Attributes

### 1.10.3.1. id
Primary key (locally generated UUID or identifier).

#### 1.10.3.1.2. Type
TEXT

#### 1.10.3.1.3. Is Required
True

#### 1.10.3.1.4. Is Primary Key
True

### 1.10.3.2. serverId
Server-side UUID after successful synchronization.

#### 1.10.3.2.2. Type
TEXT

#### 1.10.3.2.3. Is Required
False

### 1.10.3.3. submissionId
Foreign key linking to the local FormSubmission.

#### 1.10.3.3.2. Type
TEXT

#### 1.10.3.3.3. Is Required
True

#### 1.10.3.3.4. Is Foreign Key
True

#### 1.10.3.3.5. References
FormSubmission.id

### 1.10.3.4. fieldId
Foreign key linking to the local FormField definition.

#### 1.10.3.4.2. Type
TEXT

#### 1.10.3.4.3. Is Required
True

#### 1.10.3.4.4. Is Foreign Key
True

#### 1.10.3.4.5. References
FormField.id

### 1.10.3.5. value
The submitted value for the field, stored as text.

#### 1.10.3.5.2. Type
TEXT

#### 1.10.3.5.3. Is Required
True

### 1.10.3.6. syncStatus
Synchronization status of the record.

#### 1.10.3.6.2. Type
VARCHAR

#### 1.10.3.6.3. Is Required
True

#### 1.10.3.6.4. Size
20

#### 1.10.3.6.5. Default Value
'Synced'

#### 1.10.3.6.6. Constraints

- CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'))

### 1.10.3.7. syncAttemptTimestamp
Unix timestamp of the last synchronization attempt.

#### 1.10.3.7.2. Type
INTEGER

#### 1.10.3.7.3. Is Required
False

### 1.10.3.8. isDeleted
Flag for soft deletion.

#### 1.10.3.8.2. Type
BOOLEAN

#### 1.10.3.8.3. Is Required
True

#### 1.10.3.8.4. Default Value
false


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints


### 1.10.6. Indexes

### 1.10.6.1. idx_mobile_formresponse_submission_field
Index for retrieving responses for a specific submission and field.

#### 1.10.6.1.2. Columns

- submissionId
- fieldId

#### 1.10.6.1.3. Type
BTree


## 1.11. User
Local copy of basic user data for authentication and role checks on the device.

### 1.11.3. Attributes

### 1.11.3.1. id
Primary key, stores the server-side UUID as text.

#### 1.11.3.1.2. Type
TEXT

#### 1.11.3.1.3. Is Required
True

#### 1.11.3.1.4. Is Primary Key
True

### 1.11.3.2. username
Username.

#### 1.11.3.2.2. Type
VARCHAR

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Size
50

### 1.11.3.3. role
User's high-level role.

#### 1.11.3.3.2. Type
VARCHAR

#### 1.11.3.3.3. Is Required
True

#### 1.11.3.3.4. Size
30

### 1.11.3.4. assignedAreaId
Foreign key linking to the local assigned administrative area.

#### 1.11.3.4.2. Type
TEXT

#### 1.11.3.4.3. Is Required
False

#### 1.11.3.4.4. Is Foreign Key
True

#### 1.11.3.4.5. References
AdministrativeArea.id


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints


### 1.11.6. Indexes


## 1.12. SyncQueueItem
Tracks data changes on the mobile device that need to be synchronized with the server.

### 1.12.3. Attributes

### 1.12.3.1. id
Local auto-incrementing primary key.

#### 1.12.3.1.2. Type
INTEGER

#### 1.12.3.1.3. Is Required
True

#### 1.12.3.1.4. Is Primary Key
True

### 1.12.3.2. entityName
Name of the entity to sync (e.g., 'Farmer', 'FormSubmission').

#### 1.12.3.2.2. Type
VARCHAR

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Size
50

### 1.12.3.3. entityId
ID (local PK) of the entity record to sync.

#### 1.12.3.3.2. Type
TEXT

#### 1.12.3.3.3. Is Required
True

### 1.12.3.4. operation
Type of operation to perform on the server.

#### 1.12.3.4.2. Type
VARCHAR

#### 1.12.3.4.3. Is Required
True

#### 1.12.3.4.4. Size
20

#### 1.12.3.4.5. Constraints

- CHECK (operation IN ('Create', 'Update', 'Delete'))

### 1.12.3.5. timestamp
Unix timestamp when the change occurred, used for ordering and conflict resolution.

#### 1.12.3.5.2. Type
INTEGER

#### 1.12.3.5.3. Is Required
True

### 1.12.3.6. status
Status of the sync queue item.

#### 1.12.3.6.2. Type
VARCHAR

#### 1.12.3.6.3. Is Required
True

#### 1.12.3.6.4. Size
20

#### 1.12.3.6.5. Default Value
'Pending'

#### 1.12.3.6.6. Constraints

- CHECK (status IN ('Pending', 'Processing', 'Completed', 'Failed', 'Conflict'))

### 1.12.3.7. attemptCount
Number of times synchronization has been attempted for this item.

#### 1.12.3.7.2. Type
INTEGER

#### 1.12.3.7.3. Is Required
True

#### 1.12.3.7.4. Default Value
0

### 1.12.3.8. errorMessage
Details of any error during sync processing for this item.

#### 1.12.3.8.2. Type
TEXT

#### 1.12.3.8.3. Is Required
False


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes

### 1.12.6.1. idx_mobile_syncqueue_status_ts
Index for processing pending items in chronological order.

#### 1.12.6.1.2. Columns

- status
- timestamp

#### 1.12.6.1.3. Type
BTree




---

# 2. Diagrams

- **Diagram_Title:** Core Entities (Farmer, Household, Farm, Plot, Geo)  
**Diagram_Area:** Farmer Registry, Land, Geo-Hierarchy  
**Explanation:** This diagram illustrates the core entities related to farmers, their households, landholdings (farms and plots), and the administrative geographical structure used for organization.  
**Mermaid_Text:** erDiagram
    Farmer {
        UUID id PK
        timestamp deletedAt
    }
    Household {
        UUID id PK
        timestamp deletedAt
    }
    HouseholdMember {
        UUID id PK
        UUID householdId FK "Household"
        UUID farmerId FK "Farmer"
    }
    Farm {
        UUID id PK
        UUID farmerId FK "Farmer"
        UUID householdId FK "Household"
        timestamp deletedAt
    }
    Plot {
        UUID id PK
        UUID farmId FK "Farm"
        timestamp deletedAt
    }
    AdministrativeArea {
        UUID id PK
        UUID parentId FK "AdministrativeArea"
    }

    Household ||--|{ HouseholdMember : "has member"
    Farmer ||--o{ HouseholdMember : "is member"
    Farmer ||--o{ Farm : "manages/owns"
    Household ||--o{ Farm : "associated with"
    Farm ||--|{ Plot : "has plot"
    AdministrativeArea ||--o{ AdministrativeArea : "parent"
  
- **Diagram_Title:** Data Collection (Forms, Submissions)  
**Diagram_Area:** Dynamic Forms, Submissions, Tags  
**Explanation:** This diagram focuses on the dynamic data collection mechanism, showing how form templates are defined, fields are structured, and how farmer submissions capture data, including tagging. It also links submissions back to the farmer entity.  
**Mermaid_Text:** erDiagram
    DynamicForm {
        UUID id PK
    }
    FormField {
        UUID id PK
        UUID formId FK "DynamicForm"
    }
    FormSubmission {
        UUID id PK
        UUID formId FK "DynamicForm"
        UUID farmerId FK "Farmer"
    }
    FormResponse {
        UUID id PK
        UUID submissionId FK "FormSubmission"
        UUID fieldId FK "FormField"
    }
    Tag {
        UUID id PK
    }
    FormTag {
        UUID formId PK,FK "DynamicForm"
        UUID tagId PK,FK "Tag"
    }
    %% Include Farmer definition as it's linked
    Farmer {
        UUID id PK
        timestamp deletedAt
    }

    DynamicForm ||--|{ FormField : "has field"
    DynamicForm ||--|{ FormSubmission : "has submission"
    Farmer ||--|{ FormSubmission : "submits"
    FormSubmission ||--|{ FormResponse : "has response"
    FormField ||--|{ FormResponse : "is response for"
    DynamicForm }|--|| { Tag : "tagged with"
    %% Explicit join table links are optional when using M-N symbol
    %% DynamicForm ||--|{ FormTag : "links to tag"
    %% Tag ||--|{ FormTag : "linked by form"
  
- **Diagram_Title:** System Users, Devices, Audit, Notifications  
**Diagram_Area:** User Management, Mobile Sync, Auditing, Notifications  
**Explanation:** This diagram shows system users, their assignment to administrative areas, associated mobile devices and sync sessions, the system audit trail, and standalone notifications.  
**Mermaid_Text:** erDiagram
    User {
        UUID id PK
        UUID assignedAreaId FK "AdministrativeArea"
        timestamp deletedAt
    }
    MobileDevice {
        UUID id PK
        UUID userId FK "User"
    }
    SyncSession {
        UUID id PK
        UUID deviceId FK "MobileDevice"
    }
    AuditLog {
        UUID id PK
        UUID userId FK "User"
    }
    Notification {
        UUID id PK
    }
    %% Include AdministrativeArea definition as it's linked
    AdministrativeArea {
        UUID id PK
        UUID parentId FK "AdministrativeArea"
    }

    User ||--|{ MobileDevice : "has device"
    MobileDevice ||--|{ SyncSession : "has session"
    User ||--|{ AuditLog : "performs action"
    AdministrativeArea ||--o{ User : "assigned area"
  


---

