Rails.application.routes.draw do
  get '/', to: 'api#index'
  get 'api/apm'
  get 'api/trace'
end
