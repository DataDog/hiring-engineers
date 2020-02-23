#!/usr/bin/env bash
# from datadog prerun.sh script - modify as needed
# Disable the Datadog Agent based on Dyno type
#if [ "$DYNOTYPE" == "run" ]; then
  #DISABLE_DATADOG_AGENT="true"
#fi
# Include application's datadog configs
# moves things into place for Heroku Runtime correctly so the App has all the right
# things self contained to go through the exercise repeatedly 
APT_DIR="$HOME/.apt"
DD_DIR="$APT_DIR/opt/datadog-agent"
DD_RUN_DIR="$DD_DIR/run"
# Export DD_BIN_DIR to be used by the wrapper
export DD_BIN_DIR="$DD_DIR/bin/agent"
DD_LOG_DIR="$APT_DIR/var/log/datadog"
DD_CONF_DIR="$APT_DIR/etc/datadog-agent"
export DATADOG_CONF="$DD_CONF_DIR/datadog.yaml"

# Update Env Vars with new paths for apt packages
export PATH="$APT_DIR/usr/bin:$DD_BIN_DIR:$PATH"
# Export agent's LD_LIBRARY_PATH to be used by the agent-wrapper
export DD_LD_LIBRARY_PATH="$APT_DIR/opt/datadog-agent/embedded/lib:$APT_DIR/usr/lib/x86_64-linux-gnu:$APT_DIR/usr/lib"

# Set Datadog configs
export DD_LOG_FILE="$DD_LOG_DIR/datadog.log"
DD_APM_LOG="$DD_LOG_DIR/datadog-apm.log"
APP_DATADOG="$APT_DIR/datadog"
APP_DATADOG_CONF_DIR="$APP_DATADOG/conf.d"
echo "$APP_DATADOG_CONF_DIR"
#hack for placemnent of AgentCheck custom metrics for Heroku (issue filed)
echo "Copy my_metric"
cp -pr "/app/datadog/checks.d/my_metric.d/my_metric.py" "$DD_CONF_DIR/checks.d/"
echo "Copy conf_d"
echo "$file"
echo "$DD_CONF_DIR/conf.d/${filename}.d"
echo "Copy Yamls"

for file in "$APP_DATADOG_CONF_DIR"/*.yaml; do
  test -e "$file" || continue # avoid errors when glob doesn't match anything
  filename="$(basename -- "$file")"
  filename="${filename%.*}"
  mkdir -p "$DD_CONF_DIR/conf.d/${filename}.d"
  echo "Copy configuration Yaml"
  cp "$file" "$DD_CONF_DIR/conf.d/${filename}.d/conf.yaml"
done
# Update the Postgres configuration from above using the Heroku application environment variable
if [ -n "$DATABASE_URL" ]; then
  POSTGREGEX='^postgres://([^:]+):([^@]+)@([^:]+):([^/]+)/(.*)$'
  if [[ $DATABASE_URL =~ $POSTGREGEX ]]; then
    sed -i "s/<YOUR HOSTNAME>/${BASH_REMATCH[3]}/" "$DD_CONF_DIR/conf.d/postgres.d/conf.yaml"
    sed -i "s/<YOUR USERNAME>/${BASH_REMATCH[1]}/" "$DD_CONF_DIR/conf.d/postgres.d/conf.yaml"
    sed -i "s/<YOUR PASSWORD>/${BASH_REMATCH[2]}/" "$DD_CONF_DIR/conf.d/postgres.d/conf.yaml"
    sed -i "s/<YOUR PORT>/${BASH_REMATCH[4]}/" "$DD_CONF_DIR/conf.d/postgres.d/conf.yaml"
    sed -i "s/<YOUR DBNAME>/${BASH_REMATCH[5]}/" "$DD_CONF_DIR/conf.d/postgres.d/conf.yaml"
  fi
fi
