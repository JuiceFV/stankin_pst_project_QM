from aiohttp import web
import asyncio
import jinja2
import aiohttp_jinja2
from . import settings
from .routes import setup_routes
from .database import Database
from .generators import TokenGenerator
from .queue import Queue
import platform

# Sets EventLoopPolicy for windows usage
# Without this loop policy aiopg.sa simply doesn't work
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def create_app(config:dict=None):
    app = web.Application()

    app['config'] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATES_DIR)
    )

    setup_routes(app)
    app['static_root_url'] = '/static'

    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)

    return app


async def on_start(app):
    config = app['config']
    app['db'] = Database()
    await app['db'].create_engine(config['dsn'])
    # Clearing the database queue
    await app['db'].delete({})
    app['sockets'] = list()
    app['token_gen'] = TokenGenerator()
    app['queue'] = Queue(app)


async def on_shutdown(app):
    await app['db'].close()
