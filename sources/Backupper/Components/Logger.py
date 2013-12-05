import os
import time

__author__ = 'Denis'


class Logger(object):

    __logRoot = None

    def __init__(self, logRoot):
        timeStamp = time.strftime("%d.%m.%Y_%H.%M.%S")
        self.__logRoot = logRoot

        destDirectory = logRoot + "/" + timeStamp
        if not os.path.exists(destDirectory):
            os.makedirs(destDirectory)

        """
        Here create the log file
        """
        print(timeStamp)

    def testMethod(self):
        print('tested 11')