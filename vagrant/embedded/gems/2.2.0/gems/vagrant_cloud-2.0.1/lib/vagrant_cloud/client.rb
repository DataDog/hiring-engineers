require 'json'

module VagrantCloud
  class Client
    # Base Vagrant Cloud API URL
    URL_BASE = 'https://vagrantcloud.com/api/v1'.freeze
    attr_accessor :access_token

    # @param [String] access_token - token used to authenticate API requests
    # @param [String] url_base - URL used to make API requests
    def initialize(access_token = nil, url_base = nil)
      if url_base
        @url_base = url_base
      else
        @url_base = URL_BASE
      end

      @access_token = access_token
    end

    # @param [String] method
    # @param [String] path
    # @param [Hash] params
    # @param [String] token
    # @return [Hash]
    def request(method, path, params = {}, token = nil)
      headers = {}

      if token
        headers['Authorization'] = "Bearer #{token}"
      elsif @access_token
        headers['Authorization'] = "Bearer #{@access_token}"
      end

      headers['Accept'] = 'application/json'

      request_params = {
        method: method,
        url: @url_base + path,
        headers: headers,
        ssl_version: 'TLSv1'
      }

      if ['get', 'head', 'delete'].include?(method.downcase)
        headers[:params] = params
      else
        request_params[:payload] = params
      end

      begin
        result = RestClient::Request.execute(request_params)

        parse_json(result)
      rescue RestClient::ExceptionWithResponse => e
        raise ClientError.new(e.message, e.http_body, e.http_code)
      end
    end

    protected

    # Parse string of JSON
    #
    # @param [String] string JSON encoded string
    # @return [Object]
    # @note This is included to provide expected behavior on
    # Ruby 2.3. Once it has reached EOL this can be removed.
    def parse_json(string)
      JSON.parse(string)
    rescue JSON::ParserError
      raise if string != 'null'
    end
  end
end
