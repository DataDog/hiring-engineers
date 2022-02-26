# Datadog Technical Exercise Sale Engineering position
 by Jeff Hollis 2021
## Answers
Vargrant VM method. Quick install

<img width="615" alt="installing the agent Ubuntu" src="https://user-images.githubusercontent.com/87458325/155767763-6e1b9c40-2c60-4275-8f30-c673ac595a9a.PNG">

# Prerequisites - Setup the environment 

<img width="943" alt="Agent capture to API" src="https://user-images.githubusercontent.com/87458325/155801376-491cd4a9-1dcd-43f5-9528-662dacbb0447.PNG">

# Collecting Metrics

## Adding Tags

<img width="602" alt="Adding Tags" src="https://user-images.githubusercontent.com/87458325/155813006-c8193297-8abb-4745-a38d-0ae3467e20ec.PNG">

<img width="869" alt="Host map capture" src="https://user-images.githubusercontent.com/87458325/155813310-c3098ae4-dd6f-4537-9c60-2200e8970bfd.PNG">


After adding tags be sure to do a $ sudo service datadog-agent restart to apply YAML file changes.

## Installing MYSQL
sudo apt ugrade & sudo apt update
sudo apt install mysql-server
https://docs.datadoghq.com/database_monitoring/setup_mysql/selfhosted/?tab=mysql80

<img width="471" alt="Creating Datadog user and grant basic permissions" src="https://user-images.githubusercontent.com/87458325/155818635-d4541565-801c-4b46-bcb5-ed8699446bbb.PNG">

## Verify successful user creation
<img width="644" alt="verifying successful creation" src="https://user-images.githubusercontent.com/87458325/155819308-74819e2e-0a52-4cd7-8583-1d24628bc156.PNG">

## Metric Collection conf.yaml configuration

<img width="764" alt="Metric collection mysql" src="https://user-images.githubusercontent.com/87458325/155821022-e50657d1-5797-421f-b0bc-1150b645284b.PNG">



