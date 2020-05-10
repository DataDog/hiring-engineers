BEGIN;

CREATE USER datadog with password 'datadog';
GRANT pg_monitor TO datadog;

COMMIT;
