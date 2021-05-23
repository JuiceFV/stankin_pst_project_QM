from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from ..sources.app import create_app
from ..sources.settings import load_config


# This class tests aiohttp application functions and methods
class TestTokeGenerator(AioHTTPTestCase):
    # Creating aiohttp application for tests
    async def get_application(self):
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_generator(self):
        """
        testing getting first token in queue
        """
        assert 'A00' == self.app['token_gen'].generate()
        assert 'A01' == self.app['token_gen'].generate()
        assert 'A02' == self.app['token_gen'].generate()

    @unittest_run_loop
    async def test_token_decade_number(self):
        """
        testing the decade number of token (A10, A20, A30, ...)
        """

        result = []
        result.append(self.app['token_gen'].generate())
        for i in range(3):
            for _ in range(9):
                self.app['token_gen'].generate()

            result.append(self.app['token_gen'].generate())

        assert 'A00' == result[0]
        assert 'A10' == result[1]
        assert 'A20' == result[2]
        assert 'A30' == result[3]

    @unittest_run_loop
    async def test_token_char(self):
        """
        testing the char of token (A00, B00, C00, ...)
        """

        result = []
        result.append(self.app['token_gen'].generate())
        for i in range(3):
            for _ in range(99):
                self.app['token_gen'].generate()

            result.append(self.app['token_gen'].generate())

        assert 'A00' == result[0]
        assert 'B00' == result[1]
        assert 'C00' == result[2]
        assert 'D00' == result[3]

    @unittest_run_loop
    async def test_generator_multiple(self):
        """
        testing multiple tokens getting
        """
        expected_tokens = ['A00', 'A01', 'A02', 'A03', 'A04', 'A05']

        result = []
        for _ in range(6):
            result.append(self.app['token_gen'].generate())

        assert expected_tokens == result

    @unittest_run_loop
    async def test_generator_overflow(self):
        """
        testing generator overflow by getting token when the queue is full (current token Z99)
        """
        expected_token = 'A00'
        self.app['token_gen'].cur_token = ['Z', '9', '9']

        assert expected_token == self.app['token_gen'].generate()