import sys

from membership import *
from equivalence import *

def init_table(sigma, rta):
    S = [Element([],[])]
    R = []
    E = []
    for action in sigma:
        new_tw = Timedword(action, 0)
        new_element = Element([new_tw],[])
        R.append(new_element)
    for s in S:
        fill(s, E, rta)
    for r in R:
        fill(r, E, rta)
    T = Table(S, R, E)
    return T

def main():
    para = sys.argv
    filename = str(para[1])
    A, sigma = buildRTA(filename)
    AA = buildAssistantRTA(A)
    AADFA = rta_to_fa(AA, "receiving")
    
    print "**************Start to learn ...*******************"
    start = time.time()
    T1 = init_table(sigma, AA)
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
    end = time.time()
    if target is None:
        print "Error! Learning Failed."
    else:
        print "Succeed! The learned RTA is as follows."
        target.show()
        print "---------------------------------------------------"
        print "Total time: " + str(end-start)
    return 0

if __name__=='__main__':
	main()

