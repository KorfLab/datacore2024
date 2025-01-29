Splicing
========

Build procedure for smallgenes
------------------------------

+ The region must be less than 1200 bp (99 flank on each side)
+ There must be a single protein-coding gene (no weird ovelaps)
+ The transcript must have an intron with at least 10,000 observations
+ The transcript may not have any non-canonical gene features
	+ GT..AG introns only
	+ Exons >= 25 bp
	+ Introns >= 35 bp
+ The gene must have less than 10 million putative isoforms
+ The locus must not be too similar to other loci (95% pct of 95% length)

Stuff you need

+ grimoire in your PYTHONPATH
+ grimoire's `haman` in your PATH
+ isoform in your PYTHONPATH
+ blast in your PATH

Requires doing a C.elegans gene build with `--issuesok`. In the lines below,
`$DATA` is wherever you keep your data.

	mkdir build
	cd build
	ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
	ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz
	gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
	cd ..
	haman build/genome.gz build/ws282.gff3 pcg genes --issuesok --plus
	python3 gene_selector.py build/genes

This results in 2 new file: `initial.genes.txt` and `initial.log.json`

To remove paralogs that are too close and build the final set:

	perl gene_reducer.pl


