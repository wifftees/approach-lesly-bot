## ADDED Requirements

### Requirement: Dynamic tabs generated from entity types
The Mini App SHALL display tabs generated dynamically from the /api/entity-types response. The first tab SHALL always be "Общая" (overall). Subsequent tabs SHALL correspond to each entity_type by display_name.

#### Scenario: Two entity types configured
- **WHEN** the Mini App loads and /api/entity-types returns girl and beautiful_girl
- **THEN** three tabs are displayed: "Общая", "Девочка", "Красивая девочка"

#### Scenario: New entity type added
- **WHEN** a new entity_type is added and the user refreshes
- **THEN** a new tab appears for the added entity type

### Requirement: Overall tab shows total points leaderboard
The "Общая" tab SHALL display a bar chart where each bar represents a user. Bar height equals the sum of (count * points) across all entity types. Bars SHALL be sorted in descending order by total points. Each bar SHALL display the total points value on top. User Telegram username SHALL be displayed below each bar.

#### Scenario: Multiple users with data
- **WHEN** the Overall tab is active and users have entries
- **THEN** a bar chart displays users sorted by total points descending, with point values on top of each bar

#### Scenario: No data
- **WHEN** the Overall tab is active and no entries exist
- **THEN** an empty state message is displayed

### Requirement: Entity tab shows entity-specific leaderboard
Each entity tab SHALL display a bar chart where bar height equals count * points for that entity type. Bars SHALL be sorted by descending points. The label on top of each bar SHALL show "N pts (K шт)" where N is the points and K is the count.

#### Scenario: Entity tab with data
- **WHEN** a user opens the "Девочка" tab
- **THEN** a bar chart shows users sorted by girl points descending, labels show "10 pts (5 шт)"

### Requirement: Entity tab supports contact viewing
Each entity tab SHALL include a dropdown to select a user and a "Показать контакты" button. When clicked, the contacts for the selected user and entity type SHALL be loaded and displayed as a list.

#### Scenario: View contacts
- **WHEN** a user selects another user from the dropdown and clicks "Показать контакты"
- **THEN** the system fetches contacts from /api/contacts and displays them as a list of @usernames (NULL contacts shown as "без контакта")

### Requirement: Entity tab supports sending contacts via bot
Each entity tab SHALL include a "Отправить контакты" button. When clicked, it SHALL trigger the bot to send the selected user's contacts to the current user's Telegram chat.

#### Scenario: Send contacts
- **WHEN** a user selects a target user and clicks "Отправить контакты"
- **THEN** a POST request is made to /api/send-contacts and a success notification is shown in the Mini App

#### Scenario: Send contacts confirmation
- **WHEN** the send-contacts request succeeds
- **THEN** the Mini App shows a toast/notification "Контакты отправлены в чат!"

### Requirement: Refresh button reloads all data
The Mini App SHALL have a refresh button that reloads statistics from the API.

#### Scenario: User refreshes data
- **WHEN** a user clicks the refresh button
- **THEN** all tabs data is re-fetched from /api/stats and charts are updated

### Requirement: Telegram theme integration
The Mini App SHALL adapt to the Telegram client's theme (light/dark) using Telegram.WebApp.themeParams for colors and styling.

#### Scenario: Dark mode
- **WHEN** the user's Telegram client is in dark mode
- **THEN** the Mini App renders with dark theme colors matching Telegram's dark palette

#### Scenario: Light mode
- **WHEN** the user's Telegram client is in light mode
- **THEN** the Mini App renders with light theme colors matching Telegram's light palette

### Requirement: Mantine UI for modern interface
The Mini App SHALL use Mantine UI Kit for all interface components (tabs, buttons, selects, notifications) to ensure a modern, polished appearance.

#### Scenario: UI consistency
- **WHEN** any component is rendered
- **THEN** it uses Mantine components with consistent styling throughout the application
