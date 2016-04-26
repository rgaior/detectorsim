import numpy as np
import matplotlib.pyplot as plt

fLO = 5.15e9

fnames = ['easier61.txt','344.txt','norsat.txt']
legs = ['DMX241', 'GI301','Norsat8115']

for fname, leg in zip(fnames,legs):
    f = open(fname,'r')
    lines = f.readlines()
    freq = np.array([])
    power = np.array([])
    for l in lines[1:]:
        ls = l.split()
        freq = np.append(freq,float(ls[0]))
        power = np.append(power,float(ls[1]))
    if fname == 'norsat.txt':
        freq = freq/1000
    g = np.power(10,power/10)
    g = g/np.max(g)
    f = open(leg+'_n.txt','w')
    newf = freq*1e9
    newf = fLO - newf
    newf = newf[::-1]
    for fr, ngain in zip(newf,g):
        f.write(str(fr) + ' ' + str(ngain) + '\n')
    f.close()
