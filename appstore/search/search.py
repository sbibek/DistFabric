from appmaster.app import DfApp
from utils.filereader import readTextFile
from os import path
from utils.grep import grep
from terminaltables import AsciiTable
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class DfSearchApp(DfApp):

    def run(self, args, whoAmI, dir, onComplete, logger):
        # logger.info("DfSearchApp({})".format(args[whoAmI]))
        myArgs = args[whoAmI]
        logger.info("Search(..) invoked")
        results = {} 
        _dir = '{}{}'.format(dir, myArgs[0])
        for keyword in myArgs[1]:
           results[keyword] = grep(_dir, keyword)
        logger.info("{} keywords searched".format(len(results)))
        onComplete(results)
    
    def formatArguments(self, args):
        return args

    def processResults(self, results):
        return results
    
    def __filef(self, files):
        result = ""
        for file in files:
            result += "{}({}), ".format(file, files[file])
        return result
    
    def __dumpResult(self, logdir, data):
        logfile = "{}search_{}.txt".format(logdir, get_random_string(5))
        f = open(logfile, 'w')
        for row in data:
            f.write("{}, {}, {}\n".format(row[0], row[1], row[2]))
        f.close()
        return logfile



    def logResults(self, results, timeTaken, logdir):
        tableData = [
        ]

        log = {}

        for row in results:
            r = row['result']
            for keyword in r:
                if keyword not in log:
                    log[keyword] = {'total_results': len(r[keyword]), 'files':{}}

                for row in r[keyword]:
                    file = row[0].split('/')[-1]
                    _rr = [keyword, "{}:{}".format(file, row[1]), row[2]]
                    tableData.append(_rr)

                    if file not in log[keyword]['files']:
                        log[keyword]['files'][file] = 1 
                    else:
                        log[keyword]['files'][file] += 1
        
        table = [['keyword', 'total hits', 'files']]
        for l in log:
            r = [l, log[l]['total_results'], self.__filef(log[l]['files']) ]
            table.append(r)
        t = AsciiTable(table)
        print(t.table)
        print("Time taken: {}s".format(round(timeTaken,2)))
        _fd = self.__dumpResult(logdir, tableData)
        print("Detailed results available at '{}'".format(_fd))

        # for row in tableData:
        #     print("{}, {}, {}".format(row[0], row[1], row[2])) 

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

