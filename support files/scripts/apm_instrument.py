from ddtrace import tracer

with tracer.trace("apm.basics", service="apm_services") as span:
  span.set_tag("role", "exercise")