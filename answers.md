# Stig's answers

Hey Datadogs - my name is Stig and I've had he pleasure of going through your hiring exercice. 
These are my answers, screenshots and links - enjoy :)

## Pre-reqs
FYI - I chose to use my private MacBook. First of all because I was curious about what the agent is able to pull our of it. And secondly I was too lazy to set up the vagrant and virtualbox stuff to get my environment running. 
So - my private Mac is what you'll see. It is rather old as well, so this should be a great challenge :)

## Collecting metrics
I added 2 screenshots here. One is my Hostmap after installing the initial agent, postgres, the integration and adding the tags (agent and user). In the second one (no bonuspoints expected!) I played with the grouping. It doesn't make too much sense when only monitoring one host, but it adds some context to the map (which I like).
Not sure if you can access my Datadog user, but added the links as well (just in case)

![Alt text](screenshots/Stigs-Hostmap.png?raw=true "Hostmap")
[Stig's Hostmap](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false ".. hope it works!")

![Alt text](screenshots/Stigs-grouped-Hostmap.png?raw=true "Hostmap")
[Stig's grouped Hostmap](https://app.datadoghq.com/infrastructure/map?mapid=3556&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=role%2Cenv&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false ".. hope it works!")

And now to the custom check. I started off writing the hello.world check - just to check how things worked. Then I wrote the random_number check. Instead of writing a random number function or using something like randint, I chose to ask for it through a public API I have used in the past, which delivers the random number and additionally a fun fact about that number. Reason for it was that I wanted to test the events as well. To not clog the event list (although the aggregation string works well), I only send an event for numbers < 100.

I used the documented <i>min_collection_interval</i> to set the collection interval to 45 seconds. It doesn't seem to be 100% accurate though, I see the metrics mostly in 1 minute intervals in the metric explorer. I didn't find another way to do it though.

<b>Bonus question:</b> Is there another way to change the collection interval? I am really not sure, but my best guess is that it can changed globally in the agent configuration. It could probably be programmed as well (in the .py).

Attached code+config is [random_number.py](src/random_number.py) and [random_number.yaml](src/random_number.yaml).
