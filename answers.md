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

<img width="833" alt="Metric collection mysql" src="https://user-images.githubusercontent.com/87458325/155828798-530ecd4c-69e3-48f3-bf50-9a13ef407c9e.PNG">
<img width="824" alt="Metric collection mysql2" src="https://user-images.githubusercontent.com/87458325/155828804-cb220369-8af9-41c3-beb3-c3c7aabbd798.PNG">

sudo service datadog-agent restart

<img width="545" alt="installed MySQL" src="https://user-images.githubusercontent.com/87458325/155829597-af46b943-aa1a-494e-a55f-3886f4da3827.PNG">

## Creating a custom Agent check
sudo nano my_metric.yaml --- Content "instances: [{}]"

<img width="896" alt="conf d_yaml_my_metric" src="https://user-images.githubusercontent.com/87458325/155830523-f096ce1f-6f44-4094-a6fa-bd6743303635.PNG">

<img width="900" alt="check d_my_metric" src="https://user-images.githubusercontent.com/87458325/155831516-195af2b6-0a35-4fa6-9073-72f91fa88792.PNG">



