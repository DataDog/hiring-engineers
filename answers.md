# ANSWERS

## Prerequisites - Setup the environment
Here are the steps I took to install docker and the datadog agent on Ubuntu 12.04 VM:

[Per Getting Started with Vagrant](https://www.vagrantup.com/intro/getting-started/index.html)
- [Install and run VirtualBox](https://www.virtualbox.org/)
- [Install the lastest version of Vagrant](https://www.vagrantup.com/downloads.html)

### Vagrant setup
- In the terminal, navigate to a folder you wish to work from
- Create the Vagrantfle
```
vagrant init hashicorp/precise64
```
- Start the virtual machine
```
vagrant up
```
- Enter the virtual machine
```
vagrant ssh
```

### Docker install on vagrant@precise64
- Install curl
```
sudo apt-get install curl
```
- Upgrade the system (When you see \<OK\> fields hit 'Enter')
```
curl -L https://gist.github.com/steakknife/9094991/raw/run_me_000__system_upgrade.sh | bash
```
- The box will disconnect, then restart it with:
```
vagrant ssh
```
- Install docker
```
curl -L https://gist.github.com/steakknife/9094991/raw/run_me_001__install_docker_and_fixes.sh | bash
```

### DataDog agent install
- Use easy one-step install line at https://app.datadoghq.com/account/settings#agent/docker
- Append ``sudo`` to the front

### Start the docker container with the DataDog agent
- In one terminal tab start the docker daemon:
```
sudo docker daemon
```
- In a separate terminal tab start the dd-agent container:
```
sudo docker start dd-agent
```

### Verification of docker and dd-agent install
```
docker --version
sudo docker ps
```
![Screenshot](/screenshots/01_dd-agent_installed.png?raw=true "Install Verification")

