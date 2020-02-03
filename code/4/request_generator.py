"""
This continuously hits each of our main Flask App's three endpoints randomly,
waiting a random amount of time between requests (0-125 ms).
"""

import random
import requests
import time
import urllib.parse

BASE_URL = 'http://localhost:5050'
ENDPOINTS = ['/', '/api/apm', '/api/trace']

while True:
    app_endpoint = ENDPOINTS[random.randint(0, 2)]
    full_url = urllib.parse.urljoin(BASE_URL, app_endpoint)

    print(f'Sending request to `{full_url}`')
    r = requests.get(url=full_url)

    ms_to_wait = random.randint(0, 125)
    time.sleep(ms_to_wait / 1000)
