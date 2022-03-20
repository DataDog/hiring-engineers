Your answers to the questions go here.

1. Adding tags to Agent config file

![1Tags](https://user-images.githubusercontent.com/11410885/159150192-bc07f8c5-895b-428c-8161-5971f2634b6c.PNG)

2. Postgres database integration

![2DatabaseIntegration](https://user-images.githubusercontent.com/11410885/159150216-63d9c99a-06c5-4a0f-8cb8-fa7bbd43373b.PNG)

3. Custom agent check for my_metric

![3MyMetric](https://user-images.githubusercontent.com/11410885/159150222-2b144e6c-1cc7-4716-9c7a-6439d8ccb024.PNG)

4. Change check interval

![4ChangeInterval](https://user-images.githubusercontent.com/11410885/159150247-9cc2bc2a-ff15-4915-bdc3-f34258d9ca8b.PNG)

5. Collection interval without changing python file - I did this through the config yaml as shown on https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

![5NotChangingPythonFile](https://user-images.githubusercontent.com/11410885/159150295-512d4154-e820-4b82-b501-a8450524b223.PNG)

6, 7, 8 Combined answer - I created the dashoboard using the console and used the get API on that dashboard ID to see the JSON it generated. I used that JSON to create the bash script to programmatically create a new dashboard with the desired configuration.

- See 678DashboardScript.sh file

9, 10 Combined answer - Dashboard timeframe to past 5 minutes, take a snapshop and send it to myself

![910SnapshotAndAlert](https://user-images.githubusercontent.com/11410885/159150456-6e245c32-dd9f-4e36-ace9-81b4301b7f24.PNG)

11. Detects when a metric is outside of its usual pattern and trend based on previous trends such as day of week and time of day.

12, 13, 14 Combined answer

![12to14AlertConditions](https://user-images.githubusercontent.com/11410885/159150496-e8d6eece-fa95-45c5-9708-be489ef0038d.PNG)

15, 16, 17 Combined answer

![15to17AlertVariables](https://user-images.githubusercontent.com/11410885/159150500-e221a937-bddc-47d1-b944-37c2aff4af59.PNG)

18. Email alert

![18EmailAlert](https://user-images.githubusercontent.com/11410885/159150510-c5f77beb-d34d-464b-95f3-b6f3ad8f9be0.PNG)

19. Weekday silence

![19WeekdaySilence](https://user-images.githubusercontent.com/11410885/159150517-c0b1072b-c077-4cdc-805b-93c642436448.PNG)

20. Weekend silence

![20WeekendSilence](https://user-images.githubusercontent.com/11410885/159150521-c252ee39-5f54-45e8-8af8-5aadb7461ea9.PNG)

21. Weekday silence email, weekend silence email

![21WeekdaySilenceEmail](https://user-images.githubusercontent.com/11410885/159150535-3d941e74-be8b-456f-a532-3b3d6e4988f7.PNG)
![21WeekendSilenceEmail](https://user-images.githubusercontent.com/11410885/159150538-ccc9b0af-b741-4586-803f-760b49902c99.PNG)

22. APM Data - I used the same Flask app as given and used pip to install ddtrace. I started the application using the command generated from the APM console. I generated traces with curl commands.

Start command used - DD_SERVICE="sampleapp" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python3 sample.py
Example curl command - curl http://10.0.2.15:5050/api/trace

Public dashboard link - https://p.datadoghq.com/sb/c7c302b4-a77d-11ec-8ce8-da7ad0900002-27af1f1337e66483b569ed61cec38710

![22ApmData](https://user-images.githubusercontent.com/11410885/159150751-f2f34109-f3d5-4a2b-82e5-04e6e169ecb0.PNG)

23. Resources and services - Resources are associated with services and are typically individual endpints or queries. A service is a set of processes that do the same job.

24. Final question - I would see what datadog could do with agricultural IoT, such as arrays of sensors in a farm collecting data such as moisture, temperature, sunshine, rainfall, and soil data. This data could be used to establish local and wider trends for an area to maximize agricultural output. Live data could be used to detect issues and proactively respond to them.
