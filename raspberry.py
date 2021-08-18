import threading

class RaspberryThread(threading.Thread):
    def __init__(self, function):
        
        self.paused = True
        self.state = threading.Condition()
        self.function = function
        super(RaspberryThread, self).__init__()
        
    def start(self):
        super(RaspberryThread, self).start()
    
    def run(self):
        
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()
            while not self.paused:
                self.function()
    
    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()
    
    def pause(self):
        with self.state:
            self.paused = True