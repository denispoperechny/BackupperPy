import os
import time

__author__ = 'Denis'


class Logger(object):

    __destDirectory = ""

    def __init__(self, logRoot):
        self.__init__(logRoot, time.strftime("%d.%m.%Y_%H.%M.%S"))

    def __init__(self, logRoot, timeStamp):
        self.__destDirectory = os.path.join(logRoot, timeStamp)
        if not os.path.exists(self.__destDirectory):
            os.makedirs(self.__destDirectory)

    def log(self, message):
        timeStamp = time.strftime("%H:%M:%S")
        line = timeStamp + " - " + message
        print(line)
        self.__writeLineToFile("log.txt", line)

    def logIgnoredObject(self, path):
        self.__writeLineToFile("skipped.txt", path)

    # Objects which presented at backup directory but not existed at source
    def logObsoleteObject(self, path):
        self.__writeLineToFile("obsolete.txt", path)

    def __writeLineToFile(self, file, line):
        logFilePath = os.path.join(self.__destDirectory, file)
        with open(logFilePath, 'a') as f:
            f.write(line + "\n")