module VagrantCloud
  class Version
    attr_accessor :box
    attr_accessor :number

    # @param [Box] box
    # @param [String] number
    # @param [Hash] data
    # @param [String] description
    # @param [String] access_token
    def initialize(box, number, data = nil, description = nil, access_token = nil, custom_server = nil)
      @box = box
      @number = number
      @data = data
      @description = description
      @client = Client.new(access_token, custom_server)
    end

    #--------------------
    # Metadata Helpers
    #--------------------

    # @return [String]
    def version
      data['version'].to_s
    end

    # @return [String]
    def description
      data['description_markdown'].to_s
    end

    # @return [String]
    def status
      data['status'].to_s
    end

    # @return [Array<Provider>]
    def providers
      data['providers'].map { |data| Provider.new(self, data['name'], data) }
    end

    # @return [String]
    def to_s
      version
    end

    #--------------------
    # Version API Helpers
    #--------------------

    # @return [Hash]
    def data
      @data ||= @client.request('get', version_path)
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @return [Hash]
    def read(username = nil, box_name = nil, version_number = nil)
      @client.request('get', version_path(username, box_name, version_number))
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @param [String] description
    def update(description = nil, username = nil, box_name = nil, version_number = nil)
      update_data = !(username && box_name && version_number)
      description ||= @description
      version = { description: description }
      data = @client.request('put',
                             version_path(username, box_name, version_number),
                             version: version)

      @data = data if update_data
      data
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    def delete(username = nil, box_name = nil, version_number = nil)
      @client.request('delete', version_path(username, box_name, version_number))
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    def release(username = nil, box_name = nil, version_number = nil)
      data = @client.request('put', "#{version_path(username, box_name, version_number)}/release")

      @data = data if !(username && box_name && version_number)
      data
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    def revoke(username = nil, box_name = nil, version_number = nil)
      update_data = !(username && box_name && version_number)
      data = @client.request('put', "#{version_path(username, box_name, version_number)}/revoke")

      @data = data if update_data
      data
    end

    # @param [String] number
    # @param [String] description
    # @param [String] org
    # @param [String] box_name
    # @return [Hash]
    def create_version(number = nil, description = nil, org = nil, box_name = nil)
      update_data = !(org && box_name && description && number)
      number ||= @number
      description ||= @description

      params = { version: number, description: description }
      data = @client.request('post', create_version_path(org, box_name).to_s, version: params)

      @data = data if update_data
      data
    end

    #--------------------
    # Old Provider Helpers
    #--------------------

    # @param [String] name
    # @param [Hash] data
    # @return [Provider]
    def get_provider(name, data = nil)
      Provider.new(self, name, data)
    end

    # @param [String] name
    # @param [String] url
    # @return [Provider]
    def create_provider(name, url = nil)
      params = { name: name, url: url }.delete_if { |_, v| v.nil? }
      data = @client.request('post', "#{version_path}/providers", provider: params)
      get_provider(name, data)
    end

    # @param [String] name
    # @param [String] url
    # @return [Provider]
    def ensure_provider(name, url)
      provider = providers.select { |p| p.name == name }.first
      provider ||= create_provider(name, url)
      provider.update(url) if url != provider.url
      provider
    end

    private

    # @return [Account]
    def account
      box.account
    end

    # Path used to generate a new version on a box
    #
    # @param [String] - username
    # @param [String] - box_name
    # @return [String]
    def create_version_path(username = nil, box_name = nil)
      if username && box_name
        "/box/#{username}/#{box_name}/versions"
      else
        "/box/#{account.username}/#{box.name}/versions"
      end
    end

    # @param [String] - username
    # @param [String] - box_name
    # @param [String] - version_number
    # @return [String]
    def version_path(username = nil, box_name = nil, version_number = nil)
      if username && box_name && version_number
        "/box/#{username}/#{box_name}/version/#{version_number}"
      else
        "/box/#{account.username}/#{box.name}/version/#{number}"
      end
    end
  end
end
