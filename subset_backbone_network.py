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


subset_backbone_network.py implements the graph edge reduction algorithm introduced in:

M. Angeles Serrano, Marian Boguna, and Alessandro Vespignani
Extracting the multiscale backbone of complex weighted networks
PNAS 2009 106 (16) 6483-6488

The algorithm takes as input a list of undirected edges in the graph and the alpha
cutoff value that an edge must have to be maintained. The edge list must be formatted
as follows:

node name 1,node name 2,edge weight

e.g.,

AskReddit,pics,5928
funny,AskReddit,9266


The algorithm stores all significant edges, their normalized weights, and the p-value for
the edge in an output file with "backbone-network-pval" appended to the end of the input
file name. Example output:

AskReddit,pics,0.4,0.00109
funny,AskReddit,0.31,0.0095

"""

from collections import defaultdict
from scipy.integrate import quad
import sys

if len(sys.argv) < 3:
	print("")
	print("Invalid parameters provided.")
	print("")
	print("Usage: python subset_backbone_network.py EDGE_FILE_NAME ALPHA_CUTOFF")
	print("\tEDGE_FILE_NAME: The name of the file containing all edges for the network")
	print("\tALPHA_CUTOFF: The level of significance that an edge must have to be maintained")
	print("")
	quit()

infilename = sys.argv[1]
siglevel = float(sys.argv[2])
outfilename = infilename.replace(".csv", "") + "-backbone-network-pval" + str(siglevel) + ".csv"

weights = defaultdict(list)

with open(infilename) as infile:
    for line in infile:
        sline = line.replace("\n", "").split(",")
        nodeA = sline[0]
        nodeB = sline[1]
        try:
            W = float(sline[2])
            
        # if the weight isn't real valued, print the problem line and stop
        except:
            print("Error: edge does not have a real valued weight.")
            print(sline)
            quit()
        
		if [nodeB, W] not in weights[nodeA]:
			weights[nodeA].append([nodeB, W])
		if [nodeA, W] not in weights[nodeB]:
			weights[nodeB].append([nodeA, W])


integrand = lambda x,k : (1 - x) ** (k - 2)

with open(outfilename, "w") as outfile:
    for nodeA in weights:

        print "computing edges for " + str(nodeA) + "..."
        
        k = len(weights[nodeA])
        weight_sum = 0.0

        if k > 1:
            
            # sum all of the edge weights for the current node
            for other in weights[nodeA]:
                weight_sum += other[1]
                
            for other in weights[nodeA]:
                nodeB = other[0]
                
                # normalize the edge weight between nodeA and nodeB
                W = other[1] / weight_sum
                
                # compute the probability of this edge happening by chance
                pval = 1.0 - (k - 1.0) * quad(integrand, 0.0, W, args=(k))[0]
                
                # only save the edge if the probability of this edge happening is lower
                # than the specified significance cutoff
                if pval < siglevel:
                    outfile.write(nodeA + "," + nodeB + "," + str(W) + "," + str(pval) + "\n")
