from datadog import initialize, api
import json

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

initialize(**options)

#print api.Timeboard.get_all()
print json.dumps(api.Timeboard.get(516072))