#!/usr/bin/env bash

# This script is used to generate unique passwords for mysql users
# Never generate prod passwords as is done below!

mysql_root_password=`date | md5sum | cut -f1 -d' '`
echo "Updating MySQL root password"
sed -i "/MYSQL_ROOT_PASSWORD=/c\MYSQL_ROOT_PASSWORD=${mysql_root_password}" ./mysql/.env 


sleep 1 # Ensures date | md5sum  will be different for datadog user password
mysql_datadog_password=`date | md5sum | cut -f1 -d' '`
echo "Updating MySQL datadog user password"
sed -i "/MYSQL_PASSWORD=/c\MYSQL_PASSWORD=${mysql_datadog_password}" ./mysql/.env 
sed -i "/pass:/c\    pass: ${mysql_datadog_password}" datadog/conf.d/mysql.yaml
