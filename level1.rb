require 'rubygems'
require 'dogapi'

api_key='8c259a49030624992bbf66837140134a'

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new('This is a test.', :msg_title => 'Test message', :email => 'event-n3wf1a4l@dtdg.co'))
