# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    set -a
    source /vagrant/.env
    set +a

    sudo apt-get update
    sudo apt-get install apt-transport-https
    sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable main' > /etc/apt/sources.list.d/datadog.list"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7A7DA52
    sudo apt-get update
    sudo apt-get install datadog-agent
    sudo sh -c "sed 's/api_key:.*/api_key: $API_KEY/' /etc/dd-agent/datadog.conf.example > /etc/dd-agent/datadog.conf"
    sudo sh -c "sed 's/# tags:.*/tags: $TAGS/' /etc/dd-agent/datadog.conf > /etc/dd-agent/temp.conf"
    sudo sh -c "mv /etc/dd-agent/temp.conf /etc/dd-agent/datadog.conf"
    sudo /etc/init.d/datadog-agent start

    sudo apt-get install -y postgresql postgresql-contrib postgresql-client python3-pip tmux
    sudo -i -u postgres psql postgres < /vagrant/setup_dd_user.sql
    pip3 install datadog Flask ddtrace

    sudo cp /vagrant/dd-agent/conf.d/* /etc/dd-agent/conf.d/
    sudo cp /vagrant/dd-agent/checks.d/* /etc/dd-agent/checks.d/

    sudo /etc/init.d/datadog-agent restart

    python3 /vagrant/create_timeboard.py

    tmux start-server
    tmux new-session -d -s flask -n flaskapp
    tmux send-keys "python3 /vagrant/flaskapp.py" C-m

    tmux new-window -t flask:1 -n psql
    tmux select-window -t flask:1
    tmux send-keys "sudo -i -u postgres psql postgres" C-m
  SHELL
end
