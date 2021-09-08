import os,sys,glob
from Bio import SeqIO as Seq

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("usage: python singlecopy_from_OrthoFinder.py OrthoFinder_InputDIR Output_DIR Minimal_taxa"+'\n'+'\n')
		sys.exit



	inDIR = "./"+sys.argv[1] +"/"
	outDIR = sys.argv[2]

	try:
		if not(os.path.isdir(outDIR)):
			os.makedirs(os.path.join(outDIR))
	except OSError as e:
		if e.errno != errno.EEXIST:
			print("Fail to create output directory")
			raise


	f = open( glob.glob(inDIR + "OrthoFinder/Results_*/Orthogroups/Orthogroups.txt")[0] , "r")
	s = glob.glob(inDIR+"OrthoFinder/Results_*/Orthogroup_Sequences")[0]

	for line in f:
                line = line.rstrip('\n')
                line = line.split()
                taxon = []
                for index in range(1, len(line)):
                    taxon.append(  str(line[index].split("@")[0]))


                if len(taxon) == len(list(set(taxon))):
                    if len(taxon) >= int(sys.argv[3]):
                        result =  str(line[0].rstrip(":")) +".fa"
                        scopy = open(outDIR+"/"+result,"w")
                        for fa in Seq.parse(s+"/"+result ,"fasta"):
                            scopy.write(">"+str(str(fa.id).split("@")[0])+'\n'+str(fa.seq).rstrip("*")+'\n')

                            scopy.close()
				

