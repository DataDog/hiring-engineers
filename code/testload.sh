#!/bin/bash

while :
do
   curl localhost:5000/
   sleep 2
   curl localhost:5000/api/apm
   sleep 2
   curl localhost:5000/api/trace
   sleep 2
done
