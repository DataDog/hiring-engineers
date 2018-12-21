##Prerequisits - Setup the environment

1) [Went to GitHub repo and forked it onto my local computer](/hiring-engineers/pics_for_environment_setup/0_github_repo_forked.png)
1.5) Virtual machine already installed on local computer
2) [Installed vagrant](/hiring-engineers/pics_for_environment_setup/1_installingvagrant/2_successwithvagrant.png)
3) [Vagrant successfully installed](/hiring-engineers/pics_for_environment_setup/2_successwithvagrant.png)
4) [virtual box running from terminal](/hiring-engineers/pics_for_environment_setup/3_virtualboxrunning.png)
5) [attempted to install DD needed curl so installed curl](/hiring-engineers/pics_for_environment_setup/4_installingcurl.png)
6) [Installed DD using prompted command](/hiring-engineers/pics_for_environment_setup/5_installingdatadogonVM.png)
7) [DD success in terminal](/hiring-engineers/pics_for_environment_setup/6_DataDogRuns.png)
8) [DD Reports metrics from local machine](/hiring-engineers/pics_for_environment_setup/7_DataDogReportsmetricsfromlocalmachine.png)
9) Environment setup complete! :D

##Collecting Metrics

0) Trying to figure out how  to agent config file so I can add a tag
1) needed sudo nano /etc/datadog-agent/datadog.yaml to read the .yaml file
2) got a NTP error
3) research how to fix NTP error. NTP fixed itself?
4) Check to see if agent is running, there is a problem.
5) found the error, went into the .yaml and fixed it
6) It works!! There are the tags!
7) Went to host map and put tags there to see them

8) Installing mysql server on VM
9) It LIVES!!! Mwahahahahaha (the mysql server
10) give dd access to mysql. Test. success!
11) checked for mysql.yaml after editing
12) success

13) my_metric.yaml 
14) my_metric.py 
15) changed interval from 30 seconds to 45 seconds between updates

Note: I started here https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6 but was confused when after following the instructions it didn't work. 

I have never done this before so I Googled how to do this. The website that looked the most promising is this: https://datadog.github.io/summit-training-session/handson/customagentcheck/. Which is similar to  but not the same. In step 3 it says to go into the conf.d. Then step 4 is create the .yaml file. In step 6 says "Create a new check file in the checks.d directory. Name the file checkvalue.py." However, as noted above we are in conf.d and checks.d is in the parent directory. There was a lot of confusion in this regard.

It took me quite a while to figure out that checks.d and conf.d are in the same directory and that I shouldn't create a new one. I would like to suggest that when giving instructions that the full path be utilized to avoid this kind of error.


Bonus: Yes, the instance rate is found in the .yaml not the .py

