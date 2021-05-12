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

    # Function that checks if ip is in queue
    async def is_got_token(self):
        # Getting all rows (whole queue) from database
        ip_addresses = await self.db.get_ip_addresses()
        # Trying to find client's ip address in queue
        is_ip_exist = self.ip in ip_addresses
        # Checking if client already got token
        is_token_exist = self.token is not None

        return is_token_exist or is_ip_exist

    async def check_token_in_queue(self, token):
        tokens = await self.db.get_tokens()
        if not tokens:
            return False
        else:
            return token in tokens

    # Function that handles all messages from client and performing action with data
    async def handle(self, action, data):
        func = getattr(self, action)  # getting specific function depending on the action
        await func(data)  # executing handle function with data dictionary

    async def init_token(self, data):
        self.token = data['token']
        await self.send_token(self.token)

        self.is_in_queue = await self.check_token_in_queue(self.token)
        if self.is_in_queue:
            await self.send_queue()

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_token(self, _):
        if not await self.is_got_token():
            # Getting TokenGenerator object from app and generating new token
            token = self.app['token_gen'].generate()
            # Saving client's token for subsequent checks, when client is trying to insert token
            self.token = token

            await self.send_token(self.token)

        else:
            await self.send_error('has_token')

    # Function handles insert_token request from client
    async def insert_token(self, data):  # accepts data dict from handler
        if self.is_in_queue:
            await self.send_error('is_in_queue')
            return

        token = data['token']
        if token == self.token:
            self.is_in_queue = True
            await self.app['queue'].insert(token=self.token, ip=self.ip)

        else:
            await self.send_error('token_mismatch')

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_image(self, _):
        if self.app['queue'].is_empty:
            await self.send_error('empty_queue')
            return

        if await self.app['queue'].is_first_in_queue(token=self.token, ip=self.ip):
            # Generating new cat image url
            img_url = await generate_image()
            # Forming data to send to client-side in json format
            data = {'url': img_url}
            await self.response(action='show_image', data=data)
            await self.response(action='delete_token', data={})

            # Skipping current waiting task (client got his cat image)
            # Getting to the next one
            await self.app['queue'].skip()

        else:
            await self.send_error('not_first')

    # Function that sending response from server to client side
    # with some action (function to do) and data (function arguments)
    async def response(self, action, data):
        # Creating message with name of function to run and its arguments (data)
        msg = {'action': action, 'data': data}
        await self.websocket.send_json(msg)

    async def send_queue(self):
        # Getting all rows (entire queue) from updated database
        queue = await self.db.get_tokens()
        # sending queue to current client-side websocket
        await self.response(action='show_queue', data=queue)

    async def send_token(self, token):
        # Forming data to send to client-side in json format
        data = {'token': token}
        # Sending show token action with data that contains generated token
        await self.response(action='show_token', data=data)

    async def send_error(self, error_type):
        # Responding with error
        data = {'error': error_type}
        await self.response(action='show_error', data=data)