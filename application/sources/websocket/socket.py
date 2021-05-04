from aiohttp.web import WebSocketResponse
from ..generators import generate_image

"""
This class describes server-side socket with action handle functions
"""

class WebSocket:
    def __init__(self, request):
        self.app = request.app
        self.db = self.app['db']
        # Creating websocket for communicating with client websocket
        self.websocket = WebSocketResponse()
        # Getting client's ip
        self.ip = request.transport.get_extra_info('peername')[0]
        self.token = None
        self.is_in_queue = False

    # When client got his cat image or time to get cat image is over, we reset its token
    def reset_token(self):
        self.token = None
        self.is_in_queue = False

    # Function that sending response from server to client side
    # with some action (function to do) and data (function arguments)
    async def response(self, action, data):
        # Creating message with name of function to run and its arguments (data)
        msg = {'action': action, 'data': data}
        await self.websocket.send_json(msg)

    # Function that handles all messages from client and performing action with data
    async def handle(self, action, data):
        func = getattr(self, action)  # getting specific function depending on the action
        await func(data)  # executing handle function with data dictionary

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_token(self, _):
        if not self.token:
            # Getting TokenGenerator object from app and generating new token
            token = self.app['token_gen'].generate()
            # Saving client's token for subsequent checks, when client is trying to insert token
            self.token = token
            # Forming data to send to client-side in json format
            data = {'token': token}
            # Sending show token action with data that contains generated token
            await self.response(action='show_token', data=data)

        else:
            # Responding with error and specific data
            data = {'error': 'has_token'}
            await self.response(action='show_error', data=data)


    # Function handles insert_token request from client
    async def insert_token(self, data):  # accepts data dict from handler
        if self.is_in_queue:
            data = {'error': 'is_in_queue'}
            await self.response(action='show_error', data=data)
            return

        token = data['token']
        if token == self.token:
            self.is_in_queue = True
            await self.app['queue'].insert(token=self.token, ip=self.ip)

        else:
            data = {'error': 'token_mismatch'}
            await self.response(action='show_error', data=data)

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_image(self, _):
        if self.app['queue'].is_empty:
            data = {'error': 'empty_queue'}
            await self.response(action='show_error', data=data)
            return

        if await self.app['queue'].is_first_in_queue(token=self.token, ip=self.ip):
            # Generating new cat image url
            img_url = await generate_image()
            # Forming data to send to client-side in json format
            data = {'url': img_url}
            await self.response(action='show_image', data=data)

            # Skipping current waiting task (client got his cat image)
            # Getting to the next one
            await self.app['queue'].skip()

        else:
            data = {'error': 'not_first'}
            await self.response(action='show_error', data=data)