!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" << EOSQL
        -- create the service user needed for the postgres integration in Datadog
        create user datadog with password 'Agnzr5uEKeLrt81ZRhucdjqc';
        -- grant access to a default/built-in database in postgres
        grant SELECT ON pg_stat_database to datadog;
EOSQL
