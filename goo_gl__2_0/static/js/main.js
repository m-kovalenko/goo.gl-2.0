get_url_arguments_re = /[\?\&](\w+)=(\d+)/g
get_url_arg_val_re = /[\?\&](\w+)=(\d+)/

var GET_args = []


if ( user_id == 0 ) {
	document.getElementById('logout-link').style.display='none';
}
else {
	document.getElementById('login-link').style.display='none';
}

arg_matches = location.search.match(get_url_arguments_re);
if ( arg_matches ) {
	arg_matches.forEach(function(element) {
		let argument = element.match(get_url_arg_val_re)
		GET_args[argument[1]] = argument[2]
	});
}