#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    create user datadog with password '$DD_POSTGRES_PSWD';
    grant pg_monitor to datadog;
    grant SELECT ON pg_stat_database to datadog;
EOSQL