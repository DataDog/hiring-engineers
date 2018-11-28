1. Datadog Agent installed 
Installed in MacOS
$ DD_API_KEY=04b457d18fc4f92ecd500f802a01449d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"

// Your Agent is running properly. It will continue to run in the
background and submit metrics to Datadog.

You can check the agent status using the ##datadog-agent status## command or by opening the webui using the ##datadog-agent launch-gui## command.

If you ever want to stop the Agent, please use the Datadog Agent App or the launchctl command. It will start automatically at login.

2. Accessed datadog-agent launch-gui. Goes to http://127.0.0.1:5002/ 

3. Access conf files and added tags on conf files
$ vim ~/.datadog-agent/datadog.yaml

tags: region:USEast, role:localmachine
screenshots/tags_on_agent_config_file.png
screenshots/tags_on_ui.png

Then, restarted agent: 
$ launchctl stop com.datadoghq.agent
$ launchctl start com.datadoghq.agent

Then, tags were on host map page
screenshots/tags_on_host_map_page.png
screenshots/tags_on_host_map_page2.png

4. Checked PostgreSQL was already installed.
psql --version
psql (PostgreSQL) 10.5

Run PostgreSQL
$ psql
Then, 
$ create user datadog with password 'albertodatadog'

Run returning Postgres connection - OK but not requiring password.
$ psql -h localhost -U datadog postgres -c \ "select * from pg_stat_database LIMIT(1);" && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ || echo -e "\e[0;31mCannot connect to Postgres\e[0m"

Changed name postgres.yaml.example to postgres.yaml
Added tags: database:postgresql

Restarted Agent as before. Then, run 
$ datadog-agent status
Postgres is under Running checks
Then, Postgres shows on host map page

5. Created files 2 files, my_metric.py and my_metric.yaml. saved in /etc/dd-agent/checks.d and /etc/dd-agent/conf.d respectively.
Followed this directions: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
screenshots/my_metrics_py_file.png
screenshots/my_metrics_yaml_collection_interval_45.png
screenshots/my_metrics_graph.png


6. Created Ruby app with datadog gem (gem "dogapi").
After bundle install, I wrote the script for creating a Timeboard with 3 graphs. 
Went to https://app.datadoghq.com/account/settings#api and created an Application key. The API key was already created. Added the keys to the script.
After executing the script ($ruby run.rb) the terminal printed the response. The timeboard was available in the UI "Dashboard >> Dashboard list".

The anomalies 

7. Detail step by step how to adjust timeboards.
8. Detail step by step how to create and customize metric monitors.

9. Created Rails app without database or test framework. $ rails new instrumented-app -T --skip-active-record

Added 
