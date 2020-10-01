import cmd

class DfCommander(cmd.Cmd):

    prompt = '> '

    def __init__(self, orchestrator, config, logger):
        cmd.Cmd.__init__(self)
        self.orchestrator = orchestrator
        self.config = config
        self.logger = logger
    
    def do_ls(self, args):
        print("\nInstalled Apps")
        apps = self.orchestrator.getApps()
        i = 1 
        for app in apps:
            print('{}. {} ({})'.format(i, app, apps[app]['description'] ))
            i = i + 1
        print()

    def do_sync(self, args):
        "sync the shared directory between all the nodes and master"
        self.orchestrator.performSync()

    def do_invoke(self, args):
        "invoke the app in all the nodes. Usage invoke $app $args"
        _args = args.split()
        self.orchestrator.invokeApp(_args[0], _args[1:])
    
    def do_exit(self,args):
        return True