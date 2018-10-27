module VagrantCloud
  class Account
    attr_accessor :username
    attr_accessor :access_token

    # @param [String] username
    # @param [String] access_token
    def initialize(username, access_token, custom_server = nil)
      @username = username
      @access_token = access_token
      @client = Client.new(access_token, custom_server)
    end

    #---------------------------
    # Authentication API Helpers
    #---------------------------

    # @param [String] password
    # @param [String] description
    # @param [String] 2FA code
    # @return [Hash] response body
    def create_token(password, description = nil, code = nil)
      token_data_params = {
        token: { description: description },
        user:  { login: @username, password: password },
        two_factor: code
      }.delete_if { |_, v| v.nil? }

      token_response = @client.request('post', '/authenticate', token_data_params)
      token_response
    end

    # @param [String] token
    def delete_token(access_token = nil)
      token_response = @client.request('delete', '/authenticate', nil, access_token)
      token_response
    end

    # Validates a token on the account or a one-off validation token request.
    # Will return nil if token is valid, otherwise will return Hash of response
    # from Vagrant Cloud
    #
    # @param [String] access_token
    # @return [Hash] response body
    def validate_token(access_token = nil)
      token_response = @client.request('get', '/authenticate', nil, access_token)
      token_response
    end

    # @param [String] delivery_method
    # @param [String] password
    # @return [Hash] response body
    def request_2fa_code(delivery_method, password)
      twofa_code_params = {
        two_factor: { delivery_method: delivery_method },
        user: { login: @username, password: password }
      }

      code_response = @client.request('post', '/two-factor/request-code', twofa_code_params)
      code_response
    end

    #---------------------------
    # Organization API Helpers
    #---------------------------

    # @param [String] - organization
    # @return [Hash]
    def read_organization(org = nil)
      if org
        name = org
      else
        name = @username
      end

      @client.request('get', "/user/#{name}")
    end

    #--------------------
    # Old Box API Helpers
    #--------------------

    # @param [String] name
    # @param [Hash] data
    # @return [Box]
    def get_box(name, data = nil)
      Box.new(self, name, data)
    end

    # @param [String] name
    # @param [Hash] args
    # @return [Box]
    def create_box(name, *args)
      params = box_params(*args)
      params[:name] = name

      data = @client.request('post', '/boxes', box: params)
      get_box(name, data)
    end

    # @param [String] name
    # @param [Hash] args
    # @return [Box]
    def ensure_box(name, *args)
      params = box_params(*args)

      begin
        box = get_box(name)
        box.data
      rescue RestClient::ResourceNotFound
        box = create_box(name, params)
        # If we've just created the box, we're done.
        return box
      end

      # Select elements from params that don't match what we have in the box
      # data. These are changed parameters and should be updated.
      update_params = params.select do |k, v|
        box.data[box.param_name(k)] != v
      end

      # Update the box with any params that had changed.
      box.update(update_params) unless update_params.empty?

      box
    end

    #--------------------
    # Old Box API Helpers
    #--------------------

    # REMOVED IN FAVOR OF CLIENT CLASS, but still exists to support any old clients
    #
    # @param [String] method
    # @param [String] path
    # @param [Hash] params
    # @return [Hash]
    def request(method, path, params = {})
      headers = {}

      headers['Authorization'] = "Bearer #{access_token}" if access_token

      result = RestClient::Request.execute(
        method: method,
        url: url_base + path,
        payload: params,
        headers: headers,
        ssl_version: 'TLSv1'
      )
      result = JSON.parse(result)
      errors = result['errors']
      raise "Vagrant Cloud returned error: #{errors}" if errors

      result
    end

    private

    # @return [String]
    def url_base
      'https://vagrantcloud.com/api/v1'
    end

    # @param [Array] args
    # @return [Hash]
    def box_params(*args)
      # Prepares a hash based on the *args array passed in.
      # Acceptable parameters are those documented by Hashicorp for the v1 API
      # at https://vagrantcloud.com/docs

      # This dance is to simulate what we could have accomplished with **args
      # in Ruby 2.0+
      # This will silently discard any options that are not passed in as a
      # hash.
      # Find and remove the first hash we find in *args. Set params to an
      # empty hash if we weren't passed one.
      params = args.select { |v| v.is_a?(Hash) }.first
      if params.nil?
        params = {}
      else
        args.delete_if { |v| v == params }
      end

      # Default boxes to public can be overridden by providing :is_private
      params[:is_private] = false unless params.key?(:is_private)

      params
    end
  end
end
