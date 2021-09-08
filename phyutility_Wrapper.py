#Phyutility installation such as $sudo apt-get install phyutility
import sys,os
from Bio import SeqIO as Seq

def Phyutility(DIR, align_file, min_aln):
	" Phyutility -clean with minimum column occupancy sequences and remove sequence shorter than 10 aa in this scripts"
	if DIR[-1] != "/":
		DIR +="/"
	cleaned_file = align_file + "-cln"
	if os.path.exists(DIR + cleaned_file):
		return cleaned_file
	cmd = "phyutility -aa -clean " + str(min_aln) + " -in " +DIR + align_file +" -out " +DIR+align_file+".phy"
	print(cmd)
	os.system(cmd)
	assert os.path.exists(DIR+align_file+".phy"),"Running Error Phyutility,Plz confirm PATH of phyutility "
	#Remove empty and short alignment sequences < 10 aa aln
	outfile = open(DIR+cleaned_file,"w")
	for phy_seq in Seq.parse( DIR + align_file+".phy" , "fasta"):
		if len( str(phy_seq.seq).replace("-","")) >= 10:  #Min_chr without gap
			outfile.write(">"+str(phy_seq.name) + '\n' + str(phy_seq.seq)+'\n')
	outfile.close()
	os.remove(DIR+align_file+".phy")
	return cleaned_file

def main(DIR,min_aln):
	if DIR[-1] != "/":
		DIR +="/"
	count = 0
	for i in os.listdir(DIR):
		if i.endswith(".aln"):
			count +=1
			Phyutility(DIR,i, min_aln)
	assert count > 0, "We can`t fount .aln files from prank alignment" 

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("python phyutility_Wrapper.py inDIR min_align_column")
		sys.exit(0)
	DIR=sys.argv[1]
	min_aln = sys.argv[2]
	main(DIR,min_aln)

