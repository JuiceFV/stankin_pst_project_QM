from ..websocket import WebSocket
import json


async def ws_handler(request):
    """
    This function handles server websocket. Once user connects to website this function is started
    """
    app = request.app
    socket = WebSocket(request)  # creating object that describes socket
    app['sockets'].append(socket)  # saving socket for subsequent access and sending messages
    ws = socket.websocket  # getting WebSocketResponse object

    await ws.prepare(request)  # starting websocket with specific request

    # starting infinite loop for listening messages from client websocket
    try:
        async for msg in ws:
            data = json.loads(msg.data)  # loading json data from received client
            action, received_data = data['action'], data['data']
            # execution of specific function depending on the passed action with variable number of arguments
            await socket.handle(action, received_data)

    # Client disconnects from website
    finally:
        app['sockets'].remove(socket)  # removing WebSocketResponse object from app