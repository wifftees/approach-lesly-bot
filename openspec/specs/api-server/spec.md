## ADDED Requirements

### Requirement: Telegram initData validation on all endpoints
The system SHALL validate Telegram Mini App initData (HMAC-SHA256) on every API request via aiohttp middleware. The middleware SHALL extract user_id from validated initData and make it available to handlers.

#### Scenario: Valid initData
- **WHEN** a request includes a valid initData header/parameter
- **THEN** the request proceeds to the handler with extracted user_id

#### Scenario: Invalid or missing initData
- **WHEN** a request has invalid, expired, or missing initData
- **THEN** the system responds with HTTP 401 and JSON error message

### Requirement: GET /api/entity-types returns all entity types
The system SHALL provide an endpoint that returns all entity_types with their display names, slugs, and point values, sorted by sort_order.

#### Scenario: Fetch entity types
- **WHEN** a GET request is made to /api/entity-types
- **THEN** the response contains a JSON array of objects with fields: id, slug, display_name, points

### Requirement: GET /api/stats returns leaderboard data
The system SHALL provide an endpoint that returns aggregated statistics for all users across all entity types.

#### Scenario: Fetch full statistics
- **WHEN** a GET request is made to /api/stats
- **THEN** the response contains:
  - `users`: array of {user_id, username, first_name}
  - `stats`: array of {user_id, entity_type_slug, count, points} where points = count * entity_type.points
  - `entity_types`: array of entity type objects with points

#### Scenario: No data yet
- **WHEN** a GET request is made to /api/stats and no entries exist
- **THEN** the response contains empty stats array and users who have registered

### Requirement: GET /api/contacts returns user contacts for entity type
The system SHALL provide an endpoint that returns contact usernames for a specific user and entity type.

#### Scenario: Fetch contacts with data
- **WHEN** a GET request is made to /api/contacts?user_id=X&entity_type_slug=Y
- **THEN** the response contains:
  - `contacts`: array of contact_username strings (including nulls for skipped contacts)
  - `user`: {username, first_name}
  - `entity_type`: {display_name}

#### Scenario: Missing required parameters
- **WHEN** a GET request to /api/contacts is missing user_id or entity_type_slug
- **THEN** the system responds with HTTP 400 and error message

### Requirement: POST /api/send-contacts sends contacts via bot
The system SHALL provide an endpoint that triggers the bot to send a list of contacts to the requesting user's Telegram chat.

#### Scenario: Send contacts successfully
- **WHEN** a POST request is made to /api/send-contacts with body {"target_user_id": X, "entity_type_slug": Y}
- **AND** the requesting user (from initData) is valid
- **THEN** the bot sends a formatted message listing all contacts of user X for entity type Y to the requesting user's Telegram chat
- **AND** the response is HTTP 200 with {"ok": true}

#### Scenario: No contacts to send
- **WHEN** a POST request is made to /api/send-contacts but the target user has no contacts for the entity type
- **THEN** the bot sends a message saying there are no contacts
- **AND** the response is HTTP 200 with {"ok": true, "message": "no_contacts"}

#### Scenario: Activity logged
- **WHEN** a successful send-contacts request is made
- **THEN** an activity_log entry is created with action='send_contacts' and metadata containing target_user_id and entity_type_slug

### Requirement: Static file serving for Mini App
The system SHALL serve the built React Mini App static files (HTML, JS, CSS) from the /app path via aiohttp static routes.

#### Scenario: Mini App loaded
- **WHEN** a GET request is made to /app or /app/index.html
- **THEN** the system serves the React Mini App's index.html with correct content-type
