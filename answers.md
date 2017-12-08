<h1>Table of Content</h1>
1. Installing DataDog Agent

2. Collecting Metrics
  
  
 <h2>1. Installing Datadog Agent</h2>
  
Begin by signing up the Datadog website and filling out all required credentials and information.
   ![Logo](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/debdbde804f263ec43926b810dc206986dd7639d/Screenshot%20from%202017-12-05%2021-19-32.png)
   
Reach this screen by clicking the link below.
![Logo](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-22-40.png)
  <br>https://app.datadoghq.com/signup/agent
  
Depending on the Operarting system you are using, click on the operating system on the left bar and click on it. In this case since we are using Ubuntu, click on Ubuntu.
  
Press CLT + ALT + T to pull up the terminal. Copy the key and paste it into the terminal and press enter.
![alt text](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-30-01.png)

The installation should be successful if you see the screen below.

![alt text](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2022-20-42.png)

<h2>2. Collecting Metrics</h2>
To show that your machine is currently being monitored, it has to tagged to be shown on the Host Map. We will set it up to show the storage capacity of the monitored machine.

Hover over Metrics and Click on Explorer

Under graph, select the option "System.disk.free", Under over, select your machine & select "device" under one graph per:
