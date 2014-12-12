var current_switch_state = true;

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
}

function get_light_state (listener) {
	simple_get("/light/state/get", function (xhr) {
		if (xhr.readyState == 4 && xhr.status == 200) {
			var state = xhr.responseText;
			listener(state);
		};
	})
}

function set_light_state (state, listener) {
	simple_get("light/state/set?on="+state?"1":"0", function (xhr) {
		if (xhr.readyState == 4 && xhr.status == 200) {
			current_switch_state = state;
			switch_light_ui(current_switch_state);
		};
	})
}

document.addEventListener("DOMContentLoaded", function () {
	get_light_state(function (state) {
		switch_light_ui(state == "1");
		getElementById('start-overlay').style.display="none";
		document.getElementById('light-switch').onclick = function (event) {
			current_switch_state = !current_switch_state;
			set_light_state(current_switch_state);
		}
	})
})