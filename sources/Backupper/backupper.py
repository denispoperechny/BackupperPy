#!/usr/local/bin/python
import os
from shutil import copyfile
import sys
from Components.ConfigReader import ConfigReader
from Components.Logger import Logger
from os import listdir
from os.path import isfile

__author__ = 'Denis'
__configs__ = None
__mainConfigFile__ = "backupper.cfg"


def unhandledExceptionUtilizer(type, value, traceback):
        logger = Logger(__configs__.getValuesByKey("logs")[0])
        logger.log("Unhandled Exception")
        logger.log("Type:" + str(type))
        logger.log("Value:" + str(value))
        #TODO: log the traceback
        print("Traceback:" + traceback)
sys.excepthook = unhandledExceptionUtilizer


class Program(object):

    __logger = None

    def start(self):
        self.__logger = Logger(__configs__.getValuesByKey("logs")[0])
        self.__logger.log("Starting")
        self.__logger.log("Reading directories config: " + __configs__.getValuesByKey("directories_config")[0])
        configReader = ConfigReader(__configs__.getValuesByKey("directories_config")[0], "=>")
        directories = configReader.getTuples()
        self.__logger.log("Directories to be backed up: " + str(len(directories)))
        self.__logger.log("Starting backup process")
        for i in range(0, len(directories)):
            self.processDirectoryRecursively("", directories[i][0], directories[i][1])
            self.__logger.log("Directory backed up: " + directories[i][0])
        self.__logger.log("Backup finished")

    def processDirectoryRecursively(self, currentDirectory, sourceRoot, destinationRoot):
        sourceDir = os.path.join(sourceRoot, currentDirectory)
        destDir = os.path.join(destinationRoot, currentDirectory)

        if os.path.isfile(os.path.join(sourceDir, ".backup-ignore")):
            self.__logger.logIgnoredObject(sourceDir)
            return

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
            self.processDirectoryRecursively(os.path.join(currentDirectory, nextDir), sourceRoot, destinationRoot)

    # TODO: Refactor (code duplicating)
    def __checkObsoleteFiles(self, destDir, sourceDir):
        destFiles = [f for f in listdir(destDir) if isfile(os.path.join(sourceDir, f))]
        destDirectories = [f for f in listdir(destDir) if not isfile(os.path.join(sourceDir, f))]
        sourceFiles = [f for f in listdir(sourceDir) if isfile(os.path.join(sourceDir, f))]
        sourceDirectories = [f for f in listdir(sourceDir) if not isfile(os.path.join(sourceDir, f))]

        for dFile in destFiles:
            if not dFile in sourceFiles:
                self.__logger.logObsoleteObject(os.path.join(destDir, dFile))
        for dDir in destDirectories:
            if not dDir in sourceDirectories:
                self.__logger.logObsoleteObject(os.path.join(destDir, dDir))


if __name__ == "__main__":
    __configs__ = ConfigReader(__mainConfigFile__, ":")
    Program().start()
