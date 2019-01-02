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

<h5>Following logs after Running the Vagrant up command inside the Vgarant Setup Folder Using Terminal</h5>
Here is the link of Logs Info 

https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/Vagrant%20Up%20logs.docx

Some Important command For Vagrant

For Destroying- vagrant destroy

For suspend- vagrant suspend

For resuming – vagrant resume 


<h6> We can also change VM base memory and ram </h6>

vb.memory=2048
    vb.cpus =4
    
    
    in the vagrant file 
after saving the file we can reload vagrant -- reload then it will change

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20reload.png">


Now we gonna install vagrant ssh using command vagrant ssh 


Logs below
$ vagrant ssh

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20ssh.png">
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 3.13.0-163-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

  System information as of Wed Dec 26 17:02:38 UTC 2018

  System load:  0.69              Processes:           128
  Usage of /:   3.6% of 39.34GB   Users logged in:     0
  Memory usage: 4%                IP address for eth0: 10.0.2.15
  Swap usage:   0%

  Graph this data and manage this system at:
    https://landscape.canonical.com/

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.

New release '16.04.5 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


vagrant@vagrant-ubuntu-trusty-64:~$







<h4>Below are the steps How to do configurations of Vagrant Setup</h4>

config.vm.box - operating system

config.vm.provider - Virtualbox

config.vm.network - How your host sees your box

config.vm.synced -  how you access files from your computer 

config.vm.provision - what want to setup















