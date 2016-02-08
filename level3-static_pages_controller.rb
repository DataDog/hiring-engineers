class StaticPagesController < ApplicationController
  require 'statsd'
  layout false
  
  def common_tags 
    return ["support"]
  end

  def contact
    start = Time.now
    s = Statsd.new
    tags = common_tags().push("page:contact")
    s.increment('web.page_views', :tags => tags)
    render 'contact'
    lag = Time.now - start
    s.histogram('latency', lag, :tags => tags)
  end

  def demoreel
    start = Time.now
    s = Statsd.new
    tags = common_tags().push("page:demoreel")
    s.increment('web.page_views', :tags => tags)
    render 'demoreel'
    lag = Time.now - start
    s.histogram('latency', lag, :tags => tags)
  end

  def production
    start = Time.now
    s = Statsd.new
    tags = common_tags().push("page:production")
    s.increment('web.page_views', :tags => tags)
    render 'production'
    lag = Time.now - start
    s.histogram('latency', lag, :tags => tags)
  end

  def resume
    start = Time.now
    s = Statsd.new
    tags = common_tags().push("page:resume")
    s.increment('web.page_views', :tags => tags)
    render 'resume'
    lag = Time.now - start
    s.histogram('latency', lag, :tags => tags)
  end

end
