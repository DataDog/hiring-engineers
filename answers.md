# CJ's guide to the Datadog Hiring Challenge completed on Windows 8

## Level 1 - Data Collection
### Signing up for a Datadog Account
To start the process of the Hiring Challenge, you must begin by setting up a Datadog account. Go to "https://app.datadoghq.com" to begin. As seen in the photo below, click on the 'sign up' link circled in red.
![][loginpage]  
  
On the next page, fill in your information, making sure to fill in the company field with 'Datadog Recruiting Candidate' as seen below in red.  
![][accountsetup]
  
To verify that the Datadog Agent is correctly reporting metrics from your local machine, go to the Metrics Explorer page (see red circle on the left of the page below) and input 'system.cpu.system' into the graph textbox (see top middle, underlined in red below). If the Agent is correctly reporting you will be able to see a graph on the right side of the page, circled in red below).
![][metricexplorer]
  
### Bonus question: In your own words, what is the agent?
>The Agent is a piece of software that integrates all hosts’ events and metrics and puts them in one centralized location making tracking easier for the user. From here, creating monitors and visualizations are made easy through the easy-to-use GUI keeping the user in the loop whenever certain user-defined scenarios arise.

### Adding tags to Agent config
To open the Agent config file, open the Datadog Agent Manager and click on the settings tab in the top left corner (circled in red below). In order to add the tags to the config file, add text replacing the 'CJtag1' and 'CJtag2' in the bottom center (circled in red below). For more information on basic agent usage on Windows visit: https://docs.datadoghq.com/guides/basic_agent_usage/windows/
![][settings]
  
### Checking the Agent config file
To verify that the Agent config file was successfully updated, go to the Host Map within the Agent and ensure that your custom tags appear under the 'Tags' section labeled 'Datadog Agent' For more information on the host map visit: https://docs.datadoghq.com/guides/hostmap/
![][hostmap]
  
### Install MongoDB and its Datadog Integration
Begin this step by visting the MongoDB website (URL circled in red at the top in image below, https://www.mongodb.com/download-center#community). Select the appropriate version from the dropdown box based on your machine.
![][mongodb]
  
Next visit the integrations page within the Agent (see circled in red below).  Find the integration you wish to install, in this case it is MongoDB, and hover over the icon. A button will appear to begin the installation. Once the integration is installed, hover over the icon again and click 'configure'.
![][integrations]
  
Follow the instructions from the dialog box that appears. In order to get the Mongo Shell running in Windows, open a command prompt and run 'mongod' from the installation directory (see image below for example).  Once the Mongo Shell is up and running, copy and paste the code from the dialog box to set up an administrator for Datadog. Be careful to note here that there are 2 tabs, one for Mongo 2.x and one for Mongo 3.x, ensure that you have selected the tab corresponding to your system's MongoDB.
![][mongodbload]
  
Within the Datadog Agent Manager, select 'Mongo' from the left (see highlighted in blue below). From here you can directly edit the conf.d file for the MongoDB integration. Again copying the code from the dialog box from the configuration menu (see example below), you can create a connection between the Agent and MongoDB on your machine. 
![][mongoconfd]
  
To verify that the machine is properly communicating with the Agent, click on 'Logs and Status' (see circled in red below) within the Datadog Agent Manager and go to the 'Agent Status'.  If there is proper communication, there will be a section under 'Checks' labeled 'mongo' that will have an 'OK' (see circled in red below).
![][mongodbcheck]
  
### Creating a custom Agent check
To create a custom Agent check, you must write a script saved in the checks.d folder (located at samplepath\Datadog\Datadog Agent\agent\checks.d). Below shows an example script written in Python that samples a random metric, 'test.support.random'. For more information on custom Agent checks see: https://docs.datadoghq.com/guides/agent_checks/  
![][randomcode]
  
## Level 2 - Data Visualization
### Clone a dashboard and add metrics
To clone a database integration dashboard, you must first open up the original dashboard (circled in red on left below). Select the MongoDB dashboard to open it (circled in red on right below)
![][dashboard]
  
From the dashboard, click on the settings button in the top right corner (circled in red on the top right below). This opens up a drop down box. Select 'Clone dashboard' (see circled in red below).
![][howtoclone]
  
To add metrics to the cloned dashboard that you just created, drag and drop the corresponding icon at the top (circled in red below) onto the dashboard where you would like it to appear. If you do not see this toolbar, click on the 'Edit Board' icon and it will appear. After the icon has been dropped onto the dashboard, a window will appear in which you can choose the details of the metric. 
![][addmetrics]
  
From the metric editor, you can select details relevant to the type of metric you are adding. In the image below you see an example of the graph editor which has 4 sections. First, you can select the type of graph visualization. Second, you can add metrics and events to show. This can be filtered by tags and select hosts. Additionally, multiple metrics can be overlaid onto the same graph. Third, you can select the display preferences which includes the x-scale and the option to include a legend. Lastly, you add or omit a title for the graph and there are formatting options. For more information on graphing see: https://docs.datadoghq.com/graphing/
![][grapheditor]
  
The image below shows an example of two graphs that have been added to the cloned dashboard. Once the graphs are made, they can be re-sized and moved around the dashboard to be placed where convenient.
![][cloneddashboard]

### Bonus question: What is the difference between a timeboard and a screenboard?
>Timeboards are time-synchronized with an automatic layout. That is, all graphs will appear equal size and on the same time scale. This is mainly used for troubleshooting and correlation. Screenboards, on the other hand, are more flexible and customizable. These can include widgets and graphs of different sizes and timeframes. It utilizes a drag-and-drop style to help the user develop a custom view on their system.

### Take a snapshot of the graph test.support.random
From the integrations dashboard 'Custom Metrics - test', you can take a snapshot of the graph by hovering the mouse over the graph and clicking on the camera icon at the top right. This will open a window where you can select a portion of the graph to add a note to. Additionally, you can add a box around a specific portion of the graph that you would like to draw attention to (see second image below for example) If you would like to send this snapshot in an e-mail, be sure to add a notification to the message with the format '@sample@email.address' (see circled in red in the first image below). The second image below is an example of the e-mail that will be received. For more information on the @-notifications see: https://help.datadoghq.com/hc/en-us/articles/203038119-What-do-notifications-do-in-Datadog-
![][snapexample]
![][snapshot]

## Level 3 - Data Monitoring
### Create a monitor
To create a monitor, go to the monitors drop down menu and select 'New Monitor'. From here you can select your monitor. For this example we will show how to set up a monitor for the metric test.support.random (see 'metric' highlighted in blue below).  For more information on monitoring see: https://docs.datadoghq.com/guides/monitors/
![][monitortype]
  
Since we want to create an alert that will trigger when test.support.random goes above 0.90, we will select 'Threshold Alert'. Next, we define the metric 'test.support.random' with the option to filter where the data is coming from. For this example we will leave the default settings. Then, we will make it a multi-alert so that it has scalability when our infrastructure grows. The multi-alert will be triggered by host (see circled in red below).
![][monitor1]
  
Step 3 is where we define the details of the alert. In this example we want to be alerted when the metric goes above 0.90 during the last 5 minutes. Thus, we set the information accordingly as seen in the image below. The red box is the alert threshold with an optional warning threshold if you'd like to be alerted when the metric is approaching the alert threshold. For this example we will not use the warning threshold. Be sure to note that after you input the alert threshold, the graph at the top of the page will be modified to visualize where the threshold is in red (see second image below). There are a handful of other settings that can be manipulated to make the monitor work exactly as you need, including modifiers that will require a full window of data and no missing data in order to alert.
![][monitor2]
![][monitorthreshold]
  
Lastly, we need to set up the monitor to alert the team when the threshold is crossed. Similar to the snapshot example above, the monitor messaging supports the '@' handle to notify teammates via e-mail and is markdown supported. As seen in the image below, this message can be succinct to get the point across quickly or could be built out to include much more information. It is good practice to include a link to the dashboard for convenience. The second image shows an example e-mail of what an alert would look like (note: the graph doesn't properly show the metric going above 0.90 due to granularity issues.)
![][monitor3]
![][monitor]

### Set up a scheduled downtime
To schedule a downtime, go to the monitors drop down menu and select 'Manage Downtime'. Click on the 'Schedule Downtime' link in the yellow box (see image below). This will open the schedule downtime window.
![][scheduledowntime]
  
Within the schedule downtime window, you can choose which monitors you would like to silence, including being able to filter it using scope (For more information on scope see: https://docs.datadoghq.com/graphingjson/#scope). In this example I have set the monitor we setup above to be silenced and the local host as the scope. Similarly, the downtime will take place daily from 7:00pm to 9:00am. Ensure that the time zone is set to the proper location. There is also the option to have the downtime end on a certain date, if that is desirable.
![][downtime1]
  
The next step is to add a message to alert the team when the downtime will be scheduled. Similar to the monitor above, this message supports markdown, as well as the '@' handle for notifying teammates. The first image below gives an example message and the second image below gives an example e-mail that would be received.
![][downtime2]
![][downtime]

[cloneddashboard]: https://image.ibb.co/hw4SPk/cloneddashboard.png
[hostmap]: https://image.ibb.co/iZWvVF/hostmap.png
[snapshot]: https://image.ibb.co/bMPHPk/snapshotbox.png
[randomcode]: https://image.ibb.co/b4t0VF/test_random_code.png
[downtime]: https://image.ibb.co/gDgtja/downtime.png
[monitor]: https://image.ibb.co/f0QTja/trigger.png
[accountsetup]: https://image.ibb.co/fGkwfF/account_setup.png
[loginpage]: https://image.ibb.co/fmRf7v/login_page.png
[metricexplorer]: https://image.ibb.co/edkJua/metric_explorer.png
[settings]: https://image.ibb.co/bCvJua/settings.png
[integrations]: https://image.ibb.co/iSW0qF/integrations.png
[mongoconfd]: https://image.ibb.co/nPKLqF/mongoconfd.png
[mongodb]: https://image.ibb.co/dwVtAF/mongodb.png
[mongodbcheck]: https://image.ibb.co/f1VtAF/mongodbcheck.png
[mongodbload]: https://image.ibb.co/ijJPHv/mongodbload.png
[dashboard]: https://image.ibb.co/nbkbVF/dashboard.png
[howtoclone]: https://image.ibb.co/i7R0qF/howtoclone.png
[addmetrics]: https://image.ibb.co/d2VZ4k/addmetricsdashboard.png
[grapheditor]: https://image.ibb.co/d14ac5/grapheditor.png
[snapexample]: https://image.ibb.co/eehNPk/snapshotexample.png
[monitorthreshold]: https://image.ibb.co/jBJNqQ/monitoralertthreshold.png
[monitor1]: https://image.ibb.co/cdb8VQ/monitorstep1.png
[monitor2]: https://image.ibb.co/gvcRH5/monitorstep2.png
[monitor3]: https://image.ibb.co/nstcPk/monitorstep3.png
[monitortype]: https://image.ibb.co/hkY0c5/monitortype.png
[scheduledowntime]: https://image.ibb.co/nN7U4k/scheduledowntime.png
[downtime1]: https://image.ibb.co/cdjvAQ/downtimestep1.png
[downtime2]: https://image.ibb.co/dUvwH5/downtimestep2.png
