Your answers to the questions go here.

## Getting Metrics:
1. Image: ![image](https://user-images.githubusercontent.com/96433227/146793385-14a81adb-dd83-4e8a-b7a7-a50969077dd5.png)

   yaml file: ![image](https://user-images.githubusercontent.com/96433227/147419214-599259ad-44e3-439a-b94a-108b10dea0b1.png)
   
   Datadog Agent Manager: ![image](https://user-images.githubusercontent.com/96433227/147419191-8eec02d8-916d-4b71-81e8-93b5f3b40ac6.png)
   
2. MongoDB Installed: ![image](https://user-images.githubusercontent.com/96433227/146794365-5a45d99d-86c3-40c0-9239-4faf04831771.png)

3. Random Number Generator:

code: ![image](https://user-images.githubusercontent.com/96433227/146829641-2408964f-0f0c-4c7c-9372-729c2bf50086.png)

graph: ![image](https://user-images.githubusercontent.com/96433227/146827897-3d3ef2a3-5133-4b94-ac8e-c0a0f038ce40.png)

4. Collection Interval:

code: ![image](https://user-images.githubusercontent.com/96433227/147419248-cd13a4c5-a344-4d6a-bcf0-182b70f9b897.png)

graph: ![image](https://user-images.githubusercontent.com/96433227/146829130-c4684b45-f4fb-455c-89db-1f874195589d.png)

## Visualizing Data:
1. Snapshot to myself: ![image](https://user-images.githubusercontent.com/96433227/147123303-44c50a09-2b0d-43d5-936f-76693ca0cef3.png)

Dashboard: ![image](https://user-images.githubusercontent.com/96433227/147418879-5e79026c-8b8e-4af0-ae45-62ab78adf7a9.png)

Link to Dashboard: https://p.datadoghq.com/sb/65ff405c-6109-11ec-aeaa-da7ad0900002-cee234a0119938c9fc6746661b709e91

***Note: I couldn't get the data from my MongoDB to send to Datadog. I tried to configure the mongo.d/conf.yaml file to create a custom query but couldn't get that to send either so I moved on to the next part.***

_Bonus:_ If there was an anomaly graph, it would use the stats it collected to show the data that is 2 deviations outside the standard norm. 

Code used: [Postman_API_Timeboard_code.txt](https://github.com/bridget-harrod/hiring-engineers/files/7763969/Postman_API_Timeboard_code.txt)

## Monitoring Data:
1. Email alert:![image](https://user-images.githubusercontent.com/96433227/147295622-e3acebdb-2a53-41cc-926c-52b56226063a.png)

JSON file: [Presents_over_800_monitor.txt](https://github.com/bridget-harrod/hiring-engineers/files/7771582/Presents_over_800_monitor.txt)

_Bonus:_ M-F downtime scheduled:![image](https://user-images.githubusercontent.com/96433227/147295254-edee775a-eb97-4621-b608-cfd700ec7cf1.png)

Sat,Sun downtime scheduled: ![image](https://user-images.githubusercontent.com/96433227/147295473-9a81a691-840a-4fa7-9f41-eaee49b698c8.png)

## Collecting APM Data
App Code: [datadog_app.txt](https://github.com/bridget-harrod/hiring-engineers/files/7777507/datadog_app.txt)

Dashboard: ![image](https://user-images.githubusercontent.com/96433227/147418945-9af5e0ae-c320-4c71-a7aa-f4e2c44ed124.png)

Link to Dashboard: https://p.datadoghq.com/sb/65ff405c-6109-11ec-aeaa-da7ad0900002-3f207689ffa835ab7a8d319d5b08ebb5

_Bonus:_ A service is a grouping of aspects of a microservice, such as endpoints, queries, or jobs. A resource is specified within a service and each resource is tied to it's own service.

## Final Question
I would use Datadog to monitor professional soccer players. Each soccer play in the English Premier League wears a monitor that collects heart rate as well as a few other aspects like distance run during each game. The heart rates of the players are analyzed to determine how in shape players are and how at risk they are for injury. This data can be crucial to expand into other sports like football and basketball to reduce the injuries of players and keep them healthy. 
