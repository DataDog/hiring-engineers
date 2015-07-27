require 'bundler'
require 'statsd'


class Metric

  attr_reader :statsd

  def initialize
    @statsd = Dogstatsd.new('localhost', 8125)
  end

  def page_view_latency(page_name)
    start_time = Time.now
    page_views(page_name)
    duration = Time.now - start_time
    @statsd.histogram('page_view_latency', duration, :tags => ['support', 'page:#{page_name}'])
  end

  def page_views(page_name)
    @statsd.increment('web.page.views', :tags => ['support', 'page:#{page_name}'])
  end

end
