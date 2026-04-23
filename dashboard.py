#!/usr/bin/env python
"""Dashboard Viewer - Display all metrics"""
import httpx
import json
from datetime import datetime

print("\n" + "="*70)
print("📊 YASHODA PROPERTIES - DASHBOARD")
print("="*70 + "\n")

try:
    # Health check
    r = httpx.get('http://localhost:8000/health', timeout=5)
    if r.status_code == 200:
        print("✅ API Status: ONLINE")
    
    # Create user and get data
    user_data = {
        "username": f"dashboard_user_{int(datetime.now().timestamp())}",
        "email": f"dashboard_{int(datetime.now().timestamp())}@test.com",
        "password": "Pass123456!",
        "role": "admin"
    }
    
    r = httpx.post('http://localhost:8000/users', json=user_data, timeout=5)
    if r.status_code in [200, 201]:
        username = r.json()['username']
        print(f"✅ User Created: {username}")
        
        # Login
        r = httpx.post('http://localhost:8000/token', 
                       data={"username": username, "password": "Pass123456!"}, 
                       timeout=5)
        if r.status_code == 200:
            token = r.json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            print(f"✅ Authentication: TOKEN OBTAINED\n")
            
            # Get all metrics
            print("📥 Fetching data from API...\n")
            
            customers = httpx.get('http://localhost:8000/customers', headers=headers, timeout=5).json()
            templates = httpx.get('http://localhost:8000/templates', headers=headers, timeout=5).json()
            campaigns = httpx.get('http://localhost:8000/campaigns', headers=headers, timeout=5).json()
            messages = httpx.get('http://localhost:8000/messages', headers=headers, timeout=5).json()
            festivals = httpx.get('http://localhost:8000/festivals', headers=headers, timeout=5).json()
            
            # Display metrics
            print("="*70)
            print("📊 SYSTEM METRICS")
            print("="*70)
            print(f"👥 Total Customers:        {len(customers):>10}")
            print(f"📝 Total Templates:        {len(templates):>10}")
            print(f"📢 Total Campaigns:        {len(campaigns):>10}")
            print(f"💬 Total Messages:         {len(messages):>10}")
            print(f"🎊 Total Festivals:        {len(festivals):>10}")
            print("="*70)
            
            # API Info
            print("\n🔗 API INFORMATION")
            print("="*70)
            print(f"API Endpoint:              http://localhost:8000")
            print(f"API Documentation:        http://localhost:8000/docs")
            print(f"Alternative Docs:         http://localhost:8000/redoc")
            print(f"OpenAPI Schema:            http://localhost:8000/openapi.json")
            print("="*70)
            
            # Database Info
            print("\n💾 DATABASE INFORMATION")
            print("="*70)
            print(f"Database Type:             SQLite")
            print(f"Database File:             e:\\yashodaproperties\\backend\\app.db")
            print(f"Tables:")
            print(f"  • Users")
            print(f"  • Customers ({len(customers)} records)")
            print(f"  • Templates ({len(templates)} records)")
            print(f"  • Campaigns ({len(campaigns)} records)")
            print(f"  • Messages ({len(messages)} records)")
            print(f"  • Festivals ({len(festivals)} records)")
            print("="*70)
            
            # Export JSON
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "status": "online",
                "server": {
                    "api_url": "http://localhost:8000",
                    "docs_url": "http://localhost:8000/docs",
                    "port": 8000
                },
                "metrics": {
                    "total_customers": len(customers),
                    "total_templates": len(templates),
                    "total_campaigns": len(campaigns),
                    "total_messages": len(messages),
                    "total_festivals": len(festivals)
                },
                "database": {
                    "type": "SQLite",
                    "file": "app.db",
                    "path": "e:\\yashodaproperties\\backend\\app.db"
                },
                "authentication": {
                    "type": "JWT",
                    "password_algorithm": "Argon2",
                    "token_endpoint": "/token"
                }
            }
            
            print("\n📋 DASHBOARD DATA (JSON)")
            print("="*70)
            print(json.dumps(dashboard_data, indent=2))
            print("="*70)
            
            # Customer samples
            if customers:
                print("\n👥 SAMPLE CUSTOMERS (Latest)")
                print("="*70)
                for i, customer in enumerate(customers[-3:], 1):
                    print(f"{i}. {customer.get('name', 'N/A')}")
                    print(f"   Phone: {customer.get('phone', 'N/A')}")
                    print(f"   Email: {customer.get('email', 'N/A')}")
                    print(f"   Birthday: {customer.get('birthday', 'N/A')}")
                    print()
            
            # Templates sample
            if templates:
                print("\n📝 SAMPLE TEMPLATES (Latest)")
                print("="*70)
                for i, template in enumerate(templates[-3:], 1):
                    print(f"{i}. {template.get('name', 'N/A')}")
                    print(f"   Type: {template.get('type', 'N/A')}")
                    print(f"   Body: {template.get('body', 'N/A')[:50]}...")
                    print()
            
            print("\n✅ DASHBOARD READY")
            print("="*70)
            print("📊 Open http://localhost:8000/docs to view complete API")
            print("="*70 + "\n")

except httpx.ConnectError:
    print("❌ ERROR: Cannot connect to API at http://localhost:8000")
    print("Make sure the backend is running:")
    print("  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
except Exception as e:
    print(f"❌ ERROR: {e}")
