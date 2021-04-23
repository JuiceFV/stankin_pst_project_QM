from aiohttp.web import WebSocketResponse
from . import db
from sqlalchemy import select, insert


"""
This class describes server-side socket with action handle functions
"""

class WebSocket:
    def __init__(self, request):
        self.app = request.app
        self.websocket = WebSocketResponse()  # creating websocket for communicating with client websocket
        self.ip = request.transport.get_extra_info('peername')[0]

    async def handle(self, action, data):
        func = getattr(self, action)  # getting specific function depending on the action
        await func(data)  # executing handle function with data dictionary

    # Function handles get_token request from client. Arguments don't needed so it accepts nothing
    async def get_token(self, _):
        token = self.app['token_gen'].generate()
        msg = {'token': token}
        await self.websocket.send_json(msg)  # sending json data to client-side

    # Function handles send_token request from client
    async def send_token(self, data):  # accepts data dict from handler
        token = data['token']
        if token in self.app['token_gen'].tokens:
            # Acquiring new connection to database
            async with self.app['db'].acquire() as conn:
                # Inserting values into database
                query = db.tokens.insert().values({'ip':self.ip, 'token':token})
                await conn.execute(query)

                # Printing all database values for testing
                query = db.tokens.select()
                async for row in conn.execute(query):
                    print(row)