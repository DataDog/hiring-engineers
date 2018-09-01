# Prerequisites - Setup the environment

Answers : I use Vagrant and VirtualBox to setup the test environment. Since I am working on a windows PC, I choose cmder as the console emulator for Shell.

**Step 1.**

Download Vagrant (Windows 64 bit) from [here](https://releases.hashicorp.com/vagrant/2.1.4/vagrant_2.1.4_x86_64.msi).👈

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/1.png" width="750px" />
</div>

Download VirtualBox from [here](https://download.virtualbox.org/virtualbox/5.2.18/VirtualBox-5.2.18-124319-Win.exe).👈

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/10.png" width="750px" />
</div>

Download cmder from [here](https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder.zip).👈

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/30.png" width="750px" />
</div>

**Step 2.**

Install the above tools and locate the ubuntu image from [here](https://app.vagrantup.com/boxes/search)

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/40.png" width="750px" />
</div>

**Step 3.**

Create a new folder as c:\Ubuntu, run cmder.exe and run cmd "vagrant box add ubuntu/xenial64" to copy the Ubuntu image to the local host. Once Vagrant finish copying the image, run "cd c:\Ubuntu" and "vagrant init ubuntu/xenial64" to generate the config files in c:\ubuntu. Then run "vagrant up" to spin up the test environment.

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/50.PNG" width="750px" />
</div>

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/60.PNG" width="750px" />
</div>

**Step 4.**

After input "vagrant up" through cmder.exe, a virtual machine will be generated in Virtualbox, once that has been confirmed, run cmd "vagrant ssh-config" through cmder to get the ssh login info and run the cmd "ssh vagrant@127.0.0.1 -p *port number* -i *location of the private key*" to login to the VM.

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/80.PNG" width="750px" />
</div>

**Step 5.**

Signup a free datadog trail account from [here](https://www.datadoghq.com/#) and use “Datadog Recruiting Candidate” in the “Company” field and login after creating the account.

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/90.png" width="750px" />
</div>

# Collecting Metrics

**Step 1.**


