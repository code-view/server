from aiohttp import web
from .main import app

if __name__ == '__main__':
    web.run_app(app)
