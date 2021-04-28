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
        # Starting timer that will pop up token from queue every 10 second
        self.timer = Timer(self.pop, 3)
        self.cur_row = None

    # Method pops up last row in database
    async def pop(self):
        self.cur_row = await self.db.pop()

        # Notifying all clients about changes in database and sending updated queue to all of them
        await self.notify_all()

        return self.cur_row

    # Method that notifying all clients and sending updated queue
    async def notify_all(self):
        # Getting all rows (entire queue) from updated database
        queue = await self.db.get_tokens()

        # Creating message with name of function to run and its arguments (data)
        msg = {'action': 'show_queue', 'data': queue}
        # sending updated queue converted to json to all clients
        for sock in self.app['sockets']:
            if sock.is_in_queue:
                await sock.websocket.send_json(msg)
