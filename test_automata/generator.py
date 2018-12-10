#Generate rta randomly.
import sys
import random
import math
import json
import io

class Tran:
    def __init__(self, tran_id = "", source = "", label = "", intervals = "", target = ""):
        self.tran_id = tran_id
        self.source = source
        self.label = label
        self.intervals = intervals
        self.target = target
        
    def show(self):
        return {self.tran_id : [self.source, self.label, self.intervals, self.target]}

class RTAGenerator:
    def __init__(self, name, statesnumber, sigmasize, partitionsize):
        self.name = name
        self.sigma = self.random_sigma(sigmasize)
        self.s, self.init, self.accept = self.random_states(statesnumber)
        self.tran,_ = self.random_trans(sigmasize, partitionsize)

    def random_states(self, statesnumber):
        states = []
        i = 0
        while i < statesnumber:
            i = i + 1
            states.append(str(i))
        init = str(1)
        floor = 1
        if int(math.floor(statesnumber / 5.0)) < 2:
            floor = 1
        else:
            floor = int(math.floor(statesnumber / 5.0))
        acceptsize = random.randint(floor,int(math.floor(statesnumber / 2.0))+1)
        accept = random.sample(states, acceptsize)
        accept.sort()
        return states, init, accept

    def random_sigma(self, sigmasize):
        temp = "abcdefghijklmnopqrstuvwxyz"
        sigmalist = list(temp)[:sigmasize]
        return sigmalist
    
    def random_trans(self, sigmasize, partitionsize):
        traveled = []
        while len(traveled) != len(self.s):
            trans = []
            tran_id = 0
            traveled = []
            untraveled = set('1')
            while len(untraveled) > 0:
                source = untraveled.pop()
                temp_trans, reach_states, tran_id = self.random_trans_source(tran_id, source, sigmasize, partitionsize)
                trans.extend(temp_trans)
                if len(temp_trans) > 0:
                    traveled.append(source)
                for state in reach_states:
                    if state not in traveled:
                        untraveled.add(state)
        return trans, traveled

    def random_trans_source(self, tran_id, source, sigmasize, partitionsize):
        tid = tran_id
        trans = []
        reach_states = set()
        labels = random.sample(self.sigma, random.randint(1, sigmasize))
        for label in labels:
            next_trans_num, intervals = self.random_intervals(partitionsize)
            target = random.sample(self.s, next_trans_num)
            for i in range(next_trans_num):
                temp_tran = Tran(str(tid), source, label, intervals[i], target[i])
                trans.append(temp_tran)
                tid = tid + 1
                if target[i] not in reach_states:
                    reach_states.add(target[i])
        return trans, reach_states, tid

    def random_intervals(self, partitionsize):
        intervals = []
        intervals_num =random.randint(1, int(math.floor(partitionsize / 2.0)))
        endpoint_set = set()
        endpoint_list = []
        count = intervals_num*2
        while len(endpoint_set) < count:
            endpoint = random.randint(0,20)
            endpoint_set.add(endpoint)
        endpoint_list = [i for i in endpoint_set]
        endpoint_list.sort()
        odd_index = []
        even_index = []
        if intervals_num == 0:
            intervals = []
        else:
            odd_index = endpoint_list[0::2]
            even_index = endpoint_list[1::2]
            for i in range(intervals_num-1):
                left = random.sample(['[','('], 1)
                right = random.sample([']',')'], 1)
                temp_interval = left[0] + str(odd_index[i]) + ',' + str(even_index[i]) + right[0]
                intervals.append(temp_interval)
            flag = random.randint(0,1)
            if flag == 0:
                even_index[intervals_num-1] = '+'
                left = random.sample(['[','('], 1)
                right = ')'
                temp_interval = left[0] + str(odd_index[intervals_num-1]) + ',' + even_index[intervals_num-1] + right
                intervals.append(temp_interval)
            else:
                left = random.sample(['[','('], 1)
                right = random.sample([']',')'], 1)
                temp_interval = left[0] + str(odd_index[intervals_num-1]) + ',' + str(even_index[intervals_num-1]) + right[0]
                intervals.append(temp_interval)
        return intervals_num, intervals
    
    def show(self):
        print "name :", self.name
        print "s :", self.s
        print "sigma :", self.sigma
        print "tran :"
        for t in self.tran:
            t_dict = t.show()
            print t_dict.keys()[0], t_dict.values()[0]
        print "init :", self.init
        print "accept :", self.accept

def validation(g):
    state_nums = len(g.s)
    sources = [state for state in g.accept]
    temp = [s for s in sources]
    states_set = set()
    for s in g.accept:
        states_set.add(s)
    i = 0
    while i < state_nums:
        i = i + 1
        for t in g.tran:
            temp = []
            if t.target in sources:
                temp.append(t.source)
                states_set.add(t.source)
                if len(states_set) == len(g.s):
                    return True
        sources = temp
    if len(states_set) < len(g.s):
        return False
    else:
        return True
"""
def buildjson(g):
    tran_dict = {}
    for t in g.tran:
        t_dict = t.show()
        tran_dict[t_dict.keys()[0]] = t_dict.values()[0]
    
    gdict = {"name":g.name, "s":g.s, "sigma":g.sigma, "tran":tran_dict, "init":g.init, "accept":g.accept}
    with open("test.json", "w") as f:
        json.dump(gdict,f)
"""

def buildjson(g, filename):
    tran_dict = {}
    for t in g.tran:
        t_dict = t.show()
        tran_dict[t_dict.keys()[0]] = t_dict.values()[0]
    
    gdict = {"name":g.name, "s":g.s, "sigma":g.sigma, "tran":tran_dict, "init":g.init, "accept":g.accept}
    text = json.dumps(gdict)
    formattext = jsonformat(text)
    with open(filename+'.json', 'w') as f:
        f.write(formattext)

def jsonformat(text):
    text_list = []
    left_brace_num = 0     # {
    right_brace_num = 0    # }
    bracket_num = 0 
    for i in range(len(text)):
        text_list.append(text[i])
        if text[i] == '[' and left_brace_num == 1:
            bracket_num = bracket_num + 1
        if text[i] == ']' and left_brace_num == 1:
            bracket_num = bracket_num - 1
        if text[i] == '{':
            left_brace_num = left_brace_num + 1
            if left_brace_num == 1:
                text_list.append('\n' + " "*4)
            else:
                bracket_num = 0
                text_list.append('\n' + " "*4 + "    "*(left_brace_num-1))
        if text[i] == '}':
            left_brace_num = left_brace_num - 1
        if text[i] == ',':
            if text[i-1] == ']' and left_brace_num == 2:
                if left_brace_num == 2:
                    text_list.append('\n' + " "*7)
                if left_brace_num == 1:
                    text_list.append('\n' + " "*3)
            elif text[i-1] == '}':
                text_list.append('\n' + " "*3)
                bracket_num = 0
            elif left_brace_num == 1 and bracket_num == 0:
                text_list.append('\n' + " "*3)
        if text[i] == ']':
            if text[i+1] == '}' and left_brace_num == 2:
                text_list.append('\n' + " "*4)
            if text[i+1] == '}' and left_brace_num == 1:
                text_list.append('\n')
    format_str = "".join(text_list)
    return format_str
    
def main():
    para = sys.argv
    filename = str(para[1])
    n, k, m = filename.split('_')
    g = RTAGenerator(filename,int(n),int(k),int(m))
    #g = RTAGenerator('30_2_3',30,2,3)
    #while validation(g) != True:
        #g = RTAGenerator('30_2_3',30,2,3)
    g.show()
    buildjson(g, filename)
    return 0

if __name__=='__main__':
	main()  
