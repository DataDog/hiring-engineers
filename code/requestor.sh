```
number=$((RANDOM % 1000)); for ((run=1; run <= number; run++)); do curl http://0.0.0.0:5050/api/trace; curl http://0.0.0.0:5050/api/apm; curl http://0.0.0.0:5050/; done
```
