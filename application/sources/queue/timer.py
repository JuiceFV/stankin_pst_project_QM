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
        # Variable that controls while loop in run() method and represents running state
        self.is_running = False
        # Main task that starting run() method that never ends
        # ensure_future here for instant canceling task
        # if we stopping the timer
        self.run_task = None
        # Waiting task that makes run() method wait for certain time
        # ensure_future for instant canceling (skipping) this task
        # if client getting an image
        self.sleep_task = None

    async def start(self):
        self.is_running = True
        # Starting run() task with ensure_future, which will allow us to start run() method and go on
        # It will never be executed
        self.run_task = asyncio.ensure_future(self.run())

    # Waiting coroutine that waits for interval time
    async def wait(self):
        # Sleep coroutine that will be executed
        self.sleep_coro = asyncio.sleep(self.interval)
        # Wrapping sleep coroutine into ensure_future that gives us future object
        # Future object can be canceled instantly
        self.sleep_task = asyncio.ensure_future(self.sleep_coro)

        try:
            # Starting sleep task and wait for it
            # Now we can interrupt sleep by executing sleep_task.cancel() because it's future object
            await self.sleep_task
        except asyncio.CancelledError:
            # sleep task is canceled and we just returning
            return
        finally:
            # sleep task is finished and we just returning too
            return

    # Run method does main timer's work
    async def run(self):
        # An infinite loop that after a certain interval has elapsed executing callback
        # and then again if running state is True
        while self.is_running:
            # Executing callback function before timer starts
            await self.on_start()
            # Waiting for some time interval
            await self.wait()
            # Executing callback function after timer ends
            await self.on_end()

    # Method skips current waiting by canceling current sleep task
    async def skip(self):
        self.sleep_task.cancel()

    # Method that instantly stops timer
    def cancel(self):
        self.is_running = False
        self.sleep_task.cancel()
        self.run_task.cancel()

    # Method resets timer (stops and then starts it again)
    async def reset(self):
        self.cancel()
        await self.start()