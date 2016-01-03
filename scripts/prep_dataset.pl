#!/usr/bin/perl -w

if ($#ARGV < 1) {
    print "$0: unexpected number of arguments";
    die;
}

my $count = 0;

my %should_be_removed = map { $_ => 1 } ();
my $PREPROCESSOR = "preprocess/_main.py";
my $source_dir = shift @ARGV;
my $dest_dir = shift @ARGV;

open INDEX, ">$dest_dir/index.indx" or die "$0: cannot open $dest_dir/index.indx for writting\n";

for my $dir (glob "$source_dir/usr_*") {
    print "$0: processing directory:$dir\n" ;
    
    for my $filename (glob "$dir/*.tiff") {
	
	print "$0: processing file:$filename\n";
	my $filename_base = `basename $filename`;
	my $dirname = `basename \`dirname $filename\``;
	my $file_id = "-1";
	if ($filename_base =~ /^(\d+)t\d+\./) {
	    $file_id = $1;
	}

	if ($should_be_removed{$file_id}) {
	} else {
	    $dest_filename = $dirname;
	    $dest_filename =~ s/usr_(\d+)/$1/; chomp $dest_filename;
	    $dest_filename = "$dest_dir/u" . $dest_filename . "_" . "$filename_base" ; chomp $dest_filename;
	    print "$0: $dest_filename \t $file_id\n";
	    
	    `cp $filename $dest_filename`;

	    `python $PREPROCESSOR $dest_filename $dest_dir`;
	    $file_id = $file_id + 1 - 1;
	   
	    print INDEX "$filename\t$file_id\n";
	    $count = $count + 1;
	    print "$count of images processed so far\n"
	}
	
    }

}

close INDEX
