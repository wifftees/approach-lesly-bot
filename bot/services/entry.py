from bot.db import get_client


async def create_entry(user_id: int, entity_type_id: int, contact_username: str | None = None) -> int:
    client = get_client()
    response = await (
        client.table("entries")
        .insert(
            {
                "user_id": user_id,
                "entity_type_id": entity_type_id,
                "contact_username": contact_username,
            }
        )
        .execute()
    )
    return response.data[0]["id"]


async def get_entries_count(user_id: int, entity_type_id: int) -> int:
    client = get_client()
    response = await (
        client.table("entries")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .eq("entity_type_id", entity_type_id)
        .execute()
    )
    return response.count or 0


async def get_contacts(user_id: int, entity_type_id: int) -> list[str | None]:
    client = get_client()
    response = await (
        client.table("entries")
        .select("contact_username")
        .eq("user_id", user_id)
        .eq("entity_type_id", entity_type_id)
        .order("created_at")
        .execute()
    )
    return [r["contact_username"] for r in response.data]
