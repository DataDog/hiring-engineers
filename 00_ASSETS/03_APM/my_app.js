const tracer = require('dd-trace').init({
  debug: true
})
const span = tracer.startSpan('web.request')

span.setTag('http.url', '/login')
span.finish()
