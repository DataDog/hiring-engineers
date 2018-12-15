Your answers to the questions go here.

<h1>Collecting metrics:</h1><br>

<h4>Host and its tags on the Host Map page in Datadog</h4>

![alt text](https://lh3.googleusercontent.com/gLfPsk9qtFoHbXBjhYvaCaRiTE8lttrL3FUYogAhoqHuGjBKTN51PbGlk4TpzyZdIdC440lEPb1u7yGju-QVARX-2jSxfnR4FkgmVoIwxTwHb_UuVpye-rl7C8x5HM2U0QgKfrBseYqu0sW7ANymBFoTIpZhQm__E7jH8mkNdkDYYcIR9zVHl6TNYZYro8zHbZQD5XyfVd3l2MrSmTwZxxNQTqwf9fEgk4cc1JJbNLeA7ciPL3KneVsd6L52N6nAjchWD301zO5ZnTnciRWV5bvdbnoU5ZD5xIqjE2GLHVubWmjw2SZzSnRxNc22lCl-RSjrbkVWS09nf6ldeLDovGte6vB3GKTm92Jc_-jPyJMQ-tzCJ3T9eWR2sB5ndso6Hf0Kbf1GB_x_7eFquxrxhWPjhOEsz6YvMz16GUFp27ZuTQB0wB0vd2TXwDzRBbF-DTiokcYBdToo39LRAveV1o4aU2Lelc5A7-4x7zLrlOqH4zJJafIKLbDRXWV-6EswPSPxvMmSh2NYArlqX0n0BUD1KaC8DGaR7lFJHRfyCir4dlDzPjFH7eE5UlbXP2KQ_wf2DcLyBcebdD4wL1FqCGC6OQj-z-_wUMvcA9eWUlxtlfkTkOnUp-5XIerOf4dwtFR9nS6U2FQmU38hPSCIKoqjF8QI0ekKDNyCMRfSAVAHzbkCiGeTZ7cv_nfuNm8W5Jq9muMENmcRsNMetA=w1514-h901-no-tmp.jpg "Host Map with tags screenshot")


<h4>Bonus Question Can you change the collection interval without modifying the Python check file you created?</h4>
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
<h4>Take a snapshot of this graph and use the @ notation to send it to yourself.</h4>

![alt text](https://lh3.googleusercontent.com/zeBznAXleciYlxginvEYTBWfxWNRbvSLGznk7fsoOizJTg0rqAYfH7xk-MnDnuHkg0DYa69uiyN0wAFokQY4gb6hpbKuQsltb0ZcY1mYbkiT4VkM-WpubKqP9GrtvjG2zdB7RHLGKCZJ1oeglDdLIS7qqn3jdm80Xk4sKaAxkZ18gk0tQw6qyvONf0zzTVIvX9crh0qoHDBoSSy3iJANNm5X8gHitlOB94F5zwlq0oAlii4dQtzYVCWXjvGKNaF-XejjsMGyFWHSrFUrSVzs3axAXZfn01MJMRvvvAB7wnmi19-a4KtpyKS72okjogHXzhJBzJ8BFx3MXsexKooyWYEfvD96QrTawvqxQpWUsQYxreXuKFZNYgVT8AIl2DfYSnuqoT-vC4T1YTaHEbYP6Gm5bpubqElSL8AbWGHi7xf3yDrNEbXf3TCEzTTcOzqvyA1M_mq_-FIQwZ3jt660Mw4gJusJU8IHBMsWpiGiZtVcz5Kz_eBGgSSh4Jpij_z04qYEieLgfUsqUq0DfJB8IvsMNT9kes2Sqe1pqSJHmOz4Hc9sNxmUsFg5agJn_jP6JxBj04Qa4Ja80Mrbl0XJi6csBJyezmjX3hF8YogD4a8MMRavZFtt1MV3ZOtbCLaWlA6_HyNCmWQceBT1R775bboCnBy1wme9MW-4oBsABeUs-eAREATztQj4wuOyC4eO6RuSmJvaf76N9yRW9g=w707-h583-no-tmp.jpg "my_metric 5 min timeframe")

<h4>Bonus Question: What is the Anomaly graph displaying?</h4>
Anomalies tend to disappear when zooming in the data, meaning that some standalone points might not represent an anomaly.

<hr>
<h1>Monitoring data:</h1><br>

<h4>Please configure the monitor’s message so that it will:

 - Send you an email whenever the monitor triggers.

 - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

 - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

 - When this monitor sends you an email notification, take a screenshot of the email that it sends you.</h4>
 
 Alert triggered :
   ![alt text](https://lh3.googleusercontent.com/Svyf9W725SWKb3KItUQkab3tw_cQTlGIqLPMp7EWX164eS8vqRFwaU58DrJcRuyRO4BypvtGqk9cHyPqEyk18O78_6cgY4uyH17YZU7uUSQ7J8IPa2kCxCAcKzcBbV-W3vSL4WYKV_9aCpNKiAnWVmN0r8ix7Q1_5_rQN0lkHCXB_P2eiRPkmH1oQmSqrs5iMu1-o4wzSfiUeBS0q-KYM_DiAcGWuS7l8fNRGv4joKUz4lV-RVz2sZdYc7Qz6mEY65M6bVneF9Btktpcuo3LIAw5n80hMczyuxrnPdGHeRoQtCq7PvoUeqbCm2yX_RqrKBktnwWQ3OoSjqm8P6avPs0UwO3GIVXYo4NyWk5Bu5NbNNyeLhv9u5_DKHkvMfLIMCDjTtGnMtb04e3ltu6sib_TnnvE2impFblqbqSF-2RD0btW5RNJPxKm8D_9WhxnUu7WS7keFN46dFaYrGB0-mt-4-PHfnstw2S53MJJiML7ooGpIPR5d8GQxkwPLNGOg9VNqaHGB7gvIZhpQXTd79BzDK2bBxPpAZGt0B9Ax1kMMJ6pwsTq-Iq8G8JusTFy00SV_dFau3xKS0sM85mjCuNexINGa3mUoAG0mzxfQvZbNn02oKFbSFBOUEkCpWjn4rgHKUl5taPAR6QICacEpkMPtpww7DcjzRElwMLVbKUiu-UDRCeIv0wWtzofRi0Isk9q0RFwRvbQwFZ_SQ=w709-h736-no-tmp.jpg "my_metric monitor alert triggered")
   
 No data triggered :
    ![alt text](https://lh3.googleusercontent.com/LGhglkerLBch4uG_EBhZxVEASOlYde02KJqGP-1EZT-ysrDAAaXuuhVbaLBl7Dnwnr7P-SUAmUof0aEVoHLrJRNQBVPivhZrKOJJ7BxGHLrFXlm1gdmGX9UJoAwnyRPZD1uaKIIl3CTHspQ6wKM891G4InkNUWg30x0q12-eGD1qXo0_dyrTwfUV2JcORu8JIlL1HbKK9wrWd9IQ2u53Nyu4RJ_6UzSnVsg__VZv22uGn_i-ChkaP9QeyV7s3roPgq9nM52W4GUEvvYtFokvJYB2_d8n_m1jEzcoj0P86S9bHfYhCZXoG04i78kNGKBu31kMeVUYUxej25DhQgGrxjC1OLiMJfDMQqU3utaTWwODCN7MV9cj2jhh5U7rYN9bDnIvO9rhqTy48YeEQHXGTNC_FzQULAea-z49gVBeJtHs94yP_KvObxVWdKtUT6NUH5YpCDdFYU5CJXJYzJ8dgPQbNvok-qs_XYd4Qpe5ssjOr4XZdODL6-uPsSFyk3OH07e87SUEjEoBXU_WCX0I0mPG30AVQrNyQCw9vpyzCdqOu7notOA6lss1v6JiV4Fkmxekc6ecm2J1q4uZJ40MLGZOOqHbvZKB3lU696yPBogYidNrcTZCSs2axdggJ73d_dZJGYmBh1UEng54d51NVgx9Vxwn4WY1yvdkSbax9mfW-ekDcRKyzjO76TL2jyI9s_fkz6myetYmfM3ymw=w704-h533-no-tmp.jpg "my_metric monitor no data triggered"

<h4>Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:</h4>

   <h4>One that silences it from 7pm to 9am daily on M-F</h4>
   
   ![alt text](https://lh3.googleusercontent.com/MQIgW52Qm_F8dpzLPVs_xjlhfgO8vzKZVbsTSDpDU5cvUJ44rde-ClbsPL9u25PCbovKA8GDmClzUHk2p4D39sCtKWni_qCJohwkw4Qz23aVGAsuw50BNSqQBqMGmfZF4lsofaea-Dv7lU0p2p0qbf_VcR3vIoBdxRnsuGlbcwpHM2VALJ9KxfmLEdJbadNUG3mdmI84EAKQ9FKy_Wy9TkM5c7PINKx4WUewqZSNkTDoIPxUZ_L73MfG8yKUVD94aBICI3j-ceyo47GlTsyk_fDvOdvX6dd22R6aG0koKSss3bCATv8llWGSq_9HQSm7gC66nsw536xaRw6T-Yix3Sey8lpNb95ebZ5Av0xi_ezGUtrvLVNnNu2ZUxXvKe_X-cGXj2VN3GrjYF1EzHKbkvYddQtymTNi359cj9o9jmnZIE7PFYG4xTe4iqdvlSg1BQ-a3dgoiY1GF-KrjhGMMK2pxOBREFPbkuA8So-HFam3nTTgTtBx87NLmZ1W4YbcAmMyhim9Wft9T6SNCSn_K3jIqOxLDcRB1pyKvlSuBx5YzVnl9MJ-ZQc_vu5YPVHDxCra3c8OgHmR3_qkhpSeVchemDoIPzk3LRTw6MW1cUrtf8wY0LtGIVlC72Gzu737lkJNPqN-Tys9C5OtdkhDUGzNJd2DizcrZp_Wu78kOvDGeG7ElV9p319BlRzlVJTzm5r4vMbXjSyGFA4RrQ=w705-h408-no-tmp.jpg "my_metric monitor 1st scheduled downtime email notification")
   
   <h4>And one that silences it all day on Sat-Sun</h4>
   
   ![alt text](https://lh3.googleusercontent.com/G_dpIzs1okNkwbVxVMWA4Sr_75C06nNHPz4KsO3gm6QMgfj5XsCs4ao4RDLp8l19L8bgLJ3oD0Yhq3Y2bAw98vO_Kktmf6cKOE4wutqgtJ9nEn2H12auHGctmUM_fgq0miyWefOOThqXfSyh7svmp-AGC5B8R1Q-GzIj69icnH3xZHgrnHvJhJTkc-jz0aHt4k-CPUB1mPeTZ7kJXzVETNq8YaFhnrhZgJ8iV-_3HSZBwN1wKCVyJeE-p0QgiTMd786EDHXdorZznhfB9p4WF5nwVC2seQ3u5ofqaA7PsNTunAOLy8B6SI9CnO3gooWSk2Xzr5iC44DeexTR7mqBVL-zy7XzTAB9rnMV_oVDH7PD2JMU6Adn4GiZLdLI5rObzwJD-8FDKB6gIN3iK5_FXGgzh0esE5xxqZqUFh3vgTXdD2xCxBFGmqynUZ5GacLak-2m3YnM-Hr2oWbdXQ6u9J4AnqxCv21OCgOQbuoHEN-5d6ti2PNQLKNd9Tuc0nvzOKd5Pf0Q7OzwQ-IMVl3WrzGy-oQASTmqv7N7AB2L69yJwX7_TVEdUCgemMFAG5L3D_WCiq0RlY-w0kYUCT3pKqVjpjat24eyw8Z2JsBb_sMlCPTFGwc2zTiPfhzExKJNhXFhx9elrhyfaa3VGcUKnaCd_7wPt11DtfZCsHJzgzvWewJqDFdrna18ZdzvFN-a49BrUZqAEDSYOgeHDw=w708-h409-no-tmp.jpg "my_metric monitor 2nd scheduled downtime email notification")

<hr>
<h1>Collecting APM data:</h1><br>
<h4>App used for instrumentation:</h4>

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

<h4>Bonus Question: What is the difference between a Service and a Resource?</h4>

A service is a set of processes doing the same job. A website service might be comprised of a frontend process, a backend process and a database process. Services are defined by users when instrumenting an app.
A resource is a service component, discovered through app instrumentation.Resources are, for instance, a SQL query for a database, or a canonical url for a web app.

<h3>Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics</h3>

![alt text](https://lh3.googleusercontent.com/rWstc2pDUx9APhXybSKSpgnwCrqKbpjJ2oMO_lbPUWLa5etDJYw5rni4L_zpn_Siq0TAYvp5SEy3nZwxbay4FuB8O5jxehCdAR3aWLGQebV6YXCxygYs7UeZL9DbFb3Shnp9sh_qDYz8DUCv-8pIAkXGuv0j-SlP7GQt8L3eWk4WvtMrt1xGiWQzz36AP9IC8YJ-pZK0gsBfIGE_dsxLYpJT6G8CeV6ud81IA1OKMjf9H0W5KZvm0WB-DLIJi9kGXtP6QY1b31Lv2znbSQgN7Otfnyrq5UZ9J7SYFhpdvDBRrgEv_fCR_81A31u6EWK5V5zZdM-oVgb9KenpJL0JQIB3u-CAcEHm8DVNQPim3SzMoY967xydCywD29Z3lJRrlEGo5PmiHfngeR3jNU_GjvtJJxJmyI570lX_eM_eSzKKeJJPdzOivjFQgBucqA22VvkT26VdJzZD8V2CGbAWF9_eWgmVYU7UKPJ_EzvzeAinsnPiJ0MxrV20eOodW8Og11Wq5RRUp1qUHvtI7smF8P8InZ6HSwUneqiXmzGPDuPoVmap0g85uEZ_h5eBJCt6enBGwKjnJY_oPTTubaEu_7LjwfOOi-N5zwFhy0N5ZraXh-mqoeTrCZCvUcim5UKSjC5mL_XmbiWjV2JbR1Vfe5gIoS-R3ikGfDKqByTIunaaIETntqIOI77FCFYkms2v-uHBSoyp59UGdtg6_A=w1745-h887-no-tmp.jpg "APM and infrastructure metrics")

<hr>
<h1>Final question</h1><br>
Is there anything creative you would use Datadog for?
 
- Get data from BACNET enabled devices ( power consumption, cooling systems, etc ), useful in Datacenter environment monitoring.

  There is a python library related to this : (http://bacpypes.sourceforge.net/)
  
-  Monitor flight status, like aircraft type, Longitude, latitude, groundspeed and altitude, origin and destination.

   For the latter, it would be really good to have kind of geo map widget.
   https://flightaware.com/commercial/flightxml/

- Get data from M-Bus enabled devices. M-Bus is a European standard for remote reading of heatmeters and it is also usable for all other types of consumption meters as well as for various sensors and actuators.
