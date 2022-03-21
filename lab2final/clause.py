"""

CSCI-630: Foundation of AI
lab2 Code - clause.py
Author: Prakhar Gupta
Username: pg9349

"""


from predicate import Predicate
from term import Term,Variable,Function
from constant import Constant

class Clause:

    def __init__(self):
        self.pred=[]
        self.english=None
        self.base=None


    def create_clause(self,x,maindict):
        x=x.strip()
        for j in x.split(" "):
            negation = False
            if "(" in j:
                str = j.split("(")
                str=str[0]
                s=j
                load = s[s.find('(') + 1:s.rfind(')')]
                if "," not in load:
                    load=[load]
                else:
                    load=load.split(",")
                terms=[]
                for i in load:
                    if i in maindict and maindict[i]=="Functions":
                        func = Function(i, 0, [], ["empty"])
                        term = Term(i, func, "Functions")
                        terms.append(term)

                    elif "(" in i:
                        functionname = i.split("(")
                        functionname = functionname[0]
                        loadfunction = i[i.find('(') + 1:i.rfind(')')]
                        typeofload=maindict[loadfunction]
                        if typeofload=="Variables":
                            var=Variable(loadfunction,0)
                            func = Function(functionname,0,[var],[typeofload])
                            term=Term(i,func,"Functions")
                            terms.append(term)


                    elif i in maindict:
                        type=maindict[i]
                        if type=="Constants":
                            const=Constant(i,0)
                            term=Term(i,const,type)
                            terms.append(term)
                        if type=="Variables":
                            var=Variable(i,0)
                            term=Term(i,var,type)
                            terms.append(term)
                load=terms

            else:
                str=j
                if "!" in str:
                    negation = True
                    #str = str[1:]
                    load=[Term(j,str[1:],"prop")]
                else:
                    load = [Term(j, j, "prop")]
            if "!" in str:
                negation = True
                str = str[1:]

            pred=Predicate(str,load,negation)


            self.pred.append(pred)


    def getpred(self):
        return self.pred

    def __str__(self):
        self.english=""
        l=[]
        for i in self.pred:
            l.append(str(i))
            #self.english=self.english+" "+str(i)
        l.sort()
        for i in l:
            self.english=self.english+" "+i
        return self.english

    def get_type(self):
        l=[]
        for i in self.pred:
            l.append(i.get_type())
        return l