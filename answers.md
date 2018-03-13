## Prerequisites - Setup the environment

This exercise uses [Docker](https://www.docker.com/) containers to allow you to run the code on any modern operating system. A container is a lightweight, stand-alone, executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings. Available for both Linux and Windows based apps, containerized software will always run the same, regardless of the environment.<sup id="a1">[1](#f1)</sup>

[Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. The [docker-compose.yaml](docker-compose.yaml) file in this repo contains all the instructions and configuration for you to be able to see the results of the exercises, with one convenient command.

To see these results, in addition to [Docker for your platform](https://store.docker.com/search?type=edition&offering=community), you'll need a [DataDog account](https://app.datadoghq.com/signup). After creating credentials and answering a short questionnaire about your stack, you'll be brought to the Agent Setup screen. On this screen you won't need to download an agent, but you will need your personal API key. You should keep this key secret - if you need to revoke it due to accidental disclosure, there are [instructions for doing so](https://help.datadoghq.com/hc/en-us/articles/210267806-How-do-I-reset-my-Datadog-API-keys-).

![API key screenshot](./images/api_key.png)

These exercises require that your API key is available as a environment variable. The easiest way to do this is to add it to your `~/.bash_profile`:

```
echo 'export DD_API_KEY=0123456789abcdef' >> ~/.bash_profile
source ~/.bash_profile
```

This will ensure it will persist across system restarts.

Now you're ready to get the agent reporting metrics from your local machine! Simply run `docker-compose up`. Docker will download the Dockerized agent from DataDog and launch it. Once it launches, the Agent Setup screen will automatically update notifying you that the agent is reporting and you can continue to the next step

![API key screenshot](./images/agent_reporting.png)



## Footnotes

<sup id="a1">[1](#f1)</sup> https://www.docker.com/what-container [↩](#a1)
