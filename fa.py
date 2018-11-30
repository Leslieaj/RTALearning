#some definitions about finite automaton

from rta import *

class TimedLabel:
    def __init__(self, name="", label="", nfc = None):
        self.name = name
        self.label = label
        self.nfc = nfc
    def show(self):
        print self.name
        print self.label
        self.nfc.show()

    def __eq__(self, timedlabel):
        if self.label == timedlabel.label and nform_equal(self.nfc, timedlabel.nfc) == True:
            return True
        else:
            return False

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
        print "timed alphabet: (in normalform)"
        for term in self.timed_alphabet:
            print term
            print
            for timedlabel in self.timed_alphabet[term]:
                timedlabel.show()
                print
        print "State (name, init, accept)"
        for s in self.states:
            print s.name, s.init, s.accept
        print "transitions: (id, source, target, timed label(in normalform)): "
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
        print "transitions (id, source, target, label, normalform index in timed alphabet): "
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
        nfc = copy.deepcopy(tran.nfc)
        timed_label = TimedLabel("",label,nfc)
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
            if timedlabel.label == label:
                temp_set[label].append(timedlabel)
    return temp_set

def alphabet_combine(alphabet1, alphabet2):
    combined_alphabet = {} 
    for key in alphabet1:
        combined_alphabet[key] = alphabet1[key] + alphabet2[key]
    return combined_alphabet

def alphabet_partitions(timed_alphabet):
    alphapartitions = {}
    for key in timed_alphabet:
        nfpatitions = []
        for timedlabel in timed_alphabet[key]:
            nfpatitions = nforms_partitions(nfpatitions, timedlabel.nfc)
        alphapartitions[key] = nfpatitions
    return alphapartitions

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
            if nform_containedin(nf, tran.timedlabel.nfc) == True:
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

def has_deadstates(rfa):
    source_states = []
    for tran in rfa.trans:
        if tran.source not in source_states:
            source_states.append(tran.source)
    dead_states = []
    for s in rfa.states:
        if s.name not in source_states:
            if s.accept == False:
                dead_states.append(s)
    return len(dead_states)

def clean_deadstates(rfa):
    cleanrfa = copy.deepcopy(rfa)
    source_states = []
    for tran in cleanrfa.trans:
        if tran.source not in source_states:
            source_states.append(tran.source)
    dead_statesnames = []
    live_states = []
    for s in cleanrfa.states:
        if (s.name not in source_states) and s.accept == False:
            dead_statesnames.append(s.name)
        else:
            live_states.append(s)
    cleanrfa.states = live_states
    live_trans = []
    for tran in cleanrfa.trans:
        if (tran.target not in dead_statesnames) and (tran.source not in dead_statesnames):
            live_trans.append(tran)
    cleanrfa.trans = live_trans
    for tran, i in zip(cleanrfa.trans, range(0, len(cleanrfa.trans))):
        tran.id = i
    if len(cleanrfa.states) == 0:
        cleanrfa.initstate_name = ""
    if has_deadstates(cleanrfa) > 0:
        return clean_deadstates(cleanrfa)
    else:
        return cleanrfa

def rfa_to_fa(rfa):
    name = rfa.name
    states = copy.deepcopy(rfa.states)
    timed_alphabet = {}
    for term in rfa.timed_alphabet:
        timed_alphabet[term] = []
    trans = []
    for tran in rfa.trans:
        tran_id = tran.id
        source = tran.source
        target = tran.target
        label = tran.label
        nf = NForm([],[],1,1)
        for i in tran.nfnums:
            nf = nform_union(nf, rfa.timed_alphabet[label][i])
        timedlabel = TimedLabel("", label, nf)
        if timedlabel not in timed_alphabet[label]:
            timed_alphabet[label].append(timedlabel)
        new_tran = FATran(len(trans), source, target, timedlabel)
        trans.append(new_tran)
    initstate_name = rfa.initstate_name
    accept_names = copy.deepcopy(rfa.accept_names)
    fa = FA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return fa

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
        nf = NForm([],[],1,1)
        for i in tran.nfnums:
            nf = nform_union(nf, rfa.timed_alphabet[label][i])
        timedlabel = TimedLabel("", label, nf)
        temp_constraints = nform_to_union_intervals(timedlabel.nfc)
        constraints = unintersect_intervals(temp_constraints)
        nfc = union_intervals_to_nform(constraints)
        new_tran = RTATran(tran_id, source, target, label, constraints, nfc)
        trans.append(new_tran)
    initstate_name = rfa.initstate_name
    accept_names = copy.deepcopy(rfa.accept_names)
    rta = RTA(name, sigma, states, trans, initstate_name, accept_names)
    return rta

def nfa_to_dfa(rfa):
    name = rfa.name
    #initstate_name = rfa.initstate_name
    timed_alphabet = copy.deepcopy(rfa.timed_alphabet)
    newstate_list = []
    newstate_list.append([rfa.initstate_name])
    final_newstate = copy.deepcopy(newstate_list)
    f = {}
    statename_value = {}
    index = 0
    while len(newstate_list) > 0:
        temp_state = newstate_list.pop(0)
        index = index + 1
        state_name = str(index)
        statename_value[state_name] = temp_state
        f[state_name] = {}
        for term in timed_alphabet:
            for nf in timed_alphabet[term]:
                i = timed_alphabet[term].index(nf)
                f[state_name][term+'_'+str(i)] = []
                label_targetlist = []
                for tran in rfa.trans:
                    if tran.source in temp_state and term == tran.label and i in tran.nfnums:
                            label_targetlist.append(tran.target)
                f[state_name][term+'_'+str(i)].extend(label_targetlist)
                if label_targetlist not in final_newstate:
                    if len(label_targetlist) > 0:
                        newstate_list.append(label_targetlist)
                        final_newstate.append(label_targetlist)
    states = []
    for statename in f:
        init = False
        accept = False
        for sn in statename_value[statename]:
            if sn == rfa.initstate_name:
                init = True
            if sn in rfa.accept_names:
                accept = True
        new_state = State(statename, init, accept)
        states.append(new_state)

    refined_f = copy.deepcopy(f)
    for statename in refined_f:
        for label in refined_f[statename]:
            for key in statename_value:
                if refined_f[statename][label] == statename_value[key]:
                    refined_f[statename][label] = key
    trans = []
    for statename in refined_f:
        source = statename
        target_label = {}
        #label_target = {}
        for label in refined_f[statename]:
            #if not label_target.has_key(label):
                #label_target[label] = []
            if len(refined_f[statename][label]) > 0:
                new_target = refined_f[statename][label]
                if not target_label.has_key(new_target):
                    target_label[new_target] = []
                    target_label[new_target].append(label)
                else:
                    target_label[new_target].append(label)
        for target in target_label:
            labels = target_label[target]
            label_nfnums = {}
            for label_nfnum in labels:
                label, nfnum = label_nfnum.split('_')
                if not label_nfnums.has_key(label):
                    label_nfnums[label] = []
                    label_nfnums[label].append(int(nfnum))
                else:
                    label_nfnums[label].append(int(nfnum))
            for label in label_nfnums:
                nfnums = label_nfnums[label]
                if len(nfnums) > 0:
                    new_tran = RFATran(len(trans), source, target, label, nfnums)
                    trans.append(new_tran)
    initstate_name = ""
    accept_names = []
    for s in states:
        if s.init == True:
            initstate_name = s.name
        if s.accept == True:
            accept_names.append(s.name)
    d_rfa = RFA(name, timed_alphabet, states, trans, initstate_name, accept_names)
    return d_rfa

#In this tool, we do not need the kleen star of normalform, and in normal form k==1 and len(X2) <=1.
#So, we have a methods to transform a normalform to unintersection constraints
#then we can transform a transformed FA to a RTA
def nform_to_union_intervals(X):
    constraints = [c for c in X.x1]
    if len(X.x2) == 0:
        return constraints
    elif len(X.x2) == 1:
        min_value = X.x2[0].min_value
        max_value = "+"
        temp_guard = ""
        if X.x2[0].closed_min == True:
            temp_guard = "["
        else:
            temp_guard = "("
        temp_guard = temp_guard + min_value + "," + max_value + ")"
        temp_constraint = Constraint(temp_guard)
        constraints.append(temp_constraint)
        return constraints
    else:
        return None

def fa_to_rta(fa):
    temp_name = copy.deepcopy(fa.name)
    names = temp_name.split('_')
    name = names[len(names)-1]
    initstate_name = fa.initstate_name
    accept_names = [name for name in fa.accept_names]
    sigma = [term for term in fa.timed_alphabet]
    states = [state for state in fa.states]
    trans = []
    for tran in fa.trans:
        source = tran.source
        target = tran.target
        label = tran.timedlabel.label
        temp_constraints = nform_to_union_intervals(tran.timedlabel.nfc)
        constraints = unintersect_intervals(temp_constraints)
        nfc = union_intervals_to_nform(constraints)
        temp_tran = RTATran(tran.id, source, target, label, constraints, nfc)
        trans.append(temp_tran)
    rta = RTA(name, sigma, states, trans, initstate_name, accept_names)
    return rta

def main():
    print("---------------------a.json----------------")
    A,_ = buildRTA("a.json")
    A.show()
    print("-------------a_secret.json-----------------")
    AS,_ = buildRTA("a_secret.json")
    AS.show()
    print("------------A to fa------------------------")
    A_FA = rta_to_fa(A, "generation")
    A_FA.show()
    print("-----------A_secret to FA-----------------------")
    AS_FA = rta_to_fa(AS, "receiving")
    AS_FA.show()
    print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(A_FA.timed_alphabet, AS_FA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    #for key in alphapartitions:
        #print key
        #for nf in alphapartitions[key]:
            #nf.show()
            #print
    print("-------------------B: A to rfa--------------------")
    A_RFA = fa_to_rfa(A_FA, alphapartitions)
    A_RFA.show()
    print("-------------------B_secret: A_secret to rfa--------------------")
    AS_RFA = fa_to_rfa(AS_FA, alphapartitions)
    AS_RFA.show()
    print("-------------------B_secret_comp: B_secret complement--------------------")
    C_AS_RFA = rfa_complement(AS_RFA)
    C_AS_RFA.show()
    print("-------------------B x B_secret_comp----------------------")
    P_A_AS = rfa_product(A_RFA, C_AS_RFA)
    P_A_AS.show()
    print("-------------------clean rfa-----------------------")
    clean_P_A_AS = clean_deadstates(P_A_AS)
    clean_P_A_AS.show()
    print("-------------------Bns: rfa to fa----------------------")
    Bns_FA = rfa_to_fa(clean_P_A_AS)
    Bns_FA.show()

if __name__=='__main__':
	main()
