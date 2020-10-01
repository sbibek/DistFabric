from config.conf import getConf
from utils.logger import DfLogger
from sync.sync import DfSync
from broker.broker import DfBroker
from orchestrator.orchestrator import DfOrchestrator
from master.commander import DfCommander

if __name__ == '__main__':
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfbroker = DfBroker(config, logger)
    dforchestrator = DfOrchestrator(config, logger, dfbroker, dfsync)    
    dforchestrator.orchestrate()

    if config['whoAmI'] == 'MASTER':
        DfCommander(dforchestrator, config, logger).cmdloop()
