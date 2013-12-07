#!/usr/local/bin/python
import sys
from Components.ConfigReader import ConfigReader
from Components.Logger import Logger


__author__ = 'Denis'
__directoriesConfig__ = "directories.cfg"

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
        self.__logger.log("Reading directories config: " + __directoriesConfig__)
        configReader = ConfigReader(__directoriesConfig__, "=>")
        directories = configReader.getTuples()
        self.__logger.log("Directories to be backed up: " + str(len(directories)))
        self.__logger.log("Starting backup process")
        for i in range(0, len(directories)):
            self.processDirectoryRecursively("/", directories[i][0], directories[i][1])

    def processDirectoryRecursively(self, currentDirectory, sourceRoot, destinationRoot):
        print(sourceRoot + "==>" + destinationRoot)



if __name__ == "__main__":
    Program().start()
