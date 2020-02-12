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

def say_hello(hello_to):
    with tracer.start_span('say-hello') as span:
        span.set_tag('hello-to', hello_to)

        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})

        print(hello_str)
        span.log_kv({'event': 'println'})

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)

time.sleep(2)
tracer.close()
