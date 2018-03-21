# Andy Roberts - Solution Engineer Answers

## Prerequesites

- upgraded VirtualBox on MacOSX
- download & install of Vagrant
- vagrant init hashicorp/precise64
- vagrant up
- vagrant ssh
- sudo apt-get install curl
- created DataDog account as andy@apr-ltd.com
- installed datadog-agent : DD_API_KEY=8f81d670622eca859c920ec9e9514ecf bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

### So What, Who Cares ?

- very simple to test and demonstrate basic setup which means simple for customer to deploy
- simple agent installation and configuration and also easy to automate with Chef, Puppet etc
- no monitoring server deployment required massively reducing time to value/demonstration of solution

## Collecting Metrics

- Edited DataDog config : sudo vi /etc/datadog-agent/datadog.yaml
- uncommented tags section and made some changes 

 ![alt text](https://github.com/stackparty/hiring-engineers/blob/master/dd_agent_config.png "Tags in Agent Config")
 
- Restarted service (not sure if necessary) : sudo service datadog-agent restart

![alt text](https://github.com/stackparty/hiring-engineers/blob/master/dd_hostmap.png "Host map in Datadog")

- Installed

