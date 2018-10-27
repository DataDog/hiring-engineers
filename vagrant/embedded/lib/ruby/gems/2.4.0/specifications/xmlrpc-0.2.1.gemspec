# -*- encoding: utf-8 -*-
# stub: xmlrpc 0.2.1 ruby lib

Gem::Specification.new do |s|
  s.name = "xmlrpc".freeze
  s.version = "0.2.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["SHIBATA Hiroshi".freeze]
  s.bindir = "exe".freeze
  s.date = "2016-12-22"
  s.description = "XMLRPC is a lightweight protocol that enables remote procedure calls over HTTP.".freeze
  s.email = ["hsbt@ruby-lang.org".freeze]
  s.homepage = "https://github.com/ruby/xmlrpc".freeze
  s.licenses = ["Ruby".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.4.0dev".freeze)
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "XMLRPC is a lightweight protocol that enables remote procedure calls over HTTP.".freeze

  s.installed_by_version = "2.6.14.1" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<bundler>.freeze, [">= 0"])
      s.add_development_dependency(%q<rake>.freeze, [">= 0"])
      s.add_development_dependency(%q<test-unit>.freeze, [">= 0"])
    else
      s.add_dependency(%q<bundler>.freeze, [">= 0"])
      s.add_dependency(%q<rake>.freeze, [">= 0"])
      s.add_dependency(%q<test-unit>.freeze, [">= 0"])
    end
  else
    s.add_dependency(%q<bundler>.freeze, [">= 0"])
    s.add_dependency(%q<rake>.freeze, [">= 0"])
    s.add_dependency(%q<test-unit>.freeze, [">= 0"])
  end
end
