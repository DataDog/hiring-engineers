#!/bin/bash
#
# Author : Lutz Lange <lutzinberlin@gmail.com>
# 
# This is part of a simple load generator for postgres
#   Here we check repeatetly how many entries we have in the checkin table


while true; do
    psql sampledb -th localhost -c 'select COUNT(*) from checkin;' 2>/dev/null | grep -v -e '^$'
    sleep 0.5
done

