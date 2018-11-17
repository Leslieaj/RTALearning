#define the functions about equivalence query

from hypothesis import *
from fa import *

def findpath(rta, paths):
    """
        find paths one more step.
    """
    current_paths = [path for path in paths]
    onemorestep_paths = []
    for path in current_paths:
        for tran in rta.trans:
            temp_path = copy.deepcopy(path)
            if tran.source == path[len(path)-1]:
                temp_path.append(tran.target)
                onemorestep_paths.append(temp_path)
    return onemorestep_paths

def buildctx(rta, path, value):
    """
        The input path can reach a accept state.
        We build a ctx depending on the path.
    """
    tws = []
    for i in range(0, len(path)-1):
        for tran in rta.trans:
            if tran.source == path[i] and tran.target == path[i+1]:
                action = tran.label
                time = min_constraints_number(tran.constraints)
                tw = Timedword(action, time)
                tws.append(tw)
                break
    ctx = Element(tws,[value])
    return ctx
                
def findctx(rta, value):
    """
        1. find a counter example: a accept path of rta.
        2. the value is 0 or 1, it depends that if teacher do complement, it is 0.
    """
    ctx = Element([],[value])
    if len(rta.states) == 0 or len(rta.accept_names) == 0:
        return ctx
    else:
        initpath = [rta.initstate_name]
        current_paths = [initpath]
        #the length of the longest path is less than states numbers
        step = len(rta.states)-1
        while(step > 0):
            new_paths = findpath(rta, current_paths)
            step = step - 1
            current_paths = [p for p in new_paths]
            for path in new_paths:
                if path[len(path)-1] in rta.accept_names:
                    print path
                    ctx = buildctx(rta, path, value)
                    return ctx
    return ctx

def clean_rfa(rfa):
    initpath = [rfa.initstate_name]
    current_paths = [initpath]
    state_names = [state.name for state in rfa.states]
    reach_names = [rfa.initstate_name]
    step = len(rfa.states)-1
    while(step > 0):
        new_paths = findpath(rfa, current_paths)
        step = step - 1
        current_paths = [p for p in new_paths]
        for path in new_paths:
            if path[len(path)-1] not in reach_names:
                reach_names.append(path[len(path)-1])
    trans = copy.deepcopy(rfa.trans)
    temp_trans = copy.deepcopy(rfa.trans)
    for tran in trans:
        if (tran.source not in reach_names) or (tran.target not in reach_names):
            temp_trans.remove(tran)
    states = []
    accept_names = []
    for state in rfa.states:
        if state.name in reach_names:
            states.append(state)
        if state.name in rfa.accept_names:
            accept_names.append(state.name)
    cleanrfa =  RFA(rfa.name, rfa.timed_alphabet, states, temp_trans, rfa.initstate_name, accept_names) 
    return cleanrfa

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
    
    AADFA = rta_to_fa(AA, "receiving")
    print("----------------------T1--------------------------")
    T1 = Table(S,R,E)
    T1.show()
    print("----------------------EA1-------------------------")
    ea1 = buildEvidenceAutomaton(T1, sigma)
    ea1.show()
    print("----------------------H1--------------------------")
    H1 = buildhypothesis(ea1, 1)
    H1.show()
    print("----------------------ctx1------------------------")
    H1DFA = rta_to_fa(H1, "receiving")
    combined_alphabet = alphabet_combine(H1DFA.timed_alphabet, AADFA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    rH1DFA = fa_to_rfa(H1DFA, alphapartitions)
    rAADFA = fa_to_rfa(AADFA, alphapartitions)
    comp_rH1DFA = rfa_complement(rH1DFA)
    product1 = clean_rfa(rfa_product(comp_rH1DFA, rAADFA))
    product_rta1 = rfa_to_rta(product1)
    ctx1 = findctx(product_rta1, 1)
    print [tw.show() for tw in ctx1.tws], ctx1.value
    print("----------------------T2--------------------------")
    #ctx1 = tws3
    T2 = add_ctx(T1, ctx1.tws, AA)
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
    print("----------------------ctx2------------------------")
    H2DFA = rta_to_fa(H2, "receiving")
    combined_alphabet = alphabet_combine(H2DFA.timed_alphabet, AADFA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    rH2DFA = fa_to_rfa(H2DFA, alphapartitions)
    rAADFA = fa_to_rfa(AADFA, alphapartitions)
    comp_rAADFA = rfa_complement(rAADFA)
    product2 = clean_rfa(rfa_product(rH2DFA, comp_rAADFA))
    product_rta2 = rfa_to_rta(product2)
    #product_rta2.show()
    ctx2 = findctx(product_rta2, 0)
    print [tw.show() for tw in ctx2.tws], ctx2.value
    print("----------------------T4--------------------------")
    #ctx2 = tws6
    T4 = add_ctx(T3, ctx2.tws, AA)
    T4.show()
    print("----------------------EA3-------------------------")
    ea3 = buildEvidenceAutomaton(T4, sigma)
    ea3.show()
    print("----------------------H3--------------------------")
    H3 = buildhypothesis(ea3, 3)
    H3.show()
    print("----------------------ctx3------------------------")
    H3DFA = rta_to_fa(H3, "receiving")
    combined_alphabet = alphabet_combine(H3DFA.timed_alphabet, AADFA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    rH3DFA = fa_to_rfa(H3DFA, alphapartitions)
    rAADFA = fa_to_rfa(AADFA, alphapartitions)
    comp_rAADFA = rfa_complement(rAADFA)
    product3 = clean_rfa(rfa_product(rH3DFA, comp_rAADFA))
    product_rta3 = rfa_to_rta(product3)
    product_rta3.show()
    ctx3 = findctx(product_rta3, 0)
    print [tw.show() for tw in ctx3.tws], ctx3.value
    print("----------------------T5--------------------------")
    #ctx3 = tws8
    T5 = add_ctx(T4, ctx3.tws, AA)
    T5.show()
    print("----------------------T6--------------------------")
    T6 = make_consistent(T5, sigma, AA)
    T6.show()
    #print("----------------------T7--------------------------")
    #T7 = make_closed(T6, sigma, AA)
    #T7.show()
    #print("----------------------EA4-------------------------")
    #ea4 = buildEvidenceAutomaton(T7, sigma)
    #ea4.show()
    #print("----------------------H4--------------------------")
    #H4 = buildhypothesis(ea4, 4)
    #H4.show()
    #print("----------------------H_DFA4----------------------")
    #HDFA4 = rta_to_fa(H4, "receiving")
    #HDFA4.show()
    #print("----------------------AADFA----------------------")
    #AADFA = rta_to_fa(AA, "receiving")
    #AADFA.show()
    #print("---------------------partitions-------------")
    #combined_alphabet = alphabet_combine(HDFA4.timed_alphabet, AADFA.timed_alphabet)
    #alphapartitions = alphabet_partitions(combined_alphabet)
    #print("---------------------rH_DFA4---------------------")
    #rH_DFA4 = fa_to_rfa(HDFA4, alphapartitions)
    #rH_DFA4.show()
    #print("---------------------rAADFA----------------------")
    #rAADFA = fa_to_rfa(AADFA, alphapartitions)
    #rAADFA.show()
    #print("---------------------comp of rH_DFA4-------------")
    #comp_rH_DFA4 = rfa_complement(rH_DFA4)
    #comp_rH_DFA4.show()
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
    #print("---------------------product------------------------")
    #product4 = clean_rfa(rfa_product(comp_rH_DFA4, rAADFA))
    #product4.show()
    #print("---------------------product_rta4------------------------")
    #product_rta1 = fa_to_rta(rfa_to_fa(product1))
    #product_rta4 = rfa_to_rta(product4)
    #product_rta4.show()
    #print("---------------------findctx-------------------------")
    #ctx4 = findctx(product_rta4, 1)
    #print [tw.show() for tw in ctx4.tws], ctx4.value
    return 0

if __name__=='__main__':
	main()
