$script = <<SCRIPT
  echo I am provisioning...
  date > /etc/vagrant_provisioned_at
SCRIPT

Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'

  config.vm.provision 'shell', inline: $script
  config.vm.provision 'shell', path: 'postgres_bootstrap.sh'
  config.vm.network 'forwarded_port', guest: 5432, host: 15_432

  config.vm.provision 'file', source: 'bootstrap_scripts/random_value.py', destination: 'random_value.py'
  config.vm.provision 'file', source: 'bootstrap_scripts/random_value.yaml', destination: 'random_value.yaml'

  config.vm.provision 'file', source: '.env', destination: '.env'
  config.vm.provision 'shell', path: 'dd_agent_bootstrap.sh'
end
