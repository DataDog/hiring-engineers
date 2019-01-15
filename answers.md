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

![install_2](./screenshots/install_2.png)

# Collecting Metrics

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I didn't really know what a tag was or how to implement it so I had to check out the [Tag Docs](https://docs.datadoghq.com/tagging/assigning_tags/?tab=go) which showed me how to  implement a tag using the terminal.

1. You have to `cd ..` until you hit the root directory of the VM.
2. Then navigate to `/etc/datadog-agent` . In this directory you'll find a file named `datadog.yaml`.
3. Vagrant has a built in editor named nano that we can use. We can open the file with `sudo nano datadog.yaml` You need to include the `sudo` or else you won't have permissions to change the file!

These are my tags :

![host_map_1](./screenshots/host_map_1.png)

Upon saving these changes , you have to restart the agent using `sudo service datadog-agent restart`. After you've restarted the agent, you can go to the Datadog web application and click the Infrastructure then click Host Map to see your tags.

This is how it should appear :

![host_map_2](./screenshots/host_map_2.png)
