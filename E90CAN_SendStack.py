
class SendStack():

    stack = []

    def __init__(self, bus):
        self.bus = bus
    

        
    
    def send(self, message):
        self.stack.append(message)
    
    def trySend(self):
        for message in self.stack:
            try:
                self.bus.send(message)
            except:
                print("Message not sent")
            else:
                self.stack.remove(message)


        
