from bot.db import get_client
from bot.models import EntityType

_cache: list[EntityType] = []
_by_command: dict[str, EntityType] = {}
_by_slug: dict[str, EntityType] = {}


async def load_entity_types() -> list[EntityType]:
    global _cache, _by_command, _by_slug
    client = get_client()
    response = await (
        client.table("entity_types")
        .select("*")
        .order("sort_order")
        .execute()
    )
    _cache = [EntityType(**r) for r in response.data]
    _by_command = {et.command: et for et in _cache}
    _by_slug = {et.slug: et for et in _cache}
    return _cache


def get_all() -> list[EntityType]:
    return _cache


def get_by_command(command: str) -> EntityType | None:
    return _by_command.get(command)


def get_by_slug(slug: str) -> EntityType | None:
    return _by_slug.get(slug)
