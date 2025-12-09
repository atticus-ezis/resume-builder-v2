#!/usr/bin/env python
"""Script to test email confirmation key"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_builder.settings")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "testserver,localhost")
django.setup()

# Update ALLOWED_HOSTS for testing
from django.conf import settings

settings.ALLOWED_HOSTS = ["testserver", "localhost", "*"]

from django.urls import reverse
from rest_framework.test import APIClient
import json

# The key to test
key = "3DMjY:1vSBCF:Y-GogYG7YxWbdz5-6TJcFI1OiLcZ52nsg7aRTAa2zMg"

print(f"Testing email confirmation key: {key}")
print("-" * 60)

# Try to find the correct URL
url = None
url_names_to_try = [
    "rest_verify_email",
    "account_email_verification_sent",
    "verify_email",
]

for url_name in url_names_to_try:
    try:
        url = reverse(url_name)
        print(f"Found URL name '{url_name}': {url}")
        break
    except:
        continue

if not url:
    # Use the direct path from urls.py
    url = "/dj-rest-auth/account-confirm-email/"
    print(f"Using direct path: {url}")

# Make the request
client = APIClient()
response = client.post(url, {"key": key}, format="json")

print(f"\nResponse Status: {response.status_code}")

# Try to get response data
try:
    if hasattr(response, "data"):
        print(f"Response Data: {json.dumps(response.data, indent=2)}")
    elif hasattr(response, "content"):
        try:
            data = json.loads(response.content.decode("utf-8"))
            print(f"Response Data: {json.dumps(data, indent=2)}")
        except:
            print(f"Response Content: {response.content.decode('utf-8')[:200]}")
except Exception as e:
    print(f"Could not parse response: {e}")

if response.status_code == 200:
    print("\n✅ SUCCESS: Key is valid!")
elif response.status_code == 400:
    print("\n❌ ERROR: Key is invalid or has already been used")
elif response.status_code == 404:
    print("\n❌ ERROR: Endpoint not found")
else:
    print(f"\n⚠️  Unexpected status code: {response.status_code}")



