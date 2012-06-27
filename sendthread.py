import multiprocessing
from pynsca import NSCANotifier
import re

class SendThread(multiprocessing.Process):
    def __init__(self, id, queue, nsca_host, nsca_port=5667, nsca_crypt=1, password=None):
        print "Initialized SendThread id " + str(id)
        self.quit = False
        self.id = id
        self.queue = queue
        self.nsca = NSCANotifier(nsca_host, monitoring_port=nsca_port, encryption_mode=nsca_crypt, password=password)

        multiprocessing.Process.__init__(self)

    def run(self):
        print "Running SendThread id " + str(id)
        while self.quit is False:
            line = self.queue.get()
            print str(self.id) + " | Received event: " + str(line)
            (host, service, code, output) = self.parse(line)
            print host + " " + service + " " + str(code) + " " + output
            self.nsca.svc_result(host, service, code, output)

    def parse(self, line):
        r = re.match(r'(?P<time>[0-9]+)\sPROCESS_SERVICE_CHECK_RESULT;(?P<host>\S+);(?P<service>\S+);(?P<code>[0-9]+);(?P<output>.+)\n', line)
        return (r.group("host"), r.group("service"), int(r.group("code")), r.group("output"))
