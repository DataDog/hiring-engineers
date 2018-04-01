Your answers to the questions go here.



1) Can you change the collection interval without modifying the Python check file you created?

- The Python file itself doesn't need to be modified but to change the interval of the check, the user needs to modify the yaml config file associated with the Python check file. This is the file whose parent folder shares the same name as the Python check. The user can specify a [ min_collection_interval ] parameter that modifies the interval at which the check will be performed.