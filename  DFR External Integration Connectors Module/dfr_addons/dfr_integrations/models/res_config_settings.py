from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # National ID Validation Settings
    dfr_national_id_api_url = fields.Char(
        string="National ID API URL",
        config_parameter='dfr_integrations.national_id_api_url',
        help="Base URL for the National ID Validation API."
    )
    dfr_national_id_api_key = fields.Char(
        string="National ID API Key",
        config_parameter='dfr_integrations.national_id_api_key',
        help="API Key for the National ID Validation Service."
    )
    dfr_national_id_api_timeout = fields.Integer(
        string="National ID API Timeout (s)",
        config_parameter='dfr_integrations.national_id_api_timeout',
        default=10,
        help="Timeout in seconds for National ID API requests."
    )

    # SMS Gateway Settings
    dfr_sms_gateway_provider = fields.Selection(
        string="SMS Gateway Provider",
        config_parameter='dfr_integrations.sms_gateway_provider',
        selection=[
            ('none', 'None (Disable External SMS)'),
            ('twilio', 'Twilio'),
            ('vonage', 'Vonage (Placeholder)'), # Add actual providers as implemented
            ('other', 'Other (Manual Config)')
        ],
        default='none',
        help="Select the SMS gateway provider."
    )
    # Twilio Specific (example)
    dfr_sms_twilio_account_sid = fields.Char(
        string="Twilio Account SID",
        config_parameter='dfr_integrations.sms_twilio_account_sid'
    )
    dfr_sms_twilio_auth_token = fields.Char(
        string="Twilio Auth Token",
        config_parameter='dfr_integrations.sms_twilio_auth_token',
        help="Authentication token for Twilio." # Added help for clarity
    )
    dfr_sms_twilio_api_url = fields.Char( 
        string="Twilio API Base URL",
        config_parameter='dfr_integrations.sms_twilio_api_url',
        help="Optional: Override Twilio API base URL. E.g., https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID. If not set, service may construct default."
    )
    dfr_sms_twilio_default_sender_id = fields.Char(
        string="Twilio Default Sender ID/Number",
        config_parameter='dfr_integrations.sms_twilio_default_sender_id',
        help="Default 'From' phone number or Alphanumeric Sender ID for Twilio." # Added help
    )
    
    # Generic 'Other' SMS provider settings
    dfr_sms_gateway_url = fields.Char(
        string="Other SMS Gateway URL",
        config_parameter='dfr_integrations.sms_gateway_url',
        help="Base URL if 'Other' provider is selected." # Added help
    )
    dfr_sms_gateway_api_key = fields.Char(
        string="Other SMS Gateway API Key",
        config_parameter='dfr_integrations.sms_gateway_api_key',
        help="API Key if 'Other' provider is selected." # Added help
    )
    dfr_sms_gateway_secret = fields.Char(
        string="Other SMS Gateway Secret/Token",
        config_parameter='dfr_integrations.sms_gateway_secret',
        help="API Secret or Token if 'Other' provider is selected." # Added help
    )
    dfr_sms_gateway_timeout = fields.Integer(
        string="SMS Gateway Timeout (s)",
        config_parameter='dfr_integrations.sms_gateway_timeout',
        default=10,
        help="General timeout in seconds for SMS gateway requests." # Added help
    )

    # Email Gateway Settings
    dfr_email_gateway_provider = fields.Selection(
        string="Email Gateway Provider",
        config_parameter='dfr_integrations.email_gateway_provider',
        selection=[
            ('odoo', 'Odoo Default Mail Server'),
            ('sendgrid', 'SendGrid'),
            # ('mailgun', 'Mailgun (Placeholder)'), # Add actual providers
            ('other', 'Other (Manual Config)')
        ],
        default='odoo',
        help="Select the Email gateway provider. 'Odoo Default' uses built-in Odoo mail servers configured under Settings."
    )
    # SendGrid Specific (example)
    dfr_email_sendgrid_api_key = fields.Char(
        string="SendGrid API Key",
        config_parameter='dfr_integrations.email_sendgrid_api_key',
        help="API Key for SendGrid integration." # Added help
    )
    dfr_email_sendgrid_api_url = fields.Char(
        string="SendGrid API Base URL",
        config_parameter='dfr_integrations.email_sendgrid_api_url',
        default='https://api.sendgrid.com/v3',
        help="Base URL for the SendGrid API."
    )
    
    dfr_default_email_from = fields.Char(
        string="Default 'From' Email Address (Integrations)",
        config_parameter='dfr_integrations.default_email_from',
        help="Default sender email address for messages sent via DFR integrations if not specified per message. This can override Odoo's system default email if set."
    )
    dfr_email_gateway_timeout = fields.Integer(
        string="Email Gateway Timeout (s)",
        config_parameter='dfr_integrations.email_gateway_timeout',
        default=15,
        help="General timeout in seconds for email gateway requests." # Added help
    )

    # Placeholder for Weather Service Config
    dfr_weather_service_api_url = fields.Char(
        string="Weather Service API URL", 
        config_parameter='dfr_integrations.weather_api_url',
        help="Base URL for the Weather Service API."
    )
    dfr_weather_service_api_key = fields.Char(
        string="Weather Service API Key", 
        config_parameter='dfr_integrations.weather_api_key',
        help="API Key for the Weather Service API."
    )
    dfr_weather_service_timeout = fields.Integer(
        string="Weather Service Timeout (s)",
        config_parameter='dfr_integrations.weather_api_timeout', # As per inferred logic
        default=10,
        help="Timeout in seconds for Weather Service API requests."
    )
    
    # Placeholder for Payment Platform Config
    dfr_payment_platform_api_url = fields.Char(
        string="Payment Platform API URL", 
        config_parameter='dfr_integrations.payment_api_url',
        help="Base URL for the Payment Platform API."
    )
    dfr_payment_platform_api_key = fields.Char(
        string="Payment Platform API Key", 
        config_parameter='dfr_integrations.payment_api_key',
        help="API Key for the Payment Platform."
    )
    dfr_payment_platform_secret_key = fields.Char(
        string="Payment Platform Secret Key", 
        config_parameter='dfr_integrations.payment_secret_key',
        help="Secret key for the Payment Platform (if applicable)."
    )
    dfr_payment_platform_timeout = fields.Integer(
        string="Payment Platform Timeout (s)",
        config_parameter='dfr_integrations.payment_api_timeout', # As per inferred logic
        default=20,
        help="Timeout in seconds for Payment Platform API requests."
    )