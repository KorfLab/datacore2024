Splicing
========

APC Build
---------

+ The region must be less than 1200 bp (99 flank on each side)
+ There must be a single protein-coding gene (no weird ovelaps)
+ The transcript must have an intron with at least 10,000 observations
+ The transcript may not have any non-canonical gene features
	+ GT..AG introns only
	+ Exons >= 25 bp
	+ Introns >= 35 bp
+ The gene must have less than 1 million putative isoforms

Might want to post-process to remove genes that are too similar to each other?


Stuff you need

+ grimoire in your PYTHONPATH
+ grimoire's `haman` in your PATH
+ isoform in your PYTHONPATH

Requires doing a C.elegans gene build with `--issuesok`. In the lines below,
`$DATA` is wherever you keep your data.

	mkdir build
	cd build
	ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
	ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz
	gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
	cd ..
	haman build/genome.gz build/ws282.gff3 pcg genes --issuesok --plus
	./apc_build genes

2 new files: `apc.genes.txt` and `apc.log.json`

	mkdir apc
	mv genes build
	perl gather.pl apc.genes.txt
	tar -zcf apc.tar.gz apc
	mv apc build

The apc set for ws282 is XXX genes.
