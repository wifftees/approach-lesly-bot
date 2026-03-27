## Why

Users lack motivation to continue adding entries after the initial novelty wears off. A gamification layer with achievements creates milestone-based goals that drive engagement, reward consistency, and add social competition through visible progress trees.

## What Changes

- New `achievements` and `user_achievements` database tables to define milestones and track user progress
- Achievement check logic triggered after every new entry creation
- Telegram bot sends a congratulation message when a user unlocks a new achievement
- New REST API endpoint to fetch achievement definitions and user progress
- New "Ачивки" (Achievements) tab in the Mini App with:
  - Two horizontal progress-chain trees (one per entity type: girl, beautiful_girl)
  - Green nodes for unlocked achievements, gray for locked
  - Dropdown to view other users' achievement trees
  - Default view shows current user's achievements

### Achievement Trees

**Girl tree** (thresholds: 1, 5, 10, 25, 50):

| Threshold | Name | Emoji |
|-----------|------|-------|
| 1 | Первый шаг | 👋 |
| 5 | Разгон | 🔥 |
| 10 | Десятка | ⭐ |
| 25 | Мастер | 💪 |
| 50 | Легенда | 👑 |

**Beautiful girl tree** (thresholds: 1, 3, 5, 10, 25):

| Threshold | Name | Emoji |
|-----------|------|-------|
| 1 | Ценитель | 💎 |
| 3 | Коллекционер | 🌟 |
| 5 | Знаток | 🏆 |
| 10 | Эксперт | 💫 |
| 25 | Легенда красоты | 👑 |

## Capabilities

### New Capabilities
- `achievement-definitions`: Database schema and seed data for achievement milestones per entity type
- `achievement-tracking`: Backend logic to check and grant achievements after entry creation, plus Telegram notifications
- `achievement-ui`: Mini App tab displaying achievement progress trees with user selection dropdown

### Modified Capabilities
- `telegram-bot`: Entry creation handlers gain achievement check hook after recording an entry
- `api-server`: New `/api/achievements` endpoint added to the REST API
- `mini-app`: New "Ачивки" tab added to the tab bar, new component and API client function

## Impact

- **Database**: Two new tables (`achievements`, `user_achievements`), new migration file
- **Backend**: New `bot/services/achievement.py` service, modifications to `bot/handlers/add_entry.py`, new API handler and route
- **Frontend**: New `AchievementsTab.tsx` component, new types and API client function, `App.tsx` tab addition
- **API**: New `GET /api/achievements?user_id=<optional>` endpoint
- **Dependencies**: No new external dependencies required
