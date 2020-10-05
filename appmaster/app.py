class DfApp:
    def run(self, args, whoAmI, onComplete, logger):
       onComplete() 
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return result

    # only invoked by the master 
    def prepareArguments(self, args, config):
        return args
    
    def distributeTasks(self, _args, nodes):
        return _args