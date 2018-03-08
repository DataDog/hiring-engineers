$postgres_script = <<SCRIPT
  echo I am provisioning...
  date > /etc/vagrant_provisioned_at
SCRIPT

$python_script = <<SCRIPT
  sudo apt-get update
  sudo apt-get -y install python-pip
  sudo apt-get install python-dev
  sudo pip install Flask
  sudo pip install ddtrace
  export FLASK_APP=flask-app.py
  flask run &
SCRIPT
Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'

  # Postgres
  config.vm.provision 'shell', inline: $postgres_script
  config.vm.provision 'shell', path: 'postgres_bootstrap.sh'
  config.vm.network 'forwarded_port', guest: 5432, host: 15_432

  # Custom Agent
  config.vm.provision 'file', source: 'bootstrap_scripts/random_value.py', destination: 'random_value.py'
  config.vm.provision 'file', source: 'bootstrap_scripts/random_value.yaml', destination: 'random_value.yaml'

  # Datadog Agent
  config.vm.provision 'file', source: '.env', destination: '.env'
  config.vm.provision 'shell', path: 'dd_agent_bootstrap.sh'

  # Flask
  config.vm.provision 'file', source: 'flask-app.py', destination: 'flask-app.py'
  config.vm.provision 'shell', inline: $python_script
  config.vm.network 'forwarded_port', guest: 5000, host: 15_000
end
