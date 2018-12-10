#some definitions about deterministic real-time automaton
#load rta model files (*.json)
import sys
import json
from interval import Constraint, complement_intervals, lbsort, union_constraints

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
    def __init__(self, id, source="", target="", label="", constraints = None):
        self.id = id
        self.source = source
        self.target = target
        self.label = label
        self.constraints = constraints or []
    
    def is_pass(self, tw):
        """
            determine whether the timeword tw can pass the transition.
        """
        # - means empty
        #if tw.action == "-":
            #return True
        if tw.action == self.label:
            for constraint in self.constraints:
                if constraint.isininterval(tw.time):
                    return True
        else:
            return False
        return False

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
    
    def is_accept(self, tws):
        """
            determine whether RTA accepts a timed words or not.
        """
        if len(tws) == 0:
            if self.initstate_name in self.accept_names:
                return 1
            else:
                return 0
        else:
            current_statename = self.initstate_name
            for tw in tws:
                flag = False
                for tran in self.trans:
                    if tran.source == current_statename and tran.is_pass(tw):
                        current_statename = tran.target
                        flag = True
                        break
                if flag == False:
                    return -1
            if current_statename in self.accept_names:
                return 1
            else:
                return 0

    def show(self):
        print "RTA name: "
        print self.name
        print "sigma and length of sigma: "
        print self.sigma, len(self.sigma)
        print "State (name, init, accept) :"
        for s in self.states:
            print s.name, s.init, s.accept
        print "transitions (id, source_state, label, target_state, constraints): "
        for t in self.trans:
            print t.id, t.source, t.label, t.target, t.show_constraints()
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
        rta_tran = RTATran(tran_id, source, target, label, constraints_list)
        trans += [rta_tran]
    return RTA(name, sigma, S, trans, initstate, accept_list), sigma

def buildAssistantRTA(rta):
    """
        build an assistant RTA which has the partitions at every node.
        The acceptance language is equal to teacher.
    """
    location_number = len(rta.states)
    tran_number = len(rta.trans)
    new_state = State(str(location_number+1), False, False)
    flag = False
    new_trans = []
    for s in rta.states:
        s_dict = {}
        for key in rta.sigma:
            s_dict[key] = []
        for tran in rta.trans:
            if tran.source == s.name:
                for label in rta.sigma:
                    if tran.label == label:
                        for constraint in tran.constraints:
                            s_dict[label].append(constraint)
        for key in s_dict:
            cuintervals = []
            if len(s_dict[key]) > 0:
                cuintervals = complement_intervals(s_dict[key])
            else:
                cuintervals = [Constraint("[0,+)")]
            if len(cuintervals) > 0:
                temp_tran = RTATran(tran_number, s.name, new_state.name, key, cuintervals)
                tran_number = tran_number+1
                new_trans.append(temp_tran)
    assist_name = "Assist_"+rta.name
    assist_states = [state for state in rta.states]
    assist_trans = [tran for tran in rta.trans]
    assist_init = rta.initstate_name
    assist_accepts = [sn for sn in rta.accept_names]
    if len(new_trans) > 0:
        assist_states.append(new_state)
        for tran in new_trans:
            assist_trans.append(tran)
        for label in rta.sigma:
            constraints = [Constraint("[0,+)")]
            temp_tran = RTATran(tran_number, new_state.name, new_state.name, label, constraints)
            tran_number = tran_number+1
            assist_trans.append(temp_tran)
    return RTA(assist_name, rta.sigma, assist_states, assist_trans, assist_init, assist_accepts)

def refine_rta_trans(rta):
    for tran in rta.trans:
        c_list = [c for c in tran.constraints]
        lbsort(c_list)
        union_intervals = union_constraints(c_list)
        tran.constraints = union_intervals

class Timedword():
    """
        define the timed word. a timed-words is a list of timed words
    """
    def __init__(self, action = "", time = 0):
        self.action = action
        self.time = time
    def __eq__(self, tw):
        if self.action == "" and tw.action == "":
            return True
        if self.action != tw.action:
            return False
        else:
            if self.time == tw.time:
                return True
            else:
                return False
    def getTW(self):
        return [self.action, self.time]
    def show(self):
        return "("+self.action+","+str(self.time)+")"

def tws_equal(tws1,tws2):
    if len(tws1) != len(tws2):
        return False
    else:
        for i in range(0, len(tws1)):
            if tws1[i] != tws2[i]:
                return False
        return True

def main():
    paras = sys.argv
    #A,_ = buildRTA("test_automata/test.json")
    A,_ = buildRTA(paras[1])
    AA = buildAssistantRTA(A)
    #print("---------------------a.json----------------")
    #A.show()
    #print("--------------------Assistant---------------------------")
    #AA.show()
    with open('lineAA.txt', 'a') as f:
        f.write(str(len(AA.trans))+',')
    with open('lineA.txt', 'a') as f:
        f.write(str(len(A.trans)) + ',')
    print len(A.trans), len(AA.trans)

if __name__=='__main__':
	main()
