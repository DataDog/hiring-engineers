#!/bin/bash

for i in $(seq 0 1000); do
    curl http://localhost:8050/
    curl http://localhost:8050/api/apm
    curl http://localhost:8050/api/trace
    sleep 3
done

