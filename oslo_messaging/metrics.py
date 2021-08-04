import logging
import threading, queue
import statsd

LOG = logging.getLogger(__name__)

class Metrics():
   def __init__(self, host, port):
      self._port = port
      self.queue = queue.Queue()
      self.statsd = statsd.StatsClient(host, port)

   def start(self):
      # gets killed once the main process exits
      threading.Thread(target=self.counter, daemon=True).start()

   def counter(self):
      while True:
         try:
            incoming = self.queue.get()
            message = incoming['message'].message

            method = message.get('method')
            stat = "oslo.messaging.{}.{}".format(method, incoming['tag'])
            self.statsd.incr(stat)
            self.queue.task_done()
         except Exception:
            LOG.exception('Exception during message metrics handling')