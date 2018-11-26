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