import datetime
import enum

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"

class TemplateType(str, enum.Enum):
    birthday = "birthday"
    festival = "festival"
    campaign = "campaign"
    custom = "custom"

class CampaignStatus(str, enum.Enum):
    pending = "pending"
    scheduled = "scheduled"
    sent = "sent"
    failed = "failed"

class MessageStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    delivered = "delivered"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(256), nullable=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.staff)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    phone = Column(String(32), unique=True, nullable=False, index=True)
    email = Column(String(256), nullable=True)
    birthday = Column(Date, nullable=True)
    tags = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("Message", back_populates="customer")

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    type = Column(Enum(TemplateType), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    campaigns = relationship("Campaign", back_populates="template")

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=True)
    send_all = Column(Boolean, default=False)
    recipient_ids_raw = Column('recipient_ids', String(256), nullable=True)
    status = Column(Enum(CampaignStatus), nullable=False, default=CampaignStatus.pending)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    template = relationship("Template", back_populates="campaigns")
    messages = relationship("Message", back_populates="campaign")

    @property
    def recipient_ids(self) -> list[int]:
        return [int(value) for value in (self.recipient_ids_raw or "").split(",") if value]

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    content = Column(Text, nullable=False)
    event_type = Column(String(32), nullable=True)
    event_name = Column(String(128), nullable=True)
    status = Column(Enum(MessageStatus), default=MessageStatus.pending)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    customer = relationship("Customer", back_populates="messages")
    campaign = relationship("Campaign", back_populates="messages")

class Festival(Base):
    __tablename__ = "festivals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    template = relationship("Template")
