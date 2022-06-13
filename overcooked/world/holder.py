class Holder:
    def __init__(self):
        self.object = None
        
    @property
    def empty(self):
        return self.object == None
    
    def get(self):
        obj = self.object
        self.object = None
        return obj
    
    def put(self, obj):
        self.object = obj
    
    def interact(self, holding):
        if holding is not None:
            self.put(holding)
        else:
            return self.get()

    def render(self, tile):
        if self.object:
            return self.object.render(tile)
