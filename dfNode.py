from config.conf import getConf
from utils.logger import DfLogger
from sync import DfSync
from communication.receiver import DfReceiver

if __name__ == '__main__':
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfComm = DfReceiver(config)
    dfComm.start()