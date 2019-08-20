#!/home/jd/t/git/perl-5.26.1/out/bin/perl
use CGI;                             
use Data::Dumper; 
#use JSON; 

$co = new CGI;                        

&main(); 

sub main()
{
	$| = 1;
	print $co->header;
	#print $co->header, $co->start_html( -title=>'CGI Example', -author=>'yourName', -BGCOLOR=>'white', -LINK=>'red');
=pod
=cut

#print Dumper($co); 

	my $ff = "perl $ENV{perl_p}/ff.PL"; 
	my @fc_tmi =  qx{cat ./tmi_templ.txt |grep tell_my_ip| $ff 0 1 2 6}; 
	#my @fc_tmi =  qx{$ENV{t}/tell_my_ip/tell_my_ip all|grep tell_my_ip| $ff 0 1 2 6}; 



   
   my @fc_templ = `cat ./tell_my_ip.html`;
   #my @fc_templ = `cat $ENV{t}/cgi_test/cgi-bin/tell_my_ip.html`;
   my @fc_ip_list = `cat ./ip_list.txt`;
   #my @fc_ip_list = `cat $ENV{t}/cgi_test/cgi-bin/ip_list.txt`;

   my $flag_clear_table = 0; 
   my $cnt_table = 0; 
   my $loc_table = 0; 
   map
   {
       if (m/\<table/)
       {
           $flag_clear_table = 1;
           $loc_table = $cnt_table;
       }
       if (m/\<\/table/)
       {
           $_ = "";
           $flag_clear_table = 0;  
       }
       
       if ($flag_clear_table == 1)
       {
           $_ = "";
       }

       $cnt_table++;
   }@fc_templ;



	my $ret_str =  ""; 
	if (1)
	{
		$ret_str = q{<table>}."\n"; 

		$ret_str .= q{<thead>
			<tr>
				<th>time</th>
				<th>type</th>
				<th>ip</th>
				<th>mac_addr</th>
				</tr>
				</thead>
		} . "\n"; 

		$ret_str .= "<tbody>"."\n"; 


		map{s/.tell_my_ip.txt//; }@fc_tmi;

		@fc_tmi = &fc_hash_it(\@fc_tmi);

		$ret_str .=  &for_each_line($fc_tmi[0], "b") . "\n"; 

		map{$ret_str .= &for_each_line($_);}@fc_tmi[1..@fc_tmi-2];



		$ret_str .= q{</tbody></table> }."\n"; 

		$fc_templ[$loc_table] = $ret_str;
		$fc_templ[$loc_table+1] = &raw_ip_data(\@fc_ip_list). q{<br>
			<hr> <p><div syle="font-size:41px" align=right >
				Written by Jidor Tang tlqtangok@126.com. Copyright 2018-2019
				</div></p></hr> <br>};

	}

    #print $ret_str; 

    print @fc_templ, "<br>", q{};



    0;

	#print $co->end_html; 
}

sub raw_ip_data(\@)
{
	my $ref_fc = shift;

	my $ret_str = q{<br><br><br><br><table>
		<thead>
			<tr>
			<th>MAC</th><th>PW</th><th>hostname</th><th>location</th><th>responsible</th><th>CPU</th><th>MEM</th><th>storage</th><th>GPU</th><th>usage</th><th>whom</th><th>serial</th>
			</tr>
			</thead>}; 


	map{
		$ret_str .= &for_each_line_ip_list($_);
	}@$ref_fc;

	return $ret_str. q{</tbody></table>};
}

sub for_each_line_ip_list($, $)
{
	my $e_line = shift;
	my $need_b = shift;

	chomp($e_line);
	my @arr = split "\t", $e_line;
	my $ret_str = "\n"; 

	map{$_ = "<td>$_</td>"."\n"; }@arr;

	my $k_str = "@arr"; 

	if ($need_b ne "")
	{
		$ret_str .= q{<tr style="font-weight:bold">}. $k_str . q{</tr>}. "\n"; 
	}
	else
	{
		$ret_str .= q{<tr>}. $k_str . q{</tr>}. "\n"; 
	}
	return $ret_str; 
}


sub for_each_line($, $)
{
	my $e_line = shift;
	my $need_b = shift;

	chomp($e_line);
	my @arr = split m/\s+/, $e_line;
	my $ret_str = "\n"; 

	map{$_ = "<td>$_</td>"."\n"; }@arr;

	my $k_str = "@arr"; 

	if ($need_b ne "")
	{
		$ret_str .= q{<tr style="font-weight:bold">}. $k_str . q{</tr>}. "\n"; 
	}
	else
	{
		$ret_str .= q{<tr>}. $k_str . q{</tr>}. "\n"; 
	}
	return $ret_str; 
}


sub fc_hash_it(\@fc)
{
	my $ref_fc = shift; 

	@$ref_fc = reverse @$ref_fc;
	my %hash_ip = (); 

	my @ret_fc = (); 
	for ( @$ref_fc )
	{

		my @fields = split m/\s+/,$_;
		if (! exists $hash_ip{$fields[-1]} )
		{
			$hash_ip{@fields[-1]}  = $_;
			push @ret_fc, $_; 
		}
	}



	return @ret_fc;

}
