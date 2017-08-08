Patrick McBrien

DataDog Answer
08/07/17

**Let's really expand on what others have already accomplished**

Taking a step back i realized that anything on the internet can be monitored with the agent. I got the agent running flawlessly in minutes so I am going to add to what others have already done but go in a slightly different direction seeing as how github user cklener has done a thorough job in answering the questions and explaining along the way. So far I have several datadog agents running with the metrics coming in from these 3 sources. I can look at graphs and CPU but let's go further. I have data is coming from a few places right now.

1. AWS including ec2 instances and disks. Just type in the API key, create a IAM role and you are AWS cloud monitoring.
2. Datadog agent on Vagrant Ubuntu based VM
3. Locally on a Macintosh running under OSX

It really does not matter where the agent gets installed! You can even install it on any IOT device, or even Rasberry PI or Arduino, or a nuclear reactor or a dam. You could even alert on something like temperature or humidity or any 3rd party or custom application.

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/linking-to_aws.png)

I went ahead with the agent and installed in both locations using the same account access key. I also added a LAMP stack as well as mysql to the a shell script and used a very basic Vagrant image. This is a very easy to use system and I really do like using it. I took a slightly different approach to add to the discussion.

**Installing something I can monitor, including mysql**

Mostly complete script to install LAMP environment. 

#!/bin/bash
sudo apt-get -y update
sudo apt-get -y install apache2
sudo apt-get install mysql-server 
sudo apt-get -y install php5 libapache2-mod-php5 php5-mcrypt

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/downloadvagrant.png)

**Local, Vagrant & AWS Setup**

I headed on over to datadoghq.com and created an account that took care of the explaining of most of the integrations. The icons are arranged nicely and mention every devops tool i have ever heard of. They even have a step by step of commands needed to integrate. 

Whether it is bare metal, virtual machines or even communicating to my servers in the cloud is pretty easy to do with no knowledge needed depending on cups of coffee consumed. Datadog is making it easier for people to monitor infrastructure and web applications, that is for sure. Maybe these screenshots I took will help others along the way. 

Vagrant is up and running using a precise64 base is the image we went with

The agent has infinite possibilities beyond normal metrics like CPU and disk or memory utilization.  The agent is like your favorite dog playing fetch. I like the examples you provide. 

Now i have this agent, that can via the webapp at datadoghq.com monitor more than just my cpu. I can write my own custom itegrations, or use ones that datadog has written just like MySQL. 

I am going to be using a Vagrant VM, install virtualbox locally and get the datadog agent installed to monitor mysqld. So far everything has gone smoothly.

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/installing_virtualbox_mac.png)

This worked on Ubuntu to get the agent running

DD_API_KEY=X123123XXXXXYOURKEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

In the meantime, We are showing multiple hosts in the infrastructure area! First is my precise64 Ubuntu box, then my Macintosh.

I now have a nice HTTP symbol in my infrastucture. Now i need to get mysql working.

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/mysql.png)

Now we can see that our all of our service(s) are being monitored including MYSQL, HTTP using Apache, NTP. We can now start a monitor or add a new service integtration with a few steps that can be found in datadog documentaion.

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/More-Apps-MYSQL.png)

Here is an example of an AWS alert with team notifications

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/AWSalertNotify.png)

**Here is my infrastructure running myrandomcheck and a test program that collects data**

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/CustomIntegration.png)

Setting up a basic monitor with tags

![ScreenShot](https://raw.github.com/pmcbrien/hiring-engineers/master/ddog/Monitor.png)

You can also see here that the metrics area now has our custom random check

https://app.datadoghq.com/dash/336506?live=true&page=0&is_auto=false&from_ts=1502153472687&to_ts=1502157072687&tile_size=m

Bonus: Difference between Timeboard and Screenboard.

TimeBoards are used for data correclation so you can make decisions based on grid like data from diffrent sources. They are very specific.

Screenboards can be shared as a whole live and as a read-only entity and are very flexible in terms of the layout. They can also be a summary of datapoints from different places.

Take a look at my graph going over .9


