markdown
# Software Design Specification: DFR Notification System Module (dfr_notifications)

## 1. Introduction

This document outlines the software design for the Digital Farmer Registry (DFR) Notification System Module. This Odoo 18.0 Community addon is responsible for managing and dispatching automated notifications (SMS, email, push) based on system events and configurable templates. It integrates with third-party gateway services and is configured primarily through the Odoo Admin Portal by National Administrators.

**Current Repository Scope:** This SDS covers the `dfr_notifications` Odoo module. Its primary responsibilities include:
- Defining and managing notification templates.
- Configuring and managing notification gateway credentials and settings.
- Dispatching notifications based on system events and rules.
- Logging notification dispatch attempts.
- Providing administrative UIs for these functions.

**Key Requirements Addressed:**
- REQ-NS-001: Trigger-based alerts for system events.
- REQ-NS-003: Support for SMS, email, and potential push notification channels.
- REQ-NS-005: Management of notification templates with localization and dynamic placeholders.
- REQ-SYSADM-004: Configuration of notification system by National Administrators (triggers, templates, gateways).

## 2. System Architecture

The `dfr_notifications` module adheres to a **Modular Monolith** architecture, leveraging Odoo's inherent module system.

**Architectural Layers Involved:**
- **DFR Odoo Presentation Layer:** Provides UIs for administrators to manage templates and gateway configurations.
- **DFR Odoo Application Services Layer:** Contains the core logic for notification dispatch and template rendering.
- **DFR Integration Layer:** Facilitates communication with external notification gateway services (via `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS`).

**Dependencies:**
- `DFR_MOD_CORE_COMMON`: For shared utilities, base models, or configurations.
- `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS`: For actual communication with SMS/Email/Push gateways.
- Odoo `mail` module: For leveraging Odoo's default email sending capabilities if configured.
- Odoo `base` module: Standard Odoo dependency.

## 3. Data Design

The module introduces the following Odoo models:

### 3.1. `dfr.notification.template`
   - **Description:** Stores notification templates for different channels.
   - **Fields:**
     - `name` (Char, required): User-friendly name for the template (e.g., "Farmer Registration Welcome Email").
     - `technical_name` (Char, required, unique): A unique technical identifier for the template, used by automated actions to reference it (e.g., `farmer_registration_welcome_email`).
     - `channel_type` (Selection, required): Type of notification channel. Values: `[('email', 'Email'), ('sms', 'SMS'), ('push', 'Push Notification')]`.
     - `model_id` (Many2one `ir.model`, required): The Odoo model that provides the context for this template (e.g., `res.partner` for farmer, `dfr.registration.event`).
     - `model_name` (Char, related `model_id.model`, store=True): Technical name of the model, for easier reference.
     - `subject_template` (Text, translate=True): QWeb/Jinja2 template for the notification subject (primarily for email/push).
     - `body_template_qweb` (Text, translate=True, required): QWeb/Jinja2 template for the notification body. This field will be used for all channel types.
     - `lang` (Char): Optional language code (e.g., 'en_US'). If set, this template is specific to this language. If not set, it's a default template. The dispatch service will try to find a language-specific template first.
     - `gateway_config_id` (Many2one `dfr.notification.gateway.config`): Optional preferred gateway for this template. If not set, a default gateway for the channel type will be used.
     - `active` (Boolean, default=True): Whether the template is active and can be used.
   - **Methods:**
     - `render_template(self, record_ids)`:
       - **Input:** `record_ids` (list of integers or Odoo recordset for `model_id`): The records for which the template needs to be rendered.
       - **Output:** `dict`: A dictionary where keys are record IDs and values are tuples `(rendered_subject, rendered_body)`.
       - **Logic:** Iterates through `record_ids`. For each record, uses Odoo's QWeb rendering engine (`env['ir.qweb']._render()`) to render `subject_template` and `body_template_qweb` using the record as context. Handles potential rendering errors gracefully.
       - **Purpose:** To generate the actual notification content based on dynamic data from Odoo records.

### 3.2. `dfr.notification.gateway.config`
   - **Description:** Stores configuration and credentials for third-party notification gateways.
   - **Fields:**
     - `name` (Char, required): User-friendly name for the gateway configuration (e.g., "Country X Primary SMS Gateway").
     - `channel_type` (Selection, required): Type of notification channel this gateway serves. Values: `[('email', 'Email'), ('sms', 'SMS'), ('push', 'Push Notification')]`.
     - `provider_name` (Char): Name of the gateway provider (e.g., "Twilio", "SendGrid", "FCM", "Odoo Default Email"). This field can be used by `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` to select the appropriate connector logic.
     - `api_key` (Char, `password=True`): API key for the gateway. Odoo's `password=True` attribute obscures the value in the UI.
     - `api_secret` (Char, `password=True`): API secret or token for the gateway.
     - `base_url` (Char): Base URL for the gateway's API (if applicable).
     - `sender_id` (Char): Sender ID for SMS or push notifications.
     - `email_from` (Char): "From" email address for email notifications.
     - `is_odoo_default_email` (Boolean, default=False): If True, this configuration represents using Odoo's built-in email sending capabilities (via `mail.mail` model and configured mail servers). If so, other credential fields might be ignored.
     - `active` (Boolean, default=True): Whether this gateway configuration is active.
   - **Security Note:** While Odoo's `password=True` obscures fields in the UI, for production-grade security, sensitive credentials should ideally be stored in environment variables or a dedicated secrets management system, and accessed by the `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` module. This model provides the UI for configuration; the connectors module handles the secure retrieval and use.

### 3.3. `dfr.notification.log`
   - **Description:** Logs all notification dispatch attempts.
   - **Fields:**
     - `template_id` (Many2one `dfr.notification.template`, ondelete='set null'): The template used for the notification.
     - `recipient_partner_id` (Many2one `res.partner`, ondelete='set null'): The `res.partner` record of the recipient, if applicable.
     - `recipient_email` (Char): Email address of the recipient.
     - `recipient_phone` (Char): Phone number of the recipient.
     - `channel_type` (Selection, required): Channel used. Values from `dfr.notification.template`.
     - `gateway_config_id` (Many2one `dfr.notification.gateway.config`, ondelete='set null'): The gateway configuration used.
     - `subject` (Char): The rendered subject of the notification.
     - `body_preview` (Text): A preview or snippet of the rendered body (to avoid storing full sensitive content long-term if necessary, or store full if policy allows).
     - `status` (Selection, required): Dispatch status. Values: `[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed'), ('delivered', 'Delivered'), ('read', 'Read')]` (delivered/read statuses depend on gateway feedback capabilities).
     - `error_message` (Text): Any error message if dispatch failed.
     - `dispatch_timestamp` (Datetime, default=fields.Datetime.now, required): Timestamp of the dispatch attempt.
     - `related_record_model` (Char): Model name of the record that triggered the notification (e.g., `res.partner`).
     - `related_record_id` (Integer): ID of the record that triggered the notification.
     - `message_id_external` (Char): Optional: External message ID provided by the gateway.

## 4. Module Structure (`dfr_addons/dfr_notifications/`)


dfr_notifications/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── dfr_notification_template.py
│   ├── dfr_notification_gateway_config.py
│   └── dfr_notification_log.py
├── services/
│   ├── __init__.py
│   └── notification_dispatch_service.py
├── views/
│   ├── dfr_notification_template_views.xml
│   ├── dfr_notification_gateway_config_views.xml
│   ├── dfr_notification_log_views.xml
│   └── dfr_notifications_menus.xml
├── data/
│   ├── ir_actions_server_data.xml  # Example server actions for triggers
│   └── dfr_notification_template_data.xml # Example templates
├── security/
│   ├── ir.model.access.csv
│   └── dfr_notifications_groups.xml # Optional, if specific groups are needed
├── i18n/
│   └── dfr_notifications.pot
└── static/ # Optional: if any specific JS/CSS needed for views
    └── ...


## 5. Core Components and Logic

### 5.1. `notification_dispatch_service.py` (`dfr.notification.dispatch.service`)

This service is the heart of the notification system.

**Methods:**

- `send_notification_by_template_name(self, template_technical_name, record_id, recipient_partner_ids=None, recipient_emails=None, recipient_phones=None, force_channel_type=None, custom_context=None)`
    - **Purpose:** Primary public method to send a notification using a template's technical name.
    - **Logic:**
        1. Fetch the `dfr.notification.template` record by `template_technical_name`. If not found or inactive, log an error and return.
        2. Call `send_notification_by_template_id` with the fetched template object.
- `send_notification_by_template_id(self, template_obj, record_id, recipient_partner_ids=None, recipient_emails=None, recipient_phones=None, force_channel_type=None, custom_context=None)`
    - **Purpose:** Sends a notification using a direct template object.
    - **Logic:**
        1. **Input Validation:** Ensure `template_obj` is valid and `record_id` is provided.
        2. **Determine Recipients:**
           - If `recipient_partner_ids` (Odoo `res.partner` recordset) is provided, iterate through partners. Extract email/phone based on partner fields.
           - If `recipient_emails` (list of strings) is provided, use them.
           - If `recipient_phones` (list of strings) is provided, use them.
           - Ensure at least one recipient type is available based on `template_obj.channel_type` or `force_channel_type`.
        3. **Fetch Context Record:** `record = self.env[template_obj.model_id.model].browse(record_id)`
        4. **Iterate through Recipients:** For each resolved recipient:
           a. **Render Content:** Call `_render_template_content(template_obj, record, custom_context)` to get `rendered_subject`, `rendered_body`.
           b. **Determine Gateway:**
              - If `template_obj.gateway_config_id` is set and active, use it.
              - Else, find an active `dfr.notification.gateway.config` matching the `template_obj.channel_type` (or `force_channel_type`). Add logic for selecting a default/preferred gateway if multiple exist (e.g., sequence, specific flag).
              - If no suitable gateway is found, log an error for this recipient and continue.
           c. **Dispatch:** Call `_dispatch_via_channel(template_obj, gateway_config, rendered_subject, rendered_body, recipient_info)`. `recipient_info` should contain email or phone.
- `_render_template_content(self, template_obj, record, custom_context=None)`
    - **Purpose:** Renders subject and body of a template for a given record.
    - **Logic:**
        1. Prepare rendering context: `{'object': record, 'user': self.env.user, **(custom_context or {})}`.
        2. Render subject: `rendered_subject = self.env['ir.qweb']._render(template_obj.subject_template, rendering_context)` if `subject_template` exists. Handle `translate=True` field behavior by rendering in the appropriate language (e.g., recipient's lang if available, then template's `lang` field, then system default).
        3. Render body: `rendered_body = self.env['ir.qweb']._render(template_obj.body_template_qweb, rendering_context)`. Handle `translate=True` similar to subject.
        4. Return `(rendered_subject, rendered_body)`.
- `_dispatch_via_channel(self, template_obj, gateway_config, subject, body, recipient_info)`
    - **Purpose:** Calls the appropriate connector service from `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` or Odoo's mail system.
    - **Logic:**
        1. Determine `channel = template_obj.channel_type`.
        2. **If `channel == 'email'`:**
           - If `gateway_config.is_odoo_default_email` is True or no specific email gateway is configured to take precedence:
             - Use Odoo's `mail.mail` model:
               python
               mail_values = {
                   'subject': subject,
                   'body_html': body,
                   'email_to': recipient_info.get('email'),
                   'email_from': gateway_config.email_from or self.env['ir.mail_server']._get_default_bounce_address(),
                   # Add other relevant mail.mail fields
               }
               mail = self.env['mail.mail'].sudo().create(mail_values)
               mail.send()
               status = 'sent' # Assuming Odoo mail.mail send is synchronous or queues reliably
               error_message = None
               
             - Log the attempt via `_log_notification_attempt`.
           - Else (custom email gateway):
             - `status, error_message = self.env['dfr.email.connector'].send_email(gateway_config, recipient_info.get('email'), subject, body)`
             - Log the attempt.
        3. **If `channel == 'sms'`:**
           - `status, error_message = self.env['dfr.sms.connector'].send_sms(gateway_config, recipient_info.get('phone'), body)`
           - Log the attempt.
        4. **If `channel == 'push'`:**
           - `status, error_message = self.env['dfr.push.connector'].send_push(gateway_config, recipient_info.get('device_token'), subject, body, custom_payload_from_template_maybe)`
           - Log the attempt.
- `_log_notification_attempt(self, template_obj, recipient_info, gateway_config, status, error_message=None, subject=None, body_preview=None)`
    - **Purpose:** Logs the notification attempt to `dfr.notification.log`.
    - **Logic:**
        python
        log_values = {
            'template_id': template_obj.id,
            'recipient_partner_id': recipient_info.get('partner_id'),
            'recipient_email': recipient_info.get('email'),
            'recipient_phone': recipient_info.get('phone'),
            'channel_type': template_obj.channel_type,
            'gateway_config_id': gateway_config.id if gateway_config else None,
            'subject': subject,
            'body_preview': body_preview[:500] if body_preview else None, # Truncate for preview
            'status': status,
            'error_message': error_message,
            'related_record_model': template_obj.model_id.model,
            'related_record_id': recipient_info.get('record_id_context'), # Pass context record ID
        }
        self.env['dfr.notification.log'].sudo().create(log_values)
        

### 5.2. Odoo Automated Actions / Server Actions
   - **Purpose:** To trigger the `notification_dispatch_service` based on specific system events (e.g., farmer creation, status change).
   - **Configuration:** National Administrators will configure these via Odoo's UI (`Settings > Technical > Automation > Automated Actions` or `Server Actions`).
   - **Example `ir_actions_server_data.xml`:**
     xml
     <record id="action_notify_farmer_registration" model="ir.actions.server">
         <field name="name">Notify Farmer on Registration</field>
         <field name="model_id" ref="dfr_farmer_registry.model_dfr_farmer_profile"/> <!-- Example model -->
         <field name="state">code</field>
         <field name="code">
if records:
    # Assuming 'dfr_farmer_registration_welcome_email' is a technical_name of a template
    # and 'dfr_farmer_registration_welcome_sms' for SMS
    email_template_tech_name = 'dfr_farmer_registration_welcome_email'
    sms_template_tech_name = 'dfr_farmer_registration_welcome_sms'
    
    for record in records:
        # Send Email
        if record.email: # Check if farmer has an email
            env['dfr.notification.dispatch.service'].send_notification_by_template_name(
                email_template_tech_name,
                record.id,
                recipient_emails=[record.email]
            )
        # Send SMS
        if record.phone: # Check if farmer has a phone
             env['dfr.notification.dispatch.service'].send_notification_by_template_name(
                sms_template_tech_name,
                record.id,
                recipient_phones=[record.phone]
            )
         </field>
         <field name="trigger_id" eval="ref('model_dfr_farmer_profile_on_create')"/> <!-- Hypothetical trigger on create -->
     </record>
     
     *Note: The trigger mechanism needs to be defined properly based on Odoo's capabilities. A common way is to call server actions from overridden `create`/`write` methods of the base models if direct event triggers are not flexible enough.*
     A more robust approach might be to add specific methods to the core DFR models (e.g., `dfr_farmer_profile`) like `action_send_registration_notifications(self)` which then calls the dispatch service. These actions can then be called by automated actions or workflows.

### 5.3. Views and Menus (`views/`)
   - **`dfr_notification_template_views.xml`**:
     - Form view: Allows editing name, technical_name, channel_type, model_id, subject_template, body_template_qweb (using Odoo's HTML editor widget for rich text emails, or a simple text area for SMS/Push if preferred for simplicity), lang, active, gateway_config_id.
     - Tree view: Displays name, technical_name, channel_type, active.
     - Search view: Filter by name, channel_type.
   - **`dfr_notification_gateway_config_views.xml`**:
     - Form view: Fields for name, channel_type, provider_name, api_key (`widget="password"`), api_secret (`widget="password"`), base_url, sender_id, email_from, is_odoo_default_email, active.
     - Tree view: Displays name, channel_type, provider_name, active.
     - Search view: Filter by name, channel_type.
   - **`dfr_notification_log_views.xml`**:
     - Tree view (read-only focus): Displays dispatch_timestamp, recipient (computed preferred contact), channel_type, subject snippet, status.
     - Form view (read-only focus): Displays all log fields.
     - Search view: Filter by status, channel_type, date range, recipient.
   - **`dfr_notifications_menus.xml`**:
     - Main Menu: "DFR Notifications" (under main DFR app or Settings).
       - Sub-menu: "Templates" -> Action for `dfr.notification.template`.
       - Sub-menu: "Gateway Configurations" -> Action for `dfr.notification.gateway.config`.
       - Sub-menu: "Dispatch Logs" -> Action for `dfr.notification.log`.

### 5.4. Security (`security/`)
   - **`ir.model.access.csv`**:
     - `dfr.notification.template`: Full CRUD for National Admins (e.g., a group `dfr_common.group_dfr_national_administrator`). Read-only for other relevant admin/support roles if needed.
     - `dfr.notification.gateway.config`: Full CRUD for National Admins.
     - `dfr.notification.log`: Read-only for National Admins and Support roles. No create/write/delete for most users (logs created by system).
   - **`dfr_notifications_groups.xml`**: (Optional) If more granular control is needed than existing DFR groups, define groups like `group_dfr_notification_viewer` or `group_dfr_notification_manager`.

### 5.5. Default/Example Data (`data/`)
   - **`dfr_notification_template_data.xml`**:
     - Pre-define a few common templates:
       - Welcome email for new farmer registration.
       - SMS confirmation for new farmer registration.
       - Notification for self-registration received (to admin/supervisor).
       - Notification for farmer profile approval.
   - **`ir_actions_server_data.xml`**:
     - Example server actions demonstrating how to trigger the templates above, possibly linked to `on_create` or `on_write` of relevant models like `dfr.farmer_profile` or `dfr.self_registration_submission`. Administrators can then activate/customize these.

## 6. Integration Points

- **`DFR_MOD_CORE_COMMON`**: May provide base models or utility functions.
- **`DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS`**: This is a **critical dependency**. The `notification_dispatch_service` will invoke services/methods defined in this connectors module to actually send SMS, custom emails (non-Odoo default), and push notifications. The `dfr_notifications` module itself will **not** contain the direct API call logic to Twilio, SendGrid, FCM, etc. It only orchestrates and passes data to the connector.
    - **Expected Interface from `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS`:**
        - `self.env['dfr.sms.connector'].send_sms(gateway_config_obj, phone_number, message_body)` -> returns `(status, error_message_or_None)`
        - `self.env['dfr.email.connector'].send_email(gateway_config_obj, email_to, subject, html_body)` -> returns `(status, error_message_or_None)`
        - `self.env['dfr.push.connector'].send_push(gateway_config_obj, device_token_or_topic, title, body, data_payload=None)` -> returns `(status, error_message_or_None)`
- **Odoo Business Models (e.g., `dfr_farmer_registry.dfr_farmer_profile`)**: These models may have methods (e.g., `action_send_welcome_notification`) that are called by workflows/automated actions, which in turn call the `notification_dispatch_service`.
- **Odoo Automated Actions / Server Actions Framework**: Used by administrators to define event-driven triggers for notifications.

## 7. User Interface (Admin Portal)

- **Notification Template Management (DFR_MOD_NOTIF_TEMPLATE_ADMIN_VIEW):**
    - List view of all templates.
    - Form view to create/edit templates, including selection of channel, context model, QWeb/Jinja2 editor for subject and body, language selection, and preferred gateway.
- **Gateway Configuration Management (DFR_MOD_NOTIF_GATEWAY_CONFIG_ADMIN_VIEW):**
    - List view of configured gateways.
    - Form view to create/edit gateway configurations, including provider details, API credentials (masked), and channel type.
- **Notification Log Viewer:**
    - List view of notification logs, filterable and searchable.
    - Read-only form view showing details of a specific log entry.

## 8. Error Handling

- The `notification_dispatch_service` must gracefully handle errors during template rendering (e.g., invalid placeholders, QWeb errors) and during dispatch (e.g., gateway API errors returned by connectors, network issues).
- Errors should be logged in `dfr.notification.log` with meaningful messages.
- Failures in sending a notification should not typically roll back the primary transaction that triggered the notification (e.g., farmer registration should still succeed even if the welcome email fails to send). Consider using Odoo's job queue (`@job` decorator from `odoo.addons.queue_job`) for asynchronous dispatch of notifications to improve robustness and user experience if synchronous calls to gateways are slow or unreliable.

## 9. Localization

- All UI elements (views, field labels, messages) in this module will be translatable via `dfr_notifications.pot`.
- Notification template content (`subject_template`, `body_template_qweb`) will be translatable (`translate=True`). The `notification_dispatch_service` will attempt to render templates in the recipient's language if available, or the template's explicit language, or a system default.

## 10. Security Considerations

- **Access Control:** Strictly control access to template management and gateway configuration using Odoo groups (National Administrators). Log viewing access may be wider (Support roles).
- **Credential Storage:** While Odoo's `password=True` provides UI-level obscuring for `api_key` and `api_secret` in `dfr.notification.gateway.config`, the `DFR_MOD_EXTERNAL_INTEGRATION_CONNECTORS` module should be responsible for securely retrieving and using these, ideally from environment variables or a proper secrets management solution if the hosting environment supports it. Avoid logging full credentials.
- **Input Validation:** Validate inputs for template and gateway configurations.
- **QWeb/Jinja2 Security:** Ensure that template rendering context does not expose unintended methods or data that could be exploited if templates were somehow compromised or maliciously crafted. Use Odoo's standard rendering mechanisms which have some built-in safeguards.

## 11. Future Considerations (Optional)

- **Batching Notifications:** For high-volume scenarios, consider batching notifications to reduce load on gateways.
- **User Preferences:** Allow users (farmers via portal, system users via preferences) to opt-in/out of certain notification types or choose preferred channels.
- **Advanced Analytics on Logs:** Provide more detailed reporting on notification delivery rates, failures, etc.
- **Feedback Loop:** For gateways that support delivery/read receipts, update the `dfr.notification.log` status accordingly.
