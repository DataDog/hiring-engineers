# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'
# Get sensitive data from file
secrets_file = 'secrets.yaml'
if File.file?(secrets_file)
  secrets = YAML.load_file(secrets_file)
  dd_api_key = secrets["dd_api_key"]
end
# Get tags data from file
tags_file = 'tags.yaml'
if File.file?(tags_file)
  tags = YAML.load_file(tags_file)
  dd_tags = tags["dd_tags"]
end

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "./", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    # include parse_yaml function
    source /vagrant_data/parse_yaml.sh
    APIKEY="#{dd_api_key}"
    TAGS="#{dd_tags}"
    if [[ $APIKEY = "" || -z $APIKEY ]]; then
      # In cases where `vagrant provision` is being run rather than `vagrant up`
      # or `vagrant reload` #{dd_api_key} will not be available, so try loading
      # the file from disk via bash
      # try to eval, if not fall back to `true` -- allows script to exit cleanly
      eval $(parse_yaml #{secrets_file} "config_")
      APIKEY="$config_dd_api_key"
      if [[ $APIKEY = "" || -z $APIKEY ]]; then
        echo "No Datadog API key found. Make sure 'secrets.yaml' exists. VM will come up without Datadog agent installed."
        # Do not exit here -- we still want the vagrant box to come up if the
        # user has not yet created `secrets.yaml`
      fi
    fi
    # TODO: Refactor: more DRY/re-useable with the APIKEY logic above
    if [[ $TAGS = "" || -z $TAGS ]]; then
      # In cases where `vagrant provision` is being run rather than `vagrant up`
      # or `vagrant reload` #{dd_api_key} will not be available, so try loading
      # the file from disk via bash
      # try to eval, if not fall back to `true` -- allows script to exit cleanly
      eval $(parse_yaml #{tags_file} "tags_")
      TAGS="$tags_dd_tags"
      if [[ $TAGS = "" || -z $TAGS ]]; then
        echo "No Datadog Tags found. Make sure 'tags.yaml' exists."
      fi
    fi
    # Re-check to see if able to load the DD API Key
    if [[ $APIKEY != "" && ! -z $APIKEY ]]; then
      sudo apt-get update
      sudo apt-get install apt-transport-https
      sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable main' > /etc/apt/sources.list.d/datadog.list"
      sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7A7DA52
      sudo apt-get update
      sudo apt-get install datadog-agent
      sudo sh -c "sed 's/api_key:.*/api_key: $APIKEY/' /etc/dd-agent/datadog.conf.example > /etc/dd-agent/datadog.conf"
      sudo sh -c "sed 's/# tags:.*/tags: $TAGS/' /etc/dd-agent/datadog.conf > /etc/dd-agent/temp.conf"
      sudo sh -c "mv /etc/dd-agent/temp.conf /etc/dd-agent/datadog.conf"
      sudo /etc/init.d/datadog-agent start
    fi
  SHELL
end
