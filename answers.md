# Monitoring an EKS cluster and deployed applications with DataDog

This document will guide you through the process of using Datadog to monitor an EKS Cluster and a sample Python application.
We will use Terraform to deploy the AWS EKS Cluster with the Datadog Agent installation included in the automation. 
After having the cluster properly setup and working and ensuring the Datadog agents are operating correctly, we will also go through the creation of a sample Python application deployment in the cluster and monitor the applications performance using Datadog APM(Application Performance Monitoring).


## AWS EKS Cluster creation with Datadog Agent installation

In this section we will go through the process of creating the AWS EKS Cluster using Terraform.
For this task we assume the user already has a properly configured aws working environment([aws cli installed](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) with an Access Key and Secret Access Key), we also assume the required binaries are installed in the environment([kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), [terraform](https://www.terraform.io/downloads.html)).

The terraform automation will handle the EKS cluster creation as well as the deployment of the [Datadog Daemonset](https://docs.datadoghq.com/agent/cluster_agent/setup/?tab=secret#configure-the-datadog-agent).
The [Datadog Daemonset manifest](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/cluster/kubernetes/dd-daemonset.yaml) has all the required components such as the RBAC components as well as the Daemonset itself.

### Terraform execution

To be able to execute the automation, we need to download the [source code folder](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/cluster).
Once the download completes, we can edit the local copy of the [terraform.tfvars](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/cluster/terraform.tfvars) file and update the variables according to our environment, as well as updating the "DD_API_KEY" environment variable in the [Datadog Daemonset](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/cluster/kubernetes/dd-daemonset.yaml).
After updating the variables to match our environment, we can move on to the actual execution of terraform.

#### Terraform init
Ensuring we are in the "cluster" folder we can initialize terraform by running the command bellow

```bash
terraform init
```

If the command executed successfully, we should see an output similar to the one bellow

![Terraform init](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/tf-init.png)

#### Terraform plan
We can now move to the planning stage
```bash
terraform plan
```

If the command executed successfully, we should see in the output 10 resources to add

![Terraform plan](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/tf-plan.png)

#### Terraform apply
Now that the planning stage completed, we can move to the apply stage, worth noting that the EKS cluster creation can take up to 15mins so just please just be patient until the execution finishes

```bash
terraform apply -auto-approve
```

If the command executed successfully, we should see an output similar to the one bellow

![Terraform apply](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/tf-apply.png)

#### Resource creation validation
Now that the Terraform execution completed and we have our infra-structure created, we need to ensure the cluster is working properly and that the Datadog agents are reporting correctly.

Checking that the cluster is operating properly can be done by executing the following command

```bash
kubectl get all --all-namespaces
```

Assuming everything is working as expected we should see an output similar to this

![kubectl get all --all-namespaces](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/eks-get.png)

We can see in the image above that we have 2 "datadog-agent" pods running(1 for each worker node).


#### Datadog agent reporting
If we have a look at the [Datadog HostMap page](https://app.datadoghq.eu/infrastructure/map) we can see that the agents are reporting and we can see the tags we defined in the Daemonset manifest are present.
 ![HostMap Agents](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/ddog-hostmap.png)


## Deploying a sample application
Now that we have the infrastructure created and being monitored by Datadog, we can deploy our application in the cluster.
In this case we will be using a [sample web application](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/myapp/webapp/datadog.py) based in Python.
Along with the sample application we will also deploy a [custom Datadog Agent metric](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/myapp/mymetric/my-metric.py) that in this example will be sending a random number between 1-999 as a [Gauge Metric](https://docs.datadoghq.com/developers/metrics/dogstatsd_metrics_submission/?tab=python#gauge) leveraging [DogstatsD](https://docs.datadoghq.com/developers/dogstatsd/?tab=python), a Datadog customized StatsD implementation.

In order to deploy our application we will use a Kubernetes Deployment and two custom built Docker Images.

### Building the docker images to use
In this section we will go through the process of creating the two container images required.
We will use a Dockerfile to create the required container images and push these images to a private Docker Registry.

#### Building the custom metric image
To build the custom metrics image we use this [Dockerfile](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/myapp/mymetric/Dockerfile).
We can build the image moving into the myapp/my-metrics folder and running

```bash
docker build . -t mymetric 
```

The output of this command should be similar to this
![mymetric docker build](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/mymetric-dockerbuild.png)

Now we need to tag and push the image to the remote registry where we will be storing the image.
To do so we can run the below commands replacing the remote registry shown by a valid registry

```bash
docker tag mymetric remote-registry.registrydomain.com/mymetric:v.01
docker push remote-registry.registrydomain.com/mymetric:v.01
```

An output similar to this should result signalling that the image was correctly uploaded to the remote registry
![mymetric docker push](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/mymetric-dockerpush.png)

#### Building the webapp image
To build the webapp image we use this [Dockerfile](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/myapp/webapp/Dockerfile) but because we want to have a more detailed view of our application, we will instrument our app to use Datadog APM(application performance monitoring).
We can see in the webapp dockerfile that instead of simply using the python binary to call our application like in the my-metric file, in this case, we call the Datadog tracing library [ddtrace-run](https://github.com/DataDog/dd-trace-py) before calling the python binary, which ensures that all the trace details generated by our application will be sent to the APM aggregator running on the Datadog Agents.
![webapp apm](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/webapp-dockerfile-apm.png)


As in the previous case, we need to ensure we are in the myapp/webapp folder and we can build the image by running
```bash
docker build . -t webapp 
```

The output of this command should be similar to this
![webapp docker build](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/webapp-dockerbuild.png)

Once again, we need to tag and push the image to the remote registry where we will be storing the image.

```bash
docker tag webapp remote-registry.registrydomain.com/webapp:v.01
docker push remote-registry.registrydomain.com/webapp:v.01
```

And once again, an output similar to this should result signalling that the image was correctly uploaded to the remote registry
![webapp docker push](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/webapp-dockerpush.png)


### Deploying our sample application
Now that we have both container images stored in a remote registry, we can deploy our application to our EKS cluster.
To do so we will use this [deployment manifest](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/cluster/kubernetes/myapp.yaml).
Before being able to deploy the sample application we need to update the deployment manifest with the proper container images.

![deployment images](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/deployment-images.png)

We also need to ensure our Deployment manifest has the environment variable required to enable the Datadog APM to properly send the trace data to the Datadog agents running in each node of the cluster and to so we use the "DD_AGENT_HOST" environment variable.

![webapp apm env var](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/webapp-apm.png)

We can also change the default custom metric reporting interval by changing the "interval" environment variable(in this case we are setting it to a 45 seconds interval).  

![mymetric interval env var](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/mymetric-interval.png)

Once we have reviewed the manifest and are happy with it we can run the following command to deploy our application
```bash
kubectl apply -f kubernetes/myapp.yaml
```

We can confirm that our application is running as expected by running the following command
```bash
kubectl get deployments
```

We should see an output similar to the one below which will our application running as expected
![kubectl get deployments myapp](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/myapp-getdep.png)

## Timeboards Monitors and Downtimes
Now that we have our application deployed in our cluster we can focus on creating [Timeboards](https://docs.datadoghq.com/dashboards/timeboards/) so we can aggregate and filter data as we please, [Monitors](https://docs.datadoghq.com/monitors/) so we can get notifications in case of any abnormality in our infra-structure and [Downtimes](https://docs.datadoghq.com/monitors/downtimes/) so we can suppress notifications during non-business hours.
We will use once again terraform to automate the creation of a custom Timeboard, a Monitor and two Downtimes(weekdays and weekends).

### Terraform execution
Similarly to what we did in the initial section, to be able to execute the automation, we need to download the [source code folder](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/boards).
Once the download completes, we can edit the local copy of the [terraform.tfvars](https://github.com/affoliveira/hiring-engineers/tree/solutions-engineer/boards/terraform.tfvars) file and update the variables according to our environment.
After updating the variables to match our environment, we can move on to the actual execution of terraform.


As we already followed the terraform deployment process, we will not focus on each step at this stage but rather perform the deployment using the commands bellow

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

Once the execution completes we should see a total of 4 resources being created and at this stage we can navigate to the [Dashboard List](https://app.datadoghq.eu/dashboard/lists) where our newly created Timeboard should be visible


![Dashboard](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/dashboard.png)


As well as navigate to our [Monitor list](https://app.datadoghq.eu/monitors/manage) where our new Monitor can also be viewed
![Monitor](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/monitor.png)

### Analyzing Data using our Timeboard
If we look at the Timeboard created, we will be able to see our custom metric scoped over our 2 EKS worker nodes.
We will also be able to see our custom metric with the rollup function applied to sum up all the points for the past hour.
And, because we have a DynamoDB to support our webapp(deployment not covered in this document) we also have a graph of the table items with the **anomaly function applied which allows DataDog to algorithmically identify a metric that is behaving differently than it has in the past**.
In our case, because the DynamoDB table is new, Datadog doesn't have enough historic information to provide any data.
![Timeboard](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/timeboard.png)

### Analyzing our Monitor
The monitor we created was once again based on the my_metric custom metric we created in the previous step.
With this monitor we are creating alerts when:

    Warning threshold of 500
    Alerting threshold of 800
    And also ensure that it will notify you if there is No Data for this query over the past 10m.


![Monitor specs](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/monitor-definition.png)

We have configured the monitor to send a notification message with a specific message for each of the thresholds above which includes both the host where the metric as caused an alarm and the value of the metric that caused the alarm.
As we can see in the email message bellow
![Monitor email](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/monitor-message.png)

Now, because this is not a critical system and we don't want to be notified outside of our working ours, which is why we have also created a couple of Downtimes, one for weekends and another for weekdays
![Downtime](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/downtime.png)

## Using Datadog APM
Now that we have our Timeboard our Monitor and Downtimes configured, we can start having a look at Application specific data.
As we configured our EKS Cluster Datadog agents to support APM and we instrumented our webapp application to send all the trace information to Datadog, we can now have a detailed look at our application performance details.

If we navigate to the [APM section](https://app.datadoghq.eu/apm/services) we will have a global view of all our [Services](https://docs.datadoghq.com/tracing/visualization/service/).
**A Service is a set of processes that do the same job**, in our case, the flask process running on our pods is our Service
![Service](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/service.png)

Once we select the "flask" service we will see a detailed view of data related to our webapp, such as "Total Requests", "Total Errors", "Latency".
This information is available because Datadog provides [Out of the Box](https://docs.datadoghq.com/tracing/visualization/service/#out-of-the-box-graphs) a set of graphs for any service.

As we scroll down on this dashboard, we will see our Service [Resources](https://docs.datadoghq.com/tracing/visualization/resource/).
**Resources are particular actions or endpoints for a given Service**, in our flask webapp case, our Resources are the endpoints we have configured
![Resources](https://github.com/affoliveira/hiring-engineers/blob/solutions-engineer/images/resources.png)



Now that we have an infra-structure and an application being monitored by Datadog what else could we do with Datadog?
I live in Dublin and currently the vast majority of domestic electricity meters are "dumb" devices but ESB(the electric infra-structure provider for Ireland) is starting to roll out new "Smart" devices.
We could use Datadog to monitor these new smart devices and provide aggregated information in case of power outages to help pin point the source of the power outage based on all the devices affected.