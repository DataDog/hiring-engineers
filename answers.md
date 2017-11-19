# ANSWERS

## Prerequisites - Setup the environment
I didn't see a link to the instructions in the README so I decided to figure this out on my own. Here is what worked for me:

[Per Getting Started with Vagrant](https://www.vagrantup.com/intro/getting-started/index.html)
- [Install and run VirtualBox](https://www.virtualbox.org/)
- [Install the lastest version of Vagrant](https://www.vagrantup.com/downloads.html)

### In the terminal, navigate to a folder you wish to work from:
```
vagrant init hashicorp/precise64 // create the Vagrantfile
vagrant up // starts the virtual machine
vagrant ssh // enters the virtual machine
```

### Docker install on vagrant@precise64
- Install curl
```
sudo apt-get install curl
```
- Upgrade the system (When you see <OK> fields hit 'Enter')
```
curl -L https://gist.github.com/steakknife/9094991/raw/run_me_000__system_upgrade.sh | bash
```
- The box will disconnect, then restart with:
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
