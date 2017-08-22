file {"/etc/dd-agent/checks.d/random_check.py":
  source => '/vagrant/files/random_check.py',
  notify => Service[datadog-agent]
}

file {"/etc/dd-agent/conf.d/random_check.yaml":
  source => '/vagrant/files/random_check.yaml',
  notify => Service[datadog-agent]
}

service {"datadog-agent":
  ensure => running
}
