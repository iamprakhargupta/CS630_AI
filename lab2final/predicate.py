"""

CSCI-630: Foundation of AI
lab2 Code - predicate.py
Author: Prakhar Gupta
Username: pg9349

"""



class Predicate:

    def __init__(self,name,load,neg,type=None):
        self.name=name
        self.neg=neg
        self.load=load
        self.type=type

    def value(self):
        l = []
        for i in self.load:
            l.append(i.value())
        return l

    def get_type(self):
        l=[]
        for i in self.load:
            l.append(i.get_type())
        return l

    def __str__(self):
        x=[]
        for i in self.load:
            if i.get_type()=="prop":
                x.append(self.name)
                if self.neg:
                    return str("!"+self.name)
                else:
                    return str(self.name)

            else:
                x.append(i.name)

        #x.sort()
        y=str(self.name)+"("+", ".join(x)+")"
        if self.neg:
            return "!"+y
        return y








    def name_ofload(self):
        l = []
        for i in self.load:
            l.append(i.value())
        return l

    def get_term_name(self):
        pass