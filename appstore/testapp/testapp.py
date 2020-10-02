from appmaster.app import DfApp

class TestApp(DfApp):
    def run(self, args, onComplete, logger):
        logger.info("invoking the test app with args {}".format(args))
        onComplete("done from test app")
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return results