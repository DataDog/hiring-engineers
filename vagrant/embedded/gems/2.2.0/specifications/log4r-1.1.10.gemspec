# -*- encoding: utf-8 -*-
# stub: log4r 1.1.10 ruby lib

Gem::Specification.new do |s|
  s.name = "log4r".freeze
  s.version = "1.1.10"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Colby Gutierrez-Kraybill".freeze]
  s.date = "2012-01-02"
  s.description = "See also: http://logging.apache.org/log4j".freeze
  s.email = "colby@astro.berkeley.edu".freeze
  s.homepage = "http://log4r.rubyforge.org".freeze
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "Log4r, logging framework for ruby".freeze

  s.installed_by_version = "2.6.14.1" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<bundler>.freeze, [">= 1.0.0"])
      s.add_development_dependency(%q<rake>.freeze, ["~> 0.8.7"])
    else
      s.add_dependency(%q<bundler>.freeze, [">= 1.0.0"])
      s.add_dependency(%q<rake>.freeze, ["~> 0.8.7"])
    end
  else
    s.add_dependency(%q<bundler>.freeze, [">= 1.0.0"])
    s.add_dependency(%q<rake>.freeze, ["~> 0.8.7"])
  end
end
