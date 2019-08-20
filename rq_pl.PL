use HTTP::Request::Common; 
use LWP::UserAgent;
$user_agent = LWP::UserAgent->new;
# ../cgi-bin/cgi.cgi
$request = POST 'http://localhost:10244/cgi-bin/cgi.cgi', 
[text1 => 'Hello', text2 => 'there'];
$response = $user_agent->request($request);
print $response->as_string;

