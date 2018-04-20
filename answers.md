# Datadog Solutions Engineer Exercise
The responses to all questions in this exercise are based off of the original document:
https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md

# Prerequisites - Setup the environment:

Items used to complete this exercise:
- Macbook Pro
- *Vagrant*
- *Virtualbox*
- *Ubuntu Trusty 64*
- *Various Linux utilities*
- Datadog trial account

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Vagrant%20install%20Ubuntu.png)

Once the Ubuntu server is installed, the next task is to install the Datadog Ubuntu agent. The agent deployment information can be found on the Integrations -> Agents -> Ubuntu page.

`sudo DD_API_KEY=76919a606a574952a97b6faf68987b49 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/DD%20Agent%20Install.png)

The Datadog agent can be stopped or started using the following commands:
`sudo stop datadog-agent`
`sudo start datadog-agent`

# Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

Tags can be created either in the Datadog GUI or by editing the mysql.yaml file.

`sudo nano /etc/datadog-agent/datadog.yaml`

Look for the section in the file that starts with “Set the host’s tags (optional)", remove the comment (#) in front of tags, edit them with the relevant information and place them on a single line. The entry should show the following:

`tags: host:dwlinux, env:lab, role:engineering`

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Edit%20datadog.yaml%20to%20input%20tags.png)

After restarting the Datadog agent, the tags will show up in the GUI.

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Restart%20dd%20agent%20after%20tags%20inserted.png)

![Settings Window](https://github.com/dhwest14/hiring-engineers/blob/master/Host%20map%20with%20tags.png)
