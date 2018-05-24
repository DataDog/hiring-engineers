Datadog answers.
===

## Prerequisites - Setup the environment

* First cloned the repo and made a branch called Iliyan\_Solutions\_Engineer.  
* Then downloaded and installed Vagrant and VirtualBox.  
* Made a directory inside hiring-engineers folder called vm.  
* Inside vm directory ran

    >vagrant init

  command that created a Vagrantfile.  
* Went on https://vagrantcloud.com/search to browse for vagrant boxes and chose a box 'ubuntu/xenial64'.  
* Opened Vagrantfile and replaced:  
    
    >config.vm.box = "base" to config.vm.box = "ubuntu/xenial64"
  
* On the command line ran.
  
    >vagrant box add ubuntu/xenial64
 
* Inside Vagrantfile changed the arguments of config.vm.synced_folder to:  

    >config.vm.synced_folder "../src/vm_files", "/vagrant_data". 

 
This made the files inside 'src/vm\_files' available to the vitrual machine inside  '/vagrant\_data'.  

* Signed up for a trial datadog account.  
* To install Datadog agent everytime Vagrant is up, provisioned the following inside Vagrantfile:

        DD_API_KEY=6caaef27352ea09f824410ddeea49c52 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"


## Collecting Metrics:

* To add tags in the agent config file as well as to get rid of some warning messages modified the above mentioned script to:

        DD_API_KEY=6caaef27352ea09f824410ddeea49c52 DD_HOST_TAGS=env:qa,role:service_db_a DEBIAN_FRONTEND=noninteractive bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"




<p align="center">
<img src="/src/screenshots/tags.png">
</p>


* To install the database added to Vagrantfile:
        
        apt-get install -y postgresql postgresql-contrib

* To set up a user added:

        su postgres -c "psql -c \\"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant'\\" "

* To create a database called sampledb added:

        su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O vagrant sampledb"

* To create a Datadog user with CREATEROLE privileges and grant access to pg\_stat\_database:

        su postgres -c "psql -c \\"CREATE USER datadog WITH PASSWORD 'Penhorse131'\\" "
        su postgres -c "psql -c \\"GRANT SELECT ON pg_stat_database TO datadog\\" "


* To configure the agent to collect PostgreSQL metrics,  added a file called datadog\_agent\_postgres\_conf.yaml  inside "../src/vm_files" that instructs the agent to access metrics locally:

        #postgres.yaml
        init_config:    
        instances:
         - host: localhost
           port: 5432
           username: datadog
           password: Penhorse131

* Then added to Vagrantfile the following line to copy that file from the synced folder '/vagrant_data/'  to '/etc/datadog-agent/conf.d/postgres.d/' as conf.yaml

        cp /vagrant_data/datadog_agent_postgres_conf.yaml /etc/datadog-agent/conf.d/postgres.d/conf.yaml

* After that added the following code to Vagrantfile to bounce Datadog's agent so the changes can take effect:

        service datadog-agent restart

* On the command line pressed ctrl-D to exit and from the vm folder restarted vagrant with the following commands:

>$vagrant destroy  
>$vagrant up  
>$vagrant ssh

* When vagrant restarted ran the following command as root to confirm the integration:

>datadog-agent status | less

<p align="center">
<img src="/src/screenshots/postgres-agent-integration.png">
</p>

---
To create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000 did the following:

* Created two files in "../src/vm_files" called mymetric.py and mymetric.yaml that became available in "/vagrant\_data"

* Added the following to Vagrantfile to copy the files to the right locations so they are available when Ubuntu daemon is running. 

        cp /vagrant_data/mymetric.yaml /etc/datadog-agent/conf.d/mymetric.yaml
        cp /vagrant_data/mymetric.py /etc/datadog-agent/checks.d/mymetric.py


* To set a random value for the check, in mymetric.py after importing random used:  

        random.randrange(0, 1001, 1)

  where the upper range of 1001 is not included and 1 is the step.  

  This is how mymetric.py looks after the change:


        import random
        from checks import AgentCheck
        class MyMetric(AgentCheck):
        def check(self, instance):
            self.gauge('my_metric', random.randrange(0, 1001, 1))

* To set the collection's interval so that it only submits the metric once every 45 seconds edited mymetric.yaml to:

        init_config:
        instances:
         - min_collection_interval: 45

note: (The collector  runs every 15-20 seconds and the interval is not precise)

<p align="center">
<img src="/src/screenshots/mymetric_with_45sec_interval.png">
</p>


## Visualizing Data:

For the "Visualizing Data" challenge I used the UI to create a timeboard with the required 3 graphs and checked the JSON representation of the graphs. Then followed Datadog's API docs to see an example request in Ruby. The script to create the timeboard is at:

    /src/source_monitoring/screenboard.rb

Inside the same directory created a 'Gemfile' with the following content:

    source 'https://rubygems.org'

    gem "dogapi"
    gem "pp"

In order to execute the ruby code entered the following commands inside the '/source_monitoring' folder:

>bundle install   
>bundle install dogapi   
>bundle install pp

note:(pp is not necessary. Installed to make debugging easier) 

To create the timeboard ran:

>ruby screenboard.rb


This produced the following result(screenshot taken couple of days after the timeboard was created):

<p align="center">
<img src="/src/screenshots/Iliyans_timeboard.png">
</p>

The Timeboard's timeframe set to the past 5 minutes with @ notation to send it to myself.

<p align="center">
<img src="/src/screenshots/timeboard-5min-interval.png">
</p>

Bonus Question: What is the Anomaly graph displaying?

Anomaly graph displays deviations from what is expected, based on historical trends.


## Monitoring Data

To create a monitor I used the UI with the following settings:

<p align="center">
<img src="/src/screenshots/monitor_setup.png">
</p>

Email notification:

<p align="center">
<img src="/src/screenshots/monitor_email_notification.png">
</p>

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* To schedule downtimes used the following setup.

<p align="center">
<img src="/src/screenshots/database_monitor_silenced.png">
</p>

<p align="center">
<img src="/src/screenshots/monitor_downtime_Sat_Sun.png">
</p>


* The scheduled downtimes produced the following emails:

<p align="center">
<img src="/src/screenshots/silenced_monitor_email.png">
</p>

<p align="center">
<img src="/src/screenshots/silenced_monitor_email_Sat_Sun.png">
</p>


## Collecting APM Data

For this exercise decided to go further and create a systemd service that will be responsible for starting the Flask app.

First created a file at '/src/vmfiles/' called flaskapp.py using the provided Flask app and added the following lines:

    import blinker as _
    from ddtrace import tracer
    from ddtrace.contrib.flask import TraceMiddleware

    traced_app = TraceMiddleware(app, tracer, service="flask_app", distributed_tracing=False)



Then added the following to Vagrantfile: 

* To install pip installer for python packages,
Flask, ddtrace and blinker:

        apt-get install -y python-pip
        pip install Flask ddtrace blinker

* To create a '/flaskapp' folder and copy 'flask_app.py' inside it:

        mkdir /usr/local/flaskapp
        cp /vagrant_data/flask_app.py /usr/local/flaskapp/flask_app.py

* In order to register a flask app as a systemd service created a user called flaskapp. This is not necessary but prevents the service from executing commands as root:

        useradd --system -s /bin/false flaskapp

Then created systemd service file called flaskapp.service in '/src/vm_files/flaskapp.service that starts flask_app.py using Flask on port 8080 with the following contents:

    [Unit]
    Description=Run a flaskapp service
    After=syslog.target network.target datadog-agent-trace.service
    
    [Service]
    SyslogIdentifier=flask_app
    User=flaskapp
    Group=flaskapp
    ExecStart=/bin/bash -c "cd /usr/local/flaskapp && FLASK_ENV=development FLASK_APP=flask_app.py flask run --port 8080"
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target


Back in Vagrantfile copied 'flaskapp.service' to the systemd services in the Linux environment:

    cp /vagrant_data/flaskapp.service /etc/systemd/system/flaskapp.service

And to enable and start the service added the following:

    systemctl enable flaskapp.service
    service flaskapp start


Restarted Vagrant and used curl to test the service:

    curl http://127.0.0.1:8080


<p align="center">
<img src="/src/screenshots/APM_flask_app.png">
</p>


Bonus Question: What is the difference between a Service and a Resource?

The difference is that while a 'service' is a set of processes that work together to provide a feature set(a single database service or a single webapp service), a 'resource' can be a query to a database or a canonical URL. 


Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

<p align="center">
<img src="/src/screenshots/custom_dashboard.png">
</p>

___
## Final Question:

Is there anything creative you would use Datadog for?

The first implementation that comes to mind is for a weather app. Datadog can be set to monitor and notify users if snow accumulation goes above certain range or there are extreme weather conditions.

Another implementation can be to monitor traffic and notify users so they can avoid traffic congestion. It can also be set to notify the authorities so someone can be sent to coordinate traffic at backed up intersections.

There are endless opportunities in agriculture, medicine and education system to name a few.










