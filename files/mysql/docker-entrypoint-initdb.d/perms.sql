use mysql;
CREATE USER 'datadog'@'%' IDENTIFIED BY 'badChoices';
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'%' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS on *.* TO 'datadog'@'%';
use performance_schema;
GRANT SELECT ON performance_schema.* TO 'datadog'@'%';
flush privileges;
