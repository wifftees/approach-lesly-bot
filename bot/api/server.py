import pathlib

from aiohttp import web

from bot.api.routes import setup_routes

STATIC_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "miniapp" / "dist"


def create_app(bot) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    setup_routes(app)

    if STATIC_DIR.exists():
        async def serve_index(request):
            return web.FileResponse(STATIC_DIR / "index.html")

        app.router.add_get("/app", serve_index)
        app.router.add_get("/app/", serve_index)
        app.router.add_static("/app", STATIC_DIR)

    return app


async def start_server(app: web.Application, host: str, port: int) -> None:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
