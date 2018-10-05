# Collecting APM Data

Install and configure Application Performance Monitoring (APM) on the VM and a Flask App.

0. Install python-setuptools and pip:
    ```
    sudo apt-get install python-setuptools
    sudo easy_install pip
    ```

1. Install ddtrace and flask
    ```
    sudo pip install ddtrace
    sudo pip install flask
    ```

2. Create the /home/vagrant/app.py file:
    ```
    from flask import Flask
    import logging
    import sys
    
    # Have flask use stdout as the logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    c = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c.setFormatter(formatter)
    main_logger.addHandler(c)
    
    app = Flask(__name__)
    
    @app.route('/')
    def api_entry():
        return 'Entrypoint to the Application'
    
    @app.route('/api/apm')
    def apm_endpoint():
        return 'Getting APM Started'
    
    @app.route('/api/trace')
    def trace_endpoint():
        return 'Posting Traces'
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5050')
    ```
    Link to app [here]().
    
3. Modify run permission:
    ```
    chmod +x app.py 
    ```
4. Modify Vagrantfile to add config.vm.network settings
    ```
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-16.04"
      config.vm.network "forwarded_port", guest: 5050, host: 8080
    ```

5. Restart Vagrant:
    ```
    vagrant reload
    ``` 

6. Run the application using ddtrace:
    ```
    ddtrace-run python app.py
    ```

7. Call the API on the browser by entering any of the three:
    - http://localhost:8080/
    - http://localhost:8080/api/trace
    - http://localhost:8080/api/apm

### Dashboard with both APM and Infrastructure Metrics

![Alt text](../images/4_dashboard.png?raw=true "Dashboard with both APM and Infrastructure Metrics")

### Service versus Resource
A service is a set of processes that do the same job. For instance, a simple web application may consist of two services: A single webapp service and a single database service.

A Resource is a particular action for a service. For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks). For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

For more information, check the guide [here](https://docs.datadoghq.com/tracing/visualization/).