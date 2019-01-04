DBHOST=localhost
DBNAME=dbname
DBUSER=dbuser
DBPASSWD=dbpasswd

# Enable apt https access
apt-get install apt-transport-https

# Update/upgrade packages
apt-get update
apt-get upgrade

# Initial Installations
apt-get install -y apache2       # Apache
apt-get install -y git           # Git

## MySQL ========================
    # Set MySQL Password
    debconf-set-selections <<< "mysql-server mysql-server/root_password password $DBPASSWD"
    debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DBPASSWD"

    # Install MySQL
    apt-get -y install mysql-server

    # Create a new database
    mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"

# Update again
apt-get update

# Enable Apache mods
a2enmod rewrite

# Restart Apache
service apache2 restart

# Install DataDog Agent and do NOT start the Agent
    # need to manually change datadog.yaml file, then run a datadog start command
DD_INSTALL_ONLY=true DD_API_KEY=<API-KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
