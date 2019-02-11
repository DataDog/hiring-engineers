Your answers to the questions go here.
Prerequisites - Setup the environment

I used a Windows Server with SQL Server and Python installed for the APM exercise. 

For the next step --->
"Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine."

I went to the datadoghq.com website and signed up for my own account following the instruction prompts. On the first login I followed the getting started instructions to install the agent. It is very easy to get the agent started as there is a one step install command for Windows.

<<Insert Image001>>>

In a very short time, the agent started reporting data:

<<<Insert Image002>>>

<<Insert Image004>>


Collecting Metrics:

    Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    I added host tags and users tags as shown in the screenshot:
    
    <<Insert Image005>>>
    
    Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    
    For SQL Server monitoring, I followed the steps outlined in the documentation:
https://docs.datadoghq.com/integrations/sqlserver/

<<Insert Image003>>> SQL YAML Config

    Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    Change your check's collection interval so that it only submits the metric once every 45 seconds.
    
    I created a my_metric check using documentation link:
    https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
    
    <<Insert Image 007>>>
    
    
    Bonus Question Can you change the collection interval without modifying the Python check file you created?
    
    It is possible to change the interval without modifyinh the .py file. 
    
    Yes, you can change it in the YAML
    
    <<Insert Image 008>>>
    
    Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

    Your custom metric scoped over your host.
    Any metric from the Integration on your Database with the anomaly function applied.
    Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

<<Insert API Timeboard.py>>> File

Once this is created, access the Dashboard from your Dashboard List in the UI:

    Set the Timeboard's timeframe to the past 5 minutes
    Using "ALT + ]" I zoomed to 5 min interval
    Take a snapshot of this graph and use the @ notation to send it to yourself.
    <<Insert 5 min @ snapshot>>
    Bonus Question: What is the Anomaly graph displaying?
    
    The part of the "Anomalies Sql Batch Requests" graph that are shown in RED are showing that for this metric the value is outside of normal. In this case the mathematical formula used ('1e-3', direction='above') for any spikes above the value of 1e-3 will be highlighted as outside of the normal.  It uses the history of the metric to predict the future values. If the value is outside of the expected range it will color it red on the graph.

