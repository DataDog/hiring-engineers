require './models/metric.rb'
require 'bundler'
Bundler.require


class ApplicationController < Sinatra::Base

    @@metric = Metric.new

    account_sid ||= ENV["account_sid"]
    auth_token ||= ENV["auth_token"]
    twilio_number ||= ENV["twilio_number"]
    api_key ||= ENV["api_key"]
    app_key ||= ENV["app_key"]
    # $dyno_id ||= ENV['DYNO']

    dog = Dogapi::Client.new(api_key, app_key)
    # dog.emit_event(Dogapi::Event.new('Datadog Event submission via API - @mstines007@gmail.com', :msg_title => 'Level 1 Email test'))
    # dog.emit_event(Dogapi::Event.new('App test', :msg_title => 'Level 2 App test'))

    get '/' do
        # @@metric.page_views("home")
        @@metric.page_view_latency("home")

        erb :home
    end

    post '/' do
        @recipient = params[:recipient]
        @keyword = params[:keyword]
        @number = params[:number]
        @message = params[:message]
        @sender = params[:sender]
        @greeting = "Hey #{@recipient}!, #{@message} - Sent by #{@sender}"
        @gif = Giphy.random(tag=@keyword).image_original_url.to_s

        @client = Twilio::REST::Client.new account_sid, auth_token 
     
        @client.account.messages.create({
        :from => twilio_number, 
        :to => @number,
        :body => @greeting, 
        :media_url => @gif })

        # @@metric.page_views("results")
        @@metric.page_view_latency("results")

        erb :result
    end 

end