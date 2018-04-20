<b> For full answers, thoughts, screenshots from exercise please see Answers.docx</b>


<b>Changing collection interval and Bonus Question:</b>
The bonus question asked if there was a way to change the collection interval without modifying the Python check file. Which according to the latest documentation, https://docs.datadoghq.com/agent/agent_checks/, you are supposed to change the yaml file by adding in the min_collection_interval under the instance.

If I was to modify the python file I would add this line:

time.sleep(30) 

before my check call in the script, to add 30 seconds to the defaulted 15 seconds check time


<b>Bonus Question: What is the Anomaly graphing displaying?</b>
“If it ain’t broke, don’t fix it!” If you are only looking for what is broken, you will miss all other potential issues of your application. How do you know what broken is? Is it just when the application is down? What if it is running s….l…o…w… and causing issues for your customers? Anomaly detection will measure where values are in a normal range, and will alert you if they are suddenly outside the range. 
It is a lot like a golf swing, if you are always hitting your draw and then suddenly you hit a terrible slice, that is an anomaly. Your swing isn’t broken, because you still hit the golf bad, but it certainly wasn’t good. Now this is where analytics and metrics will come into play, maybe it was because your ball was below your feet, or maybe out of the sand, but you can determine the potential cause. This is the same thing that DataDog can do with the Anomaly detection and all the other metrics gathered, show you the reason behind something out of the ordinary.


<b>Bonus Question: What is the difference between a Service and a Resource?</b>
•	Resource is a single query or action to a service. For example a SQL query or a url call.

•	Service is a set of processes that are working together to provide a feature set. For example a webapp, a master-db, and a replica-db. In DataDog if we define a “Service” for these three processes it will help us quickly analyze issues between different processes.

<b>Final Question: What would I monitor with Datadog?</b> 
	Chick-fil-a close to my house with data related to when fresh fries are made and the length of the line. I would also monitor traffic data from my house to the said Chick-fil-a. Combining and analyzing this data I would find the optimal time to leave my house, be in line, order, and get the freshest fries possible!
