# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. 
# reference documentation: https://docs.vagrantup.com.

# The "2" in Vagrant.configure configures the configuration version.
Vagrant.configure("2") do |config|

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "hashicorp/precise64"

  # Shell provisioner to setup the machine with the bootstrap.sh file.
  config.vm.provision :shell, path: "bootstrap.sh"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. 
  config.vm.network :forwarded_port, guest: 80, host: 4567
end
