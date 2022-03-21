"""

CSCI-630: Foundation of AI
lab2 Code - term.py
Author: Prakhar Gupta
Username: pg9349

"""


class Term:
    def __init__(self, name,load, type):
        self.name =name
        self.load=load
        self.type=type


    def value(self):
        if self.type=='prop':
            return self.load
        else:
            return self.load.value()

    def get_type(self):
        return self.type

    def __str__(self):
        if self.type == 'prop':
            return self.load
        else:
            return self.load.value()



class Variable:
    def __init__(self,load,neg):
        self.load=load
        self.neg=neg
        self.unifyTo=[]
        self.name=self.load

    def value(self):
        return self.load

    def __str__(self):
        return self.load

    def get_type(self):
        return "Variables"


class Function:
    def __init__(self,name,neg,load=[],loadtype=[]):
        self.name=name
        self.load=load
        self.neg=neg
        self.loadtype=loadtype

    def __str__(self):
        if len(self.load)==0:
            return self.name
        else:
            l=[]
            for i in self.load:
                l.append(i.value())
            y = str(self.name) + "(" + ", ".join(l) + ")"
            return y

    def value(self):
        return self.load

    def get_type(self):
        return self.loadtype

