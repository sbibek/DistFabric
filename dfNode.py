from config.conf import getConf
from utils.logger import DfLogger
from sync.sync import DfSync
from communication.sender import DfSender

if __name__ == '__main__':
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfComm = DfSender(config)
    dfComm.sendToNodes({"to":"*", "action":"EXEC_APP", "app":"test", "args":"supp"})