function is_state_on(state) {
    return state == 1 || state == '1' || state == true;
}

function ajax(path, method, async, listener) {
    var xhr = new XMLHttpRequest();
    var host = "http://home.joker.li:3568"
    xhr.open(method, host + path, async);
    xhr.onreadystatechange = function(e) {
        if (!listener) {
            return;
        }
        var xhr = e.target;
        if (xhr.readyState == 4) {
            if (xhr.status == 200 && listener.success) {
                listener.success(xhr);
            } else if (listener.error) {
                listener.error(xhr);
            }
        }
    };
    xhr.send();
}

function simple_get(path, listener) {
    ajax(path, "GET", true, listener);
}

function get_lights(listener) {
    simple_get("/lights", {
        success: function(xhr) {
            var res = JSON.parse(xhr.response);
            listener(res);
        }
    })
}

document.addEventListener("DOMContentLoaded", function() {
    var scanVm = new Vue({
        el: "#scan-dialog",
        data: {
        	scaning: true,
            lights: []
        },
        methods: {
            selectScan: function(e) {
                var light = this.lights[e];
                simple_get("/add/" + light.addr + "/" + light.name, {
                    success: this.connectSuccess
                });
            },
            connectSuccess: function(xhr) {
                console.log(xhr.response);
                get_lights(function(lights) {
                    vm.ready = true;
                    vm.lights = lights.map(function(lt) {
                        if (lt.online) {
                            lt.on = (lt.value === "N1");
                        }
                        return lt;
                    });
                    setTimeout(vm.updateMDL, 0);
                });
            },
            scanBle: function() {
                document.querySelector("#scan-dialog").showModal();
                this.scaning = true;
                simple_get("/scan", {
                    success: this.onScanResult,
                });
            },
            closeDialog: function() {
                document.querySelector("#scan-dialog").close();
            },
            onScanResult: function(xhr) {
                var bles = JSON.parse(xhr.response);
                this.lights = bles;
                this.scaning = false;
            }
        }
    });

    var vm = new Vue({
        el: "#smart-container",
        data: {
            ready: false,
            showScanDialog: false,
            lights: []
        },
        methods: {
            updateMDL: function() {
                document.querySelectorAll("label.mdl-switch").forEach(function(mdl_sw) {
                    componentHandler.upgradeElement(mdl_sw);
                })
            },
            addDevice: function(e) {
                scanVm.scanBle();
            },
            updateName: function(e) {
                var light = this.lights[e];
                var name = prompt("给个新名字嘛~");
                if (name) {
                    simple_get("/light/name/" + light.addr + "/" + name);
                }
            },
            toggleLightSwitch: function(e) {
                var light = this.lights[e];
				console.log(light);
                simple_get("/light/set/" + light.addr + "?val=S" + (light.on ? 1 : 0) + "$", {
                    success: function(xhr) {
                        if (xhr.response === "N1") {
                            console.log("switch light on!");
                        }
                    },
                    error: function(xhr) {
                        console.error(JSON.stringify(xhr));
                    }
                });
            }
        }
    });


    get_lights(function(lights) {
        vm.ready = true;
        vm.lights = lights.map(function(lt) {
            if (lt.online) {
                lt.on = (lt.value === "N1");
            }
            return lt;
        });
        setTimeout(vm.updateMDL, 0);
		scanVm.closeDialog();
    });

})
