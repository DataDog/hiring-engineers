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
    ![info](./datadog_pics/my_success.png)

4) Write a Custom Agent Check

  * First, we will want to go back to the Datadog Docs and select the "Writing an Agent Check Option" on the left scrollbar, which will take us to step-by-step instructions of writing one's first check.
    ![agent_check_doc](./datadog_pics/agent_check_doc.png)

  * In order to run a a custom check correctly, we must create two separate files
    1) a .yaml file in the etc/dd-agent/conf.d directory 
    2) a .py file in the etc/dd-agent/checks.d directory 
  
  * These files names MUST MATCH (test.yaml, test.py for example) or the process will not work.

  * For the yaml file and the purposes of this challenge, the config presented in the docs should be fine. In other situations the init will allow you to set config options that will run on every check of self.init_config.
    ![yaml](./datadog_pics/yaml.png)

  * For the py file, we need to first make sure that we are inheriting from the AgentCheck class, as well as importing the random module. Every check class should have a check method, inside of which we can use any of the built-in DogStatd methods (A list of the methods can be find on this Doc page, under "sending metrics"). For these purposes we want to use the gauge method, like so:
    ![random](./datadog_pics/random.png)

  * After these files are created and saved, we must restart the agent for them to take effect. If everything runs smoothly, we can then run our agent info request (seen in the Guide to the Agent portion of the docs), and see if our check is running:
    ![check_success](./datadog_pics/agent_check_success.png)

  * We can also check our custom checks by calling them through the Agent (custom checks cannot be directly called from Python). In ubuntu, this done with:
    
    sudo -u dd-agent dd-agent check <CHECK_NAME>
  
  which should bring up a status similar to this:
    ![random_check](./datadog_pics/random_check.png)

### Level 2: Visualizing Your Data 

1) Clone the Database Integration Dashboard and Add Metrics 

  * Go back to your Datadog home page, and select the "dashboard list" option after clicking the Dashboard button, which looks like this:
    ![dashboard_button](./datadog_pics/dashboard_button.png)

  * On the page this leads you to, scroll down into "Integration Dashboards" and select the Database that you had decided to integrate previously (MySQL in my case).

  * From here we are going to want to click on the settings button on the top right, and then select "Clone Dashboard"
    ![clone](./datadog_pics/clone.png)

  * This will bring up a small box where you can rename the new dashboard. Do what makes sense to you and simply click Confirm to create the cloned dashboard, which can now be found under "Custom Dashboards" in the dashboard list.

 # Adding Metrics 

  * The first thing we will want to do is find the Graphing Primer. If we go to the datadog docs and search "graphing" in the search bar on the top left, the graphing primer should pop up as the first option. Select the option and you should now be at this page:
    ![primer](./datadog_pics/graphing_primer.png)

  * You should have a specific metric that you are interested in mind. The [summary](https://app.datadoghq.com/metric/summary) is a good place to see some potential metrics to choose from.

  * Using the primer as a guide, go back to your newly cloned dashboard and scroll down until you see an empty square that says "add a graph". Selecting this will bring up a set of graph options at the bottom to choose from. Choose whichever you think will be most helpful for you and drag your choice into the empty box. This should open up a page that looks like this:
    ![new_metric](./datadog_pics/new_metric.png)

  * From this page search for the metric you wish to track and select "Add Metric". You can also filter and aggregate hosts through this, but for the purpose of this excercise it is not necessary. When you have added your metric(s), simply select Save at the bottom right of the screen. After saving, your new metric graph should show up at the bottom of your dashboard, named with the title you gave it 
    ![packet](./datadog_pics/packet.png)

  * To add your custom check from the end of level 1, simply repeat the same process, and search for "test.support.random" as the desired metric. As long as the check was set up correctly previously, it should show up, and you can simply select the metric, name the graph, and viola:
    ![custom](./datadog_pics/custom.png)

  **BONUS** What is the difference between a timeboard and a screenboard?

  * A *timeboard* is used primarily for troubleshooting and correlation representation. They show time synchronized events, and a good example would be the database integration dashboard that we have.
    ![timeboard](./datadog_pics/timeboard.png)


  * A *screenboard* is used primarily for status boards and sharing data. You can mix widgets and timeframes, and there is a customizable drag and drop layout
    ![screenboard](./datadog_pics/screenboard.png)






