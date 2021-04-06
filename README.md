# Algae review - phylotranscritpomic analysis pipeline

Citation: Cheon, S., Zhang, J. and Park, C., 2020. Is phylotranscriptomics as reliable as phylogenomics?. Molecular biology and evolution, 37(12), pp.3672-3683.  
  
\##Notice: Consistent text formatting helps reders to interpret information. \<text\> means parameters for Linux shell and python scripts such as input file name or integer values.
  
- - -

```bash
for i in range(0, 1):
  print("test")
```
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
## Tutorial

\##Notice: if you have a proteome sequence or translated de novo assembled reference transcrits. you can starts from part 2. 

### Part 1. RNA-seq raw data download from NCBI SRA database
for phylogeny with RNA-seq data. we are download RNA-seq raw data from NCBI SRA database.
``` bash
fastq-dump --defline-seq '@$sn[_$rn]/$ri' --split-files <SRAaccessionID>
```

