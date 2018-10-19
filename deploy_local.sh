#!/bin/bash

echo "##### Check environment varialbes #####"
if [ ! -n "${YOUR_LOCAL_IP}" ]; then
  echo "export YOUR_LOCAL_IP"
elif [ ! -n "${DD_API_KEY}" ]; then
  echo "export DD_API_KEY"
else
  if [ ! -n "${DOCK_DEFAULT_GW}" ]; then
    export DOCK_DEFAULT_GW="172.17.0.1"  #Change to 172.18.0.1 or else to fit to your environment
  fi

  echo "##### Exporting Environemt Valiables #####"
  export NGINX_HOST=${YOUR_LOCAL_IP}
  export NGINX_PORT=80
  export APP_HOST=${YOUR_LOCAL_IP}
  export APP_PORT=8000
  export DB_HOST=${YOUR_LOCAL_IP}
  export DB_PORT=5432

  echo "##### Confirm local IP #####"
  echo "Your local IP address : ${YOUR_LOCAL_IP}"
  echo "Your Docker Default Gateway : ${DOCK_DEFAULT_GW}"
  echo "NGINX_HOST: ${NGINX_HOST}"
  echo "NGINX_PORT: ${NGINX_PORT}"
  echo "APP_HOST: ${APP_HOST}"
  echo "APP_PORT: ${APP_PORT}"
  echo "DB_HOST: ${DB_HOST}"
  echo "DB_PORT: ${DB_PORT}"

  echo "##### Building container images #####"
  docker-compose build

  echo "##### Startng DB datadog containers first #####"
  docker-compose up -d db datadog

  echo "##### Waiting for their services to be up #####"
  sleep 5

  echo "##### Creating postgres user for Datadog #####"
  docker run -it -e PGPASSWORD=Test1Pass postgres:9.6-alpine  psql -U postgres -h ${DB_HOST} -c "create user datadog with password 'Test1Pass';"
  docker run -it -e PGPASSWORD=Test1Pass postgres:9.6-alpine  psql -U postgres -h ${DB_HOST} -c "grant SELECT ON pg_stat_database to datadog;"
   ##Cannot Moved to Dockerfile_postgres because it starts to create a user before postgres starts, which fails.

  echo "##### Starting db migration for app #####"
  docker run -it \
    -e DOCKPGHOST=${YOUR_LOCAL_IP}  \
    -e DOCKPGPORT=5432 \
    -e DOCKPGDB=testweb \
    -e DOCKPGUSER=postgres \
    -e SECRET_KEY=Example5ecretKey \
    -e NEVERCACHE_KEY=Example2evercacheKey \
    -e DOCKPGPASSWD=Test1Pass \
    -e DEBUG=False \
    -e DOCK_DEFAULT_GW=${DOCK_DEFAULT_GW}  \
    testweb_app:test \
    /usr/bin/python3 /project/testweb/manage.py migrate # db migrate to postgres container

  echo "##### Starting APP and WEB containers #####"
  docker-compose up -d
  sleep 3

  echo "##### Local Deploy Result  #####"
  docker ps

  echo "##### Command to stop all containers #####"
  echo "docker-compose down"
fi
