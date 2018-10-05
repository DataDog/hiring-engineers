### Setting the Environment (prerequisite)

Setup the Datadog Agent on an Ubuntu 16.04 virtual machine (VM) running on VirtualBox and Vagrant

1. Download and install VirtualBox [here](https://www.virtualbox.org/).
2. Download and install Vagrant [here](https://www.vagrantup.com/docs/installation/).
3. Set config.vm.box in Vagrantfile as follows:
    ```
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-16.04"
    ```
    More details [here](https://app.vagrantup.com/bento/boxes/ubuntu-16.04).

4. On the terminal, run the following command to create your VM:
    ```
    $ vagrant up
    ```

5. SSH into the your fresh VM using the following command:
    ```
    $ vagrant ssh
    ```

6. Install the Datadog agent by running the one-step command:
    ```
    $ DD_API_KEY=2726c4e30cc681d3f0dc01b8bc1a931d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
    ```
    More details [here](https://app.datadoghq.com/account/settings#agent/ubuntu).
