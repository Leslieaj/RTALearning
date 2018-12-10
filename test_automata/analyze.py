import numpy as np
import sys

def main():
    paras = sys.argv
    filenames = [str(paras[i]) for i in range(1,len(paras))]
    mem_result = []
    eq_result = []
    for filename in filenames:
        print filename
        text_lines = []
        with open(filename, 'r') as f:
            text_lines = f.readlines()
        lines = [line.strip('\n').rstrip(' ') for line in text_lines]
        #print lines
        num_strs = [strs.split(' ') for strs in lines]
        membership_num = [int(num_strs[i][5]) for i in range(0,len(num_strs))]
        equivalence_num = [int(num_strs[i][6]) for i in range(0,len(num_strs))]
        membership_num.sort()
        #print membership_num
        equivalence_num.sort()
        #print equivalence_num
        member_min_num = min(membership_num)
        member_max_num = max(membership_num)
        member_mean_num = np.mean(membership_num)
        member_median_num = np.median(membership_num)
        member = [member_min_num, member_max_num, float('%.2f' % member_mean_num) , member_median_num]
        mem_result.append(member)
        eq_min_num = min(equivalence_num)
        eq_max_num = max(equivalence_num)
        eq_mean_num = np.mean(equivalence_num)
        eq_median_num = np.median(equivalence_num)
        eq = [eq_min_num, eq_max_num, float('%.2f' % eq_mean_num), eq_median_num]
        eq_result.append(eq)
        #print member_min_num, member_max_num, member_mean_num, member_median_num
        #print member
        #print eq_min_num, eq_max_num, eq_mean_num, eq_median_num
        #print eq
    print "membership :"
    for element in mem_result:
        print element
    print "equivalence :"
    for element in eq_result:
        print element
    return 0

if __name__ == '__main__':
    main()
