Your answers to the questions go here.

(Please see README_ddtest.pdf for additional explanations about my thought process throughout this challenge.)

1) Can you change the collection interval without modifying the Python check file you created?

- The Python file itself doesn't need to be modified but to change the interval of the check, the user needs to modify the yaml config file associated with the Python check file. This is the file whose parent folder shares the same name as the Python check. The user can specify a [ min_collection_interval ] parameter that modifies the interval at which the check will be performed.


2) What is the Anomaly graph displaying?

- The anomaly graph is displaying the number of connections to the PostgreSQL database on my machine and comparing this to the number of connections it expects to see based on past usage. Since I started out with a single persistent connection under my default username, the anomaly graph is expecting to see just one connection. When an anomaly occurs, such as when I connect to the database with a second account, the new value is marked in red on the graph (see screenshots snapshotAnomaly.png and snapshotAnomaly2).  Link to Dashboard: https://app.datadoghq.com/dash/750319/my-metric?live=true&page=0&is_auto=false&from_ts=1522674501584&to_ts=1522678101584&tile_size=m


3) What is the difference between a Service and a Resource?

- A Service is a set of processes that work together to perform a particular job or function such as the Flask web app that I implemented for this challenge. A Resource is a query or other action performed on a Service such as the http requests I sent to my app whenever I accessed one of its three pages.


4) Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
   Is there anything creative you would use Datadog for?

- As someone who has become increasingly more concerned about my impact on the environment over the past few years, I have made efforts to reduce wasteful consumption of products in my house. This is easy enough to do when it comes to counting the number of trash bags I've thrown out over the last month or the number of paper towel rolls I've bought on my last few trips to the store but it's not so easy to get a good idea of how much water and electricity I'm using (at least, not until the utilities bill arrives). In a connected home, Datadog would be very helpful in identifying my usage patterns for water and electricity in a way that wouldn't be possible otherwise. Looking at a monthly bill is one thing but even the most meticulously itemized bill won't tell me at what hours my utility usage is spiking and that information would be invaluable for learning what specific activities are becoming excessive. Is my huge water bill due to long showers or is that dish washer not as efficient as advertized? Is my video-gaming habit responsible for the heart attack I nearly had when I saw what I owed the electric company or is the culprit really the host of old appliances that I still haven't gotten around to replacing? Datadog's analytical capabilities and alerts would give me the kind of granular analysis that I need to answer these kinds of questions.