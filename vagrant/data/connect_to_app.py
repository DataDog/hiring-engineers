import requests
import time
from random import randint

url1 = 'http://localhost:8080'
url2 = 'http://localhost:8080/api/apm'
url3 = 'http://localhost:8080/api/trace'
parameters = {'x-api-version':2,'accept':'text/json','content-type':'text/json'}

while 1:
    print('Sending requests')
    con_num = randint(1,20)
    for i in range(randint(1,20)):
        response = requests.get(url1,params=parameters)
    for i in range(randint(1,15)):
        response = requests.get(url2,params=parameters)
    for i in range(randint(1,10)):
        response = requests.get(url3,params=parameters)