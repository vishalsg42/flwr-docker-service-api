import asyncio
import aiohttp_cors
from aiohttp import web
from routes.server import server_endpoint, server_compose_endpoint
from routes.client import client_endpoint, client_compose_endpoint
from aiohttp_swagger import setup_swagger

PORT = 8090
async def init_app():
    app = web.Application()
    version = '/v1'
    app.router.add_post(f'{version}/server', server_endpoint)
    app.router.add_post(f'{version}/client', client_endpoint)
    app.router.add_post(f'{version}/server-compose', server_compose_endpoint)
    app.router.add_post(f'{version}/client-compose', client_compose_endpoint)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Enable CORS on all routes
    for route in list(app.router.routes()):
        cors.add(route)


    # Setup Swagger
    setup_swagger(app, swagger_from_file="swagger.yml",
                  swagger_url="/api/doc", ui_version=3)
    return app

if __name__ == '__main__':
    app = asyncio.run(init_app())
    web.run_app(app, port=PORT)
