#Generate rta randomly.

import random

class RTAGenerator:
    def __init__(self, statesnumber, sigmasize, partitionsize):
        self.size = statesnumber
        self.sigmasize = sigmasize
        self.partitionsize = partitionsize

    def random_state(self):
        states = []
        i = 0
        while i < self.size:
            i = i + 1
            states.append(str(i))
        init = str(1)
        acceptsize = random.randint(1,2)
        accept = random.sample(states, acceptsize)
        accept.sort()
        return states, init, accept

    def random_sigma(self):
        temp = "abcdefghijklmnopqrstuvwxyz"
        sigmalist = list(temp)[:self.sigmasize]
        return sigmalist

def main():
    g = RTAGenerator(4,4,3)
    print g.random_sigma()
    print g.random_state()
    return 0

if __name__=='__main__':
	main()  
