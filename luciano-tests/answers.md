Sales Engineer – Exercise Answers
Following the questions on https://github.com/DataDog/hiring-engineers/
I did my own way over here...

-	Host: Centos 7 as a VM on Virtual Box
-	DD-agent installed using the single command for Centos
-	Apache HTTPD installed and hosting a simple App in JS Node. (Datadog integration enabled)
-	Tomcat also has been installed hosting a single HTML PAGE listening on port 8080 (Datadog  is monitoring as well)
-	Docker service has been installed and being monitored by Datadog integration as well.

Below the screenshots for each monitored service mentioned above:
 
![image](https://user-images.githubusercontent.com/44204746/130949784-facf6fe5-25b4-48bc-b073-442f22917aae.png)
Datadog agent installed and running

![image](https://user-images.githubusercontent.com/44204746/130949839-29b0d0e9-565c-4b5a-b8ef-a0a59acc789f.png)
Confirmed installation on Datadog GUI (Web Console)

![image](https://user-images.githubusercontent.com/44204746/130949865-005e7bac-f003-44a4-9795-51eaf0287777.png)

![image](https://user-images.githubusercontent.com/44204746/130949897-45c25483-2880-40cb-8812-021c641969bc.png)
TAG

APACHE HTTP has installed and hosting a web App on /var/www/html directory
![image](https://user-images.githubusercontent.com/44204746/130949920-ddf0d7af-de69-47f9-b83b-d219630f411f.png)


![image](https://user-images.githubusercontent.com/44204746/130949930-b485164a-8f6e-4738-ada8-db784f5529ae.png)


Datadog Apache metrics Enabled

![image](https://user-images.githubusercontent.com/44204746/130949945-7b053b13-4a3b-4d70-b124-dfee4d0b1f4b.png)


Tomcat metrics integration enabled

![image](https://user-images.githubusercontent.com/44204746/130949973-b0e6820e-e432-4967-966f-814bb179e327.png)


Tomcat.d/conf.yaml JVM enabled listening on port 8080

![image](https://user-images.githubusercontent.com/44204746/130950003-de532db1-42ff-4b86-9609-699cdba7665d.png)


Output of agent restart after tomcat integration enabled

![image](https://user-images.githubusercontent.com/44204746/130950029-3ac0093f-eb18-41b7-be1c-0eccb89b82d5.png)


Datadog web GUI console showing tomcat metrics results

![image](https://user-images.githubusercontent.com/44204746/130950052-181b4757-01e7-4e90-b3a6-49040053eb15.png)


![image](https://user-images.githubusercontent.com/44204746/130950061-00dbbfc3-f559-4b21-b8ae-799e03805e2a.png)


![image](https://user-images.githubusercontent.com/44204746/130950070-4b274eb1-2fc7-4ae2-9fc3-e3f78a297c7c.png)


Docker service running on host and Datadog integration enabled

![image](https://user-images.githubusercontent.com/44204746/130950099-9dd8fbe0-35d5-4f32-9264-e3e7d1c3ce89.png)


![image](https://user-images.githubusercontent.com/44204746/130950122-90f44354-4ce7-48ab-8cdd-62b2c1b297d5.png)


No containers have been created so far.


A monitor has been created to monitor the if datadog agent is running properly on the host


![image](https://user-images.githubusercontent.com/44204746/130950149-f219da6b-6727-41da-aab2-b2605fec5770.png)


Downtime has been set as well

![image](https://user-images.githubusercontent.com/44204746/130950170-1a67fa65-4409-4107-bba7-6c5cbb5513ee.png)


From here are my BLOCKERS
When I tried to install APM I have been blocked by an error

![image](https://user-images.githubusercontent.com/44204746/130950196-9561ad0d-f584-4de7-aeb5-d67f0369bddc.png)


![image](https://user-images.githubusercontent.com/44204746/130950209-54b7f332-b505-4846-a748-d7da6d1668e5.png)


The App is running OK, however, APM integration couldn’t be enabled so far... I am still working on it.
Public Dashboard also have been created
https://p.datadoghq.eu/sb/4b2083cc-fb92-11eb-8b64-da7ad0900005-f796e4562d9676c4cd91b75f4f07e957
MongoDB also have been installed, however, couldn’t enable mondoDB integration, after creation of the DB for Datado tests and user, the service could not be restarted again, still working on it.

PS. 
-	I have attached all my conf files and the app.
-	Services have been installed using the official documentation for Centos 7 using YUM repository
Glossary: 
https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7
https://www.digitalocean.com/community/tutorials/how-to-install-apache-tomcat-8-on-centos-7
https://docs.docker.com/engine/install/centos/
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/


 Nothing I did was enabling APM .
I have checked all those steps
https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/?tab=containers
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html
https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/?tab=containers#configure-the-datadog-agent-for-apm

Restarted the agent nothing.
Even tried AWS integration instead my local VM on VirtualBox.

Is there anything else I could try? I have searched Youtube videos as well.

I believe is something with my application side.

EXTRA integration with AWS
AWS Integration Success

![image](https://user-images.githubusercontent.com/44204746/130950324-7f7052ff-b588-4c6b-b951-6cf5da317f32.png)

