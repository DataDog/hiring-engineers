# -*- encoding: utf-8 -*-
# stub: vagrant 2.2.0 ruby lib

Gem::Specification.new do |s|
  s.name = "vagrant".freeze
  s.version = "2.2.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 1.3.6".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Mitchell Hashimoto".freeze, "John Bender".freeze]
  s.date = "2018-10-16"
  s.description = "Vagrant is a tool for building and distributing virtualized development environments.".freeze
  s.email = ["mitchell.hashimoto@gmail.com".freeze, "john.m.bender@gmail.com".freeze]
  s.executables = ["vagrant".freeze]
  s.files = ["bin/vagrant".freeze]
  s.homepage = "https://www.vagrantup.com".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(["< 2.6".freeze, "~> 2.2".freeze])
  s.rubyforge_project = "vagrant".freeze
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "Build and distribute virtualized development environments.".freeze

  s.installed_by_version = "2.6.14.1" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<childprocess>.freeze, ["~> 0.6.0"])
      s.add_runtime_dependency(%q<erubis>.freeze, ["~> 2.7.0"])
      s.add_runtime_dependency(%q<i18n>.freeze, ["<= 0.8.0", ">= 0.6.0"])
      s.add_runtime_dependency(%q<listen>.freeze, ["~> 3.1.5"])
      s.add_runtime_dependency(%q<hashicorp-checkpoint>.freeze, ["~> 0.1.5"])
      s.add_runtime_dependency(%q<log4r>.freeze, ["< 1.1.11", "~> 1.1.9"])
      s.add_runtime_dependency(%q<net-ssh>.freeze, ["~> 5.0.0"])
      s.add_runtime_dependency(%q<net-sftp>.freeze, ["~> 2.1"])
      s.add_runtime_dependency(%q<net-scp>.freeze, ["~> 1.2.0"])
      s.add_runtime_dependency(%q<rb-kqueue>.freeze, ["~> 0.2.0"])
      s.add_runtime_dependency(%q<rest-client>.freeze, ["< 3.0", ">= 1.6.0"])
      s.add_runtime_dependency(%q<rubyzip>.freeze, ["~> 1.2.2"])
      s.add_runtime_dependency(%q<wdm>.freeze, ["~> 0.1.0"])
      s.add_runtime_dependency(%q<winrm>.freeze, ["~> 2.1"])
      s.add_runtime_dependency(%q<winrm-fs>.freeze, ["~> 1.0"])
      s.add_runtime_dependency(%q<winrm-elevated>.freeze, ["~> 1.1"])
      s.add_runtime_dependency(%q<vagrant_cloud>.freeze, ["~> 2.0.0"])
      s.add_runtime_dependency(%q<ruby_dep>.freeze, ["<= 1.3.1"])
      s.add_development_dependency(%q<rake>.freeze, ["~> 12.0.0"])
      s.add_development_dependency(%q<rspec>.freeze, ["~> 3.5.0"])
      s.add_development_dependency(%q<rspec-its>.freeze, ["~> 1.2.0"])
      s.add_development_dependency(%q<webmock>.freeze, ["~> 2.3.1"])
      s.add_development_dependency(%q<fake_ftp>.freeze, ["~> 0.1.1"])
    else
      s.add_dependency(%q<childprocess>.freeze, ["~> 0.6.0"])
      s.add_dependency(%q<erubis>.freeze, ["~> 2.7.0"])
      s.add_dependency(%q<i18n>.freeze, ["<= 0.8.0", ">= 0.6.0"])
      s.add_dependency(%q<listen>.freeze, ["~> 3.1.5"])
      s.add_dependency(%q<hashicorp-checkpoint>.freeze, ["~> 0.1.5"])
      s.add_dependency(%q<log4r>.freeze, ["< 1.1.11", "~> 1.1.9"])
      s.add_dependency(%q<net-ssh>.freeze, ["~> 5.0.0"])
      s.add_dependency(%q<net-sftp>.freeze, ["~> 2.1"])
      s.add_dependency(%q<net-scp>.freeze, ["~> 1.2.0"])
      s.add_dependency(%q<rb-kqueue>.freeze, ["~> 0.2.0"])
      s.add_dependency(%q<rest-client>.freeze, ["< 3.0", ">= 1.6.0"])
      s.add_dependency(%q<rubyzip>.freeze, ["~> 1.2.2"])
      s.add_dependency(%q<wdm>.freeze, ["~> 0.1.0"])
      s.add_dependency(%q<winrm>.freeze, ["~> 2.1"])
      s.add_dependency(%q<winrm-fs>.freeze, ["~> 1.0"])
      s.add_dependency(%q<winrm-elevated>.freeze, ["~> 1.1"])
      s.add_dependency(%q<vagrant_cloud>.freeze, ["~> 2.0.0"])
      s.add_dependency(%q<ruby_dep>.freeze, ["<= 1.3.1"])
      s.add_dependency(%q<rake>.freeze, ["~> 12.0.0"])
      s.add_dependency(%q<rspec>.freeze, ["~> 3.5.0"])
      s.add_dependency(%q<rspec-its>.freeze, ["~> 1.2.0"])
      s.add_dependency(%q<webmock>.freeze, ["~> 2.3.1"])
      s.add_dependency(%q<fake_ftp>.freeze, ["~> 0.1.1"])
    end
  else
    s.add_dependency(%q<childprocess>.freeze, ["~> 0.6.0"])
    s.add_dependency(%q<erubis>.freeze, ["~> 2.7.0"])
    s.add_dependency(%q<i18n>.freeze, ["<= 0.8.0", ">= 0.6.0"])
    s.add_dependency(%q<listen>.freeze, ["~> 3.1.5"])
    s.add_dependency(%q<hashicorp-checkpoint>.freeze, ["~> 0.1.5"])
    s.add_dependency(%q<log4r>.freeze, ["< 1.1.11", "~> 1.1.9"])
    s.add_dependency(%q<net-ssh>.freeze, ["~> 5.0.0"])
    s.add_dependency(%q<net-sftp>.freeze, ["~> 2.1"])
    s.add_dependency(%q<net-scp>.freeze, ["~> 1.2.0"])
    s.add_dependency(%q<rb-kqueue>.freeze, ["~> 0.2.0"])
    s.add_dependency(%q<rest-client>.freeze, ["< 3.0", ">= 1.6.0"])
    s.add_dependency(%q<rubyzip>.freeze, ["~> 1.2.2"])
    s.add_dependency(%q<wdm>.freeze, ["~> 0.1.0"])
    s.add_dependency(%q<winrm>.freeze, ["~> 2.1"])
    s.add_dependency(%q<winrm-fs>.freeze, ["~> 1.0"])
    s.add_dependency(%q<winrm-elevated>.freeze, ["~> 1.1"])
    s.add_dependency(%q<vagrant_cloud>.freeze, ["~> 2.0.0"])
    s.add_dependency(%q<ruby_dep>.freeze, ["<= 1.3.1"])
    s.add_dependency(%q<rake>.freeze, ["~> 12.0.0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.5.0"])
    s.add_dependency(%q<rspec-its>.freeze, ["~> 1.2.0"])
    s.add_dependency(%q<webmock>.freeze, ["~> 2.3.1"])
    s.add_dependency(%q<fake_ftp>.freeze, ["~> 0.1.1"])
  end
end
