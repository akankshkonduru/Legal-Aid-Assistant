
import sys
import os
import json
from fastapi.testclient import TestClient

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from api_server import app

client = TestClient(app)

def test_list_templates():
    print("Testing /templates endpoint...")
    response = client.get("/templates")
    if response.status_code == 200:
        data = response.json()
        templates = data.get("templates", [])
        print(f"Success! Found {len(templates)} templates.")
        for t in templates:
            print(f" - {t['title']} ({t['id']})")
        return templates
    else:
        print(f"Failed! Status code: {response.status_code}")
        print(response.text)
        return []

def test_generate_document(template_id):
    print(f"\nTesting /document/generate endpoint with template '{template_id}'...")
    
    payload = {
        "template_name": template_id,
        "user_inputs": {
            "name": "John Doe",
            "address": "123 Main St",
            "date": "2023-10-27",
            "details": "Test incident details",
            "applicant_name": "Jane Doe",
            "caste": "General",
            "reason": "Education"
        },
        "user_query": "Generate a test document"
    }
    
    response = client.post("/document/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"Message: {data.get('message')}")
        print(f"PDF URL: {data.get('pdf_url')}")
        print(f"Preview: {data.get('content_preview')[:100]}...")
    else:
        print(f"Failed! Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    templates = test_list_templates()
    if templates:
        # Test with the first template found
        test_generate_document(templates[0]['id'])
