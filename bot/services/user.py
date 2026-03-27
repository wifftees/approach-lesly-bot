from bot.db import get_client


async def upsert_user(user_id: int, username: str | None, first_name: str | None, last_name: str | None) -> None:
    client = get_client()
    await (
        client.table("users")
        .upsert(
            {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            },
            on_conflict="user_id",
        )
        .execute()
    )


async def get_user(user_id: int) -> dict | None:
    client = get_client()
    response = await (
        client.table("users")
        .select("*")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    return response.data
