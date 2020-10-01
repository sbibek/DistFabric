from conf import getConf
from logger import DfLogger
from sync import DfSync


if __name__ == '__main__':
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfsync.sync()