#!perl 
use strict ;
use feature qw(say);
use List::Util qw(first sum max shuffle maxstr);
use threads;
#use List::MoreUtils qw(uniq);
use File::Spec::Functions;
use File::Basename qw(dirname basename);
use Data::Dumper;
use Scalar::Util qw/reftype/;
use File::Copy;
use File::Find;
use POSIX qw(assert);
use Cwd qw(abs_path); 
use MIME::Base64 qw( encode_base64 decode_base64); 
#use IPC::SysV qw(IPC_PRIVATE S_IRUSR S_IWUSR S_IRWXU); 
#use IPC::SharedMem;


#use Redis; 
### global var ###

###

&main();

### sub list ### 
sub main()
{
	my $port = 10241; 
	my $cmd_run_http_server = "python -m CGIHTTPServer $port &"; 

	while (1)
	{
		my @fc = ` pgrep -l python -f |grep CGIHTTPServer |grep $port |grep -v pgrep`; 

		if (@fc == 0)
		{
			say "- restart cgi http server on $port"; 
			`cd $ENV{t}/cgi_test && $cmd_run_http_server `;
		}
		sleep 5; 
	}
}

