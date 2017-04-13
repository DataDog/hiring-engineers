**Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.**
> RMullins407


**Bonus question: In your own words, what is the Agent?**
> The agent is a service that independently runs on each VM or Container and relays performance metrics back to the DataDog webservice for user interaction

**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**


```{r, engine='sh', count_lines}
vagrant@precise64:~$ grep -m 1 tags: /etc/dd-agent/datadog.conf 
tags: RoyMullinsExercise, env:test, role:exercise
```

[Host Tags](hiring-engineers/HostTags.PNG)




