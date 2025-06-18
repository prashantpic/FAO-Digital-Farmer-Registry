from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class NationalIdValidationRequest(BaseModel):
    id_number: str = Field(..., description="The National ID number to validate.")
    id_type: str = Field(..., description="The type of National ID (e.g., 'PASSPORT', 'NATIONAL_CARD').")
    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code.")
    # Add any other parameters required by the specific National ID API

class NationalIdValidationResponse(BaseModel):
    is_valid: bool = Field(..., description="Whether the ID is considered valid.")
    full_name: Optional[str] = Field(None, description="Validated full name associated with the ID.")
    date_of_birth: Optional[date] = Field(None, description="Validated date of birth.")
    # Include other validated fields like gender, address components if provided by API
    raw_response: Optional[dict] = Field(None, description="The raw response from the external API for debugging.")
    error_message: Optional[str] = Field(None, description="Error message if validation failed or an error occurred.")
    error_code: Optional[str] = Field(None, description="Specific error code from the external API.")