from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=8)
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    tags: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    phone: Optional[str] = Field(None, min_length=8)
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    tags: Optional[str] = None

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class TemplateBase(BaseModel):
    name: str
    type: str
    body: str

class TemplateCreate(TemplateBase):
    pass

class TemplateRead(TemplateBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class CampaignBase(BaseModel):
    name: str
    template_id: int
    send_all: bool = False
    recipient_ids: Optional[List[int]] = None
    scheduled_at: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignRead(CampaignBase):
    id: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class MessageBase(BaseModel):
    customer_id: int
    campaign_id: Optional[int] = None
    content: str
    event_type: Optional[str] = None
    event_name: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    status: str
    timestamp: datetime

    model_config = {
        "from_attributes": True,
    }

class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: Optional[EmailStr] = None
    role: str = Field(...)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class FestivalBase(BaseModel):
    name: str
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    template_id: int
    active: bool = True

class FestivalCreate(FestivalBase):
    pass

class FestivalRead(FestivalBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class DashboardMetrics(BaseModel):
    total_customers: int
    total_messages: int
    sent_messages: int
    delivered_messages: int
    failed_messages: int
    total_campaigns: int
    scheduled_campaigns: int
