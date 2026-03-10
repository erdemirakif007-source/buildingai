import json
import requests

# Test the login endpoint
response = requests.post(
    'http://localhost:8001/login',
    json={'email': 'erdemirakif@gmail.com', 'password': 'test123'},
    headers={'Content-Type': 'application/json'}
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Content-Type: {response.headers.get('content-type')}")
print(f"Response Body: {response.text}")
print(f"Response JSON: {response.json()}")

if response.status_code == 200:
    print("\n✓ Login endpoint is working correctly!")
else:
    print("\n✗ Login endpoint returned an error")
