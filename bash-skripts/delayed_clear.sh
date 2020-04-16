#!/bin/bash
#
# Author : Lutz Lange <lutzinberlin@gmail.com>
# 
# This is part of a simple load generator for postgre
#
# Run this if you are running the inserts.sh and you want to prevent your disc filling up

while true; do
  sleep 600
  psql sampledb -h localhost -c 'DELETE from checkin;' 2>/dev/null
done

