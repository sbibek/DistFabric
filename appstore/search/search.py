from appmaster.app import DfApp
from utils.filereader import readTextFile
from os import path

class DfSearchApp(DfApp):

    def run(self, args, onComplete, logger):
        logger.info("DfSearchApp({})".format(args))
        onComplete(['result1', 'result2'])
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return results
    
    def prepareArguments(self, args, config):
        # there are two argments, we will parse the 2nd argument to the file list
        wordlist = readTextFile(args[1]) 
        if wordlist == None:
            print("DfSearchApp::file {} not found!!".format(args[1]))
            return None
        
        if not path.exists('{}{}'.format(config['sync']['dir'], args[0])):
            printf("DfSearchApp::dir {} not found!!".format(args[0]))
            return None
        
        return [args[0], wordlist.strip().split('\n')]