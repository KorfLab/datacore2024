Splicing
========

APC Build
---------

+ Isolated protein-coding genes that do no overlap other genes
+ Genes must have an intron
+ Have a single annotated isoform (no argument about which one is canonical)
+ Genes must have at least 100,000 RNAseq introns matching the annotation
+ No non-canonical gene features
	+ GT..AG introns only
	+ Exons >= 25 bp
	+ Introns >= 35 bp
+ The primary transcript must be less than 1000 bp
+ The transcript must have at most 3 introns
+ The gene must have less than 1 million putative isoforms


Stuff you need

+ grimoire in your PYTHONPATH
+ grimoire's `haman` in your PATH
+ genomikon's `isocounter` in your PATH

Requires doing a C.elegans gene build with `--issuesok`. In the lines below,
`$DATA` is wherever you keep your data.

	mkdir build
	cd build
	ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
	ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz 
	gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
	cd ..
	haman build/genome.gz build/ws282.gff3 pcg genes --issuesok
	./apc_build genes

2 new files: `apc.genes.txt` and `apc.log.json`

	mkdir apc
	mv genes build
	perl gather.pl apc.genes.txt
	tar -zcf apc.tar.gz apc
	mv apc build

The apc set for ws282 is 589 genes.