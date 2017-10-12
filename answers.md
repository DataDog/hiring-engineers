[Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&app=randomcheck&host=350540781)

<img src="Host map and tags.png">

[Random Check Dashboard](https://app.datadoghq.com/dash/integration/custom%3Arandomcheck?live=true&tpl_var_scope=host%3AMinas-Air&page=0&is_auto=false&from_ts=1507832536172&to_ts=1507836136172&tile_size=m)

<img src="Graph showing data above 0.9.png">

[Random Check Dashboard Cloned](https://app.datadoghq.com/dash/378054/custom-metrics---randomcheck-cloned?live=true&page=0&is_auto=false&from_ts=1507832638706&to_ts=1507836238706&tile_size=m)

### Monitor email for when graph hit above 09:
<img src="Monitor email, graph hit above 0.9.png">

### Down time email:
<img src="Down time email.png">
Sidenote: my down time email was sent at a radnom time for testing purposes becuase it was past 7pm, and it is now set up to have the correct down time 7pm-9am.


### Bonus Question #1. In your own words, what is the Agent?

The Agent is software that runs on your hosts, it collects events and metrics and sends them to Datadog. Datadog then allows you to easily observe and use your monitoring and performance data.

The Agent is made up of three parts: 
1. Collector: runs checks on your machine for your integrations and captures system metrics
2. Dogstatsd: statsd backend server that recieves custom metrics from an application
3. Forwarder: sends data from dogstatsd and the collecter to datadog

### Bonus Question #2. What is the difference between a timeboard and a screenboard?

Timeboards or for troubleshooting, seeing correlations, and tirage investigations.  They help pinpoint what is happening across metrics and services at the same time.  All graphs are scoped to the same time, and will appear in a grid like fashion, these graphs can only be shared individually.

Screenboards show you general status boards with the overall helath.  Screen are more flexible and customizebale than timeboards and useful for getting a high-level look into a system. These can be customized with widgets, graphs (with different time frames!), images, and visual cues to make your data presentable in any way you like. Screenboards can be shared with a public url as a read-only entity.
