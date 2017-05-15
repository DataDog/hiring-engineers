
# The Challenger – Marc Ian Bucad

## Level 0 – Setting up an Ubuntu VM

### Installing and configuring the software and tools to set up an Ubuntu VM provisioned using Vagrant using Oracle VirtualBox as the hypervisor/provider.

- Operating System: Windows 10 Home x64

#### Oracle VM VirtualBox
  *  Source: https://www.virtualbox.org/
  <img src="https://dl.dropboxusercontent.com/s/euih82oyla8ze1h/001.png=0" />
  *  Downloaded an installed the VirtualBox platform for Windows Hosts
  *  Downloaded and installed Oracle CM VirtualBox Exension Pack. Useful for private net
  *  Version: 5.1.22
  <img src="https://dl.dropboxusercontent.com/s/8ft4733ehqltjon/002.png?dl=0" />
 

#### Vagrant
*  Source: https://www.vagrantup.com/
 <img src="https://dl.dropboxusercontent.com/s/uxmugieq3rv4yfm/003.png?dl=0" />

*  Downloaded an installed latest available version of Vagrant for Windows.
*  Version: 1.9.4
 <img src="https://dl.dropboxusercontent.com/s/5sttcgvjj40txli/004.png?dl=0" />


#### MobaXterm
*  Source: http://mobaxterm.mobatek.net
 <img src="https://dl.dropboxusercontent.com/s/e5qxvgjjewg34p4/005.png?dl=0" />

*  Brings some common Linux command tools to windows. Acts as shell, SSH, SCP client.
*  Version 10.2
 <img src="https://dl.dropboxusercontent.com/s/9w7v6yh6rrfs634/006.png?dl=0" />



*  Additional configuration needed to make MobaXterm work with Vagrant.
  * Set environment variable “VAGRANT_HOME”
 <img src="https://dl.dropboxusercontent.com/s/s8betn46h6rnv30/007.png?dl=0" />

  * Configure MobaXterm to use Windows PATH variable. This will bring variables within the Windows space to be available in the Linux-like environment in MobaXterm
 <img src="https://dl.dropboxusercontent.com/s/5hhmppkxufqkn7q/008.png?dl=0" />

<img src="https://dl.dropboxusercontent.com/s/qz8sauxoee5efzi/009.png?dl=0" />

 
#### Provisioning the VM
*  Verify Vagrant setup.
  * Ran `vagrant -h` to check if vagrant binaries are accessible.
  * Error encountered below.
 <img src="https://dl.dropboxusercontent.com/s/lr564n0qvgjcvpt/010.png?dl=0" />

  * As per research, it is a known issue which can be resolved by upgrading vagrant-share plugin
  * Resolution: Upgrade vagrant-share plugin
  * Reference: https://github.com/mitchellh/vagrant/issues/8532
 <img src="https://dl.dropboxusercontent.com/s/i6t2zrwl148djet/011.png?dl=0" />

  * Ran the command to upgrade the plugin
 <img src="https://dl.dropboxusercontent.com/s/kvenlbj7324c5nn/012.png?dl=0" />

  * Verified if issue was resolved. Successfully ran `vagrant -h` 
 <img src="https://dl.dropboxusercontent.com/s/y5upe4jo25igzqs/013.png?dl=0" />


*  Created VagrantFile to provision an Ubuntu 14.04 VM using virtualbox as provider.
 <img src="https://dl.dropboxusercontent.com/s/r5w8tmc23j0mnvg/014.png?dl=0" />

  * ../data on the host PC is shared to /vagrant_data on VM in case files needs to be transferred to and fro
  * IP address set explicitly but will actually still get a default IP from VirtualBox starting from .15


*  Provision the VM
  * Once VagrantFile is created, create/provision Vm using “vagrant up” command.
  * Downloaded the binaries for Ubuntu successfully.
  * Error encountered below when provisioning/starting up the VM using “vagrant up” command.
 <img src="https://dl.dropboxusercontent.com/s/t0h0ulky85uls14/015.png?dl=0" />

  * Resolution: Upgrade to Vagrant 1.9.5 (Not yet GA)
  * As per research, the error message is already a known issue 
  * Workaround: Replace certain YAML and Ruby files
    * Backed up original files and replaced with ones downloaded below.
    * Reference: https://github.com/mitchellh/vagrant/issues/8520
 <img src="https://dl.dropboxusercontent.com/s/cwn3ulotz260crr/016.png?dl=0" />

  * `vagrant up` command no longer resulted to errors and successfully provisioned the VM
  * Checked if VM is running.
 <img src="https://dl.dropboxusercontent.com/s/fq9efrev4igx37u/017.png?dl=0" />


*  Verify access to VM
  * Issue when accessing VM via `vagrant ssh`.
 <img src="https://dl.dropboxusercontent.com/s/gu0yzkksdcvqv2q/018.png?dl=0" />

  * Workarounds
    * If private IP accessible from Host, SSH directly.
 <img src="https://dl.dropboxusercontent.com/s/21480zy8zh2c46v/019.png?dl=0" />

    * If Oracle VirtualBox Extensions installed, SSH via forwarded port
 <img src="https://dl.dropboxusercontent.com/s/scs8vs7g32f2j2e/020.png?dl=0" />

    * Override “vagrant” command via .BASHRC
      * Reference: https://github.com/mitchellh/vagrant/issues/5559
 <img src="https://dl.dropboxusercontent.com/s/v718qds1l3sbacr/021.png?dl=0" />
<img src="https://dl.dropboxusercontent.com/s/p0ottr0yg22vtmp/022.png?dl=0" />

 

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
 <img src="https://dl.dropboxusercontent.com/s/hj1ac1yh5rtbrpy/023.png?dl=0" />
