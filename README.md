# Algae review - phylotranscritpomic analysis pipeline

Citation: Cheon, S., Zhang, J. and Park, C., 2020. Is phylotranscriptomics as reliable as phylogenomics?. Molecular biology and evolution, 37(12), pp.3672-3683.  
  
\##Notice: Consistent text formatting helps reders to interpret information. **\<text\>** means parameters for Linux shell and python scripts such as input file name or integer values.

- - -
<br>  

## Requirement

**Hardware**  
32-core processors (recommend > 8-core processors)  
256 Gb (Gigabytes) of RAM (recommend > 120 Gb of RAM)  
\> 1 Terabytes of space require for raw sequencing data and processed data  
Ubuntu 16.04 LTS (recommend LTS version)  
Internet accessible environments  
  
**Software**  
Python2.7 with [Biopython](https://biopython.org)  
JAVA 1.8 (or higher)  
cmake  
[SRA Toolkit](https://www.ncbi.nlm.nih.gov/home/download/) (v 2.10.8 or higher)  
[Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic) (v 0.36 or higher)  
[Samtools](http://www.htslib.org)  
[Trinity](https://github.com/trinityrnaseq/trinityrnaseq) (v 2.2.0 or higher)  
[Jellyfish](https://github.com/gmarcais/Jellyfish) (v 2.3.0 or higher)  
[Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) (v 2.3.5.1 or higher)  
[TransDecoder](https://github.com/TransDecoder/TransDecoder) (v 3.0.0 or higher)  
[CD-hit](http://weizhongli-lab.org/cd-hit/) (v 4.6.6 or higher)  
[BLAST+](https://www.ncbi.nlm.nih.gov/home/download/) (v 2.9.0 or higher)  
[OrthoFinder](https://github.com/davidemms/OrthoFinder) (v.2.4.0 or higher)  
[DIAMOND](https://github.com/bbuchfink/diamond/releases) (v. 0.9.24 or higher)  
[MCL](https://micans.org/mcl/)  
[Prank](http://wasabiapp.org/software/prank/) (v.150803)  
[Phyutility](https://github.com/blackrim/phyutility) (v.2.7.1)  
[IQ-Tree](http://www.iqtree.org) (v. 1.6.11 or higher)  
  
  
## Installation on Linux with conda
1. Install [anaconda](https://www.anaconda.com/products/individual)
``` bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh  

sh https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh  
  
rm https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
```
  
2. Create conda environmental and installation
``` bash
conda update conda

conda env create -n phylo --file 2021.May.Phylo_env.yaml

conda activate phylo
```
3. Phyutility linux package download
``` bash
sudo apt-get install phyutility
```
4. Trimmpmatic file download
```bash
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip

unzip Trimmomatic-0.39.zip
```
  



- - -
## Quick start.
  1.[Quick start guideline for example raw data download](https://github.com/CSB-SeongminCheon/Algae_review_test/blob/main/Quick%20start%20guideline%20for%20example%20raw%20data%20download.md)  
  2.[Quick start guideline from translated de novo assembled transcripts with example dataset](https://github.com/CSB-SeongminCheon/Algae_review_test/blob/main/Quick%20start%20guideline%20from%20translated%20de%20novo%20assembled%20transcripts%20with%20example%20dataset.md)  
  
 <br>  
   
## Tutorial
  
  
\##Notice: if you have a proteome sequence or translated de novo assembled reference transcrits. you can starts from part 2. 
  
### Part 1. RNA-seq raw data download from NCBI SRA database
For phylogeny with RNA-seq data. we are download RNA-seq raw data from NCBI SRA database.
``` 
fastq-dump --defline-seq '@$sn[_$rn]/$ri' --split-files <SRA Accession ID>
```

<br>  

### part 2. de novo transcritpome assembly and translation  
    
    
__1. *De novo* transcriptome assembly with Trinity__  
Short reads RNA sequencing data processed by Trinity assembler with Trimmomatic read trimming toool for illumina NGS data.  
  
For data sets with known adaptor sequence and phred scores for base quality.  
  
If you have single-end sequencing data  
``` bash
Trinity --seqType fq --trimmomatic --quality_trimming_params <"ILLUMINACLIP:/home/your/path/trinity-plugins/Trimmomatic-0.36/adapters/TruSeq3-PE.fa>:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"> --max_memory <200G> --CPU <32> --full_cleanup --single <single-end reads.fastq> --output <trinity_output_Name>
```
<br>  

or paired-end sequencing data  
``` bash
Trinity --seqType fq --trimmomatic --quality_trimming_params <"ILLUMINACLIP:/home/your/path/trinity-plugins/Trimmomatic-0.36/adapters/TruSeq3-PE.fa>:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"> --max_memory 200G --CPU 32 --full_cleanup --left <forward reads.fastq> --right <reverse reads.fastq> --output <trinity_output_Name>
```  

<br>  
  
**2. Find Open Reading Frames and translate using TransDecoder with blastp for orfs selection**  
  
Assembled transcripts were translated with TransDecoder programs and choosing orfs with blastp results.  
For blastp, download and make database file from [Uniprot/Swiss-Prot](https://www.uniprot.org/downloads)


``` bash
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gzip -d uniprot_sprot.fasta.gz
makeblastdb -i uniprot_sprot.fasta -dbtype prot
  
TransDecoder.LongOrfs -t <transcripts> -S
blastp -query <transcripts>.transdecoder_dir/longest_orfs.pep -db uniprot_sprot.fasta -max_target_seqs 1 -outfmt 6 -evalue 10 -num_threads 32 -out Genus_Species.outfmt6
TransDecoder.Predict -t <transcripts> --retain_blastp_hits Genus_Species.outfmt6 --cpu 32
```
<br>  
  
**3. Clustering with CD-hit**  
  
Reduce translated sequence redundancy with CD-hit  
``` bash
cdhit -i <transcripts>.transdecoder.pep -o <Genus Species>.fa.cdhit -c 0.99 -n 5 -T 32
```  
<br>  

**4. Sequence ID fixation.**  
  
CD-hit output file " Genus_Species.fa.cdhit" sequence ID change to shorten name to Genus_Species@seqID. The special character "@" is used to separate taxon name and sequence ID. Any "-" (hyphen) in the sequence name will be replaces py phyutility and cause problems in downstream process.
``` bash
python2 fix_names_from_CDhit.py <CDhit output file.cdhit> <Genus name> <Species name>
```  

<br> 

### part 3. Orthology inference and single copy orthologous extraction  
  
**1. Running OrthoFinder**  

Orthology inference, Copy all the Genus_Species.fix.fa files (or any proteom sequences) into a new directory such as <OrthoFinder_running_dir>.
```bash
orthofinder -f <OrthoFinder_running_dir>
```
<br>  

**2. Single copy orthologous prediction**  
  
Choose the minimal number of taxa filters for single copy orthologs inference (recommend half of taxa)
```bash
python2 singlecopy_from_OrthoFinder.py <OrthoFinder_running_dir> SingleCopy <Min number of taxa>
```  
<br>  

**3. Multiple sequence alignment with Prank**   
```bash
python2 prank_Wrapper.py SingleCopy
```

<br>  

**4. Alignment trimming with Phyutility**  
  
I usually use 0.3 for minimal aling column.
```bash
python2 phyutility_Wrapper.py <single copy results> <min_align_column>
```

<br>  
   
**5. Concatenate supermatrix**  

You can choose minimal cleaned alignment length per orthologs and minimal number of taxa filters (recommand 150, half of taxa for amino acid tree).  
Concatenate with selected cleand orthologous for supermatrix.  

```bash
python2 supermatrix_concatenate.py <single copy results> <min_align_length> <min_taxa> <output_name>
```

<br>

### part 4. Phylotranscritpomic tree reconstruction  
  
Run IQ-Tree with 1000 UFBoot replications and search for best fit tree. Use LG+C60+R+F model.
```bash
iqtree -s <Concatenate_matrix>.phy -spp <Concatenate_matrix>.model -m LG+C60+R+F -bb 1000 -nt 32
```







