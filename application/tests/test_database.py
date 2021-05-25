from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from ..sources.app import create_app
from ..sources.settings import load_config
from ..sources.generators import TokenGenerator


class TestDatabase(AioHTTPTestCase):
    # Creating aiohttp application for tests
    async def get_application(self):
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_database(self):
        """
        testing database by inserting one row and selecting it
        """
        expected = {'token': 'A00', 'ip': '255.255.255.255'}

        await self.app['db'].insert(expected)
        result = await self.app['db'].get_first_row()

        assert expected['token'] == result['token']
        assert expected['ip'] == result['ip']

    @unittest_run_loop
    async def test_database_empty(self):
        """
        testing selecting row from empty database
        """
        expected = None

        result = await self.app['db'].get_first_row()

        assert expected == result

    @unittest_run_loop
    async def test_select_multiple_rows(self):
        """
        testing multiple rows selection from database
        """
        token_gen = TokenGenerator()
        expected_len = 10

        for i in range(expected_len):
            token = token_gen.generate()
            await self.app['db'].insert({'token': token, 'ip': 'null'})

        result = await self.app['db'].select({})

        assert expected_len == len(result)

    @unittest_run_loop
    async def test_database_get_tokens(self):
        """
        testing selecting only tokens from database
        """
        expected_tokens = ['A00', 'A99', 'Z99']
        rows = [
            {'token': expected_tokens[0], 'ip': '255.255.255.255'},
            {'token': expected_tokens[1], 'ip': '127.0.0.1'},
            {'token': expected_tokens[2], 'ip': '0.0.0.0'}
        ]

        for row in rows:
            await self.app['db'].insert(row)

        result = await self.app['db'].get_tokens()
        for i, token in enumerate(result):
            assert expected_tokens[i] == token

    @unittest_run_loop
    async def test_database_get_ip(self):
        """
        testing selecting only ip addresses from database
        """
        expected_ip = ['255.255.255.255', '127.0.0.1', '0.0.0.0']
        rows = [
            {'token': 'A00', 'ip': expected_ip[0]},
            {'token': 'A99', 'ip': expected_ip[1]},
            {'token': 'Z99', 'ip': expected_ip[2]}
        ]

        for row in rows:
            await self.app['db'].insert(row)

        result = await self.app['db'].get_ip_addresses()
        for i, ip in enumerate(result):
            assert expected_ip[i] == ip

    @unittest_run_loop
    async def test_database_delete(self):
        """
        testing deleting row from database
        """
        expected = None

        await self.app['db'].insert({'token': 'A00', 'ip': '255.255.255.255'})
        await self.app['db'].delete({'token': 'A00'})
        result = await self.app['db'].get_first_row()

        assert expected == result