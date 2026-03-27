## MODIFIED Requirements

### Requirement: Tab bar includes achievements
The Mini App tab bar SHALL include an "Ачивки" tab that renders the `AchievementsTab` component. The tab SHALL appear after entity type tabs in the tab order.

#### Scenario: Achievements tab appears in navigation
- **WHEN** the Mini App is loaded with entity types fetched
- **THEN** the tab bar SHALL show: "Общая", then one tab per entity type, then "🏆 Ачивки"

## ADDED Requirements

### Requirement: Achievement API client function
The API client module SHALL export a `fetchAchievements(userId?: number)` function that calls `GET /api/achievements` with optional `user_id` query parameter and returns typed achievement data.

#### Scenario: Fetching achievements with user ID
- **WHEN** `fetchAchievements(123)` is called
- **THEN** it SHALL make a GET request to `/api/achievements?user_id=123` with the Telegram initData header

#### Scenario: Fetching achievements without user ID
- **WHEN** `fetchAchievements()` is called
- **THEN** it SHALL make a GET request to `/api/achievements` without a user_id parameter

### Requirement: Achievement TypeScript types
The types module SHALL export `Achievement` and `AchievementsResponse` interfaces matching the API response schema.

#### Scenario: Types are importable
- **WHEN** a component imports from `types.ts`
- **THEN** `Achievement` and `AchievementsResponse` interfaces SHALL be available
