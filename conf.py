import json

__isLoaded = False
conf = {}

def __load():
    global conf
    with open('conf.json') as conf_file:
        conf = json.load(conf_file)
    __isLoaded = True


# get conf
def getConf():
    if __isLoaded:
        return conf
    else:
        __load()
        return conf
