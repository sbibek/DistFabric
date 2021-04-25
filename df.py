from config.conf import getConf
from utils.logger import DfLogger
from sync.sync import DfSync
from broker.broker import DfBroker
from orchestrator.orchestrator import DfOrchestrator
from master.commander import DfCommander
import pyfiglet


if __name__ == '__main__':
    df = pyfiglet.figlet_format("DistFabric")
    print(df)
    print("V 1.0")
    config = getConf()
    logger = DfLogger()
    dfsync = DfSync(config, logger)
    dfbroker = DfBroker(config, logger)
    dforchestrator = DfOrchestrator(config, logger, dfbroker, dfsync)    
    dforchestrator.orchestrate()

    if config['whoAmI'] == 'MASTER':
        print("I am master, dropping to command console (type help for help)\n")
        DfCommander(dforchestrator, config, logger).cmdloop()
    else:
        print("I am node {}, waiting for MASTER to issue commands".format(config["whoAmI"]))
