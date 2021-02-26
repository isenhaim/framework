class Logger:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
