#!/usr/bin/env python
"""Quick test of the scraper endpoint"""
import requests
import json

url = 'http://127.0.0.1:5000/api/scrape-job'
payload = {'url': 'https://example.com'}

print('Testing Scraper Endpoint...')
print(f'POST {url}')
print(f'Body: {json.dumps(payload, indent=2)}')
print()

try:
    r = requests.post(url, json=payload, timeout=10)
    print(f'Status: {r.status_code}')
    print(f'Response:')
    print(json.dumps(r.json(), indent=2))
    print()
    print('✅ SCRAPER WORKING!')
except Exception as e:
    print(f'❌ ERROR: {e}')
