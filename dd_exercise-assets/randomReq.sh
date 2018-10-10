#!/bin/bash

randaomNum=$(( $RANDOM % 3 ))

if [ $randaomNum = 0 ]; then
    curl localhost:5050/
elif [ $randaomNum = 1 ]; then
    curl localhost:5050/api/apm
else
    curl localhost:5050/api/trace
fi