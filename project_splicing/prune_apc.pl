use strict;
use warnings;

my @genes;
open(my $fh, "apc.genes.txt") or die;
while (<$fh>) {
	next if /^#/;
	chomp;
	my ($ch, $introns, $rna, $iso) = split;
	push @genes, {base => $ch, introns => $introns, rna => $rna, iso => $iso};
}

if (not -s "build/apc.fa") {
	foreach my $gene (@genes) {
		`cat build/genes/$gene->{base}.fa >> build/apc.fa`;
	}
	`makeblastdb -in build/apc.fa -dbtype nucl`;
	`blastn -db build/apc.fa -query build/apc.fa -evalue 1e-20 -outfmt 6 > build/apc.blast`;
}

my %clust;
my %used;
open(my $bfh, "build/apc.blast") or die;
while (<$bfh>) {
	my ($q, $s, @f) = split;
	next if $q eq $s;
	print;
	next if exists $used{$s};
	$clust{$q}{$s} = 1;
	$used{$s} = 1;
}

foreach my $id (keys %used) {print "$id\n"}




__END__

my $root = "build/genes";
while (<>) {
	next if /^#/;
	my ($id) = split;
	system("cp $root/$id.fa apc");
	system("cp $root/$id.gff3 apc");
}


ch.13484        ch.13484        100.000 537     0       0       1       537     1       537     0.0     992
ch.13506        ch.13506        100.000 683     0       0       1       683     1       683     0.0     1262
