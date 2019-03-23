import sys

import time
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

def learn(AA, AADFA, sigma, file_pre):
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
    eq_number = 0
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
        eq_number = eq_number + 1
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
        print "*******************Failed .***********************"
    else:
        print "Succeed! The learned RTA is as follows."
        print
        target.show()
        print "---------------------------------------------------"
        print "Total time of learning: " + str(end-start)
        print "---------------------------------------------------"
        print "Time intervals simplification..."
        print
        print "The learned Canonical Real-time Automtaton: "
        print
        refine_rta_trans(target)
        target.show()
        print "---------------------------------------------------"
        print "Total time: " + str(end-start)
        print "The element number of S in the last table: " + str(len(table.S))
        print "The element number of R in the last table: " + str(len(table.R))
        print "The element number of E in the last table (excluding the empty-word): " + str(len(table.E))
        print "Total number of observation table: " + str(t_number)
        print "Total number of membership query: " + str((len(table.S)+len(table.R))*(len(table.E)+1))
        print "Total number of equivalence query: " + str(eq_number)
        print "*******************Successful !***********************"
        folder,fname = file_pre.split('/')
        with open(folder+'/result/'+fname + '_result.txt', 'w') as f:
            output = " ".join([str(end-start), str(len(table.S)), str(len(table.R)), str(len(table.E)), str(t_number), str((len(table.S)+len(table.R))*(len(table.E)+1)), str(eq_number), '\n'])
            f.write(output)
    return 0

def main():
    para = sys.argv
    filename = str(para[1])
    file_pre,_ = filename.split('.',1)
    A, sigma = buildRTA(filename)
    AA = buildAssistantRTA(A)
    #AADFA = rta_to_fa(A, "receiving")
    AADFA = rta_to_fa(AA, "receiving")
    learn(AA, AADFA, sigma, file_pre)
    return 0

if __name__=='__main__':
	main()

