#!/bin/bash
if [ ! -n "${YOUR_LOCAL_IP}" ]; then
  echo "export YOUR_LOCAL_IP"
elif [ ! -n "${YOUR_DD_API_KEY}" ]; then
  echo "export YOUR_DD_API_KEY"
else

  echo ${YOUR_LOCAL_IP}
  echo "##### Build container images #####"
  export NGINX_HOST=${YOUR_LOCAL_IP}
  export NGINX_PORT=80
  export APP_HOST=${YOUR_LOCAL_IP}
  export APP_PORT=8000
  export DB_HOST=${YOUR_LOCAL_IP}
  export DB_PORT=5432

  echo "##### Build container images #####"
  docker-compose build
  echo "##### Start DB container first #####"
  docker-compose up -d db
  echo "##### Wait for db to start #####"
  sleep 5
  PGPASSWORD=Test1Pass psql -U postgres -h localhost -c "create user datadog with password 'Test1Pass';"
  PGPASSWORD=Test1Pass psql -U postgres -h localhost -c "grant SELECT ON pg_stat_database to datadog;"
  PGPASSWORD=Test1Pass psql -U postgres -h localhost -d testweb  -c \
         "select * from pg_stat_database LIMIT(1);" \
         && echo -e "\e[0;32mPostgres connection - OK\e[0m" \
         || echo -e "\e[0;31mCannot connect to Postgres\e[0m"

  echo "##### Start db migrate #####"
  docker run -it \
    -e DOCKPGHOST=$YOUR_LOCAL_IP  \
    -e DOCKPGPORT=5432 \
    -e DOCKPGDB=testweb \
    -e DOCKPGUSER=postgres \
    -e SECRET_KEY=adf7sgEF93E33 \
    -e NEVERCACHE_KEY=adfkaafadsfad97093gawegsdg \
    -e DOCKPGPASSWD=Test1Pass \
    -e DEBUG=True \
    testweb_app:test \
    /usr/bin/python3 /project/testweb/manage.py migrate # db migrate to postgres container
  echo "##### Start APP and WEB containers #####"
  docker-compose up -d
  sleep 3
  docker ps
  echo "##### CMD to stop all containers #####"
  echo "docker-compose down"
fi
