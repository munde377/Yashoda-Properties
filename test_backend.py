#!/usr/bin/env python
"""
Comprehensive Backend API Test Script
Tests all critical endpoints and functionality
"""
import httpx
import asyncio
import sys
import json

BASE_URL = "http://localhost:8000"

async def test_api():
    """Run comprehensive API tests"""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        results = {
            "status": "testing",
            "tests": {},
            "errors": []
        }
        
        # Test 1: Health Check
        print("\n=== Test 1: Health Check ===")
        try:
            response = await client.get("/health")
            if response.status_code == 200:
                print("✓ Health check passed")
                results["tests"]["health"] = {"status": "PASS", "code": 200}
            else:
                print(f"✗ Health check failed: {response.status_code}")
                results["tests"]["health"] = {"status": "FAIL", "code": response.status_code}
        except Exception as e:
            print(f"✗ Health check error: {e}")
            results["errors"].append(f"Health check: {str(e)}")
        
        # Test 2: OpenAPI Docs
        print("\n=== Test 2: OpenAPI Documentation ===")
        try:
            response = await client.get("/docs")
            if response.status_code == 200:
                print("✓ OpenAPI docs available")
                results["tests"]["docs"] = {"status": "PASS", "code": 200}
            else:
                print(f"✗ OpenAPI docs unavailable: {response.status_code}")
                results["tests"]["docs"] = {"status": "FAIL", "code": response.status_code}
        except Exception as e:
            print(f"✗ OpenAPI docs error: {e}")
            results["errors"].append(f"OpenAPI docs: {str(e)}")
        
        # Test 3: Create User (Admin)
        print("\n=== Test 3: Create Admin User ===")
        admin_user = {
            "username": "admin",
            "email": "admin@yashodaproperties.com",
            "password": "admin123",
            "role": "admin"
        }
        try:
            response = await client.post("/users", json=admin_user)
            if response.status_code in [200, 201]:
                print("✓ Admin user created")
                results["tests"]["create_admin"] = {"status": "PASS", "code": response.status_code}
            else:
                print(f"✗ Failed to create admin: {response.status_code}")
                if response.status_code == 400:
                    print(f"  Response: {response.json()}")
                results["tests"]["create_admin"] = {"status": "FAIL", "code": response.status_code}
        except Exception as e:
            print(f"✗ Create admin error: {e}")
            results["errors"].append(f"Create admin: {str(e)}")
        
        # Test 4: Login
        print("\n=== Test 4: User Login ===")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        token = None
        try:
            response = await client.post("/token", data=login_data)
            if response.status_code == 200:
                token = response.json().get("access_token")
                print("✓ Login successful")
                results["tests"]["login"] = {"status": "PASS", "code": 200}
            else:
                print(f"✗ Login failed: {response.status_code}")
                print(f"  Response: {response.json()}")
                results["tests"]["login"] = {"status": "FAIL", "code": response.status_code}
        except Exception as e:
            print(f"✗ Login error: {e}")
            results["errors"].append(f"Login: {str(e)}")
        
        # Test 5: Get Current User
        if token:
            print("\n=== Test 5: Get Current User ===")
            headers = {"Authorization": f"Bearer {token}"}
            try:
                response = await client.get("/users/me", headers=headers)
                if response.status_code == 200:
                    print("✓ Current user retrieved")
                    print(f"  User: {response.json()}")
                    results["tests"]["get_me"] = {"status": "PASS", "code": 200}
                else:
                    print(f"✗ Failed to get current user: {response.status_code}")
                    results["tests"]["get_me"] = {"status": "FAIL", "code": response.status_code}
            except Exception as e:
                print(f"✗ Get current user error: {e}")
                results["errors"].append(f"Get current user: {str(e)}")
            
            # Test 6: Create Customer
            print("\n=== Test 6: Create Customer ===")
            customer_data = {
                "name": "Raj Kumar",
                "phone": "+919876543210",
                "email": "raj@example.com",
                "birthday": "1990-05-15",
                "tags": ["vip", "premium"]
            }
            customer_id = None
            try:
                response = await client.post("/customers", json=customer_data, headers=headers)
                if response.status_code in [200, 201]:
                    customer_id = response.json().get("id")
                    print("✓ Customer created")
                    print(f"  ID: {customer_id}")
                    results["tests"]["create_customer"] = {"status": "PASS", "code": response.status_code}
                else:
                    print(f"✗ Failed to create customer: {response.status_code}")
                    print(f"  Response: {response.json()}")
                    results["tests"]["create_customer"] = {"status": "FAIL", "code": response.status_code}
            except Exception as e:
                print(f"✗ Create customer error: {e}")
                results["errors"].append(f"Create customer: {str(e)}")
            
            # Test 7: Get Customers
            print("\n=== Test 7: Get Customers ===")
            try:
                response = await client.get("/customers", headers=headers)
                if response.status_code == 200:
                    customers = response.json()
                    print(f"✓ Customers retrieved: {len(customers)} customers")
                    results["tests"]["get_customers"] = {"status": "PASS", "code": 200, "count": len(customers)}
                else:
                    print(f"✗ Failed to get customers: {response.status_code}")
                    results["tests"]["get_customers"] = {"status": "FAIL", "code": response.status_code}
            except Exception as e:
                print(f"✗ Get customers error: {e}")
                results["errors"].append(f"Get customers: {str(e)}")
            
            # Test 8: Create Template
            print("\n=== Test 8: Create Message Template ===")
            template_data = {
                "name": "Birthday Greeting",
                "template_type": "birthday",
                "content": "🎉 Happy Birthday! Wishing you a wonderful day ahead.",
                "variables": ["customer_name"]
            }
            try:
                response = await client.post("/templates", json=template_data, headers=headers)
                if response.status_code in [200, 201]:
                    print("✓ Template created")
                    results["tests"]["create_template"] = {"status": "PASS", "code": response.status_code}
                else:
                    print(f"✗ Failed to create template: {response.status_code}")
                    print(f"  Response: {response.json()}")
                    results["tests"]["create_template"] = {"status": "FAIL", "code": response.status_code}
            except Exception as e:
                print(f"✗ Create template error: {e}")
                results["errors"].append(f"Create template: {str(e)}")
            
            # Test 9: Get Dashboard Metrics
            print("\n=== Test 9: Get Dashboard Metrics ===")
            try:
                response = await client.get("/dashboard/metrics", headers=headers)
                if response.status_code == 200:
                    metrics = response.json()
                    print("✓ Dashboard metrics retrieved")
                    print(f"  Metrics: {json.dumps(metrics, indent=2)}")
                    results["tests"]["dashboard_metrics"] = {"status": "PASS", "code": 200}
                else:
                    print(f"✗ Failed to get metrics: {response.status_code}")
                    results["tests"]["dashboard_metrics"] = {"status": "FAIL", "code": response.status_code}
            except Exception as e:
                print(f"✗ Dashboard metrics error: {e}")
                results["errors"].append(f"Dashboard metrics: {str(e)}")
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        passed = sum(1 for test in results["tests"].values() if test.get("status") == "PASS")
        failed = sum(1 for test in results["tests"].values() if test.get("status") == "FAIL")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print(f"⚠ Errors: {len(results['errors'])}")
        
        if results['errors']:
            print("\nError Details:")
            for error in results['errors']:
                print(f"  - {error}")
        
        results["status"] = "completed"
        results["summary"] = {
            "passed": passed,
            "failed": failed,
            "errors": len(results['errors']),
            "total": len(results["tests"])
        }
        
        return results

if __name__ == "__main__":
    print("🚀 Backend API Test Suite")
    print(f"Testing: {BASE_URL}")
    print("="*50)
    
    results = asyncio.run(test_api())
    
    print("\n" + "="*50)
    print("Test Results (JSON):")
    print(json.dumps(results, indent=2))
    
    # Exit with appropriate code
    if results["summary"]["failed"] > 0 or results["summary"]["errors"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
