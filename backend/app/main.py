"""
FastAPI application for customer engagement and WhatsApp automation.
"""

from datetime import datetime
import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
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

# Create database tables
models.Base.metadata.create_all(bind=engine)

from .config import settings

# Initialize FastAPI app
app = FastAPI(title="Customer Engagement & WhatsApp Automation API")

# Configure CORS for frontend integration
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
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    """Initialize background tasks and create default admin user."""
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
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
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
    """Create new user account. Requires admin privileges."""
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
    """Create new customer record."""
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
    """List customers with optional filtering."""
    return crud.get_customers(db, skip=skip, limit=limit, search=search, tag=tag)


@app.get("/customers/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """Get specific customer by ID."""
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
    """Update customer information."""
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
    """Delete customer record."""
    crud.delete_customer(db, customer_id)
    return {"detail": "Customer deleted"}

@app.post("/templates", response_model=schemas.TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(
    template: schemas.TemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create message template. Requires admin privileges."""
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
    """List message templates with optional type filter."""
    return crud.get_templates(db, skip=skip, limit=limit, template_type=type)


@app.post("/campaigns", response_model=schemas.CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: schemas.CampaignCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create and execute WhatsApp campaign. Requires admin privileges."""
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
    """List WhatsApp campaigns."""
    return crud.get_campaigns(db, skip=skip, limit=limit)

@app.post("/campaigns/{campaign_id}/send", response_model=schemas.CampaignRead)
def send_campaign(campaign_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """Manually trigger campaign message sending."""
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
    """Send WhatsApp message to customer."""
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
    """List messages with optional filtering by customer or campaign."""
    return crud.get_messages(db, customer_id=customer_id, campaign_id=campaign_id, skip=skip, limit=limit)

@app.post("/festivals", response_model=schemas.FestivalRead, status_code=status.HTTP_201_CREATED)
def create_festival(
    festival: schemas.FestivalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create festival event for automated greetings. Requires admin privileges."""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return crud.create_festival(db, festival)


@app.get("/festivals", response_model=list[schemas.FestivalRead])
def list_festivals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """List all festival events."""
    return crud.get_festivals(db)


@app.get("/dashboard", response_model=schemas.DashboardMetrics)
def dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get dashboard statistics and metrics."""
    return crud.get_dashboard_metrics(db)


# Mount static files for frontend (SPA fallback)
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

frontend_dist_path = os.getenv("FRONTEND_DIST_PATH", settings.frontend_dist_path)
print(f"DEBUG: Frontend dist path: {frontend_dist_path}")
print(f"DEBUG: Directory exists: {os.path.exists(frontend_dist_path)}")

# Debug: List directory contents
if os.path.exists(frontend_dist_path):
    try:
        contents = os.listdir(frontend_dist_path)
        print(f"DEBUG: Contents of {frontend_dist_path}: {contents}")
        
        # Check for assets directory
        assets_path = os.path.join(frontend_dist_path, "assets")
        if os.path.exists(assets_path):
            assets_contents = os.listdir(assets_path)
            print(f"DEBUG: Assets folder contents: {assets_contents[:5]}...")  # First 5 items
        else:
            print(f"WARNING: Assets directory not found at {assets_path}")
    except Exception as e:
        print(f"ERROR listing directory: {e}")

# Try to mount from primary path first
if os.path.exists(frontend_dist_path):
    print("DEBUG: Mounting static files from primary path")
    app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="frontend")
else:
    print(f"WARNING: Frontend dist directory not found at {frontend_dist_path}")
    # Try alternate path calculation
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alt_path = os.path.join(base_dir, "..", "frontend", "dist")
    print(f"DEBUG: Trying alternate path: {alt_path}")
    print(f"DEBUG: Alternate path exists: {os.path.exists(alt_path)}")
    
    if os.path.exists(alt_path):
        print("DEBUG: Mounting static files from alternate path")
        try:
            contents = os.listdir(alt_path)
            print(f"DEBUG: Contents of alternate path: {contents}")
            assets_path_alt = os.path.join(alt_path, "assets")
            if os.path.exists(assets_path_alt):
                assets_contents_alt = os.listdir(assets_path_alt)
                print(f"DEBUG: Assets folder contents (alt): {assets_contents_alt[:5]}...")
        except Exception as e:
            print(f"ERROR listing alt directory: {e}")
        
        app.mount("/", StaticFiles(directory=alt_path, html=True), name="frontend")
    else:
        # Fallback: serve a simple HTML page
        @app.get("/")
        def read_root():
            return {"message": "Frontend not available. Please check deployment configuration."}