#define the functions about equivalence query

from hypothesis import *
from fa import *

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
    print("----------------------H_DFA1----------------------")
    HDFA1 = rta_to_fa(H1, "receiving")
    HDFA1.show()
    print("----------------------AADFA----------------------")
    AADFA = rta_to_fa(AA, "receiving")
    AADFA.show()
    print("---------------------partitions-------------")
    combined_alphabet = alphabet_combine(HDFA1.timed_alphabet, AADFA.timed_alphabet)
    alphapartitions = alphabet_partitions(combined_alphabet)
    for key in alphapartitions:
        print key
        for nf in alphapartitions[key]:
            nf.show()
            print
    #print("---------------------rH_DFA1---------------------")
    rH_DFA1 = fa_to_rfa(HDFA1, alphapartitions)
    #rH_DFA1.show()
    print("---------------------rAADFA----------------------")
    rAADFA = fa_to_rfa(AADFA, alphapartitions)
    rAADFA.show()
    print("---------------------comp of rH_DFA1-------------")
    comp_rH_DFA1 = rfa_complement(rH_DFA1)
    comp_rH_DFA1.show()
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
    product = rfa_product(comp_rH_DFA1, rAADFA)
    product.show()
    return 0

if __name__=='__main__':
	main()
