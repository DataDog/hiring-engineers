#!/bin/sh

ConfigureDatadogAgent () {
  echo "Configure DD agent Started"
  # Configure DD agentproperties
  if [ -n "${NGINX_HOST}" ];then
    echo $NGINX_HOST
    envsubst '$$NGINX_HOST' < /conf.d/nginx.d/conf.template > /conf.d/nginx.d/conf.yml
    cat  /conf.d/nginx.d/conf.yml 
    rm -rf /conf.d/nginx.d/conf.template
  else
    /bin/echo "ERROR: nginx hostname is missing, please define NGINX_HOST environment variable."
  fi
}

ConfigureDatadogAgent

exec "$@"
