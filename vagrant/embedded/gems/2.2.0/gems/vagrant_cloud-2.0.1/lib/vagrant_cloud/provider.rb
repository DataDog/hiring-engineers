module VagrantCloud
  class Provider
    attr_accessor :version
    attr_accessor :name

    # @param [Version] version
    # @param [String] name
    # @param [Hash] data
    # @param [String] access_token
    def initialize(version, name, data = nil, url = nil, username = nil, box_name = nil, access_token = nil, custom_server = nil)
      @version = version
      @name = name
      @data = data
      @username = username
      @box_name = box_name
      @url = url
      @client = Client.new(access_token, custom_server)
    end

    #--------------------
    # Metadata Helpers
    #--------------------

    # @return [String]
    def url
      data['original_url'].to_s
    end

    # @return [String]
    def download_url
      data['download_url'].to_s
    end

    #--------------------
    # Provider API Helpers
    #--------------------

    # @return [Hash]
    def data
      @data ||= @client.request('get', provider_path)
    end

    # Creates a provider for *this* Provider object, or if all params are given,
    # will make a one-off request to create a Provider and return its data
    #
    # @param [String] name
    # @param [String] url
    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    def create_provider(name = nil, url = nil, username = nil, box_name = nil, version_number = nil)
      update_data = !(username && version_number && provider_name && box_name)
      name ||= @name
      url ||= @url
      username ||= @username
      box_name ||= @box_name
      version_number ||= @version

      params = { name: name, url: url }.delete_if { |_, v| v.nil? }
      data = @client.request('post', create_provider_path(username, box_name, version_number), provider: params)

      @data = data if update_data
      data
    end

    # @param [String] url
    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @param [String] provider_name
    def update(url = nil, username = nil, box_name = nil, version_number = nil, provider_name = nil)
      update_data = !(username && version_number && provider_name && box_name)
      provider_name ||= @name
      url ||= @url
      username ||= @username
      box_name ||= @box_name
      version_number ||= @version

      params = { url: url }
      data = @client.request('put',
                             provider_path(username, box_name, version_number, provider_name),
                             provider: params)

      @data = data if update_data
      data
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @param [String] provider_name
    def delete(username = nil, box_name = nil, version_number = nil, provider_name = nil)
      @client.request('delete', provider_path(username, box_name, version_number, provider_name))
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @param [String] provider_name
    # @return [String]
    def upload_url(username = nil, box_name = nil, version_number = nil, provider_name = nil)
      @client.request('get', "#{provider_path(username, box_name, version_number, provider_name)}/upload")['upload_path']
    end

    # @param [String] username
    # @param [String] box_name
    # @param [String] version_number
    # @param [String] provider_name
    # @param [String] file_path
    def upload_file(file_path, username = nil, box_name = nil, version_number = nil, provider_name = nil)
      url = upload_url(username, box_name, version_number, provider_name)
      payload = File.open(file_path, 'r')
      RestClient::Request.execute(
        method: :put,
        url: url,
        payload: payload,
        ssl_version: 'TLSv1'
      )
    end

    private

    # @return [Box]
    def box
      version.box
    end

    # @return [Account]
    def account
      box.account
    end

    def create_provider_path(username = nil, box_name = nil, version_number = nil)
      if username && box_name && version_number
        "/box/#{username}/#{box_name}/version/#{version_number}/providers"
      else
        "/box/#{account.username}/#{box.name}/version/#{version.number}/providers"
      end
    end

    def provider_path(username = nil, box_name = nil, version_number = nil, provider_name = nil)
      if username && box_name && version_number && name
        "/box/#{username}/#{box_name}/version/#{version_number}/provider/#{provider_name}"
      else
        "/box/#{account.username}/#{box.name}/version/#{version.number}/provider/#{name}"
      end
    end
  end
end
