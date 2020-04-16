#!/bin/bash

mysql -B --disable-column-names -u instanian -pinstant21 sampledb -e'select COUNT(*) from checkin;' 2>/dev/null

