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


To find out the vagrant box visit https://app.vagrantup.com/boxes/search
We are going to select the Ubuntu 16.04 Vagrant Box for the Virtual Box

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20box%20Ubuntu.PNG">

vagrant init ubuntu/xenial64

vagrant up











