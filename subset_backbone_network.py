from collections import defaultdict
from scipy.integrate import quad
from math import log
import sys

infilename = sys.argv[1]
siglevel = float(sys.argv[2])
outfilename = infilename.replace(".csv", "") + "-backbone-network-pval" + str(siglevel) + ".csv"

weights = defaultdict(list)

with open(infilename) as infile:
    for line in infile:
        sline = line.replace("\n", "").split(",")
        subA = sline[0]
        subB = sline[1]
        try:
            W = float(sline[2])
        except:
            print sline
            quit()
        if W != 1.0:
            if [subB, W] not in weights[subA]:
                weights[subA].append([subB, W])
            if [subA, W] not in weights[subB]:
                weights[subB].append([subA, W])




integrand = lambda x,k : (1 - x) ** (k - 2)

with open(outfilename, "w") as outfile:
    for subA in weights:

        print "calculating edges for " + str(subA) + "..."
        
        k = len(weights[subA])
        weight_sum = 0.0

        if k > 1:
            
            for other in weights[subA]:
                weight_sum += other[1]
                
            for other in weights[subA]:
                subB = other[0]
                W = other[1] / weight_sum
                
                pval = 1.0 - (k - 1.0) * quad(integrand, 0.0, W, args=(k))[0]
                
                if pval < siglevel:
                    #outfile.write(subA + "," + subB + "," + str(other[1]) + "," + str(pval) + "\n")
                    outfile.write(subA + "," + subB + "," + str(W) + "," + str(pval) + "\n")
