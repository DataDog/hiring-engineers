# DataDog Solutions Engineer Exercise
Datadog is a cloud monitoring service for different applications. They can analyze and monitor servers, containers, container managements services, datadabases or if they don't have the integration you can make it :)

If you want more information or want to see it in action log in for their trial at [Datadog](https://datadoghq.com)

## Environment
- I created a droplet in [DigitalOcean](https://m.do.co/c/a4c588c90cf4), you can use the referral code if you want to test it out.
- You can simply start an Ubuntu 16.04 or any version of Ubuntu with a simply click.
- Install the agent 
```bash 
DD_API_KEY=$YOUR_API_KEY_HERE bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
- You will get a confirmation that its running and how to start / stop it. If you want more set of commands for the latest agent you can go to [Agent Usage](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/)
- All the configuration of the agent can be found
```bash
/etc/datadog-agent/datadog.yaml
```

## Collecting Metrics:
### Tagging
> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Based on the [Tagging Documentation](https://docs.datadoghq.com/getting_started/tagging/) we created the following tags
```bash
tags:
   - ddse
   - env:dev
   - role:app
   - hosted:digitalocean
   - region:us_east
```
You can see the tags on the Host in the following screenshot
![cli_tags](/images/cli_tags.png)
