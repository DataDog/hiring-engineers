# Setting the Environment (prerequisite)

Setup the Datadog Agent on an Ubuntu 16.04 virtual machine (VM) running on VirtualBox and Vagrant

1. Download and install VirtualBox [here](https://www.virtualbox.org/).
2. Download and install Vagrant [here](https://www.vagrantup.com/docs/installation/).
3. Set config.vm.box in the Vagrantfile as follows:
    ```
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-16.04"
    ```
    More details [here](https://app.vagrantup.com/bento/boxes/ubuntu-16.04).

4. On the terminal, run the following command to create your VM:
    ```
    $ vagrant up
    ```

5. SSH into the your fresh VM using:
    ```
    $ vagrant ssh
    ```
    
    You can check your Ubuntu 16.04 installation using:
    ```
    $ lsb_release -a
    ```

6. Follow the instructions for getting started with Datadog, and create a Datadog account [here](https://docs.datadoghq.com/).


7. Install the Datadog agent for Ubuntu 16.04 by running:
    ```
    $ DD_API_KEY=2726c4e30cc681d3f0dc01b8bc1a931d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
    ```
    More details [here](https://app.datadoghq.com/account/settings#agent/ubuntu).

If you have finished until 7, then you've finished installing your first Datadog Agent. Congratulations!