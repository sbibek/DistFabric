from appmaster.app import DfApp
from utils.filereader import readTextFile
from os import path
from utils.grep import grep

class DfSearchApp(DfApp):

    def run(self, args, whoAmI, dir, onComplete, logger):
        # logger.info("DfSearchApp({})".format(args[whoAmI]))
        myArgs = args[whoAmI]
        results = []
        _dir = '{}{}'.format(dir, myArgs[0])
        for keyword in myArgs[1]:
           results[keyword] = grep(_dir, keyword)
        onComplete(results)
    
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
            print("DfSearchApp::dir {} not found!!".format(args[0]))
            return None
        
        return [args[0], wordlist.strip().split('\n')]

    def distributeTasks(self, _args, nodes):
        args = _args[1]
        totalNodes = len(nodes)
        totalKeywords = len(args)
        keywordsPerNode =  totalKeywords//totalNodes
        firstNodeKeywordsLen = keywordsPerNode + (totalKeywords - keywordsPerNode * totalNodes)
        isFirst = True
        fargs = {} 
        for node in nodes:
            if isFirst:
                fargs[node["id"]] = [ _args[0], args[:firstNodeKeywordsLen]]
                args = args[firstNodeKeywordsLen:]
                isFirst = False
            else:
                fargs[node["id"]] = [_args[0], args[:keywordsPerNode]]
                args = args[keywordsPerNode:]
        return fargs

