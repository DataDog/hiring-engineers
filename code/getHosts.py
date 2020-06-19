import requests
import pprint

s = requests.session()
s.params = {
  'api_key': 'd7afa42139e5f46b428466e4e935f8b5',
  'application_key': '43d17872e83a15abc8196ded43689d73c4a49bb7',  
}
infra_link = 'https://app.datadoghq.eu/api/v1/hosts'
infra_content = s.request(
  method='GET', url=infra_link, params=s.params
).json()

#print(infra_content)
pprint.pprint(infra_content)

