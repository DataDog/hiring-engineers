#!/bin/bash
#
# Author : Lutz Lange <lutzinberlin@gmail.com>
# 
# This is part of a simple load generator for postgres
#   Here we check repeatetly insert timestamps into the checkin table

while true; do
   psql sampledb -h localhost -c 'INSERT into checkin VALUES (now());' 2>/dev/null
   sleep 0.2
done

