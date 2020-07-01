sudo docker network create ddnetwork

sudo docker run \
-d \
-l "com.datadoghq.ad.logs"='[{"source": "mysql container", "service": "mysql"}]' \
--name=mysql1 \
--network ddnetwork \
--env="MYSQL_ROOT_PASSWORD=datadog" \
--publish 6603:3306 \
--mount type=bind,src=/home/datadog/mysql_config/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/home/datadog/mysql_config/data,dst=/var/lib/mysql \
--mount type=bind,src=/home/datadog/mysql_config/scripts/,dst=/docker-entrypoint-initdb.d/ \
mysql/mysql-server
