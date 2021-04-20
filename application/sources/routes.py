from .views import frontend
from . import settings


def setup_routes(app):
    app.router.add_static('/static', 'sources/static', name='static')
    app.router.add_route('GET', '/', frontend.index)
    app.router.add_route('GET', '/ws/', frontend.ws_handler)