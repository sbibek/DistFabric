import subprocess

# syncs the project shared folder
class DfSync:
    def __init__(self, options, logger):
        self.syncDir = options["sync"]["dir"] 
        self.nodes = options["nodes"]
        self.logger = logger

    def __rsync(self, nodeInfo):
        process = subprocess.Popen(['rsync', '-a', self.syncDir, '{}@{}:{}'.format(nodeInfo['user'], nodeInfo['host'], self.syncDir)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if len(stderr) is not 0:
            raise Exception('sync error for node {}'.format(nodeInfo['host']))
        self.logger.info('syncing {}..done'.format(nodeInfo['host']))
    
    def sync(self):
        self.logger.info("starting directory sync")
        for node in self.nodes:
            self.__rsync(node)
        self.logger.info('OK {} nodes synced'.format(len(self.nodes)))