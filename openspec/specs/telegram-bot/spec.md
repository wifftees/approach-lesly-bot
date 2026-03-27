## ADDED Requirements

### Requirement: Start command provides full introduction
The system SHALL respond to /start with a welcome message in Russian that explains: available commands, how to add entries, how to view statistics, and the scoring system. The message SHALL include the ReplyKeyboard with all available commands.

#### Scenario: New user starts bot
- **WHEN** a new user sends /start
- **THEN** the bot creates the user in DB, sends a welcome message with full feature description in Russian, and displays the ReplyKeyboard

#### Scenario: Existing user sends /start
- **WHEN** an existing user sends /start
- **THEN** the bot sends the welcome message and refreshes the ReplyKeyboard

### Requirement: Help command shows available commands
The system SHALL respond to /help with a list of all available commands, their descriptions, and point values, generated dynamically from entity_types.

#### Scenario: User requests help
- **WHEN** a user sends /help
- **THEN** the bot responds with a formatted list showing each command, its entity display_name, and points value

### Requirement: Dynamic ReplyKeyboard generated from entity_types
The system SHALL display a persistent ReplyKeyboard containing slash commands for all entity_types (sorted by sort_order), plus /stats and /help. The keyboard SHALL be regenerated from entity_types data.

#### Scenario: Keyboard displays all commands
- **WHEN** a user receives any bot message
- **THEN** the ReplyKeyboard SHALL contain buttons for each entity_type command (e.g. "/add_girl", "/add_beautiful_girl"), plus "/stats" and "/help"

#### Scenario: New entity type added
- **WHEN** a new entity_type is added to the database and bot is restarted
- **THEN** the ReplyKeyboard SHALL include the new command button

### Requirement: Add entry FSM handles contact collection
The system SHALL implement a universal FSM (Finite State Machine) for adding entries that works for any entity_type. When a user sends an entity command, the bot SHALL ask for the contact @username with inline buttons.

#### Scenario: Add entry with optional contact - user provides contact
- **WHEN** a user sends a command for an entity_type with contact_required=false (e.g. /add_girl)
- **AND** the bot asks for contact with inline buttons [Пропустить] [Отмена]
- **AND** the user sends a @username text
- **THEN** the entry is saved with the contact_username, and the bot sends a congratulation message

#### Scenario: Add entry with optional contact - user skips
- **WHEN** a user sends a command for an entity_type with contact_required=false
- **AND** the user presses [Пропустить]
- **THEN** the entry is saved with contact_username=NULL, and the bot sends a congratulation message

#### Scenario: Add entry with required contact - user provides contact
- **WHEN** a user sends a command for an entity_type with contact_required=true (e.g. /add_beautiful_girl)
- **AND** the bot asks for contact with only inline button [Отмена] (no skip)
- **AND** the user sends a @username text
- **THEN** the entry is saved with the contact_username, and the bot sends an enhanced congratulation message

#### Scenario: Add entry with required contact - user tries to skip
- **WHEN** a user sends a command for an entity_type with contact_required=true
- **THEN** there SHALL be no [Пропустить] button, only [Отмена]

#### Scenario: User cancels entry
- **WHEN** a user presses [Отмена] during any add entry flow
- **THEN** no entry is saved, the bot confirms cancellation, and FSM state is cleared

### Requirement: Congratulation messages are randomized from DB
The system SHALL select a random congratulation message from the entity_type's congratulation_texts array and replace {points} with the actual point value.

#### Scenario: Girl added congratulation
- **WHEN** a girl entry is saved
- **THEN** the bot sends one of: "Красавчик! +2 очков 🔥", "Ещё одна в коллекции! +2 💪", "Машина! Продолжай! +2 🚀"

#### Scenario: Beautiful girl added congratulation
- **WHEN** a beautiful_girl entry is saved
- **THEN** the bot sends one of: "ЛЕГЕНДА! Красотка — это +6 очков! 🏆", "Ты МОНСТР! +6 за красотку! 💎", "Невероятно! Красотка в кармане — +6! 👑"

### Requirement: Stats command opens Mini App
The system SHALL respond to /stats with a message containing an inline button (WebAppInfo) that opens the Mini App.

#### Scenario: User views stats
- **WHEN** a user sends /stats
- **THEN** the bot sends a message "Открой статистику:" with an inline button labeled "Статистика 📊" that opens the Mini App URL

### Requirement: Activity logging for all bot interactions
The system SHALL log every user interaction to the activity_log table with appropriate action type and metadata.

#### Scenario: Command usage logged
- **WHEN** a user sends any command (/start, /help, /add_girl, /stats, etc.)
- **THEN** an activity_log entry is created with action='command' and metadata={"command": "<command_name>"}

#### Scenario: Entry creation logged
- **WHEN** a user successfully creates an entry
- **THEN** an activity_log entry is created with action='add_entry' and metadata={"entity_type_slug": "<slug>", "entry_id": <id>}
