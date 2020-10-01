import datetime

class DfLogger:
    def info(self, message):
        currentts = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        print('[INFO] [{}] {}'.format(currentts, message))