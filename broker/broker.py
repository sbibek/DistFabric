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
            _d = body.decode('utf-8')
            if len(_d) == 0: return
            self.callback(json.loads(_d))
        
        def run(self):
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
        # message to master should be especially marked
        # if instance is master, only related data would be passed on above
        if data['to'] == '*' and self.config['whoAmI'] == 'MASTER':
            return;

        # the broker will send the data upstream if only the configuration says its appropriate
        if data['to'] == '*' or data['to'] == self.config['whoAmI']:
            self.callback(data)
    
    def sendToMaster(self, message):
        payload = {"to": 'MASTER', "from":self.config['whoAmI'],"action":"RESPONSE", "message": message}
        self.sender.sendToNodes(payload)
    
    def broadcast(self, message):
        payload = {"to": '*', "from":self.config['whoAmI'], "message": message}
        self.sender.sendToNodes(payload)
    
    def send(self, to, message):
        payload = {"to": to, "from":self.config['whoAmI'], "message": message}
        self.sender.sendToNodes(payload)
    