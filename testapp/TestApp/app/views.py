from app import app

@app.route('/')
def api_entry():
        return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
        return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
        return 'Posting Traces'
