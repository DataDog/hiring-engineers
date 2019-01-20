#!/bin/bash

for i in $(seq 1000); do
  if (($i % 5));
  then
    curl localhost:5050/api/trace
    echo
  if  (($i % 2));
  then
    curl localhost:5050
    echo
  fi
  else
    curl localhost:5050/api/apm
    echo
  fi
done
