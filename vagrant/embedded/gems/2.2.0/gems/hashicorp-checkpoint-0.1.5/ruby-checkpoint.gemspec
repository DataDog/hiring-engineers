# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'checkpoint/version'

Gem::Specification.new do |spec|
  spec.name          = "hashicorp-checkpoint"
  spec.version       = Checkpoint::VERSION
  spec.authors       = ["Mitchell Hashimoto"]
  spec.email         = ["mitchell@hashicorp.com"]
  spec.summary       = %q{Internal HashiCorp service to check version information.}
  spec.description   = %q{Internal HashiCorp service to check version information}
  spec.homepage      = "http://www.hashicorp.com"
  spec.license       = "MPL2"

  spec.files         = `git ls-files -z`.split("\x0")
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.test_files    = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths = ["lib"]

  spec.add_development_dependency "bundler", "~> 1.6"
  spec.add_development_dependency "rake"
  spec.add_development_dependency "rspec", "~> 3.0.0"
  spec.add_development_dependency "rspec-its", "~> 1.0.0"
end
