## 1. Database

- [x] 1.1 Create `migrations/002_achievements.sql` with `achievements` and `user_achievements` tables, indexes, and seed data for all 10 achievements (5 girl + 5 beautiful_girl)

## 2. Backend Models

- [x] 2.1 Add `Achievement` and `UserAchievement` Pydantic models to `bot/models.py`

## 3. Backend Achievement Service

- [x] 3.1 Create `bot/services/achievement.py` with cache initialization (`load_achievements`, `get_all`, `get_by_entity_type`) following the `entity_type.py` caching pattern
- [x] 3.2 Add `get_user_achievement_ids(user_id)` function that queries `user_achievements` and returns a list of achievement IDs
- [x] 3.3 Add `check_and_grant(user_id, entity_type_id, count)` function that compares count against cached thresholds, inserts new grants with ON CONFLICT DO NOTHING, and returns list of newly granted `Achievement` objects
- [x] 3.4 Call `achievement.load_achievements()` in `bot/main.py` startup alongside existing `entity_type.load_entity_types()`

## 4. Bot Handler Integration

- [x] 4.1 Modify `on_skip_contact` in `bot/handlers/add_entry.py` to call `get_entries_count` then `check_and_grant` after entry creation, and send achievement notification messages
- [x] 4.2 Modify `on_contact_input` in `bot/handlers/add_entry.py` with the same achievement check and notification logic

## 5. API Endpoint

- [x] 5.1 Add `get_achievements` handler in `bot/api/handlers.py` that returns achievement definitions (from cache), user achievement IDs (from DB), and users list
- [x] 5.2 Add `GET /api/achievements` route in `bot/api/routes.py`

## 6. Frontend Types and API Client

- [x] 6.1 Add `Achievement` and `AchievementsResponse` interfaces to `miniapp/src/types.ts`
- [x] 6.2 Add `fetchAchievements(userId?: number)` function to `miniapp/src/api/client.ts`

## 7. Frontend Achievements Tab

- [x] 7.1 Create `miniapp/src/components/AchievementsTab.tsx` with user dropdown, two progress-chain trees (girl + beautiful_girl), green/gray node styling
- [x] 7.2 Add "🏆 Ачивки" tab to `miniapp/src/App.tsx` tab bar after entity type tabs

## 8. Build Verification

- [x] 8.1 Run `npm run build` in miniapp directory and verify no TypeScript errors
