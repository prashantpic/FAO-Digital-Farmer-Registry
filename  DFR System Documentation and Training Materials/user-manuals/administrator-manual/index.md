# DFR Administrator Manual

## 1. Introduction

Welcome to the Digital Farmer Registry (DFR) System Administrator Manual. This guide is designed for **National Administrators** and **Super Administrators** who are responsible for managing, configuring, and overseeing their country's DFR instance.

This manual provides comprehensive instructions on various administrative tasks, system settings, user management, and other key functionalities available in the DFR Odoo backend.

**Target Audience:** National Administrators, Super Administrators, IT Support Staff involved in DFR system management.
*Req IDs: B.3.B1.13, C.1.1*

## 2. Administrator Role Overview

As a DFR System Administrator, your key responsibilities typically include:

*   **User Management:** Creating and managing user accounts, assigning roles and permissions.
*   **Dynamic Form Management:** Designing, configuring, and deploying dynamic forms for data collection.
*   **Business Rule Configuration:** Setting up and managing workflows, de-duplication rules, and notification triggers.
*   **System Configuration:** Managing country-specific settings, administrative hierarchies, and localization.
*   **Data Management:** Overseeing data quality, performing bulk operations (import/export), and assisting with data migration validation.
*   **Analytics and Reporting:** Accessing system dashboards, generating reports, and managing custom views.
*   **System Monitoring:** Basic monitoring of system health and audit logs.
*   **Support:** Providing first-level support to other users within your organization.
*   **Farmer Self-Service Portal Management:** Enabling or disabling the portal and managing related configurations.

This manual will guide you through performing these tasks effectively.

## 3. Table of Contents

This manual is organized into the following sections:

1.  **[Introduction](./01-introduction.md)**
    *   Administrator Role and Responsibilities
    *   Navigating the DFR Admin Dashboard
2.  **[User Management](./02-user-management.md)**
    *   Creating New Users
    *   Assigning Roles and Permissions
    *   Managing User Groups
    *   Password Policies and Resetting Passwords
    *   Multi-Factor Authentication (MFA) Setup and Management
    *   Deactivating and Reactivating Users
3.  **[Dynamic Form Builder](./03-dynamic-form-builder.md)**
    *   Accessing the Form Builder
    *   Creating a New Form
    *   Adding and Configuring Field Types (Text, Number, Date, Select, GPS, etc.)
    *   Setting Up Validation Rules
    *   Implementing Conditional Logic (Show/Hide Fields)
    *   Form Versioning and Publishing
    *   Managing Existing Forms
4.  **[Business Rule Configuration](./04-business-rules-config.md)**
    *   Workflow Management (e.g., Farmer Registration Approval)
    *   De-duplication Rule Configuration
    *   Status Management for Entities (e.g., Farmer, Household)
5.  **[Notification System](./05-notification-system.md)**
    *   Managing Notification Templates (Email, SMS)
    *   Configuring Notification Triggers
    *   Setting up Communication Gateways (Email Server, SMS Gateway)
6.  **[Analytics and Reporting](./06-analytics-reporting.md)**
    *   Accessing Standard Dashboards
    *   Generating Predefined Reports
    *   Creating Custom Views and Filters
    *   Exporting Data for Analysis
7.  **[Data Management](./07-data-management.md)**
    *   Bulk Data Import (e.g., Farmers, Administrative Areas)
    *   Bulk Data Export
    *   Data Migration Validation Procedures (Overview)
    *   Data Archival and Purging (Policies and Procedures)
8.  **[Localization and Country Settings](./08-localization-settings.md)**
    *   Managing Language Packs and Translations
    *   Configuring Country-Specific Parameters (e.g., UID format, currency)
    *   Managing Administrative Hierarchies
9.  **[System Monitoring and Logs](./09-system-monitoring-logs.md)**
    *   Accessing and Reviewing Audit Logs
    *   Basic System Health Checks
    *   Understanding Key Performance Indicators (KPIs)
10. **[Farmer Self-Service Portal Management](./10-portal-management.md)**
    *   Enabling/Disabling the Farmer Portal
    *   Configuring Portal Access Rules
    *   [Placeholder: Further details based on portal features]
11. **[Troubleshooting and Support](./11-troubleshooting-support.md)**
    *   Common Issues and Solutions
    *   How to Escalate Issues

---
Use the navigation pane on the left to jump to specific sections. If you are new to DFR administration, it is recommended to read through the sections sequentially.

For any terms you are unfamiliar with, please refer to the [Project Glossary](../../glossary.md).