Your answers to the questions go here.

# Collecting Metrics:

#### - Added tags: hello:world, machine:ubuntu/xenial and env:test
#### - Please see image: question1.png


## Database Integration:

```bash
> sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
> echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
> sudo apt-get update
> sudo apt-get install -y mongodb-org
> sudo systemctl start mongod
> sudo systemctl status mongod

```
From DataDog dashboard: Click Integrations and select PostgreSQL
To collect database metrics, we need to create a user on PostgreSQL and grant access
