# $script = <<SCRIPT
#   echo I am provisioning...
#   date > /etc/vagrant_provisioned_at
# SCRIPT

Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'

  config.vm.provision :file, source: '.env', destination: '.env'
  config.vm.provision :shell, path: 'dd_agent_bootstrap.sh'
  # config.vm.provision "shell", inline: $script
  # config.vm.provision :shell, path: 'postgres_bootstrap.sh'
  # config.vm.network 'forwarded_port', guest: 5432, host: 15_432
end
