from overcooked.world.holder import Holder


class Processor(Holder):
    def __init__(self, processing_time):
        self.processing_time = processing_time
        self.processing = False
        self.time_left = 0
        super().__init__()
    
    def process(self, obj):
        raise NotImplementedError()
    
    def interact(self, holding):
        if holding is not None:
            if self.processing_time == 0:
                return self.process(holding)
            else:
                self.put(holding)
                self.processing = True
                self.time_left = self.processing_time
        else:
            if not self.empty and not self.processing:
                return self.get()
    
    def update(self):
        if self.processing:
            self.time_left -= 1
        
        if self.time_left == 0:
            self.processing = False
