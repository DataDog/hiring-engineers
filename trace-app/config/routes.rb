Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root :to => "application#index"
  get '/api/apm' => 'application#show'
  get '/api/trace' => 'trace#show'
end
