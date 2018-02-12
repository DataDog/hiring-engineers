Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/precise64"
  end
end
