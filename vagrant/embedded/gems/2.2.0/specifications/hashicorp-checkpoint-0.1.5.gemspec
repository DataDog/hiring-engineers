# -*- encoding: utf-8 -*-
# stub: hashicorp-checkpoint 0.1.5 ruby lib

Gem::Specification.new do |s|
  s.name = "hashicorp-checkpoint".freeze
  s.version = "0.1.5"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Mitchell Hashimoto".freeze]
  s.date = "2018-01-19"
  s.description = "Internal HashiCorp service to check version information".freeze
  s.email = ["mitchell@hashicorp.com".freeze]
  s.homepage = "http://www.hashicorp.com".freeze
  s.licenses = ["MPL2".freeze]
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "Internal HashiCorp service to check version information.".freeze

  s.installed_by_version = "2.6.14.1" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<bundler>.freeze, ["~> 1.6"])
      s.add_development_dependency(%q<rake>.freeze, [">= 0"])
      s.add_development_dependency(%q<rspec>.freeze, ["~> 3.0.0"])
      s.add_development_dependency(%q<rspec-its>.freeze, ["~> 1.0.0"])
    else
      s.add_dependency(%q<bundler>.freeze, ["~> 1.6"])
      s.add_dependency(%q<rake>.freeze, [">= 0"])
      s.add_dependency(%q<rspec>.freeze, ["~> 3.0.0"])
      s.add_dependency(%q<rspec-its>.freeze, ["~> 1.0.0"])
    end
  else
    s.add_dependency(%q<bundler>.freeze, ["~> 1.6"])
    s.add_dependency(%q<rake>.freeze, [">= 0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.0.0"])
    s.add_dependency(%q<rspec-its>.freeze, ["~> 1.0.0"])
  end
end
