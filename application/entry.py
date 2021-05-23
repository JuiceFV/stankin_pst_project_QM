import argparse
from aiohttp import web
import asyncio
from sources import create_app
from sources.settings import load_config
from tests import start_tests


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Library uvloop is not available")

parser = argparse.ArgumentParser(description='CatsQMS')
parser.add_argument('--host', help='Host to listen', default='127.0.0.1')
parser.add_argument('--port', help='Port to accept connections', default='5000')
parser.add_argument('-r', '--reload', action='store_true', help='Autoreload code on change')
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help='Path to configuration file')
parser.add_argument('-t', '--tests', action='store_true', help='Start application unit tests')

if __name__ == '__main__':
    args = parser.parse_args()

    if not args.tests:
        app = create_app(config=load_config(args.config))
        web.run_app(app, host=args.host, port=args.port)
    else:
        start_tests()