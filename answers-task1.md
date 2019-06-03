Your answers to the questions go here.
Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

TASK #1A: You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.

ANSWER #1A: 

Brief Explanation:
Vagrant is one of the automated provisioning tool to quickly spin up virtual machines.
I spun up 2 VMs by customizing the Vagrant configuration file. I planned them for Web and Database Servers.
The 2 VMs are sg-web-01 and sg-db-01. I use the Ubuntu/Xenial64 (v. 16.04).

Steps:
-	Download Vagrant
-	Download Virtual Box
-	Install Vagrant
-	Install Virtual Box
- Within the Windows command prompt, I ran:
PS C:\HashiCorp\Vagrant\bin> .\vagrant.exe init ubuntu/xenial64
Before deploying the VMs, I edited the Vagrantfile for creating 2 VM boxes.

config.vm.define "web" do |web|
    web.vm.box = "ubuntu/xenial64"
  end

 config.vm.define "db" do |db|
    db.vm.box = "ubuntu/xenial64"
  end

PS C:\HashiCorp\Vagrant\bin> .\vagrant.exe up

Reference:
https://www.vagrantup.com/intro/getting-started/index.html
