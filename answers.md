This .md file contains the procedure [outlined](https://github.com/DataDog/hiring-engineers/tree/support-engineer) by [DataDog] (https://www.datadoghq.com/)

# Challenge Completion

## Level 0 - Installation of Vagrant on Windows 
* Download [Vagrant](https://www.vagrantup.com/docs/installation/)
Setting up a vagrant environment in Windows
* Installation of Vagrant will require a hard system restart, but this procedure allows the use of vagrant in the windows command line

###Installation of Agent to Ubuntu Environment
Note this step assumes the user is logged into DataDog with their default browser
* [Install](https://app.datadoghq.com/account/settings#agent) the DataDog Agent onto the Ubuntu Interface
* Start the Agent using the code snippet provided by DataDog
```terminal
sudo /etc/init.d/datadog-agent start
```
* [Install](https://docs.mongodb.com/v3.0/tutorial/install-mongodb-on-ubuntu/) Mongodb following the instructions here


## Level 1 - Collecting Data


* To get Agent Reporting on Metrics, login to DataDog's web dashboard interface
<img src="http://https://github.com/ziquanmiao/hiring-engineers/tree/master/imgs/fig1.PNG" width="500" height="332" alt="_DSC4652">


#### What is an Agent?
An agent is a software layer that runs in the background of an environment or service that tracks the activity of that interface and reports metrics to DataDog. This process allows users to assess the health and growth of their various internal mechanisms on DataDog's webdashboard. 




	

---------------- NOTES TO DELETE AT END
Steps.
Installation of Software
Setup of Directory
	http://stackoverflow.com/questions/23874260/error-when-trying-vagrant-up
SSH into Virtual Machine on windows
	http://stackoverflow.com/questions/27768821/ssh-executable-not-found-in-any-directories-in-the-path

