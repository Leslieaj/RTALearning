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
            2. return three values, the first one is a flag to show closed or not, 
               the second one is the new S and the third one is the new R.
        """
        new_S = [s for s in self.S]
        new_R = [r for r in self.R]
        new_S_rows = [s.row() for s in new_S]
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
                    new_S_rows = [s.row() for s in new_S]
        if len(new_S) > len(self.S):
            return False, new_S, new_R
        else:
            return True, new_S, new_R       

def main():
    tw1 = Timedword("a", 3)
    tw2 = Timedword("b", 2.1)
    tw3 = Timedword("b", 3)
    tw4 = Timedword("a", 5)
    tw5 = Timedword("b", 7)
    tws0 = []
    tws1 = [tw1,tw2,tw3,tw4]
    tws2 = [tw4]
    tws3 = [tw4,tw3,tw5]
    tws4 = [tw3,tw4]
    tws5 = [tw4,tw3,tw4,tw5]
    e0 = Element(tws0,[0,1,0,1])
    e1 = Element(tws1,[0,0,0,1])
    e2 = Element(tws2,[1,0,0,1])
    e3 = Element(tws3,[1,1,0,1])
    e4 = Element(tws4,[0,1,0,1])
    e5 = Element(tws5,[1,1,0,1])
    S = [e0,e1]
    R = [e2,e3,e4,e5]
    T = Table(S,R,[])
    flag, new_S, new_R = T.is_closed()
    print flag
    print("new_S:")
    for s in new_S:
        print s.row()
    print("new_R:")
    for r in new_R:
        print r.row()
    print len(T.S)
    print len(T.R)
    print len(T.E)
    return 0

if __name__=='__main__':
	main()
