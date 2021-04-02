import os,sys
from Bio import SeqIO as Seq


def Concat(clnDir, aln_len, minTaxa,outname):
	Min_len = int(aln_len)
	Min_taxa = int(minTaxa)
	
	print "Filtering orthologous matrix"
	select=[]
	for cln in os.listdir(clnDir):
		if cln.endswith(".aln-cln"):
			Seqlist = list(Seq.parse( clnDir+cln , "fasta"))
			num_taxa = len(Seqlist)
		#	print num_taxa
			num_align_length = len(str(Seqlist[0].seq))
			if num_taxa >= Min_taxa and num_align_length >= Min_len:
				select.append(cln)
	print str(len(select)) + " files passed the filter"

	print "\n Generate matrix occupancy statistics"
	occupancy = {}
	#dictionary description: occupancy Key is taxon name, value is list [ num_of_sequence,  total length of sequence for this species]
	total_matrix_length = 0
	cmd = "phyutility -concat -aa -out " + outname + ".nex -in "
	for cln in select:
		cmd += clnDir+cln+" "
		Seqlist = list(Seq.parse( clnDir+cln , "fasta"))
		total_matrix_length += len(str(Seqlist[0].seq))

		for sequence in Seqlist:
			taxid = str(sequence.id)
			if taxid not in occupancy:
				occupancy[taxid] = [0,0]
			occupancy[taxid][0] +=1
			occupancy[taxid][1] += len( str(sequence.seq).replace("-",""))
	cmd += '\n'


	total_orthologous = len(select)
	out_occupancy_stats = open(outname + "_matrix_taxa_occupancy_statistics.txt" ,"w")
	out_occupancy_stats.write("taxon\t#of_orthologs\t#of_total_characters_withoutGAP\tPct_orthologs\tPct_characters\n")
	sum_chr=0
	for taxon in occupancy:
		num_ortho = occupancy[taxon][0]
		chrs = occupancy[taxon][1]
		sum_chr += chrs
		out = taxon + '\t' + str(num_ortho) + '\t' + str(chrs) + '\t' + str(num_ortho/float(total_orthologous)) + '\t' + str(chrs/float(total_matrix_length)) + '\n'
		out_occupancy_stats.write(out)

	total_taxa = len(occupancy)
	out = "\n Supermatrix include " + str(total_taxa) + " taxonomy unit, " + str(total_orthologous)+" loci  and " + str(total_matrix_length) +" aligned columns\n" + "Overall matrix occupancy "+ str(sum_chr/float(total_taxa*total_matrix_length)) + "\n"
	out_occupancy_stats.write(out)

	print "Supermatrix taxon occupancy status writting to "+ outname + "_matrix_taxa_occupancy_statistics.txt"
	print "Watting for matrix concatenate to finish. This process may take several minute, Wait!!"
	os.system(cmd)

	#Convert .nex file to .phy and .model foles for IQtree -spp option
	infile = open(outname+".nex" , "r")
	outfile = open(outname+".phy","w")
	outfile2 = open(outname+".model","w")
	for line in infile:
		line = line.strip()
		if len(line) <10:
			continue
		if line[0]=="#" or line[:5]=="BEGIN" or line[:6]=="MATRIX" or line=="END;" or line[:6]=="FORMAT":
			continue
		if line[0] == "[":
			line = line.replace("[","LG,")
			line = line.replace(" ]","")
			line = line.replace(" OG","\n"+"LG,OG")
			line = line.replace(" ","=")
			outfile2.write(line.strip() + '\n')
		elif line[:10]=="DIMENSIONS":
			ntax = (line.split("NTAX=")[1]).split(" ")[0]
			nchar = (line.split("NCHAR=")[1]).replace(";","")
			outfile.write(ntax+" "+nchar+"\n")
		else:
			spls=line.split("\t")
			outfile.write(spls[0]+" "+spls[1]+"\n")
	infile.close()
	outfile.close()
	outfile2.close()
	



if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Usage: python supermatrix_concatenate.py  input_Dir  min_align_length   min_Taxa   output_name"
		sys.exit()


	clnDir = sys.argv[1]
	if clnDir[-1] != '/': clnDir +="/"
	aln_len = sys.argv[2]
	minTaxa = sys.argv[3]
	outname = sys.argv[4]

	Concat(clnDir,aln_len,minTaxa,outname)


