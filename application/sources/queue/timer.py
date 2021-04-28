import asyncio


"""
Timer class that executing callback function every time a certain time interval has passed
"""

class Timer:
    def __init__(self, callback, interval):
        # Function that will be executed everytime the time interval passes
        self.callback = callback
        self.interval = interval
        # Current token, that was just popped up from queue, for comparing with client's token
        self.cur_token = None
        # Starting run() task with ensure_future, which will allow us to start run() method and go on
        # It will never be executed
        self.task = asyncio.ensure_future(self.run())
        # Variable that controls while loop in run() method and represents running state
        self.is_running = True
        self.is_first_call = False


    # Run method does main timer's work
    async def run(self):
        # An infinite loop that after a certain interval has elapsed executing callback
        # and then again if running state is True
        while self.is_running:
            # If it's first call we immediately execute callback function
            # If it's not first call we waiting for time interval
            if not self.is_first_call:
                await asyncio.sleep(self.interval)

            # Executing callback function (queue.pop()) that returns popped token
            self.cur_token = await self.callback()

            self.is_first_call = False

    # Method that stops timer: sets running state to False and cancels run() method
    def cancel(self):
        self.is_running = False
        self.task.cancel()