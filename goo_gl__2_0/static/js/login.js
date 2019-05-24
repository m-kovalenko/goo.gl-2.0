get_url_arguments_re = /[\?\&](\w+)=(\d+)/g
get_url_arg_val_re = /[\?\&](\w+)=(\d+)/

var GET_args = []

arg_matches = location.search.match(get_url_arguments_re);
if ( arg_matches ) {
	arg_matches.forEach(function(element) {
		let argument = element.match(get_url_arg_val_re)
		GET_args[argument[1]] = argument[2]
	});
}

if ( GET_args['errorcode'] ) {
	if ( GET_args['errorcode'] == 1 )
		alert('Wrong password!');
	else if ( GET_args['errorcode'] == 2 )
		alert('Wrong username!');
	else if ( GET_args['errorcode'] == 3 )
		alert('Username already exist!');
	else if ( GET_args['errorcode'] == 4 )
		alert('Fill in all the fields!');
}