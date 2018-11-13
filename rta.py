#some definitions about deterministic real-time automaton
#load rta model files (*.json)

import json
from normalform import *

class State:
    name = ""
    init = False
    accept = False
    def __init__(self, name="", init=False, accept=False):
        self.name = name
        self.init = init
        self.accept = accept

class RTATran:
    id = None
    source = ""
    target = ""
    label = ""
    nfc = None
    def __init__(self, id, source="", target="", label="", constraints = None, nfc=None):
        self.id = id
        self.source = source
        self.target = target
        self.label = label
        self.constraints = constraints or []
        self.nfc = nfc
    
    def show_constraints(self):
        length = len(self.constraints)
        if length ==0:
            return "[0,+)"
        else:
            temp = self.constraints[0].guard
            for i in range(1, length):
                temp = temp + 'U' + self.constraints[i].guard
            return temp

class RTA:
    def __init__(self, name="", sigma= None, states=None, trans=None, initstate=None, accept=None):
        self.name = name
        self.sigma = sigma
        self.states = states or []
        self.trans = trans or []
        self.initstate_name = initstate
        self.accept_names = accept or []
    
    def show(self):
        print "RTA name: "
        print self.name
        print "sigma and length of sigma: "
        print self.sigma, len(self.sigma)
        print "State (name, init, accept) :"
        for s in self.states:
            print s.name, s.init, s.accept
        print "transitions (id, source_state, label, target_state, normalform guard): "
        for t in self.trans:
            print t.id, t.source, t.label, t.target, t.show_constraints()
            t.nfc.show()
            print
        print "init state: "
        print self.initstate_name
        print "accept states: "
        print self.accept_names

def buildRTA(jsonfile):
    """
        build the teacher RTA from a json file.
    """
    data = json.load(open(jsonfile,'r'))
    name = data["name"].encode("utf-8")
    states_list = [s.encode("utf-8") for s in data["s"]]
    sigma = [s.encode("utf-8") for s in data["sigma"]]
    trans_set = data["tran"]
    initstate = data["init"].encode("utf-8")
    accept_list = [s.encode("utf-8") for s in data["accept"]]
    #observable = [label.encode("utf-8") for label in data["observable"]]
    S = [State(state) for state in states_list]
    for s in S:
        if s.name == initstate:
            s.init = True
        if s.name in accept_list:
            s.accept = True
    trans = []
    for tran in trans_set:
        tran_id = int(tran.encode("utf-8"))
        source = trans_set[tran][0].encode("utf-8")
        label = trans_set[tran][1].encode("utf-8")
        intervals_str = trans_set[tran][2].encode("utf-8")
        intervals_list = intervals_str.split('U')
        constraints_list = []
        for constraint in intervals_list:
            new_constraint = Constraint(constraint.strip())
            constraints_list.append(new_constraint)
        target = trans_set[tran][3].encode("utf-8")
        nfc = union_intervals_to_nform(constraints_list)
        rta_tran = RTATran(tran_id, source, target, label, constraints_list, nfc)
        trans += [rta_tran]
    return RTA(name, sigma, S, trans, initstate, accept_list)
    #return RTA(name, sigma, S, trans, initstate, accept_list), observable

def main():
    print("---------------------a.json----------------")
    A = buildRTA("a.json")
    A.show()

if __name__=='__main__':
	main()
