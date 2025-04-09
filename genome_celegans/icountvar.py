import statistics
import sys

from grimoire.genome import Reader

genome = Reader(gff=sys.argv[2], fasta=sys.argv[1])
ratios = []
for chrom in genome:
	#print(chrom.name, file=sys.stderr, flush=True)
	icount = {}
	for f in chrom.ftable.features:
		if f.source != 'RNASeq_splice': continue
		icount[(f.beg, f.end)] = f.score

	for gene in chrom.ftable.build_genes():
		if len(gene.transcripts()) == 0: continue # skip ncRNAs
		if gene.issues: continue # skip genes with obvious oddities

		for tx in gene.transcripts():
			bad_tx = False
			counts = []
			for intron in tx.introns:
				isig = (intron.beg, intron.end)
				if isig not in icount:
					bad_tx = True
					break
				counts.append(icount[isig])
			if len(counts) < 2 or bad_tx: continue
			for i in range(0, len(counts)):
				for j in range(i+1, len(counts)):
					rmax = max(counts[i]/counts[j], counts[j]/counts[i])
					if rmax > 2: continue # 2-fold max
					ratios.append(rmax)

print(statistics.mean(ratios), statistics.stdev(ratios), statistics.median(ratios))
#for ratio in ratios:
#	print(f'{ratio:.2f}')
