from supabase import create_async_client, AsyncClient

from bot.config import config

_client: AsyncClient | None = None


async def init_db() -> AsyncClient:
    global _client
    _client = await create_async_client(config.supabase_url, config.supabase_key)
    return _client


async def close_db() -> None:
    global _client
    _client = None


def get_client() -> AsyncClient:
    if _client is None:
        raise RuntimeError("supabase client is not initialized")
    return _client
