## Context

The system currently tracks user entries (approaches) per entity type and displays leaderboards in a Telegram Mini App. There is no gamification beyond point accumulation. Users have no milestone-based goals, which limits long-term engagement.

Current data flow: User sends `/add_girl` → FSM collects contact → `entry_service.create_entry()` → congratulation message. The Mini App fetches stats via `/api/stats` and displays leaderboards.

## Goals / Non-Goals

**Goals:**
- Add achievement milestone system with per-entity-type progress trees
- Notify users in real-time (via Telegram message) when achievements unlock
- Display achievement progress in Mini App with ability to view other users
- Keep achievements data-driven (stored in DB, not hardcoded in code)

**Non-Goals:**
- Achievement rewards beyond notification messages (no points bonus, no badges)
- Admin interface for managing achievements
- Achievement categories beyond entry count (no streaks, no time-based)
- Push notifications or scheduled reminders about uncompleted achievements

## Decisions

### 1. Achievement definitions in database vs code constants

**Decision**: Store in `achievements` table, load and cache at startup (same pattern as `entity_types`).

**Rationale**: Follows existing project convention. Entity types use the same pattern — DB-stored, cached in memory via service module. This allows adding new achievements via migration without code changes.

**Alternative considered**: Python constants/enum — simpler but breaks the project's data-driven pattern and requires deploys for changes.

### 2. Achievement check timing — synchronous in handler vs async background job

**Decision**: Check synchronously in `add_entry` handlers, immediately after `create_entry()`.

**Rationale**: The check is lightweight (compare count against cached thresholds, one DB insert for grant). No background job infrastructure exists in the project. Adding celery/arq would be overengineering for a simple comparison operation.

**Alternative considered**: Background task queue — unnecessary complexity for O(1) threshold comparison.

### 3. Single API endpoint vs separate endpoints for definitions and progress

**Decision**: Single `GET /api/achievements?user_id=<optional>` returning both definitions and user progress.

**Rationale**: The Mini App always needs both (definitions to render the tree, progress to color nodes). Single request reduces latency. The users list is already available from `/api/stats` but we include it here too to keep the tab self-contained.

**Alternative considered**: Separate `/api/achievement-definitions` + `/api/user-achievements` — more RESTful but doubles network requests for no practical benefit.

### 4. Frontend tree visualization — custom CSS vs chart library

**Decision**: Custom CSS with Mantine components (flexbox chain with connecting lines).

**Rationale**: The "progress chain" is too simple for a tree/graph library. Five nodes connected by lines is straightforward with CSS flexbox. Mantine's `Paper`, `Badge`, and `Group` components provide the building blocks. Adding a graph library (e.g., react-flow) would be massive overkill.

### 5. User dropdown — fetch users from achievements endpoint vs reuse stats

**Decision**: Include users list in the achievements API response.

**Rationale**: Keeps the Achievements tab independent from other tabs. No cross-tab state management needed. The users list is small (typically <50 users).

## Risks / Trade-offs

**[Race condition on concurrent entries]** → Mitigated by `UNIQUE(user_id, achievement_id)` constraint. If two entries are processed simultaneously and both trigger the same achievement, the second INSERT will be a no-op (ON CONFLICT DO NOTHING). Only the first grants the achievement.

**[Achievement cache staleness after adding new achievements]** → Acceptable risk. New achievements require a migration + restart. Same trade-off as entity_types. For a small-scale bot this is fine.

**[N+1 query on achievement check]** → Not a real risk. The check reads from in-memory cache (thresholds) and does one `get_entries_count()` query (already exists) plus one INSERT. Total: 2 queries per entry, regardless of achievement count.

**[Mini App bundle size increase]** → Minimal. One new component (~150 lines), no new dependencies. Negligible impact.

## Architecture

```
User adds entry via Telegram
        │
        ▼
add_entry handler
        │
        ├── entry_service.create_entry()
        ├── entry_service.get_entries_count()
        ├── achievement_service.check_and_grant(user_id, entity_type_id, count)
        │       ├── Compare count against cached thresholds
        │       ├── INSERT into user_achievements (ON CONFLICT DO NOTHING)
        │       └── Return list of newly granted achievements
        └── Send achievement message(s) via bot.send_message()

Mini App "Ачивки" tab
        │
        ├── GET /api/achievements?user_id=X
        │       ├── All achievement definitions (from cache)
        │       ├── User's granted achievement IDs (from user_achievements)
        │       └── All users list (for dropdown)
        └── Render two progress chains (girl / beautiful_girl)
```

## Database Schema

```sql
achievements (
    id SERIAL PRIMARY KEY,
    entity_type_id INTEGER NOT NULL REFERENCES entity_types(id),
    name TEXT NOT NULL,
    emoji TEXT NOT NULL,
    threshold INTEGER NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
)

user_achievements (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    achievement_id INTEGER NOT NULL REFERENCES achievements(id),
    achieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
)
```

## API Endpoint

```
GET /api/achievements?user_id=<optional>
Response: {
    "achievements": [
        {"id": 1, "entity_type_slug": "girl", "name": "Первый шаг", "emoji": "👋", "threshold": 1, "sort_order": 1},
        ...
    ],
    "user_achievements": [1, 3, 6],  // achievement IDs
    "users": [
        {"user_id": 123, "username": "john", "first_name": "John"},
        ...
    ]
}
```

## Migration Plan

1. Run `migrations/002_achievements.sql` on Supabase (creates tables + seeds data)
2. Deploy updated backend (new service, modified handlers, new API route)
3. Build and deploy updated Mini App
4. No rollback concerns — new tables are additive, handler changes are backward-compatible
