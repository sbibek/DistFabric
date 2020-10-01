from config.conf import getConf
from utils.logger import DfLogger
from sync import DfSync
from broker.broker import DfBroker


if __name__ == '__main__':
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfbroker = DfBroker(config, logger)
