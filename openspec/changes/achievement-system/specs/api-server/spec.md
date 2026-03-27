## ADDED Requirements

### Requirement: Achievements API endpoint
The API server SHALL expose a `GET /api/achievements` endpoint that returns achievement definitions, user progress, and the users list. The endpoint SHALL accept an optional `user_id` query parameter.

#### Scenario: Fetch achievements for specific user
- **WHEN** `GET /api/achievements?user_id=123` is called
- **THEN** the response SHALL contain all achievement definitions, the list of achievement IDs unlocked by user 123, and the full users list

#### Scenario: Fetch achievements for requesting user
- **WHEN** `GET /api/achievements` is called without a `user_id` parameter
- **THEN** the response SHALL use the authenticated Telegram user's ID from initData and return their achievement progress

#### Scenario: Response format
- **WHEN** the endpoint returns successfully
- **THEN** the JSON response SHALL have the structure: `{"achievements": [...], "user_achievements": [<achievement_ids>], "users": [...]}`

### Requirement: Achievements endpoint authentication
The achievements endpoint SHALL be protected by the same Telegram initData HMAC authentication middleware as all other API endpoints.

#### Scenario: Unauthenticated request rejected
- **WHEN** a request to `/api/achievements` lacks valid `X-Telegram-Init-Data` header
- **THEN** the server SHALL return HTTP 401
