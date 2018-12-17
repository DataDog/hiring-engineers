require 'test_helper'

class ApiControllerTest < ActionDispatch::IntegrationTest
  test "should get apm" do
    get api_apm_url
    assert_response :success
  end

  test "should get trace" do
    get api_trace_url
    assert_response :success
  end

end
