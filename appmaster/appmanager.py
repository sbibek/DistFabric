from appstore.registry import apps

class DfAppManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def getApps(self):
        return apps
    
    def invokeApp(self, meta, onComplete, onError):
        # meta {'app': name of app, arguments:...}
        if meta['app'] not in apps:
            self.logger.info('app {} not found!!'.format(meta['app'])) 
            onError("app not found")
        else:
            def __onComplete(response): onComplete(meta, response)
            app = apps[meta['app']]['instance']
            app.run(app.formatArguments(meta['args']), self.config["whoAmI"],self.config["sync"]["dir"], __onComplete, self.logger)
    
    def invokeAppResultsProcessor(self, app, result):
        app = apps[app]['instance']
        return app.processResults(result)

    def invokeAppLogResults(self, app, result, timeTaken):
        app = apps[app]['instance']
        return app.logResults(result, timeTaken, self.config["logDir"])
    
    def invokeAppArgumentsProcessor(self, app, args):
        if app not in apps:
            return None
        else:
            t = apps[app]['instance'].prepareArguments(args, self.config)
            if t is None:
                return None
            return apps[app]['instance'].distributeTasks(t, self.config["nodes"])
    