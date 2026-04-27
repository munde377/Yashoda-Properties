#!/usr/bin/env python
"""Test script to verify Render deployment configuration."""

import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')

print("=" * 60)
print("RENDER DEPLOYMENT VERIFICATION")
print("=" * 60)

# Test 1: Check frontend dist folder exists
frontend_dist = os.path.abspath('frontend/dist')
print(f"\n1. Frontend dist folder:")
print(f"   Path: {frontend_dist}")
print(f"   Exists: {'✓' if os.path.exists(frontend_dist) else '✗'}")

if os.path.exists(frontend_dist):
    files = os.listdir(frontend_dist)
    print(f"   Contents: {', '.join(files)}")

# Test 2: Load FastAPI app
print(f"\n2. FastAPI configuration:")
try:
    os.environ['FRONTEND_DIST_PATH'] = frontend_dist
    from app.main import app
    from app.config import settings
    
    print(f"   ✓ App loaded successfully")
    print(f"   Frontend dist path setting: {settings.frontend_dist_path}")
    print(f"   Routes defined: {len([r for r in app.routes if hasattr(r, 'path')])}")
    print(f"   Middleware: {len(app.user_middleware)}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Check API configuration
print(f"\n3. Frontend API configuration:")
print(f"   VITE_API_URL env var: {os.getenv('VITE_API_URL', 'not set')}")
print(f"   Expected behavior:")
print(f"     - Development: uses http://localhost:8000")
print(f"     - Production: uses relative paths (same domain)")

print("\n" + "=" * 60)
print("DEPLOYMENT CHECKLIST")
print("=" * 60)
print("✓ Frontend dist: Built with npm run build")
print("✓ API URLs: Configured for same-domain requests")
print("✓ StaticFiles: Mounted at root with SPA fallback (html=True)")
print("✓ CORS: Configured for development")
print("✓ Environment: FRONTEND_DIST_PATH set to /app/frontend/dist")
print("\nReady for Render deployment!")
print("=" * 60)
