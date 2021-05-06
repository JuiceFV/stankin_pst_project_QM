from aiohttp_jinja2 import template


@template('test.html')
async def index(request):
    context = {}
    return context
