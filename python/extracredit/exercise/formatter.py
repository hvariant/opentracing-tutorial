from flask import Flask
from flask import request
from lib.tracing import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
from flask_opentracing import FlaskTracing

app = Flask(__name__)
opentracing_tracer = init_tracer('formatter')
tracing = FlaskTracing(opentracing_tracer, True, app)

@app.route("/format")
def format():
    current_span = tracing.get_span(request)
    greeting = current_span.get_baggage_item('greeting')
    if not greeting:
        greeting = 'Hello'
    hello_to = request.args.get('helloTo')
    return '%s, %s!' % (greeting, hello_to)

if __name__ == "__main__":
    app.run(port=8081)
