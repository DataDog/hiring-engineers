import requests
import urlparse
import time

# test iterations
j = 10
while (j > 0):
	print("Test " + str(j))
	requests.get("http://localhost:5050/")
	time.sleep(1)
	requests.get("http://localhost:5050/api/apm")
	time.sleep(1)
	requests.get("http://localhost:5050/api/trace")
	j -= 1	
