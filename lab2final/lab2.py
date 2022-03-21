"""
CSCI-630: Foundation of AI
lab2 Code - lab2.py
Author: Prakhar Gupta
Username: pg9349

An implementation of FOL and PL

Code uses clause.py constant.py predicate.py term.py

"""




from predicate import Predicate
from clause import Clause
from  term import Term
pred=[]
consts=[]
import copy

import os

def getData(file_path):
    """
    File path reading
    :param file_path: file path
    :return: knowledge base
    """

    predicates = []
    variables = []
    constants = []
    functions = []
    clauses = []
    maindict={}
    with open(file_path) as f:
        lines = f.readlines()

    #    create an array of predicate objects
    predicates_str = lines[0].split(':')[1].strip().split(' ')
    if len(predicates_str)>0 :
        if "" not in predicates_str:
            for i in predicates_str:

                maindict[i]="Predicates"

    variables_str = lines[1].split(':')[1].strip().split(' ')
    if len(variables_str)>0 :
        if "" not in variables_str:
            for i in variables_str:

                maindict[i]="Variables"

    constants_str = lines[2].split(':')[1].strip().split(' ')
    if len(constants_str)>0 :
        if "" not in constants_str:
            for i in constants_str:

                maindict[i]="Constants"
    functions_str = lines[3].split(':')[1].strip().split(' ')
    if len(functions_str)>0 :
        if "" not in functions_str:
            for i in functions_str:

                maindict[i]="Functions"

    # create an array of clauses.
    clauses_dict= {}
    for i in range(5,len(lines)):
        x=Clause()
        x.create_clause(lines[i],maindict)
        clauses_dict[lines[i].strip()]=x

    return clauses_dict


def check(c1,c2):

    x=str(c1)
    y=str(c2)
    if x==y:
        return False
    if "!" not in x or "!" not in y:
        return False
    x1=x.replace("!",'')
    y1=y.replace("!",'')
    if x1==y1:
        return True
    else:
        return False

## Used this unification algorithm
## https://www.youtube.com/watch?v=ZMgd47uX0Aw&list=PLpYfdzRngdXOolW_76OGeXhnkF3Gz9KBK&index=6

def unify(p1,p2):
    """
    Unification algo
    :param p1: predicate 1
    :param p2: predicate 2
    :return:
    """
    if not isinstance(p1, Predicate) and not isinstance(p2, Predicate):
        sdldk = p1.get_type()
        if p1.get_type() == "Functions" or p2.get_type() == "Functions" or p1.get_type() == "Variables" or p1.get_type() == "Constansts" or p2.get_type() == "Variables" or p2.get_type() == "Constansts":
            sdldk = p1.get_type()
            if p1.value() == p2.value() and p1.name == p2.name:
                return None
            elif p1.get_type() == "Constants" and p2.get_type() == "Functions":
                funcload = p2.load.load[0]
                return {funcload: p1}
            elif p2.get_type() == "Constants" and p1.get_type() == "Functions":
                funcload = p1.load.load[0]
                return {funcload: p2}

            elif p1.get_type() == "Variables" and p2.get_type() == "Functions":
                for i in p2.load.load:
                    if p1.value() == i.value():
                        return {"no": []}
                    return {p1: p2}

            elif p2.get_type() == "Variables" and p1.get_type() == "Functions":
                for i in p1.load.load:
                    if p2.value() == i.value():
                        return {"no": []}
                    return {p2: p1}

            elif p1.get_type() == "Variables":
                return {p2: p1}
            elif p2.get_type() == "Variables":
                return {p1: p2}
            else:
                return {'no': []}
    if p1.name != p2.name:
        return {'no': []}
    if isinstance(p1, Term) or isinstance(p2, Term):
        return {'no': []}
    elif len(p1.load) != len(p2.load):
        return {'no': []}
    substitute = dict()
    for i in range(len(p1.load)):
        x = unify(p1.load[i], p2.load[i])
        if x is None:
            return {"no": []}
        elif "no" in x.keys():
            return {"no": []}
        else:
            substitute.update(x)

    return substitute



def get_new_clauses(c1,c2,unidict):
    """
    Form new clauses
    :param c1: clasue 1
    :param c2: clasue 2
    :param unidict: substitution dict
    :return:
    """
    x=copy.deepcopy(c1)
    y = copy.deepcopy(c2)
    newx=Clause()
    newy=Clause()
    for k,v in unidict.items():
        for i in x.pred:
            for j in y.pred:
                # if i.name==j.name:
                    for g in i.load:
                        if v is None:
                            xx=111
                        for rep in v:
                            if g.name==rep.name:
                                i.load=[k if item == g else item for item in i.load]
                                #i.load.append(k)
                                # predx=Predicate(i.name,g,i.neg)
                                # newx.pred.append(predx)
                    for g in j.load:
                        for rep in v:
                            if g.name==rep.name:
                                j.load=[k if item == g else item for item in j.load]
                                #j.load.append(k)
                        # predy=Predicate(j.name,g,j.neg)
                        # newy.pred.append(predy)

    return x,y



def get_unify_clause(c1,c2):
    pred_c1=c1.pred
    pred_c2=c2.pred
    unilist=[]
    unidict={}
    for i in pred_c1:
        for j in pred_c2:
            output=unify(i,j)
            unilist.append(output)
    # if (str(c2)==' animal(x1) animal(x1)'):
    #     print("")
    for i in unilist:
        for k,v in i.items():
            if k!="no":
                if k not in unidict.keys():
                    unidict[k]=[]
                    unidict[k].append(v)
                elif k in unidict.keys():
                    unidict[k].append(v)

    if (len(unidict)>0):
        x,y=get_new_clauses(c1,c2,unidict)
        return x,y
    return None


def variable_resolver(c1,c2):
    """
    Resolving variables
    :param c1: clause 1
    :param c2: clasue 2
    :return:
    """
    cla1=copy.deepcopy(c1)
    cla2=copy.deepcopy(c2)
    c1pred=cla1.pred
    c2pred=cla2.pred
    list = []
    pair=get_unify_clause(c1,c2)
    if pair is None:
        return "skip"
    else:
        flag = 0
        clause1=pair[0].pred
        clause2=pair[1].pred
        if len(clause1) == 2 and len(clause2) == 2:

            if check(pair[0], pair[1]) and len(clause2) == len(clause1):
                size = len(clause1)
                ca1 = []
                for i in range(0, size):
                    x = Clause()
                    x.pred = [clause1[i], clause2[i]]
                    x.base = str(c1) + "<>" + str(c2)
                    ca1.append(x)

                return ca1
        for i in range(len(clause1)):
            for j in range(len(clause2)):
                if clause1[i].value() == clause2[j].value() and (clause1[i].neg != clause2[j].neg) and clause1[i].name == clause2[j].name:
                    clause1.remove(clause1[i])
                    clause2.remove(clause2[j])
                    flag = 1
                    break

            if flag:
                break

        if flag:
            for i in clause1:
                # if i not in negated:
                list.append(i)
            for j in clause2:
                # if j not in negated:
                list.append(j)
            xnew = Clause()
            xnew.pred = list
            xnew.base = str(c1) + "<>" + str(c2)
            return xnew

        return "skip"






def resolver(c1,c2):
    """
    Main resolver function
    :param c1: clause 1
    :param c2: clasue 2
    :return:
    """
    list = []
    clause1=c1.pred.copy()
    clause2 = c2.pred.copy()
    # flag will be used to ensure the fact that there is only one deletion at a time
    flag = 0
    ff=c1.get_type()
    if ["Variables"] in c1.get_type() or ["Variables"] in c2.get_type():
        cc= variable_resolver(c1,c2)
        if cc=="skip":
            return "skip"
        else:
            return cc


    if len(clause1)==2 and len(clause2)==2:

        if check(c1,c2) and len(clause2)==len(clause1):
            size=len(clause1)
            ca1 = []
            for i in range(0,size):

                x = Clause()
                x.pred = [clause1[i],clause2[i]]
                x.base = str(c1) + "<>" + str(c2)
                ca1.append(x)

            return ca1

    negated=[]
    for i in c1.pred:
        for j in c2.pred:
            x111=i.get_type()
            if i.get_type()==['prop'] and j.get_type()==["prop"]:

                if i.value() == j.value() and (i.neg!=j.neg):
                    clause1.remove(i)
                    clause2.remove(j)
                    flag = 1
                    break
            else:
                if i.value() == j.value() and (i.neg != j.neg) and i.name==j.name:
                    clause1.remove(i)
                    clause2.remove(j)
                    flag = 1
                    break


        if flag:
            break

    if flag:
        for i in clause1:
            # if i not in negated:
                list.append(i)
        for j in clause2:
            # if j not in negated:
                list.append(j)
        x = Clause()
        x.pred = list
        x.base=str(c1)+"<>"+str(c2)
        return x

    return "skip"



def isSubset(A, B):
    """
    Subset function
    :param A: list of clasue 1
    :param B: list of clasue 2
    :return: True/False
    """
    a1 = {}
    x=[]
    for clause in A:
        a1[str(clause)] = clause
        x.append(str(clause)+":"+clause.base)

    b1 = {}
    for clause in B:
        b1[str(clause)] = clause

    ca = set(a1.keys())
    cb = set(b1.keys())

    return ca.issubset(cb)




def plresolver(kb):
    """
     kownledge base resolving
    :param kb:
    :return:
    """
    clauses=[]
    used_pairs=[]
    resolved_clasues=[]
    for i,j in kb.items():

        clauses.append(j)
    newList = []
    while True:

        n = len(clauses)
        if n>10:
            dslkds=0

        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (c1, c2) in pairs:
            # if str(c2)==" !dry(t5) sprinkler(t5, l0)" and str(c1)==" !sprinkler(t9, l1)":
            #     sfdd=10
            if (str(c1),str(c2)) not in used_pairs:
                used_pairs.append((str(c1),str(c2)))
                used_pairs.append((str(c2),str(c1)))
                resolvents = resolver(c1, c2)

                if isinstance(resolvents, list):
                    resolved_clasues.extend(resolvents)
                    # used_pairs.append((resolvents[0],resolvents[1]))
                    # used_pairs.append((resolvents[1],resolvents[0]))

                elif resolvents=="skip":
                    continue

                elif len(resolvents.pred)==0:
                    return False


                else:
                    resolved_clasues.append(resolvents)



        if isSubset(resolved_clasues,clauses):
            return True
        if len(resolved_clasues)>0:
            #print(resolved_clasues)
            clauses.extend(resolved_clasues)
        if (n == len(clauses)):
            return True


def driver():
    #dirname = r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\constants'
    #dirname = r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\prop'
    #dirname = r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\universals'
    #dirname = r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\universals+constants'
    #dirname = r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\functions'
    # giving file extension
    ext = ('.cnf')

    # iterating over all files
    for files in os.listdir(dirname):
        if files.endswith(ext):
            print(files)  # printing file name of desired extension
            kb=getData(dirname+"\\"+files)
            x=plresolver(kb)
            if x:
                print("Yes")
            else:
                print("No")
        else:
            continue


if __name__ == '__main__':
    import sys
    #print(sys.argv)
    if len(sys.argv)==2:
        a = sys.argv[1]
        kb = getData(a)
        x = plresolver(kb)
        if x:
            print("Yes")
        else:
            print("No")

    else:
        print("Check args list")



#driver()
# kb=getData(r'C:\Users\Prakhar Gupta\Desktop\AI630\lab2\testcases (2)\functions\f1.cnf')
# #
# # # for i,j in kb.items():
# # #     print(j.get_type())
# print(plresolver(kb))