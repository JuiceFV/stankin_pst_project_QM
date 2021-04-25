from .views import index
from .websocket import ws_handler
from .settings import STATIC_DIR


def setup_routes(app):
    app.router.add_static('/static', STATIC_DIR, name='static')
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/ws/', ws_handler)