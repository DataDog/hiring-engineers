#!/bin/bash
echo "start"
ddtrace-run python datadogAPM.py &
sleep 5

echo "Starting datadogAPM.py"
COUNT=1
for x in $(seq 1 20)
do
  echo "Iteration $x"
  echo "homepage"
  curl "http://localhost:5050"
  echo "apm page"
  curl "http://localhost:5050/api/apm"
  echo "trace page"
  curl "http://localhost:5050/api/trace"
  echo "world page"
  curl "http://localhost:5050/api/world"
  sleep 2
done
kill $(pgrep -f 'datadogAPM.py')
sudo kill $(sudo lsof -t -i:5050)
echo "Shutting Down datadogAPM.py"
echo "finished"
