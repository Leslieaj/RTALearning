#define Evidence Automaton and build a hypothesis RTA

#import pygraphviz as pyg
from rta import *
from membership import *

class EvidenceAutomaton():
    def __init__(self, sigma= None, states=None, trans=None, initstate=None, accept=None):
        #self.name = name
        self.sigma = sigma
        self.states = states or []
        self.trans = trans or []
        self.initstate_name = initstate or []
        self.accept_names = accept or []
    
    def show(self):
        #print "EA name: "
        #print self.name
        print "sigma and length of sigma: "
        print self.sigma, len(self.sigma)
        print "State (name, init, accept) :"
        for s in self.states:
            print s.name, s.init, s.accept
        print "transitions (id, source_state, label, target_state): "
        for t in self.trans:
            print t.id, t.source, [tw.show() for tw in t.label], t.target
            print
        print "init state: "
        print self.initstate_name
        print "accept states: "
        print self.accept_names

class EATran():
    def __init__(self, id, source = "", label = None, target = ""):
        self.id = id
        self.source = source
        self.label = label or []
        self.target = target

def buildEvidenceAutomaton(table, sigma):
    new_sigma = [action for action in sigma]
    states = []
    initstate_name = ""
    accept_names = []
    value_name_dict = {}
    for s,i in zip(table.S, range(1, len(table.S)+1)):
        name = str(i)
        value_name_dict[s.whichstate()] = name
        init = False
        accept = False
        if s.tws == []:
            init = True
            initstate_name = name
        if s.value[0] == 1:
            accept = True
            accept_names.append(name)
        temp_state = State(name, init, accept)
        states.append(temp_state)
    trans_number = 0
    trans = []
    table_element = [s for s in table.S] + [r for r in table.R]
    for r in table_element:
        if r.tws == []:
            continue
        timedwords = [tw for tw in r.tws]
        w = timedwords[:-1]
        a = timedwords[len(timedwords)-1]
        source = ""
        target = ""
        label = [a]
        for element in table_element:
            if w == element.tws:
                source = value_name_dict[element.whichstate()]
            if timedwords == element.tws:
                target = value_name_dict[element.whichstate()]
        need_newtran = True
        for tran in trans:
            if source == tran.source and target == tran.target:
                if a.action == tran.label[0].action:
                    if a in tran.label:
                        need_newtran = False
                    else:
                        tran.label.append(a)
                        need_newtran = False
        if need_newtran == True:
            temp_tran = EATran(trans_number, source, label, target)
            trans.append(temp_tran)
            trans_number = trans_number + 1
    ea = EvidenceAutomaton(new_sigma, states, trans, initstate_name, accept_names)
    return ea

def buildhypothesis(ea, n):
    new_name = "H_" + str(n)
    sigma = [action for action in ea.sigma]
    states = [state for state in ea.states]
    initstate_name = ea.initstate_name
    accept_names = [name for name in ea.accept_names]
    trans = []
    for s in states:
        s_dict = {}
        for key in sigma:
            s_dict[key] = [0]
        for tran in ea.trans:
            if tran.source == s.name:
                for label in sigma:
                    if tran.label[0].action == label:
                        for tw in tran.label:
                            if tw.time != 0:
                                s_dict[label].append(tw.time)
        for tran in ea.trans:
            if tran.source == s.name:
                timepoints = [time for time in s_dict[tran.label[0].action]]
                timepoints.sort()
                constraints = []
                for tw in tran.label:
                    index = timepoints.index(tw.time)
                    temp_constraint = None
                    if index + 1 < len(timepoints):
                        if isinstance(tw.time,int) and isinstance(timepoints[index+1], int):
                            temp_constraint = Constraint("["+str(tw.time)+","+str(timepoints[index+1])+")")
                        elif isinstance(tw.time,int) and not isinstance(timepoints[index+1], int):
                            temp_constraint = Constraint("["+str(tw.time)+","+str(int(timepoints[index+1]))+"]")
                        elif not isinstance(tw.time,int) and isinstance(timepoints[index+1], int):
                            temp_constraint = Constraint("("+str(int(tw.time))+","+str(timepoints[index+1])+")")
                        else:
                            temp_constraint = Constraint("("+str(int(tw.time))+","+str(int(timepoints[index+1]))+"]")
                        constraints.append(temp_constraint)
                    else:
                        if isinstance(tw.time,int):
                            temp_constraint = Constraint("["+str(tw.time)+"," + "+" + ")")
                        else:
                            temp_constraint = Constraint("("+str(int(tw.time))+"," + "+" + ")")
                        constraints.append(temp_constraint)
                #nfc = union_intervals_to_nform(constraints)
                temp_tran = RTATran(tran.id, tran.source, tran.target, tran.label[0].action, constraints)
                trans.append(temp_tran)
    rta = RTA(new_name, sigma, states, trans, initstate_name, accept_names)
    return rta

def main():
    A,_ = buildRTA("test_automata/a.json")
    AA = buildAssistantRTA(A)
    sigma = ["a", "b"]

    tw1 = Timedword("a", 0)
    tw2 = Timedword("b", 0)
    tw3 = Timedword("a", 5)
    tw4 = Timedword("b", 4)
    tw5 = Timedword("a", 7)
    tw6 = Timedword("b", 2)
    tws0 = [] # empty
    tws1 = [tw1] # (a,0)
    tws2 = [tw2] # (b,0)
    tws3 = [tw3] # (a,5)
    tws4 = [tw3,tw1] # (a,5) (a,0)
    tws5 = [tw3,tw2] # (a,5) (b,0)
    tws6 = [tw5] # (a,7)
    tws7 = [tw4] # (b,4)
    tws8 = [tw4,tw3] # (b,4) (a,5)
    tws9 = [tw1,tw1] # (a,0) (a,0)
    tws10 = [tw1,tw2] # (a,0) (b,0)
    tws11 = [tw6,tw3] # (b,2) (a,5)
    tws12 = [tw6] #(b,2)

    e0 = Element(tws0,[0])
    e1 = Element(tws1,[0])
    e2 = Element(tws2,[0])
    #e3 = Element(tws3,[1])
    #e4 = Element(tws4,[0,1,0,1])
    #e5 = Element(tws5,[1,1,0,1])
    S = [e0]
    R = [e1,e2]
    E = []
    
    print("----------------------T1--------------------------")
    T1 = Table(S,R,E)
    T1.show()
    print("----------------------EA1-------------------------")
    ea1 = buildEvidenceAutomaton(T1, sigma)
    ea1.show()
    print("----------------------H1--------------------------")
    H1 = buildhypothesis(ea1, 1)
    H1.show()
    print("----------------------T2--------------------------")
    ctx1 = tws3
    T2 = add_ctx(T1, ctx1, AA)
    T2.show()
    print("----------------------T3--------------------------")
    flag_closed, new_S, new_R, move = T2.is_closed()
    T3 = make_closed(new_S, new_R, move, T2, sigma, AA)
    T3.show()
    print("----------------------EA2-------------------------")
    ea2 = buildEvidenceAutomaton(T3, sigma)
    ea2.show()
    print("----------------------H2--------------------------")
    H2 = buildhypothesis(ea2, 2)
    H2.show()
    print("----------------------T4--------------------------")
    ctx2 = tws6
    T4 = add_ctx(T3, ctx2, AA)
    T4.show()
    print("----------------------EA3-------------------------")
    ea3 = buildEvidenceAutomaton(T4, sigma)
    ea3.show()
    print("----------------------H3--------------------------")
    H3 = buildhypothesis(ea3, 3)
    H3.show()
    print("----------------------T5--------------------------")
    ctx3 = tws8
    T5 = add_ctx(T4, ctx3, AA)
    T5.show()
    return 0

if __name__=='__main__':
	main()
