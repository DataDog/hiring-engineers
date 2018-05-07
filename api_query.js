var request = require("request");

var options = { method: 'POST',
  url: 'https://api.datadoghq.com/api/v1/dash',
  qs: 
   { api_key: 'redacted',
     application_key: 'redacted' },
  headers: 
   { 'Postman-Token': 'a18f5173-8d8b-4e4a-9948-ecb332475f20',
     'Cache-Control': 'no-cache',
     'Content-Type': 'application/json' },
  body: 
   { graphs: 
      [ { title: 'my_metric sum',
          definition: 
           { events: [],
             requests: [ { q: 'avg:my_metric{*}.rollup(sum, 3600)' } ],
             viz: 'query_value' } },
        { title: 'my_metric dashboard',
          definition: 
           { events: [],
             requests: [ { q: 'my_metric{*} by {host}' } ],
             viz: 'timeseries' } },
        { title: 'MySQL anomalies',
          definition: 
           { events: [],
             requests: [ { q: 'anomalies(avg:mysql.performance.cpu_time{*}, \'agile\', 2, direction=\'both\', alert_window=\'last_15m\', interval=60, count_default_zero=\'true\', seasonality=\'hourly\')' } ],
             viz: 'timeseries' } } ],
     title: 'cool timeboard 8',
     description: 'testing the API',
     read_only: 'True' },
  json: true };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});
