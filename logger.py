import time


class Logger:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("LOG ---> ", text)


def debug(function):
    def inner(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("DEBUG --->", function.__name__, end - start)
        return result

    return inner
