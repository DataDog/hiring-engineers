# Level 1

## Regristration
Adress used : guillaume.deberdt@hec.edu

## What is the agent ?
The agent is a software that watch for metrics on your machine and send it to datadog.

## Event API
```ruby
require 'rubygems'
require 'dogapi'
api_key='...'
dog = Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('Hello dog !', :msg_title => 'Hello'))
```

## Event API with email
```ruby
require 'rubygems'
require 'dogapi'
api_key='...'
dog = Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('What if @guillaume.deberdt@hec.edu ?', :msg_title => 'Mailing with mention'))
```