-- Set up datadog user with required permissions
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'%' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS on *.* TO 'datadog'@'%';
GRANT SELECT on performance_schema.* TO 'datadog'@'%';

-- Just some test data to see some action on the datadog graphs
CREATE DATABASE dd_demo;
use dd_demo;
CREATE TABLE numbers(
    id int);
INSERT INTO numbers (id) VALUES (1);
INSERT INTO numbers (id) VALUES (2);
INSERT INTO numbers (id) VALUES (3);
INSERT INTO numbers (id) VALUES (4);
INSERT INTO numbers (id) VALUES (5);
