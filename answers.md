Level0 – Setup an Ubuntu VM
I created the linux VM as suggested and completed all work in this environment.

Level1 – Collecting your Data

![level1_ddinstall](https://user-images.githubusercontent.com/30450337/28699337-07761752-7317-11e7-8723-a3969e4deb42.PNG)

Retrieve Metrics - I retrieved the Agent reporting metrics by using the API and pulling all active metrics.  Please see file Level1_GetMetrics.sh
Below are the active metrics.

![level1_metrics_api](https://user-images.githubusercontent.com/30450337/28699339-0777223c-7317-11e7-8f13-fef7ba6ae88b.PNG)

Bonus – What is the Agent?
DataDog’s Agent is software that runs in the background on your hosts.  Think of it as the engine that keeps DataDog running whether you are using it or not.  The Agent is responsible for collecting the events and metrics you see in DataDog.  There are three components to the Agent - the collector, DogstatsD and the forwarder.  The Collector, as its name suggests, collects systems metrics from your integration points. This can include things like memory and CPU usage.  DogstatsD is a tool that allows you to make use of custom metrics from an application.  An example of this would be the number of page views a certain website has.  The Forwarder serves to queue up and send data received from the other two components over to DataDog.

Adding Tags – I added tags both using the Agent config file and also by using the API. See file Level1_SetTags.sh for the code to do this via API.  
Below is a screenshot of the config file and the new tags

![level1_tagsviaconffile](https://user-images.githubusercontent.com/30450337/28699354-07d6d04c-7317-11e7-8d90-df7cd38d6bb4.PNG)

Below is a screenshot of the new tags in the Host Map page.  The tags added via API as well as the ones in the config file are present.

![level1_tags](https://user-images.githubusercontent.com/30450337/28699348-07ad9c9a-7317-11e7-8767-2e798f6bcbd3.PNG)

Install a database – I chose to install PostgreSQL
Below is where I verified the PostgreSQL installation

![level1_postgresverification](https://user-images.githubusercontent.com/30450337/28699340-077716ca-7317-11e7-8a24-5d46e7e27638.PNG)

Below is a screenshot of the output from PostgreSQL check

![level1_postgrescheck](https://user-images.githubusercontent.com/30450337/28699336-0775cd60-7317-11e7-91f3-4ce4cbdae528.PNG)

Below is a screenshot of the postgres.yaml file I created to get the integration working

![level1_postgresyamlconfig](https://user-images.githubusercontent.com/30450337/28699342-0791c9fc-7317-11e7-86ef-d8b31431aa1c.PNG)

![level1_postgresafterinstallhost](https://user-images.githubusercontent.com/30450337/28699338-0776afc8-7317-11e7-9234-22a88e0a22ea.PNG)

Random value agent check – below is a screenshot of the random.yaml and the random.py used to create the custom agent check.  These have both been checked in as well.

![level1_randonyaml](https://user-images.githubusercontent.com/30450337/28699346-07943e6c-7317-11e7-973c-0401e3a58123.PNG)

![level1_ramdonpy](https://user-images.githubusercontent.com/30450337/28699344-0793c77a-7317-11e7-8c78-cd41a351dc68.PNG)

Below is the output of the test I ran against the random check

![level1_randomcheck](https://user-images.githubusercontent.com/30450337/28699343-0793b1e0-7317-11e7-88ee-bafc50c2efcb.PNG)

Below is a screenshot of the Random check in the metrics screen

![level1_randometricscreen](https://user-images.githubusercontent.com/30450337/28699345-0793d436-7317-11e7-8216-cf70d1b7666a.PNG)

Level2 – Visualizing your Data
Cloned Dashboard	
Below are 2 screenshots of the cloned dashboard with additional database metrics and test.support.random

![level2_cloneddashboardwadditionalmetrics_1of2](https://user-images.githubusercontent.com/30450337/28699350-07d4ede0-7317-11e7-80ec-b875f2b1b691.PNG)

![level2_cloneddashboardwadditionalmetrics_2of2](https://user-images.githubusercontent.com/30450337/28699351-07d5db9c-7317-11e7-9a24-9cfff876cdf7.PNG)

Bonus – Timeboard vs Screenboard

In a TimeBoard all graphs are scoped to the same time. The graphs are organized into a grid for easy comparison and correlation.  You can share graphs in a TimeBoard individually. 

A ScreenBoard is designed to be flexible and customizable.  You can drag and drop widgets onto a ScreenBoard each of which can have different time frame.  These widgets can be shared together as a whole.

Notification Snapshot

Below is a screenshot of where I sent the test.support.random notification to my email.

![level3_metricrectangle](https://user-images.githubusercontent.com/30450337/28700152-edb8ed12-731b-11e7-9bdd-f3df80dfd317.png)

Below is the email mentioned above

![level3_metricemailabove0 9](https://user-images.githubusercontent.com/30450337/28699352-07d64078-7317-11e7-9d02-5b04e16b6852.PNG)

Level3 – Alerting on your Data

Below are 4 screenshots of where I set up the monitor that notify you when my test metric goes above the 0.90 threshold at least once during the last 5 minutes

![level3_monitorstep1](https://user-images.githubusercontent.com/30450337/28700398-8b14751c-731d-11e7-81bd-e3cb797e8aef.PNG)

![level3_monitorsimplealert](https://user-images.githubusercontent.com/30450337/28699358-07f33598-7317-11e7-8930-dcaad46243cf.PNG)

![level3_monitorsetupconditions](https://user-images.githubusercontent.com/30450337/28699356-07f14a94-7317-11e7-9a94-dde0988c052e.PNG)

![level3_monitorstep4](https://user-images.githubusercontent.com/30450337/28700396-8b0dd4c8-731d-11e7-9f4f-3c5de71ee0d9.png)

![level3_monitorsetupnotification](https://user-images.githubusercontent.com/30450337/28699359-07f344e8-7317-11e7-97a2-48174dcff068.PNG)

Bonus – Multi-Alert
Below is a screenshot of where I set up the monitor above as a Multi-Alert

![level3_monitorsetupmulti-alert](https://user-images.githubusercontent.com/30450337/28699357-07f2db34-7317-11e7-8b75-37f8c68c2479.PNG)

Below is the email received from the monitor to notify me that the threshold had been surpassed

![level3_thresholdalertemail](https://user-images.githubusercontent.com/30450337/28700484-fef9f52e-731d-11e7-9ada-39781ef88541.PNG)

Bonus – Downtime

Below is the downtime configuration as well as the email I received.

![level3_monitordowntime](https://user-images.githubusercontent.com/30450337/28699349-07ca115e-7317-11e7-85f2-5d93e2effd9b.PNG)

![level3_monitordowntimeemail](https://user-images.githubusercontent.com/30450337/28699355-07e9c47c-7317-11e7-9093-54204cbc95fa.PNG)


