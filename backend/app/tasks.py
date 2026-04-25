from datetime import date, datetime
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal
from .whatsapp_client import render_template, send_whatsapp_message

scheduler = None


def send_birthday_notifications():
    with SessionLocal() as db:
        template = crud.get_template_by_type(db, models.TemplateType.birthday)
        if not template:
            return
        customers = crud.get_todays_birthdays(db)
        today = date.today()
        for customer in customers:
            if customer.birthday and customer.birthday.month == today.month and customer.birthday.day == today.day:
                content = render_template(
                    template.body,
                    {
                        "name": customer.name,
                        "date": customer.birthday.strftime("%Y-%m-%d") if customer.birthday else today.strftime("%Y-%m-%d"),
                    },
                )
                result = send_whatsapp_message(customer.phone, content)
                status = "sent" if result.get("success") else "failed"
                message_schema = crud.schemas.MessageCreate(
                    customer_id=customer.id,
                    content=content,
                    event_type="birthday",
                    event_name="Birthday",
                )
                crud.create_message(db, message_schema, status=status)


def send_festival_notifications():
    with SessionLocal() as db:
        festivals = crud.get_festivals(db)
        today = date.today()
        for festival in festivals:
            if festival.active and festival.month == today.month and festival.day == today.day:
                template = festival.template
                if not template:
                    continue
                customers = db.query(models.Customer).all()
                for customer in customers:
                    content = render_template(
                        template.body,
                        {
                            "name": customer.name,
                            "date": today.strftime("%Y-%m-%d"),
                        },
                    )
                    result = send_whatsapp_message(customer.phone, content)
                    status = "sent" if result.get("success") else "failed"
                    message_schema = crud.schemas.MessageCreate(
                        customer_id=customer.id,
                        content=content,
                        event_type="festival",
                        event_name=festival.name,
                    )
                    crud.create_message(db, message_schema, status=status)


def run_scheduled_campaigns():
    with SessionLocal() as db:
        campaigns = crud.get_scheduled_campaigns(db)
        for campaign in campaigns:
            crud.send_campaign_messages(db, campaign)


def start_scheduler() -> None:
    global scheduler
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_birthday_notifications, "cron", hour=0, minute=5)
        scheduler.add_job(send_festival_notifications, "cron", hour=0, minute=10)
        scheduler.add_job(run_scheduled_campaigns, "interval", minutes=5)
        scheduler.start()
        print("Scheduler started successfully")
    except ImportError as e:
        print(f"Warning: APScheduler not available ({e}). Scheduled tasks will not run. Background jobs disabled.")
