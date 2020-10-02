from appmaster.app import DfApp

class DfSearchApp(DfApp):
    def run(self, args, onComplete, logger):
        logger.info("DfSearchApp({})".format(args))
        onComplete(['result1', 'result2'])
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return results
    
    def prepareArguments(self, args):
        return args
