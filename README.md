# Quantifying within-host evolution of H5N1 influenza in humans and poultry in Cambodia  

#### Louise H. Moncla<sup>1</sup>, Trevor Bedford<sup>1,2</sup>, Philippe Dussart<sup>3</sup>,  Srey Viseth Horm<sup>3</sup>, Sareth Rith<sup>3</sup>, Philippe Buchy<sup>4</sup>, Erik A Karlsson<sup>3</sup>,  Lifeng Li<sup>5,6</sup>, Yongmei Liu<sup>5,6</sup>, Huachen Zhu<sup>5,6</sup>, Yi Guan<sup>5,6</sup>, Thomas C. Friedrich<sup>7,8</sup>, Paul F. Horwood<sup>9,10</sup>

<sup>1</sup>Fred Hutchinson Cancer Research Center, Seattle, Washington, United States, <sup>2</sup>University of Washington, Seattle, Washington, United States, <sup>3</sup>Virology Unit, Institut Pasteur du Cambodge, Phnom Penh, Cambodia, <sup>4</sup>GlaxoSmithKline, Vaccines R&D, Singapore, Singapore,<sup>5</sup>Joint Influenza Research Centre (SUMC/HKU), Shantou University Medical College, Shantou, People's Republic of China,<sup>6</sup>State Key Laboratory of Emerging Infectious Diseases/Centre of Influenza Research, School of Public Health, The University of Hong Kong, Hong Kong, SAR, People's Republic of China,<sup>7</sup>Department of Pathobiological Sciences, University of Wisconsin School of Veterinary Medicine, Madison, WI, United States,<sup>8</sup>Wisconsin National Primate Research Center, Madison, WI, United States,<sup>9</sup>Papua New Guinea Institute of Medical Research, Goroka, Paula New Guinea,<sup>10</sup>Australian Institute of Tropical Health and Medicine, James Cook University, Cairns, Australia.

## Abstract

Avian influenza viruses (AIVs) periodically cross species barriers and infect humans. The likelihood that an AIV will evolve mammalian transmissibility depends on acquiring and selecting mutations during spillover, but data from natural infection is limited. We analyze deep sequencing data from infected humans and domestic ducks in Cambodia to examine how H5N1 viruses evolve during spillover. Overall, viral populations in both species are predominated by low-frequency (<10%) variation shaped by purifying selection and genetic drift, and half of the variants detected within-host are never detected on the H5N1 virus phylogeny. However, we do detect a subset of mutations linked to human receptor binding and replication (PB2 E627K, HA A150V, and HA Q238L) that arose in multiple, independent humans. PB2 E627K and HA A150V were also enriched along phylogenetic branches leading to human infections, suggesting that they are likely human-adaptive. Our data show that H5N1 viruses generate putative human-adapting mutations during natural spillover infection, many of which are detected at >5% frequency within-host. However, short infection times, genetic drift, and purifying selection likely restrict their ability to evolve extensively during a single infection. Applying evolutionary methods to sequence data, we reveal a detailed view of H5N1 virus adaptive potential, and develop a foundation for studying host-adaptation in other zoonotic viruses.

## Install

The notebooks in this repo require `baltic/baltic.py`, which is available from [this GitHub repo](https://github.com/evogytis/baltic). There is a working version in this repo. Every notebook also requires R and ryp2, a package for using R within python jupyter notebooks. To ensure you have all the required packages, do the following: 

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) for your machine. 
2. Install [R](https://www.r-project.org/) if you do not have it. 
2. Clone this repo: `git clone https://github.com/blab/h5n1-cambodia`
3. Create the conda environment: `conda env create -f h5n1-cambodia-environment.yml`
4. Activate the environment: `conda activate h5n1-cambodia-environment` 
5. Navigate to the `h5n1-cambodia` directory, launch jupyter notebook and run. 

## Project structure

* [`auspice/`](auspice/): contains JSON trees viewable via Nextstrain
* [`data/`](data/): contains sample metadata, consensus genomes, within-host SNV calls, coverage data in pileup format, coding region annotations in gtf format, and phylogenies
* [`figures/`](figures/): contains Jupyter notebooks to generate manuscript figures as well as PDFs of individual figure outputs. 
* [`scripts`](scripts/): contains processing scripts

## Citation

[Moncla LH, Bedford T, Dussart P, Horm SV, Rith S, Buchy P, Karlsson EA, Li L, Liu Y, Zhu H, Guan Y, Friedrich TC, Horwood PF. 2019. Quantifying within-host evolution of H5N1 influenza in humans and poultry in Cambodia. bioRxiv: 683151.](https://doi.org/10.1101/683151)
