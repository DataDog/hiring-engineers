# Prerequisites - Setup the environment

To complete this exercise I had to download both [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

After downloading both of these programs I had to install them. Using the Vagrant [Docs](https://www.vagrantup.com/intro/getting-started/project_setup.html) I figured out the commands to install them were:

1. Make a directory (which I already have one since I have this repo.)
2. `vagrant init bento/ubuntu-16.04` to create a Ubuntu 16.04 VM
3. `vagrant up` to start the VM
4. `vagrant ssh` to use the VM


After vagrant has finished installing, I signed up for Datadog and I navigated to the Integrations Tab --> Agent Tab --> Ubuntu Tab.
![install_1](./screenshots/install_1.png)


In this tab  you will see that Datadog gives you a on line command to type into your terminal to install the client.
`DD_API_KEY={YOUR_API_KEY} bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

After you've typed this into the terminal that's running Vagrant, your terminal should look like this :

![Datadog_Agent_Installation](./screenshots/install_2.png)
