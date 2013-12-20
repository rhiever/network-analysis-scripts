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


This script formats a list of edges into a format that Gephi can import.

The edge list must be formatted as follows:

node name 1,node name 2,edge weight

e.g.,

AskReddit,pics,5928
funny,AskReddit,9266


The script stores the output into a file with "-gephi" appended to the input file name.

"""

import sys

if len(sys.argv) < 2:
	print("")
	print("Invalid parameters provided.")
	print("")
	print("Usage: python gephi_reformat.py EDGE_FILE_NAME")
	print("\tEDGE_FILE_NAME: The name of the file containing all edges for the network")
	print("")
	quit()

with open(sys.argv[1]) as infile:
    outfilename = sys.argv[1].replace(".csv", "")
    outfilename += "-gephi.csv"
    with open(outfilename, "w") as outfile:
        outfile.write("Source,Target,Weight,Type\n")
        for line in infile:
            line = line.replace("\n", "").split(",")
            for field in line[:2]:
                outfile.write(str(field) + ",")
            outfile.write(line[2] + ",")
            outfile.write("Undirected\n")
