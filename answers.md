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

https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrantup%20log



<h4>Below are the steps How to do configurations of Vagrant Setup</h4>

config.vm.box - operating system

config.vm.provider - Virtualbox

config.vm.network - How your host sees your box

config.vm.synced -  how you access files from your computer 

config.vm.provision - what want to setup


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20box%20configure%20image.png">

Here is the Configurations File URL - https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrant%20File



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


Here is the Vgarant ssh Logs File


https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrant%20ssh%20logs


If we search now var /www we will not find for that we have to install apache2 

Lets Run the below command
Sudo apt-get update
Sudo apt-get install –y  git 
Sudo apt-get install –y  apache2


vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www
html
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www/html
index.html
vagrant@vagrant-ubuntu-trusty-64:~$


For networking localhost has setup in vagrant file  and saved the file 

   config.vm.network "forwarded_port", guest: 80, host: 8080



logs –
Setting up ssl-cert (1.0.33) ...
Processing triggers for libc-bin (2.19-0ubuntu6.14) ...
Processing triggers for ufw (0.34~rc-0ubuntu2) ...
Processing triggers for ureadahead (0.100.0-16) ...
vagrant@vagrant-ubuntu-trusty-64:~$ ls var/www/html
ls: cannot access var/www/html: No such file or directory
vagrant@vagrant-ubuntu-trusty-64:~$ clear
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www
vagrant@vagrant-ubuntu-trusty-64:~$ cd html
-bash: cd: html: No such file or directory
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www/html
index.html
vagrant@vagrant-ubuntu-trusty-64:~$ exit
logout
Connection to 127.0.0.1 closed.


User@Dipankar-Barua MINGW64 ~/Desktop/SetupVagrant
$ vagrant reload
==> default: Attempting graceful shutdown of VM...

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Apache2%20run.png">


Apache setup 

http://localhost:8080/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/apache%20working%20local%208080.png">



We can also use local private network using vagrant file network setting config.vm.network "private_network", ip: "192.168.33.10"

http://192.168.33.10/


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/image16.png">



#Folder setting 
  config.vm.synced_folder ".", "/var/www/html"



# config file sync
<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/apache%20server%20file.png">




Sign up for Data dog:

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20Signup.png">


1,2.Containerized approach with Docker for Linux and our dockerized Datadog Agent image

The Datadog agent was successfully installed via the following:

We can install two ways: First one is recommended









