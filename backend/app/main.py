from datetime import datetime
import os
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user_optional,
    get_password_hash,
    oauth2_scheme,
)
from .database import SessionLocal, engine
from .tasks import start_scheduler
from .whatsapp_client import render_template, send_whatsapp_message

models.Base.metadata.create_all(bind=engine)

from .config import settings

app = FastAPI(title="Customer Engagement & WhatsApp Automation API")
allowed_origins = ["http://localhost:5173"]
if settings.frontend_url and settings.frontend_url not in allowed_origins:
    allowed_origins.append(settings.frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    start_scheduler()
    db = SessionLocal()
    try:
        if crud.get_any_user(db) is None:
            hashed_password = get_password_hash("admin123")
            crud.create_user(db, "admin", None, models.UserRole.admin, hashed_password)
            print("Created default admin user: admin / admin123")
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_current_user_optional),
):
    first_user = crud.get_any_user(db) is None
    if not first_user and (current_user is None or current_user.role != models.UserRole.admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(db, user.username, user.email, user.role, hashed_password)

@app.post("/customers", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if crud.get_customer_by_phone(db, customer.phone):
        raise HTTPException(status_code=400, detail="Customer with this phone already exists.")
    return crud.create_customer(db, customer)

@app.get("/customers", response_model=list[schemas.CustomerRead])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    tag: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_customers(db, skip=skip, limit=limit, search=search, tag=tag)

@app.get("/customers/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db, customer, customer_update)

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    crud.delete_customer(db, customer_id)
    return {"detail": "Customer deleted"}

@app.post("/templates", response_model=schemas.TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(
    template: schemas.TemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return crud.create_template(db, template)

@app.get("/templates", response_model=list[schemas.TemplateRead])
def list_templates(
    skip: int = 0,
    limit: int = 100,
    type: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_templates(db, skip=skip, limit=limit, template_type=type)

@app.post("/campaigns", response_model=schemas.CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: schemas.CampaignCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    created_campaign = crud.create_campaign(db, campaign)
    if created_campaign.scheduled_at and created_campaign.scheduled_at > datetime.utcnow():
        return created_campaign
    crud.send_campaign_messages(db, created_campaign)
    return created_campaign

@app.get("/campaigns", response_model=list[schemas.CampaignRead])
def list_campaigns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_campaigns(db, skip=skip, limit=limit)

@app.post("/campaigns/{campaign_id}/send", response_model=schemas.CampaignRead)
def send_campaign(campaign_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    campaign = crud.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    crud.send_campaign_messages(db, campaign)
    return campaign

@app.post("/messages", response_model=schemas.MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    customer = db.get(models.Customer, message.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    text = message.content
    result = send_whatsapp_message(customer.phone, text)
    status_value = "sent" if result.get("success") else "failed"
    db_message = crud.create_message(db, message, status=status_value)
    if not result.get("success"):
        raise HTTPException(status_code=502, detail=result.get("error"))
    return db_message

@app.get("/messages", response_model=list[schemas.MessageRead])
def list_messages(
    customer_id: int | None = None,
    campaign_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_messages(db, customer_id=customer_id, campaign_id=campaign_id, skip=skip, limit=limit)

@app.post("/festivals", response_model=schemas.FestivalRead, status_code=status.HTTP_201_CREATED)
def create_festival(
    festival: schemas.FestivalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return crud.create_festival(db, festival)

@app.get("/festivals", response_model=list[schemas.FestivalRead])
def list_festivals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_festivals(db)

@app.get("/dashboard", response_model=schemas.DashboardMetrics)
def dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_dashboard_metrics(db)


# Serve static frontend files for SPA routing
frontend_dist_env = os.getenv('FRONTEND_DIST_PATH')
if frontend_dist_env:
    frontend_dist = Path(frontend_dist_env)
else:
    # Calculate path: from /app/backend/app/main.py, go up 3 levels to /app, then frontend/dist
    frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"

# Fallback: if that doesn't exist, try relative to current working directory
if not frontend_dist.exists() and Path("../../frontend/dist").exists():
    frontend_dist = Path("../../frontend/dist").resolve()


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve SPA frontend for all non-API routes"""
    # Don't serve SPA for known file types (static assets)
    if full_path and ("." in full_path):
        file_path = frontend_dist / full_path
        if file_path.exists():
            return FileResponse(file_path)
        # Return 404 for missing static files
        return {"error": f"Asset not found: {full_path}"}, 404
    
    # Serve index.html for all other routes (SPA routing)
    index_path = frontend_dist / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    # If frontend not built, return helpful error with debugging info
    print(f"ERROR: Frontend dist not found at {frontend_dist}")
    print(f"Frontend dist exists: {frontend_dist.exists()}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"__file__ = {__file__}")
    
    return {
        "error": "Frontend not available", 
        "path": str(frontend_dist),
        "cwd": os.getcwd()
    }, 503
