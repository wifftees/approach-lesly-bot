from bot.db import get_client
from bot.models import Achievement

_cache: list[Achievement] = []
_by_entity_type: dict[int, list[Achievement]] = {}


async def load_achievements() -> list[Achievement]:
    global _cache, _by_entity_type
    client = get_client()
    response = await (
        client.table("achievements")
        .select("*")
        .order("entity_type_id")
        .order("sort_order")
        .execute()
    )
    _cache = [Achievement(**r) for r in response.data]
    _by_entity_type = {}
    for a in _cache:
        _by_entity_type.setdefault(a.entity_type_id, []).append(a)
    return _cache


def get_all() -> list[Achievement]:
    return _cache


def get_by_entity_type(entity_type_id: int) -> list[Achievement]:
    return _by_entity_type.get(entity_type_id, [])


async def get_user_achievement_ids(user_id: int) -> list[int]:
    client = get_client()
    response = await (
        client.table("user_achievements")
        .select("achievement_id")
        .eq("user_id", user_id)
        .execute()
    )
    return [r["achievement_id"] for r in response.data]


async def check_and_grant(user_id: int, entity_type_id: int, count: int) -> list[Achievement]:
    achievements = get_by_entity_type(entity_type_id)
    if not achievements:
        return []

    eligible = [a for a in achievements if count >= a.threshold]
    if not eligible:
        return []

    existing = set(await get_user_achievement_ids(user_id))
    to_grant = [a for a in eligible if a.id not in existing]
    if not to_grant:
        return []

    client = get_client()
    await (
        client.table("user_achievements")
        .upsert(
            [{"user_id": user_id, "achievement_id": a.id} for a in to_grant],
            on_conflict="user_id,achievement_id",
            ignore_duplicates=True,
        )
        .execute()
    )
    return to_grant
