## baltic: the Backronymed Adaptable Lightweight Tree Import Code

baltic was initially developed to extract various statistics from molecular phylogenies derived from [BEAST](https://github.com/beast-dev/beast-mcmc) in a customised way. My [influenza B virus reassortment paper](https://dx.doi.org/10.1093/molbev/msu287) used early versions of baltic’s code to look at how the human influenza B virus segment diversity is structured according to genomic background. I’ve since split up the various bits of code into three parts:

--------------------

## baltic
[`baltic.py`](baltic.py) is the tree parser itself. It uses three main classes - node, leaf and tree to import, manipulate and plot BEAST trees with their rich variety of comments. Node and leaf classes have references to the usual set of parameters you would find in a phylogeny - index of character in string designating the branch (a unique identifier within the tree), length, height, position in time (absoluteTime), X and Y coordinates, a dictionary encoding BEAST branch comments (traits) and a reference to their parent (None for root) and a string designating their type (branchType). The node class additionally have a children attribute, which is a list of the node’s children, another list called leaves that contains tip names that descend from that node, a numChildren attribute, which is the length of the leaves list and a childHeight attribute which tracks when the last tip descending from the node existed. The leaf class has two extra attributes called name and numName. Trees drawn from the posterior distribution will usually encode tips as numbers to save space and require a translation map to convert back into actual interpretable tip names. In baltic numName will be the exact name for the tip that was used in the tree string, with functions to allow the translation of numName into name.

baltic.py evolved from a [short linked list script on StackOverflow](http://stackoverflow.com/questions/280243/python-linked-list/280286#280286) and underwent a major overhaul in order to correct [an article](https://dx.doi.org/10.1126/science.aaa5646) that was wrong. The code should be fairly legible (and commented) and highly adaptable to suit anyone’s needs.

--------------------
### Usage basics

By convention baltic is imported as bt:

`import baltic as bt`

When called with a tree string the `make_tree()` function return a baltic tree object:
```python
treeString='((A:1.0,B:2.0):1.0,C:3.0);'

myTree = bt.make_tree(treeString)
```
Note that if you're not using newick, nexus or nextstrain JSON trees (`loadNewick`, `loadNexus`, and `loadJSON` functions respectively) you'll have to write some code to parse out the tree string. baltic will warn the user if it can't parse something. If this happens you should check if your tip names or annotations contain characters that should **never** be found outside of functional tree string bits, such as commas, parentheses or semicolons. Alternatively, it may be that the regexes that are used to parse out tip names or annotations don't cover some special character you use to define your taxa and will require some editing of baltic.py to alleviate the problem. Feel free to raise an issue if this happens.

`make_tree()` is a function that parses the tree string and builds the data structure that is the phylogenetic tree. It works exactly like all other tree parsers:

- Every time an opening parenthesis (`(`) is encountered in the tree string a new instance of `node` class is created. The new class' `.index` attribute is set to the index along the tree string where it was encountered, giving that particular class a unique identifier within the tree string. The `.parent` attribute is set to whatever the previous object encountered was, similarly, since the last encountered object could only be another node, the current node is added to its parents list of children. Finally we set our new node as the 'current' node of the tree and append the node to the list of objects (`.Objects`, which are branches) contained in the tree.

- Every time a string is encountered which may or may not be surrounded by quotation marks (`'` or `"`) or have the beginning of an annotation block (`[`) we create a new `leaf` class. It also receives an `.index` identifier, like the `node` class. Unlike the `node` class, however, the `.numName` attribute is also set as the string that defined the tip. In BEAST trees it will be the number that identifies the tip, but it could also be a regular string.

- Next baltic looks for annotations, which are the blocks in the format `[&parameter1=1.0,parameter2=0.0]`. These are transformed into the `.traits` dictionary for the branch. In this example the branch being parsed would receive a dictionary with two keys: `cur_branch.traits = {'parameter1' : 1.0, 'parameter2' : 0.0}`.

- Annotations should be followed by branch lengths preceded by a colon (`:`). The branch length is assigned to the current branch's `.length` attribute.

- Forks in the tree string are defined as commas (`,`) and ends of clades are defined by closing parentheses (`)`) and both mean that whatever comes next is in relation to the parent branch of whatever branch we were dealing with earlier.

- Finally tree strings are finished with a semi colon (`;`).


Before you can run any analysis you will usually have to traverse the tree such that branch lengths which are available in the tree string are transformed into branch heights:

`myTree.traverse_tree()`

This takes the `.length` attributes of each branch and sums or subtracts them, as appropriate during a tree traversal and the `.height` attribute of each branch (`node` or `leaf` object) is set, where the root of the tree has `.height = 0.0` and the most recent tip is the highest object in the tree. The tree traversal will also set the tree's `.treeHeight` attribute.

If your tree happens to have branch lengths in units of time you can use the `.height` attribute to modify the `.absoluteTime` attribute of each branch, such that the entire tree is calibrated and position correctly in time. This involves finding the most recent tip in the tree (in absolute time), subtracting the `.treeHeight` and adding the `.height` of the each branch.


Most analytic operations will involve looking at each branch individually without referring back to the tree structure much, beyond immediate children or parents of a particular branch. This is done by iterating over the tree's `.Objects` list, which contains all the branches in the tree. If you want to print out the height of each internal branch whose parent had a different trait value you would do it as:

```python
for k in myTree.Objects:
   if isinstance(k,bt.node) ## (or, alternatively if k.branchType=='node')
       if k.traits[myTrait] != k.parent.traits[myTrait]:
           print k.height
```

--------------------

## samogitia

<img src="figures/coa_samogitia.jpg" width=200px>

[`samogitia.py`](samogitia.py) is the heavy-lifting, tree file-wrangling script in the collection. It’s main role is to parse BEAST tree files, use baltic to create tree data structures, which samogitia then manipulates to create BEAST-like log files that can usually be imported into [Tracer](http://tree.bio.ed.ac.uk/software/tracer/) or used in another program.

--------------------

## austechia

<img src="figures/coa_austechia.png" width=200px>

[`austechia.ipynb`](austechia.ipynb) is the fancy Jupyter notebook that takes tree files, usually MCC trees from BEAST, and plots them. It is meant to be part teaching tool to get people to think about how trees are plotted, to allow for highly customisable representations of trees (e.g. Fig 6 in my [MERS-CoV paper](http://dx.doi.org/10.1093/ve/vev023)) and to improve the aesthetics situation in phylogenetics.

--------------------

## galindia

<img src="figures/coa_galindia.jpg" width=200px>

[`galindia.ipynb`](galindia.ipynb) is a notebook that uses baltic to plot JSONs from [nextstrain.org](nextstrain.org) in order to allow customisable, static, publication-ready figures for phylogenies coming from nextstrain's augur pipeline.

--------------------

## curonia

<img src="figures/coa_curonia.jpg" width=200px>

[`curonia.ipynb`](curonia.ipynb) generalises the [notebook](https://github.com/ebov/space-time/blob/master/Scripts/notebooks/EBOV_phylogeography_animation.ipynb) used to animate the [spread of Ebola virus in West Africa](https://www.youtube.com/watch?v=j4Ut4krp8GQ). This notebook should require minimal manual editing to produce similarly styled animation of other study systems.

--------------------
## baltic was used in the following publications:

- van Vuren JP, Ladner JT, Grobbelaar AA, Wiley MR, Lovett S, Allam M, Ismail A, le Roux C, Weyer J, Moolla N, Storm N, Kgaladi J, Sanchez-Lockhart M, Conteh O, Palacios G, Paweska JT, 2019. _Phylodynamic Analysis of Ebola Virus Disease Transmission in Sierra Leone_. __Viruses__, 11(1), 71; [doi](https://doi.org/10.3390/v11010071).
- Bell SM, Katzelnick L, Bedford T, 2018. _Dengue antigenic relationships predict evolutionary dynamics_, __bioRxiv__ 432054; [doi](https://doi.org/10.1101/432054).
- Lee JM, Huddleston J, Doud MB, Hooper KA, Wu NC, Bedford T, Bloom JD, 2018. _Deep mutational scanning of hemagglutinin helps predict evolutionary fates of human H3N2 influenza variants_, __PNAS__ 115(35): 8276-8285.
- Dokubo EK, Wendland A, Mate SE, Ladner JT, ..., Palacios G, Fallah MP, 2018. _Persistence of Ebola virus after the end of widespread transmission in Liberia: an outbreak report_, __Lancet Infect Dis__ 18: 1015–1024.
- Venkatesh D, Poen MJ, Bestebroer TM, ..., Brown IH, Fouchier RAM, Lewis NS, 2018. _Avian influenza viruses in wild birds: virus evolution in a multi-host ecosystem_, __J Virol__ 92:e00433-18.
- Chu DKW, Hui Kenrie PY, Perera RAPM, Miguel E, Niemeyer D, Zhao J, Channappanavar R, Dudas G, Oladipo JO, Traoré A, Fassi-Fihri O, Ali A, Demissie GF, Muth D, Chan MCW, Nicholls JM, Meyerholz DK, Kuranga SA, Mamo G, Zhou Z, So RTY, Hemida MG, Webby RJ, Roger F, Rambaut A, Poon LLM, Perlman S, Drosten C, Chevalier V, Peiris M, 2018. _MERS coronaviruses from camels in Africa exhibit region-dependent genetic diversity_. __PNAS__ 115(12): 3144-3149.
- Whitmer SLM, Ladner JT, Wiley MR, Patel K, Dudas G, Rambaut A, Sahr F, Prieto K, Shepard SS, Carmody E, Knust B, Naidoo D, Deen G, Formenty P, Nichol ST, Palacios G, Ströher U, 2018. _Active Ebola Virus Replication and Heterogeneous Evolutionary Rates in EVD Survivors_. __Cell Reports__ 22(5): 1159-1168.
- Dudas G, Carvalho L, Rambaut A, Bedford T. _MERS-CoV spillover at the camel-human interface_, 2017. __eLife__ 7: e31257.
- Langat P, Raghwani J, Dudas G, ..., Russell C, Pybus OG, McCauley J, Kellam P, Watson SJ. _Genome-wide evolutionary dynamics of influenza B viruses on a global scale_, 2017. __PLOS Pathogens__ 13(12): e1006749.
- Grubaugh ND, Ladner JT, Kraemer MUG, Dudas G, Tan AL, Gangavarapu K, Wiley MR, White S, Thézé J, ..., Bedford T, Pybus OG, Isern S, Palacios G, Andersen KG. _Multiple introductions of Zika virus into the United States revealed through genomic epidemiology_, 2017. __Nature__ 546: 401–405.
- Dudas G, Carvalho LM, Bedford T, Tatem AJ, ..., Suchard M, Lemey P, Rambaut A. _Virus genomes reveal the factors that spread and sustained the West African Ebola epidemic_, 2017. __Nature__ 544(7650): 309-315.
- Bell SM, Bedford T. _Modern-Day SIV viral diversity generated by extensive recombination and cross-species transmission_, 2017. __PLoS Pathog__ 13(7): e1006466.
- Holmes EC, Dudas G, Rambaut A, Andersen KG. _The Evolution of Ebola virus: Insights from the 2013-2016 Epidemic_, 2016. __Nature__ 538(7624): 193-200.
- Whitmer SLM, Albariño C, Shepard SS, Dudas G, ..., Nichol ST, Ströher U. _Preliminary Evaluation of the Effect of Investigational Ebola Virus Disease Treatments on Viral Genome Sequences_, 2016. __Journal of Infectious Diseases__:jiw177.
- Rambaut A, Dudas G, Carvalho LM, Park DJ, Yozwiak NL, Holmes EC, Andersen KG. _Comment on “Mutation rate and genotype variation of Ebola virus from Mali case sequences”_, 2016. __Science__ 353(6300):658-658.
- Lewis NS, Russell CA, Langat P, ..., Dudas G, ..., Watson SJ, Brown IH, Vincent AL. _The global antigenic diversity of swine influenza A viruses_, 2016. __eLife__ 5: e12217.
- Quick J, Loman NJ, Duraffour S, Simpson JT, Severi E, Cowley L ..., Dudas G, ..., Günther S, Carroll MW. _Real-time, portable genome sequencing for Ebola surveillance_, 2016. __Nature__ 530(7589): 228-232.
- Dudas G, Rambaut A, _MERS-CoV recombination: implications about the reservoir and potential for adaptation_, 2016. __Virus Evolution__ 2(1):vev023.
- Ladner JT, Wiley MR, Mate S, Dudas G, ... Palacios G. _Evolution and Spread of Ebola Virus in Liberia, 2014-2015_, 2015. __Cell Host & Microbe__ 18(6): 659-669.
- Park DJ, Dudas G, Wohl S, Goba A, Whitmer SLM, ..., Sabeti PC. _Ebola Virus Epidemiology, Transmission, and Evolution during Seven Months in Sierra Leone_, 2015. __Cell__ 161(7): 1516-1526.
- Carroll MW, Matthews DA, Hiscox JA, ... Dudas G, ... Günther S. _Temporal and spatial analysis of the 2014-2015 Ebola virus outbreak in West Africa_, 2015. __Nature__ 524(7563): 97-101.
- Dudas G, Bedford T, Lycett S, Rambaut A. _Reassortment between Influenza B Lineages and the Emergence of a Coadapted PB1–PB2–HA Gene Complex_, 2015. __Molecular Biology and Evolution__ 32(1): 162-172.
- Gire SK, Goba A, Andersen KG, ... Dudas G, ... Sabeti PC. _Genomic surveillance elucidates Ebola virus origin and transmission during the 2014 outbreak_, 2014. __Science__ 345(6202): 1369-1372.

--------------------

Copyright 2016 [Gytis Dudas](https://twitter.com/evogytis). Licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
