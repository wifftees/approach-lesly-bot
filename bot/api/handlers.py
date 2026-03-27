from aiohttp import web

from bot.db import get_client
from bot.services import entity_type as et_service
from bot.services import activity as activity_service
from bot.services import entry as entry_service


async def get_entity_types(request: web.Request) -> web.Response:
    entity_types = et_service.get_all()
    data = [
        {"id": et.id, "slug": et.slug, "display_name": et.display_name, "points": et.points}
        for et in entity_types
    ]
    return web.json_response(data)


async def get_stats(request: web.Request) -> web.Response:
    client = get_client()

    users_response = await (
        client.table("users")
        .select("user_id, username, first_name")
        .order("user_id")
        .execute()
    )
    users = [
        {"user_id": r["user_id"], "username": r["username"], "first_name": r["first_name"]}
        for r in users_response.data
    ]

    entries_response = await (
        client.table("entries")
        .select("user_id, entity_type_id, entity_types(slug, points)")
        .execute()
    )

    stats_map: dict[tuple[int, str], dict] = {}
    for r in entries_response.data:
        et_data = r["entity_types"]
        key = (r["user_id"], et_data["slug"])
        if key not in stats_map:
            stats_map[key] = {
                "user_id": r["user_id"],
                "entity_type_slug": et_data["slug"],
                "count": 0,
                "points": 0,
                "points_per": et_data["points"],
            }
        stats_map[key]["count"] += 1
        stats_map[key]["points"] += et_data["points"]

    stats = [
        {"user_id": v["user_id"], "entity_type_slug": v["entity_type_slug"], "count": v["count"], "points": v["points"]}
        for v in stats_map.values()
    ]

    entity_types = et_service.get_all()
    et_data = [{"slug": et.slug, "display_name": et.display_name, "points": et.points} for et in entity_types]

    return web.json_response({"users": users, "stats": stats, "entity_types": et_data})


async def get_contacts(request: web.Request) -> web.Response:
    user_id_str = request.query.get("user_id")
    entity_type_slug = request.query.get("entity_type_slug")

    if not user_id_str or not entity_type_slug:
        return web.json_response({"error": "user_id and entity_type_slug required"}, status=400)

    user_id = int(user_id_str)
    et = et_service.get_by_slug(entity_type_slug)
    if not et:
        return web.json_response({"error": "unknown entity_type_slug"}, status=400)

    contacts = await entry_service.get_contacts(user_id, et.id)

    client = get_client()
    user_response = await (
        client.table("users")
        .select("username, first_name")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    user_info = {"username": user_response.data["username"], "first_name": user_response.data["first_name"]} if user_response.data else {}

    return web.json_response({
        "contacts": contacts,
        "user": user_info,
        "entity_type": {"display_name": et.display_name},
    })


async def send_contacts(request: web.Request) -> web.Response:
    body = await request.json()
    target_user_id = body.get("target_user_id")
    entity_type_slug = body.get("entity_type_slug")

    if not target_user_id or not entity_type_slug:
        return web.json_response({"error": "target_user_id and entity_type_slug required"}, status=400)

    et = et_service.get_by_slug(entity_type_slug)
    if not et:
        return web.json_response({"error": "unknown entity_type_slug"}, status=400)

    contacts = await entry_service.get_contacts(int(target_user_id), et.id)
    requesting_user = request["telegram_user"]
    requesting_user_id = requesting_user["id"]

    bot = request.app["bot"]

    if not contacts or all(c is None for c in contacts):
        await bot.send_message(requesting_user_id, f"У пользователя нет контактов для «{et.display_name}»")
        return web.json_response({"ok": True, "message": "no_contacts"})

    client = get_client()
    target_response = await (
        client.table("users")
        .select("username, first_name")
        .eq("user_id", int(target_user_id))
        .maybe_single()
        .execute()
    )
    target_row = target_response.data
    target_name = target_row["first_name"] or target_row["username"] or str(target_user_id) if target_row else str(target_user_id)

    lines = [f"Контакты {target_name} — {et.display_name}:\n"]
    for i, c in enumerate(contacts, 1):
        lines.append(f"{i}. @{c}" if c else f"{i}. без контакта")

    await bot.send_message(requesting_user_id, "\n".join(lines))
    await activity_service.log_activity(
        requesting_user_id, "send_contacts",
        {"target_user_id": target_user_id, "entity_type_slug": entity_type_slug},
    )
    return web.json_response({"ok": True})
