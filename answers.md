##### My answers are below:
-------------------------------------------------------------------------------
## Prerequisites - Setup the environment
### Spinning up a fresh linux VM via Vagrant
  - Per the instructions I go here: https://www.vagrantup.com/intro/getting-started/
  - Install Vagrant and VirtualBox using the download links on the page
  - In terminal, input the first 'Up and Running' command:
    ![Get a Vagrantfile](/assets/setup/Get_a_vagrantfile.png)
  - Use vagrant up to bring up the machine
    ![vagrant up](/assets/setup/vagrant_up.png)
  - And ssh into the machine using vagrant ssh
    ![vagrant ssh](/assets/setup/vagrant_ssh.png)
  - Run vagrant init as detailed in instructions here: https://www.vagrantup.com/intro/getting-started/project_setup.html
  - That throws an error saying 'The program 'vagrant' is currently not installed.' Terminal says to install it with sudo apt-get install vagrant, so I try that.
  - I still get an error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
  - Neither of those work, so I google and find this link:    
    https://askubuntu.com/questions/364404/e-unable-to-fetch-some-archives-maybe-run-apt-get-update-or-try-with-fix-mis
  - Which tells me to try this: sudo apt-get update. And that seems to work!
    ![apt-get update](/assets/setup/apt_get_update.png)
  - Then I run sudo apt-get install vagrant again. Yaas, this works! So I run vagrant init and get this message:
    ![vagrant init](/assets/setup/vagrant_init.png)
  - I run vagrant box add hashicorp/precise64 and get an error. Curious, I click ahead in the instructions and realize I'm already done and this step was unnecessary.
    ![install box](/assets/setup/install_box.png)
  - So I open up Virtual Box and it seems it's up and running!
    ![virtual box](/assets/setup/virtual_box.png)
### Signing up for Datadog    
  - On the Datadog signup page here: https://app.datadoghq.com/signup I follow the steps to sign up:
    Filling out form info:
    ![sign up 1](/assets/setup/signup_1.png)
    ![sign up 2](/assets/setup/signup_2.png)

    I want to install the agent on Ubuntu so I use these directions:
    ![agent setup instructions](/assets/setup/agent_setup.png)
    I paste the one step install step into terminal, where I'm told I need to install curl:
    ![one_step_install_first_try](/assets/setup/one_step_install_first_try.png)
    So I run this: sudo apt-get install curl
    And then try the one step install line again, which gives me this:
    ![agent_install_confirmation](/assets/setup/agent_install_confirmation.png)
    And on the Datadog site, I get a message that the Agent is reporting!
    ![agent_reporting](/assets/setup/agent_reporting.png)
    I click finish and am in!
    ![welcome_page](/assets/setup/welcome_page.png)

## Collecting Metrics
### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  - To do this I creep around the Datadog Docs until I find this: https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files
  - This link: https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#configuration tells me that I need to go to /etc/datadog-agent/datadog.yaml to find the configuration files and folders for the Agent.
  - So I cd into the /datadog-agent folder, where I see the datadog.yaml file
    ![datadog-agent folder](/assets/metrics/datadog-agent.png)
  - I run sudo vim datadog.yaml to get into the yaml file, and scroll down until I see the tags section:
    ![tags section](/assets/metrics/tags_section.png)
  - This link: says the first method below is valid for tags
    ![ways to put in tags](/assets/metrics/ways_to_put_tags_in.png)
    so I press I to edit text, and enter in this info:
    ![new tags](/assets/metrics/add_tags.png)
    Then press :wq to save and ESC out of vim.
  - I don't see the tags showing up in my host map, so I google around and read here: https://docs.datadoghq.com/agent/basic_agent_usage/windows/#starting-and-stopping-the-agent that 'Any time you modify a Datadog integration you’ll need to restart the Datadog Agent service
  - this page: https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#commands says the restart command is: sudo service datadog-agent restart
  - So I try it in terminal:
    ![restart agent](/assets/metrics/restart_agent.png)
  - And when I refresh my host map, the tags are there!
    ![tags](/assets/metrics/tags.png)

### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.   
  - Part 1: Install a database on your machine (MongoDB, MySQL, or PostgreSQL)
    - I google around and find this link: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04 to download PostgreSQL
    - Which says to use these two commands in terminal:
      sudo apt-get update
      sudo apt-get install postgresql postgresql-contrib
    - And that seems to work!  
      ![install postgres](/assets/metrics/install_postgres.png)

  - Part 2: Install the respective Datadog integration for that database
    - https://docs.datadoghq.com/integrations/postgres/
    - To start psql on my PostgreSQL database, I use instructions from here (https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04) and type sudo -i -u postgres in terminal, and then psql to access the Postgres prompt:
      ![access postgres prompt](/assets/metrics/access_postgres_prompt.png)
    - Then I create a user (datadog) and grant datadog access with these command prompts, following directions found here: https://docs.datadoghq.com/integrations/postgres/#prepare-postgres
    ![create_user](/assets/metrics/create_user.png)
    - Then I freak out because I copied and pasted the create user command without changing the password (so currently datadog's password is <PASSWORD>)
    - So I take a quick detour and find this link: https://stackoverflow.com/questions/12720967/how-to-change-postgresql-user-password
    - The above link says I can do this to change the password, and it seems to work:
      ![change password](/assets/metrics/change_password.png)
    - So I run the command to verify the correct permissions, which prompts me for my (new) password:
      ![password prompt](/assets/metrics/password_prompt.png)
    - And that works! I get this!
      ![success](/assets/metrics/success.png)
    - The last step is to edit the postgres.d/conf.yaml file in the conf.d/ folder. so I cd into that folder:
      ![cd into postgres.d](/assets/metrics/postgres_d.png)
    - And run sudo vim conf.yaml:
      ![conf.yaml](/assets/metrics/conf_yaml.png)
     and then copy everything from here: https://github.com/DataDog/integrations-core/blob/master/postgres/conf.yaml.example
    into Terminal
    - Then I scroll up to this part and update the username, password, and dbname
      ![update info](/assets/metrics/update_info.png)
    - I grab the restart command from  https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#commands says the restart command is: sudo service datadog-agent restart so I run it:
      ![restart agent after postgres](/assets/metrics/restart_agent_after_postgres.png)
    - This link: https://docs.datadoghq.com/integrations/postgres/#validation says to run the status subcommand and 'look for postgres under the Checks section'. So I run sudo datadog-agent status and scroll down to the Checks section:
    - Alas! There's an error saying database "pg_stat_database" doesn't exist
      ![postgres error](/assets/metrics/postgres_error.png)
    - My guess as to this error is: when I edited the conf.yaml folder, I named the db pg_stat_database, but I think that's not actually the name of the database and I should have left that section blank. So I cd into the postgres.d folder, and then run sudo vim conf.yaml to comment out the db name:
      ![edit conf.yaml](/assets/metrics/edit_conf_yaml.png)
    - I run the restart command: sudo service datadog-agent restart
      ![restart agent second try](/assets/metrics/restart_agent_V2.png)
    - I run sudo datadog-agent status again to see if Postgres looks normal, and this time it does look normal! I see it in the Checks section!
      ![successful postgres](/assets/metrics/successful_postgres_integration.png)
    - Also I see it on my Host Map page:
      ![postgres in host map](/assets/metrics/host_map_with_postgres.png)

### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  - I start by going to this link: https://docs.datadoghq.com/developers/agent_checks/#configuration
  - Reading the directions, it seems like I should start by making a hello check
    - So I cd into conf.d and run sudo vim hello.yaml
      ![make hello yaml](/assets/metrics/make_hello_yaml.png)
    - And copy and paste this in:
      ![hello yaml](/assets/metrics/hello_yaml.png)  
    - And then cd info checks.d and run sudo vim hello.py
      ![make hello py](/assets/metrics/make_hello_py.png)
    - And copy and paste this in:
      ![hello py](/assets/metrics/hello_py.png)
    - This link: https://docs.datadoghq.com/developers/agent_checks/#putting-it-all-together says to restart the agent for changes to be enabled so I run the restart command: sudo service datadog-agent restart
    - And then run this: sudo -u dd-agent -- datadog-agent check hello
    - It looks like this works!
      ![check hello](/assets/metrics/check_hello.png)
  - Okay now that we've made a hello check, we need to do something very similar except the metric name is my_metric instead of hello.word, and the value will be a random value between 0 and 1000 instead of 1.
    - So lets go back into conf.d and run sudo vim my_metric.yaml and paste this into the file
      ![my metric.yaml](/assets/metrics/my_metric_yaml.png)
    - And then cd info checks.d and run sudo vim my_metric.py
    - I google and find this link with directions to find a random number (I'm going to assume an integer is okay) from 1 to 100. I'll tweak this for my purposes: https://pythonspot.com/random-numbers/
    - I paste this into the my_metric.py file:
      ![my metric.py](/assets/metrics/my_metric_py.png)
    - I run the restart command: sudo service datadog-agent restart  
    - And then run this: sudo -u dd-agent -- datadog-agent check my_metric
    - It looks like this works!
      ![check my metric](/assets/metrics/check_my_metric.png)

### Change your check's collection interval so that it only submits the metric once every 45 seconds.   
  - I see here: https://docs.datadoghq.com/developers/agent_checks/#configuration that the example has a min_collection_interval line in the yaml, so I will edit that.
  - I cd into conf.d and run sudo vim my_metric.yaml to make this edit:
    ![add interval](/assets/metrics/add_interval.png)
  - I run the restart command: sudo service datadog-agent restart  
  - This time I go to the Metrics Explorer in the dashboard to make sure I'm collecting a metric at regular intervals. It seems like it's working from this graph:
    ![metrics_explorer](/assets/metrics/metrics_explorer.png)
    Note - the values are all between 1 and 100 for a while because I accidentally set the random value to be between 1 and 100 for a while, and then changed it to be between 0 and 1000 when I noticed.

### Bonus Question Can you change the collection interval without modifying the Python check file you created?  
    Yep! I only edited the yaml file above.

## Visualizing Data
### Utilize the Datadog API to create a Timeboard that contains:
  - Your custom metric scoped over your host.
  - Any metric from the Integration on your Database with the anomaly function applied.
  - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

  Okay so here's a list of things I need to figure out, with links I find helpful:
  - how to make a timeboard, so find instructions here:
    - I find instructions here: https://docs.datadoghq.com/api/?lang=python#create-a-timeboard
    - and I think the instructions above have directions for 'your custom metric scoped over your host'
  - Any metric from the Integration on your Database with the anomaly function applied.
    - Here's a list of metrics: https://docs.datadoghq.com/integrations/postgres/#metrics
    - Anomaly function: I think I need this: https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api
  - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. Info about rollups, I found here: https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time
  - I plan to use Postman to make API calls, and when I google around to see if there might be a tutorial, I find this link: https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs

  Cool, so I think I have an idea of what to do.   
  - First things first: The sample code on https://docs.datadoghq.com/api/?lang=python#create-a-timeboard suggests I need an APP KEY and an API Key.
  - I navigate to here: https://app.datadoghq.com/account/settings#api where I see I already have an API key, and I click 'Create Application Key' to make an App key
    ![make app key](/assets/visualizing_data/make_app_key.png)
  - Next I navigate to this tutorial: https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs, but I get an error!
    ![error](/assets/visualizing_data/error.png)
  - So I try the same link in Safari and it works for me:
    ![tutorial](/assets/visualizing_data/tutorial.png)
  - Per their instructions I download Postman
  - Then I download the Datadog Postman Collection from the download link and save it to my Desktop
  - Per the tutorial directions, I replace all instances of INSERT_API_KEY_HERE with my API Key of cc93d681a5105d4f54f3e9907f7167a6
    ![replace API key](/assets/visualizing_data/replace_API_key.png)
  - I do the same and replace INSERT_APP_KEY_HERE  with 381ed52d16440f81418d3d3aa315a6fba0aa3ae5
    ![replace APP key](/assets/visualizing_data/replace_APP_key.png)
  - Now it's time to import the Datadog Postman Collection:  
    - Per the instructions, I click on File > Import, drag and drop the postman_collection json file in, and click on 'Collections' to see this:
    ![datadog collection](/assets/visualizing_data/datadog_collection.png)
  - I navigate to the Timeboards Collection and click on 'Create a Timeboard' to see this:
    ![create timeboard](/assets/visualizing_data/create_timeboard.png)
  - Just to check that this works, I update the description to read 'SAMPLE EXAMPLE - A dashboard with memory info.' and click SEND
    ![make sample timeboard](/assets/visualizing_data/make_sample_timeboard.png)
  - I get this response in Postman:
    ![sample timeboard response](/assets/visualizing_data/sample_timeboard_response.png)
  - And in the Dashboards section list I see the sample one I made:
    ![sample dashboard](/assets/visualizing_data/sample_dashboard.png)
  - So my guess is, we need to update the code in the body to reflect the three things we want in our new timeboard, and then we'll see a successful response and timeboard in the Dashboard
    - For the first part of the request, 'Your custom metric scoped over your host', I follow the format outlined here: https://docs.datadoghq.com/getting_started/from_the_query_to_the_graph/
      - There is no function or space-aggregration, the scope can be left as { * } since there's just one host, and there's no time-aggregation, so I think I only have to update the metric portion so the request reads:  {"q": "my_metric{* }"}
    - For this part: Any metric from the Integration on your Database with the anomaly function applied.
      - I pick a metric of postgresql.database_size from the list here, because one time at work my database ran out of disk space and now I'm obsessed with disk space: https://docs.datadoghq.com/integrations/postgres/#data-collected
      - I update the request to include: :
        - an anomaly function
        - An updated metric name of postgresql.database_size
        - I leave out a space-aggregation because I don't think we're looking for an average
        - I leave the host as * since there's just the one host
        - There's no time-aggregation so I leave that out
        - I also add the 'basic' anomaly detection algorithm
        - This link (https://docs.datadoghq.com/graphing/miscellaneous/functions/#anomalies) says there should be a second parameter, bounds, and a value of 2 or 3 should be large enough to include normal points, so I add that in
        - Note: This link (https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api) has various other options but I think they are optional so I leave things alone and just use what I have below. Worst case scenario, the timeboard doesn't make sense and I have to redo some things:

          {"q": "anomalies(postgresql.database_size{* }, 'basic', 2)"}
    - For the third part: Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
      - Okay documentation for rollup functions is here: https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1
      - And luckily, the doc I've been using to format my queries has a rollup function in there: https://docs.datadoghq.com/getting_started/from_the_query_to_the_graph/
      - Again, I don't think we have any space-aggregation (although I think we will use 'sum' as one of the arguments in the rollup function) so I leave that out
      - the metric name I change to my_metric
      - the host I leave as is because there is only one host
      - I add .rollup(sum, 3600) because we want the sum of all the points, and if time is in seconds (based on this: https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1), 60 minutes is 3600 seconds

      - {"q": "my_metric{* }.rollup(sum, 3600)"}
    - My final request looks like this:
      ![timeboard request](/assets/visualizing_data/timeboard_request.png)
    - I click "Send" and get a 200 response:
      ![timeboard response](/assets/visualizing_data/timeboard_response.png)
    - And in the All Dashboards page I do see my new dashboard!
      ![all dashboards list](/assets/visualizing_data/all_dashboards_list.png)
    - Ack! Some of the graphs look blank though:
      ![timeboard v1](/assets/visualizing_data/timeboard_v1.png)
    - I change the time range to reflect 1 day instead of 1 hour and I do see the rollup graph change:
      ![timeboard v2](/assets/visualizing_data/timeboard_v2.png)
    - I'm not totally sure why the anomaly graph looks blank though. Maybe there are just no anomalies? That seems unlikely, though.
    - Using the GUI, I edit the 'basic' checking to 'robust', and also update the bounds to '1' , but the graph looks the same. :( So I switch back to the way things were.

### Access the Dashboard from your Dashboard List in the UI. Set the Timeboard's timeframe to the past 5 minutes
  - I stumbled upon this my accident while I was clicking all around my empty graphs, trying to figure out what was wrong.
  - If you click a point on the graph and drag your mouse, the timeboard will show only that timeframe
  - This is what 5 minutes looked like for me:
    ![5 minutes timeboard](/assets/visualizing_data/5_minutes.png)

###Take a snapshot of this graph and use the @ notation to send it to yourself.
  - This is intuitive: I click on the camera icon here:
    ![camera icon](/assets/visualizing_data/click_blue_camera.png)
  - I write a note and @ my email, and then when I press enter it sends to my email:
    ![send message](/assets/visualizing_data/send_message.png)
    ![email](/assets/visualizing_data/email.png)

### Bonus Question: What is the Anomaly graph displaying?
    Sadly my anomaly graph isn't displaying anything but it should display the value of a selected metric, and also show when that value is different from what it normally is. The algorithm takes into account trends, day of the week, and time-of-day patterns. I learned all this here: https://docs.datadoghq.com/monitors/monitor_types/anomaly/

Monitoring Data
  - Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

  Warning threshold of 500
  Alerting threshold of 800
  And also ensure that it will notify you if there is No Data for this query over the past 10m.

    - So this link: https://docs.datadoghq.com/monitors/#creating-a-monitor tells me to go to the Create Monitors page here: https://app.datadoghq.com/monitors#/create
    ![create monitors page](/assets/visualizing_data/create_monitors_page.png)
    - In the resulting page, I:
      - Define the metric as my_metric
      - Set the Alert threshold to 800
      - Set the Warning threshold to 500
      - Change 'Do Not Notify' if data is missing to: "Notify" if data is missing for more than "10" minutes

    - My screen now looks like this:
    ![set alert conditions](/assets/visualizing_data/set_alert_conditions.png)

  - Please configure the monitor’s message so that it will:
    - Send you an email whenever the monitor triggers.
      - I do this in The Notify Your Team Section
    - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
      - Done in the 'Say what's happening section'
    - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
      - Done in the 'Say what's happening section'

    My screen now looks like this:
    ![configure alerts](/assets/visualizing_data/configure_alerts.png)
    - I click "Save"
  - When this monitor sends you an email notification, take a screenshot of the email that it sends you.
    ![warning email](/assets/visualizing_data/warning_email.png)  

  - Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    - One that silences it from 7pm to 9am daily on M-F,
    - And one that silences it all day on Sat-Sun.
    - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.  

    - Based on this link: https://docs.datadoghq.com/monitors/downtimes/#manage-downtime I navigate to this page:
      ![downtime page](/assets/visualizing_data/downtime_page.png)
    - I click on the Schedule Downtime button and fill in the following info for the weekday downtimes:
      ![weekday downtimes](/assets/visualizing_data/weekly_downtimes.png)
    - After I click "Save" I see it in my list of downtimes!
      ![downtime list v1](/assets/visualizing_data/downtime_list_v1.png)
    - And here's an email screenshot which gives the downtime in UTC:
      ![email](/assets/visualizing_data/weekly_downtime_email.png)

    So for the downtime meant for all day on Saturday and Sunday, I click on 'Schedule Downtime' again and fill in this info:
      ![weekend downtimes](/assets/visualizing_data/weekend_downtimes.png)
      Note: I tried including the downtime to start today (a Sunday) but got a notice saying downtimes couldn't be in the past so I've started this downtime for the next Saturday, June 16
      - After I click "Save" I see it in my list of downtimes!
        ![downtime list v1](/assets/visualizing_data/downtime_list_v2.png)
      - And here's an email screenshot which gives the downtime in UTC:
        ![email](/assets/visualizing_data/weekend_downtime_email.png)  

Collecting APM Data
  - First I read through the docs here: https://docs.datadoghq.com/tracing/ and here: http://flask.pocoo.org/docs/0.12/quickstart/
  - Then, to get started I watch this video here: https://www.youtube.com/watch?v=faoR5M-BaSwand decide to follow his instructions, which make everything seem simple. :D
  - Per his instructions I first go to https://app.datadoghq.com/apm/docs and click 'Get Started', which takes my to this page:
    ![report traces](/assets/apm/report_traces.png)
  - Just to double check what language to pick, I google and confirm it's Python:
    ![flask language](/assets/apm/flask_language.png)
  - So in terminal, I Install the Python client using pip install ddtrace
  - I get this message: The program 'pip' is currently not installed.  You can install it by typing:
sudo apt-get install python-pip
  - So I run sudo apt-get install python-pip, and then pip install ddtrace
    ![pip_install_ddtrace](/assets/apm/flask_language.png)
  - In terminal there's a weird message of:
    "Downloading/unpacking ddtrace
      Cannot fetch index base URL http://pypi.python.org/simple/
      Could not find any downloads that satisfy the requirement ddtrace
    No distributions at all found for ddtrace" so I wonder if I should open up my Flask App before proceeding (or maybe I should've done that before this step? Not sure, but I will do it now)
  - So, now to set my Flask app up!
    - First I need to install Flask based on instructions here: http://flask.pocoo.org/docs/0.12/installation/#installation
    - So I run this: sudo apt-get install python-virtualenv, which seems to set up a virtual environment
      ![virtual_env](/assets/apm/virtual_env.png)
    - The next step in the installation instructions is to create your own environment:
      - I ignore this for now because I'm not sure that's what I want? If it is I can come back to it later.
    - I run pip install Flask but am not sure this is what I'm supposed to see:
      ![install Flask](/assets/apm/pip_install_Flask.png)
    - anyway so back to these docs: http://flask.pocoo.org/docs/0.12/quickstart/
    - I make a file called my_flask_app.py and save the contents of the app in there   
      ![Flask app v1](/assets/apm/initial_Flask_app.png)  
    - And I try running the commands needed to get the app running but get an error:
      ![Flask not found](/assets/apm/flask_not_found.png)  
    - so I google around and find this link: https://stackoverflow.com/questions/30227360/installed-flask-in-a-virtualenv-yet-command-not-found. I try all the solutions listed here but none work.
    - So on a whim I go back to the Installation page and try this again: sudo apt-get install python-virtualenv
    And I think something good happens? At least, this is what I see in terminal:
      ![virtual env v2](/assets/apm/virtual_env_v2.png)
    - Then I try virtualenv venv in the terminal to create my own environment (maybe we do need one?) and see this:
      ![virtualenv venv](/assets/apm/virtualenv_venv.png)
    - Now that I'm on a roll, I activate the environment and then deactivate it, just out of curiosity:
      ![activate and deactivate](/assets/apm/activate_deactivate.png)
    - I try pip install Flask and still get this error:
      ![flask install error](/assets/apm/flask_error.png)
    - I'm not sure if this error is okay or not, so I just google the exact error (pip install flask Cannot fetch index base URL http://pypi.python.org/simple/) and the first link that shows up is: https://stackoverflow.com/questions/21294997/pip-connection-failure-cannot-fetch-index-base-url-http-pypi-python-org-simpl
    - I try all the solutions there and keep getting the same error :(
    - Time to try something else: I google around again and come upon this tutorial: http://hanzratech.in/2015/01/16/setting-up-flask-in-ubuntu-14-04-in-virtual-environment.html
      - I follow:
      sudo apt-get install python-virtualenv
      sudo apt-get install python-pip
      virtualenv --version
      mkdir flask-application
      cd flask-application
      Note- I think maybe my previous commands weren't working because I had put the flask app folder in the hiring engineers folder, but not within the vagrant VM. But lets see if it works now...
    - At this point my terminal looks like:
      ![in progress flask app](/assets/apm/in_progress_flask_app.png)  
    - Okay so I run virtualenv flask-env according to the directions and see this:
      ![flask env](/assets/apm/flask_env.png)
    - So I guess I successfully created a virtual environment. Now I try activating it with: source flask-env/bin/activate
    - And then try this again: pip install Flask
    - Ugh I get this again:
      ![flask error v2](/assets/apm/flask_error_v2.png)
    - Let me trying cd-ing into the logs folder... ah okay so it seems there is an SSL issue:
      ![error log](/assets/apm/error_log.png)
    - Okay I go back here: http://flask.pocoo.org/docs/0.12/installation/ and the 'Living on the Edge' section:
      sudo apt-get install git
      sudo git clone http://github.com/pallets/flask.git (tried without sudo and it didn't work)
      cd flask
      sudo virtualenv venv
    - ![install pip again](/assets/apm/install_pip.png)  
    then i run: . venv/bin/activate
    sudo python setup.py develop
    and my screen looks like what's below. I'm not totally sure if this worked but will forge ahead!
    - ![flask installed](/assets/apm/flask_installed.png)
- Um. Okay I go back to: https://app.datadoghq.com/apm/install and see the command for instrumenting my application (I've made a new file called my_flask_app.py and copied the app in there)
- Lets just run it and see what happens.. ack! more errors!
  - ![more errors](/assets/apm/more_errors.png)
- Okay lets change tracks and try doing this with a Ruby app...
- I'll try making a quick new Rails app using instructions here: http://guides.rubyonrails.org/getting_started.html
- First I run gem install rails in my terminal to get this:
  - ![gem install rails](/assets/apm/gem_install_rails.png)
- then I run rails new blog to make an app called 'blog', and cd into it:
  - ![rails new blog](/assets/apm/rails_new_blog.png)
- Then I boot up the rails server with: bin/rails server
  - ![rails server](/assets/apm/boot_rails_server.png)
- and go to localhost:3000 to confirm that stuff works so far...
  - ![localhost](/assets/apm/localhost.png)
- all right, lets quickly create a welcome page so the app does something...
  I run: bin/rails generate controller Welcome index in terminal to create a Welcome controller and "Index" action.
    - ![welcome controller](/assets/apm/welcome_controller.png)
- And then edit the text a user sees on the welcome page:
  - ![edit welcome page text](/assets/apm/edit_welcome_page.png)
- Just to double check that it works I go back to http://localhost:3000/welcome/index and see this:
  - ![app homepage](/assets/apm/app_hp.png)
- Okay cool. It's simple but it is technically a Ruby on Rails app.
- So following the instructions here: https://app.datadoghq.com/apm/install for Ruby, I run gem install ddtrace in terminal to install the Ruby client
  - ![gem install ddtrace](/assets/apm/gem_install_ddtrace.png)
- Then I click on the Rails directions to see this:
  - ![rails directions](/assets/apm/rails_directions.png)
- Per the directions, I make a file in config/intializers/datadog-tracer.rb that looks like this:
  - ![datadog tracer](/assets/apm/ddtracer.png)
- I go back here: https://app.datadoghq.com/apm/install but nothing has changed

And that's when I realize... I made a rails app in the hiring-engineers directory, but I think I should have made the new app while in my VM!!!
... Okay real quick I do the same thing I just did, except in the terminal tab with my VM.
Here are the terminal commands I use, in order:
sqlite3 --version
sudo apt-get install sqlite3
gem install rails
sudo gem install rails
sudo apt-get install ruby-rvm (I get an error saying my Ruby is out of date so google and find this command)
rvm install ruby --latest (to update to the latest Ruby version)
sudo gem install rails
sudo apt-get install rbenv (because Ruby was still too old)
sudo apt-get install ruby2.3 ruby2.3-dev (because nothing else worked)
sudo apt-get update (seems ruby is still an old version)
Ugh everytime I try ruby -v it says I have version 1.8.7
So I follow this link:
https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-with-rbenv-on-ubuntu-16-04

And try:
sudo apt-get install autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc
type rbenv
Which does show me this, and Digital Ocean says that is how it's supposed to be:
  - ![rbenv](/assets/apm/rbenv.png)
I keep blindly following this tutorial and type:
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
rbenv install -l
rbenv install 2.5.0
rbenv global 2.5.0
ruby -v
And it seems I finally have an updated version of Ruby now:
  - ![updated ruby](/assets/apm/updated_ruby.png)
okay so now I can proceed with installing rails based on the instructions here: http://guides.rubyonrails.org/getting_started.html  
  gem install rails gives me this:
    - ![gem install rails](/assets/apm/gem_install_rails_2.png)
  I confirm rails is installed by running: rails --version  
  Then create a new app called blog2 with: sudo rails new blog2
  Then cd into the folder with: cd blog2. Here's how my terminal looks:
  - ![cd into blog2](/assets/apm/cd_into_blog2.png)
- All right, now lets boot up our rails server:
  - I get an error saying 'There was an error while trying to load the gem 'uglifier'. (Bundler::GemRequireError)' which I google to find this article: https://stackoverflow.com/questions/34420554/there-was-an-error-while-trying-to-load-the-gem-uglifier-bundlergemrequire which tells me to run 'sudo apt-get install nodejs'
  - After that I run: sudo bin/rails server
  Which works!
  Terminal screenshot:
    - ![rails server 2](/assets/apm/rails_server_2.png)
  Actually when I go to localhost:3000 it says the site can't be reached.
    - ![site can't be reached](/assets/apm/site_cant_be_reached.png)
  I'm wondering if that's because I'm in a VM though, so I keep trekking along...
  Based on the instructions here: https://app.datadoghq.com/apm/install
  I run gem install ddtrace:
    - ![gem install ddtrace2](/assets/apm/gem_install_ddtrace2.png)
  Next I need to implement the Rails specific instructions here:
    - ![rails_instructions](/assets/apm/rails_instructions.png)
  So I cd into the config/initializer folder and create a datadog-tracer.rb file
    - ![tracer file](/assets/apm/tracer_file.png)
  I copy and paste the info in:
    - ![updated tracer file](/assets/apm/updated_tracer_file.png)
  Okay after a few minutes my apm install page looks the same, so I think something went wrong. I run the command bundle info ddtrace to see where it is, and get this message:
    - ![missing gem](/assets/apm/missing_gem.png)
  Okay so I think something went wrong with my original installation method, let me try going into the Gemfile and manually adding it...
  - I sudo vim Gemfile to open it up and add the ddtrace gem
    - ![add ddtrace gem](/assets/apm/add_ddtrace_gem.png)
  - Then I run sudo bundle install, and I do see the gem!
    - ![ddtrace is here](/assets/apm/ddtrace_is_here.png)
  - So I wander around the Datadog docs, wondering where I went wrong, and see this: https://docs.datadoghq.com/tracing/setup/
  And I remember - I think when I was dealing with all the Flask install drama, I totally forgot to go through the APM Setup process!
  So I go back into my datadog.yaml and file and comment back in this part:
    - ![apm_config_true](/assets/apm/apm_config_true.png)
  And restart my agent with: sudo service datadog-agent restart
  Still nothing.
  hmm, I go into my datadog. yaml file and change to this:
    - ![env_none](/assets/apm/env_none.png)
  And restart my agent with: sudo service datadog-agent restart
  Hmm, still nothing
  I see this: https://docs.datadoghq.com/tracing/setup/ruby/#compatibility and wonder if my Ruby version is too new. So I go back to the Digital Ocenan Ruby link: https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-with-rbenv-on-ubuntu-16-04
  and run rbenv install 2.4.0 to install Ruby v 2.4
  then I run rbenv global 2.4.0 to set that as my global version, and running ruby -v shows that's successful:
    - ![ruby v](/assets/apm/ruby_v.png)
  hmm I remember when I was in the datadog.yaml file I saw something about SSLs. I also remember that the log stuff from the Flask drama had to do with SSL. I'll try commenting it back in and telling the agent to skip validation and just... see what happens.
  https://cl.ly/1u0w0Y0G3q0C
  Not sure if it's too early or not but I restart the agent: sudo service datadog-agent restart
  Still get this error - https://cl.ly/2Q112k291v2A
  Hmm okay I'll go back and comment out the SSL stuff:
    - ![comment out ssl again](/assets/apm/comment_out_ssl_again.png)

Okay time to change tactics: I google around for a Datadog APM tutorial and find this: https://github.com/DataDog/trace-examples/tree/master/ruby
So I decide to try instrumenting the basic Ruby app. Surely if this is a Datadog example, it will work? And if it doesn't I'll be able to assume I messed up somewhere in the configuration/setup phase.
Okay so the sample app is here that I'm going to use. So while in my VM I run gem install ddtrace:
  - ![gem install ddtrace](/assets/apm/gem_install_ddtrace3.png)
  (Note - why does it say I installed two gems at the end? I have no idea.
  -  Then create a file called my_app.rb
    - ![my_app.rb](/assets/apm/my_app.png)
  - Then I run sudo vim my_app.rb to get into it, and copy in the info from the same ruby app:
    - ![ruby_app](/assets/apm/ruby_app.png)
  - Then according to documentation I wrap the Datadog.tracer.trace around the app like so:
    - ![add trace](/assets/apm/add_trace.png)
  - I restart the agent but still am not seeing traces.

Okay let me start totally from scratch because something is wrong with the tracing, I think.
I uninstall the agent with:  sudo apt-get --purge remove datadog-agent -y
Download the Mac OS X agent with: DD_API_KEY=cc93d681a5105d4f54f3e9907f7167a6 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"
I exit my VM and just run the Mac OS X agent on my computer
https://cl.ly/3A412B0V2e2B
Once that's done, I have two hosts! How exciting!
https://cl.ly/3C1T3h3L3Y2v
Okay that's step 1 of the directions here: https://docs.datadoghq.com/tracing/setup/#setup-process
Now for step 2: I go here: https://github.com/DataDog/datadog-trace-agent#run-on-osx
- and download the latest OSX Trace Agent release
- I run this: but nothing happens: ./trace-agent-osx-X.Y.Z -config /opt/datadog-agent/etc/datadog.conf
- I try a couple of variations of this (adding version name instead of X.Y.Z., etc. but they don't work). I google around and find this is an issue: https://github.com/DataDog/datadog-trace-agent/issues/397 but see someone got it working with an old version here: https://github.com/DataDog/datadog-trace-agent/releases?after=5.21.1
- Nvm just reinstall the Ubuntu agent: DD_API_KEY=cc93d681a5105d4f54f3e9907f7167a6 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
- Edit yaml file: https://cl.ly/0N1H2s3H1a0E
- Restart agent: sudo service datadog-agent restart
- Still nothing...
For now I just move on...

EDIT - Okay coming back to this!
- In my VM, I make a new file and copy the Flask app in there.
  - ![make new flask app](/assets/apm/make_new_flask_app.png)
- I run pip install ddtrace but get the same error I've been getting_startedhttps://cl.ly/013x0F1z2X1f
- One thing I saw while trying to debug was 'installing from source' so I look up a tutorial and find this: https://www.howtogeek.com/105413/how-to-compile-and-install-from-source-on-ubuntu/
  - I run sudo apt-get install build-essential
  - I go here to find source files: https://pypi.org/project/ddtrace/#files and download them
  - I guess and make a shared folder  according to
  https://cl.ly/1W2P2K2v151V
Actually let me see if making a new VM does the trick...
vagrant destroy
delete old Vagrantfile
 vagrant init hashicorp/precise64
 vagrant up
 vagrant ssh to get this:
 https://cl.ly/3r2G1S1P2R08
 One step Ubuntu agent install: DD_API_KEY=cc93d681a5105d4f54f3e9907f7167a6 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

And I see this: https://cl.ly/0w0f1Z2S180K
Agent successfully installed!
sudo vim app.py to make a new file for the app, copy flask app in there
pip install ddtrace
Get this message: https://cl.ly/3t0X3W1e1H0e
sudo apt-get install python-pip - from this link here: https://askubuntu.com/questions/672808/sudo-apt-get-install-python-pip-is-failing
I try this pip install ddtrace again: AND IT WORKS
https://cl.ly/0l0I2a2s3x0V
Then try:
ddtrace-run python app.py
It gives me a 'no module for Flask error'
So I just replace the flask app with the same python app here: https://github.com/DataDog/trace-examples/blob/master/python/sample_app.py
I run this again: ddtrace-run python my_app.py
And I see stuff in my console!!!!! https://cl.ly/0u3V3Z1G1u1j
AND I see a message saying my first traces are now available!!!!
(apm_dashboard_overview)
Here are my beautiful graphs:
APM graphs
https://cl.ly/0q2w381N2y2V
Link: https://app.datadoghq.com/apm/service/sample-app/request?start=1528856813185&end=1528860413185&env=none&paused=false
A copy of the instrument python app is in app.py. It's taken from here: https://github.com/DataDog/trace-examples/blob/master/python/sample_app.py
(Note: there is also a my_flask_app.py and rails blog folder in here from attempts that didn't work. I left them in here but they're not being used)





Bonus Question: What is the difference between a Service and a Resource?
  Based on this link: https://docs.datadoghq.com/tracing/visualization/#services a service is a set of process that does the same job (ie: a database). And a resource is a particular action for that service (so for example, an individual endpoint).

Final Question:  
- I'd love to see Datadog used to monitor noise levels around the city. There are things like this: https://mashable.com/2012/01/11/noisetube-noise-pollution/#_HU9y2nvs8qA that help to track noise pollution and all you need is a smartphone. If the technology that powers this used Datadog, it would allow users to see what locations in the city are the most quiet at any given time. Users could also segment data by time of day, or day of the week, or even season to know how to avoid noise pollution. One of my favorite things to do after work is go on long walks, but I hate hearing the sound of honking horns, so something like this would be perfect for me.
