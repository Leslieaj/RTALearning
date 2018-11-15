#define the fucntions in the membership query

from rta import *

class Element():
    def __init__(self, tws=[], value=[]):
        self.tws = tws or []
        self.value = value or []

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

class Table():
    """
        observation table.
    """
    def __init__(self, S = None, R = None, E=[]):
        self.S = S
        self.R = R
        #if E is empty, it means that there is an empty action in E.
        self.E = E
    
    def is_closed(self):
        """
            1. determine whether the table is closed.
               For each r \in R there exists s \in S such that row(s) = row(r).
            2. return four values, the first one is a flag to show closed or not, 
               the second one is the new S and the third one is the new R,
               the last one is the list of the elements moved from R to S.
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

def make_closed(table, sigma, rta):
    flag, new_S, new_R, move = table.is_closed()
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
        #for stws in S_R_tws:
        for stws in S_tws:
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
    A = buildRTA("a.json")
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
    tws12 = [tws6] #(b,2)

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
    
    T3 = make_closed(T, sigma, AA)
    ctx2 = tws6
    T4 = add_ctx(T3, ctx2, AA)
    print("new_S:"+str(len(T4.S)))
    for s in T4.S:
        print [tw.show() for tw in s.tws], s.row()
    print("new_R:"+str(len(T4.R)))
    for r in T4.R:
        print [tw.show() for tw in r.tws], r.row()
    print len(T3.S), len(T4.S)
    print len(T3.R), len(T4.R)
    print len(T3.E), len(T4.E)
    print("-----------------------------------------------------")
    ctx3 = tws8
    T5 = add_ctx(T4, ctx3, AA)
    print("new_S:"+str(len(T5.S)))
    for s in T5.S:
        print [tw.show() for tw in s.tws], s.row()
    print("new_R:"+str(len(T5.R)))
    for r in T5.R:
        print [tw.show() for tw in r.tws], r.row()
    print len(T4.S), len(T5.S)
    print len(T4.R), len(T5.R)
    print len(T4.E), len(T5.E)

    #test_close(T, sigma, AA)
    #test_prefixes()

    return 0

if __name__=='__main__':
	main()
