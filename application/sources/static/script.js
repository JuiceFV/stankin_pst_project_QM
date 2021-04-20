try {
    var socket = new WebSocket('ws://' + window.location.host + '/ws/')
}
catch (err) {
    var socket = new WebSocket('wss://' + window.location.host + '/ws/')
}


function change_token(event) {
    event.preventDefault()
    socket.send(JSON.stringify({action: 'change'}))
}

function update_html(event) {
    data = JSON.parse(event.data)
    $('#token').html(data.token)
}


$('#change-token').click(function(e) {
    change_token(e)
});

socket.onmessage = function(e) {
    update_html(e)
}