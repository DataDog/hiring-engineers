CREATE USER datadog WITH PASSWORD 'datadog';
GRANT SELECT ON pg_stat_database TO datadog;
