Your answers to the questions go here.
-------------------------------------------------------------------------------

Prerequisites - Setup the environment
- Spinning up a fresh linux VM via Vagrant
  - Per instruction I go here: https://www.vagrantup.com/intro/getting-started/
  - Install Vagrant and VirtualBox using the download links on the page
  - In terminal, input the first 'Up and Running' command:
    ![Get a Vagrantfile](/assets/setup/Get_a_vagrantfile.png)
  - Use vagrant up to bring up the machine
    ![vagrant up](/assets/setup/vagrant_up.png)
  - And ssh into the machine using vagrant ssh
    ![vagrant ssh](/assets/setup/vagrant_ssh.png)
  - Run vagrant init as detailed in instructions here: https://www.vagrantup.com/intro/getting-started/project_setup.html
  - That throws an error saying 'The program 'vagrant' is currently not installed.' Terminal says to install it with sudo apt-get install vagrant, so I try that.
  - I still get an error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
  - Neither of those work, so I google and find this link:    
    https://askubuntu.com/questions/364404/e-unable-to-fetch-some-archives-maybe-run-apt-get-update-or-try-with-fix-mis
  - Which tells me to try this: sudo apt-get update. And that seems to work!
    ![apt-get update](/assets/setup/apt_get_update.png)
  - Then I run sudo apt-get install vagrant again. Yaas, this works! So I run vagrant init and get this message:
    ![vagrant init](/assets/setup/vagrant_init.png)
  - Um, I think my earlier steps to get the Vagrantfile might have been enough and I didn't need to go through all that drama if vagrant init-ing. But oh well, onwards to Vagrant Boxes!
  - I run vagrant box add hashicorp/precise64 and get an error. Curious, I click ahead in the instructions and realize I'm already done and this step was unnecessary.
    ![install box](/assets/setup/install_box.png)
  - So I open up Virtual Box and it seems it's up and running!
    ![virtual box](/assets/setup/virtual_box.png)
