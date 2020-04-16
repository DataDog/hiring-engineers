#!/bin/bash

mysql -u instanian -pinstant21 sampledb -e'DELETE from checkin;' 2>/dev/null

