
#The Challenger – Marc Ian Bucad
##Level 0 – Setting up an Ubuntu VM
###Installing and configuring the software and tools to set up an Ubuntu VM provisioned using Vagrant using Oracle VirtualBox as the hypervisor/provider.
-Operating System: Windows 10 Home x64
####Oracle VM VirtualBox
  *  Source: https://www.virtualbox.org/
 
  *  Downloaded an installed the VirtualBox platform for Windows Hosts
  *  Downloaded and installed Oracle CM VirtualBox Exension Pack. Useful for private net
  * Version: 5.1.22
 


####Vagrant
*  Source: https://www.vagrantup.com/
 
*  Downloaded an installed latest available version of Vagrant for Windows.
*  Version: 1.9.4
 


####MobaXterm
*  Source: http://mobaxterm.mobatek.net
 

*  Brings some common Linux command tools to windows. Acts as shell, SSH, SCP client.
*  Version 10.2
 


*  Additional configuration needed to make MobaXterm work with Vagrant.
  * Set environment variable “VAGRANT_HOME”
 
  * Configure MobaXterm to use Windows PATH variable. This will bring variables within the Windows space to be available in the Linux-like environment in MobaXterm
 

 
####Provisioning the VM
*  Verify Vagrant setup.
  * Ran `vagrant -h` to check if vagrant binaries are accessible.
  * Error encountered below.
 
  * As per research, it is a known issue which can be resolved by upgrading vagrant-share plugin
  * Resolution: Upgrade vagrant-share plugin
  * Reference: https://github.com/mitchellh/vagrant/issues/8532
 
  * Ran the command to upgrade the plugin
 
  * Verified if issue was resolved. Successfully ran `vagrant -h` 
 

*  Created VagrantFile to provision an Ubuntu 14.04 VM using virtualbox as provider.
 
  * ../data on the host PC is shared to /vagrant_data on VM in case files needs to be transferred to and fro
  * IP address set explicitly but will actually still get a default IP from VirtualBox starting from .15


*  Provision the VM
  * Once VagrantFile is created, create/provision Vm using “vagrant up” command.
  * Downloaded the binaries for Ubuntu successfully.
  * Error encountered below when provisioning/starting up the VM using “vagrant up” command.
 
  * Resolution: Upgrade to Vagrant 1.9.5 (Not yet GA)
  * As per research, the error message is already a known issue 
  * Workaround: Replace certain YAML and Ruby files
  * Backed up original files and replaced with ones downloaded below.
  * Reference: https://github.com/mitchellh/vagrant/issues/8520
 
  * `vagrant up` command no longer resulted to errors and successfully provisioned the VM
  * Checked if VM is running.
 

*  Verify access to VM
  * Issue when accessing VM via `vagrant ssh`.
 
  * Workarounds
    * If private IP accessible from Host, SSH directly.
 
    * If Oracle VirtualBox Extensions installed, SSH via forwarded port
 
    * Override “vagrant” command via .BASHRC
      * Reference: https://github.com/mitchellh/vagrant/issues/5559
 
 

*  Used below modified script to allow running `vagrant ssh <name>`
```
[mibucad.Bucad-Lenovo] → cat .bashrc

vagrant() {
  if [[ $1 == "ssh" ]];
  then
    if [[ -z "$2" ]] ;
    then
      command vagrant ssh-config > vagrant-ssh-config && ssh -A -F vagrant-ssh-config $(cat vagrant-ssh-config  |cut -d" " -f2 | head -1 | xargs echo -n)
    else
      command vagrant ssh-config > vagrant-ssh-config && ssh -A -F vagrant-ssh-config "$2"
    fi

  else
    command vagrant "$@"
  fi
}
```

  * Verified that “vagrant ssh” is able to access default VM.
 
