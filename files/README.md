# Datadog SE Exercise
## Docker Environment
This project contains a docker-compose.yml that spins up the datadog agent `dd-agent`, a mysql database, and a flask application for APM / Tracing.

## Usage
```docker-compose up```

This will spin up all the assets, as well as build the flask app docker container before running it.

** Be sure to update the env directory with all the required secrets **