Setup the environment

I created an AWS Linux AMI in AWS and an Azure Windows 2012 vm for testing with Datadog.

![image](https://user-images.githubusercontent.com/38929107/39657790-25b649c2-4fc0-11e8-837d-a2265c0ac36f.png)
![image](https://user-images.githubusercontent.com/38929107/39770700-9e20318e-52a4-11e8-8be9-d07cb6a39845.png)

Installed Datadog agent on Windows Server 2012
![image](https://user-images.githubusercontent.com/38929107/39771125-ed5cf45c-52a5-11e8-8f50-97eb28d72717.png)
![image](https://user-images.githubusercontent.com/38929107/39771227-3c2c447a-52a6-11e8-9ae3-03598ecad026.png)

Installed Datadog agent on AWS Linux server
![image](https://user-images.githubusercontent.com/38929107/39771293-720673fe-52a6-11e8-95c8-604407471a98.png)
![image](https://user-images.githubusercontent.com/38929107/39771337-9ae0ddaa-52a6-11e8-8631-2760695378f4.png)

Installed MySQL on the AWS Linux server
![image](https://user-images.githubusercontent.com/38929107/39771367-be14136e-52a6-11e8-817a-4a5624250cb8.png)

Configured MySQL for Datadog
![image](https://user-images.githubusercontent.com/38929107/39771391-dfcb152a-52a6-11e8-9d8d-2f82bd99872e.png)

Configured MySQL integration in Datadog portal
![image](https://user-images.githubusercontent.com/38929107/39771423-011c395c-52a7-11e8-9e58-515ff0479549.png)

Also configured Azure integration in Datadog portal for the heck of it.
![image](https://user-images.githubusercontent.com/38929107/39771457-1e4ef064-52a7-11e8-909e-4a6fae09132d.png)

Added tags to both server’s agent config files (TAG=datadogtestvm)
Windows 2012 vm with TAG
![image](https://user-images.githubusercontent.com/38929107/39771494-43073d94-52a7-11e8-824e-b5c8050c81b3.png)

Linux vm with TAG
![image](https://user-images.githubusercontent.com/38929107/39771528-61c9b2b6-52a7-11e8-8012-c9893e59b626.png)

Screenshot of vm’s with TAG=datadogtestvm
![image](https://user-images.githubusercontent.com/38929107/39771559-7caeb9dc-52a7-11e8-9c77-23656e1fd5fa.png)

Created a custom Agent check that submits a metric named my_metric with a random value between 0-1000.
![image](https://user-images.githubusercontent.com/38929107/39772716-d11fe81c-52aa-11e8-9b0a-f43cf43819d9.png)

Change your check's collection interval so that it only submits the metric once every 45 seconds.
![image](https://user-images.githubusercontent.com/38929107/39772802-06ebc2cc-52ab-11e8-9374-fd9febf8e789.png)
