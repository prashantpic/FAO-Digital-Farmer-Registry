# DFR Codebase Governance Framework

## 1. Introduction
This document outlines the governance framework for managing the Digital Farmer Registry (DFR) shared codebase, which primarily consists of Odoo modules and potentially mobile application source code. The framework aims to ensure consistency, quality, maintainability, and collaboration across different development teams and country deployments.
*Req IDs: A.3.2*

## 2. Core Principles
*   **Shared Core, Localized Extensions:** A central, robust core DFR codebase will be maintained, providing common functionalities. Country-specific requirements will be met through configurable parameters or separate, well-defined extension modules.
*   **Collaboration and Transparency:** Open communication and transparent processes are key. All changes to the core codebase will be subject to review.
*   **Quality First:** Emphasis on robust coding standards, thorough testing, and comprehensive documentation.
*   **Sustainability:** Practices that ensure the long-term health and adaptability of the codebase.

## 3. Codebase Architecture
*   **Core DFR Modules (Shared):**
    *   A set of Odoo addons that implement the fundamental features of DFR (e.g., `dfr_farmer_registry`, `dfr_dynamic_forms`, `dfr_api`).
    *   These modules are intended to be used across all country deployments.
    *   Changes to these modules require a stringent review process.
*   **Country-Specific Configuration Modules:**
    *   Separate Odoo addons or configuration files (e.g., XML data files) that handle localization aspects like administrative hierarchies, specific form templates initially, language translations, and initial user roles for a particular country.
    *   These typically depend on the core DFR modules.
*   **Country-Specific Extension Modules (If Necessary):**
    *   For unique functionalities required by a specific country that cannot be met by configuring the core modules.
    *   These should be developed with care to minimize divergence from the core and ensure upgradability.
    *   The architecture should strive to incorporate common functionalities back into the core if applicable to multiple countries.
*   **Mobile Application Codebase:**
    *   If a single mobile app codebase is used, country-specific configurations might be managed via backend API responses or build flavors.
    *   `[Placeholder: Details on mobile app codebase governance if it involves shared components vs. forked versions]`

## 4. Branching Strategy (Git)
A standardized branching strategy based on **GitFlow** (or a simplified version like GitHub Flow) is recommended.

*   **`main` (or `master`):**
    *   Represents the latest stable, production-ready version of the core codebase.
    *   Only receives merges from `develop` (for releases) or hotfix branches.
    *   Tagged for releases (e.g., `v1.0.0`, `v1.1.0`).
*   **`develop`:**
    *   The primary integration branch for ongoing development of the next release.
    *   All feature branches are merged into `develop`.
    *   Nightly builds or CI builds run against this branch.
*   **Feature Branches (`feature/<feature-name>` or `feat/<feature-name>`):**
    *   Created from `develop` for new features or significant changes.
    *   Example: `feature/farmer-deduplication-enhancement`.
    *   Merged back into `develop` via Pull/Merge Requests.
*   **Release Branches (`release/<version-number>`):**
    *   Branched from `develop` when preparing for a new production release.
    *   Used for final testing, bug fixing, and documentation updates for that release.
    *   Once ready, merged into `main` (and tagged) and back into `develop` (to incorporate any last-minute fixes).
    *   Example: `release/v1.1.0`.
*   **Hotfix Branches (`hotfix/<issue-identifier>` or `fix/<issue-identifier>`):**
    *   Branched from `main` to address critical bugs in production.
    *   Once fixed and tested, merged back into both `main` (and tagged) and `develop` (or active release branch).
    *   Example: `hotfix/login-bug-prod`.
*   **Country-Specific Branches (for configuration/extensions):**
    *   May be maintained for country-specific modules, branching off tagged core releases to ensure stability.
    *   Strategy: `[Placeholder: Define strategy for managing country-specific module branches and their relation to core releases. E.g., country/<country_code>/develop based on core/release/vx.y.z]`

## 5. Versioning Policy
**Semantic Versioning 2.0.0 (SemVer)** (e.g., `MAJOR.MINOR.PATCH`) will be used for the core DFR software.

*   **MAJOR version (X.y.z):** Incremented for incompatible API changes or significant architectural changes.
*   **MINOR version (x.Y.z):** Incremented for new functionalities added in a backward-compatible manner.
*   **PATCH version (x.y.Z):** Incremented for backward-compatible bug fixes.

Releases will be tagged in Git (e.g., `git tag -a v1.0.0 -m "Version 1.0.0"`).

## 6. Contribution Model & Code Review
1.  **Issue Tracking:**
    *   All bugs, feature requests, and tasks related to the core codebase will be managed in a designated issue tracker (e.g., Jira, GitHub Issues, GitLab Issues).
    *   `[Placeholder: Specify the chosen issue tracking system and project board]`
2.  **Development Workflow:**
    *   Developers pick an issue from the tracker.
    *   Create a feature branch from `develop` (or appropriate base).
    *   Implement the changes, adhering to [Coding Standards](./../standards/coding-standards.md) and [Documentation Standards](./../standards/documentation-standards.md).
    *   Write/update unit tests.
    *   Ensure all tests pass locally.
3.  **Pull/Merge Request (PR/MR):**
    *   Push the feature branch to the central repository.
    *   Create a PR/MR targeting the `develop` branch.
    *   The PR/MR description should clearly explain the changes, link to the relevant issue, and include testing notes.
4.  **Code Review:**
    *   At least one other developer (preferably a senior developer or technical lead) must review the PR/MR.
    *   Reviewers check for:
        *   Correctness and completeness of the solution.
        *   Adherence to coding standards and best practices.
        *   Potential performance or security issues.
        *   Adequacy of tests.
        *   Clarity of code and comments.
        *   Impact on other parts of the system.
    *   Feedback is provided via comments on the PR/MR. The original developer addresses the feedback and pushes updates.
5.  **Automated Checks (CI):**
    *   The CI pipeline should automatically run linters, build the code, and execute automated tests on each PR/MR.
    *   PR/MRs can only be merged if all CI checks pass.
6.  **Merging:**
    *   Once reviewed, approved, and CI checks pass, the PR/MR is merged into `develop` (typically using a "squash and merge" or "rebase and merge" strategy to keep history clean).
    *   The original feature branch is then deleted.

## 7. Maintenance Plan
*   **Bug Fixes:** Prioritized based on severity and impact. Hotfixes for critical production issues. Regular patch releases for non-critical bugs.
*   **Security Patches:** Applied promptly as vulnerabilities are discovered in Odoo core or dependencies.
*   **Dependency Updates:** Regular review and updates of third-party libraries and Odoo itself (for minor/patch versions within Odoo 18.0).
*   **Refactoring:** Periodic refactoring to improve code quality, performance, and maintainability, scheduled as needed.

## 8. Update/Deployment Policy for Country Instances
*   Country instances should run stable, tagged releases of the core DFR software.
*   Updates to new MINOR or MAJOR versions should be planned carefully, involving testing on a staging environment specific to that country.
*   PATCH releases can generally be applied more frequently, but still require testing.
*   A clear communication plan must be in place for informing national counterparts about upcoming updates and any potential impact.
*   `[Placeholder: Detailed procedures for rolling out updates to country instances, including data migration considerations if any.]`

## 9. Guidelines for Country-Specific Extensions
*   **Necessity Review:** Before creating a country-specific extension module, a thorough analysis must confirm that the requirement cannot be met through configuration of the core modules.
*   **Naming Conventions:** Country-specific modules should follow a clear naming convention (e.g., `dfr_xx_<feature_name>`, where `xx` is the country code).
*   **Dependency Management:** Extensions should clearly define their dependency on specific versions of the core DFR modules.
*   **Minimize Core Overrides:** Avoid directly overriding core DFR module methods or views. Prefer using Odoo's inheritance mechanisms (`_inherit`), server actions, or well-defined extension points (hooks/APIs if provided by core).
*   **Documentation:** Country-specific extensions must be documented, explaining their purpose, functionality, and any specific configurations.
*   **Contribution Back to Core:** If a country-specific feature is deemed beneficial for other countries, a process should be in place to adapt and integrate it into the core DFR modules.

## 10. Repository Management
*   **Access Control:** Define roles (e.g., Read, Write, Maintainer, Admin) for repository access.
*   **Protected Branches:** `main` and `develop` branches should be protected, requiring PR/MRs and reviews for changes.
*   `[Placeholder: Link to the specific Git repository URL]`

This governance framework is a living document and may be updated as the DFR project evolves.