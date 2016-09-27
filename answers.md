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


#### In my own words, what is an Agent?
An agent is a software specific solution that is integrated into a web or infrastructure service tracking all the conceivable metrics produced. The agent interacts with Datadog's webservice allowing serviced members to determine the quality and health of their systems using DataDog's high level visualization tools. 

#### Adding tags to config file
Access the nano text editor 
```
	sudo nano /etc/dd-agent/datadog.conf 
```
I uncommented the sample tag provided by datadog and added my own tag: ziquanstag

<img src="https://raw.github.com/ziquanmiao/hiring-engineers/tree/master/imgs/fig2.PNG" width="500" height="332" alt="_DSC4652">
The picture below shows a screenshot of my host and its tags in the Host Map Page of Datadog.
<img src="https://raw.github.com/ziquanmiao/hiring-engineers/tree/master/imgs/fig3.PNG" width="500" height="332" alt="_DSC4652">
		

#### Connecting and Integrating MongoDB
I integrated Mongodb following the instructions [here](https://app.datadoghq.com/account/settings#integrations/mongodb)

The image below shows my connection activity to MongoDB from the hosts page
<img src="https://raw.github.com/ziquanmiao/hiring-engineers/tree/master/imgs/fig4.PNG" width="500" height="332" alt="_DSC4652">



#### Custom Agent Check
I added the conf.YAML and check.py files into the correct locations, allowing me to access the metric on datadoghq
<img src="https://raw.github.com/ziquanmiao/hiring-engineers/tree/master/imgs/fig5.PNG" width="500" height="332" alt="_DSC4652">


## Level 2 - Visualization of Data


---------------- NOTES TO DELETE AT END
Steps.
Installation of Software
Setup of Directory
	http://stackoverflow.com/questions/23874260/error-when-trying-vagrant-up
SSH into Virtual Machine on windows
	http://stackoverflow.com/questions/27768821/ssh-executable-not-found-in-any-directories-in-the-path
	set PATH=%PATH%;C:\Program Files\Git\usr\bin
