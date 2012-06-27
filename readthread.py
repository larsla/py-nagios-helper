import multiprocessing

class ReadThread(multiprocessing.Process):
    def __init__(self, id, fifoname, queue):
        print "Initialized ReadThread id " + str(id)
        self.quit = False
        self.id = id
        self.fifoname = fifoname
        self.queue = queue

        multiprocessing.Process.__init__(self)

    def run(self):
        print "Running ReadThread id " + str(id)
        self.f = open(self.fifoname, 'r')
        while self.quit is False:
            line = self.f.readline()
            if not '\n' in line: continue
            if not 'PROCESS_SERVICE_CHECK_RESULT' in line: continue
            print str(self.id) + " | Putting event on queue: " + str(line)
            self.queue.put(line)

    def quit(self):
        self.quit = True


