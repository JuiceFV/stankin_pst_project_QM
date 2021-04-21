from aiohttp.web import WebSocketResponse


"""
This class describes server-side socket with action handle functions
"""

class WebSocket:
    def __init__(self, request):
        self.app = request.app
        self.websocket = WebSocketResponse()  # creating websocket for communicating with client websocket

    async def handle(self, *args):  # args[0] - fucntion name, args[1] other arguments
        func = getattr(self, args[0])  # getting specific function depending on action
        await func(args[1])  # executing handle fucntion
                             # each function each function takes its own number of arguments

    async def get_token(self, _):
        token = self.app['token_gen'].generate()
        msg = {'token': token}
        await self.websocket.send_json(msg)  # sending json data to client-side


    async def send_token(self, token):
        print(token)