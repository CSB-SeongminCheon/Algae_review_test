# Algae review - phylotranscritpomic analysis pipeline

Citation: Cheon, S., Zhang, J. and Park, C., 2020. Is phylotranscriptomics as reliable as phylogenomics?. Molecular biology and evolution, 37(12), pp.3672-3683.  
  
\##Notice: Consistent text formatting helps reders to interpret information. \<text\> means parameters for Linux shell and python scripts such as input file name or integer values.

- - -
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
  
- - -
## Quick start.
  1.[Quick start guideline from Raw data with examples](https://github.com/CSB-SeongminCheon/Algae_review_test/blob/main/Quick_Start_Guideline_from_RawData.md)  
  2.[Quick start guideline from translated de novo assembled transcripts]()  
  
   
## Tutorial
  
  
\##Notice: if you have a proteome sequence or translated de novo assembled reference transcrits. you can starts from part 2. 
  
### Part 1. RNA-seq raw data download from NCBI SRA database
for phylogeny with RNA-seq data. we are download RNA-seq raw data from NCBI SRA database.
``` bash
fastq-dump --defline-seq '@$sn[_$rn]/$ri' --split-files <SRA Accession ID>
```
  
  
  
### part 2. de novo transcritpome assembly and translation

1. *De novo* transcriptome assembly with Trinity
Short reads RNA sequencing data processed by Trinity assembler with Trimmomatic read trimming toool for illumina NGS data.  
For data sets with known adaptor sequence and phred scores for base quality.  

if you have single-end sequencing data  
``` bash
Trinity --seqType fq --trimmomatic --quality_trimming_params "ILLUMINACLIP:/home/your/path/trinity-plugins/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36" --max_memory 200G --CPU 32 --full_cleanup --output taxonID.trinity --single <single-end reads.fastq> --output <trinity_output_Name>
```
or paired-end sequencing data  
``` bash
Trinity --seqType fq --trimmomatic --quality_trimming_params "ILLUMINACLIP:/home/your/path/trinity-plugins/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36" --max_memory 200G --CPU 32 --full_cleanup --output taxonID.trinity --left <forward reads.fastq> --right <reverse reads.fastq> --output <trinity_output_Name>
```
  
  
  
2. Find Open Reading Frames and translate using TransDecoder with blastp for orfs selection  
  
Assembled transcripts were translated with TransDecoder programs. and choosing orfs with blastp results.  
for blastp, download and make database file from [Uniprot/Swiss-Prot](https://www.uniprot.org/downloads)


``` bash
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gzip -d uniprot_sprot.fasta.gz
makeblastdb -i uniprot_sprot.fasta -dbtype prot
  
TransDecoder.LongOrfs -t <transcripts> -S
blastp -query <transcripts>.transdecoder_dir/longest_orfs.pep -db uniprot_sprot.fasta -max_target_seqs 1 -outfmt 6 -evalue 10 -num_threads 32 -out Genus_Species.outfmt6
TransDecoder.Predict -t <transcripts> --retain_blastp_hits Genus_Species.outfmt6 --cpu 32
```




