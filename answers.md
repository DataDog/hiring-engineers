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

Install the above tools and locate the ubuntu image from [here](https://app.vagrantup.com/boxes/search?utf8=%E2%9C%93&sort=downloads&provider=&q=ubuntu)👈
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/40.png" width="750px" />
</div>

**Step 3.**

Create a new folder as c:\ubuntu, run cmder.exe and run cmd "vagrant box add ubuntu/xenial64" to copy the Ubuntu image to the local host. Once Vagrant finish copying the image, run "cd c:\Ubuntu" and "vagrant init ubuntu/xenial64" to generate the config files in c:\ubuntu. Then run "vagrant up" to spin up the test environment.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/50.PNG" width="750px" />
</div>

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/60.PNG" width="750px" />
</div>

**Step 4.**

After input "vagrant up" through cmder.exe, a virtual machine will be generated in Virtualbox, once that has been confirmed, run cmd "vagrant ssh-config" through cmder to get the ssh login info and run the cmd "ssh vagrant@127.0.0.1 -p *port number* -i *location of the private key*" to login to the VM. (The third step only happens on the first login)
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

Install the datadog agent: When login for the first time, datadog will ask to setup the agent, choose "Ubuntu" to get the install cmd as _DD_API_KEY=b233617fcf6a0f29a9715078391b4716 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"_. In the meantime, bottom is displayed as "Waiting for agent to report".
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/92.png" width="750px" />
</div>

Login to Shell through cmder as step 4 in the previous section and run the datadog install cmd.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/110.PNG" width="750px" />
</div>

Once you see the below screenshot, that means the agent has been installed successfully. Also, the agent status will change to as in the screenshot below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/120.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/93.png" width="750px" />
</div>

Move to the /etc/datadog-agent directory and edit datadog.yaml, update it as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/130.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/140.PNG" width="750px" />
</div>

Run cmd "apt-get update" when you login as root and then run "reboot" to restart the VM. Then the tags are updated as in the screenshot.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/81.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/160.png" width="750px" />
</div>

**Step 2.**

Install mysql on ubuntu by running cmd "apt-get install mysql-server", during the installation, mysql will ask for root password, input the password and hit ok. Once it finishs installing, run cmd "systemctl status mysql.service" to check the status, when you see the screenshot below, that means mysql has been installed successfully.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/170.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/180.PNG" width="750px" />
</div>

Follow the latest mysql integration doc from [here](https://docs.datadoghq.com/integrations/mysql/).
Login to mysql and Create the datadog user and give access:
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/190.PNG" width="750px" />
</div>

Run the check cmds.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/200.PNG" width="750px" />
</div>

Give access to performance_schema.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/210.PNG" width="750px" />
</div>

Create the conf.yaml in mysql.d directory and edit it as described in the doc.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/220.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/230.PNG" width="750px" />
</div>

Install the mysql integration from datadog website.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/240.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/250.png" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/260.PNG" width="750px" />
</div>

