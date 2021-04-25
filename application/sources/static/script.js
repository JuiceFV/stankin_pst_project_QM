// Creating WebSocket object and initializing server-side websocket
let socket
try {
    // getting the client's ip address and accessing to the server
    // HTTP protocol (ws)
    socket = new WebSocket('ws://' + window.location.host + '/ws/')
}
catch (err) {
    // if error - accessing to the server with HTTPS protocol (wss)
    socket = new WebSocket('wss://' + window.location.host + '/ws/')
}

get_token = []
get_token['header'] = $('.get-token_header')
get_token['token'] = $('.get-token_token')
get_token['submit'] = $('.get-token_submit')

send_token = []
send_token['div'] = $('.send-token')
send_token['input'] = $('.send-token_input')
send_token['submit'] = $('.send-token_submit')

queue = []
queue['rows_num'] = 16
queue['cols_num'] = 4
queue['div'] = $('.queue')
queue['table'] = $('.queue_table')

cat_image = []
cat_image['div'] = $('.cat-image')
cat_image['img'] = $('.cat-image_img')


get_token['submit'].click(function(e) {
    e.preventDefault()  // blocking default event actions
    socket.send(JSON.stringify({action: 'get_token', data: {}}))  // sending json message to server websocket
});

send_token['submit'].click(function(e) {
    e.preventDefault()

    _token = send_token['input'].val()  // Getting value from input

    sending_data = {token: _token}  // Preparing data to send to server-side
    socket.send(JSON.stringify({action: 'send_token', data: sending_data}))
});

$('.get-image').click(function(e) {
    e.preventDefault()

    // Sending get image request on server
    socket.send(JSON.stringify({action: 'get_image', data: {}}))
});


socket.onmessage = function(e) {
    // This function executes once server-side websocket sends message
    // event object contains message in "data" property (e.data)
    msg = JSON.parse(e.data)  // parsing json massege that contains event object
    // executing function with same name as msg.action with arguments from msg.data
    window[msg.action](msg.data);
}


function show_token(data) {
    send_token['div'].show()
    get_token['header'].show()
    get_token['token']
        .show()
        .html(data.token)  // showing token paragraph and updating text in html
}

function show_queue(data) {
    queue['div'].show()
    queue['table'].html('')

    html = ''

    // For that builds html code of table which represents queue
    // i is rows index, j is columns index
    for (let i = 0; i < queue['rows_num']; i++) {
        // Starting new row in table
        html += '<tr>'
        for (let j = 0; j < queue['cols_num']; j++) {
            // Finding index offset
            // For example: if we have table with 16 rows and 4 columns
            // Each column is 16 rows, so offsets will be: 0, 16, 32, 48
            offset = j * queue['rows_num']
            // Then finding queue index by offset + row index
            index = i + offset
            // Since the queue indexes go sequentially from zero to len - 1
            // We can easily check out of queue bounds
            if (index < data.length)
                // Adding new column into row
                html += `<td>${data[index].token}</td>`
            else
                // Stop columns loop, because we already out of bounds
                // Next loop iterations will only increase the index
                break
        }
        // Ending new row in table
        html += '</tr>'
    }

    // Appending html code into table
    queue['table'].append(html)
}

function show_image(data) {
    cat_image['div'].show()
    cat_image['img'].attr('src', data['url'])
}