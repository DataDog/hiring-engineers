#!/bin/bash
#
#  push current number of lines in sampledb.checkin to Instana checks via statsd
#

while true ; do 
  sleep 10
  NUM=$(~/bin/check.sh)
  # echo $NUM
  echo "recent_checkins:$NUM|g" | nc -u -w5 127.0.0.1 8125
done


