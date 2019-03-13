#!/usr/bin/env python2

# this will parse vcf files output from varscan and annotated with snpeff
# there is an extremely weird bug, where the vcfs need to be saved as "electronic business 
# card" under "kind". This can be done by setting them to open by default in Atom.

import sys, subprocess, glob, os, shutil, re, importlib, vcf, Bio
from subprocess import call
from Bio import SeqIO

genes_list = ["PB2","PB1","PA","HA","H5","NA","N1","NP","M1","MP","NS","NS1","NEP"]
file_list = []

outfilename = "normalized_outfile.txt"

# make an empty dictionary which will contain the sequence name with the number of dashes it has at the beginning of the sequece
#seq_normalizer = {}
#infilename = "/Users/lmoncla/src/H5N1/IRD_consensus_sequences/IRD_all_H5_HA/combined_IRD_and_HKU_170906.aligned.fasta"

#for seq in SeqIO.parse(infilename, "fasta"):
	#dash_count = 0
	#for base in seq.seq:
		#if base == "-":
			#dash_count += 1
		#else:
			#break

	#seq_normalizer[seq.name] = dash_count
	#print seq.name



with open(outfilename, "w") as outfile:
	outfile.write("sample\tgene\treference_position\treference_allele\tvariant_allele\tcoding_region_change\tfrequency(%)\tfrequency\tseverity_of_change\tamino_acid_change\n")

for file in glob.glob("*.vcf"):						# glob will find instances of all files ending in .fastq as shell would
	file_list.append(file)

for file in file_list:
	frequencies = []

	# perform a grep search for the SNP frequency and if there is a match, set frequency = the percentage; capture the portion of SearchStr that is in ()
	SearchStr = '.+\:([0-9]{1,2}\.{0,1}[0-9]{0,2}\%)'
	with open(file, "r") as infile:
		for line in infile:
			if "#" not in line:

				result = re.search(SearchStr,line)
				if result:
					frequency = '\t'.join(result.groups())

				else:
					frequency = "none reported"

				frequencies.append(frequency)

	vcf_reader = vcf.Reader(filename = file)
	#vcf_reader = vcf.Reader(open(file, 'r'))

	count = 0
	for record in vcf_reader:

		# set frequency = the entry in the frequency list indexed as the same as the current record
		frequency_percent = frequencies[count]
		#print frequency_percent
		count += 1
		frequency = frequency_percent.replace("%","")
		frequency = (float(frequency))/100

		chromosome = repr(record.CHROM)   # converts record.CHROM to a string
		chromosome = chromosome.replace("'", '')
		#print chromosome

		for gene in genes_list:
			query = "_" + gene

			if query in chromosome:
				chrom = chromosome.replace(query,'')
				break
			else:
				chrom = chromosome

		position = record.POS
		reference = record.REF

		# convert position to normalized position
		#normalized_position = position + seq_normalizer[chromosome]

		# convert record.INFO to a string
		info_string = ''.join(record.INFO['ANN'])
		info_string = info_string.split('|')


		variant_allele = info_string[0]
		variant_type = info_string[1]
		variant_impact_severity = info_string[2]
		gene = info_string[4]
		gene = gene.replace("_circ","")
		amino_acid_change = info_string[10].replace("p.", "")
		

		#print record.FORMAT

		with open(outfilename, "a") as outfile:
			outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chrom, gene, position, reference, variant_allele, variant_type, frequency_percent, frequency, variant_impact_severity, amino_acid_change))
		
		if len(info_string) == 31:
			variant_type2 = info_string[16]
			variant_impact_severity2 = info_string[17]
			gene2 = info_string[19]
			gene2 = gene2.replace("_circ","")
			amino_acid_change2 = info_string[25].replace("p.", "")
			print gene2, amino_acid_change2
			
		if len(info_string) == 46:
			variant_type3 = info_string[31]
			variant_impact_severity3 = info_string[32]
			gene3 = info_string[34]
			gene3 = gene3.replace("_circ","")
			amino_acid_change3 = info_string[40].replace("p.", "")
			print gene3, amino_acid_change3


	# record.INFO saves all of the info headers as a dictionary with info name: key
