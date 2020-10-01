from appmaster.appmanager import DfAppManager

class DfOrchestrator:
    def __init__(self, config, logger, broker):
        self.config = config
        self.logger = logger
        self.borker = broker
        self.appmanager = DfAppManager(config, logger)
    
    def processMsg(self, message):
        # check if this master only message
        # this hook will be called only if this instance is master
        if message['to'] == 'MASTER':
            self.__processMasterOnlyMessage(message);
            return

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
        self.logger.info("got master only message {}".format(message))


    def orchestrate(self):
        self.borker.startReceiver(self.processMsg)
