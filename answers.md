Your answers to the questions go here.
<br><br>Setup environment:
  <br>https://github.com/DataDog/hiring-engineers/tree/solutions-engineer
  <br>DataDog Demo Setup (14-day trial)
  <br>Be sure to specify “Datadog Recruiting Candidate”
 
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-1-image1.jpg)
 ![alt tag](https://github.com/wmc2112/datadogimages/blob/master/pg-2-image1.jpg)
 
  These instructions are for CentOS/RHEL 6 and above.                                                                    
  <br>Use our easy one-step install.                                                                                                                                                                                                                  
  <br> DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"                                                                                                                                                                                                             
  <br>This will install the YUM packages for the Datadog Agent and will prompt you for your password.                         
  If the Agent is not already installed on your machine and you don't want it to start automatically                      
  after the installation, just prepend DD_INSTALL_ONLY=true to the above script before running it.                                                                                                                                                
  <br>Run:                                                                                                                                                                                                                                            sudo 
  <br>DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"                                                                                
  <br>-> Running transaction check                                                                                            
  <br>---> Package datadog-agent.x86_64 1:6.15.1-1 will be installed                                                          
  <br>--> Finished Dependency ResolutionDependencies Resolved                                                                 
  <br>================================================================================                                        
  <br>Package               Arch           Version             Repository       Size                                          <br>================================================================================                                        
  <br>Installing: datadog-agent         x86_64         1:6.15.1-1          datadog         161       

<br>These instructions are for CentOS/RHEL 6 and above.
Use our easy one-step install.
<strong>DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</strong>
<p>This will install the YUM packages for the Datadog Agent and will prompt you for your password.<br /> If the Agent is not already installed on your machine and you don't want it to start automatically after the installation, just prepend&nbsp;</p>
<p>DD_INSTALL_ONLY=true</p>
<p>&nbsp;to the above script before running it.</p>
<p>&nbsp;</p>
<p>Run:</p>
<p><strong>sudo DD_API_KEY=b18a088feb147e7535796e62ad33fc42 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"</strong></p>
<p>-&gt; Running transaction check</p>
<p>---&gt; Package datadog-agent.x86_64 1:6.15.1-1 will be installed</p>
<p>--&gt; Finished Dependency Resolution</p>
<p>Dependencies Resolved</p>
<p>================================================================================</p>
<p>&nbsp;Package&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Arch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Repository&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Size</p>
<p>================================================================================</p>
<p>Installing:</p>
<p>&nbsp;datadog-agent&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x86_64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:6.15.1-1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; datadog&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 161 M</p>
<p>&nbsp;</p>
<p><strong>Stop, Start and check status of &nbsp;Datadog Agent using:</strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; systemctl start/stop datadog-agent</p>
<p>&nbsp;</p>
<p>systemctl status datadog-agent</p>
<p>datadog-agent.service - Datadog Agent</p>
<p>&nbsp;&nbsp; Loaded: loaded (/usr/lib/systemd/system/datadog-agent.service; enabled; vendor preset: disabled)</p>
<p>&nbsp;&nbsp; Active: active (running) since Mon 2019-12-16 20:37:16 EST; 4min 32s ago</p>
<p>&nbsp;Main PID: 5784 (agent)</p>
<p>&nbsp;&nbsp; CGroup: /system.slice/datadog-agent.service</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; └─5784 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/a..</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Your agent is now reporting to Datadog cloud.&nbsp;</p>
<p>&nbsp;</p>
<p>Because my laptop gets shutdown frequently, I will create some machines in AWS which will allow continuous data flow.</p>
<p>The default Datadog setup will allow access to numerous AWS services, most with read-only access.</p>
<p>&nbsp;</p>
<p>Next setup your AWS access</p>
