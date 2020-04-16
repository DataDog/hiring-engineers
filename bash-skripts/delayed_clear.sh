#!/bin/bash

while true; do
  sleep 300
  mysql -u instanian -pinstant21 sampledb -e'DELETE from checkin;' 2>/dev/null
done

