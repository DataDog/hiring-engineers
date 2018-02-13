VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do | config |
    # https://app.vagrantup.com/debian/boxes/stretch64
    config.vm.box = "debian/stretch64"


    # fix some time and timezone info to make sure it is correct for anyone who travels
    require 'time'
	offset = ((Time.zone_offset(Time.now.zone) / 60) / 60)
	timezone_suffix = offset >= 0 ? "-#{offset.to_s}" : "+#{offset.to_s}"
	timezone = 'Etc/GMT' + timezone_suffix
	config.vm.provision :shell, :inline => "sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/" + timezone + " /etc/localtime", run: "always"
end
