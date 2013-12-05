#!/usr/local/bin/python
import sys
from Components.Logger import Logger


__author__ = 'Denis'

def unhandledExceptionUtilizer(type, value, traceback):
        logger = Logger('Logs')
        logger.log("Unhandled Exception")
        logger.log("Type:" + str(type))
        logger.log("Value:" + str(value))
        #TODO: log the traceback
        print("Traceback:" + traceback)
sys.excepthook = unhandledExceptionUtilizer

class Program(object):

    __logger = None

    def start(self):
        self.__logger = Logger('Logs')
        self.__logger.log("Starting")


if __name__ == "__main__":
    Program().start()
