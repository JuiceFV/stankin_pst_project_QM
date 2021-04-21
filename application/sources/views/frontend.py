from aiohttp.web import WebSocketResponse
import asyncio
import json
from aiohttp_jinja2 import template
from ..WebSocket import WebSocket


@template('index.html')
async def index(request):
    context = {}
    return context


async def ws_handler(request):
    """
    This function handles server websocket. Once user connects to website this function is started
    """
    app = request.app
    socket = WebSocket(request)  # creating object that describes socket
    ws = socket.websocket  # getting WebSocketResponse object

    await ws.prepare(request)  # starting websocket with specific request

    app['websockets'].append(ws)  # saving websocket for subsequent access and sending messages

    # starting infinite loop for listening messages from client websocket
    try:
        async for msg in ws:
            data = json.loads(msg.data)  # loading json data from received client
            action = data['action']
            args = data['args']
            await socket.handle(action, args)  # execution of specific function depending on the passed action
                                               # with variable number of arguments4

    # Client disconnects from website
    finally:
        app['websockets'].remove(ws)  # removing WebSocketResponse object from app=
