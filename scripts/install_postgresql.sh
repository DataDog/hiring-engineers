#!/bin/bash
# Installs PostgreSQL, Creates a user & Configures Datadog integration
# It is assumed that datadog is already installed prior to running this script

set -e

# Constants
declare -r PSQL_USER="sudo -i -u postgres"
declare -r PSQL_COMMAND="/usr/bin/psql -U postgres -c"
declare CHECK_INSTALLED=$(basename $(which psql))

# Variables
declare DB_USER
declare PSSWD
declare DB_NAME

function usage() {
  echo "Usage: $0 [username] [database name] [password]"
  echo 'Examples:'
  echo "    $0 dbname - Will check if db exists, will create if it doesn't."
  echo "    $0 datadog password - Will check is user exists, test user or create user & test."
  echo "    $0 datadog dbname password - Will create user w/ password for db and/or test if it is successful."
  exit 0
}

# Ensure proper parameters
case $# in
    ( 1 )
         DB_NAME="$1" ;;
    ( 2 )
         DB_USER="$1"
         PSSWD="$2" ;;
    ( 3 )
         DB_USER="$1"
         DB_NAME="$2"
         PSSWD="$3" ;;
    ( * ) usage ;;
esac
[[ "$#" -eq 1  ||  "$#" -eq 2  ||  "$#" -eq 3 ]] && user_int="$#" || usage

function install_postgres() {
  # Checking wether postgresql is installed or not
  if [ $CHECK_INSTALLED == 'psql' ]
  then
      echo "PostgreSQL already installed."
  else
    echo "Installing PostgreSQL." \
    sudo apt-get update \
    sudo apt-get install -y postgresql postgresql-contrib
  fi
}

function create_user() {
  # Here I am running the createuser command as the postgres user to create a read-only datadog user
  # -D=Cannot create databases, -R=Cannot create roles, -S=Not Superuser
  $PSQL_USER /usr/bin/createuser -U postgres -D -R -S $DB_USER && echo "$DB_USER user has been created."
}

function create_db() {
     # Will create a database with the name provided, or fail if exists
     $PSQL_USER createdb $DB_NAME && echo "Database $DB_NAME has been created."
}

function auth_priveledge() {
  # Give the user a password and databse privileges
  $PSQL_USER $PSQL_COMMAND "ALTER USER $DB_USER WITH PASSWORD '$PSSWD'"
  #$PSQL_USER $PSQL_COMMAND "GRANT SELECT ON DATABASE $DB_NAME TO $DB_USER"
  $PSQL_USER $PSQL_COMMAND "GRANT SELECT ON pg_stat_database TO $DB_USER"
}

function test_user() {
  # Test if postgres connection is successful
  echo "Testing $DB_USER with password $PSSWD"
        /usr/bin/expect <<- DONE
    set timeout -1
    log_user 0
    spawn /usr/bin/psql -h localhost -U $DB_USER postgres -c "select * from pg_stat_database LIMIT(1);"
    # Look for passwod prompt
    expect "Password for user $DB_USER: "
    # Send password aka $PSSWD
    send -- "$PSSWD\r"
    send_user "Password was successful, '\q' quitting out of database view."
    send -- "\r"
    send -- "q"
    expect eof
        DONE
}

function config_agent() {
  #Configure the agent to connect to the PostgreSQL server
  cat > /etc/dd-agent/conf.d/postgres.yaml <<EOF
  init_config:

  instances:
     -   host: localhost
         port: 5432
         username: $DB_USER
         password: $PSSWD
         tags:
              - Database:DBTest
              - Script:Success

EOF

  #Restart Datadog-Agent
  sudo service datadog-agent restart && echo "Datadog Agent has been restarted."
}

function final() {
  if [ $user_int -eq  1 ]; then
    install_postgres && create_db
  elif [ $user_int -eq 2 ]; then
    install_postgres && create_user && auth_priveledge && test_user
  elif [ $user_int -eq 3 ]; then
    install_postgres && create_user && create_db && auth_priveledge && test_user && config_agent
  else
    echo "Final function has failed & case statement failed to catch it."
fi

}

final

exit 0
