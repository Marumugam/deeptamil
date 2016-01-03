#!/usr/bin/perl -w 


if ($#ARGV < 0) {
    print "$0: unexpected number of arguments";
    die;
}


my $SRCDIR = shift @ARGV;
my $LABEL = shift @ARGV;

print "$SRCDIR -- $LABEL\n";

my $COMMAND = "python sfilter.py";

for my $dir (glob "$SRCDIR/*") {        
    print "under -- $dir\n";
    if (! -e "$dir/discard") {
	    print "mkdir $dir/discard\n";
	    `mkdir $dir/discard`;
    }
    print "$COMMAND $dir/ `basename $dir`\n";
    print `$COMMAND $dir/ \`basename $dir\``;
}
