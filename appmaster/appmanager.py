from appstore.registry import apps

class DfAppManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def invokeApp(self, meta, onComplete, onError):
        # meta {'app': name of app, arguments:...}
        if meta['app'] not in apps:
            self.logger.info('app {} not found!!'.format(meta['app'])) 
            onError(-1)
        else:
            def __onComplete(response): onComplete(meta, response)
            app = apps[meta['app']]
            app.run(meta['args'], __onComplete, self.logger)