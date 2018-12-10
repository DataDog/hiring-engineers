# Data Dog - Solutions Engineer Exercise
The following document contains the answers for the Data Dog hiring engineer exercise by Scott Ford.

## Setup the Test Environment
For the exercise participants are asked to demonstrate their ability to use the data dog platform with real applications running on servers. One easy way to spin up test environments is though the use of HashiCorp's tool [Vagrant](http://vagrantup.com). Vagrant by itself is really powerful, but it really flies when you add some configuration management into the mix. There are a number of great configuration managment tools out there, but for my walkthrough I am going to use [Chef](https://docs.chef.io). Lastly, I am going to be running this exercise on MacOSX 10.14.

### Time to install some tools
Installing software on Mac is very easy with [Homebrew](https://brew.sh/). In the next section I will be using Homebrew to install the following software:
 - [Vagrant](https://vagrantup.com) - Vagrant is a tool for building and managing virtual machine environments in a single workflow
 - [VirtualBox](https://www.virtualbox.org/) - VirtualBox is a powerful x86 and AMD64/Intel64 virtualization product that is freely available as Open Source Software under the terms of the GNU General Public License (GPL) version 2
 - [Chef Workstation](https://www.chef.sh/) - Chef Workstation provides you all of the tools you need to write and test Chef code
 - *OPTIONAL* - Programmer's Text editor like [Visual Studio Code](https://code.visualstudio.com/), [Atom](http://atom.io), or [Sublime Text 2](http://www.sublimetext.com/)

#### Install Vagrant
Vagrant is a tool for building and managing virtual machine environments in a single workflow. With an easy-to-use workflow and focus on automation, Vagrant lowers development environment setup time, increases production parity, and makes the "works on my machine" excuse a relic of the past.

You can install Vagrant on MacOSX with Homebrew simply by opening up a terminal of choice (I use [iTerm2](https://www.iterm2.com/)) and running `brew cask install vagrant`. Once installed you can validate your Vagrant installation:

```
$ vagrant --version
Vagrant 2.2.2
```

#### Install VirtualBox
Vagrant by itself is not enough to get a development environment going though, you also need some kind of hypervisor to launch a guest VM. For this I use [VirtualBox](https://www.virtualbox.org/), which is a free open source virtualization platform for Mac, Windows, Linux and more. Again, with homebrew this is a simple one-liner `brew cask install virtualbox`. Validate your VirtualBox installation:

```
$ VBoxManage --version
5.2.22r126460
```

#### Install Chef Workstation
Lastly we need Chef Workstation which provides all of the tools you need to develop Chef code. Chef Workstation can be easily installed via Homebrew as well with `brew cask install chef-workstation`.  You can validate chef is properly installed by opening a terminal and running `chef --version`

```
$ chef --version
Chef Workstation: 0.2.39
  chef-run: 0.2.4
  chef-client: 14.7.17
  delivery-cli: master (5234f9fda9629d727169c37882d026dec9ed7d00)
  berks: 7.0.7
  test-kitchen: 1.23.2
  inspec: 3.0.52
```

With the tools installed, it is time to configure a test VM.

### Launch a test instance with Test Kitchen
Chef Workstation comes with a handy tool for launching test instances call [Test Kitchen](https://docs.chef.io/kitchen.html). Test Kitchen can launch test instances using various drivers like Vagrant, EC2, Azure, Google and more. For local development, Vagrant is the easiest way to go, and it is the default driver for Test Kitchen. But first we need to generate out a Chef cookbook...

Open a terminal and run `chef generate cookbook chef_datadog_example`

Once you have generated the cookbook, you can `cd` into the `chef_datadog_example` directory which contains all of the cookbook files...

```
scottford$ cd chef_datadog_example/
scottford$ ls -al
total 64
drwxr-xr-x  14 scottford  staff   448 Dec  9 17:15 .
drwxr-xr-x   9 scottford  staff   288 Dec  9 17:15 ..
drwxr-xr-x   5 scottford  staff   160 Dec  9 17:15 .delivery
-rw-r--r--   1 scottford  staff   197 Dec  9 17:15 .gitignore
-rw-r--r--   1 scottford  staff   442 Dec  9 21:53 .kitchen.yml
-rw-r--r--   1 scottford  staff    77 Dec  9 17:15 Berksfile
-rw-r--r--   1 scottford  staff   172 Dec  9 17:15 CHANGELOG.md
-rw-r--r--   1 scottford  staff    70 Dec  9 17:15 LICENSE
-rw-r--r--   1 scottford  staff    65 Dec  9 17:15 README.md
-rw-r--r--   1 scottford  staff  1090 Dec  9 17:15 chefignore
-rw-r--r--   1 scottford  staff   777 Dec  9 17:15 metadata.rb
drwxr-xr-x   3 scottford  staff    96 Dec  9 17:15 recipes
drwxr-xr-x   4 scottford  staff   128 Dec  9 17:15 spec
drwxr-xr-x   3 scottford  staff    96 Dec  9 17:15 test
```

Inside that directory you will find a `.kitchen.yml` file which is the configuration file for Test Kitchen. My initial `.kitchen.yml` looks like this...

```.kitchen.yml
---
driver:
  name: vagrant
  vm_hostname: vagrant1.scottford.io
  network:
    - ["private_network", {ip: "192.168.33.33"}]

provisioner:
  name: chef_zero
  always_update_cookbooks: true

verifier:
  name: inspec

platforms:
  - name: ubuntu-18.04

suites:
  - name: mongodb
    run_list:
      - recipe[chef_datadog_example::default]
    verifier:
      inspec_tests:
        - test/integration/default
    attributes:
```

Once configured, we can validate our configuration by running `kitchen list`:

```
$ kitchen list
Instance             Driver   Provisioner  Verifier  Transport  Last Action    Last Error
mongodb-ubuntu-1804  Vagrant  ChefZero     Inspec    Ssh        <Not Created>  <None>
```

### Kitchen Create
With our `.kitchen.yml` file configured we can now move on to creating and converging Chef code on a running Ubuntu-16.04 box. Test Kitchen has a number of different commands to interact with the tool. We've already seen the `kitchen list` will print out the configuration of the `.kitchen.yml`. At any point you can run `kitchen --help` to see all of the commands. The next command we are going to learn is `kitchen create` which will provision out a new instance of the platform(s) we have configured. Since we only have one platform configured at this point, we can run `kitchen create` which will call Vagrant and then provision a VM in VirtualBox. 

```
$ kitchen create
-----> Starting Kitchen (v1.23.2)
-----> Creating <mongodb-ubuntu-1804>...
...
       [SSH] Established
       Vagrant instance <mongodb-ubuntu-1804> created.
       Finished creating <mongodb-ubuntu-1804> (0m47.77s).
-----> Kitchen is finished. (0m50.05s)
```

Once Test Kitchen has finished the create process, we now have a sanbox instance that we can configure and interact with. Running `kitchen list` again we can see that our instance is created:

```
$ kitchen list
Instance             Driver   Provisioner  Verifier  Transport  Last Action  Last Error
mongodb-ubuntu-1804  Vagrant  ChefZero     Inspec    Ssh        Created      <None>
```

We can even login to the instance just by running `kitchen login`:

```
$ kitchen login
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-29-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Dec 10 07:28:38 UTC 2018

  System load:  0.24              Processes:           94
  Usage of /:   2.4% of 61.80GB   Users logged in:     0
  Memory usage: 13%               IP address for eth0: 10.0.2.15
  Swap usage:   0%                IP address for eth1: 192.168.33.33


0 packages can be updated.
0 updates are security updates.


Last login: Mon Dec 10 07:27:32 2018 from 10.0.2.2
vagrant@vagrant1:~$
```

You can logout of the instance by typing `exit` at the command line

```
vagrant@vagrant1:~$ exit
logout
Connection to 127.0.0.1 closed.
```

We could just start manually configuring this instance at this point, but that would be slow and error prone. Instead let's jump right into the power of Chef and test out the capabities of DataDog. 

### Kitchen Converge
In order to configure our instance with Chef, we will first need to install the `chef-client` on the instance. The `chef-client` is an agent that runs locally on every node that is under management by Chef. When a chef-client is run, it will perform all of the steps that are required to bring the node into the expected state. If something is already in the expected state, then `chef-client` will perform no action. 

To get `chef-client` installed on our instance we simply need to run `kitchen converge`

```
$ kitchen converge
-----> Starting Kitchen (v1.23.2)
-----> Converging <mongodb-ubuntu-1804>...
       Preparing files for transfer
       Preparing dna.json
       Resolving cookbook dependencies with Berkshelf 7.0.7...
       Removing non-cookbook files before transfer
       Preparing validation.pem
       Preparing client.rb
-----> Installing Chef Omnibus (install only if missing)
...
       Running handlers:
       Running handlers complete
       Chef Client finished, 0/0 resources updated in 01 seconds
       Downloading files from <mongodb-ubuntu-1804>
       Finished converging <mongodb-ubuntu-1804> (0m11.38s).
-----> Kitchen is finished. (0m14.36s)
```

The above output shows that the `kitchen converge` ran an install script that determined our platform of Ubuntu-1804 and then pulled down the latest version of `chef-client` from the internet and installed it on the system. After the installation completed, the `chef-client` ran for the first time running something called the `default.rb` recipe, which at this point contains no configuraiton code. We'll talk more about Chef Recipes in the following sections, but with the client installed we are ready to start configuring our host!

## Collecting Metrics
Now that I have a test instance to play with I need to get the DataDog agent installed. The Datadog Agent is open source software that runs on your host and allows you collect events and metrics to send to Datadog where you can further analyze and monitor the data. DataDog has made installing the agent extremely easy by providing numerous methods for accomplishing the task, including via Chef.

### Installing the dd-agent
DataDog provides excellent [documentation](https://docs.datadoghq.com/agent/) on how to get the agent installed on whatever platform you are monitoring, but they also provide a community [Chef cookbook](https://github.com/DataDog/chef-datadog) that we can leverage to get the agent installed. In order to do that we first must configure our Chef cookbook depend on DataDog's Chef cookbook. Adding a [dependency](https://docs.chef.io/config_rb_metadata.html) on DataDog's community cookbook will allow us to call the recipes, attributes, and any custom code it provides.

#### Edit the metadata.rb
Open the `chef_datadog_example/metadata.rb` in an editor and add a dependency on the DataDog community cookbook:

```
name 'chef_datadog_example'
maintainer 'Scott Ford'
maintainer_email 'smford22@gmail.com'
license 'All Rights Reserved'
description 'Installs/Configures chef_datadog_example'
long_description 'Installs/Configures chef_datadog_example'
version '0.1.0'
chef_version '>= 13.0'
depends 'datadog' # <-- DEPENDENCY
```

Before we can run this or any community Chef code, it is best to read the [README](https://github.com/DataDog/chef-datadog/blob/master/README.md) file to understand what functionality the cookbook provides. A quick read through explains that the DataDog API will be requried to authenticate with our DataDog account. In order to configure our API key we can leverage Chef Attributes provided by the DataDog community cookbook to pass to our test instance. You can think of attributes almost list a variable that can be overwritten by the chef-client in various ways. The DataDog cookbook has an attribute called `default['datadog']['api_key']` that allows us to set our api_key with the data dog agent. Our `.kitchen.yml` has a section where we can configure attributes for any suites we've defined. That being said, DataDog API keys should always be kept secret, so we are going to instead use an ENVIRONMENT VARIABLE on our workstation, and configure Test Kitchen to pull that configuration in.

#### Export environment variable
On your workstation, open a terminal and run the following command:
```
$ export DD_API_KEY=<YOUR API KEY GOES HERE>
```

#### Edit attribute
Back in our `.kitchen.yml` file, set the attribute for the api key:
```
suites:
  - name: default
    run_list:
      - recipe[chef_datadog_example::default]
    verifier:
      inspec_tests:
        - test/smoke/default
    attributes:
      datadog:
        api_key: <%= ENV['DD_API_KEY'] %>
```

#### Run the default recipe from the DataDog cookbook
A fundamental aspect of using Chef is the understanding Resources and Recipes. Resources are simply a piece of the system (and its desired state), a provider defines the steps that are needed to bring that piece of the system from its current state into the desired state. Examples of resources in chef includes `package`, `service`, `file`, `user`, `group` etc. A recipe is just an ordered list of resources that the chef-client will execute and ensure the system is in the desired state. 

The DataDog community cookbook contains a recipe called `dd-agent` which will install the agent and start reporting to your DataDog account using the API key configured. In order to run that recipe, we just need to include it in our default recipe...

##### Edit `chef_datadog_example/recipes/default.rb`
```
#
# Cookbook:: chef_datadog_example
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
include_recipe 'datadog::dd-agent'
```

Now run `kitchen converge` again to run the recipe and install the agent...

```
$ kitchen converge
-----> Starting Kitchen (v1.23.2)
-----> Converging <mongodb-ubuntu-1804>...
       Preparing files for transfer
       Preparing dna.json
       Resolving cookbook dependencies with Berkshelf 7.0.7...
       Removing non-cookbook files before transfer
       Preparing validation.pem
       Preparing client.rb
-----> Chef Omnibus installation detected (install only if missing)
       Transferring files to <mongodb-ubuntu-1804>
       Starting Chef Client, version 14.7.17
       resolving cookbooks for run list: ["chef_datadog_example::default"]
       Synchronizing Cookbooks:
         - chef_datadog_example (0.1.0)
         - apt (7.1.1)
         - datadog (2.16.1)
         - chef_handler (3.0.3)
         - windows (5.2.2)
         - yum (5.1.0)
       Installing Cookbook Gems:
       Compiling Cookbooks...
       Converging 19 resources
       Recipe: datadog::dd-agent
         * ruby_block[datadog-api-key-unset] action run (skipped due to only_if)
       Recipe: apt::default
         * file[/var/lib/apt/periodic/update-success-stamp] action nothing (skipped due to action :nothing)
         * apt_update[periodic] action periodic
           - update new lists of packages
           * directory[/var/lib/apt/periodic] action create (up to date)
           * directory[/etc/apt/apt.conf.d] action create (up to date)
           * file[/etc/apt/apt.conf.d/15update-stamp] action create_if_missing (up to date)
           * execute[apt-get -q update] action run
             - execute ["apt-get", "-q", "update"]

         * execute[apt-get update] action nothing (skipped due to action :nothing)
         * execute[apt-get autoremove] action nothing (skipped due to action :nothing)
         * execute[apt-get autoclean] action nothing (skipped due to action :nothing)
         * directory[/var/cache/local] action create
           - create new directory /var/cache/local
           - change mode from '' to '0755'
           - change owner from '' to 'root'
           - change group from '' to 'root'
         * directory[/var/cache/local/preseeding] action create
           - create new directory /var/cache/local/preseeding
           - change mode from '' to '0755'
           - change owner from '' to 'root'
           - change group from '' to 'root'
         * template[/etc/apt/apt.conf.d/10dpkg-options] action create
           - create new file /etc/apt/apt.conf.d/10dpkg-options
           - update content in file /etc/apt/apt.conf.d/10dpkg-options from none to c918ac
           --- /etc/apt/apt.conf.d/10dpkg-options       2018-12-10 07:34:59.723749412 +0000
           +++ /etc/apt/apt.conf.d/.chef-10dpkg-options20181210-2044-1custna    2018-12-10 07:34:59.723749412 +0000
           @@ -1 +1,4 @@
           +# Managed by Chef
           +DPkg::Options {
           +}
           - change mode from '' to '0644'
           - change owner from '' to 'root'
           - change group from '' to 'root'
         * template[/etc/apt/apt.conf.d/10recommends] action create
           - create new file /etc/apt/apt.conf.d/10recommends
           - update content in file /etc/apt/apt.conf.d/10recommends from none to f41e1d
           --- /etc/apt/apt.conf.d/10recommends 2018-12-10 07:34:59.735755411 +0000
           +++ /etc/apt/apt.conf.d/.chef-10recommends20181210-2044-6wbxf2       2018-12-10 07:34:59.735755411 +0000
           @@ -1 +1,4 @@
           +# Managed by Chef
           +APT::Install-Recommends "1";
           +APT::Install-Suggests "0";
           - change mode from '' to '0644'
           - change owner from '' to 'root'
           - change group from '' to 'root'
         * apt_package[apt-transport-https, gnupg, dirmngr] action install
           - install version 1.6.6 of package apt-transport-https
       Recipe: datadog::repository
         * apt_package[install-apt-transport-https] action install (up to date)
         * apt_repository[datadog] action add
           * execute[install-key A2923DFF56EDA6E76E55E492D3A80E30382E94DE] action run
             - execute apt-key adv --recv --keyserver hkp://keyserver.ubuntu.com:80 A2923DFF56EDA6E76E55E492D3A80E30382E94DE
           * execute[apt-cache gencaches] action run
             - execute ["apt-cache", "gencaches"]
           * execute[apt-cache gencaches] action nothing (skipped due to action :nothing)
           * apt_update[datadog] action nothing (skipped due to action :nothing)
           * file[/etc/apt/sources.list.d/datadog.list] action create
             - create new file /etc/apt/sources.list.d/datadog.list
             - update content in file /etc/apt/sources.list.d/datadog.list from none to de9651
             --- /etc/apt/sources.list.d/datadog.list   2018-12-10 07:35:03.705739411 +0000
             +++ /etc/apt/sources.list.d/.chef-datadog20181210-2044-8tpmfv.list 2018-12-10 07:35:03.705739411 +0000
             @@ -1 +1,2 @@
             +deb      "http://apt.datadoghq.com" stable main
             - change mode from '' to '0644'
             - change owner from '' to 'root'
             - change group from '' to 'root'
           * execute[apt-cache gencaches] action run
             - execute ["apt-cache", "gencaches"]
           * apt_update[datadog] action update
             - force update new lists of packages
             * directory[/var/lib/apt/periodic] action create (up to date)
             * directory[/etc/apt/apt.conf.d] action create (up to date)
             * file[/etc/apt/apt.conf.d/15update-stamp] action create_if_missing (up to date)
             * execute[apt-get -q update] action run
        - execute ["apt-get", "-q", "update"]


         * apt_repository[datadog-beta] action remove (up to date)
       Recipe: datadog::_install-linux
         * apt_package[datadog-agent-base] action remove (skipped due to not_if)
         * apt_package[datadog-agent] action install
           - install version 1:5.29.0-1 of package datadog-agent
       Recipe: datadog::dd-agent
         * directory[/etc/dd-agent] action create
           - change group from 'dd-agent' to 'root'
         * template[/etc/dd-agent/datadog.conf] action create
           - create new file /etc/dd-agent/datadog.conf
           - update content in file /etc/dd-agent/datadog.conf from none to 803b4d
           - suppressed sensitive resource
           - change mode from '' to '0640'
           - change owner from '' to 'dd-agent'
           - change group from '' to 'root'
         * service[datadog-agent] action enable (up to date)
         * service[datadog-agent] action start
           - start service service[datadog-agent]
         * service[datadog-agent] action restart
           - restart service service[datadog-agent]

       Running handlers:
       Running handlers complete

       Deprecated features used!
         Resource chef_handler from a cookbook is overriding the resource from the client. Please upgrade your cookbook or remove the cookbook from your run_list before the next major release of Chef. at 1 location:
           - /opt/chef/embedded/lib/ruby/gems/2.5.0/gems/chef-14.7.17/lib/chef/log.rb:51:in `caller_location'
          See https://docs.chef.io/deprecations_map_collision.html for further details.

       Chef Client finished, 19/36 resources updated in 27 seconds
       Downloading files from <mongodb-ubuntu-1804>
       Finished converging <mongodb-ubuntu-1804> (0m33.25s).
```

The output above shows `chef-client` running again, pulling down the DataDog cookbook and any of it's dependencies, and then running the `datadog::dd-agent` recipe on the instance. Running `kitchen converge` again you will see the power of configuration management as `chef-client` determines that the system is already in the desired state and does not need to make any changes. 

Logging into the host you can see that the agent is indeed now running:
```
$ kitchen login
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-29-generic x86_64)
...
vagrant@vagrant1:~$ sudo service datadog-agent status
● datadog-agent.service - "Datadog Agent"
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2018-12-10 07:57:43 UTC; 3min 19s ago
 Main PID: 2990 (agent)
    Tasks: 9 (limit: 1135)
   CGroup: /system.slice/datadog-agent.service
           └─2990 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid
```

##### Add some tags
DataDog allows you to create tags allowing you to organize and query the instances you have to monitor. Using the DataDog cookbook we can easily add tags to our instance:

```
suites:
  - name: mongodb1
    run_list:
      - recipe[chef_datadog_example::default]
    verifier:
      inspec_tests:
        - test/smoke/default
    attributes:
      datadog:
        api_key: <%= ENV['DD_API_KEY'] %>
        tags: 
          name: scottford-test
          environment: localdev
          config_mgmt: chef
```

Run `kitchen converge` again to add the tags to our instance. This adds the tags to the `/etc/datadog-agent/datadog.yaml` file:

```
vagrant@vagrant1:~$ sudo grep -A 3 tags: /etc/datadog-agent/datadog.yaml
tags:
- name:vagrant1.scottford.io
- environment:localdev
- config_mgmt:chef
```

We can now login to DataDog and see the host in the Host Map with the specified tags:

![alt text](screenshots/screenshot1.png)

#### DataDog Chef Intergration (BONUS)
DataDog provides an intergration for Chef so we can monitor the health of our Chef runs. To take advantage of this integration we need to generate an Data Dog Application key, export the key to an environment variable, update our `.kitchen.yml`, and then add the `dd-handler` recipe from the DataDog community cookbook to our default recipe...

1. Generate an Application Key [here](https://app.datadoghq.com/account/settings#api)
2. Export the Data Dog Application key as an environment variable on your workstation `scottford$ export DD_APP_KEY='<DD_APP_KEY GOES HERE>'`
3. Update `.kitchen.yml`
```
suites:
  - name: mongodb
    run_list:
      - recipe[chef_datadog_example::default]
    verifier:
      inspec_tests:
        - test/integration/default
    attributes:
      datadog:
        agent6: true
        api_key: <%= ENV['DD_API_KEY'] %>
        application_key: <%= ENV['DD_APP_KEY'] %>
        tags: 
          name: vagrant1.scottford.io
          environment: localdev
          config_mgmt: chef
```
4. Add the `dd-handler` recipe to the `default.rb`
```
include_recipe 'datadog::dd-agent'
include_recipe 'datadog::dd-handler'
```

Run `kitchen converge` again

### Install MongoDB and the DataDog MongoDB integration
Next we will use Chef to install MongoDB on our instance and dive deeper into DataDog. While there is a Chef community MongoDB cookbook for installing and configuring Mongo, for this exercise we are going to do things a bit more manually, and write the Chef code ourselves. 

First we will use the `chef` command to add a new recipe to hold all of our Mongo Chef code...

```
$ chef generate recipe mongodb
```

Using Chef resources we can configure the `mongodb.rb` recipe to install MongoDB, manage its configuration, and manage the service. In addition in the same recipe we can configure the MongoDB integration 

```
#
# Cookbook:: chef_datadog_example
# Recipe:: mongodb
#
# Copyright:: 2018, The Authors, All Rights Reserved.

#
# Install mongodb
#
package 'mongodb'

#
# Start mongodb
#
service 'mongodb' do 
  action [:enable, :start]
end

#
# Setup the DataDog user in Mongo if not created
# 
execute 'setup-datadog-user' do 
  command <<-EOH 
    sleep 10
    mongo admin --eval "db.createUser({'user':'datadog', 'pwd': 'datadog', 'roles' : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})"
  EOH
  not_if 'mongo admin --eval \'db.getUsers()\'|tr -d \'\n\'|grep datadog'
end

#
# Command to restart the datadog-agent
#
execute 'restart-datadog-agent' do
  command 'service datadog-agent restart'
  action :nothing
end

template '/etc/datadog-agent/conf.d/mongo.yaml' do
  source 'mongo.yaml.erb'
  owner 'dd-agent'
  group 'root'
  mode '0600'
  notifies :run, 'execute[restart-datadog-agent]', :immediately
end
```

#### Generate a template for /etc/datadog-agent/conf.d/mongo.yaml
Additonally, we need to create a template for the DataDog agent to monitor our service:

```
$ chef generate template mongo.yaml
Recipe: code_generator::template
  * directory[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates] action create
    - create new directory /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates
  * template[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/mongo.yaml.erb] action create
    - create new file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/mongo.yaml.erb
    - update content in file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/mongo.yaml.erb from none to e3b0c4
    (diff output suppressed by config)
```

#### Add content for mongo.yaml template
We can now add the following content to `chef_datadog_example/templates/mongo.yaml.erb`:

```
---
logs: []


instances:
  - server: mongodb://datadog:datadog@localhost:27017/admin

init_config:
# No init_config details needed
```

With our recipe written we need to add it to our `default` recipe and then run `kitchen converge` again

#### Edit `chef_datadog_example/recipes/default.rb`
```
#
# Cookbook:: chef_datadog_example
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
include_recipe 'datadog::dd-agent'
include_recipe 'datadog::dd-handler'
include_recipe 'chef_datadog_example::mongodb'
```

Run `kitchen converge` again

Logging into the instance we can now see that the mongo integration is now running:

```
vagrant@vagrant1:~$ sudo datadog-agent status|grep -A 5 mongo
    hostname: mongodb-ubuntu-1804
    socket-fqdn: vagrant1.scottford.io.
    socket-hostname: vagrant1
    hostname provider: configuration

=========
--
    mongo (1.6.1)
    -------------
        Instance ID: mongo:90349833a2cae6f6 [OK]
        Total Runs: 26
        Metric Samples: 121, Total: 3,146
        Events: 0, Total: 0
        Service Checks: 1, Total: 26
        Average Execution Time : 18ms
```

We can also now see the mongodb integration working in DataDog:

We can now login to DataDog and see the host in the Host Map with the specified tags:

![alt text](screenshots/screenshot2.png)

#### Creating a Custom Check
In this next section we will create a custom check called 'my_metric' that tests a random interval on our instance


```
$ chef generate template my_metric.py
Recipe: code_generator::template
  * directory[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates] action create (up to date)
  * template[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.py.erb] action create
    - create new file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.py.erb
    - update content in file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.py.erb from none to e3b0c4
    (diff output suppressed by config)
```

```
$ chef generate template my_metric.yml
Recipe: code_generator::template
  * directory[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates] action create (up to date)
  * template[/Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.yml.erb] action create
    - create new file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.yml.erb
    - update content in file /Users/scottford/src/data_dog/hiring-engineers/chef_datadog_example/templates/my_metric.yml.erb from none to e3b0c4
    (diff output suppressed by config)
```

##### Edit `chef_datadog_example/templates/my_metric.py.erb`
```
from random import *
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(1, 1000), tags=['my_metric'])
```

##### Edit `chef_datadog_example/templates/my_metric.yml.erb` 
```
init_config:
  min_collection_interval: 5

instances:
    [{}]
```

#### Create a new recipe to configure our custom check
`$ chef generate recipe dd_custom_check`

##### Edit `chef_datadog_example/recipes/dd_custom_check`
```
#
# Cookbook:: chef_datadog_example
# Recipe:: dd_custom_check
#
# Copyright:: 2018, The Authors, All Rights Reserved.
template '/etc/dd-agent/conf.d/my_metric.yaml' do
  source 'my_metric.yaml.erb'
end

template '/etc/dd-agent/checks.d/my_metric.py' do
  source 'my_metric.py.erb'
end
```

##### Edit `chef_datadog_example/recipes/default.rb` 
```
#
# Cookbook:: chef_datadog_example
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
include_recipe 'datadog::dd-agent'
include_recipe 'datadog::dd-handler'
include_recipe 'chef_datadog_example::mongodb'
include_recipe 'chef_datadog_example::dd_custom_check'
```

Run `kitchen converge` again to add our custom check to the instance.

Now with Chef managing the `my_metric.yml` configuration file we can easily change the check interval to 45 seconds..

##### Edit `chef_datadog_example/templates/my_metric.yaml.erb`
```
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

## Vizualizing Data
Using the DataDog API we can add a timeboard...

```
require 'rubygems'
require 'dogapi'

api_key=ENV['DD_API_KEY']
app_key=ENV['DD_APP_KEY']

dog = Dogapi::Client.new(api_key, app_key)


# Create a timeboard.
title = 'My Timeboard'
description = 'A basic timeboard generated via the API'
graphs = [{
  "definition" => {
    "events" => [],
    "requests"=> [
      {
        "q" => "avg:my_metric.check{host:mongodb-ubuntu-1604}",
        "type" => "line"
      },
      {
        "q" => "anomalies(avg:mongodb.mem.virtual{*}, 'basic', 2)",
        "type" => "line"
      },
      {
        "q" => "avg:my_metric.check{*}.rollup(sum, 3600)",
        "type" => "line"
      }
    ],
  "viz" => "timeseries"
  },
  "title" => "Random int check"
}]
template_variables = [{
	"name" => "host1",
	"prefix" => "host",
	"default" => "host:my-host"
}]

res = dog.create_dashboard(title, description, graphs, template_variables)
```


