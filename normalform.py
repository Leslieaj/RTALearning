#some defines about normal form of the union of unintersect intervals
# depended on Dima's paper "Real-time Automaton"

import time
import math
from interval import *

class NForm:
    def __init__(self, x1, x2, k, N):
        self.x1 = x1
        self.x2 = x2
        self.k = k
        self.N = N
    def isEmpty(self):
        if (self.x1 == None or len(self.x1) == 0) and (self.x2 == None or len(self.x2) == 0):
            return True
        else:
            return False
    def show(self):
        print "x1: "
        for c in self.x1:
            print c.show()
        print "x2: "
        for c in self.x2:
            print c.show()
        print "k: ", self.k
        print "N: ", self.N

class WNForm:
    def __init__(self, x1, x2, k):
        self.x1 = x1
        self.x2 = x2
        self.k = k
    def isEmpty(self):
        if (self.x1 == None or len(self.x1) == 0) and (self.x2 == None or len(self.x2) == 0):
            return True
        else:
            return False
    def show(self):
        print "x1: "
        for c in self.x1:
            print c.show()
        print "x2: "
        for c in self.x2:
            print c.show()
        print "k: ", self.k

def gcd(a, b):  
    #assert a > 0 and b > 0,'parameters must be greater than 0.'     
    while True:  
        if a >= b:  
            if a % b == 0:  
                return b  
            else:  
                a, b = a - b, b  
        else:  
            a, b = b, a  
  
def lcm(a, b):  
    #assert a > 0 and b > 0,'parameters must be greater than 0.'  
    return int(a * b / gcd(a, b))

def union_intervals_to_nform(uintervals):
    if len(uintervals) == 0:
        return NForm([],[],1,1)
    if len(uintervals) >= 1:
        x1 = unintersect_intervals(uintervals)
        k = 1
        constraint = x1[len(x1)-1]
        N = None
        x2 = []
        if constraint.max_value == '+':
            N = int(constraint.min_value)+1
            left,_ = constraint.guard.split(',')
            right = str(N) + ')'
            new_constraint = Constraint(left+','+right)
            x1 = x1[:-1]
            x1.append(new_constraint)
            x2.append(Constraint('['+str(N)+','+str(N+1)+')'))
        else:
            N = int(constraint.max_value)+1
        return NForm(x1,x2,k,N)

def nform_union(X, Y):
    m = lcm(X.k, Y.k)
    new_x1 = []
    new_x1.extend(X.x1)
    new_x1.extend(Y.x1)
    new_x1 = unintersect_intervals(new_x1)
    m_k_1 = m/X.k - 1
    m_l_1 = m/Y.k - 1
    new_x2 = []
    for i in range(m_k_1 + 1):
        k_constraint = Constraint('['+str(i * X.k)+','+str(i * X.k)+']')
        for constraint in X.x2:
            new_constraint = constraint + k_constraint
            new_x2.append(new_constraint)
    for i in range(m_l_1 + 1):
        l_constraint = Constraint('['+str(i * Y.k)+','+str(i * Y.k)+']')
        for constraint in Y.x2:
            new_constraint = constraint + l_constraint
            new_x2.append(new_constraint)
    new_x2 = unintersect_intervals(new_x2)
    wnform = WNForm(new_x1, new_x2, m)
    #return wnform
    nform = wnform_to_nform(wnform)
    return nform

def nform_complement(X):
    #weak normalform:x1 = comp(X.x1) join [0,Nk), x2 = comp(X.x2) join [Nk, (N+1)k), k = X.k
    #then transform it to normalform
    #x1
    complement_x1 = complement_intervals(X.x1)
    cover1 = Constraint('[' + '0' + ',' + str(X.N * X.k) + ')')
    wnform_x1 = []
    for c in complement_x1:
        temp_inter, flag_inter = intersect_constraint(c, cover1)
        if flag_inter == True:
            wnform_x1.append(temp_inter)
    wnform_x1 = unintersect_intervals(wnform_x1)
    #x2
    complement_x2 = complement_intervals(X.x2)
    cover2 = Constraint('[' + str(X.N * X.k) + ',' + str((X.N+1)*X.k) + ')')
    wnform_x2 = []
    for c in complement_x2:
        temp_inter, flag_inter = intersect_constraint(c, cover2)
        if flag_inter == True:
            wnform_x2.append(temp_inter)
    wnform_x2 = unintersect_intervals(wnform_x2)
    #k
    wnform_k = X.k
    wnform = WNForm(wnform_x1, wnform_x2, wnform_k)
    #return wnform
    # to normalform
    nform = wnform_to_nform(wnform)
    return nform

def nform_add(X, Y):
    #build wnform1: x1 = X.x1 + Y.x1, x2 = X.x1 + Y.x2, k = Y.k
    wnform1_x1 = []
    for c1 in X.x1:
        for c2 in Y.x1:
            temp = c1 + c2
            #print temp.show()
            if temp.isEmpty() == False:
                wnform1_x1.append(temp)
    wnform1_x1 = unintersect_intervals(wnform1_x1)
    wnform1_x2 = []
    for c1 in X.x1:
        for c2 in Y.x2:
            temp = c1 + c2
            #print temp.show()
            if temp.isEmpty() == False:
                wnform1_x2.append(temp)
    wnform1_x2 = unintersect_intervals(wnform1_x2)
    wnform1_k = Y.k
    wnform1 = WNForm(wnform1_x1, wnform1_x2, wnform1_k)
    #build wnform2: x1 = [], x2 = X.x2 + Y.x1, k = X.k
    wnform2_x1 = []
    wnform2_x2 = []
    for c1 in X.x2:
        for c2 in Y.x1:
            temp = c1 + c2
            if temp.isEmpty() == False:
                wnform2_x2.append(temp)
    wnform2_x2 = unintersect_intervals(wnform2_x2)
    wnform2_k = X.k
    wnform2 = WNForm(wnform2_x1, wnform2_x2, wnform2_k)
    #build wnform3: x1 = [], x2 = X.x2 + Y.x2, k = {X.k}* + {Y.k}*
    #then we transform it to: x1 = X.x2 + Y.x2 + B, x2 = X.x2 + Y.x2 + {lcm(X.k, Y.k)}, k = gcd(X.k, Y.k)
    #where B = {a \in Q| 0<=a<lcm(X.k, Y.k), a = l*X.k + m*Y.k, l,m \in N}
    B, B_dot = calculate_B(X.k, Y.k)
    wnform3_x1 = []
    for c1 in X.x2:
        for c2 in Y.x2:
            for c3 in B:
                temp1 = c1 + c2
                temp2 = temp1 + c3
                if temp2.isEmpty() == False:
                    wnform3_x1.append(temp2)
    wnform3_x1 = unintersect_intervals(wnform3_x1)
    ceil = lcm(X.k, Y.k)
    lcm_constraint = Constraint('['+str(ceil)+','+str(ceil)+']')
    wnform3_x2 = []
    for c1 in X.x2:
        for c2 in Y.x2:
            temp1 = c1 + c2
            temp2 = temp1 + lcm_constraint
            if temp2.isEmpty() == False:
                wnform3_x2.append(temp2)
    wnform3_x2 = unintersect_intervals(wnform3_x2)
    wnform3_k = gcd(X.k, Y.k)
    wnform3 = WNForm(wnform3_x1, wnform3_x2, wnform3_k)
    #return wnform1, wnform2, wnform3
    #transform the 3 weak normalform to normalform, then get their union, return the normalform of the union finally.
    nform1 = wnform_to_nform(wnform1)
    nform2 = wnform_to_nform(wnform2)
    nform3 = wnform_to_nform(wnform3)
    wn_1_U_2 = nform_union(nform1,nform2)
    n_1_U_2 = wnform_to_nform(wn_1_U_2)
    wn_1_U_2_U_3 = nform_union(n_1_U_2, nform3)
    n_1_U_2_U_3 = wnform_to_nform(wn_1_U_2_U_3)
    return n_1_U_2_U_3

def nform_relative_complement(X, Y):
    #X\Y = X inter comp(Y)
    comp_Y_nf = nform_complement(Y)
    X_sub_Y = nform_intersection(X, comp_Y_nf)
    return X_sub_Y

def nform_intersection(X, Y):
    comp_X_nf = nform_complement(X)
    comp_Y_nf = nform_complement(Y)
    comp_X_nf_U_comp_Y_nf = nform_union(comp_X_nf, comp_Y_nf)
    x_inter_Y = nform_complement(comp_X_nf_U_comp_Y_nf)
    return x_inter_Y

def nform_equal(X, Y):
    X_sub_Y = nform_relative_complement(X, Y)
    Y_sub_X = nform_relative_complement(Y,X)
    if X_sub_Y.isEmpty() == True and Y_sub_X.isEmpty() == True:
        return True
    else:
        return False

def nform_containedin(X, Y):
    #Is X subset of Y ?  X \ Y = \emptyset
    X_sub_Y = nform_relative_complement(X, Y)
    if X_sub_Y.isEmpty() == True:
        return True
    else:
        return False
    
def calculate_B(p, q):
    #B = {a \in Q| 0<=a<lcm(p, q), a = l*p + m*q, l,m \in N}
    ceil = lcm(p,q)
    l = 0
    m = 0
    B_dot = []
    while l*p < ceil:
        l = l + 1
    while m*q < ceil:
        m = m + 1
    for i in range(0, l+1):
        for j in range(0, m+1):
            if i*p + j*q < ceil:
                a= i*p + j*q
                #print a
                if a not in B_dot:
                    B_dot.append(a)
    B_dot.sort()
    B = []
    for a in B_dot:
        new_constraint = Constraint('['+str(a)+','+str(a)+']')
        B.append(new_constraint)
    return B, B_dot

def wnform_to_nform(X):
    if (len(X.x1) > 0 and X.x1[len(X.x1)-1].max_bn.value == '+') or (len(X.x2) > 0 and X.x2[len(X.x2)-1].max_bn.value == '+'):
        return wnform_to_nform_inf(X)
    else:
        return wnform_to_nform_fin(X)

def wnform_to_nform_inf(X):
    #if there is inf in x1 or x2 of wnform
    #build L, n, N
    L = 0
    L_bn = None
    if len(X.x1) > 0 and len(X.x2) == 0:
        L = X.x1[len(X.x1)-1].min_bn.getIntvalue()
        L_bn = X.x1[len(X.x1)-1].min_bn 
    elif len(X.x1) == 0 and len(X.x2) > 0:
        L = X.x2[len(X.x2)-1].min_bn.getIntvalue()
        L_bn = X.x2[len(X.x2)-1].min_bn        
    elif len(X.x1) > 0 and len(X.x2) > 0:
        if X.x1[len(X.x1)-1].min_bn.getIntvalue() < X.x2[len(X.x2)-1].min_bn.getIntvalue():
            L = X.x1[len(X.x1)-1].min_bn.getIntvalue()
            L_bn = X.x1[len(X.x1)-1].min_bn
        else:
            L = X.x2[len(X.x2)-1].min_bn.getIntvalue()
            L_bn = X.x2[len(X.x2)-1].min_bn
    else:
        return NForm([],[],1,1)        
    n = int(math.floor(L/X.k))
    N = L + 1
    #build z1
    z1_list = []
    z1_list.extend(X.x1)
    for i in range(0, n+1):
        ik_constraint = Constraint('[' + str(i*X.k) + ',' + str(i*X.k) + ']')
        for c in X.x2:
            new_constraint = c + ik_constraint
            z1_list.append(new_constraint)
    z1_list.append(Constraint(L_bn.getbn()+','+str(N)+')'))
    z1_list = unintersect_intervals(z1_list)
    z1 = []
    cover = Constraint('['+'0'+','+str(N)+')')
    for c in z1_list:
        temp_inter, flag_inter = intersect_constraint(c, cover)
        if flag_inter == True:
            z1.append(temp_inter)
    z1 = unintersect_intervals(z1)
    #build z2, k
    z2 = Constraint('['+str(N)+','+str(N+1)+']')
    nform_k = 1
    #get nform
    nform = NForm(z1,z2,nform_k,N)
    return nform

def wnform_to_nform_fin(X):
    #if there is no inf in x1 or x2 of wnform
    M = 0   
    if len(X.x1) > 0 and len(X.x2) == 0:
        M = X.x1[len(X.x1)-1].max_bn.getIntvalue() 
    elif len(X.x1) == 0 and len(X.x2) > 0:
        M = X.x2[len(X.x2)-1].max_bn.getIntvalue()       
    elif len(X.x1) > 0 and len(X.x2) > 0:
        if X.x1[len(X.x1)-1].max_bn.getIntvalue() > X.x2[len(X.x2)-1].max_bn.getIntvalue():
            M = X.x1[len(X.x1)-1].max_bn.getIntvalue()
        else:
            M = X.x2[len(X.x2)-1].max_bn.getIntvalue()
    else:
        return NForm([],[],1,1)
    n = int(math.floor(M/X.k))+1
    #print M, n
    #build z1
    z1_list = []
    z1_list.extend(X.x1)
    temp_z1_list = []
    for i in range(0, (n-1)+1):
        ik_constraint = Constraint('['+str(i*X.k)+','+str(i*X.k)+']')
        for c in X.x2:
            new_constraint = c + ik_constraint
            temp_z1_list.append(new_constraint)
    cover1 = Constraint('['+'0'+','+str(n*X.k)+')')
    for c in temp_z1_list:
        temp_inter, flag_inter = intersect_constraint(c, cover1)
        if flag_inter == True:
            z1_list.append(temp_inter)
    z1_list = unintersect_intervals(z1_list)
    #build z2
    z2_list = []
    temp_z2_list = []
    for i in range(1, n+1):
        ik_constraint = Constraint('['+str(i*X.k)+','+str(i*X.k)+']')
        for c in X.x2:
            new_constraint = c + ik_constraint
            temp_z2_list.append(new_constraint)
    cover2 = Constraint('['+str(n*X.k)+','+str((n+1)*X.k)+')')
    for c in temp_z2_list:
        temp_inter, flag_inter = intersect_constraint(c, cover2)
        if flag_inter == True:
            z2_list.append(temp_inter)
    z2_list = unintersect_intervals(z2_list)    
    #build k, N
    nform_k = X.k
    nform_N = n
    #get nform
    nform = NForm(z1_list,z2_list,nform_k,nform_N)
    return nform

def nforms_partitions(nfpartitions, X):
    init_partitions = None
    if len(nfpartitions) == 0:
        init_partitions = [union_intervals_to_nform([Constraint("[0,+)")])]
    else:
        init_partitions = copy.deepcopy(nfpartitions)
    final_partitions = []
    for nf in init_partitions:
        temp_inter = nform_intersection(nf, X)
        if temp_inter.isEmpty() == False:
            final_partitions.append(temp_inter)
        temp_rc = nform_relative_complement(nf, X)
        if temp_rc.isEmpty() == False:
            final_partitions.append(temp_rc)
    return final_partitions

def nform_star(X):
    x1_allpoints = True
    x2_allpoints = True
    for c in X.x1:
        if c.isPoint() == False:
            x1_allpoints = False
            break
    for c in X.x2:
        if c.isPoint() == False:
            x2_allpoints = False
            break
    allpoints = x1_allpoints and x2_allpoints
    if allpoints == True:
        return nform_star_allpoints(X)
    else:
        return nform_star_nonpoints(X, x1_allpoints, x2_allpoints)

def nform_star_allpoints(X):
    #x1*
    nform1 = points_star(X.x1)
    #x2 to nf
    temp_nform1 = union_intervals_to_nform(X.x2)
    #(x2 U {k})*
    points_list = []
    points_list.extend(X.x2)
    #points_list = copy.deepcopy(X.x2)
    k_constraint = Constraint('['+str(X.k)+','+str(X.k)+']')
    if k_constraint not in points_list:
        points_list.append(k_constraint)
    temp_nform2 = points_star(points_list)
    # x2 + (x2 U {k})*, both normalform
    temp_nform = nform_add(temp_nform1, temp_nform2)
    #{0} to nf
    floor_nform = NForm([Constraint("[0,0]")],[],1,1)
    #(x2+{k}*)* == {0} U (x2 + (x2 U {k})*), all normalform
    nform2 = nform_union(floor_nform, temp_nform)
    #X* = x1* + (x2+{k}*)*
    nf = nform_add(nform1, nform2)
    return nf

def points_star(points_list):
    #star of empty set is [0,0]
    if len(points_list) == 0:
        return NForm([Constraint("[0,0]")],[],1,1)
    elif len(points_list) == 1: # there is just one point, but we can see as two same points
        pointnum = int(points_list[0].min_value)
        return twopoints_star(pointnum, pointnum)
    else:
        pointnum = int(points_list[0].min_value)
        temp_nform = twopoints_star(pointnum, pointnum)
        for i in range(1,len(points_list)):
            temp_num = int(points_list[i].min_value)
            #easier, but may get very large k and N
            #temp_nform = nform_add(temp_nform, twopoints_star(temp_num, temp_num))
            if temp_num == 0:
                continue
            wnform1 = WNForm([], temp_nform.x1, temp_num)
            nform1 = wnform_to_nform(wnform1)
            wnform2_x1 = []
            B,_ = calculate_B(temp_nform.k, temp_num)
            for c1 in temp_nform.x2:
                for c2 in B:
                    temp = c1+c2
                    if temp.isEmpty() == False:
                        wnform2_x1.append(temp)
            wnform2_x1 = unintersect_intervals(wnform2_x1)
            wnform2_x2 = []
            lcm_constraint = Constraint('['+str(lcm(temp_nform.k, temp_num))+','+str(lcm(temp_nform.k, temp_num))+']')
            for c in temp_nform.x2:
                temp = c + lcm_constraint
                if temp.isEmpty() == False:
                    wnform2_x2.append(temp)
            wnform2_x2 = unintersect_intervals(wnform2_x2)
            wnform2_k = gcd(temp_nform.k, temp_num)
            wnform2 = WNForm(wnform2_x1, wnform2_x2, wnform2_k)
            nform2 = wnform_to_nform(wnform2)
            temp_nform = nform_union(nform1, nform2)
        return temp_nform

def twopoints_star(p, q):
    if p == 0 and q == 0:
        return NForm([Constraint("[0,0]")],[],1,1)
    elif p == 0 and q > 0:
        return twopoints_star(q,q)
    elif p > 0 and q == 0:
        return twopoints_star(p,p)
    else:
        x1,_ = calculate_B(p, q)
        x2 = [Constraint('['+str(lcm(p,q))+','+str(lcm(p,q))+']')]
        k = gcd(p,q)
        wnform = WNForm(x1, x2, k)
        #return wnform
        nform = wnform_to_nform(wnform)
        return nform

def nform_star_nonpoints(X, x1_allpoints, x2_allpoints):
    flag = 0
    zero_constraint = Constraint("[0,0]")
    temp_intervals = []
    temp_intervals.extend(X.x1)
    temp_intervals.extend(X.x2)
    if zero_constraint in temp_intervals:
        temp_intervals.remove(zero_constraint)
    if len(temp_intervals) == 0:
        return NForm([zero_constraint],[],1,1)
    else:
        low = temp_intervals[0]
        # if low = <0, a> (a>0), so  we remove [0,0], then low = (0, a>. 
        #The min low_bound is still 0, so We donot need to do that, just see the value is 0 or not.
        if low.min_bn.value == '0': 
            flag = 0
        else:
            flag = int(low.min_bn.value)
    if len(X.x2) > 0:
        flag2 = int(X.x2[0].min_value)
    else:
        flag2 = 1 # unuseful
    if flag == 0:
        nform_x1 = [Constraint("[0,1)")]
        nform_x2 = [Constraint("[1,2)")]
        nform_k = 1
        nform_N = 1
        return NForm(nform_x1, nform_x2, nform_k, nform_N)
    if flag > 0:
        #get minmal M
        allintervals = []
        allintervals.extend(X.x1)
        allintervals.extend(X.x2)
        M = MAXVALUE
        for c in allintervals:
            a = int(c.min_value)
            b = c.max_bn.getIntvalue()
            if 0 < a and a < b: # 0 < a < b
                temp_m = int(math.ceil(a * (int(math.floor(a/(b-a))) + 1))) + 1
                if temp_m < M:
                    M = temp_m
        #calculate Y
        Y = []
        cover = Constraint('['+'0'+','+str(M)+')')
        if X.N * X.k >= M:
            for c in X.x1:
                temp_inter, flag_inter = intersect_constraint(c, cover)
                if flag_inter == True:
                    Y.append(temp_inter)
            Y = unintersect_intervals(Y)
        else:
            temp = []
            temp.extend(X.x1)
            n = int(math.ceil(M/flag2))
            for i in range(0, n+1):
                k_constraint = Constraint('['+str(i*X.k)+','+str(i*X.k)+']')
                for c in X.x2:
                    new_constraint = c + k_constraint
                    if new_constraint.isEmpty() == False:
                        temp.append(new_constraint)
            for c in temp:
                temp_inter, flag_inter = intersect_constraint(c, cover)
                if flag_inter == True:
                    Y.append(temp_inter)
            Y = unintersect_intervals(Y)
        #calculate z1
        z1 = []
        Y_bound = int(math.ceil(M/flag))
        temp_z1 = []        
        zero_constraint = Constraint("[0,0]")
        temp_z1 = [zero_constraint]
        num = Y_bound
        #start = time.time()
        index = 0
        while num > 0:
            num = num - 1
            temp = copy.deepcopy(temp_z1)
            for i in range(index, len(temp)):
                for c2 in Y:
                    new_constraint = temp[i] + c2
                    if new_constraint.isEmpty() == False and new_constraint not in temp:
                        temp_z1.append(new_constraint) 
            index = len(temp)  
        #end = time.time()
        #print end-start
        """
        start = time.time()
        temp_z1 = horner(Y, Y_bound)
        end = time.time()
        print end-start
        """
        #start = time.time()
        for c in temp_z1:
            temp_inter, flag_inter = intersect_constraint(c, cover)
            if flag_inter == True:
                z1.append(temp_inter)
        #end = time.time()
        #print end-start
        start = time.time()
        z1 = unintersect_intervals(z1)
        #end = time.time()
        #print end-start
        #calculate z2
        z2 = [Constraint('['+str(M)+','+str(M+1)+')')]
        nform_k = 1
        nform_N = M
        nform = NForm(z1,z2,nform_k,nform_N)
        return nform

def horner(Y, num):
    empty_list = []
    zero_constraint = Constraint("[0,0]")
    i = 1
    poly = []
    while i < num + 2:
        i = i+1
        temp = copy.deepcopy(poly)
        for c1 in temp:
            for c2 in Y:
                new_constraint = c1 + c2
                if new_constraint.isEmpty() == False and (new_constraint not in temp):
                    poly.append(new_constraint)
        if zero_constraint not in poly:
            poly.append(zero_constraint)
    return poly

def main():
    c1 = Constraint("[4,5]")
    c2 = Constraint("[6,7)")
    c3 = Constraint("[3,5]")
    c4 = Constraint("[0,1)")
    c5 = Constraint("(8,+)")
    l1 = [c2,c1,c5,c4,c3]
    
    c6 = Constraint("[2,2]")
    c7 = Constraint("[3,4]")
    c8 = Constraint("(5,7]")
    c9 = Constraint("[12,13)")
    l2 = [c7,c9,c6,c8]
    
    print("------------------nf1--------------------")
    nf1 = union_intervals_to_nform(l1)
    nf1.show()
    print("------------------nf2--------------------")
    nf2 = union_intervals_to_nform(l2)
    nf2.show()
    print("-------------nf1 U nf2-------------------")
    u_nf1_2 = nform_union(nf1, nf2)
    u_nf1_2.show()
    print("--------------calculate_B----------------")
    p = 1
    q = 1
    B, B_dot = calculate_B(p,q)
    for c in B:
        print c.show()
    print B_dot    
    print("-------------nf1 complement--------------")
    comp_nf1 = nform_complement(nf1)
    comp_nf1.show()
    print("-------------nf2 complement--------------")
    comp_nf2 = nform_complement(nf2)
    comp_nf2.show()
    #print("------------u_nf1_2 to nform-------------")
    #nf1_2_nf = wnform_to_nform(u_nf1_2)
    #nf1_2_nf.show()
    print("--------------nf1 + nf2------------------")
    nform12 = nform_add(nf1,nf2)
    nform12.show()
    print("----------nf1 inter nf2------------------")
    nf1_inter_nf2 = nform_intersection(nf1, nf2)
    nf1_inter_nf2.show()
    print("----------u_nf1_2 \ nf1 -----------------")
    nf_12_rc_1 = nform_relative_complement(u_nf1_2, nf1)
    nf_12_rc_1.show()
    print("----------u_nf1_2 \ nf2 -----------------")
    nf_12_rc_2 = nform_relative_complement(u_nf1_2, nf2)
    nf_12_rc_2.show()
    print("----------partitions nf1 nf2---------------")
    nfpartitions1 = nforms_partitions([], nf1)
    nfpartitions12 = nforms_partitions(nfpartitions1, nf2)
    for nf in nfpartitions12:
        print nfpartitions12.index(nf)
        nf.show()
        print 
    print("-------------nform equal-----------------")
    print nform_equal(nf1, nf2)
    print nform_equal(nf2, nf2)
    print nform_equal(wnform_to_nform(nf2), nf2)
    print("-----------------test--------------------")
    p1 = Constraint("[1,1]")
    p2 = Constraint("[2,2]")
    p3 = Constraint("[3,3]")
    p4 = Constraint("[7,7]")
    pnform = points_star([p2])
    pnform.show()
    zero_point = union_intervals_to_nform([Constraint("[0,0]")])
    zero_point.show()
    print("----------------------X* points-----------------")
    px1 = NForm([Constraint("[0,0]")],[],1,1)
    star1 = nform_star(px1)
    star1.show()
    print("-----------------")
    px1.show()
    #px2 = NForm([Constraint("[2,3]"), Constraint("(4,7]")],[],1,8)
    #star2 = nform_star(px2)
    #star2.show()

if __name__=='__main__':
	main()
