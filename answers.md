# Application as 'Biblical Sales Engineer' at Datadog


 ...I'm sorry, but Senior is no longer the right element within a job title for me!! :trollface:


## So, who the hack is 'The Logfather'

This nickname was given to me by former colleagues at Splunk. Although my focus goes far beyond simple log files, I still carry this name with a certain pride.

I am now biblically 54 years old and have been working for almost 20 years as presales in various companies, but ALWAYS for start-up companies.
Where, if not in such young, agile and open companies, does the own acting and thinking have so much positive influence on the prosperity, the growth and the coming events of ingenious ideas, products and companies.

Before I started in the IT industry, I worked as a roofer, plumber, steel constructor and a lot more.
I also worked as a full-time paramedic for almost ten years.
I gained a foothold in IT about twenty years ago after training as a Java programmer.
However, I am not the code nerd who loves to sit between undefinable amounts of cold pizza boxes and let his genius run free to create incredibly good lines of code.
I'm rather the type of nerd who loves to successfully bring the ingenious ideas of others to the table. For me there is nothing more pleasing than to see how a great idea first becomes a convincing product, and in the next step a brilliant business idea becomes a successful company for everyone involved.

[So let's get started!](https://www.youtube.com/watch?v=IKqV7DB8Iwg)


### And the Oscar goes to....
![And the Oscar goes to....](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_oscar_goes_to.jpeg)

My thanks go to _**Lee Farrar**_ and Datadog for their interest in me and for giving me the opportunity to apply as a Sales Engineer.

# Following now all my answers. 

For everyone's information, the cloud also contains another, very individual version of the answers: https://spark.adobe.com/page/DtglP7uGh51BG/


## Starting with Datadog - Setup the environment

### Step 1: Download

First things first I created a new user account on https://www.datadoghq.com/.

![datadog_account.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_account.png)

From there on I decided to download and run a standalone agent on my macos system, instead of using a VM or Docker approach.   

![datadog_install_1.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_1.png)   

Instead of downloading and running a DMG file on MAC you can simply download and start the installation of the agent buy the use of a simple command line in your terminal:

DD_API_KEY=719d714d7132af72ce6e1f2d8b67b618 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"  

### Step 2: Install

I ran the DMG package and updated the datadog.yaml file with the API key provided on the download page of Datadog!
datadog.yaml config file refers to the path: /opt/datadog-agent/etc/  

![datadog_install_3.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_3.png)

After installing the Datadog agent you can always check the actual status by running following command:

`datadog-agent status`

After successfully installing your agent you will see a message within the Datadog webpage!

![datadog_install_4.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_4.png)

### Step 3: See the results

And from now on you will be able to see first results in the Datadog App!

![datadog_install_5.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_5.png)

## Tagging

Tags are key to Datadog because they allow you to aggregate metrics across your infrastructure at any level you choose while they decouple collection and reporting. Tags can be used to dynamically add additional dimensions to monitoring and analysis. The more unknown levels, areas and entities there are in a monitored environment, the more unmanageable a naming scheme becomes.

Hostnames i.e. can be automatically or manually tagged.  

![datadog_tagging_2.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tagging_2.png)

Tagging different assets helps you to sort which hosts are located in a specific federal state.  

![datadog_tagging_3.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tagging_3.png)  

### Create a new tag  
Tagging is made very easy within Datadog by the ability to create new tags or assign tags to different assets.  

![datadogs_tagging_4](https://github.com/simuvid/hiring-engineers/blob/master/images/datadogs_tagging_4.png)

Or you use the only true approach for seasoned men within the datadog.yaml file.  

Don't forget to save the file and restart the agent after the changes have been made.  

![datadog_tags_config](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_tags_config.png)

From now on you can start to group, search and filter by tags.

![hosts](https://github.com/simuvid/hiring-engineers/blob/master/images/hosts.png)

## Integrations

Datadog offers out of the box more than 200 integrations in every imaginable environment:
  
- AWS
- Azure
- Google
- Cloud
- OS & Systems
- Databases
and way more....
  
As an example for an integration I decided to build one for my PostgreSQL DB.

### Step 1: Create a user  

Thankfully we have already deployed an agent on my system that already runs a PostgreSQL DB.

So at next we have to define a new Datadog user within PostgreSQL, like shown on the left, to grant appropriate access for the agent to PSQL.

![create an user in PSQL](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_postgre_user.png)

### Step 2: Configure the Datadog agent   

In the postgres.d/conf.yaml file in the conf.d directory a few adjustments have to be made. Then restart the agent.

![config PSQL](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_postgre_conf.png)  

### Step 3: Watch the new host
The SQL DB Server now appears as a new host in our Datadog environment.

![PSQL Integration](https://github.com/simuvid/hiring-engineers/blob/master/images/postgre_host.png)  
  
  
## Custom agents
### Chicken or Egg?  

Integration vs. Agent Check

Agent checks are a great way to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service or open source project, we recommend that you write an Integration.
  
### Step 1: Create your files
<Your_Project>.py within opt⁩ ▸ ⁨datadog-agent⁩ ▸ ⁨etc⁩ ▸ ⁨checks.d⁩
<Your_Project>.yaml within opt⁩ ▸ ⁨datadog-agent⁩ ▸ ⁨etc⁩ ▸ ⁨conf.d⁩ ▸ ⁨<your_project>.d⁩  

For my example I decided to create an Agent check which simulates a CPU usage metric, means a random value between 1 and 99 percent usage.  
  
![Agent Python](https://github.com/simuvid/hiring-engineers/blob/master/images/logfather.py.png)  
    
Each check has a YAML configuration file that is placed in the conf.d directory. The file name should match the name of the check module (e.g.: logfather.py and logfather.yaml).  
    
![Agent Config](https://github.com/simuvid/hiring-engineers/blob/master/images/logfather.yaml.png)  

### Step 2: Deploy and test the files  

After copying the files into the appropriate directories like shown earlier, we can test our Agent checks before using them by running following command:  

`Logfather$ datadog-agent check logfather` 

![Agent Check](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_AgentCheck_Test.png)

### Step 3: Run the Agent check  

After successfully testing the check we can restart the Agent and after a few moments we see in the Datadog App our new metric!
