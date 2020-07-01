# To run script on contrain lauch use
#  --mount type=bind,src=/home/datadog/config/scripts/,dst=/docker-entrypoint-initdb.d/ \
CREATE USER 'dduser'@'%' IDENTIFIED WITH mysql_native_password by 'datadog';
GRANT REPLICATION CLIENT ON *.* TO 'dduser'@'%';
GRANT PROCESS ON *.* TO 'dduser'@'%';
ALTER USER 'dduser'@'%' WITH MAX_USER_CONNECTIONS 5;
GRANT SELECT ON performance_schema.* TO 'dduser'@'%';