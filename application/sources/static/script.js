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


error_msg = {
    'has_token': 'You already have token. You need to send it to queue.',
    'empty_token': 'You sent empty token. Try again.',
    'is_in_queue': 'You are already in the queue. Please wait for your turn.',
    'token_mismatch': 'Sent token does not belong to you or does not exist. Try again.',
    'empty_queue': 'Current queue is empty. Get another token.',
    'not_first': 'You are not first in the queue. Please wait for your turn.'
}

get_token = []
get_token['header'] = $('.get-token_header')
get_token['token'] = $('.get-token_token')
get_token['submit'] = $('.get-token_submit')

insert_token = []
insert_token['div'] = $('.insert-token')
insert_token['input'] = $('.insert-token_input')
insert_token['submit'] = $('.insert-token_submit')

queue = []
queue['rows_num'] = 16
queue['cols_num'] = 4
queue['div'] = $('.queue')
queue['table'] = $('.queue_table')

cat_image = []
cat_image['div'] = $('.cat-image')
cat_image['submit'] = $('.get-image_submit')
cat_image['img'] = $('.cat-image_img')


get_token['submit'].click(function(e) {
    e.preventDefault()  // blocking default event actions
    socket.send(JSON.stringify({action: 'get_token', data: {}}))  // sending json message to server websocket
});

$('.get-token_copy').click(function(e) {
    e.preventDefault()  // blocking default event actions

    token = $('#token')[0].innerHTML
    copyToClipboard(token)
});

insert_token['submit'].click(function(e) {
    e.preventDefault()

    _token = insert_token['input'].val()  // Getting value from input

    if (_token) {
        sending_data = {token: _token}  // Preparing data to send to server-side
        socket.send(JSON.stringify({action: 'insert_token', data: sending_data}))

        insert_token['input'].val('')
    }
    else {
        data = {error: 'empty_token'}
        show_error(data)
    }

});

cat_image['submit'].click(function(e) {
    e.preventDefault()

    // Sending get image request on server
    socket.send(JSON.stringify({action: 'get_image', data: {}}))
});


socket.onmessage = function(e) {
    // This function executes once server-side websocket sends message
    // event object contains message in "data" property (e.data)
    msg = JSON.parse(e.data)  // parsing json message that contains event object
    // executing function with same name as msg.action with arguments from msg.data
    window[msg.action](msg.data);
}


function show_token(data) {
    insert_token['div'].show()
    get_token['header'].show()
    get_token['token']
        .show()
        .html(data.token)  // showing token paragraph and updating text in html
}

function show_queue(tokens) {
    queue['div'].show()
    queue['table'].html('')

    html = get_queue_html(tokens)

    // Appending html code into table
    queue['table'].append(html)
}

function hide_queue(_) {
    // if client got image or missed his turn - hiding queue block and showing image block
    queue['table'].html('')
    queue['div'].hide()
}

function show_image(data) {
    cat_image['div'].show()
    cat_image['img'].attr('src', data['url'])
}

function show_error(data) {
    alert(error_msg[data.error])
}


function get_queue_html(tokens) {
    html = ''
    // Building html code of table which represents queue
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
            if (index < tokens.length)
                // Adding new column into row
                html += `<td>${tokens[index]}</td>`
            else
                // Stop columns loop, because we already out of bounds
                // Next loop iterations will only increase the index
                break
        }
        // Ending new row in table
        html += '</tr>'
    }

    return html
}

function copyToClipboard(str) {
    let area = document.createElement('textarea');
    document.body.appendChild(area);

    area.value = str;
    area.select();
    document.execCommand("copy");

    document.body.removeChild(area);
}