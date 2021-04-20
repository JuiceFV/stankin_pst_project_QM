from aiohttp import web
import asyncpgsa
import jinja2
import aiohttp_jinja2
from . import settings
from .routes import setup_routes
from .token_generator import TokenGenerator


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
    app['db'] = await asyncpgsa.create_pool(**config['dsn'])
    app['websockets'] = list()
    app['token_gen'] = TokenGenerator()


async def on_shutdown(app):
    await app['db'].close()