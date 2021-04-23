// Creating WebSocket object and initializing server-side websocket
try {
    // getting the client's ip address and accessing to the server
    // HTTP protocol (ws)
    var socket = new WebSocket('ws://' + window.location.host + '/ws/')
}
catch (err) {
    // if error - accessing to the server with HTTPS protocol (wss)
    var socket = new WebSocket('wss://' + window.location.host + '/ws/')
}

get_token = []
get_token['header'] = $('.get-token_header')
get_token['token'] = $('.get-token_token')
get_token['submit'] = $('.get-token_submit')

send_token = []
send_token['input'] = $('.send-token_input')
send_token['submit'] = $('.send-token_submit')


get_token['submit'].click(function(e) {
    e.preventDefault()  // blocking default event actions
    socket.send(JSON.stringify({action: 'get_token', data: {}}))  // sending json message to server websocket
});

socket.onmessage = function(e) {
    // This function executes once server-side websocket sends message
    // event object contains message in "data" property (e.data)
    data = JSON.parse(e.data)  // parsing json massege that contains event object
    get_token['header'].show()
    get_token['token'].show().html(data.token)  // showing token paragraph and updating text in html
}


send_token['submit'].click(function(e) {
    e.preventDefault()

    _token = send_token['input'].val()  // Getting value from input

    sending_data = {token: _token}  // Preparing data to send to server-side
    socket.send(JSON.stringify({action: 'send_token', data: sending_data}))
});