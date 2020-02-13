from flask import Flask
from flask import request
from lib.tracing import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
from flask_opentracing import FlaskTracing

app = Flask(__name__)
opentracing_tracer = init_tracer('publisher')
tracing = FlaskTracing(opentracing_tracer, True, app)

@app.route("/publish")
def publish():
    hello_str = request.args.get('helloStr')
    print(hello_str)
    return 'published'

if __name__ == "__main__":
    app.run(port=8082)
