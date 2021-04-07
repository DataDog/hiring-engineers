#!/usr/bin/python3
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

PROTOCOLO = 'https'
ENDERECO = 'api.datadoghq.com'
URL = '%s://%s/api/v1/dashboard' % (PROTOCOLO, ENDERECO)
DD_API_KEY = 'REDACTED'
DD_APP_KEY = 'REDACTED'

PAYLOAD = json.dumps({
   "title": "Criando um Timeseries através da API",
   "widgets": [
       {
           "definition": {
               "type": "timeseries",
               "requests": [
                   {
                       "q": "anomalies(max:mysql.performance.com_select{host:ruan-virtualbox}, 'basic', 2)",
                       "display_type": "line",
                       "style": {
                           "palette": "dog_classic",
                           "line_type": "solid",
                           "line_width": "normal"
                       }
                   }
               ],
               "yaxis": {
                   "max": "auto",
                   "scale": "linear",
                   "min": "auto",
                   "label": "",
               },
               "title": "Performance de Selecta com a função de Detecção de Anomalias"
           }
       },

       {
           "definition": {
               "type": "timeseries",
               "requests": [
                   {
                       "q": "my_metric{host:ruan-virtualbox}"
                   }
               ],
               "yaxis": {
                   "max": "auto",
                   "scale": "linear",
                   "min": "auto",
                   "label": "",
               },
               "title": "my_metric com a configuração padrão"
           }
       },

       {
           "definition": {
               "type": "timeseries",
               "requests": [
                   {
                       "q": "sum:my_metric{host:ruan-virtualbox}.rollup(sum,3600)"
                   }
               ],
               "yaxis": {
                   "max": "auto",
                   "scale": "linear",
                   "min": "auto",
                   "label": "",
               },
               "title": "my_metric somado pela última hora"
           }
       },
   ],

   "layout_type": "ordered",
   "description": "Um dashboard criado através de REST API",
   "notify_list": ["ruanmarins96@gmail.com"],
   "template_variables": [
       {
           "name": "host",
           "prefix": "host"
       }
   ],

})

if __name__ == '__main__':
   response = requests.post(url=URL, data=PAYLOAD,
                            headers={'Content-Type': 'application/json', 'DD-API-KEY': DD_API_KEY,
                                     'DD-APPLICATION-KEY': DD_APP_KEY, }, verify=False)
   print(json.dumps(response.json(), indent=2))