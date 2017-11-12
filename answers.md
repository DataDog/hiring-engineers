Datadog Solutions Engineer Challenge
Owen Cummings

Q: Collecting Metrics

Added tags in the Agent and recieved the tags from Host Map as below.
![My image](https://github.com/owencummings/hiring-engineers/tree/Owen_Cummings_Solutions_Engineer/img/13.png?raw=true)
![My image](https://github.com/owencummings/hiring-engineers/tree/Owen_Cummings_Solutions_Engineer/img/14.png)


MongoDB was already installed on my machine, so I ran this in the mongo shell to activate it on the host device. Notified of integration success the Datadog WebApp.
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/02.png)


Created the two following files at the required locations.
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/03.png)
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/04.png)



Q: Visualizing Data

I used the API .py file in this repository to generate the following dashboard. I could find no documentation on the anomaly function and I assume that it isn't working. I read something about using anomalies in monitors but decided not to pursue it since it seemed off-task. The MongoDB metric is there, it's just a low value.

![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/06.png)



Q: Monitoring Data

I set the following alert/downtime conditions and recieved the appropriate emails.

![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/07.png)
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/08.png)
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/09.png)
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/10.png)
![My image](https://github.com/owencummings/hiring-engineers/blob/Owen_Cummings_Solutions_Engineer/img/11.png)




Q: Collecting APM Data

<Filling in ASAP>



Sources:
I mostly referenced the following documentation.

http://pypi.datadoghq.com/trace/docs/#
https://docs.datadoghq.com/guides/monitors/
https://docs.datadoghq.com/guides/tagging/
https://docs.datadoghq.com/guides/agent_checks/
https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time
