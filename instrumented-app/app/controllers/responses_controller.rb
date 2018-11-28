class ResponsesController < ApplicationController

  def index
    response = 'Entrypoint to the Application'
    render json: response, status: 200
  end

  def apm
    response = 'Getting APM Started'
    render json: response, status: 200
  end

  def trace
    response = 'Posting Traces'
    render json: response, status: 200
  end

end
