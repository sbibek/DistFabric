from appmaster.appmanager import DfAppManager
import time

class DfOrchestrator:
    def __init__(self, config, logger, broker, sync):
        self.config = config
        self.logger = logger
        self.borker = broker
        self.sync = sync
        self.appmanager = DfAppManager(config, logger)

        # location to hold current app invokes
        # we always will allow just one invoke for now
        self.process = {'state':'idle', 'results': []}
    
    def processMsg(self, payload):
        # check if this master only message
        # this hook will be called only if this instance is master
        if payload['to'] == 'MASTER':
            self.__processMasterOnlyMessage(payload);
            return
        
        message = payload['message']

        # here all actions are non master only
        if message['action'] == 'EXEC_APP':
            self.appmanager.invokeApp({"app": message['app'],"args": message['args']}, self.__onAppInvokeSuccessfullyCompleted, self.__onAppInvokeFailed)
        else:
            self.logger.info("Orchestrator was unable to find action {}".format(message['action']))
    
    def __onAppInvokeSuccessfullyCompleted(self, originalMessage, result):
        self.logger.info('invoke successful response: {}'.format(result))
        # on every successful invoke, the messge will be sent to master
        self.borker.sendToMaster({"args": originalMessage, "result": result})


    def __onAppInvokeFailed(self, originalMessage, result):
        pass

    def __processMasterOnlyMessage(self, message):
        # self.logger.info("got master only message {}".format(message))
        if message['action'] == 'RESPONSE':
            self.process['results'].append(message['message'])
        
        if len(self.process['results']) >= len(self.config['nodes']):
            self.process['state'] = 'complete'


    def orchestrate(self):
        self.borker.startReceiver(self.processMsg)

    def getApps(self):
        return self.appmanager.getApps()
    
    def performSync(self):
        self.sync.sync()

    def invokeApp(self, app, args):
        self.borker.broadcast({"action":"EXEC_APP", "app":app, "args":args})
        self.process['state'] = 'running'
        results = self.__waitfForResults()
        print(results)
    
    def __waitfForResults(self):
        # this is called after each of the invoke, this will mandatorily make the master wait for 
        # the responses before doing anything
        while self.process['state'] != 'complete':
            time.sleep(1)
        
        # if we are here means the state is complete
        self.process['state'] = 'idle'
        res = self.process['results']
        self.process['results'] = []
        return res
