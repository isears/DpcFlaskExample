var FRONTEND_STATE = {
    "active": false
}

function refresh_data(){
    console.log("Calling refresh endpoint: /api/refresh_data")
    var request = new XMLHttpRequest()
    request.open("GET", "/api/refresh_data", true)
    request.send()
}

function sync_state(new_state){
    console.log("Syncing frontend and backend states")
    console.log(new_state.active)

    status_indicator = document.getElementById("status_indicator");

    if(new_state.active) {
        $("#status_indicator").removeClass().addClass("active_request")
        $("#status_indicator").text("DPC refresh request in progress")
    }else {
        $("#status_indicator").removeClass().addClass("no_requests")
        $("#status_indicator").text("No DPC requests in progress")
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
    
            if(backend_state.active != FRONTEND_STATE.active) {

                if(FRONTEND_STATE.active) { // State change from "waiting for request" -> "request complete"
                    console.log("Fetching new data...")
                    get_data()
                }

                console.log("State sync required!")
                sync_state(backend_state)
            }
        }
    }
    
    setInterval(status_checker, 1000)
    sync_state(FRONTEND_STATE)
});
