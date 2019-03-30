#!/bin/bash

#curl -X GET 'http://localhost:5050/'
#Generate some continuos traffic to flask demo app 
while [ 1 ]
do
for i in / /api/apm /api/trace; do
echo "$i\n"
curl -X GET "http://localhost:5050$i"
sleep 3
done
done
