Level 1/

Thank you for choosing Datadog!

To start your journey with us, please sign up for free here https://www.datadoghq.com/pricing/ .

At the end of the sign up process, you'll be given your API key, a 32 characters long hexadecimal string. Please record it, we'll need it later.

Then, you'll need to install the agent. The agent is a piece of software running on your machine that is here to collect events and metrics from 
your machine or other elements in your infrastructure. For more information about the agent, please visit http://docs.datadoghq.com/guides/basic_agent_usage/ .

You can download the agent for your operating system here https://app.datadoghq.com/account/settings#agent

On a Linux machine you can simply run the following command :

```
#DD_API_KEY=your_api_key_goes_here bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

To check that is is started run the following command : 

```
#/etc/init.d/datadog-agent status
Datadog Agent (supervisor) is running all child processes
```

If you're running a modern version of Windows you can use this oneliner from an elevated powershell session :

```
Invoke-WebRequest -Uri https://s3.amazonaws.com/ddagent-windows-stable/ddagent-cli.msi -OutFile ddagent-cli.msi | msiexec.exe /qn /i ddagent-cli.msi APIKEY="your_api_key_goes_here"
```

To check that it is started run the following command :

```
get-service -Name DatadogAgent

Status   Name               DisplayName
------   ----               -----------
Running  DatadogAgent       Datadog Agent
```

Now let's take a look at the Event Stream. 
The Event Stream allows you to browse what happened in your infrastructure and looks like a timeline. It also works similar to a blog : you can post events to it, comment events or search for events using different criteria.
To look at your event stream, visit this page https://app.datadoghq.com/event/stream

We'll try to create an event programmatically using Datadog's REST API. You can find the API documentation here http://docs.datadoghq.com/api/ .

If you are running Windows, take a look at the Powershell code in New-DataDogEvent.ps1, then in a Powershell session run :

```
. .\New-DatadogEvent.ps1
New-DataDogEvent -title "Apache seems down" -text "Looks like it's using all the memory!" -ApiKey "your_api_key_goes_here"
```


You should get a response with Status Code 200 and you should see the event on your Stream.

If you are on Linux, pasting this into your prompt should give you the same result : 

```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Apache seems down",
      "text": "Looks like it's using all the memory!",
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=your_api_key_goes_here'
```

Did you know that Datadog has a notification system built into the Event Stream? Try to enter the  following in the 'text' statement of your request :
"@your@email.domain message" 
where "your@email.domain" is the email you have signed in with and "message" is the content of your message.
You can look at the file capture-api-email.PNG to see what the email looks like. 
You can find out more about the @ notifications here http://docs.datadoghq.com/faq/
 





