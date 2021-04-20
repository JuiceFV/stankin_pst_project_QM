from aiohttp import web
from aiohttp_jinja2 import template
from sqlalchemy import select
from .. import db


@template('index.html')
async def index(request):
    context = {'some_text': 'First setup'}
    return context


@template('test.html')
async def test(request):
    async with request.app['db'].acquire() as conn:
        query = select([db.tokens.c.id, db.tokens.c.ip, db.tokens.c.token])
        result = await conn.fetchrow(query)
        context = {'row': result}

    return context