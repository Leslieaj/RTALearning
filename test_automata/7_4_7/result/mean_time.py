import sys
import numpy as np

paras = sys.argv

filename = paras[1]

with open(filename, 'r') as f:
     text_lines = f.readlines()
     time = [float(text.split(' ')[0]) for text in text_lines]
     print(np.mean(time))
