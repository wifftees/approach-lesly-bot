from aiohttp import web

from bot.api.handlers import get_achievements, get_contacts, get_entity_types, get_stats, send_contacts
from bot.api.middleware import telegram_auth_middleware


def setup_routes(app: web.Application) -> None:
    app.middlewares.append(telegram_auth_middleware)
    app.router.add_get("/api/entity-types", get_entity_types)
    app.router.add_get("/api/stats", get_stats)
    app.router.add_get("/api/contacts", get_contacts)
    app.router.add_get("/api/achievements", get_achievements)
    app.router.add_post("/api/send-contacts", send_contacts)
