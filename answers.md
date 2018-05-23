# Solutions Engineer Challenge for Datadog

### Prerequisites - Setting up the environment

1. Set up [Vagrant Ubuntu 12.04 VM](https://www.vagrantup.com/intro/getting-started/)
  - Downloaded [proper package](https://www.vagrantup.com/downloads.html) for operating system
  - Run in terminal to have fully running virtual machine:
    `$ vagrant init hashicorp/precise64`
    `$ vagrant up`
2. Sign up for Datadog
  - Run api key command in terminal
    `DD_API_KEY=4XXXXXXXXXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"`

    # <img src="/images/collecting_metrics1.png" height=300>
