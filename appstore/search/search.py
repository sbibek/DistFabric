from appmaster.app import DfApp
from utils.filereader import readTextFile

class DfSearchApp(DfApp):
    def run(self, args, onComplete, logger):
        logger.info("DfSearchApp({})".format(args))
        onComplete(['result1', 'result2'])
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return results
    
    def prepareArguments(self, args):
        # there are two argments, we will parse the 2nd argument to the file list
        wordlist = readTextFile(args[1]) 
        if wordlist == None:
            print("DfSearchApp::file {} not found!!".format(args[1]))
            return None
        
        return [args[0], wordlist.strip().split('\n')]