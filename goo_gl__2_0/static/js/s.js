
var input = document.getElementById('link-input');
var button = document.getElementById('submit-button');
var saved_url = 'Не вводи мой костылик(';
var link_for_saver = '/s/?';

const url_regex = /[-a-zA-Z0-9@:%\._\+~#=]{2,256}\.[a-z0-9]{2,6}\b[-a-zA-Z0-9@:%_\+.~#?&\/=]*/u;

const BUTTON_STATE_READY = 0;
const BUTTON_STATE_SAVED = 1;
const BUTTON_STATE_INVALID = 2;

button_states_map = [
	[
		'Submit',
		'ready'
	],
	[
		'Saved!',
		'saved'
	],
	[
		'Invalid input!',
		'invalid'
	]
];

function set_button_state(state) {
	if ( button.innerHTML != button_states_map[state][0] ) {
		button.innerHTML =  button_states_map[state][0];
		button_states_map.forEach(function(element) {
			button.classList.remove('button-' + element[1]);
		});
		if ( state == 1 || state == 2 ) {
			button.setAttribute('disabled', '');
		}
		else {
			button.removeAttribute('disabled', '');
		}
		button.classList.add('button-' + button_states_map[state][1]);
	}
}


function input_event_hook() {
	if ( input.value == saved_url ) {
		set_button_state(BUTTON_STATE_SAVED)
	}
	else {
		let url = input.value.match(url_regex);
		if ( url == null ) {
			set_button_state(BUTTON_STATE_INVALID);
		}
		else {
			set_button_state(BUTTON_STATE_READY);
		}
	}
};
input_event_hook()
input.oninput = input_event_hook

function make_xhr() {
	let xhr = new XMLHttpRequest();
	let params = 'link=' + encodeURIComponent(input.value);
	let param_user_id = 0
	if ( user_id != 0 && document.getElementById('is-private-checkbox').checked ) {
		param_user_id = user_id
	}
	params += '&user_id=' + encodeURIComponent(param_user_id);
	xhr.open("GET", link_for_saver + params, true);
	xhr.send();
	xhr.onreadystatechange = function() {
	if (xhr.readyState != 4) return;
		if (xhr.status != 200) {
			alert( 'Error! ' + xhr.status + ': ' + xhr.statusText );
		} else {
			xhr_response = xhr.responseText;
			xhr_response = JSON.parse(xhr_response)
			if ( xhr_response.status.code != 0 ) {
				alert( 'Error! ' + xhr_response.status.code + ': ' + xhr_response.status.text );
			}
			else {
                input.value = xhr_response.landing_url;
                saved_url = xhr_response.landing_url
                set_button_state(BUTTON_STATE_SAVED)
		    }
		}
	}
}