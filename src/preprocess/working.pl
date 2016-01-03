#!/usr/bin/perl -w

print "$ARGV[0] -- $ARGV[1]\n";


if ($#ARGV < 1) {
    print "$0: unexpected number of arguments";
    print "$0: <src_dir> <dest_dir>";
    die;
}

my $count = 0;

my $source_dir = shift @ARGV;
my $dest_dir = shift @ARGV;

print "$0: processing directory:$source_dir\n" ;
    
for my $filename (glob "$source_dir/*.png") {
    
    print " $0: processing file:$filename\n";
    my $filename_base = `basename $filename`;   #should be in format
    my $dirname = `basename \`dirname $filename\``;
    my $file_id = "-1";
    if ($filename_base =~ /^u\d+_(\d+)t\d+\./) {
	$file_id = $1;
    }
    
    
    if ( $file_id == -1 ) { 
	print "file: $filename not added" ;
	next; 
    }
        
    if ( ! -e "$dest_dir/$file_id" ) {
	mkdir  "$dest_dir/$file_id" or die "cannot create $dest_dir/$file_id" ;
    }
    
    $dest_filename = "$dest_dir/$file_id/$filename_base";
    
    print "$0: $dest_filename \t $file_id\n";
    print "cp $filename $dest_filename\n";
    `cp $filename $dest_filename`;

    $count = $count + 1;
    print "$count of images processed so far\n"
}
