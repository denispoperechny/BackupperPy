__author__ = 'Denis'

class ConfigReader(object):

    __configFile = ""
    __delimiter = ""
    __data = None

    def __init__(self, file, delimeter):
        self.__configFile = file
        self.__delimiter = delimeter

    def __readData(self):
        print("Not implemented")

    def count(self):
        return self.getTuples().count()

    def getTuples(self):
        if self.__data is None:
            self.__readData()

        return self.__data