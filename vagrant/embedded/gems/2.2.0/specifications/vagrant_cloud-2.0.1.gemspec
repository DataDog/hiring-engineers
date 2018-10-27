# -*- encoding: utf-8 -*-
# stub: vagrant_cloud 2.0.1 ruby lib

Gem::Specification.new do |s|
  s.name = "vagrant_cloud".freeze
  s.version = "2.0.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["HashiCorp".freeze, "Cargo Media".freeze]
  s.date = "2018-10-17"
  s.description = "Ruby library for the HashiCorp Vagrant Cloud API".freeze
  s.email = "vagrant@hashicorp.com".freeze
  s.homepage = "https://github.com/hashicorp/vagrant_cloud".freeze
  s.licenses = ["MIT".freeze]
  s.post_install_message = "NOTICE: As of the 2.0.0 release, the vagrant_cloud gem provides library functionality\n        and no longer includes a command line client. For a command line client,\n        use the `vagrant cloud` subcommand from Vagrant. Vagrant can be downloaded\n        from: https://www.vagrantup.com/downloads.html".freeze
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "Vagrant Cloud API Library".freeze

  s.installed_by_version = "2.6.14.1" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<rest-client>.freeze, ["~> 2.0.2"])
      s.add_development_dependency(%q<rake>.freeze, ["~> 10.4"])
      s.add_development_dependency(%q<rspec>.freeze, ["~> 3.0"])
      s.add_development_dependency(%q<rubocop>.freeze, ["~> 0.59.1"])
      s.add_development_dependency(%q<webmock>.freeze, ["~> 3.0"])
    else
      s.add_dependency(%q<rest-client>.freeze, ["~> 2.0.2"])
      s.add_dependency(%q<rake>.freeze, ["~> 10.4"])
      s.add_dependency(%q<rspec>.freeze, ["~> 3.0"])
      s.add_dependency(%q<rubocop>.freeze, ["~> 0.59.1"])
      s.add_dependency(%q<webmock>.freeze, ["~> 3.0"])
    end
  else
    s.add_dependency(%q<rest-client>.freeze, ["~> 2.0.2"])
    s.add_dependency(%q<rake>.freeze, ["~> 10.4"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.0"])
    s.add_dependency(%q<rubocop>.freeze, ["~> 0.59.1"])
    s.add_dependency(%q<webmock>.freeze, ["~> 3.0"])
  end
end
