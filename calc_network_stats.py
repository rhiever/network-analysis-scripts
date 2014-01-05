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

You should have received a copy of the GNU General Public License along with the Network
Analysis Scripts library. If not, see http://www.gnu.org/licenses/.


calc_network_stats computes the following for the given network over a list of alpha
cutoff values:

* number of nodes in the network

* number of edges in the network

* average clustering coefficient

* average shortest path length between all nodes

* number of communities / clusters of nodes

* modularity value

It is recommended that you run subset_backbone_network on your edge list first with an
alpha cutoff of 1.0, so all edges are assigned a p-value.

"""

import sys
import networkx as nx
import community
import csv
from numpy import arange

if len(sys.argv) < 2:
	print("")
	print("Invalid parameters provided.")
	print("")
	print("Usage: python calc_network_stats.py EDGE_FILE_NAME")
	print("\tEDGE_FILE_NAME: The name of the file containing all edges for the network")
	print("")
	quit()

infilename = sys.argv[1]
outfilename = infilename.replace(".csv", "") + "-network-stats.csv"

pairWeight = {}

with open(outfilename, "w") as network_outfile:
    network_outfile.write("alpha,num_nodes,num_edges,avg_clustering_coeff,avg_shortest_path_length,num_communities,modularity_value\n")

    print("reading in edge list...")

    with open(infilename) as infile:
        for line in infile:
            line = line.replace("\n", "").split(",")
            srA = line[0]
            srB = line[1]
            weight = float(line[2])
            pval = float(line[3])

			# if both edges are present, only keep the strongest edge
            if (srB, srA) in pairWeight:
            	# replace the other edge if it is present but weaker
            	otherEdgeWeight = pairWeight[(srB, srA)][0]
                if weight > otherEdgeWeight:
                    pairWeight[(srB, srA)] = (weight, pval)
            else:
            	# otherwise just store the edge
                pairWeight[(srA, srB)] = (weight, pval)


    print("calculating network measures...")

	# create a list of alpha values on a logarithmic scale
    alphas = list(arange(1e-4, 1e-3, 1e-4))
    alphas.extend(list(arange(1e-3, 1e-2, 1e-3)))
    alphas.extend(list(arange(1e-2, 1e-1, 1e-2)))
    alphas.extend(list(arange(1e-1, 1e-0 + 0.00001, 1e-1)))

    for alpha in alphas:
        num_nodes = 0
        num_edges = 0
        avg_clustering_coeff = 0.0
        avg_shortest_path_length = 0.0
        num_communities = 0
        modularity_value = 0.0

        print("\talpha = " + str(alpha) + "...")

        edge_weights = []

        for (srA, srB) in pairWeight:
            weight = pairWeight[(srA, srB)][0]
            pval = pairWeight[(srA, srB)][1]

			# only keep significant edges according to the current alpha
            if pval < alpha:
                edge_weights.append((int(srA), int(srB), weight))

		# store the edge weights into a NetworkX graph
		cur_graph = nx.Graph()
        cur_graph.add_weighted_edges_from(edge_weights)

		# find the largest connected component
        if not nx.is_connected(cur_graph):
            sub_graphs = nx.connected_component_subgraphs(cur_graph)
            
            main_graph = sub_graphs[0]

            for sg in sub_graphs:
                if len(sg.nodes()) > len(main_graph.nodes()):
                    main_graph = sg

            cur_graph = main_graph
        

        # create separate file to save the degree of each node
        degrees = cur_graph.degree()
        
        with open(infilename.replace(".csv", "") + "-degree-dist-pval" + str(alpha) + ".csv", "w") as out_file:
            w = csv.DictWriter(out_file, degrees.keys())
            w.writeheader()
            w.writerow(degrees)
            
        # calculate number of nodes w/ degree > 0 and total number of edges
        num_nodes = len(cur_graph.nodes())
        num_edges = len(cur_graph.edges())

        # calculate clustering coefficients
        avg_clustering_coeff = nx.average_clustering(cur_graph)
        
        # calculate shortest paths
        avg_shortest_path_length = nx.average_shortest_path_length(cur_graph)
        
        # calculate communities and modularity value
        partition = community.best_partition(cur_graph)
        num_communities = len(set(partition.values()))
        modularity_value = community.modularity(partition, cur_graph)

        network_outfile.write(str(alpha) + "," + str(num_nodes) + "," + str(num_edges) + "," + str(avg_clustering_coeff) + "," + str(avg_shortest_path_length) + "," + str(num_communities) + "," + str(modularity_value) + "\n")
