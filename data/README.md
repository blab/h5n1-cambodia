# Data

## Within-host data  
All within-host variants reported in the manuscript and analyzed are available in "within-host-variants-1%.txt". This data file includes all variants present at a frequency of at least 1% in all human and duck samples. Fastq files were processed and variants called using [this pipeline](https://github.com/lmoncla/illumina_pipeline), briefly outlined below: 

1. Adapter and quality trimming with [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic )
2. Mapping with [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
3. Manual inspection of mapping and consensus genome calling with [Geneious](https://www.geneious.com/) 
4. Re-mapping fastq files called consensus with [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)


### Trimming
Trimming was performed with [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic ) to remove Illumina adapter sequencing and ends of reads with low quality scores. Reads were trimmed in 5 bp windows to a quality score of Q30, and trimmed reads with length < 100 bp were discarded, using the following command: `java -jar Trimmomatic-0.36/trimmomatic-0.36.jar SE input.fastq output.fastq ILLUMINACLIP:Nextera_XT_adapter.fa:1:30:10 SLIDINGWINDOW:5:30 MINLEN:100`

### Mapping 
We performed a local mapping of our trimmed reads to reference sequences previously released by [Rith et al.](https://jvi.asm.org/content/88/23/13897.long) using [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml), with the following command:` bowtie2 -x reference_sequence.fasta -U read1.trimmed.fastq,read2.trimmed.fastq -S output.sam --local`

The mapping (bam) file was manually inspected in [Geneious](https://www.geneious.com/). 

### Consensus sequence calling
Consensus sequences were called in Geneious, with nucleotide sites with <100x coverage called as Ns. Consensus genomes were exported in fasta format and are available [here](https://github.com/blab/h5n1-cambodia/tree/master/data/h5n1-consensus-genomes.fasta).

### Remapping
To avoid issues with mapping to improper reference sequences, we then remapped each sample's fastq files to its own consensus sequence. These bam files were again manually inspected in Geneious, and a final consensus sequence was called. Those consensus genomes for which we acquired at least 80% full-genome coverage are available [here](https://github.com/blab/mumps-seq/tree/master/data/consensus-genomes) as fasta files. 

### Variant calling
Variants were called using [Varscan](http://varscan.sourceforge.net/), requiring  minimum coverage of 100x at the polymorphic site, a minimum quality of Q30, and a minimum SNP frequency of 1% with the following command: `java -jar VarScan.v2.3.9.jar mpileup2snp input.pileup --min-coverage 100 --min-avg-qual 30 --min-var-freq 0.01 --strand-filter 1 --output-vcf 1 > output.vcf`

### Amino acid annotation
Coding region changes were annotated using [this jupyter notebook](https://github.com/blab/h5n1-cambodia/tree/master/scripts).

## Consensus genomes 
All consensus sequences are available [here](https://github.com/blab/mumps-seq/tree/master/data/consensus-genomes). The fasta header contains the following information: strain name | sample collection date | country of sampling | host species. 


## Trees 
Tree files shown in Figure 1 are available in json format [here](https://github.com/blab/h5n1-cambodia/tree/master/data/tree-jsons). These jsons were generated using the (Nextstrain avian-flu)[https://github.com/nextstrain/avian-flu] pipeline with no geographic or regional subsampling. 
