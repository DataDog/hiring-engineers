Your answers to the questions go here.
-------------------------------------------------------------------------------

Prerequisites - Setup the environment
- Spinning up a fresh linux VM via Vagrant
  - Per instruction I go here: https://www.vagrantup.com/intro/getting-started/
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
  - Um, I think my earlier steps to get the Vagrantfile might have been enough and I didn't need to go through all that drama if vagrant init-ing. But oh well, onwards to Vagrant Boxes!
  - I run vagrant box add hashicorp/precise64 and get an error. Curious, I click ahead in the instructions and realize I'm already done and this step was unnecessary.
    ![install box](/assets/setup/install_box.png)
  - So I open up Virtual Box and it seems it's up and running!
    ![virtual box](/assets/setup/virtual_box.png)
- Signing up for Datadog    
  - On the Datadog signup page here: https://app.datadoghq.com/signup I follow the three steps to sign up
    Filling out form info:
    1. ![sign up 1](/assets/setup/signup_1.png)
    2. ![sign up 2](/assets/setup/signup_2.png)

    Installing the agent:
    3. I want to install the agent on Ubuntu so I use these directions:
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

Collecting Metrics
  - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
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

  - Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.   
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
        - fdsnoin113543
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
      -Then I scroll up to this part and update the username, password, and dbname
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
  - Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
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
  - Change your check's collection interval so that it only submits the metric once every 45 seconds.   
    - I see here: https://docs.datadoghq.com/developers/agent_checks/#configuration that the example has a min_collection_interval line in the yaml, so I will edit that.
    - I cd into conf.d and run sudo vim my_metric.yaml to make this edit:
      ![add interval](/assets/metrics/add_interval.png)
    - I run the restart command: sudo service datadog-agent restart  
    - This time I go to the Metrics Explorer in the dashboard to make sure I'm collecting a metric at regular intervals. It seems like it's working from this graph:
      ![metrics_explorer](/assets/metrics/metrics_explorer.png)
        Note - the values are all between 1 and 100 for a while because I accidentally set the random value to be between 1 and 100 for a while, and then changed it to be between 0 and 1000 when I noticed.
  - Bonus Question Can you change the collection interval without modifying the Python check file you created?  
    Yep! I only edited the yaml file above.
