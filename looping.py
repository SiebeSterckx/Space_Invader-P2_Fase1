class LoopingVariable:
    def __init__(self, value):
        self.__looping= value

    def value(self):
        return self.__looping

    def setvalue(self, value):
        self.__looping = value

    def increase(self, amount):
        self.__looping = self.__looping + amount
        if self.__looping >= 4206:
            self.__looping = 0