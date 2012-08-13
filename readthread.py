import multiprocessing
import time

class ReadThread(multiprocessing.Process):
    def __init__(self, id, fifoname, queue, debug=False):
        print "Initialized ReadThread id %i" % id
        self.quit = False
        self.tid = id
        self.fifoname = fifoname
        self.queue = queue
        self.debug = debug

        multiprocessing.Process.__init__(self)

    def run(self):
        print "%i | Running ReadThread" % self.tid
        self.f = open(self.fifoname, 'r')
        while self.quit is False:
            line = self.f.readline()
            if not '\n' in line:
                time.sleep(0.01)
                continue
            if not 'PROCESS_SERVICE_CHECK_RESULT' in line: continue
            if self.debug:
                print "Read line: %s" % line
            while self.queue.full():
                print "Queue full, sleeping"
                time.sleep(1)
            self.queue.put(line)

    def quit(self):
        self.quit = True


