Your answers to the questions go here.

# The Exercise
## Prerequisites - Setup the environment

I used a Vagrantfile to persist a simple Ubuntu 12.04 VM on my local machine.

```
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/precise64"
  end
end```

## Collecting metrics
