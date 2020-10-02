class DfApp:
    def run(self, arguments, onComplete):
       onComplete() 
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return result

    # only invoked by the master 
    def prepareArguments(self, args):
        return args