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
- Signing up for Datadog    
  - On the Datadog signup page here: https://app.datadoghq.com/signup I follow the three steps to sign up
    Filling out form info:
    1. ![sign up 1](/assets/setup/signup_1.png)
    2. ![sign up 2](/assets/setup/signup_2.png)

    Installing the agent:
    3. I want to install the agent on Ubuntu so I use these directions:
      ![agent setup instructions](/assets/setup/agent_setup.png)
      I paste the one step install step into terminal, where I'm told I need to install curl:
      ![one_step_install_first_try](/assets/setup/one_step_install_first_try.png)
      So I run this: sudo apt-get install curl
      And then try the one step install line again, which gives me this:
      ![agent_install_confirmation](/assets/setup/agent_install_confirmation.png)
      And on the Datadog site, I get a message that the Agent is reporting!
      ![agent_reporting](/assets/setup/agent_reporting.png)
      I click finish and am in!
      ![welcome_page](/assets/setup/welcome_page.png)
