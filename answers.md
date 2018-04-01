Your answers to the questions go here.



1) Can you change the collection interval without modifying the Python check file you created?

- The Python file itself doesn't need to be modified but to change the interval of the check, the user needs to modify the yaml config file associated with the Python check file. This is the file whose parent folder shares the same name as the Python check. The user can specify a [ min_collection_interval ] parameter that modifies the interval at which the check will be performed.


2) What is the Anomaly graph displaying?

- The anomaly graph is displaying the number of connections to the postgresl database on my machine and comparing this to the number of connections it expects to see based on past usage. Since I started out with a single persistent connection under my default username, the anomaly graph is expecting to see just one connection. When an anomaly occurs, such as when I connect to the database with a second account, the new value is marked in red on the graph (see screenshots snapshotAnomaly.png and snapshotAnomaly2).