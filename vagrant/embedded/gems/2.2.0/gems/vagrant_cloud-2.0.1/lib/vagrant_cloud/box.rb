module VagrantCloud
  class Box
    attr_accessor :account
    attr_accessor :name

    # @param [String] account
    # @param [String] name
    # @param [Hash] data
    # @param [String] description
    # @param [String] short_description
    # @param [String] access_token
    def initialize(account, name = nil, data = nil, short_description = nil, description = nil, access_token = nil, custom_server = nil)
      @account = account
      @name = name
      @data = data
      @description = description
      @short_description = short_description
      @client = Client.new(access_token, custom_server)
    end

    #--------------------
    # Box API Helpers
    #--------------------

    # Read this box
    # @return [Hash]
    def data
      @data ||= @client.request('get', box_path)
    end

    # Update a box
    #
    # @param [Hash] args
    # @param [String] org - organization of the box to read
    # @param [String] box_name - name of the box to read
    # @return [Hash]
    def update(args = {})
      # hash arguments kept for backwards compatibility
      data = @client.request('put', box_path(args[:organization], args[:name]), box: args)

      # Update was called on *this* object, so update
      # objects data locally
      @data = data if !args[:organization] && !args[:name]
      data
    end

    # A generic function to read any box on Vagrant Cloud
    # If org and box name is not supplied, it will default to
    # reading the given Box object
    #
    # @param [String] org - organization of the box to read
    # @param [String] box_name - name of the box to read
    # @return [Hash]
    def delete(org = nil, box_name = nil)
      @client.request('delete', box_path(org, box_name))
    end

    # A generic function to read any box on Vagrant Cloud
    #
    # @param [String] org - organization of the box to read
    # @param [String] box_name - name of the box to read
    # @return [Hash]
    def read(org = nil, box_name = nil)
      @client.request('get', box_path(org, box_name))
    end

    # @param [String] short_description
    # @param [String] description
    # @param [Bool] is_private
    # @return [Hash]
    def create(short_description = nil, description = nil, org = nil, box_name = nil, is_private = false)
      update_data = !(org && box_name)

      org ||= account.username
      box_name ||= @name
      short_description ||= @short_description
      description ||= @description

      params = {
        name: box_name,
        username: org,
        is_private: is_private,
        short_description: short_description,
        description: description
      }.delete_if { |_, v| v.nil? }

      data = @client.request('post', '/boxes', box: params)

      # Create was called on *this* object, so update
      # objects data locally
      @data = data if update_data
      data
    end

    #--------------------
    # Metadata Helpers
    #--------------------

    # @return [String]
    def description
      data['description_markdown'].to_s
    end

    # @return [String]
    def description_short
      data['short_description'].to_s
    end

    # @return [TrueClass, FalseClass]
    def private
      !!data['private']
    end

    # @return [Array<Version>]
    def versions
      version_list = data['versions'].map { |data| VagrantCloud::Version.new(self, data['number'], data) }
      version_list.sort_by { |version| Gem::Version.new(version.number) }
    end

    #------------------------
    # Old Version API Helpers
    #------------------------

    # @param [Integer] number
    # @param [Hash] data
    # @return [Version]
    def get_version(number, data = nil)
      VagrantCloud::Version.new(self, number, data)
    end

    # @param [String] name
    # @param [String] description
    # @return [Version]
    def create_version(name, description = nil)
      params = { version: name }
      params[:description] = description if description
      data = @client.request('post', "#{box_path}/versions", version: params)
      get_version(data['number'], data)
    end

    # @param [String] name
    # @param [String] description
    # @return [Version]
    def ensure_version(name, description = nil)
      version = versions.select { |v| v.version == name }.first
      version ||= create_version(name, description)
      if description && (description != version.description)
        version.update(description)
      end
      version
    end

    # @param [Symbol]
    # @return [String]
    def param_name(param)
      # This needs to return strings, otherwise it won't match the JSON that
      # Vagrant Cloud returns.
      ATTR_MAP.fetch(param, param.to_s)
    end

    private

    # Constructs the box path based on an account and box name.
    # If no params are given, it constructs a path for *this* Box object,
    # but if both params are given it will construct a path for a one-off request
    #
    # @param [String] - username
    # @param [String] - box_name
    # @return [String] - API path to box
    def box_path(username = nil, box_name = nil)
      if username && box_name
        "/box/#{username}/#{box_name}"
      else
        "/box/#{account.username}/#{name}"
      end
    end

    # Vagrant Cloud returns keys different from what you set for some params.
    # Values in this map should be strings.
    ATTR_MAP = {
      is_private: 'private',
      description: 'description_markdown'
    }.freeze
  end
end
