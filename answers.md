# Prerequisites - Setup the Environment

I used the **macOS** environment to complete this exercise.

1- I created my account on https://www.datadoghq.com/
2- To install the **Agent** on my machine I chose the **Mac OS X** platform from the menu list because I'm using the macOS environment and copied this installation command (I removed the API KEY value from the command below to make sure that I don't expose it, and hid it using a black banner on the screenshot image below): 


`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<API KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"` 
![Agent Installation](/images/img1.png)

3- From here I was able to access the **Datadog Agent Manager** and check the Agent reporting metrics.

![Agent Status](/images/img2.png)

![Agent Logs](/images/img3.png)

# Collecting Metrics
## Adding Tags
I added tags in 2 ways by checking [Getting started with Tags](https://docs.datadoghq.com/getting_started/tagging/):
1- Manually using the configuation file where I search for the **tags** section and added 2 tags there and restarted the agent.

![Tags1](/images/img4.png)


2- Using the UI of the Host Map Page. I added 1 new tag

![Tags1](/images/img5.png)

## Database Installation
1)I decided to install and work with **MongoDB**.
 I followed the [official mongoDB documentation](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) to install mongoDB community edition on my     local machine. <br>
 - I installed it with **brew** using these 2 commands:
  `brew tap mongodb/brew` <br>
  `brew install mongodb-community@4.4` <br>
  
  I started the MongoDB service using `brew services start mongodb-community@4.4` and to make sure that its running I used this command `brew services list`
  ![MongoDB Started](/images/img6.png)
Now that I have MongoDB installed on my local machine, I need to install its corresponding Datadog Integration. I followed this [official Datadog document](https://docs.datadoghq.com/integrations/mongo/?tab=standalone) for the MongoDB integration.
I opened the **Mongo Shell** in the terminal using the command `mongo` and created a database with a read-only user.

```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```



