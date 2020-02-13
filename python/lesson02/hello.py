import sys
import opentracing
import logging
import jaeger_client
import time

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = jaeger_client.Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    return config.initialize_tracer()

tracer = init_tracer('hello-world')

def format_string(hello_to):
    with tracer.start_active_span('format') as scope:
        hello_str = 'Hello, %s!' % hello_to
        scope.span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def print_hello(hello_str):
    with tracer.start_active_span('println') as scope:
        print(hello_str)
        scope.span.log_kv({'event': 'println'})

def say_hello(hello_to):
    with tracer.start_active_span('say-hello') as scope:
        scope.span.set_tag('hello-to', hello_to)
        hello_str = format_string(hello_to)
        print_hello(hello_str)

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)

time.sleep(2)
tracer.close()
