from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class SmsSendRequest(BaseModel):
    recipient_phone: str = Field(..., description="Recipient's phone number in E.164 format.")
    message_body: str = Field(..., description="The content of the SMS message.")
    sender_id: Optional[str] = Field(None, description="Optional sender ID (alphanumeric).")
    # Add other common SMS parameters like `message_type` (e.g., 'text', 'unicode') if needed

class SmsSendResponse(BaseModel):
    message_sid: Optional[str] = Field(None, description="Unique message identifier from the gateway.")
    status: str = Field(..., description="Dispatch status (e.g., 'queued', 'sent', 'failed', 'delivered').")
    error_code: Optional[str] = Field(None, description="Gateway-specific error code if sending failed.")
    error_message: Optional[str] = Field(None, description="Human-readable error message if sending failed.")
    raw_response: Optional[dict] = Field(None, description="The raw response from the SMS gateway.")

class SmsProviderConfig(BaseModel):
    provider_name: str
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None # For Twilio account_sid, auth_token, etc.
    extra_config: Optional[Dict[str, Any]] = Field(None, description="Provider-specific extra configuration, e.g., {'default_sender_id': 'MyCompany'}")
    # Add other provider-specific fields