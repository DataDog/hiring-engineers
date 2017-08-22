class {'postgresql::server':} ->

postgresql::server::role { 'datadog':
  password_hash => postgresql_password('datadog', lookup('datadog_agent::integrations::postgres::password'))
} ->

class {'datadog_agent::integrations::postgres':}
