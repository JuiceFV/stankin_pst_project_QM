from .timer import Timer
import asyncio


"""
Class that represents clients queue
Clients queue starts the timer, that pops up tokens (rows) from database
Also it provides notifies to all clients that are currently in queue
"""

class Queue:
    def __init__(self, app):
        self.app = app
        self.db = app['db']
        # Starting timer that will pop up token from queue every 15 seconds
        self.timer = Timer(self.pop_first, self.remove_first, 10)
        self.first = None

    # Method that pops up first row in database
    async def pop_first(self):
        #self.first_in_queue = await self.db.pop()
        self.first = await self.db.get_first_row()

    # Method deletes first row in database, that was popped up earlier
    async def remove_first(self):
        await self.db.delete({'id':self.first['id']})
        # Sending updated queue to all clients
        await self.send_queue()

    # Method that notifying all clients and sending updated queue
    async def send_queue(self):
        # Getting all rows (entire queue) from updated database
        queue = await self.db.get_tokens()

        # Creating message with name of function to run and its arguments (data)
        msg = {'action': 'show_queue', 'data': queue}
        # sending updated queue converted to json to all clients
        for sock in self.app['sockets']:
            if sock.is_in_queue:
                await sock.websocket.send_json(msg)

    def is_first_in_queue(self, token, ip):
        if token == self.first['token'] and ip == self.first['ip']:
            return True

        return False
