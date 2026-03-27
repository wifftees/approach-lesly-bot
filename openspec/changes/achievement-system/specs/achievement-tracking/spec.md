## ADDED Requirements

### Requirement: Achievement check after entry creation
The system SHALL check for newly unlocked achievements immediately after every successful entry creation. The check SHALL compare the user's current entry count for the entity type against all achievement thresholds for that entity type.

#### Scenario: User reaches an achievement threshold
- **WHEN** a user creates an entry and their total count for that entity type equals or exceeds an achievement threshold they have not yet unlocked
- **THEN** the system SHALL insert a row into `user_achievements` and return the achievement as newly granted

#### Scenario: User already has the achievement
- **WHEN** a user creates an entry and their count exceeds a threshold for an achievement they already have
- **THEN** the system SHALL NOT attempt to re-grant the achievement

#### Scenario: User count does not reach any new threshold
- **WHEN** a user creates an entry but their count does not meet any un-granted achievement threshold
- **THEN** the system SHALL return an empty list of newly granted achievements

### Requirement: Telegram notification on achievement unlock
The system SHALL send a Telegram message to the user for each newly unlocked achievement immediately after granting it. The message SHALL include the achievement emoji and name.

#### Scenario: Single achievement unlocked
- **WHEN** one new achievement is granted after entry creation
- **THEN** the bot SHALL send a message like "🏆 Ачивка разблокирована: 👋 Первый шаг!"

#### Scenario: Multiple achievements unlocked simultaneously
- **WHEN** multiple achievements are granted after a single entry (e.g., user's first entry unlocks threshold 1)
- **THEN** the bot SHALL send one message per unlocked achievement
