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