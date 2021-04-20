

class TokenGenerator:
    def __init__(self):
        self.token = None

    def generate(self):
        if self.token is None:
            self.token = ['A', '0', '0']
        elif self.token[2] < '9':
            self.token[2] = chr(ord(self.token[2]) + 1)
        elif self.token[1] < '9':
            self.token[2] = '0'
            self.token[1] = chr(ord(self.token[1]) + 1)
        elif self.token[0] < 'Z':
            self.token[2] = self.token[1] = '0'
            self.token[0] = chr(ord(self.token[0]) + 1)

        return ''.join(self.token)