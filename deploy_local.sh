#!/bin/bash

echo "##### Check environment varialbes #####"
if [ ! -n "${YOUR_LOCAL_IP}" ]; then
  echo "export YOUR_LOCAL_IP"
elif [ ! -n "${DD_API_KEY}" ]; then
  echo "export DD_API_KEY"
else

  echo "##### Confirm local IP #####"
  echo "Your Local IP address is : ${YOUR_LOCAL_IP}"

  echo "##### Exporting Environemt Valiables #####"
  export DOCKER_DEFAULT_GATEWAY="172.19.0.1"       #Might change to 172.17.0.1 or else to fit to your environment
  export NGINX_HOST=${YOUR_LOCAL_IP}
  export NGINX_PORT=80
  export APP_HOST=${YOUR_LOCAL_IP}
  export APP_PORT=8000
  export DB_HOST=${YOUR_LOCAL_IP}
  export DB_PORT=5432

  echo "##### Building container images #####"
  docker-compose build

  echo "##### Startng DB datadog containers first #####"
  docker-compose up -d db datadog

  echo "##### Waiting for their services to be up #####"
  sleep 5

  echo "##### Creating postgres user for Datadog #####"
  PGPASSWORD=Test1Pass psql -U postgres -h ${DB_HOST} -c "create user datadog with password 'Test1Pass';"
  PGPASSWORD=Test1Pass psql -U postgres -h ${DB_HOST} -c "grant SELECT ON pg_stat_database to datadog;"
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
    -e DD_AGENT_PORT_8126_TCP_ADDR=${YOUR_LOCAL_IP} \
    -e DD_HOST=${DOCKER_DEFAULT_GATEWAY}  \
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
