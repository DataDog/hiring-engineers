module VagrantCloud
  class Search
    attr_accessor :account

    def initialize(access_token = nil, custom_server = nil)
      @client = Client.new(access_token, custom_server)
    end

    # Requests a search based on the given parameters
    #
    # @param [String] query
    # @param [String] provider
    # @param [String] sort
    # @param [String] order
    # @param [String] limit
    # @param [String] page
    # @return [Hash]
    def search(query = nil, provider = nil, sort = nil, order = nil, limit = nil, page = nil)
      params = {
        q: query,
        provider: provider,
        sort: sort,
        order: order,
        limit: limit,
        page: page
      }.delete_if { |_, v| v.nil? }

      @client.request('get', '/search', params)
    end
  end
end
