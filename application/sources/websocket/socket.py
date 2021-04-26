from aiohttp.web import WebSocketResponse
import asyncio
from ..generators import generate_image

"""
This class describes server-side socket with action handle functions
"""

class WebSocket:
    def __init__(self, request):
        self.app = request.app
        self.db = self.app['db']
        self.websocket = WebSocketResponse()  # creating websocket for communicating with client websocket
        self.ip = request.transport.get_extra_info('peername')[0]

    async def handle(self, action, data):
        func = getattr(self, action)  # getting specific function depending on the action
        await func(data)  # executing handle function with data dictionary

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_token(self, _):
        # Getting TokenGenerator object from app and generating new token
        token = self.app['token_gen'].generate()
        # Forming data to send to client-side in json format
        data = {'token': token}
        # Creating message with name of function to run and its arguments (data)
        msg = {'action': 'show_token', 'data': data}

        await self.websocket.send_json(msg)  # sending json data to client-side

    # Function handles send_token request from client
    async def send_token(self, data):  # accepts data dict from handler
        token = data['token']
        if token in self.app['token_gen'].tokens:
            # Calling custom function to insert new row into database
            await self.db.insert(token, self.ip)

            # Getting all rows (entire queue) from updated database
            queue = await self.db.select()

            # Creating message with name of function to run and its arguments (data)
            msg = {'action': 'show_queue', 'data': queue}
            # sending updated queue converted to json to all clients
            await asyncio.wait([sock.send_json(msg) for sock in self.app['websockets']])

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_image(self, _):
        # Generating new cat image url
        img_url = await generate_image()
        # Forming data to send to client-side in json format
        data = {'url': img_url}
        # Creating message with name of function to run and its arguments (data)
        msg = {'action': 'show_image', 'data': data}

        await self.websocket.send_json(msg)  # sending json data to client-side