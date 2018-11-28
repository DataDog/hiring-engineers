Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  get '/', to: 'responses#index'
  get '/api/apm', to: 'responses#apm'
  get '/api/trace', to: 'responses#trace'

end
