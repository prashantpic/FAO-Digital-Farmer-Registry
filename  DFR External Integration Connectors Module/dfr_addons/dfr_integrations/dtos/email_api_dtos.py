from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

class EmailAttachmentDTO(BaseModel):
    filename: str
    content_base64: str # Base64 encoded content
    content_type: str # MIME type

class EmailSendRequest(BaseModel):
    to_email: List[EmailStr] = Field(..., description="List of recipient email addresses.")
    from_email: EmailStr = Field(..., description="Sender email address.")
    reply_to_email: Optional[EmailStr] = Field(None, description="Optional reply-to email address.")
    subject: str = Field(..., description="Email subject.")
    html_body: Optional[str] = Field(None, description="HTML content of the email.")
    text_body: Optional[str] = Field(None, description="Plain text content of the email.")
    attachments: Optional[List[EmailAttachmentDTO]] = Field(None, description="List of attachments.")
    # Add cc, bcc if needed

class EmailSendResponse(BaseModel):
    message_id: Optional[str] = Field(None, description="Unique message identifier from the gateway.")
    status: str = Field(..., description="Dispatch status (e.g., 'accepted', 'sent', 'failed').")
    error_message: Optional[str] = Field(None, description="Error message if sending failed.")
    raw_response: Optional[dict] = Field(None, description="The raw response from the email gateway.")

class EmailProviderConfig(BaseModel):
    provider_name: str
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None # Some email providers might use a secret
    extra_config: Optional[Dict[str, Any]] = Field(None, description="Provider-specific extra configuration.")
    # Add other provider-specific fields