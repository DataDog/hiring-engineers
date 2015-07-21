Your answers to the questions go here.

######## LEVEL 1 ##########

  # "Sign up for Datadog, get the agent reporting metrics from your local machine."
    - Local metrics => Matthews-MacBook-Pro.local
      - screenshot => https://flic.kr/p/w2cDKb

  # "Bonus question: what is the agent?"
    - The agent is a lightweight piece of opensource software that is responsible for collecting events and metrics on behalf of the host user and delivering them to Datadog. Its arcitechture comprises four main components, each running as a seperate process. They are as follows: 

      - Collector - Checks the current machine for integrations and captures standard system metrics (i.e., CPU and/or memory usage) every fifteen seconds.
      - Dogstatsd - Aggregates local metics via code from the host. This is a StatD backend server implemented in Python.
      - Forwarder - Cues data pushed from both the Collector and Dogstatsd by listening for requests over HTTP. This cued data is buffered and forwarded to Datadog via HTTPS.
      - SupervisorD - This is the master process which essentially supervises the other three main components. 

  # "Submit an event via the API."
    - First things first... I set up an API key.
      - screenshot => https://flic.kr/p/wgw4pb
    - Next, I downloaded the dogapi ruby gem.
      - screenshot => https://flic.kr/p/wiSigX
    - Then I ran the dog-api.rb file I created and recieved a JSON event response.
      - screenshot => https://flic.kr/p/wgCcg1

  # "Get an event to appear in your email inbox (the email address you signed up for the account with)"
    - I added my email in the event message text section of the API request via a "@" notification.
      - screenshot => https://flic.kr/p/w2p3NS
    - The event notification email then arrived in my inbox.
      - screenshot => https://flic.kr/p/wj1Tpa


######## LEVEL 2 ###########

  # "Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics."


  # "While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!"


  # "Create a histogram to see the latency; also give us the link to the graph"


  # "Bonus points for putting together more creative dashboards."