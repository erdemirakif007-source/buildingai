import requests
import time

print("Starting 125 requests...")
for i in range(125):
    res = requests.get("http://127.0.0.1:8000/")

print("125th response status:", res.status_code)
print("125th response detail:", res.json() if res.status_code == 429 else "OK")
