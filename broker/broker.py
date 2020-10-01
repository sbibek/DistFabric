from communication.sender import DfSender
from communication.receiver import DfReceiver
import threading
import json

class DfBroker:

    class ReceiverThread(threading.Thread):
        def __init__(self, config, logger, callback):
            threading.Thread.__init__(self)
            self.logger = logger
            self.callback = callback
            self.receiver = DfReceiver(config, self.onMessage)
        
        def onMessage(self, body):
            data = json.loads(body.decode('utf-8'))
            self.callback(data)
        
        def run(self):
            self.logger.info("started broker receiver")
            self.receiver.start()


    def __init__(self,config, logger):
        self.config = config
        self.logger = logger
        self.sender = DfSender(config)
        self.recever = DfBroker.ReceiverThread(config, logger, self.onMessage)

    def startReceiver(self, callback):
        self.callback = callback
        self.recever.start()

    def onMessage(self, data):
        print(data)
        self.callback(data)
    
    ## TODO broker knows how to talok, this is the main part of the implementation of the broker
