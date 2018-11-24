### Installation

Vagrant is a powerful vm orchestrator but I have already in my personal notebook an Ubuntu vm image with Docker. I'm using VirtualBox. I will then install the dockerized version of mongodb and datadog agent:

```shell
sudo docker run --name mongodb \
-e MONGO_INITDB_ROOT_USERNAME=lionh \
-e MONGO_INITDB_ROOT_PASSWORD=******** \
-p 27017 \
-d mongo:latest
```

```shell
sudo docker run -d --name dd-agent \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v /proc/:/host/proc/:ro \
-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
-v /opt/datadog-agent-conf.d:/conf.d:ro \
-v /opt/datadog-agent-checks.d:/checks.d \
-p 8125:8125 \
-p 8126:8126 \
-p 5002:5002 \
--link mongodb:mongodb \
-e DD_TAGS=host:lionh-vm\ availability-zone:eu-west-a1\ region:west \
-e DD_API_KEY=44777b5614adfe98cfc78886cbea1eba datadog/agent:latest
```
The run command allow us to share volume between the docker container and the docker host to persist our file configuration. I also made a linkage with the mongodb container and added some custom tags.

![alt-text](pictures/001%20-%20docker%20run.png "Running the agent")

It's necessary to add a user in mongodb to allow the datadog agent to access in ro to the database metrics:

```shell
creating user datadog in mongo:
db.createUser({
... "user":"datadog",
... "pwd": "********",
... "roles" : [
... {role: 'read', db: 'admin'},
... {role: 'clusterMonitor', db: 'admin'},
... {role: 'read', db: 'local' }
... ]
... })
Successfully added user: {
	"user" : "datadog",
	"roles" : [
		{
			"role" : "read",
			"db" : "admin"
		},
		{
			"role" : "clusterMonitor",
			"db" : "admin"
		},
		{
			"role" : "read",
			"db" : "local"
		}
	]
}
```

Here a screenshot of my host in the Host Map page in Datadog:

![alt-text](pictures/Host%20Map.png "Screenshot of my host in the Host Map page")
