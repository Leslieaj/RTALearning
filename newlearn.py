from membership import *
from equivalence import *

def main():
    A = buildRTA("a.json")
    AA = buildAssistantRTA(A)
    sigma = ["a", "b"]

    AADFA = rta_to_fa(AA, "receiving")
    
    tw1 = Timedword("a", 0)
    tw2 = Timedword("b", 0)
    tws0 = [] # empty
    tws1 = [tw1] # (a,0)
    tws2 = [tw2] # (b,0)
    e0 = Element(tws0,[])
    e1 = Element(tws1,[])
    e2 = Element(tws2,[])

    S = [e0]
    R = [e1,e2]
    E = []
    for s in S:
        fill(s, E, AA)
    for r in R:
        fill(r, E, AA)
    T1 = Table(S, R, E)
    t_number = 1
    print "Table " + str(t_number) + " is as follow."
    T1.show()
    print "--------------------------------------------------"
    equivalent = False
    table = copy.deepcopy(T1)
    h_number = 0
    target = None
    while equivalent == False:
        prepared = table.is_prepared()
        while prepared == False:
            flag_closed, new_S, new_R, move = table.is_closed()
            if flag_closed == False:
                temp = make_closed(new_S, new_R, move, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print "Table " + str(t_number) + " is as follow."
                table.show()
                print "--------------------------------------------------"
            flag_consistent, new_a, new_e_index = table.is_consistent()
            if flag_consistent == False:
                temp = make_consistent(new_a, new_e_index, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print "Table " + str(t_number) + " is as follow."
                table.show()
                print "--------------------------------------------------"
            flag_evi_closed, new_added = table.is_evidence_closed()
            if flag_evi_closed == False:
                temp = make_evidence_closed(new_added, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print "Table " + str(t_number) + " is as follow."
                table.show()
                print "--------------------------------------------------"
            prepared = table.is_prepared()
        ea = buildEvidenceAutomaton(table, sigma)
        #h_number = h_number + 1
        h_number = t_number
        h = buildhypothesis(ea, h_number)
        target = copy.deepcopy(h)
        equivalent, ctx = equivalence_query(h, AADFA)
        if equivalent == False:
            temp = add_ctx(table, ctx.tws, AA)
            table = temp
            t_number = t_number + 1
            print "Table " + str(t_number) + " is as follow."
            table.show()
            print "--------------------------------------------------"
    if target is None:
        print "Error! Learning Failed."
    else:
        print "Succeed! The learned RTA is as follows."
        target.show()
        

if __name__=='__main__':
	main()

