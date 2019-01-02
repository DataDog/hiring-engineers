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

Run Below command Inside your Ubuntu Server

DD_API_KEY=610080f148d9e4d47efed7c611e64d7d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20agent%20install%20on%20Ubuntu.png">

Step by Step Installation:

Run these commands step by step to install the Datadog Agent in your Server.

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20agent%20step%20by%20step.png">


1.3   Datadog Container Docker Install by following command 


docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=610080f148d9e4d47efed7c611e64d7d datadog/agent:latest


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Docker%20install%20on%20Ubuntu%20.png">


Docker installtion logs:

vagrant@ubuntu-xenial:~$ sudo docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=610080f148d9e4d47efed7c611e64d7d datadog/agent:latest
Unable to find image 'datadog/agent:latest' locally
latest: Pulling from datadog/agent
790c37dedd62: Pull complete
289cb409a94c: Pull complete
c8c8c4faaf9e: Pull complete
237fb89e1ed6: Pull complete
f57b386ca81e: Pull complete
847930fc0785: Pull complete
dc7a1564846a: Pull complete
2f9394a89b51: Pull complete
Digest: sha256:301adad25c80a2d976c47f77b5341479cf0e5f2f81db353c90568e8c42ab6576
Status: Downloaded newer image for datadog/agent:latest
6ee6039e47b205ea357fb9485ca04ddf99a48581b9c1dd7736cf59a56844a2bd
vagrant@ubuntu-xenial:~$


Is Datadog is running or not  to know I run the command below
sudo datadog-agent status

Here is the Datadog running status Logs:

https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/datadog_running_statusd_log



To get the related info of Datadog agent we can use below command 

DESCRIPTION	COMMAND
Start Agent as a service	sudo service datadog-agent start

Stop Agent running as a service	sudo service datadog-agent stop

Restart Agent running as a service	sudo service datadog-agent restart

Status of Agent service	sudo service datadog-agent status

Status page of running Agent	sudo datadog-agent status

Send flare	sudo datadog-agent flare

Display command usage	sudo datadog-agent --help

Run a check	sudo -u dd-agent -- datadog-agent check <check_name>


I have already installed all the necessary packages those are all in vagrant provision shell script.

To get the MySQL config file change the directory 



vagrant@vagrant-ubuntu-trusty-64:/etc/datadog-agent/conf.d$

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20metric.png">

And also install manually MySQL integrations.
After installing the MySQL integration I restart my datadog agent

by following command 

sudo service datadog-agent restart

logs

vagrant@vagrant-ubuntu-trusty-64:/etc/datadog-agent/conf.d/mysql.d$ cd

vagrant@vagrant-ubuntu-trusty-64:~$ sudo service datadog-agent restart

datadog-agent stop/waiting

datadog-agent start/running, process 9504

vagrant@vagrant-ubuntu-trusty-64:~$




vagrant@vagrant-ubuntu-trusty-64:~$ sudo service datadog-agent restart

datadog-agent stop/waiting

datadog-agent start/running, process 9712


# Collecting Metrics:

Mysql 
sudo mysql -u root -p



I used this Documents to create new user with password;
https://docs.datadoghq.com/integrations/mysql/

Configuration

Edit conf.d/mysql.d/conf.yaml in the root of your Agent’s configuration directory in order to connect the Agent to your MySQL server. You will begin collecting your MySQL metrics and logs right away. See the sample configuration filefor all available configuration options.

PREPARE MYSQL
On each MySQL server, create a database user for the Datadog Agent:
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';
    
Query OK, 0 rows affected (0.00 sec)

For mySQL 8.0+ create the datadog user with the native password hashing method:
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by '<UNIQUEPASSWORD>';
Query OK, 0 rows affected (0.00 sec)


sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog';"

CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog';

GRANT PROCESS ON *.* TO 'datadog'@'localhost';

I gave user is datadog and password also datadog

# Images:
<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/mysql%20configurations%20for%20tags.png">




