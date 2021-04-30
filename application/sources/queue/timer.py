import asyncio


"""
Timer class that executing callback function every time a certain time interval has passed
"""

class Timer:
    def __init__(self, on_start, on_end, interval):
        # Function that will be executed everytime the time interval starts
        self.on_start = on_start
        # Function that will be executed everytime the time interval ends
        self.on_end = on_end
        self.interval = interval
        # Starting run() task with ensure_future, which will allow us to start run() method and go on
        # It will never be executed
        self.task = asyncio.ensure_future(self.run())
        # Variable that controls while loop in run() method and represents running state
        self.is_running = True

    # Run method does main timer's work
    async def run(self):
        # An infinite loop that after a certain interval has elapsed executing callback
        # and then again if running state is True
        while self.is_running:
            # Executing callback function before timer starts
            await self.on_start()

            await asyncio.sleep(self.interval)
            # Executing callback function after timer ends
            await self.on_end()

    # Method that stops timer: sets running state to False and cancels run() method
    def cancel(self):
        self.is_running = False
        self.task.cancel()