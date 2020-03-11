#!/bin/bash

count=$((RANDOM % 1000))
echo "count=$count"

for ((run=0; run < count; run++));
do
    echo -n "."
    curl http://octodev02:3000/api/trace 2&>1 
    curl http://octodev02:3000/api/apm 2&>1
done
