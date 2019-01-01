<h2>Dipankar Barua DataDog Techncial Assignment</h2>
<h3>Spin up a fresh Ubuntu VM via Vagrant</h3>

<h4>1 Let’s Setup Vagrant:</h4>

Before going to setup Vagrant  we have to install some prerequisites such as :

<h4>1.1.Windows Terminal / Mac Terminal / Gitbash Terminal (Recommended For Windows users).</h4>

You can Download Those Terminal Following below Links:

Gitbash- - https://git-scm.com/downloads For Windows.
let's Install Gitbash For Windows Users:

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Gitbash%20Terminal.png" alt="Gitbash Terminal">


Iterm2 - https://www.iterm2.com/ For Mac 

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Iterm2%20for%20Mac%20Users.PNG" alt="Iterm2 Terminal ">


<h4>1.2.Virtual Box /VMware Etc.</h4>

Download the  VirtualBox  Tool – To download this tool visit the website https://www.virtualbox.org/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Virtualbox%20after%20install.PNG" alt="Virtualbox After Installed">

1.3. Now we are going to setup Fresh Ubuntu Platform using in Virtual Box tools via Vagrant.

Download Vagrant and Install it on your system-  https://www.vagrantup.com/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20Website.PNG">

Is vagrant installed or not you can check it by the following command on your Terminal 
Vagrant -v 

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Vagrant%20Version.PNG">

Let’s create a folder on Desktop using Terminal 

Run below command on Terminal

User@Dipankar-Barua MINGW64 ~/Desktop
$ mkdir SetupVagrant

User@Dipankar-Barua MINGW64 ~/Desktop
$

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Vagrant%20Folder%20On%20Desktop.PNG">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/VM%20and%20Terminal.PNG">

To find out the vagrant box visit https://app.vagrantup.com/boxes/search
We are going to select the Ubuntu 16.04 Vagrant Box for the Virtual Box

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20box%20Ubuntu.PNG">

vagrant init ubuntu/xenial64

vagrant up

Then Next I run the Command vagrant up inside the Vagrant Folder

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Ubuntu%20install.PNG">

Following logs after Running the Vagrant up command inside the Vgarant Setup Folder Using Terminal
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'ubuntu/trusty64'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'ubuntu/trusty64' is up to date...
==> default: Setting the name of the VM: SetupVagrant_default_1545842663884_87801
==> default: Clearing any previously set forwarded ports...
==> default: Vagrant has detected a configuration issue which exposes a
==> default: vulnerability with the installed version of VirtualBox. The
==> default: current guest is configured to use an E1000 NIC type for a
==> default: network adapter which is vulnerable in this version of VirtualBox.
==> default: Ensure the guest is trusted to use this configuration or update
==> default: the NIC type using one of the methods below:
==> default:
==> default:   https://www.vagrantup.com/docs/virtualbox/configuration.html#default-nic-type
==> default:   https://www.vagrantup.com/docs/virtualbox/networking.html#virtualbox-nic-type
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 4.3.36
    default: VirtualBox Version: 5.2
==> default: Mounting shared folders...
    default: /vagrant => C:/Users/User/Desktop/SetupVagrant














