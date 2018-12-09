# DataDog Technical Excercise 

#### Applicant: 
#### Date: December 12 2018

## Environment setup

I have setup and tested several environments - in Azure and locally. In Azure it was a Ubuntu Linux host, a Kubernetes based container and a Windows 10 workstation. Localy it was an Ubuntu VM host. 
<img src="01_azureoverview.jpg" width="100%">
The **DD Hostmap** then looks like:

<img src="02_ddhostoverview.jpg" width="100%">

For the sake of this assignment all tasks are beign done on the **testmachine.smit.net** host which is the local VM.I have preconfigured the environment with all necessary packages - python, pip, bench tools etc.
To have reaosnable data and events sent to the DD collector, I simulated certain situation, like high CPU usage with **stress-ng --cpu 0 --perf** and generated traffic on the simple webapp which used a local DB hosted with a simple script like: **for i in `seq 1 1000`; do curl http://0.0.0.0:9999/<name_here>; done**. App has its own randomizer inbuilt. 

