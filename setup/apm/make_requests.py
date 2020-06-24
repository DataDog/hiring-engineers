# simulate some traffic by making a few reqests to the REST API

import requests
import random

endpoints = ["/", "/api/apm", "/api/trace"]
count = 10

# randomly call one of the possible endpoints (10 times)
while count > 0:
  index = random.randint(0, 2)
  requests.get(f"http://localhost:5533{endpoints[index]}")
  count = count - 1
