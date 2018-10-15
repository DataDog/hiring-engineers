#!/bin/sh

ConfigureDatadogforNginx () {
  echo "Configure DD agent for Nginx"
  if [ -n "${NGINX_HOST}" ];then
    echo $NGINX_HOST
    envsubst '$$NGINX_HOST' < /conf.d/nginx.d/conf.template > /etc/datadog-agent/conf.d/nginx.d/conf.yaml
    cat  /etc/datadog-agent/conf.d/nginx.d/conf.yaml
  else
    /bin/echo "ERROR: nginx hostname is missing, please define NGINX_HOST environment variable."
  fi
}


ConfigureDatadogforPostgres () {
  echo "Configure DD agent for Postgres"
  if [ -n "${DB_HOST}" ];then
    echo $DB_HOST
    envsubst '$$DB_HOST' < /conf.d/postgres.d/conf.template > /etc/datadog-agent/conf.d/postgres.d/conf.yaml
    cat  /etc/datadog-agent/conf.d/postgres.d/conf.yaml
  else
    /bin/echo "ERROR: postgres hostname is missing, please define DB_HOST environment variable."
  fi
}

AddCustomMetrics () {
  echo "Configure DD agent for Custom Metrics"
  cp -p /conf.d/*.yaml /etc/datadog-agent/conf.d/
}


ConfigureDatadogforNginx
ConfigureDatadogforPostgres 
AddCustomMetrics

exec "$@"
