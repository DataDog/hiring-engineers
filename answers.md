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
