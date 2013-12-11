##!/usr/local/bin/python
import os
from shutil import copyfile
import sys
from Components.ConfigReader import ConfigReader
from Components.Logger import Logger
from os import listdir
from os.path import isfile
import time

__author__ = 'Denis'
__appTimeStamp__ = time.strftime("%d.%m.%Y_%H.%M.%S")
__configs__ = None
__mainConfigFile__ = "backupper.cfg"
__timeLabel__ = ".last-backed-up"
__ignoreLabel__ = ".backup-ignore"
__scriptDir__ = os.path.dirname(os.path.realpath(__file__))


def unhandledExceptionUtilizer(type, value, traceback):
        logger = Logger(__configs__.getValuesByKey("logs")[0], __appTimeStamp__)
        logger.log("Unhandled Exception")
        logger.log("Type:" + str(type))
        logger.log("Value:" + str(value))
        #TODO: log the traceback
        print("Traceback:" + traceback)
sys.excepthook = unhandledExceptionUtilizer


class Program(object):

    __logger = None

    def start(self):
        self.__logger = Logger(__configs__.getValuesByKey("logs")[0], __appTimeStamp__)
        self.__logger.log("Starting")
        self.__logger.log("Reading directories config: " + __configs__.getValuesByKey("directories_config")[0])
        configReader = ConfigReader(__configs__.getValuesByKey("directories_config")[0], "=>")
        directories = configReader.getTuples()
        self.__logger.log("Directories to be backed up: " + str(len(directories)))
        self.__logger.log("Starting backup process")
        for i in range(0, len(directories)):
            self.__processDirectoryRecursively("", directories[i][0], directories[i][1])
            self.__logger.log("Directory backed up: " + directories[i][0])
            self.__updateLabel(directories[i][1])
        self.__logger.log("Backup finished")

    def __updateLabel(self, directory):
        labelPath = os.path.join(directory, __timeLabel__)
        if os.path.isfile(labelPath):
            os.remove(labelPath)
        with open(labelPath, 'a') as f:
            f.write(time.strftime("%d.%m.%Y %H:%M:%S"))

    def __processDirectoryRecursively(self, currentDirectory, sourceRoot, destinationRoot):
        sourceDir = os.path.join(sourceRoot, currentDirectory)
        destDir = os.path.join(destinationRoot, currentDirectory)

        # Skip directory if ignored
        if os.path.isfile(os.path.join(sourceDir, __ignoreLabel__)):
            self.__logger.logIgnoredObject(sourceDir)
            return

        # Create destination directory if needed
        if not os.path.exists(destDir):
            os.makedirs(destDir)

        self.__checkObsoleteFiles(destDir, sourceDir)

        onlyfiles = [f for f in listdir(sourceDir) if isfile(os.path.join(sourceDir, f))]
        directories = [f for f in listdir(sourceDir) if not isfile(os.path.join(sourceDir, f))]

        for file in onlyfiles:
            sFile = os.path.join(sourceDir, file)
            dFile = os.path.join(destDir, file)
            # TODO: Maybe add check to prevent file copying
            # if file exists and modified date the same -> skip
            # if not (os.path.exists(dFile) and os.path.getmtime(dFile) == os.path.getmtime(sFile)):
            copyfile(sFile, dFile)

        for nextDir in directories:
            self.__processDirectoryRecursively(os.path.join(currentDirectory, nextDir), sourceRoot, destinationRoot)

    def __checkObsoleteFiles(self, destDir, sourceDir):
        destObjects = [f for f in listdir(destDir) if not f == __timeLabel__]
        sourceObjects = [f for f in listdir(sourceDir)]
        for dObj in destObjects:
            if not dObj in sourceObjects:
                self.__logger.logObsoleteObject(os.path.join(destDir, dObj))


if __name__ == "__main__":
    __configs__ = ConfigReader(os.path.join(__scriptDir__, __mainConfigFile__), ":")
    Program().start()
