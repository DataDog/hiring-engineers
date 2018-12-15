Your answers to the questions go here.

<h1>Collecting metrics:</h1><br>

<h4>Host and its tags on the Host Map page in Datadog</h4>

![alt text](https://lh3.googleusercontent.com/gLfPsk9qtFoHbXBjhYvaCaRiTE8lttrL3FUYogAhoqHuGjBKTN51PbGlk4TpzyZdIdC440lEPb1u7yGju-QVARX-2jSxfnR4FkgmVoIwxTwHb_UuVpye-rl7C8x5HM2U0QgKfrBseYqu0sW7ANymBFoTIpZhQm__E7jH8mkNdkDYYcIR9zVHl6TNYZYro8zHbZQD5XyfVd3l2MrSmTwZxxNQTqwf9fEgk4cc1JJbNLeA7ciPL3KneVsd6L52N6nAjchWD301zO5ZnTnciRWV5bvdbnoU5ZD5xIqjE2GLHVubWmjw2SZzSnRxNc22lCl-RSjrbkVWS09nf6ldeLDovGte6vB3GKTm92Jc_-jPyJMQ-tzCJ3T9eWR2sB5ndso6Hf0Kbf1GB_x_7eFquxrxhWPjhOEsz6YvMz16GUFp27ZuTQB0wB0vd2TXwDzRBbF-DTiokcYBdToo39LRAveV1o4aU2Lelc5A7-4x7zLrlOqH4zJJafIKLbDRXWV-6EswPSPxvMmSh2NYArlqX0n0BUD1KaC8DGaR7lFJHRfyCir4dlDzPjFH7eE5UlbXP2KQ_wf2DcLyBcebdD4wL1FqCGC6OQj-z-_wUMvcA9eWUlxtlfkTkOnUp-5XIerOf4dwtFR9nS6U2FQmU38hPSCIKoqjF8QI0ekKDNyCMRfSAVAHzbkCiGeTZ7cv_nfuNm8W5Jq9muMENmcRsNMetA=w1514-h901-no-tmp.jpg "Host Map with tags screenshot")


- Bonus Question Can you change the collection interval without modifying the Python check file you created?<br>
Yes, we only need to modify Python check's config, a yaml file located in conf.d agent's directory. 
Just add:<br>

```- min_collection_interval: 45 ```

<hr>
<h1>Visualizing data:</h1><br>

<h4>HTimeboard screenshot</h4>

![alt text](https://lh3.googleusercontent.com/dg2zXs4JOmt-2r_A26o3K4K14qc6jmuyttfm-y0vLuShHO24dF8EURuYHbc7Ppulg2EFqPQBwupkm3WHywI_hipa2rm9y9RFDAUBxBps2eptseFut3W3rZFgkh_7PNZyfoIzplJKH4C_cSv6gvVO6ePtfeRDdSNKoF7thRnNkIIZVBn_cLErxE3HjFmfZ8rHMxtQ_dV6fPvu1-YnecX_rUm6KK2HtQ6Pv250zZbI4fHp6e030pFTONI93XlVthTr55cYI2cKBGBcrXKq54vpQ39wyuJHN-lm7o6mqweu5klc-qMyCO4Oz1F08fX92LO3dnmB9psYxwYC-IPjKAfNqf3K_Trn2hUUkQt43AJPAalLWaxTNzFLgPTCLtr4tmy2KDyh9gvXwnktmWzFk3P13aYZPGyRXtvks5WhTJRiO5jnEQ5n5juIKCtjaEuEmvx3v47BbfOzLUYVtpcrA1pBrniDKgIwO2VnEjNroVLOFCefWwXCPsnogBVgf5fGHME-YQLBosHr1u-jd0nAUbOqIabRHgmpjPfWlEVQ1G3KN-SPAt4CKbUHstLBEJpbUkAFO9qgwnjCAHKeW7wCh0ZAwLLomU7UuJ75MGcKwYPPALF7KIJB3An-QYf-w89lQTFFsyIJfTvkxV0ksEb40Z7t900EPHQduwpq1HuXLIETrQoVrsw75O5nlBbhqEqG1Mnsw6JY3TMkchoUDe_1QA=w1761-h611-no-tmp.jpg "Timeboard screenshot")

<h4>Script used to create Timeboard:</h4><br>

```python
#!/usr/bin/env python
from datadog import initialize, api

options = {
    'api_key': 'f100449dca7313b71f6abeb488c312c7',
    'app_key': '82818b84506cc9a41c43181b8b88bfd8567a14da'
}

initialize(**options)


title = "Datadog Hiring"
description = "Mix of graphs."
graphs = [
# first graph, my_metric
{
    "definition": {
        "events": [],
        "requests": [{"q": "custom.my_metric{host:datadog-test}", "type": "area"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random"
},
# 2nd graph, mysql metric with anomalies function
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:mysql.innodb.buffer_pool_free{host:datadog-test}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Mysql, buffer pool free, anomalies"
},
# 3rd graph, again my_metric but with anomalies function
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:custom.my_metric{host:datadog-test}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random, anomalies"
},
# 4th graph, my_metric rolled up
{
    "definition": {
        "events": [],
        "requests": [{"q": "custom.my_metric{host:datadog-test}.rollup(avg,3600)"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random, rolled up"
}
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```

<hr>
<h1>Monitoring data:</h1><br>

[Link](https://photos.app.goo.gl/r3emijTofDdN6nh4A) to my_metric monitor config screenshot showing thresholds.

[Link](https://photos.app.goo.gl/9UcJp9emSm4hbBUYA) to my_metric monitor config screenshot showing custom message and receiver.

- Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    One that silences it from 7pm to 9am daily on M-F,
    And one that silences it all day on Sat-Sun.

[Link](https://photos.app.goo.gl/SzpxQ4ziyP6nR7B56) to my_metric monitor 1st scheduled downtime email notification.

[Link](https://photos.app.goo.gl/1RjhvoM1d4hRiGxW9) to my_metric monitor 2nd scheduled downtime email notification.

hr>
<h1>Collecting APM data:</h1><br>
<h3>App used for instrumentation:</h3>

```python
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

