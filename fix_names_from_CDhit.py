import os,sys
from Bio import SeqIO as seq

if __name__ == "__main__":
	if len(sys.argv) !=4:
		print("usage: python fix_name_from_CDhit.py CDhit_result.fa.cdhit GenusName SpeciesName")
		sys.exit()

	f = sys.argv[1]
	genus = sys.argv[2]
	species = sys.argv[3]
	
	fixed = open(genus +"_"+species+".fix.fa", "w")
	index = 1
	for cdhit in seq.parse(f, "fasta"):
		fixed.write(">"+genus+"_"+species+"@"+str(index)+'\n'+str(cdhit.seq).rstrip("*")+'\n')
		index +=1	

	fixed.close()



