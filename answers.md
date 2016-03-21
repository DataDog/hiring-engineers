###Level 1
The agent is a process that runs on client's machines. It provides data three ways (that I've observed so far): some system information is passed automatically, and users can pass data to the agent through agent checks as well as by sending metrics to the dogstatsd server.

I used the dogapi npm library to submit an event in app.js, which I've included in the repo; a monitor I set up then alerted me by email.

###Level 2
[Level 2 Dashboard](https://p.datadoghq.com/sb/86dbdd770-e0fc217f38)
![Alt text](https://raw.githubusercontent.com/aMattBryan/hiring-engineers/support-engineer/level2.png)

###Level 3
[Level 3/4 Dashboard](https://p.datadoghq.com/sb/86dbdd770-8be5e0fc6e)
![Alt text](https://raw.githubusercontent.com/aMattBryan/hiring-engineers/support-engineer/level34.png)
I used the loadtest npm package to write the load tests; I included the app, loadtest.js in the repo. I also combined the level 3 and 4 dashboards as the data is more helpful on the same page.

###Level 4
[Level 3/4 Dashboard](https://p.datadoghq.com/sb/86dbdd770-8be5e0fc6e)
It looks like notable spikes in number of pageviews during the load test occur during periods of low latency, which makes sense; the less time it takes to complete a request, the more requests go through in a given span.

###Level 5
[Level 5 Dashboard](https://p.datadoghq.com/sb/86dbdd770-3e5d583d32)
![Alt text](https://raw.githubusercontent.com/aMattBryan/hiring-engineers/support-engineer/level5.png)
I've included my code for randcheck.py and randcheck.yaml in the repo