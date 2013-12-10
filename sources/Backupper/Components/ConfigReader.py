__author__ = 'Denis'


class ConfigReader(object):

    __configFile = ""
    __delimiter = ""
    __data = None

    def __init__(self, file, delimeter):
        self.__configFile = file
        self.__delimiter = delimeter

    def __readData(self):
        file = open(self.__configFile, 'r')
        self.__data = list()
        for line in file:
            # TODO: How does this work (line[-1])?
            if '\n' == line[-1]:
                line = line[:-1]
            if (len(line.strip()) > 0 and line.strip()[0] != '#'):
                splitted = line.split(self.__delimiter)
                self.__data.append((splitted[0].strip(), splitted[1].strip()))

    def count(self):
        return len(self.getTuples())

    def getTuples(self):
        if self.__data is None:
            self.__readData()

        return self.__data

    def getValuesByKey(self, key):
        result = [d[1] for d in self.getTuples() if d[0] == key.strip()]
        return result