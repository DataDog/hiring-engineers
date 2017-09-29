### Level 1: Collecting Your Data 
   1a) Sign Up for Datadog
   ![sign up](./datadog_pics/sign_up.png) 
   
   1b) Get the Agent Reporting Metrics From Local Machine
    
   * After signing up, you will be taken to a screen where you can begin to set up your first agent. Here, you can choose which type of Operating System you would like to run the agent on (in my case I installed Vagrant and VirtualBox, so therefore chose Ubuntu) 
     ![agent](./datadog_pics/agent_home.png) 
    
   * After choosing your machine, you will be redirected to a page that shows how to set up the Agent. In Ubuntu's case it was as simple as copying the call provided on the page into my local VM environment. 
    ![ubuntu_api](./datadog_pics/ubuntu_agent_install.png) 

   ![api](./datadog_pics/api.png) 

   * After running the call in your terminal, when it finishes you should see the following screens, the first in your terminal and the second on the datadog agent page itself. On the bottom of the Datadog page there will be an option to continue.
    ![agent success](./datadog_pics/agent_success.png) 

   ![data dog site success](./datadog_pics/datadog_site_success.png) 

   * Finally, moving forward on the DataDog site will bring you to your Agent page and your first metrics, which look like this: 
    ![metrics](./datadog_pics/metrics_window.png) 

  **BONUS** What is The Agent? 
    
    * The Agent is the software that collects data, events, and metrics and sends them to Datadog, so that we as the customer can use this data to better monitor the performance of one's applications, as well as use the information to find potential problematic areas in the codebase. There are three pieces to the Agent: 
      1) The collector, which runs checks according to whatever integrations you have and captures system metrics.
      2) Dogstatd, which is a backend server that you can send custom metrics to.
      3) The forwarder, which gets data from the two aforementioned components and queues it up to be sent to Datadog.

