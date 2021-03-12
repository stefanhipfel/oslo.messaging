import logging
import sys
import functools
import threading
import statsd

LOG = logging.getLogger(__name__)

def threaded(fn):
   def wrapper(*args, **kwargs):
      thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
      thread.start()
      return thread
   return wrapper

class Metrics():
   def __init__(self, host, port):
      self._port = port
      self.statsd = statsd.StatsClient(host, port)

   @threaded
   def counter(self, incoming, tag):
      method = incoming.message.get('method')
      stat = "{}.{}".format(tag, method)
      self.statsd.incr(stat)