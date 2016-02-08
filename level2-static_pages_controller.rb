class StaticPagesController < ApplicationController
  require 'statsd'
  layout false

  def contact
    start = Time.now
    s = Statsd.new
    s.increment('web.page_views')
    render 'contact'
    lag = Time.now - start
    s.histogram('latency', lag)
  end

  def demoreel
    start = Time.now
    s = Statsd.new
    s.increment('web.page_views')
    render 'demoreel'
    lag = Time.now - start
    s.histogram('latency', lag)
  end

  def production
    start = Time.now
    s = Statsd.new
    s.increment('web.page_views')
    render 'production'
    lag = Time.now - start
    s.histogram('latency', lag)
  end

  def resume
    start = Time.now
    s = Statsd.new
    s.increment('web.page_views')
    render 'resume'
    lag = Time.now - start
    s.histogram('latency', lag)
  end

end