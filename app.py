import asyncio
from aiohttp import web
from routes.server import server_endpoint
from routes.client import client_endpoint

async def init_app():
    app = web.Application()
    version = '/v1'
    app.router.add_post(f'{version}/server', server_endpoint)
    app.router.add_post(f'{version}/client', client_endpoint)
    return app

if __name__ == '__main__':
    app = asyncio.run(init_app())
    web.run_app(app, port=8090)
