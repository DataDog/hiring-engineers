Rails.configuration.datadog_trace = {
  ebabled: true,
  auto_instrument: true,
  auto_instrument_redis: true,
  auto_instrument_grape: true,
  default_service: 'my-rails-app',
  default_controller_service: 'my-rails-controller',
  default_cache_service: 'my-rails-cache',
  default_database_service: 'my-database',
  template_base_path: 'views/',
  tracer: Datadog.tracer,
  debug: false,
  trace_agent_port: 8126,
  env: nil,
  tags: {}
}
