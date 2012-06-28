import multiprocessing
import time

class ReadThread(multiprocessing.Process):
    def __init__(self, id, fifoname, queue):
        print "Initialized ReadThread id " + str(id)
        self.quit = False
        self.tid = id
        self.fifoname = fifoname
        self.queue = queue

        multiprocessing.Process.__init__(self)

    def run(self):
        print str(self.tid) + "Running ReadThread id "
        self.f = open(self.fifoname, 'r')
        while self.quit is False:
            line = self.f.readline()
            if not '\n' in line:
                time.sleep(0.01)
                continue
            if not 'PROCESS_SERVICE_CHECK_RESULT' in line: continue
            while self.queue.full():
                time.sleep(1)
            self.queue.put(line)

    def quit(self):
        self.quit = True


