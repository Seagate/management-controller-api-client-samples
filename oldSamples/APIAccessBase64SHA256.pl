# Include required libraries
#!/usr/bin/perl
use LWP::UserAgent;
use XML::LibXML;
use HTTP::Request::Common;
use IO::Socket::SSL qw( SSL_VERIFY_NONE );

# For SHA-256 Authentication
use Digest::SHA qw(sha256_hex);
use constant use_basic_auth => 1;

my $user = "manage";
my $password = "Testit123!";
my $ip = "10.235.209.45";
my $protocol = "https";

# Create a user agent for sending requests
my $user_agent = LWP::UserAgent->new();

# Skip certificate verification
$user_agent->ssl_opts(
SSL_verify_mode => SSL_VERIFY_NONE,
verify_hostname => 0
);

my $request;
if( use_basic_auth ) {
    
	# Login with HTTP basic authentication
    my $auth_url = "$protocol://$ip/api/login/";
    $request = HTTP::Request->new( GET=>$auth_url );
    $request->authorization_basic( $user, $password );
} 
else {

    # Login with SHA-256 hash
    my $auth_data = "$user\_$password";
    my $sha256_hash = sha256_hex( $auth_data );
    my $auth_url = "$protocol://$ip/api/login/$sha256_hash";
    $request = HTTP::Request->new( GET => $auth_url );
}

# Request return data be XML format
$request->header( 'dataType'=>'ipa' );

# Make the request
$response = $user_agent->request( $request );

# Parse the returned XML and retrieve the returned session key
my $parser = XML::LibXML->new();
my $document = $parser->parse_string( $response->content );

my $root = $document->getDocumentElement;
my @objects = $root->getElementsByTagName( 'OBJECT' );
my @properties = $objects[0]->getElementsByTagName( 'PROPERTY' );

my $sessionKey;
foreach my $property ( @properties ) {
  my $name = $property->getAttribute( 'name' );
  if( $name eq 'response' ) {
     $sessionKey = $property->textContent;
  }
}

# Using the session key, request the system configuration
$url = "$protocol://$ip/api/show/configuration/";
$request = HTTP::Request->new( GET=>$url );
$request->header( 'sessionKey'=>$sessionKey );
$request->header( 'dataType'=>'ipa' );

$response = $user_agent->request( $request );

print$response->content;
