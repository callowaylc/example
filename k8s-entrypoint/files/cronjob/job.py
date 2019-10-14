#!/usr/bin/env python
""" Example job
    An example of job workflow, ran from a python base
    image, that sleeps for ~10 seconds as a simulation
    of process expense
"""
import os
import sys
import traceback
import random
import time
import datetime

from prometheus_client import start_http_server, Counter, Gauge

from logger import debug, info, warn, error

## constants ####################################

EXIT_STATUS_ERROR = 1
PORT = 9012

## main #########################################

def main(arguments):
  debug("Enter", { "arguments": arguments, })

  start = datetime.datetime.now()
  port = os.environ.get("PORT", 9012)
  labels = {
    "id": os.environ.get("ID"),
    "name": os.environ.get("NAME")
  }
  up = Gauge("job_up", "Job heartbeat", labels.keys())
  duration = Gauge("job_duration", "Job duration", labels.keys())
  c = Counter("job_init_total", "Job init count", labels.keys())
  delta = 0

  # increment the job init counter
  c.labels(*labels.values()).inc()

  # start metrics exporter
  debug("Start metrics server", { "port": port })
  start_http_server(int(port))

  # sleep random time between 5,10 seconds to simulate
  # long running operations
  time.sleep(random.randint(5, 10))
  delta = datetime.datetime.now() - start

  # set duration and wait for scrape event and exit
  duration.labels(*labels.values()).set(delta.seconds)

  debug("Exit", { "arguments": arguments, })

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))

    except Exception as e:
        traceback.print_exc()
        error("Unhandled exception", { "error": str(e) })
        sys.exit(EXIT_STATUS_ERROR)