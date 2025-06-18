from .base_client import BaseApiClient
from .national_id_api_client import NationalIdApiClient
from .sms_gateway_client_interface import SmsGatewayClientInterface
from .sms_twilio_client import SmsTwilioClient
# Import other SMS clients (e.g., Vonage) if implemented
from .email_gateway_client_interface import EmailGatewayClientInterface
from .email_sendgrid_client import EmailSendGridClient
# Import other Email clients if implemented
from .weather_service_client import WeatherServiceClient # Placeholder
from .payment_platform_client import PaymentPlatformClient # Placeholder