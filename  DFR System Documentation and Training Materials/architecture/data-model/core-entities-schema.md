# Core Entities Schema (Odoo Data Model)

## 1. Introduction
This document outlines the schema for the core data entities within the Digital Farmer Registry (DFR) system. These entities are primarily implemented as Odoo models. The purpose of this document is to provide a reference for developers, data administrators, and technical analysts.
*Req IDs: A.3.3, E.1.4*

!!! info "Note on Odoo Fields"
    Odoo automatically adds several fields to all models (e.g., `id`, `create_date`, `create_uid`, `write_date`, `write_uid`, `display_name`). These are not explicitly listed for each model below unless they have a specific overridden behavior or significance in the DFR context. UUIDs are planned for key entities for external referencing, which may be stored in a dedicated `uuid` field if not using Odoo's default ID for this.

## 2. Core Entities

### 2.1 Farmer (`dfr.farmer`)
*   **Purpose:** Represents an individual farmer registered in the system.
*   **Key Fields:**
    | Field Name (Technical) | Type          | Constraints / Notes                                     | Description                                     | Business Name        |
    |------------------------|---------------|---------------------------------------------------------|-------------------------------------------------|----------------------|
    | `uuid`                 | `Char`        | Indexed, Unique, Readonly after creation                | Globally unique identifier for external use     | Farmer UUID          |
    | `uid`                  | `Char`        | Indexed, Unique (per country context), Required         | Farmer Unique Identifier (human-readable)       | Farmer ID            |
    | `name`                 | `Char`        | Required                                                | Full name of the farmer                         | Full Name            |
    | `first_name`           | `Char`        |                                                         | First name(s)                                   | First Name           |
    | `last_name`            | `Char`        |                                                         | Last name                                       | Last Name            |
    | `date_of_birth`        | `Date`        |                                                         | Date of birth                                   | Date of Birth        |
    | `sex`                  | `Selection`   | `[('male', 'Male'), ('female', 'Female'), ('other', 'Other')]` | Biological sex or gender identity               | Sex / Gender         |
    | `national_id_type_id`  | `Many2one`    | `dfr.national.id.type`                                  | Type of national identification document        | National ID Type     |
    | `national_id_number`   | `Char`        |                                                         | National identification number                  | National ID Number   |
    | `contact_phone`        | `Char`        |                                                         | Primary contact phone number                    | Contact Phone        |
    | `contact_email`        | `Char`        |                                                         | Primary contact email address                   | Contact Email        |
    | `photo`                | `Binary`      |                                                         | Farmer's photograph                             | Photo                |
    | `address_text`         | `Text`        |                                                         | Full address as text                            | Address              |
    | `admin_area_id`        | `Many2one`    | `dfr.administrative.area`                               | Lowest administrative area farmer belongs to    | Administrative Area  |
    | `household_id`         | `Many2one`    | `dfr.household`                                         | Household the farmer belongs to                 | Household            |
    | `is_household_head`    | `Boolean`     | Default: False                                          | Is this farmer the head of their household?     | Head of Household    |
    | `registration_date`    | `Date`        | Default: Today, Required                                | Date of registration in DFR                     | Registration Date    |
    | `status`               | `Selection`   | `[('draft', 'Draft'), ('pending_approval', 'Pending Approval'), ('active', 'Active'), ('inactive', 'Inactive'), ('rejected', 'Rejected')]` | Registration status                             | Status               |
    | `farm_ids`             | `One2many`    | `dfr.farm`, inverse_name=`farmer_id`                    | Farms associated with this farmer               | Farms                |
    | `submission_ids`       | `One2many`    | `dfr.form.submission`, inverse_name=`farmer_id`       | Form submissions made by/for this farmer      | Submissions          |
    | `active`               | `Boolean`     | Default: True (Odoo specific for archiving)             | Active status in Odoo                           | Active               |
    | `notes`                | `Text`        |                                                         | General notes about the farmer                  | Notes                |
    | `[Placeholder: Other country-specific KYC fields]` | `Various`   |                                                         | [Placeholder: e.g., marital status, education]  |                      |

### 2.2 Household (`dfr.household`)
*   **Purpose:** Represents a household unit, which may contain one or more farmers/members.
*   **Key Fields:**
    | Field Name (Technical) | Type          | Constraints / Notes                                     | Description                                     | Business Name        |
    |------------------------|---------------|---------------------------------------------------------|-------------------------------------------------|----------------------|
    | `uuid`                 | `Char`        | Indexed, Unique, Readonly after creation                | Globally unique identifier for external use     | Household UUID       |
    | `uid`                  | `Char`        | Indexed, Unique (per country context), Required         | Household Unique Identifier                     | Household ID         |
    | `name`                 | `Char`        | Computed (e.g., "Household of [Head's Name]") or manual | Name or identifier for the household            | Household Name       |
    | `head_farmer_id`       | `Many2one`    | `dfr.farmer`, `domain="[('is_household_head', '=', True), ('household_id', '=', id)]"` | The designated head of the household            | Head of Household    |
    | `member_ids`           | `One2many`    | `dfr.farmer`, inverse_name=`household_id`               | Farmers belonging to this household             | Members              |
    | `farm_ids`             | `One2many`    | `dfr.farm`, inverse_name=`household_id`                 | Farms associated with this household (collective) | Household Farms      |
    | `admin_area_id`        | `Many2one`    | `dfr.administrative.area`                               | Lowest administrative area household is in      | Administrative Area  |
    | `registration_date`    | `Date`        | Default: Today, Required                                | Date of household registration                  | Registration Date    |
    | `status`               | `Selection`   | `[('active', 'Active'), ('inactive', 'Inactive')]`      | Status of the household                         | Status               |
    | `[Placeholder: Other household specific fields]` | `Various`   |                                                         | [Placeholder: e.g., household income level]     |                      |

### 2.3 Farm (`dfr.farm`)
*   **Purpose:** Represents a distinct farm managed by a farmer or household. A farm can contain multiple plots.
*   **Key Fields:**
    | Field Name (Technical) | Type          | Constraints / Notes                                     | Description                                     | Business Name        |
    |------------------------|---------------|---------------------------------------------------------|-------------------------------------------------|----------------------|
    | `uuid`                 | `Char`        | Indexed, Unique, Readonly after creation                | Globally unique identifier for external use     | Farm UUID            |
    | `name`                 | `Char`        | Required                                                | Name or identifier for the farm                 | Farm Name/ID         |
    | `farmer_id`            | `Many2one`    | `dfr.farmer`                                            | Primary farmer associated with this farm        | Farmer (Owner/Mgr)   |
    | `household_id`         | `Many2one`    | `dfr.household`                                         | Household associated with this farm (if collective) | Household            |
    | `total_area`           | `Float`       | Computed from sum of plot areas, `digits='DFR Area'`    | Total area of the farm                          | Total Area           |
    | `plot_ids`             | `One2many`    | `dfr.plot`, inverse_name=`farm_id`                      | Plots belonging to this farm                    | Plots                |
    | `admin_area_id`        | `Many2one`    | `dfr.administrative.area`                               | Lowest administrative area farm is located in   | Administrative Area  |
    | `primary_activity_id`  | `Many2one`    | `dfr.farm.activity.type`                                | Main agricultural activity on the farm          | Primary Activity     |
    | `[Placeholder: Other farm specific fields]` | `Various`   |                                                         | [Placeholder: e.g., land ownership type for farm] |                      |

### 2.4 Plot (`dfr.plot`)
*   **Purpose:** Represents a specific parcel of land within a farm.
*   **Key Fields:**
    | Field Name (Technical) | Type          | Constraints / Notes                                     | Description                                     | Business Name        |
    |------------------------|---------------|---------------------------------------------------------|-------------------------------------------------|----------------------|
    | `uuid`                 | `Char`        | Indexed, Unique, Readonly after creation                | Globally unique identifier for external use     | Plot UUID            |
    | `name`                 | `Char`        | Required                                                | Name or identifier for the plot                 | Plot Name/ID         |
    | `farm_id`              | `Many2one`    | `dfr.farm`, Required, OnDelete='cascade'                | Farm this plot belongs to                       | Farm                 |
    | `area_hectares`        | `Float`       | `digits='DFR Area'`, Required                           | Area of the plot in hectares                    | Area (Hectares)      |
    | `land_tenure_type_id`  | `Many2one`    | `dfr.land.tenure.type`                                  | Land tenure system for this plot                | Land Tenure Type     |
    | `soil_type_id`         | `Many2one`    | `dfr.soil.type`                                         | Predominant soil type                           | Soil Type            |
    | `primary_crop_id`      | `Many2one`    | `dfr.crop.type`                                         | Main crop cultivated on this plot               | Primary Crop         |
    | `gps_polygon`          | `Text`        | Store as GeoJSON string or similar for KML/WKT          | GPS coordinates defining the plot boundary (polygon) | GPS Polygon        |
    | `gps_centroid_lat`     | `Float`       | `digits=(10, 7)`                                        | GPS Latitude of plot centroid                   | GPS Latitude         |
    | `gps_centroid_lon`     | `Float`       | `digits=(10, 7)`                                        | GPS Longitude of plot centroid                  | GPS Longitude        |
    | `[Placeholder: Other plot specific fields]` | `Various`   |                                                         | [Placeholder: e.g., irrigation type, last soil test date] |        |

### 2.5 Administrative Area (`dfr.administrative.area`)
*   **Purpose:** Represents a geographical administrative unit (e.g., Region, District, Village). Forms a hierarchy.
*   **Key Fields:**
    | Field Name (Technical) | Type          | Constraints / Notes                                     | Description                                     | Business Name        |
    |------------------------|---------------|---------------------------------------------------------|-------------------------------------------------|----------------------|
    | `name`                 | `Char`        | Required                                                | Name of the administrative area                 | Name                 |
    | `code`                 | `Char`        | Indexed, Unique (within parent or globally - TBD)       | Official code for the administrative area       | Code                 |
    | `level_type_id`        | `Many2one`    | `dfr.admin.area.level.type`, Required                   | Type/Level of this administrative area          | Level/Type           |
    | `parent_id`            | `Many2one`    | `dfr.administrative.area`, OnDelete='restrict'          | Parent administrative area in the hierarchy     | Parent Area          |
    | `child_ids`            | `One2many`    | `dfr.administrative.area`, inverse_name=`parent_id`     | Child administrative areas                      | Sub-Areas            |

### 2.6 Supporting Reference Models
These models provide selectable options for fields in the core entities. Examples:

*   **`dfr.national.id.type`**: (e.g., Passport, National ID Card, Voter ID)
    *   `name` (Char, Required)
    *   `code` (Char)
*   **`dfr.admin.area.level.type`**: (e.g., Country, Region, District, Ward, Village)
    *   `name` (Char, Required)
    *   `level_order` (Integer, Required, for sorting hierarchy)
*   **`dfr.land.tenure.type`**: (e.g., Owned, Leased, Customary)
    *   `name` (Char, Required)
*   **`dfr.crop.type`**: (e.g., Maize, Rice, Cassava)
    *   `name` (Char, Required)
    *   `is_cash_crop` (Boolean)
*   **`dfr.soil.type`**: (e.g., Loam, Clay, Sandy)
    *   `name` (Char, Required)
*   **`dfr.farm.activity.type`**: (e.g., Crop Production, Livestock, Aquaculture)
    *   `name` (Char, Required)

`[Placeholder: Full list and details for all supporting reference models]`

## 3. Relationships and ERD
The relationships are primarily defined using Odoo's `Many2one`, `One2many`, and `Many2many` field types as described above.

A high-level ERD illustrating these core entities and their primary relationships:
```mermaid
erDiagram
    Farmer ||--o{ Farm : "manages/owns"
    Farmer }o--|| Household : "is_member_of (optional)"
    Household ||--o{ Farm : "associated_with (collective)"
    Household ||--|{ Farmer : "has_head (optional)"
    Farm ||--|{ Plot : "contains"
    Farmer ||--o{ FormSubmission : "submits"
    DynamicForm ||--o{ FormSubmission : "instance_of"
    Plot ||--o{ AdministrativeArea : "located_in (lowest)"
    Farm ||--o{ AdministrativeArea : "located_in (lowest)"
    Household ||--o{ AdministrativeArea : "located_in (lowest)"
    Farmer ||--o{ AdministrativeArea : "resides_in (lowest)"
    AdministrativeArea ||--o{ AdministrativeArea : "parent_of (hierarchy)"

    Farmer {
        string uuid PK
        string uid UK
        string name
        date date_of_birth
        string sex
        string national_id_number
        fk admin_area_id
        fk household_id
        bool is_household_head
    }
    Household {
        string uuid PK
        string uid UK
        fk head_farmer_id
        fk admin_area_id
    }
    Farm {
        string uuid PK
        string name
        fk farmer_id
        fk household_id
        fk admin_area_id
    }
    Plot {
        string uuid PK
        string name
        fk farm_id
        float area_hectares
        string gps_polygon
        fk admin_area_id_plot "Lowest admin area of plot"
    }
    AdministrativeArea {
        string id PK
        string name
        string code UK
        fk parent_id
        fk level_type_id
    }
    FormSubmission {
        string id PK
        fk farmer_id
        fk dynamic_form_id
        datetime submission_date
    }
    DynamicForm {
        string id PK
        string name
    }
```
*Note: This Mermaid ERD is a simplified representation. Odoo handles primary keys (typically `id` as integer) automatically. `uuid` fields are custom additions for external referencing. `UK` denotes a unique key consideration.*

`[Placeholder: Link to more detailed, tool-generated ERDs if available, e.g., from an SQL design tool or Odoo ERD generator - assets/images/dfr_core_entities_erd.png]`

## 4. Key Business Rules
*   A Farmer `uid` must be unique.
*   A Household `uid` must be unique.
*   A Farmer can belong to at most one Household.
*   A Household should typically have one designated `head_farmer_id` from its members.
*   Administrative Areas form a strict hierarchy.
*   [Placeholder: List other critical business rules enforced at the data model level, e.g., validation rules for specific fields, inter-entity constraints.]

## 5. Data Types and Units
*   **Area:** Standard unit is hectares (ha). Odoo `Float` fields for area should use `digits` precision suitable for this (e.g., `digits='DFR Area'` which could be defined globally as `(12, 4)`).
*   **GPS Coordinates:** Stored as `Float` with sufficient precision (e.g., 7 decimal places for lat/lon). Polygons stored as text (GeoJSON recommended).
*   **Dates:** Stored as Odoo `Date` or `Datetime` fields as appropriate.

This schema is subject to refinement during the detailed design and implementation phases.
See also:
*   [Dynamic Forms Schema](./dynamic-forms-schema.md)
*   [Audit Log Schema](./audit-log-schema.md)