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

def alphabet_combine(alphabet1, alphabet2):
    combined_alphabet = {}
    for key in alphabet1:
        combined_alphabet[key] = []
        for temp1 in alphabet1[key]:
            if temp1 not in combined_alphabet[key]:
                combined_alphabet[key].append(temp1)
        for temp2 in alphabet2[key]:
            if temp2 not in combined_alphabet[key]:
                combined_alphabet[key].append(temp2)
    return combined_alphabet

def alphabet_classify(timed_alphabet, sigma):
    temp_set = {}
    for label in sigma:
        temp_set[label] = []
        for timedlabel in timed_alphabet:
            if timedlabel.label == label and timedlabel not in temp_set[label]:
                temp_set[label].append(timedlabel)
    return temp_set

def alphabet_partitions(classified_alphabet):
    floor_bn = BracketNum('0',Bracket.LC)
    ceil_bn = BracketNum('+',Bracket.RO)
    partitioned_alphabet = {}
    bnlist_dict = {}
    for key in classified_alphabet:
        partitioned_alphabet[key] = []
        timedlabel_list = classified_alphabet[key]
        key_bns = []
        key_bnsc = []
        for timedlabel in timedlabel_list:
            temp_constraints = timedlabel.constraints
            for constraint in temp_constraints:
                min_bn = None
                max_bn = None
                temp_min = constraint.min_value
                temp_minb = None
                if constraint.closed_min == True:
                    temp_minb = Bracket.LC
                else:
                    temp_minb = Bracket.LO
                temp_max = constraint.max_value
                temp_maxb = None
                if constraint.closed_max == True:
                    temp_maxb = Bracket.RC
                else:
                    temp_maxb = Bracket.RO
                min_bn = BracketNum(temp_min, temp_minb)
                max_bn = BracketNum(temp_max, temp_maxb)
                if min_bn not in key_bns:
                    key_bns+= [min_bn]
                if max_bn not in key_bns:
                    key_bns+=[max_bn]
        key_bnsc = copy.deepcopy(key_bns)
        for bn in key_bns:
            bnc = bn.complement()
            if bnc not in key_bnsc:
                key_bnsc.append(bnc)
        if floor_bn not in key_bnsc:
            key_bnsc.append(floor_bn)
        if ceil_bn not in key_bnsc:
            key_bnsc.append(ceil_bn)
        key_bnsc.sort()
        bnlist_dict[key] = key_bnsc
        for index in range(len(key_bnsc)):
            if index%2 == 0:
                temp_constraint = Constraint(key_bnsc[index].getbn()+','+key_bnsc[index+1].getbn())
                temp_timedlabel = TimedLabel("",key, [temp_constraint])
                partitioned_alphabet[key].append(temp_timedlabel)
    for term in partitioned_alphabet:
        for timedlabel,index in zip(partitioned_alphabet[term], range(len(partitioned_alphabet[term]))):
            timedlabel.name = term + '_'+ str(index)
    return partitioned_alphabet, bnlist_dict

def fa_to_rfa(fa, alphapartitions):
    name = copy.deepcopy(fa.name)
    timed_alphabet = copy.deepcopy(alphapartitions)
    states = copy.deepcopy(fa.states)
    trans = []
    for tran in fa.trans:
        tran_id = tran.id
        source = tran.source
        target = tran.target
        label = tran.timedlabel.label
        nfnums = []
        for nf, i in zip(timed_alphabet[label], range(0, len(timed_alphabet[label]))):
            if constraint_contain(nf.constraints[0], tran.timedlabel.constraints) == True:
                nfnums.append(i)
        new_tran = RFATran(tran_id, source, target, label, nfnums)
        trans.append(new_tran)
    initstate_name = copy.deepcopy(fa.initstate_name)
    accept_names = copy.deepcopy(fa.accept_names)
    rfa = RFA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return rfa

def rfa_complement(rfa):
    name = "C_" + rfa.name
    states_num = len(rfa.states)
    states = copy.deepcopy(rfa.states)
    initstate_name = ""
    accept_names = []
    for s in states:
        if s.init == True:
            initstate_name = s.name
        if s.accept == True:
            s.accept = False
        else:
            s.accept = True
            accept_names.append(s.name)
    timed_alphabet = copy.deepcopy(rfa.timed_alphabet)
    new_state = State(str(states_num+1), False, True)
    states.append(new_state)
    accept_names.append(new_state.name)
    sigma = [term for term in rfa.timed_alphabet]
    trans = copy.deepcopy(rfa.trans)
    need_newstate = False
    for s in states:
        nfnums_need = {}
        nfnums_exist = {}
        for term in sigma:
            nfnums_need[term] = []
            nfnums_exist[term] = []
        for rfatran in rfa.trans:
            if rfatran.source == s.name:
                for i in rfatran.nfnums:
                    if i not in nfnums_exist[rfatran.label]:
                        nfnums_exist[rfatran.label].append(i)
        for term in nfnums_exist:
            for i in range(0, len(timed_alphabet[term])):
                if i not in nfnums_exist[term]:
                    nfnums_need[term].append(i)
        for term in nfnums_need:
            if len(nfnums_need[term]) > 0:
                tran_id = len(trans)
                source = s.name
                if source != new_state.name:
                    need_newstate = True
                target = new_state.name
                label = term
                nfnums = nfnums_need[term]
                new_tran = RFATran(tran_id, source, target, label, nfnums)
                trans.append(new_tran)
    new_trans = [tran for tran in trans]
    if need_newstate == False:
        states.remove(new_state)
        for tran in trans:
            if tran.source == new_state.name:
                new_trans.remove(tran)
        accept_names.remove(new_state.name)
    #if len(trans) == len(rfa.trans):
        #states.remove(new_state)
        #accept_names.remove(new_state.name)
    comp_rfa = RFA(name, timed_alphabet, states, new_trans, initstate_name, accept_names)
    return comp_rfa

def complete_rfa_complement(rfa):
    """
        In our algorithm, the RFA is complete. So the complement operation just changes the acceptence of the states
    """
    name = "C_" + rfa.name
    states = copy.deepcopy(rfa.states)
    timed_alphabet = copy.deepcopy(rfa.timed_alphabet)
    trans = copy.deepcopy(rfa.trans)
    initstate_name = rfa.initstate_name
    accept_names = []
    for s in states:
        if s.accept == True:
            s.accept = False
        else:
            s.accept = True
            accept_names.append(s.name)
    comp_rfa = RFA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return comp_rfa

def rfa_product(rfa1, rfa2):
    name = 'P_'+rfa1.name+'_'+rfa2.name
    timed_alphabet = rfa1.timed_alphabet # has same timed alphabet
    reach_states = []
    temp_states = []
    final_states = []
    for state1 in rfa1.states:
        for state2 in rfa2.states:
            new_state_name = state1.name + '_' + state2.name
            new_state_init = False
            new_state_accept = False
            if state1.init == True and state2.init == True:
                new_state_init = True
            if state1.accept == True and state2.accept == True:
                new_state_accept = True
            new_state = State(new_state_name, new_state_init, new_state_accept)
            temp_states.append(new_state)
            if new_state_init == True:
                reach_states.append(new_state)
                final_states.append(new_state)
    trans = []
    while len(reach_states) > 0:
        rstate = reach_states.pop(0)
        statename1, statename2 = rstate.name.split('_')
        for tran1 in rfa1.trans:
            if tran1.source == statename1:
                target1 = tran1.target
                label1 = tran1.label
                nfnums1 = tran1.nfnums
                for tran2 in rfa2.trans:
                    if tran2.source == statename2:
                        target2 = tran2.target
                        label2 = tran2.label
                        nfnums2 = tran2.nfnums
                        new_nfnums = []
                        if label1 == label2:
                            new_label = label1
                            for i in nfnums1:
                                for j in nfnums2:
                                    if i == j:
                                        new_nfnums.append(i)
                            new_target = target1 + '_' + target2
                            if len(new_nfnums) > 0:
                                new_tran = RFATran(len(trans), rstate.name, new_target, new_label, new_nfnums)
                                trans.append(new_tran)
                                for state in temp_states:
                                    if state.name == new_target:
                                        if state not in final_states:
                                            reach_states.append(state)
                                            final_states.append(state)
    initstate_name = ""
    accept_names = []
    for state in final_states:
        if state.init == True:
            initstate_name = state.name
        if state.accept == True:
            accept_names.append(state.name)
    product_rfa = RFA(name, timed_alphabet, final_states, trans, initstate_name, accept_names)
    return product_rfa

def rfa_to_rta(rfa):
    name = rfa.name
    states = copy.deepcopy(rfa.states)
    sigma = [term for term in rfa.timed_alphabet]
    trans = []
    for tran in rfa.trans:
        tran_id = tran.id
        source = tran.source
        target = tran.target
        label = tran.label
        temp_constraints = [rfa.timed_alphabet[label][i].constraints[0] for i in tran.nfnums]
        constraints = unintersect_intervals(temp_constraints)
        new_tran = RTATran(tran_id, source, target, label, constraints)
        trans.append(new_tran)
    initstate_name = rfa.initstate_name
    accept_names = copy.deepcopy(rfa.accept_names)
    rta = RTA(name, sigma, states, trans, initstate_name, accept_names)
    return rta

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
    A,_ = buildRTA("test_automata/c.json")
    #A.show()
    AA = buildAssistantRTA(A)
    AA.show()
    print("-----------AA to FA-----------------------")
    AA_FA = rta_to_fa(AA, "receiving")
    AA_FA.show()
    print("------------------------------------------")
    partitioned_alphabet, bnlist_dict = alphabet_partitions(AA_FA.timed_alphabet)
    for key in partitioned_alphabet:
        print key
        for c in partitioned_alphabet[key]:
            c.show()
    print("-------------rfa------------------------------")
    AA_RFA = fa_to_rfa(AA_FA, partitioned_alphabet)
    AA_RFA.show()
    print("---------------comp---------------------------")
    AA_RFA_COMP = complete_rfa_complement(AA_RFA)
    AA_RFA_COMP.show()
    print("---------------rfa to rta-----------------------")
    AA_new = rfa_to_rta(AA_RFA_COMP)
    AA_new.show()

if __name__=='__main__':
	main()  
