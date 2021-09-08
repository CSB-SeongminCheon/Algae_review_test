import os,sys


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("usage: python prank_Wrapper.py inDIR")
		sys.exit()
	
	inDir = sys.argv[1].rstrip("/") +"/"
	file_end = "fa"
	
	finish = os.listdir(inDir)
	for i in os.listdir(inDir):
		if i[-len(file_end):]!=file_end: continue
		if i+".aln" in finish: continue

		#Replace U to X to avoid crash prank
		infile = open(inDir+i,"r")
		outfile = open(inDir+i+".tmp","w")
		for line in infile:
			if line[0] !=">":
				line = line.replace("U","X")
				line = line.replace("u","x")
			outfile.write(line)
		infile.close()
		outfile.close()
		
		out = inDir+i+".aln"
		cmd = "prank -d="+inDir+i+".tmp -o="+out+" -protein"
		print(cmd)
		os.system(cmd)
		os.system("rm "+inDir+i+".tmp")
		os.system("mv "+inDir+i+".aln.best.fas " + out)
