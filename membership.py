#define the fucntions in the membership query

from rta import buildRTA, buildAssistantRTA, Timedword

class Element():
    def __init__(self, tws=[], value=[]):
        self.tws = tws or []
        self.value = value or []
    
    def __eq__(self, element):
        if self.tws == element.tws and self.value == element.value:
            return True
        else:
            return False

    def get_tws_e(self, e):
        tws_e = [tw for tw in self.tws]
        if len(e) == 0:
            return tws_e
        else:
            for tw in e:
                tws_e.append(tw)
            return tws_e

    def row(self):
        return self.value
    
    def whichstate(self):
        state_name = ""
        for v in self.value:
            state_name = state_name+str(v)
        return state_name

class Table():
    """
        observation table.
    """
    def __init__(self, S = None, R = None, E=[]):
        self.S = S
        self.R = R
        #if E is empty, it means that there is an empty action in E.
        self.E = E

    def is_prepared(self):
        flag_closed, new_S, new_R, move = self.is_closed()
        flag_consistent, new_a, new_e_index = self.is_consistent()
        flag_evid_closed, new_added = self.is_evidence_closed()
        if flag_closed == True and flag_consistent == True and flag_evid_closed == True:
            return True
        else:
            return False

    def is_closed(self):
        """
            1. determine whether the table is closed.
               For each r \in R there exists s \in S such that row(s) = row(r).
            2. return four values, the first one is a flag to show closed or not, 
               the second one is the new S and the third one is the new R,
               the last one is the list of elements moved from R to S.
        """
        new_S = [s for s in self.S]
        new_R = [r for r in self.R]
        new_S_rows = [s.row() for s in new_S]
        move = []
        for r in self.R:
            flag = False
            for s in self.S:
                if r.row() == s.row():
                    flag = True
                    break
            if flag == False:
                if r.row() not in new_S_rows:
                    new_S.append(r)
                    new_R.remove(r)
                    move.append(r)
                    new_S_rows = [s.row() for s in new_S]
        if len(new_S) > len(self.S):
            return False, new_S, new_R, move
        else:
            return True, new_S, new_R, move        

    def is_consistent(self):
        """
            determine whether the table is consistent
            (if tws1,tws2 \in S U R, if a \in sigma* tws1+a, tws2+a \in S U R and row(tws1) = row(tws2), 
            then row(tws1+a) = row(tws2+a))
        """
        flag = True
        new_a = None
        new_e_index = None
        table_element = [s for s in self.S] + [r for r in self.R]
        for i in range(0, len(table_element)-1):
            for j in range(i+1, len(table_element)):
                if table_element[i].row() == table_element[j].row():
                    temp_elements1 = []
                    temp_elements2 = []
                    #print len(table_element[2].tws), [tw.show() for tw in table_element[2].tws]
                    for element in table_element:
                        #print "element", [tw.show() for tw in element.tws]
                        if is_prefix(element.tws, table_element[i].tws):
                            new_element1 = Element(delete_prefix(element.tws, table_element[i].tws), [v for v in element.value])
                            temp_elements1.append(new_element1)
                        if is_prefix(element.tws, table_element[j].tws):
                            #print "e2", [tw.show() for tw in element.tws]
                            new_element2 = Element(delete_prefix(element.tws, table_element[j].tws), [v for v in element.value])
                            temp_elements2.append(new_element2)
                    for e1 in temp_elements1:
                        for e2 in temp_elements2:
                            #print [tw.show() for tw in e1.tws], [tw.show() for tw in e2.tws]
                            if len(e1.tws) == 1 and len(e2.tws) == 1 and e1.tws == e2.tws:
                                if e1.row() == e2.row():
                                    pass
                                else:
                                    flag = False
                                    new_a = e1.tws
                                    for i in range(0, len(e1.value)):
                                        if e1.value[i] != e2.value[i]:
                                            new_e_index = i
                                            return flag, new_a, new_e_index
        return flag, new_a, new_e_index
    
    def is_evidence_closed(self):
        """
            determine whether the table is evidence-closed.
        """
        flag = True
        table_tws = [s.tws for s in self.S] + [r.tws for r in self.R]
        #new_R = [r for r in self.R]
        new_added = []
        for s in self.S:
            for e in self.E:
                temp_se = [tw for tw in s.tws] + [tw for tw in e]
                if temp_se not in table_tws:
                    table_tws.append(temp_se)
                    new_tws = temp_se
                    new_element = Element(new_tws,[])
                    #new_R.append(new_element)
                    new_added.append(new_element)
        if len(new_added) > 0:
            flag = False
        return flag, new_added

    def show(self):
        print("new_S:"+str(len(self.S)))
        for s in self.S:
            print [tw.show() for tw in s.tws], s.row()
        print("new_R:"+str(len(self.R)))
        for r in self.R:
            print [tw.show() for tw in r.tws], r.row()
        print("new_E:"+str(len(self.E)))
        for e in self.E:
            print [tw.show() for tw in e]

def make_closed(new_S, new_R, move, table, sigma, rta):
    #flag, new_S, new_R, move = table.is_closed()
    new_E = table.E
    closed_table = Table(new_S, new_R, new_E)
    table_tws = [s.tws for s in closed_table.S] + [r.tws for r in closed_table.R]
    for s in move:
        s_tws = [tw for tw in s.tws]
        for action in sigma:
            temp_tws = s_tws+[Timedword(action,0)]
            if temp_tws not in table_tws:
                temp_element = Element(temp_tws,[])
                fill(temp_element, closed_table.E, rta)
                closed_table.R.append(temp_element)
                table_tws = [s.tws for s in closed_table.S] + [r.tws for r in closed_table.R]
    return closed_table

def make_consistent(new_a, new_e_index, table, sigma, rta):
    #flag, new_a, new_e_index = table.is_consistent()
    #print flag
    new_E = [tws for tws in table.E]
    new_e = [tw for tw in new_a]
    if new_e_index > 0:
        e = table.E[new_e_index-1]
        new_e.extend(e)
    new_E.append(new_e)
    new_S = [s for s in table.S]
    new_R = [r for r in table.R]
    for i in range(0, len(new_S)):
        fill(new_S[i], new_E, rta)
    for j in range(0, len(new_R)):
        fill(new_R[j], new_E, rta)
    consistent_table = Table(new_S, new_R, new_E)
    return consistent_table

def make_evidence_closed(new_added, table, sigma, rta):
    #flag, new_added = table.is_evidence_closed()
    for i in range(0,len(new_added)):
        fill(new_added[i], table.E, rta)
    new_E = [e for e in table.E]
    new_R = [r for r in table.R] + [nr for nr in new_added]
    new_S = [s for s in table.S]
    evidence_closed_table = Table(new_S, new_R, new_E)
    return evidence_closed_table
        
def add_ctx(table, ctx, rta):
    """
        when receiving a counterexample ctx ( a timedwords), add it and its prefixes to R
        (except those already present in S)
    """
    pref = prefixes(ctx)
    S_tws = [s.tws for s in table.S]
    S_R_tws = [s.tws for s in table.S] + [r.tws for r in table.R]
    new_S = [s for s in table.S]
    new_R = [r for r in table.R]
    new_E = [e for e in table.E]
    for tws in pref:
        need_add = True
        for stws in S_R_tws:
        #for stws in S_tws:
            #if tws_equal(tws, stws):
            if tws == stws:
                need_add = False
        if need_add == True:
            temp_element = Element(tws,[])
            fill(temp_element, new_E, rta)
            new_R.append(temp_element)
    return Table(new_S, new_R, new_E)

def prefixes(tws):
    """
        return the prefixes of a timedwords. [tws1, tws2, tws3, ..., twsn]
    """
    prefixes = []
    for i in range(1, len(tws)+1):
        temp_tws = tws[:i]
        prefixes.append(temp_tws)
    return prefixes

def is_prefix(tws, pref):
    """
        determine whether the pref is a prefix of the timedwords tws
    """
    if len(pref) == 0:
        return True
    else:
        if len(tws) < len(pref):
            return False
        else:
            for i in range(0, len(pref)):
                if tws[i] == pref[i]:
                    pass
                else:
                    return False
            return True

def delete_prefix(tws, pref):
    """
        delete a prefix of timedwords tws, and return the new tws
    """
    if len(pref) == 0:
        return [tw for tw in tws]
    else:
        new_tws = tws[len(pref):]
        return new_tws

def fill(element, E, rta):
    if len(element.value) == 0:
        f = rta.is_accept(element.tws)
        element.value.append(f)
    #print len(element.value)-1, len(E)
    for i in range(len(element.value)-1, len(E)):
        temp_tws = element.tws + E[i]
        f = rta.is_accept(temp_tws)
        element.value.append(f)


#----------------------------------------------------------------------------------------#
#---------------------------------------TEST---------------------------------------------#
#----------------------------------------------------------------------------------------#

def test_close(table, sigma, rta):
    closed_T = make_closed(T, sigma, rta)
    print("new_S:"+str(len(closed_T.S)))
    for s in closed_T.S:
        print [tw.show() for tw in s.tws], s.row()
    print("new_R:"+str(len(closed_T.R)))
    for r in closed_T.R:
        print [tw.show() for tw in r.tws], r.row()
    print len(T.S), len(closed_T.S)
    print len(T.R), len(closed_T.R)
    print len(T.E), len(closed_T.E)

def test_add_ctx(table, ctx):
    return 0

def test_is_prefix():
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
    tws12 = [tws6] #(b,2)
    tws13 = [tw3,tw1,tw2]
    tws14 = [tw1,tw3]
    print is_prefix(tws14, tws1)
    #print is_prefix(tws4, tws3)
    #print is_prefix(tws3, tws4)
    #print is_prefix(tws4, tws1)
    #print is_prefix(tws3, tws0)
    #print is_prefix(tws0, tws0)
    #print is_prefix(tws0, tws10)
    #print is_prefix(tws11, tws10)
    #print is_prefix(tws13, tws4)
    
    #print [tw.show() for tw in delete_prefix(tws4, tws3)]
    #print [tw.show() for tw in delete_prefix(tws3, tws0)]
    #print [tw.show() for tw in delete_prefix(tws0, tws0)]
    #print [tw.show() for tw in delete_prefix(tws13, tws4)]

def test_prefixes():
    tw1 = Timedword("a", 0)
    tw2 = Timedword("b", 0)
    tw3 = Timedword("a", 5)
    tw4 = Timedword("b", 4)
    tw5 = Timedword("a", 7)
    tw6 = Timedword("b", 2)
    
    tws = [tw1, tw2, tw3, tw4]
    pref = prefixes(tws)
    for tws in pref:
        print [tw.show() for tw in tws]

#----------------------------------------------------------------------------------------#
#---------------------------------------END TEST-----------------------------------------#
#----------------------------------------------------------------------------------------#

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
    e3 = Element(tws3,[1])
    e4 = Element(tws4,[0,1,0,1])
    e5 = Element(tws5,[1,1,0,1])
    S = [e0]
    R = [e1,e2,e3]
    E = []
    T = Table(S,R,E)
    
    flag_closed, new_S, new_R, move = T.is_closed()
    T3 = make_closed(new_S, new_R, move, T, sigma, AA)
    T3.show()
    
    ctx2 = tws6
    T4 = add_ctx(T3, ctx2, AA)
    T4.show()
    print("----------------------T5--------------------------")
    ctx3 = tws8
    T5 = add_ctx(T4, ctx3, AA)
    T5.show()
    print("----------------------T6--------------------------")
    flag_consistent, new_a, new_e_index = T5.is_consistent()
    T6 = make_consistent(new_a, new_e_index, T5, sigma, AA)
    T6.show()  
    print("----------------------T7--------------------------")
    flag_closed, new_S, new_R, move = T6.is_closed()
    T7 = make_closed(new_S, new_R, move, T6, sigma, AA)
    T7.show()
    print("----------------------T8--------------------------")
    ctx4 = tws11
    T8 = add_ctx(T7, ctx4, AA)
    T8.show()
    test_is_prefix()
    #test_close(T, sigma, AA)
    #test_prefixes()
    return 0

if __name__=='__main__':
	main()
