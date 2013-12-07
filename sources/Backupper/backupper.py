#!/usr/local/bin/python
import os
from shutil import copyfile
import sys
from Components.ConfigReader import ConfigReader
from Components.Logger import Logger
from os import listdir
from os.path import isfile, join


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
            self.__logger.log("Directory backed up: " + directories[i][0])
        self.__logger.log("Backup finished")

    def processDirectoryRecursively(self, currentDirectory, sourceRoot, destinationRoot):
        # TODO: Try another way of path combining
        sourceDir = sourceRoot + "/" + currentDirectory#join(sourceRoot, currentDirectory)#
        destDir = destinationRoot + "/" + currentDirectory#join(destinationRoot, currentDirectory)#

        if os.path.isfile(sourceDir + "/.backup-ignore"): #join(sourceDir, ".backup-ignore")
            self.__logger.logIgnoredObject(sourceDir)
            return

        if not os.path.exists(destDir):
            os.makedirs(destDir)

        self.__checkObsoleteFiles(destDir, sourceDir)

        onlyfiles = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]
        directories = [f for f in listdir(sourceDir) if not isfile(join(sourceDir, f))]

        for file in onlyfiles:
            sFile = sourceDir + "/" + file
            dFile = destDir + "/" + file
            # TODO: Maybe add check to prevent file copying
            # if file exists and modified date the same -> skip
            #if not (os.path.exists(dFile) and os.path.getmtime(dFile) == os.path.getmtime(sFile)):
            copyfile(sFile, dFile)

        for dir in directories:
            self.processDirectoryRecursively("/"+dir, sourceRoot, destinationRoot)

    # TODO: Refactor (code duplicating and path combining)
    # Also check if file and directory has same names
    def __checkObsoleteFiles(self, destDir, sourceDir):
        destFiles = [f for f in listdir(destDir) if isfile(join(sourceDir, f))]
        destDirectories = [f for f in listdir(destDir) if not isfile(join(sourceDir, f))]
        sourceFiles = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]
        sourceDirectories = [f for f in listdir(sourceDir) if not isfile(join(sourceDir, f))]

        for dFile in destFiles:
            if not dFile in sourceFiles:
                self.__logger.logObsoleteObject(destDir+"/"+dFile)
        for dDir in destDirectories:
            if not dDir in sourceDirectories:
                self.__logger.logObsoleteObject(destDir+"/"+dDir)


if __name__ == "__main__":
    Program().start()
