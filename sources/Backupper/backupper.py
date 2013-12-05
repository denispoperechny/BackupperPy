#!/usr/local/bin/python
from Components.Logger import Logger


__author__ = 'Denis'


def func():
    print("hi")
    asd = Logger('Logs')
    asd.logSkippedObject("hey")
    asd.logSkippedObject("hey1")
    asd.log("Started")

if __name__ == "__main__":
    func()
