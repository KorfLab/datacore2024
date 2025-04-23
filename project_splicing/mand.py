import argparse
import glob
import json
import os
import re
import statistics
import subprocess
import sys

from grimoire.genome import Reader
from isoform2 import Locus

#######
# CLI #
#######

parser = argparse.ArgumentParser(
	description='checking something...')
parser.add_argument('genes', type=str, metavar='<genes dir>',
	help='path to gene build directory')
parser.add_argument('--debug', action='store_true')
arg = parser.parse_args()

########
# Main #
########

mands = {}
for ff in glob.glob(f'{arg.genes}/*.fa'):
	gf = ff[:-2] + 'gff3'

	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome) # there is only one in a pcg build

	genes = len([None for f in chrom.ftable.features if f.type == 'gene'])
	if genes > 1: continue

	gene = chrom.ftable.build_genes()[0] # the one true gene

	#if len(gene.transcripts()) > 1: continue

	max_introns = 0
	for tx in gene.transcripts():
		if len(tx.introns) > max_introns: max_introns = len(tx.introns)
	if max_introns == 0: continue

	weird = False
	for tx in gene.transcripts():
		if tx.issues:
			weird = True
			break
	if weird: continue

	##########

	# convert RNASeq_splice counts to probs
	total_score = 0
	for f in chrom.ftable.features:
		if f.source != 'RNASeq_splice': continue
		total_score += f.score

	rss = {}
	for f in chrom.ftable.features:
		if f.source != 'RNASeq_splice': continue
		rss[(f.beg,f.end)] = f.score / total_score

	# convert tx to probs
	total_splices = 0
	splices = {}
	for tx in gene.transcripts():
		for intron in tx.introns:
			sig = (intron.beg, intron.end)
			if sig not in splices: splices[sig] = 0
			splices[sig] += 1
			total_splices += 1

	for sig, n in splices.items():
		splices[sig] = n / total_splices

	# compare RNA_seq to observed
	d = 0
	for sig in rss | splices:
		if sig in rss and sig in splices: d += abs(rss[sig] - splices[sig])
		elif sig in rss: d += rss[sig]
		elif sig in splices: d += splices[sig]
		else: sys.exit('no')

	if max_introns not in mands:
		mands[max_introns] = []

	mands[max_introns].append(d)

for i in range(1, 9):
	print(i, statistics.mean(mands[i]), statistics.stdev(mands[i]))
