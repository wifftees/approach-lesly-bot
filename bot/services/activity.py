from bot.db import get_client


async def log_activity(user_id: int, action: str, metadata: dict | None = None) -> None:
    client = get_client()
    await (
        client.table("activity_log")
        .insert({"user_id": user_id, "action": action, "metadata": metadata or {}})
        .execute()
    )
