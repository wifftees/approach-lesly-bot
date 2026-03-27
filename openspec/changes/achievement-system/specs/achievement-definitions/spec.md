## ADDED Requirements

### Requirement: Achievement milestones stored in database
The system SHALL store achievement definitions in an `achievements` table with fields: id, entity_type_id, name, emoji, threshold, and sort_order. Each achievement SHALL be linked to exactly one entity type via foreign key.

#### Scenario: Achievement table contains correct seed data for girl entity type
- **WHEN** the migration is applied
- **THEN** the `achievements` table SHALL contain 5 rows for the "girl" entity type with thresholds 1, 5, 10, 25, 50 and names "Первый шаг", "Разгон", "Десятка", "Мастер", "Легенда" respectively

#### Scenario: Achievement table contains correct seed data for beautiful_girl entity type
- **WHEN** the migration is applied
- **THEN** the `achievements` table SHALL contain 5 rows for the "beautiful_girl" entity type with thresholds 1, 3, 5, 10, 25 and names "Ценитель", "Коллекционер", "Знаток", "Эксперт", "Легенда красоты" respectively

### Requirement: User achievement progress stored in database
The system SHALL store granted achievements in a `user_achievements` table with fields: id, user_id, achievement_id, achieved_at. The table SHALL enforce a UNIQUE constraint on (user_id, achievement_id) to prevent duplicate grants.

#### Scenario: Duplicate achievement grant is prevented
- **WHEN** an INSERT into `user_achievements` is attempted with a (user_id, achievement_id) pair that already exists
- **THEN** the insert SHALL be silently ignored (no error, no duplicate row)

### Requirement: Achievement definitions cached at startup
The system SHALL load all achievement definitions from the database at startup and cache them in memory, following the same pattern as `entity_type` caching in `bot/services/entity_type.py`.

#### Scenario: Achievements are available without DB query after startup
- **WHEN** the application starts and achievement cache is initialized
- **THEN** subsequent calls to get achievement definitions SHALL return from memory without database queries
