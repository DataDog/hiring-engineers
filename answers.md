# DD-AGUERRERO-ASSESMENT
TEST DATA DOG
Alcides Guerrero

Content:
1. Setup the enviroment and Install Datadog Agent.
2. Collect Metrics.
3. Visualize Data.
4. Monitor Data.
5. Collect APM Data.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Setup the enviroment and Install Datadog Agent

First, i have downloaded and installed Vagrant 2.2.19 and Virtual Box 6.1, in my Windows 10 computer.
I have created a new folder to allocate all the files for the VM.

vagrant init hashicorp/bionic64

[![Setup-the-enviroment-1-1.png](https://i.postimg.cc/MT5qnL3k/Setup-the-enviroment-1-1.png)](https://postimg.cc/ygDw5Lzn)

Once  the virtual enviroment was ready, i run the VM:

vagrant up

[![Setup-the-enviroment-1-2.png](https://i.postimg.cc/qq8JkRfL/Setup-the-enviroment-1-2.png)](https://postimg.cc/vxZFhGZg)


[![Setup-the-enviroment-1-3.png](https://i.postimg.cc/qqGPbCV9/Setup-the-enviroment-1-3.png)](https://postimg.cc/Mfv3XHGD)

After the VM run, i proceed tosing up my trial Account in the Data Dog Web to install the  Agent: 
Then I have installed the Datadog agent: 

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=xxxxxxxxxxxxxxxxxxxx DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

[![Setup-the-enviroment-1-4.png](https://i.postimg.cc/pLvZV1jY/Setup-the-enviroment-1-4.png)](https://postimg.cc/fJHXBCBJ)

[![Setup-the-enviroment-1-5.png](https://i.postimg.cc/WpkY2yzt/Setup-the-enviroment-1-5.png)](https://postimg.cc/yW7yjvFz)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

2.Collect Metrics

After the instalation of the Datadog agent, i have added tags to the configuration file: datadog.yaml located in: /etc/datadog.agent/.

[![collect-metric-2-1.png](https://i.postimg.cc/Bv2tZsrM/collect-metric-2-1.png)](https://postimg.cc/mc2T8x2H)

Once the tags are added and the file have been saved, i restarted and check the status of the DD Agent.

sudo systemctl restart datadog-agent
sudo systemctl status datadog-agent

[![collect-metric-2-2.png](https://i.postimg.cc/T2sxsFSw/collect-metric-2-2.png)](https://postimg.cc/yW02gQ74)

After confirm everything is working good, i have check on Datadog platform:

[![collect-metric-2-3.png](https://i.postimg.cc/44Yyn6RY/collect-metric-2-3.png)](https://postimg.cc/z318cRBN)

After done with the tags, i  proceed to install and integrate mysql with datadog platform.

sudo apt-get install mysql-server

[![collect-metric-2-4.png](https://i.postimg.cc/Jzfcdr3q/collect-metric-2-4.png)](https://postimg.cc/v4vV4dNg)

Then i have check the status of the mysql server:

[![collect-metric-2-5.png](https://i.postimg.cc/x1Mb8KHv/collect-metric-2-5.png)](https://postimg.cc/sMf20GTx)

To avoid issues when the VM start up, i have set auto system start up for MySQL Server:

[![collect-metric-2-6.png](https://i.postimg.cc/C50wvqdg/collect-metric-2-6.png)](https://postimg.cc/wyWKM3hf)

Next, i have create a database user with appropriate permissions to collect metrics from the database.

mysql> CREATE USER 'datadog'@'%' IDENTIFIED WITH mysql_native_password by '<UNIQUEPASSWORD>';

[![collect-metric-2-7.png](https://i.postimg.cc/MHpFK6FB/collect-metric-2-7.png)](https://postimg.cc/5YD3sV19)
  
Next, i have prepared mysql server, giving privilegies to collect the metrics:
  
[![collect-metric-2-8.png](https://i.postimg.cc/y8420HJM/collect-metric-2-8.png)](https://postimg.cc/rKjhL7Nj)

once we have created the user, grant the acces to DB, we can see the integration showed up in the UI:

[![collect-metric-2-9.png](https://i.postimg.cc/DzyhbTH2/collect-metric-2-9.png)](https://postimg.cc/75cdppqc)
  
[![collect-metric-2-10.png](https://i.postimg.cc/5NdMSvTK/collect-metric-2-10.png)](https://postimg.cc/5j3GxHx8)
  
After, i used the agent commands to verify MySQL is integrated:
  
[![collect-metric-2-11.png](https://i.postimg.cc/tJ9N9B7m/collect-metric-2-11.png)](https://postimg.cc/FdnLZgyj)  
  
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Navigate to /etc/datadog-agent/conf.d and create a file for the Agent check, and added the following into my_metric.yaml and save the file.
  
[![collect-metric-2-12.png](https://i.postimg.cc/3xG1C0M1/collect-metric-2-12.png)](https://postimg.cc/LJHjmX8g)
  
Then navigate to /etc/datadog-agent/checks.d and create a file called my_metric.py and add the following code into the file.

 [![collect-metric-2-13.png](https://i.postimg.cc/65kL367v/collect-metric-2-13.png)](https://postimg.cc/SJGz1hfS)
  
After creating the files and added the code, i run the command: sudo -u dd-agent -- datadog-agent check my_metric to verify my metric:
  
[![collect-metric-2-14.png](https://i.postimg.cc/Vk9MkqQx/collect-metric-2-14.png)](https://postimg.cc/NKMLNr0D)
  
Showing my_metric in the summary: 
  
[![collect-metric-2-15.png](https://i.postimg.cc/wvrRGFLm/collect-metric-2-15.png)](https://postimg.cc/YG1S46Xr)
  
By default the custom check will run at 15 second intervals. Update the my_check.yaml file so that it runs at 45 second intervals:
  
[![collect-metric-2-16.png](https://i.postimg.cc/CKP4wGbF/collect-metric-2-16.png)](https://postimg.cc/HJMM27SK)
  
[![collect-metric-2-17.png](https://i.postimg.cc/NFpsnjWP/collect-metric-2-17.png)](https://postimg.cc/2LLNbrj4)
  
---------------------------------------------------------------------------------------------------------------------------------------------

QUESTION: 
  
- Can you change the collection interval without modifying the Python check file you created?

  Yes, you can update the collection interval in my_metric.yaml file that i have created.
  
  
-----------------------------------------------------------------------------------------------------------------------------------------------

  3. Visualize Data.
  
  Utilize the Datadog API to create a Timeboard.
 To create the conection with the API i have created API Key and the application key: 
  
  [![imagvisualize-data-3-1.png](https://i.postimg.cc/2ydvQLM9/imagvisualize-data-3-1.png)](https://postimg.cc/MfTvxHW1)
  
  [![imagvisualize-data-3-2.png](https://i.postimg.cc/763bd89f/imagvisualize-data-3-2.png)](https://postimg.cc/hzGSQYHB)
  
  After created the Keys for api amd app, i have validated the api keys with postman: 
  
  [![imagvisualize-data-3-3.png](https://i.postimg.cc/28bNSFpx/imagvisualize-data-3-3.png)](https://postimg.cc/Vd8V7tkS)
  
  After validation, procced with installation of the Python3-pip libraries on my vm and the data dog api-client.
  
  [![imagvisualize-data-3-4.png](https://i.postimg.cc/wxSgJbQr/imagvisualize-data-3-4.png)](https://postimg.cc/t7tKGkfd)
  
  after installing i had some issues and i have upgrade  the datadog-api-client
  
  [![imagvisualize-data-3-5.png](https://i.postimg.cc/0QhRYbDS/imagvisualize-data-3-5.png)](https://postimg.cc/9RPnVXxX)
  
  After installe dthe api client, i create the example.py file:
  
 [![imagvisualize-data-3-6.png](https://i.postimg.cc/t4JkjDLX/imagvisualize-data-3-6.png)](https://postimg.cc/BjWH55Sy)
  
 [![imagvisualize-data-3-7.png](https://i.postimg.cc/nV1G96xF/imagvisualize-data-3-7.png)](https://postimg.cc/MXvQh3XN)
  
 After installing the client and created the example.py file, I  have  run the following command to exacute the python code and create the example dashboard
  
 DD_SITE="datadoghq.com" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "example.py"
  
 [![imagvisualize-data-3-8.png](https://i.postimg.cc/4Nq7Y5Y4/imagvisualize-data-3-8.png)](https://postimg.cc/GHPhNvP6)
  
 After the execution of the command, i have confirmed into the platform that have been created.
 
  [![imagvisualize-data-3-9.png](https://i.postimg.cc/8PJsg6t2/imagvisualize-data-3-9.png)](https://postimg.cc/kBC7xBrs)
  
 After confirmed the api is working, i have edited the script in example.py.
 The First widget takes the average of metric, the second widget uses the anomalies function and the third widget uses the rollup function.
 
  [![imagvisualize-data-3-10.png](https://i.postimg.cc/59HFbTtK/imagvisualize-data-3-10.png)](https://postimg.cc/G9CpjMGv)
 
 Once i have edit the scrip, i have executed the command via terminal to see the changes in the platform:
 
 [![imagvisualize-data-3-11.png](https://i.postimg.cc/CLPtkZ0x/imagvisualize-data-3-11.png)](https://postimg.cc/0bScqyrT)
 
 
 This is the Dashboard in the Datadog platform:

[![imagvisualize-data-3-12.png](https://i.postimg.cc/Hk1MSzdZ/imagvisualize-data-3-12.png)](https://postimg.cc/GHz9tkBG)
  
 This is the response we have in the past 5 minutes: 
[![imagvisualize-data-3-13.png](https://i.postimg.cc/dV99rprm/imagvisualize-data-3-13.png)](https://postimg.cc/68yRNHHy)
  
this is the snap i have made: 

[![imagvisualize-data-3-14.png](https://i.postimg.cc/tgYVJM5g/imagvisualize-data-3-14.png)](https://postimg.cc/McJGrtgk)

This is the capture of the email from the comment:
  
[![imagvisualize-data-3-15.png](https://i.postimg.cc/NfFypn3k/imagvisualize-data-3-15.png)](https://postimg.cc/F7tsKTsY)
  
Question: 
  
  What is the Anomaly graph displaying?

The anomaly function is an algorithmic, shows as a grey band in the metric line, showing th expected behavior of a series based on the past. 
  

Capture of the anomaly graph:
[![imagvisualize-data-3-16.png](https://i.postimg.cc/gjCPyn95/imagvisualize-data-3-16.png)](https://postimg.cc/Lg37248B)
  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------  
  
4. Monitor Data.

Navigate to Monitors in the Datadog platform and create a new monitor.
I have created a new monitor for my_metryc:

Defining alert conditions
[![monitor-data-4-1.png](https://i.postimg.cc/Rh6WV6Qb/monitor-data-4-1.png)](https://postimg.cc/q6rJ17F8)  
  
create a notification that alerts yourself. Notifications support template variables with examples:

  [![monitor-data-4-2.png](https://i.postimg.cc/Y0YFkDHs/monitor-data-4-2.png)](https://postimg.cc/y36xyPWm)
  
View from DataDog platform:
  
[![monitor-data-4-3.png](https://i.postimg.cc/QMvVtg0G/monitor-data-4-3.png)](https://postimg.cc/SX7m1MBD)

Test message to confirm the notification of the 3 alerts:
  
Warning: 

[![monitor-data-4-4.png](https://i.postimg.cc/pX3SspGV/monitor-data-4-4.png)](https://postimg.cc/Yhf89qBT)
  
Alert
  
[![monitor-data-4-5.png](https://i.postimg.cc/5t8jXYGX/monitor-data-4-5.png)](https://postimg.cc/xkT97C9Q)

No Data
  
[![monitor-data-4-6.png](https://i.postimg.cc/ZK9b9vvJ/monitor-data-4-6.png)](https://postimg.cc/qzTVSRGF)
  

Scheduling downtime for the notification after 7PM week days.
  
[![monitor-data-4-7.png](https://i.postimg.cc/fRDM82gR/monitor-data-4-7.png)](https://postimg.cc/hfZFjrBk)
  
Scheduling downtime for notification on Weekends whole day: 

[![monitor-data-4-8.png](https://i.postimg.cc/zvT1jKCh/monitor-data-4-8.png)](https://postimg.cc/dZQXQ7SQ)
  
Both down times created: 

[![monitor-data-4-9.png](https://i.postimg.cc/rwn75QBb/monitor-data-4-9.png)](https://postimg.cc/68ZHXL5L)
  
[![monitor-data-4-10.png](https://i.postimg.cc/zvrQqMhL/monitor-data-4-10.png)](https://postimg.cc/2b0Gw02m)
  
  
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
5. Collecting APM Data:
  
I have installed pip, after pip i have installed ddtrace:

[![Collecting-APM-5-1.png](https://i.postimg.cc/6p8Tr174/Collecting-APM-5-1.png)](https://postimg.cc/ZWhTZHxJ)
  
Instalation of Flash: 
  
[![Collecting-APM-5-2.png](https://i.postimg.cc/cH0sbDJm/Collecting-APM-5-2.png)](https://postimg.cc/gwtFwH8X)
  
I have created a basic app, app.py:
  
[![Collecting-APM-5-3.png](https://i.postimg.cc/sgdbmMxP/Collecting-APM-5-3.png)](https://postimg.cc/ZCHfKKr0)
  
i have add configuration to the datadog's  agent for the APM:
  
[![Collecting-APM-5-4.png](https://i.postimg.cc/nzDPqZxS/Collecting-APM-5-4.png)](https://postimg.cc/Q9jmr2Hc)
  
After i have run the command of the configuration snippet
DD_SERVICE="TEST_DATADOG_ALCIDES" DD_ENV="apm_test" DD_LOGS_INJECTION=true ddtrace-run python app.py
  
[![Collecting-APM-5-5.png](https://i.postimg.cc/Yq5jxzQX/Collecting-APM-5-5.png)](https://postimg.cc/KR5ZGLqL)
  
