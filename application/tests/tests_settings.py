"""Tests responsible for 'load_config function which configure an application.
"""
import unittest
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import os
from application.sources.settings import load_config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSettingsCases(unittest.TestCase):
    """The class which tests load_config() from application/settings.
    """
    def test_load_config_without_arguments(self):
        """The first case when an user doesn't pass a configuration file as an argument.
        Therefore the configuration copies from application/config.yaml
        PASSED
        """
        expected = \
            {'dsn':
                 {
                     'database': 'catsqms',
                     'host': 'localhost',
                     'password': ' ',
                     'port': '5432',
                     'user': 'postgres'
                 }
            }
        res = load_config()
        self.assertEqual(expected, res)

    def test_load_config_with_custom_file(self):
        """A new config file updates the config.yaml (doesn't rewrite).
        Therefore it copies a data from config.yaml (rewrites if needed) and append a new data if it exists.
        FAILED
        Description: The problem appears in the dict of a dict. dict.update() add up missing values and
        replace already existing values. Due to 'dsn' exists as default value, it's gonna be replaced by another dict.
        """

        expected = \
            {
                'dsn':
                {
                    'database': 'catsqms',
                    'host': 'localhost',
                    'password': '12345qwerty',
                    'port': None,
                    'user': 'postgres'
                },
                # This is a new data which will be added to a basic configuration' data
                'option1': 'Name',
                'option2': 12345,
                'option3': 'https://rt.pornhub.com/',
                'option3_proponent': 'https://rt.pornhub.com/view_video.php?viewkey=ph5e85e9ec3f3b3'
            }

        path_to_custom_cfg = os.path.join(THIS_DIR, 'custom_cfg.yaml')
        with open(path_to_custom_cfg, 'r') as f:
            res = load_config(config_file=f)
            self.assertEqual(res, expected)
