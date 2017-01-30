require 'dogapi'
require 'pry'

api_key='0d0bc2c28b64ad1405ab8ffd71e8e222'

# submitting events doesn't require an application_key, so we don't bother
# setting it
dog = Dogapi::Client.new(api_key)

response = dog.emit_event(Dogapi::Event.new('Hello DataDog!', :msg_title => 'Ruby Script Submitting Event'))

if response[0] == "202"
  puts "Event created: #{response[1]["event"]["url"]}"
else
  puts "Something went wrong: #{response.inspect}"
end