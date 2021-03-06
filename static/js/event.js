var current_switch_state = 0;

function is_state_on (state) {
	return state == 1 || state == '1' || state == true;
}

var is_mobile = (navigator.userAgent.indexOf("Android")!=-1 || navigator.userAgent.indexOf("iPhone")!=-1)

function set_click_handler (element, handler) {
	if (is_mobile) {
		console.log('device is mobile')
		element.ontouchend = handler;
	} else {
		console.log('device is desktop computer')
		element.onclick = handler;
	}
}

function ajax (path, method, async, listener) {
	var xhr = new XMLHttpRequest();
	xhr.open(method, path, async);
	xhr.onreadystatechange = function () {
		listener(xhr);
	};
	xhr.send();
}

function simple_get (path, listener) {
	ajax(path, "GET", true, listener);
}

function switch_light_ui (light_on) {
	document.getElementById('light-switch').setAttribute("on", light_on?"true":"false");
	current_switch_state = light_on;
	console.log('set light ui to '+light_on)
}

function get_light_state (listener) {
	simple_get("/light/state/get", function (xhr) {
		if (xhr.readyState == 4 && xhr.status == 200) {
			var state = parseInt(xhr.responseText);
			console.log('got light state from server: '+state)
			listener(state);
		};
	})
}

function set_light_state (state, listener) {
	simple_get("light/state/set?on="+(state), function (xhr) {
		if (xhr.readyState == 4 && xhr.status == 200) {
			console.log('send switch light command to server: '+state)
			switch_light_ui(current_switch_state);
		};
	})
}

document.addEventListener("DOMContentLoaded", function () {
	get_light_state(function (state) {
		document.getElementById('start-overlay').style.display="none";
		switch_light_ui(state);
		set_click_handler(document.getElementById('light-switch'), function (event) {
			current_switch_state = parseInt(current_switch_state)==0?1:0;
			console.log('light-switch clicked, switch to state: '+current_switch_state)
			set_light_state(current_switch_state);
		});
	})
})