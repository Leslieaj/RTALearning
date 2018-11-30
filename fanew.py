#some definitions about finite automaton

from interval import *
from rta import *

class TimedLabel:
    def __init__(self, name="", label="", constraints = None):
        self.name = name
        self.label = label
        self.constraints = constraints or []
        lbsort(self.constraints)

    def __eq__(self, timedlabel):
        if self.label == timedlabel.label and len(self.constraints) == len(timedlabel.constraints):
            templist = [c for c in self.constraints if c in timedlabel.constraints]
            if len(templist) == len(self.constraints):
                return True
            else:
                return False
        else:
            return False
    
    def constraints_show(self):
        s = ""
        for c in self.constraints[:-1]:
            s = s + c.show() + 'U'
        s = s + self.constraints[len(self.constraints)-1].show()
        return s

    def show(self):
        print self.name, self.label, self.constraints_show()

class FATran:
    def __init__(self, id, source="", target="", timedlabel=None):
        self.id = id
        self.source = source
        self.target = target
        self.timedlabel = timedlabel

class FA:
    def __init__(self, name="", timed_alphabet = {}, states = None, trans = [], initstate_name = "", accept_names = []):
        self.name = name
        self.timed_alphabet = timed_alphabet
        self.states = states
        self.trans = trans
        self.initstate_name = initstate_name
        self.accept_names = accept_names
    def show(self):
        print "FA name: "
        print self.name
        print "timed alphabet: "
        for term in self.timed_alphabet:
            print term
            print
            for timedlabel in self.timed_alphabet[term]:
                timedlabel.show()
                print
        print "State (name, init, accept)"
        for s in self.states:
            print s.name, s.init, s.accept
        print "transitions: (id, source, target, timed label): "
        for t in self.trans:
            print t.id, t.source, t.target
            t.timedlabel.show()
            print
        print "init state: "
        print self.initstate_name
        print "accept states: "
        print self.accept_names    

class RFATran:
    def __init__(self, id, source="", target="", label="", nfnums = []):
        self.id = id
        self.source = source
        self.target = target
        self.label = label
        self.nfnums = nfnums

class RFA:
    def __init__(self, name="", timed_alphabet = {}, states = None, trans = [], initstate_name = "", accept_names = []):
        self.name = name
        self.timed_alphabet = timed_alphabet
        self.states = states
        self.trans = trans
        self.initstate_name = initstate_name
        self.accept_names = accept_names
    def show(self):
        print "RFA name: "
        print self.name
        print
        print "timed alphabet: "
        for term in self.timed_alphabet:
            print term
            print
            for timedlabel in self.timed_alphabet[term]:
                timedlabel.show()
                print
        print "State (name, init, accept): "
        for s in self.states:
            print s.name, s.init, s.accept
        print
        print "transitions (id, source, target, label, constraint index in timed alphabet): "
        for t in self.trans:
            print t.id, t.source, t.target
            print t.label, t.nfnums
            for nfnum in t.nfnums:
                self.timed_alphabet[t.label][nfnum].show()
                print
            print
        print
        print "init state: "
        print self.initstate_name
        print
        print "accept states: "
        print self.accept_names    

def rta_to_fa(rta, flag):
    temp_alphabet = []
    trans = []
    for tran in rta.trans:
        label = copy.deepcopy(tran.label)
        constraints = copy.deepcopy(tran.constraints)
        timed_label = TimedLabel("",label,constraints)
        temp_alphabet += [timed_label]
        source = tran.source
        target = tran.target
        id = tran.id
        fa_tran = FATran(id, source, target, timed_label)
        trans.append(fa_tran)
    name = "FA_" + rta.name
    states = copy.deepcopy(rta.states)
    initstate_name = rta.initstate_name
    accept_names = []
    if flag == "generation": #means generation language
        for state in states:
            state.accept = True
            accept_names.append(state.name)
    elif flag == "receiving": #means receiving language
        accept_names = copy.deepcopy(rta.accept_names)
    else:
        accept_names = copy.deepcopy(rta.accept_names)
    timed_alphabet = alphabet_classify(temp_alphabet, rta.sigma)
    return FA(name, timed_alphabet, states, trans, initstate_name, accept_names)

def alphabet_classify(timed_alphabet, sigma):
    temp_set = {}
    for label in sigma:
        temp_set[label] = []
        for timedlabel in timed_alphabet:
            if timedlabel.label == label and timedlabel not in temp_set[label]:
                temp_set[label].append(timedlabel)
    return temp_set

def main():
    c1 = Constraint("[4,+]")
    c2 = Constraint("[0,0]")
    c3 = Constraint("[4,5]")
    c4 = Constraint("[0,1)")
    c5 = Constraint("(2,3)")
    cs1 = [c1, c5]
    cs2 = [c5, c1]
    cs3 = [c1]
    cs4 = [c4]
    print cs1 == cs2
    tl1 = TimedLabel("", "a", cs1)
    tl2 = TimedLabel("", "a", cs2)
    tl3 = TimedLabel("", "b", cs1)
    tl4 = TimedLabel("", "a", cs3)
    print tl1 == tl2
    print tl1 == tl3
    print tl1 == tl4
    tl1.show()
    tl4.show()
    print("---------------------a.json----------------")
    A,_ = buildRTA("test_automata/a.json")
    #A.show()
    AA = buildAssistantRTA(A)
    AA.show()
    print("-----------AA to FA-----------------------")
    AA_FA = rta_to_fa(AA, "receiving")
    AA_FA.show()

if __name__=='__main__':
	main()  
