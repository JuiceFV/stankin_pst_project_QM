from .timer import Timer


"""
Class that represents tokens queue
Work in progress
"""

class TokenQueue:
    def __init__(self, data=None):
        self.queue = data
        # Starting timer that will pop up token from queue every second
        self.timer = Timer(self.pop, 1)
        self.token_num = 1


    async def pop(self):
        print(f'Popped token number {self.token_num}')
        self.token_num += 1

        if self.token_num > 15:
            # Canceling (stopping) timer
            self.timer.cancel()

        return None