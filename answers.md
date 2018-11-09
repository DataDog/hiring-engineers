# Application as 'Biblical Sales Engineer' at Datadog


 ...I'm sorry, but Senior is no longer the right element within a job title for me!! :trollface:


## So, who the hack is 'The Logfather'

This nickname was given to me by former colleagues at Splunk. Although my focus goes far beyond simple log files, I still carry this name with a certain pride.

I am now biblically 54 years old and have been working for almost 20 years as presales in various companies, but ALWAYS for start-up companies.
Where, if not in such young, agile and open companies, does the own acting and thinking have so much positive influence on the prosperity, the growth and the coming events of ingenious ideas, products and companies.

Before I started in the IT industry, I worked as a roofer, plumber, steel constructor and a lot more.
I also worked as a full-time paramedic for almost ten years.
I gained a foothold in IT about twenty years ago after training as a Java programmer.
However, I am not the code nerd who loves to sit between undefinable amounts of cold pizza boxes and let his genius run free to create incredibly good lines of code.
I'm rather the type of nerd who loves to successfully bring the ingenious ideas of others to the table. For me there is nothing more pleasing than to see how a great idea first becomes a convincing product, and in the next step a brilliant business idea becomes a successful company for everyone involved.

[So let's get started!](https://www.youtube.com/watch?v=IKqV7DB8Iwg)


### And the Oscar goes to....
![And the Oscar goes to....](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_oscar_goes_to.jpeg)

My thanks go to _**Lee Farrar**_ and Datadog for their interest in me and for giving me the opportunity to apply as a Sales Engineer.

## Following now all my answers. 

For everyone's information, the cloud also contains another, very individual version of the answers: https://spark.adobe.com/page/DtglP7uGh51BG/


### Starting with Datadog - Setup the environment


First things first I created a new user account on https://www.datadoghq.com/.

![datadog_account.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_account.png)

From there on I decided to download and run a standalone agent on my macos system, instead of using a VM or Docker approach.   

![datadog_account.png](https://github.com/simuvid/hiring-engineers/blob/master/images/datadog_install_1.png)   

Instead of downloading and running a DMG file on MAC you can simply download and start the installation of the agent buy the use of a simple command line in your terminal:

DD_API_KEY=719d714d7132af72ce6e1f2d8b67b618 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"
