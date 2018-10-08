

init_config:

instances:
  - server: 127.0.0.1
    user: datadog #The user we created in the database earlier
    pass: '<YOUR_CHOSEN_PASSWORD>' 
    port: 3306 #Default MySQL port
    options:
        replication: 0
        galera_cluster: 1
        extra_status_metrics: true
        extra_innodb_metrics: true
        extra_performance_metrics: false 
        schema_size_metrics: false
        disable_innodb_metrics: false