Your answers to the questions go here.



1) Can you change the collection interval without modifying the Python check file you created?

- The Python file itself doesn't need to be modified but to change the interval of the check, the user needs to modify the yaml config file associated with the Python check file. This is the file whose parent folder shares the same name as the Python check. The user can specify a [ min_collection_interval ] parameter that modifies the interval at which the check will be performed.


2) What is the Anomaly graph displaying?

- The anomaly graph is displaying the number of connections to the postgresl database on my machine and comparing this to the number of connections it expects to see based on past usage. Since I started out with a single persistent connection under my default username, the anomaly graph is expecting to see just one connection. When an anomaly occurs, such as when I connect to the database with a second account, the new value is marked in red on the graph (see screenshots snapshotAnomaly.png and snapshotAnomaly2).  Link to Dashboard: https://app.datadoghq.com/dash/750319/my-metric?live=true&page=0&is_auto=false&from_ts=1522674501584&to_ts=1522678101584&tile_size=m


3) What is the difference between a Service and a Resource?

- A Service is a set of processes that work together to perform a particular job or function such as a flask web app. A Resource is a query or other action performed on a Service (such as an http request).