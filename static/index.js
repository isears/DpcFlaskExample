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
    $("#status_indicator")

    if(new_state.active) {
        $("#status_indicator").removeClass().addClass("active_request")
        $("#status_indicator").text("DPC refresh request in progress")
    }else {
        $("#status_indicator").removeClass().addClass("no_requests")
        $("#status_indicator").text("No DPC requests in progress")
    }
}

$(document).ready(function(){    
    var status_checker = function(){
        //console.log('Checking status of in-flight requests (if any)')
        var request = new XMLHttpRequest()
        request.open("GET", "/api/check_status", true)
        request.send()
    
        request.onload = function() {
            var backend_state = JSON.parse(this.response)
    
            if(backend_state.active != FRONTEND_STATE.active) {
                FRONTEND_STATE = backend_state
                console.log("State sync required!")
                sync_state(backend_state)
            }
        }
    }
    
    setInterval(status_checker, 1000)
    sync_state(FRONTEND_STATE)
});
