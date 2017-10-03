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
    1. The collector, which runs checks according to whatever integrations you have and captures system metrics.
    2. Dogstatd, which is a backend server that you can send custom metrics to.
    3. The forwarder, which gets data from the two aforementioned components and queues it up to be sent to Datadog.

2) Tags and the Host Map 
  
  * The first thing you should do is head to the Datadog Docs (which can be found with a quick Google search) and select "Getting Started With the Agent". The Datadog Docs page looks like this:
    ![docs](./datadog_pics/datadog_docs.png)

  * After selecting this, there is a scrollbar on the left where you can choose the type of system you are running on (For me it was Ubuntu). Select your OS and it will take you to a a page with more information about Agent usage for each specific OS. Under "Configuration" on this page, there will be a specific path that shows you exactly where your Agent Config file is being held.
    ![agent_ubuntu](./datadog_pics/agent_usage_ubuntu.png)  
    ![config](./datadog_pics/agent_config.png) 
 
  * Now that we know where the file is, go back to the Datadog docs and select "Guide to Tagging" from the scrollbar on the left. This will take you to a page that looks like this:
    ![tags](./datadog_pics/guide_to_tagging.png) 
    On this page there is a section titled "Assigning tags using the configuration files", which explains how to correctly create tags in the file we located above.
    ![assign_tags](./datadog_pics/assign_tags.png) 

  * Now, in your terminal go to the directory that your specific agent config file is located, open the file and simply add tags under the portion of the file that directs you to do so.
     ![add_tags](./datadog_pics/add_tags.png) 
     After adding your tags, you will need to restart the agent to update the config files using the necessary command.

  * Now that our tags are set, we can go back to our datadog home page and click on this button to get to the HostMap:
     ![host](./datadog_pics/host_map_button.png) 

  * After getting to the HostMap page, simply click on the host (big green thing in the center), and the tags should show up on the right under "Tags" (specifically under the subheading "Datadog Agent")
    ![agent_tags](./datadog_pics/agent_tags.png) 

3) Database Integration (with MySql)

  * First, after deciding which database you would like to install (I chose MySQL), use the magic of Google to find an easy step-by-step process to install the database correctly. This will vary considerably depending on the OS in use.

  * After this, on your metrics home screen go to the puzzle-piece button at the top and select "integrations".
    ![integration_button](./datadog_pics/integration_button.png)

  * This will take you to a page with a list of a bunch of potential integrations. Select the one that matches the database you installed, and follow the instructions. The instructions will look similar to this: 
    ![instructions](./datadog_pics/integration_instructions.png)

  * After following the instructions, restart your Agent and wait five minutes. Then, if successful, you should see something like this if you click on the integration again:
    ![integration_success](./datadog_pics/integration_success.png)

  * You can also run your OS versions of the Agent info command (check the agent guide in the docs), and it should return something like this:
    ![info](./datadog_pics/info_my_success.png)

4) Write a Custom Agent Check 


