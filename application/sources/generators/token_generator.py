

class TokenGenerator:
    def __init__(self):
        self.cur_token = None
        self.tokens = list()

    def generate(self):
        if self.cur_token is None or self.cur_token == ['Z', '9', '9']:
            self.cur_token = ['A', '0', '0']
        elif self.cur_token[2] < '9':
            self.cur_token[2] = chr(ord(self.cur_token[2]) + 1)
        elif self.cur_token[1] < '9':
            self.cur_token[2] = '0'
            self.cur_token[1] = chr(ord(self.cur_token[1]) + 1)
        elif self.cur_token[0] < 'Z':
            self.cur_token[2] = self.cur_token[1] = '0'
            self.cur_token[0] = chr(ord(self.cur_token[0]) + 1)

        token = ''.join(self.cur_token)
        self.tokens.append(token)

        return token