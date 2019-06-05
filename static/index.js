var FRONTEND_STATE = {
    "running": false,
    "error_msg": "",
    "provider_id": ""
}

function refresh_data(){
    console.log("Calling refresh endpoint: /api/refresh_data")
    var request = new XMLHttpRequest()
    request.open("GET", "/api/refresh_data", true)
    request.send()
}

function sync_state(new_state){
    console.log("Syncing frontend and backend states")

    status_indicator = document.getElementById("status_indicator");
    console.log("Error msg: "  + new_state.error_msg)

    if(new_state.error_msg) {
        $("#status_indicator").removeClass().addClass("errored_request")
        $("#status_indicator").empty()
        $("#status_indicator").append("<p>Error communicating with DPC</p>")
        $("#status_indicator").append("<p>" + new_state.error_msg + "</p>")
    } else {
        if(new_state.running) {
            $("#status_indicator").removeClass().addClass("active_request")
            $("#status_indicator").text("DPC refresh request in progress")
        }else if(!new_state.running) {
            $("#status_indicator").removeClass().addClass("no_requests")
            $("#status_indicator").text("No DPC requests in progress")
        }
    }
    

    FRONTEND_STATE = new_state
}

function get_data() {
    var request = new XMLHttpRequest()
    request.open("GET", "/api/getdata", true)
    request.send()

    request.onload = function() {
        console.log("receiving data from backend...")

        $("#data_preview").empty()
        $("#data_preview").append(this.response)
    }
}

$(document).ready(function(){    
    var status_checker = function(){
        var request = new XMLHttpRequest()
        request.open("GET", "/api/check_status", true)
        request.send()
    
        request.onload = function() {
            var backend_state = JSON.parse(this.response)
    
            if(backend_state.running != FRONTEND_STATE.running) {

                if(FRONTEND_STATE.active) { // State change from "waiting for request" -> "request complete"
                    console.log("Fetching new data...")
                    get_data()
                }
            }

            if(
                backend_state.running != FRONTEND_STATE.running ||
                backend_state.provider_id != FRONTEND_STATE.provider_id ||
                backend_state.error_msg != FRONTEND_STATE.error_msg
            ){
                console.log("States out of sync, frontend changes required")
                sync_state(backend_state)
            }
        }
    }
    
    setInterval(status_checker, 1000)
    sync_state(FRONTEND_STATE)
    get_data()
});
