module VagrantCloud
  class ClientError < StandardError
    attr_accessor :error_arr
    attr_accessor :error_code

    def initialize(msg, http_body, http_code)
      begin
        errors = JSON.parse(http_body)
        vagrant_cloud_msg = errors['errors']

        if vagrant_cloud_msg.is_a?(Array)
          message = msg + ' - ' + vagrant_cloud_msg.join(', ').to_s
        else
          message = msg + ' - ' + vagrant_cloud_msg
        end
      rescue JSON::ParserError
        message = msg
      end

      @error_arr = vagrant_cloud_msg
      @error_code = http_code
      super(message)
    end
  end
end
