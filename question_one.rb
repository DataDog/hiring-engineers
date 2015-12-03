require 'rubygems'
require 'pry'
require 'dogapi'

# def dog_get_event_attribute(dog_event, attribute_str)
#   dog_event[1]["event"][attribute_str]
# end

api_key='822c15b7b2f9fb8c49e8827404903e58'
app_key='f1dab6bb368ffa58b5d5af3358d77e42f48a1a21'

dog = Dogapi::Client.new(api_key, app_key)
# dog = Dogapi::Client.new(api_key)

#include the email address with an '@' infront of it in the message of the event to have it send the event to that email address
test_event = dog.emit_event(Dogapi::Event.new("this will be the text\n@jroth@colgate.edu", :msg_title => 'My Title :)'))

# binding.pry
p "EOF"