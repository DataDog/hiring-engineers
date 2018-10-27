require 'rubygems'
require 'bundler/setup'
require 'winrm-fs'
require 'json'
require_relative 'matchers'

# Creates a WinRM connection for integration tests
module ConnectionHelper
  def winrm_connection
    WinRM::Connection.new(config)
  end

  def config
    @config ||= begin
      cfg = symbolize_keys(YAML.safe_load(File.read(winrm_config_path)))
      cfg[:basic_auth_only] = true unless cfg[:transport].eql? :kerberos
      merge_environment!(cfg)
      cfg
    end
  end

  def merge_environment!(config)
    merge_config_option_from_environment(config, 'user')
    merge_config_option_from_environment(config, 'password')
    merge_config_option_from_environment(config, 'no_ssl_peer_verification')
    config[:options][:ssl_peer_fingerprint] = ENV['winrm_cert'] if ENV['use_ssl_peer_fingerprint']
    config[:endpoint] = ENV['winrm_endpoint'] if ENV['winrm_endpoint']
    config[:transport] = ENV['winrm_transport'] if ENV['winrm_transport']
  end

  def merge_config_option_from_environment(config, key)
    env_key = 'winrm_' + key
    config[key.to_sym] = ENV[env_key] if ENV[env_key]
  end

  def winrm_config_path
    # Copy config-example.yml to config.yml and edit for your local configuration
    path = File.expand_path("#{File.dirname(__FILE__)}/config.yml")
    unless File.exist?(path)
      # user hasn't done this, so use sane defaults for unit tests
      path = File.expand_path("#{File.dirname(__FILE__)}/config-example.yml")
    end
    path
  end

  # rubocop:disable Metrics/MethodLength
  def symbolize_keys(hash)
    hash.each_with_object({}) do |(key, value), result|
      new_key = case key
                when String then key.to_sym
                else key
                end
      new_value = case value
                  when Hash then symbolize_keys(value)
                  else value
                  end
      result[new_key] = new_value
      result
    end
  end
  # rubocop:enable Metrics/MethodLength
end

RSpec.configure do |config|
  config.include(ConnectionHelper)
end
