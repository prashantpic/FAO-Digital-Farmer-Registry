# DFR Open Source Declaration

## 1. Introduction
This document provides a declaration of the primary open-source license under which the Digital Farmer Registry (DFR) software is made available. It also lists key third-party open-source components, libraries, and frameworks utilized in the DFR system, along with their respective licenses. This declaration aims to ensure transparency and compliance with open-source licensing obligations.

This document is intended for legal teams, FAO, national counterparts, developers, and any stakeholder interested in the licensing aspects of the DFR software.
*Req IDs: A.3.6*

## 2. Primary DFR Software License
The Digital Farmer Registry (DFR) core custom-developed software components (e.g., custom Odoo modules, mobile application source code developed specifically for DFR) are licensed under the:

**[Placeholder: Choose one and remove the other - e.g., Apache License 2.0 OR MIT License]**

*   **Apache License 2.0:**
    *   A permissive free software license written by the Apache Software Foundation (ASF).
    *   Allows users to use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software under the terms of the license, without concern for royalties.
    *   Requires preservation of copyright notices and disclaimers.
    *   Provides an express grant of patent rights from contributors to users.
    *   Full license text: [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

*Or (if MIT is chosen):*

*   **MIT License:**
    *   A permissive free software license originating at the Massachusetts Institute of Technology (MIT).
    *   Permits reuse within proprietary software provided that all copies of the licensed software include a copy of the MIT License terms and the copyright notice.
    *   It is simple and widely used.
    *   Full license text: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

!!! important "License Choice"
    The final choice between Apache 2.0 and MIT (or another suitable open-source license) will be confirmed by the project steering committee and legal advisors. The `LICENSE` file in the root of the DFR source code repositories will contain the full text of the chosen license.

## 3. Third-Party Open-Source Components
The DFR system leverages several third-party open-source components. The following table lists key dependencies. This is not exhaustive and will be complemented by a detailed Software Bill of Materials (SBOM).

| Component Name                 | Version (Example) | License                                       | Link to License                                       | Used In        | Notes                                          |
|--------------------------------|-------------------|-----------------------------------------------|-------------------------------------------------------|----------------|------------------------------------------------|
| **Backend (Odoo & Python)**    |                   |                                               |                                                       |                |                                                |
| Odoo Community Edition         | 18.0              | LGPL-3.0 (GNU Lesser General Public License)  | [https://www.gnu.org/licenses/lgpl-3.0.html](https://www.gnu.org/licenses/lgpl-3.0.html) | Odoo Backend   | Core ERP framework.                            |
| Python                         | 3.11.x            | Python Software Foundation License (PSFL)     | [https://docs.python.org/3/license.html](https://docs.python.org/3/license.html) | Odoo Backend   | Programming language for Odoo.                 |
| PostgreSQL                     | 15.x / 16.x       | PostgreSQL License (Permissive, MIT-like)     | [https://www.postgresql.org/about/licence/](https://www.postgresql.org/about/licence/) | Database       | Primary database for Odoo.                     |
| Werkzeug                       | `[Odoo's version]`| BSD-3-Clause License                          | [https://github.com/pallets/werkzeug/blob/main/LICENSE.rst](https://github.com/pallets/werkzeug/blob/main/LICENSE.rst) | Odoo Backend   | WSGI utility library used by Odoo.             |
| Requests                       | `[Odoo's version]`| Apache License 2.0                            | [https://github.com/psf/requests/blob/main/LICENSE](https://github.com/psf/requests/blob/main/LICENSE) | Odoo Backend   | HTTP library for Python, used by Odoo.         |
| psycopg2 / psycopg (binary)    | `[Odoo's version]`| LGPL-3.0 or later (source), various (binary)  | [https://www.psycopg.org/docs/license.html](https://www.psycopg.org/docs/license.html) | Odoo Backend   | PostgreSQL adapter for Python.                 |
| `[Placeholder: Other key Python libraries used by custom DFR Odoo modules]` | `x.y.z`           | `[License Name]`                              | `[Link to License]`                                   | Odoo Backend   | `[Purpose]`                                    |
| **Frontend (Odoo Web)**        |                   |                                               |                                                       |                |                                                |
| Owl (Odoo Web Library)         | `[Odoo's version]`| MIT License                                   | Part of Odoo, generally MIT for JS components.        | Odoo Frontend  | Odoo's frontend framework.                     |
| Bootstrap                      | `[Odoo's version]`| MIT License                                   | [https://github.com/twbs/bootstrap/blob/main/LICENSE](https://github.com/twbs/bootstrap/blob/main/LICENSE) | Odoo Frontend  | Used by Odoo's web client.                     |
| jQuery                         | `[Odoo's version]`| MIT License                                   | [https://jquery.org/license/](https://jquery.org/license/)                         | Odoo Frontend  | Used by Odoo's web client (legacy parts).      |
| **Mobile Application**         |                   |                                               |                                                       |                |                                                |
| `[Placeholder: Android SDK parts]` | `various`         | Apache License 2.0 (primarily for AOSP)       | [https://source.android.com/docs/setup/about/licenses](https://source.android.com/docs/setup/about/licenses) | Mobile App     | If native Android.                             |
| `[Placeholder: Key Android libraries, e.g., Retrofit, Room, Glide]` | `x.y.z`           | `[License Name]`                              | `[Link to License]`                                   | Mobile App     | `[Purpose]`                                    |
| `[Placeholder: Flutter Framework]` | `x.y.z`           | BSD-style license                             | [https://github.com/flutter/flutter/blob/master/LICENSE](https://github.com/flutter/flutter/blob/master/LICENSE) | Mobile App     | If Flutter is used.                            |
| `[Placeholder: Key Dart/Flutter packages]` | `x.y.z`           | `[License Name]`                              | `[Link to License]`                                   | Mobile App     | `[Purpose]`                                    |
| **Documentation Portal**       |                   |                                               |                                                       |                |                                                |
| MkDocs                         | 1.6.0             | BSD-2-Clause License                          | [https://github.com/mkdocs/mkdocs/blob/master/LICENSE.md](https://github.com/mkdocs/mkdocs/blob/master/LICENSE.md) | Docs Portal    | Static site generator.                         |
| Material for MkDocs            | 9.5.x             | MIT License                                   | [https://github.com/squidfunk/mkdocs-material/blob/master/LICENSE](https://github.com/squidfunk/mkdocs-material/blob/master/LICENSE) | Docs Portal    | Theme for MkDocs.                              |
| `[Placeholder: Other MkDocs plugins]` | `x.y.z`           | `[License Name]`                              | `[Link to License]`                                   | Docs Portal    | `[Purpose]`                                    |

`[Placeholder: This table will be populated more extensively as development progresses and a full SBOM is generated. Include libraries for GIS, image handling, reporting, etc., as they are chosen and integrated.]`

## 4. License Compatibility
A review of the licenses of third-party components has been conducted to ensure compatibility with the primary DFR software license and with each other. The DFR project aims to use permissive licenses (e.g., MIT, Apache 2.0, BSD) where possible to simplify compliance.

*   **LGPL-3.0 (from Odoo):** The LGPL license allows linking with software under other licenses (including proprietary ones or more permissive open-source licenses like Apache 2.0/MIT for custom DFR modules). If DFR custom modules are licensed under Apache 2.0 or MIT, this is compatible with linking against Odoo (LGPL). Modifications to Odoo's core LGPL-licensed code would need to be released under LGPL.
*   Other permissive licenses (MIT, BSD, Apache 2.0) are generally compatible with each other.

`[Placeholder: Add a more detailed statement on license compatibility review and any specific considerations or obligations arising from the licenses used, e.g., regarding distribution of source code for LGPL components if modifications are made to them.]`

## 5. Software Bill of Materials (SBOM)
A detailed Software Bill of Materials (SBOM) will be maintained and made available, providing a comprehensive list of all software components, their versions, licenses, and suppliers. The SBOM will be generated using industry-standard formats (e.g., SPDX, CycloneDX).

`[Placeholder: Link to the location of the latest SBOM document or generation process, e.g., /docs/sbom/dfr-sbom-latest.json]`

## 6. Copyright Notices
Copyright notices for the DFR custom-developed software will be maintained in the source code files. Copyright notices of third-party components are preserved as required by their respective licenses.

---

This document is for informational purposes. For the exact terms and conditions, please refer to the full license texts linked above and in the respective software components. If you have questions regarding licensing, please contact the DFR project team.