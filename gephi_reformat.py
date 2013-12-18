import sys

with open(sys.argv[1]) as infile:
    outfilename = sys.argv[1].replace(".csv", "")
    outfilename += "-gephi.csv"
    with open(outfilename, "w") as outfile:
        outfile.write("Source,Target,Weight,Type\n")
        #outfile.write("Source,Target,Type\n")
        for line in infile:
            line = line.replace("\n", "").split(",")
            for field in line[:2]:
                outfile.write(str(field) + ",")
            outfile.write(line[2] + ",")
            outfile.write("Undirected\n")
