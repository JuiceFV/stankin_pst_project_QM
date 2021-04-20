from aiohttp.web import WebSocketResponse
import asyncio
import json
from aiohttp_jinja2 import template


@template('index.html')
async def index(request):
    context = {}
    return context


async def change_token(app):
    token = app['token_gen'].generate()
    msg = {'token': token}

    await asyncio.wait([sock.send_json(msg) for sock in app['websockets']])


async def ws_handler(request):
    app = request.app
    ws = WebSocketResponse()
    await ws.prepare(request)

    app['websockets'].append(ws)

    try:
        async for msg in ws:
            data = json.loads(msg.data)
            if data['action'] == 'change':
                await change_token(app)

    finally:
        app['websockets'].remove(ws)

    return ws
