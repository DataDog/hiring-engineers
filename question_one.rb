require 'rubygems'
require 'pry'
require 'dogapi'

def dog_get_event_attribute(dog_event, attribute_str)
  dog_event[1]["event"][attribute_str]
end

api_key='822c15b7b2f9fb8c49e8827404903e58'
app_key='f1dab6bb368ffa58b5d5af3358d77e42f48a1a21'

# dog = Dogapi::Client.new(api_key, app_key)
dog = Dogapi::Client.new(api_key)

test_event = dog.emit_event(Dogapi::Event.new('this will be the text', :msg_title => 'My Title :)'))
event_id = dog_get_event_attribute(test_event, "id")


# binding.pry
p "EOF"