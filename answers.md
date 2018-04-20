# Datadog Solutions Engineer Exercise
The responses to all questions in this exercise are based off of the original document:
https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md

# Prerequisites - Setup the environment

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

Once the aga
