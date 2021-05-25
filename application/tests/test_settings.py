import os
import unittest
from ..sources.settings import load_config


DIR = os.path.dirname(os.path.abspath(__file__))

# This class tests config loading
class TestSettings(unittest.TestCase):
    def test_default_config(self):
        """
        testing loading default config for application
        """
        expected = {
            'dsn': {
                'host': 'db',
                'port': 5432,
                'user': 'postgres',
                'password': '1234',
                'database': 'catsqms'
            }
        }
        result = load_config()
        assert expected == result

    def test_custom_config(self):
        """
        testing loading custom config for application
        """

        expected = {
            'dsn': {
                'host': 'new_host',
                'port': 3333,
                'user': 'not_postgres',
                'password': 'other_pass',
                'database': 'some_db'
            },
            'setting1': 'First',
            'setting2': 11111,
            'some_url': 'https://google.com/',
            'dict': {
                'host': 'google.com',
                'port': 8080,
                'user': 'local',
                'password': 'pass',
                'database': 'catsqms'
            }
        }

        path = os.path.join(DIR, 'custom_cfg.yaml')
        with open(path, 'r') as file:
            result = load_config(config_file=file)

        assert expected == result