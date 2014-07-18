require 'dogapi'
require 'pry'

api_key='0d0bc2c28b64ad1405ab8ffd71e8e222'
app_key='3b2ec73762a7718e66677262b0f895b92e1310c0'

dog = Dogapi::Client.new(api_key, app_key)

# Create a new alert
dog.alert("avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 1", :name => "Bytes received on host0", :message => "We may need to add web hosts if this is consistently high.")