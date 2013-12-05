#!/usr/local/bin/python
from Components.Logger import Logger


__author__ = 'Denis'


def func():
    print("hi")
    asd = Logger('Log')
    asd.testMethod()

if __name__ == "__main__":
    func()
