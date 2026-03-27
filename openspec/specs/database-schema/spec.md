## ADDED Requirements

### Requirement: Users table stores Telegram user data
The system SHALL maintain a `users` table that stores Telegram user information. Each user SHALL be uniquely identified by their Telegram user_id (BIGINT primary key). The table SHALL store username, first_name, last_name, created_at, and last_active_at timestamps.

#### Scenario: New user registers via /start
- **WHEN** a Telegram user sends /start for the first time
- **THEN** the system creates a row in `users` with their telegram user_id, username, first_name, last_name, and current timestamp as created_at and last_active_at

#### Scenario: Existing user sends any command
- **WHEN** an already registered user sends any command
- **THEN** the system updates last_active_at to current timestamp

### Requirement: Entity types registry defines dynamic entities
The system SHALL maintain an `entity_types` table that serves as the single source of truth for all trackable entities. Each entity_type SHALL have: id (serial PK), slug (unique text), display_name (text), command (unique text, e.g. '/add_girl'), points (integer), contact_required (boolean), congratulation_texts (text array), sort_order (integer), created_at (timestamptz).

#### Scenario: Initial seed data
- **WHEN** the database is initialized
- **THEN** entity_types SHALL contain:
  - slug='girl', command='/add_girl', points=2, contact_required=false, display_name='Девочка', sort_order=1
  - slug='beautiful_girl', command='/add_beautiful_girl', points=6, contact_required=true, display_name='Красивая девочка', sort_order=2

#### Scenario: Adding a new entity type
- **WHEN** an admin INSERTs a new row into entity_types (e.g. slug='date', command='/add_date', points=10)
- **THEN** after bot restart, the new command, keyboard button, and Mini App tab SHALL appear automatically

### Requirement: Entries table stores all user records
The system SHALL maintain an `entries` table with: id (serial PK), user_id (FK to users), entity_type_id (FK to entity_types), contact_username (nullable text), created_at (timestamptz). Indexes SHALL exist on user_id and entity_type_id columns.

#### Scenario: Entry with contact
- **WHEN** a user adds a record and provides a contact username
- **THEN** the entry is stored with contact_username set to the provided value (without @ prefix)

#### Scenario: Entry without contact
- **WHEN** a user adds a record and skips the contact step
- **THEN** the entry is stored with contact_username as NULL

### Requirement: Activity log captures all user actions
The system SHALL maintain an `activity_log` table with: id (serial PK), user_id (FK to users), action (text), metadata (JSONB), created_at (timestamptz). Indexes SHALL exist on user_id and created_at columns.

#### Scenario: Command logged
- **WHEN** a user sends any command
- **THEN** the system inserts a row with action='command' and metadata containing the command name

#### Scenario: Entry addition logged
- **WHEN** a user successfully adds an entry
- **THEN** the system inserts a row with action='add_entry' and metadata containing entity_type_slug and entry_id
