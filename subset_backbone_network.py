"""
Copyright 2013 Randal S. Olson

This file is part of the Network Analysis Scripts library.

The Network Analysis Scripts library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Network Analysis Scripts library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar.
If not, see http://www.gnu.org/licenses/.
"""

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