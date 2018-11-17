#define the functions about equivalence query

from hypothesis import *
from fa import *

def findctx(rta, value):
    ctx = Element([],[value])
    if len(rta.states) == 0 or len(rta.accept_names) == 0:
        return ctx
    else:
        temp_states = [states for states in rta.states]
        init_state = None
        for s in temp_states:
            if s.init == True:
                init_state = copy.deepcopy(s)
                temp_states.remove(s)
                break
        tws = []
        reach_statenames = [init_state.name]
        current_statename = init_state.name
        for tran in rta.trans:
            if tran.source == current_statename:
                time = min_constraints_number(tran.constraints)
                tw = Timedword(tran.label, time)
                tws.append(tw)
                if tran.target in rta.accept_names:
                    ctx.tws = tws
                    return ctx
                    
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
    T3 = make_closed(T2, sigma, AA)
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
    print("----------------------T6--------------------------")
    T6 = make_consistent(T5, sigma, AA)
    T6.show()  
    print("----------------------T7--------------------------")
    T7 = make_closed(T6, sigma, AA)
    T7.show()
    print("----------------------EA4-------------------------")
    ea4 = buildEvidenceAutomaton(T7, sigma)
    ea4.show()
    print("----------------------H4--------------------------")
    H4 = buildhypothesis(ea4, 4)
    H4.show()
    print("----------------------H_DFA1----------------------")
    HDFA4 = rta_to_fa(H4, "receiving")
    HDFA4.show()
    print("----------------------AADFA----------------------")
    AADFA = rta_to_fa(AA, "receiving")
    AADFA.show()
    print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(HDFA4.timed_alphabet, AADFA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    for key in alphapartitions:
        print key
        for nf in alphapartitions[key]:
            nf.show()
            print
    #print("---------------------rH_DFA4---------------------")
    rH_DFA4 = fa_to_rfa(HDFA4, alphapartitions)
    #rH_DFA1.show()
    print("---------------------rAADFA----------------------")
    rAADFA = fa_to_rfa(AADFA, alphapartitions)
    rAADFA.show()
    print("---------------------comp of rH_DFA4-------------")
    comp_rH_DFA4 = rfa_complement(rH_DFA4)
    comp_rH_DFA4.show()
    #print("---------------------comp of rAADFA-----------------")
    #comp_rAADFA = rfa_complement(rAADFA)
    #comp_rAADFA.show()
    #print("--------------------rcH1----------------------------")
    #rcH1 = rfa_to_fa(comp_rH_DFA1)
    #rcH1.show()
    #print("---------------------rAA---------------------------")
    #rAA = rfa_to_fa(rAADFA)
    #rAA.show()
    #print("--------------------newcH1---------------------------")
    #newcH1 = fa_to_rta(rcH1)
    #newcH1.show()
    #print("---------------------newAA--------------------------")
    #newAA = fa_to_rta(rAA)
    #newAA.show()
    print("---------------------product------------------------")
    product4 = clean_deadstates(rfa_product(comp_rH_DFA4, rAADFA))
    product4.show()
    print("---------------------product_rta4------------------------")
    #product_rta1 = fa_to_rta(rfa_to_fa(product1))
    product_rta4 = rfa_to_rta(product4)
    product_rta4.show()
    return 0

if __name__=='__main__':
	main()
