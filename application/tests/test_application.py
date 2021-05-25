from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from ..sources.app import create_app
from ..sources.settings import load_config
from ..sources.generators import TokenGenerator
from ..sources.database import Database
from ..sources.queue import Queue


# This class tests aiohttp application functions and methods
class TestApplication(AioHTTPTestCase):
    # Creating aiohttp application for tests
    async def get_application(self):
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_connection(self):
        """
        testing application connection
        """
        # Sending the basic request to the index-page
        response = await self.client.get('/')
        assert response.status == 200

    def test_application_config(self):
        """
        testing application default config
        """
        expected_config = {
            'dsn':
                {
                    'host': 'db',
                    'port': 5432,
                    'user': 'postgres',
                    'password': '1234',
                    'database': 'catsqms'
                }
        }
        assert expected_config == self.app['config']

    def test_application_defaults(self):
        """
        testing application default variables
        """
        expected_token_gen = TokenGenerator()
        expected_db = Database()
        expected_sockets = list()
        expected_queue = Queue(self.app)

        self.assertEqual(type(expected_token_gen), type(self.app['token_gen']))
        self.assertEqual(type(expected_db), type(self.app['db']))
        self.assertEqual(type(expected_sockets), type(self.app['sockets']))
        self.assertEqual(type(expected_queue), type(self.app['queue']))


    @unittest_run_loop
    async def test_index_content(self):
        """
        testing title text on index page
        """
        resp = await self.client.get('/')
        assert resp.status == 200
        result = await resp.text()
        assert '<title>Cats QMS</title>' in result