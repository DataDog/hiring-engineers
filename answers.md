Prerequisites - Setup the environment
=====================================

<ol>
  <li>Environment used: Microsoft Windows 10 Surface Book
  <li>Hypervisor used: Virtual Box
  <li>Vagrant box used: Ubuntu 16.04
</ol>

The vagrant install
-------------------

<ol>
  <li>vagrant init ubuntu/xenial64
  <li>vagrant up
  <li>vagrant ssh
</ol>

<img src="http://www.thomatos.org/datadog/vagrant.png">

The agent installation
----------------------
Within the Ubuntu shell the command from the web page was provided as:

DD_API_KEY=9fcece82deb81b6846ad9d9b85893fda bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

The datadog-agent yaml file was updated and my tiny, infant, little dog started to bark.

<img src="http://www.thomatos.org/datadog/datadog-yaml.png">
