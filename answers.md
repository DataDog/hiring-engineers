# Prerequisites - Setup the environment

Answers : I use Vagrant and VirtualBox to setup the test environment. Since I am working on a windows PC, I choose cmder as the console emulator for Shell.

**Step 1.**

Download Vagrant from [here](https://www.vagrantup.com/)

![1](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/1.png)
Download VirtualBox from [here](https://www.virtualbox.org/).

![2](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/10.png)
Download cmder from [here](http://cmder.net/)

![3](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/30.png)
**Step 2.**

Install the above tools and locate the ubuntu image from [here](https://app.vagrantup.com/boxes/search)

![4](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/40.png)
**Step 3.**

Create a new folder as c:\Ubuntu, run cmder.exe and run cmd "vagrant box add ubuntu/xenial64" to copy the Ubuntu image to the local host. Once Vagrant finish copying the image, run "cd c:\Ubuntu" and "vagrant init ubuntu/xenial64" to generate the config files in c:\Ubuntu. Then run "vagrant up" to spin up the test environment.

![5](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/50.PNG)
![6](https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/60.PNG)
