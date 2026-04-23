from datetime import datetime, date
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas

# User management

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_any_user(db: Session):
    return db.query(models.User).first()


def create_user(db: Session, username: str, email: str | None, role: str, hashed_password: str):
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Customers

def get_customer_by_phone(db: Session, phone: str):
    return db.query(models.Customer).filter(models.Customer.phone == phone).first()


def get_customer(db: Session, customer_id: int):
    return db.get(models.Customer, customer_id)


def get_customers(db: Session, skip: int = 0, limit: int = 100, search: str | None = None, tag: str | None = None):
    query = db.query(models.Customer)
    if search:
        query = query.filter(
            models.Customer.name.ilike(f"%{search}%")
            | models.Customer.phone.ilike(f"%{search}%")
            | models.Customer.email.ilike(f"%{search}%")
        )
    if tag:
        query = query.filter(models.Customer.tags.ilike(f"%{tag}%"))
    return query.offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer: models.Customer, customer_update: schemas.CustomerUpdate):
    for field, value in customer_update.model_dump(exclude_none=True).items():
        setattr(customer, field, value)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = db.get(models.Customer, customer_id)
    if customer:
        db.delete(customer)
        db.commit()

# Templates

def get_templates(db: Session, skip: int = 0, limit: int = 100, template_type: str | None = None):
    query = db.query(models.Template)
    if template_type:
        query = query.filter(models.Template.type == template_type)
    return query.offset(skip).limit(limit).all()


def get_template_by_type(db: Session, template_type: str):
    return db.query(models.Template).filter(models.Template.type == template_type).order_by(models.Template.created_at.desc()).first()


def get_template(db: Session, template_id: int):
    return db.get(models.Template, template_id)


def create_template(db: Session, template: schemas.TemplateCreate):
    db_template = models.Template(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

# Campaigns

def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).order_by(models.Campaign.created_at.desc()).offset(skip).limit(limit).all()


def get_campaign(db: Session, campaign_id: int):
    return db.get(models.Campaign, campaign_id)


def create_campaign(db: Session, campaign: schemas.CampaignCreate):
    recipient_ids = None
    if campaign.recipient_ids:
        recipient_ids = ",".join(str(customer_id) for customer_id in campaign.recipient_ids)
    db_campaign = models.Campaign(
        name=campaign.name,
        template_id=campaign.template_id,
        scheduled_at=campaign.scheduled_at,
        send_all=campaign.send_all,
        recipient_ids_raw=recipient_ids,
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


def update_campaign_status(db: Session, campaign: models.Campaign, status: str):
    campaign.status = status
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def get_scheduled_campaigns(db: Session):
    return db.query(models.Campaign).filter(
        models.Campaign.status == models.CampaignStatus.scheduled,
        models.Campaign.scheduled_at <= datetime.utcnow(),
    ).all()

# Messages

def get_messages(
    db: Session,
    customer_id: int | None = None,
    campaign_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Message)
    if customer_id is not None:
        query = query.filter(models.Message.customer_id == customer_id)
    if campaign_id is not None:
        query = query.filter(models.Message.campaign_id == campaign_id)
    return query.order_by(models.Message.timestamp.desc()).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemas.MessageCreate, status: str = "pending"):
    db_message = models.Message(**message.model_dump(), status=status, timestamp=datetime.utcnow())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_customer_messages(db: Session, customer_id: int):
    return get_messages(db, customer_id=customer_id)


def get_todays_birthdays(db: Session, today: date | None = None):
    today = today or date.today()
    customers = db.query(models.Customer).filter(models.Customer.birthday.isnot(None)).all()
    return [cust for cust in customers if cust.birthday.month == today.month and cust.birthday.day == today.day]


def get_festivals(db: Session):
    return db.query(models.Festival).order_by(models.Festival.month, models.Festival.day).all()


def get_active_festivals(db: Session, today: date | None = None):
    today = today or date.today()
    return db.query(models.Festival).filter(models.Festival.active == True).all()


def get_dashboard_metrics(db: Session) -> schemas.DashboardMetrics:
    total_customers = db.query(func.count(models.Customer.id)).scalar() or 0
    total_messages = db.query(func.count(models.Message.id)).scalar() or 0
    sent_messages = db.query(func.count(models.Message.id)).filter(models.Message.status == models.MessageStatus.sent).scalar() or 0
    delivered_messages = db.query(func.count(models.Message.id)).filter(models.Message.status == models.MessageStatus.delivered).scalar() or 0
    failed_messages = db.query(func.count(models.Message.id)).filter(models.Message.status == models.MessageStatus.failed).scalar() or 0
    total_campaigns = db.query(func.count(models.Campaign.id)).scalar() or 0
    scheduled_campaigns = db.query(func.count(models.Campaign.id)).filter(models.Campaign.status == models.CampaignStatus.scheduled).scalar() or 0
    return schemas.DashboardMetrics(
        total_customers=total_customers,
        total_messages=total_messages,
        sent_messages=sent_messages,
        delivered_messages=delivered_messages,
        failed_messages=failed_messages,
        total_campaigns=total_campaigns,
        scheduled_campaigns=scheduled_campaigns,
    )


def send_campaign_messages(db: Session, campaign: models.Campaign):
    template = campaign.template
    if not template:
        campaign.status = models.CampaignStatus.failed
        db.add(campaign)
        db.commit()
        return

    if campaign.scheduled_at and campaign.scheduled_at > datetime.utcnow():
        campaign.status = models.CampaignStatus.scheduled
        db.add(campaign)
        db.commit()
        return

    if campaign.send_all:
        customers = db.query(models.Customer).all()
    else:
        customer_ids = [int(value) for value in (campaign.recipient_ids or "").split(",") if value]
        customers = db.query(models.Customer).filter(models.Customer.id.in_(customer_ids)).all()

    any_failed = False
    for customer in customers:
        content = render_template(template.body, {"name": customer.name, "date": datetime.utcnow().strftime("%Y-%m-%d")})
        result = send_whatsapp_message(customer.phone, content)
        status_value = "sent" if result.get("success") else "failed"
        if not result.get("success"):
            any_failed = True
        message_schema = schemas.MessageCreate(
            customer_id=customer.id,
            campaign_id=campaign.id,
            content=content,
            event_type="campaign",
            event_name=campaign.name,
        )
        create_message(db, message_schema, status=status_value)

    campaign.status = models.CampaignStatus.failed if any_failed else models.CampaignStatus.sent
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
