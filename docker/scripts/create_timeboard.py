import os, sys
from datadog import initialize, api


def create_timeboard():
    options = {
        'api_key': os.environ['API_KEY'],
        'app_key': os.environ['APP_KEY']
    }

    initialize(**options)

    title = "My Timeboard"
    description = "A Timeboard we created using the Datadog API"
    graphs = [{
         "definition":{
            "requests":[
               {
                  "q":"avg:my_metric{$host}",
                  "type":"line"
               },
               {
                  "q":"avg:my_metric{$host}.rollup(sum, 60)",
                  "type":"line"
               },
               {
                  "q":"anomalies(avg:mysql.net.max_connections{$host}, 'basic', 2)",
                  "type":"line"
               }
            ],
            "viz":"timeseries"
         },
         "title":"my_metric, mysql.net.max_connections"
    }]

    template_variables = [{
        "name": "host",
        "prefix": "host",
        "default": "host:ts-lab-docker"
    }]

    read_only = False

    result = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
    return result

if __name__ == "__main__":
    if "API_KEY" not in os.environ:
        print("API_KEY is not defined in .env")
        sys.exit(1)
    if "APP_KEY" not in os.environ:
        print("APP_KEY is not defined in .env.")
        sys.exit(1)

    result = create_timeboard()
    if "errors" in result:
        print("API error occurred: {}".format(result["errors"]))
        sys.exit(1)

    print("Your timeboard '{0}' was created: https://app.datadoghq.com{1}".format(result["dash"]["title"], result["url"]))
