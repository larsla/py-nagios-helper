import multiprocessing
from pynsca import NSCANotifier
import socket
import re
import time

class SendThread(multiprocessing.Process):
    def __init__(self, id, queue, nsca_host, nsca_port=5667, nsca_crypt=1, password=None, debug=False):
        print "Initialized SendThread id %i" % id
        self.quit = False
        self.tid = id
        self.queue = queue
        self.nsca = NSCANotifier(nsca_host, monitoring_port=nsca_port, encryption_mode=nsca_crypt, password=password)
        self.debug = debug

        multiprocessing.Process.__init__(self)

    def run(self):
        print "%i | Running SendThread" % self.tid
        while self.quit is False:
            if self.queue.empty():
                time.sleep(1)
                continue
            else:
                line = self.queue.get()
                if self.debug:
                    print "Line from queue: %s" % line

            parsed = self.parse(line.replace('[', '').replace(']', ''))
            if parsed:
                (t, host, service, code, output) = parsed
            else:
                continue
            if t > (int(time.time()) - 60):
                r = self.nsca.svc_result(host, service, code, output)
                if self.debug:
                    print "Line sent: %s" % line
                if not r:
                    print "Socket error, putting event back on queue and sleeping for a while. Error was: %s" % str(r)
                    self.queue.put(line)
                    time.sleep(1)
            else:
                #print str(self.tid) + " | " + str(t) + " " + host + ";" + service + ";" + str(code) + ";" + output + " | Too old, dropping"
                print "%i | %i %s;%s;%i;%s | Too old, dropping" % (self.tid, t,host,service,code,output)
            time.sleep(0.001)
        print "%i | Stopping loop" % self.tid

    def parse(self, line):
        try:
            r = re.match(r'(?P<time>[0-9]+)\sPROCESS_SERVICE_CHECK_RESULT;(?P<host>\S+);(?P<service>\S+);(?P<code>[0-9]+);(?P<output>.+)\n', line)
            return (int(r.group("time")), r.group("host"), r.group("service"), int(r.group("code")), r.group("output"))
        except AttributeError:
            print "AttributeError while parsing line: %s" % line
            return False

    def quit(self):
        self.quit = True
