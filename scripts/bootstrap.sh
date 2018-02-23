#!/usr/bin/env bash

# Input your information here

your_api_key='5b51a3a01c54d8424999428fb4298de4'
username='datadog'
password='monitoring'

# Check for API key.

if [ -z "$your_api_key" ]
then
	echo >&2 "Your API Key is missing, The datadog agent will not install / Run."
fi

# Create a Variable for tags formatted as a string or list 

tags="name:knunez, env:alpha, role:database"

 apt-get update

# Install desired packages, if already installed nothing will be done. (This will install the latest version, keep in mind if you require a specific version of a package.)

 apt-get install -y git htop

# Install / Configure DataDog Agent.

if dpkg-query -W datadog-agent; then
	echo >&2 "Datadog is already installed."
else
	DD_API_KEY=$your_api_key bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
fi

# Backup current datadog.conf and set tags in configuration according to variabl

if [ -e /etc/dd-agent/datadog.conf ] 
then
	sudo sh -c "sed -i.bk 's/^.* tags:.*/ tags: $tags/' /etc/dd-agent/datadog.conf"
else
	echo >&2 "Datadog.conf was missing, setting DD_API_KEY & tags"
	sudo sh -c "sed 's/^.* tags:.*/ tags: $tags/' /etc/dd-agent/datadog.conf.example > /etc/dd-agent/datadog.conf"
	sudo sh -c "sed 's/^.*api_key:.*/api_key: $your_api_key/' /etc/dd-agent/datadog.conf.example > /etc/dd-agent/datadog.conf"
fi

# Configure postgres datadog integration & Credentials

if grep -q '^.* tags:.* role:database*' /etc/dd-agent/datadog.conf;
then
	echo >&2 "Running postgres config."
	apt-get install -y postgresql postgresql-contrib
	update-rc.d postgresql enable
	service postgresql start
	if [ -z "$username" ]
	then 
		echo >&2 "You username appears to be missing, if this is your first run please enter the desired username."
	else
		if [ -z "$password" ]
		then 
			echo >&2 "Your password appears to be missing, if this is your first run please enter the desired password."
		else
			sudo -u postgres psql -c "CREATE USER $username WITH PASSWORD '$password';"
			sudo -u postgres psql -c "GRANT SELECT ON pg_stat_database TO $username;"
			# Checking if postgres data dog integration file is present & Configuring Credentials.
			if [ -e /etc/dd-agent/conf.d/postgres.yaml ]
			then
				echo >&2 'Starting configuration of postgres dd intergration'
				sudo sh -c "sed -i.bk 's/^.* username:.*/\    username: $username/' /etc/dd-agent/conf.d/postgres.yaml"
				sudo sh -c "sed -i.bk 's/^.* password:.*/\    password: $password/' /etc/dd-agent/conf.d/postgres.yaml"
			else
				echo >&2 'Copying example postgres integration file'
				echo >&2 'Starting configuration of postgres dd intergration'
				sudo sh -c "sed 's/^.* username:.*/\    username: $username/' /etc/dd-agent/conf.d/postgres.yaml.example > /etc/dd-agent/conf.d/postgres.yaml"
				sudo sh -c "sed -i.bk 's/^.* password:.*/\    password: $password/' /etc/dd-agent/conf.d/postgres.yaml"

			fi
		fi
	fi
else
	echo >&2 "This is not a Database Server"
fi

# Restart / Reload the datadog configuration

service datadog-agent restart

