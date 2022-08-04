# from opentelemetry import trace
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# provider = TracerProvider()
# processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor)
# trace.set_tracer_provider(provider)
# tracer = trace.get_tracer(__name__)

from flask import Flask, request
from collections import defaultdict

import requests

app = Flask(__name__)
CACHE = defaultdict(int)

@app.route("/")
def fetch():
  # with tracer.start_as_current_span(
  #     "server_request",
  #     attributes={ "endpoint": "/" } 
  # ):
  url = request.args.get("url")
  CACHE[url] += 1
  resp = requests.get(url)
  return resp.content

@app.route("/cache")
def cache():
  keys = CACHE.keys()
  return "{}".format(keys)

if __name__ == "__main__":
  app.run()