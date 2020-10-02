def readTextFile(path):
    try:
        f = open(path, 'r')
        return f.read()
    except:
        return None